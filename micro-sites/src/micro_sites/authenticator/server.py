from bareasgi import Application
from bareasgi_cors import CORSMiddleware
import bareasgi_jinja2
from easydict import EasyDict as edict
import jinja2
import logging.config
import pkg_resources
import os
import uvicorn
import yaml
from micro_sites.utils.yaml_types import initialise_types
from .auth_controller import AuthController
from .auth_service import AuthService
from micro_sites.utils.auth_middleware import JwtAuthenticator
from micro_sites.utils.token_manager import TokenManager


def load_config():
    initialise_types()
    with open(pkg_resources.resource_filename('micro_sites.authenticator', 'config.yaml'), 'rt') as fp:
        return edict(yaml.load(fp, Loader=yaml.FullLoader))


def make_app(config: edict) -> Application:
    templates_folder = pkg_resources.resource_filename('micro_sites.authenticator', 'templates')

    cors_middleware = CORSMiddleware()

    app = Application(middlewares=[cors_middleware])

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(templates_folder),
        autoescape=jinja2.select_autoescape(['html', 'xml']),
        enable_async=True
    )

    bareasgi_jinja2.add_jinja2(app, env)

    domain = os.path.expandvars(config.token_manager.domain)
    issuer = os.path.expandvars(config.token_manager.issuer)
    secret = os.path.expandvars(config.token_manager.secret)
    path = config.token_manager.path
    token_expiry = config.token_manager.token_expiry
    cookie_name = config.token_manager.cookie_name
    max_age = config.token_manager.max_age

    auth_service = AuthService()
    token_manager = TokenManager(
        secret,
        token_expiry,
        issuer,
        cookie_name,
        domain,
        path,
        max_age
    )

    token_renewal_path = config.app.path_prefix + config.app.token_renewal_path
    authenticator = JwtAuthenticator(token_renewal_path, token_manager)

    auth_controller = AuthController(
        config.app.path_prefix,
        config.app.login_expiry,
        token_manager,
        auth_service,
        authenticator)

    auth_controller.add_routes(app)

    return app


def start_server():
    config = load_config()
    logging.config.dictConfig(config.logging)
    app = make_app(config)
    uvicorn.run(app, port=config.app.port)
