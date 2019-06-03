from bareasgi import Application
from bareasgi_cors import CORSMiddleware
from bareutils import json_response, response_code
from easydict import EasyDict as edict
import logging.config
import os
import pkg_resources
import uvicorn
import yaml
from ..utils.auth_middleware import JwtAuthenticator
from ..utils.token_manager import TokenManager
from ..utils.yaml_types import initialise_types


async def get_sites(scope, info, matches, content):
    return json_response(
        response_code.OK,
        None,
        [
            {
                'code': 'site1',
                'title': 'Site1',
                'description': 'This first site',
                'url': '/micro-site/site1/ui/page1',
                'icon': 'dashboard'
            },
            {
                'code': 'site2',
                'title': 'Site2',
                'description': 'The second site',
                'url': '/micro-site/site2/ui/page1',
                'icon': 'flight_takeoff'
            },
        ]
    )


def load_config():
    initialise_types()
    with open(pkg_resources.resource_filename(__name__, 'config.yaml'), 'rt') as fp:
        return edict(yaml.load(fp, Loader=yaml.FullLoader))


def start_server():
    config = load_config()
    logging.config.dictConfig(config.logging)

    token_manager = TokenManager(
        config.token_manager.secret,
        config.token_manager.token_expiry,
        os.path.expandvars(config.token_manager.issuer),
        config.token_manager.cookie_name,
        os.path.expandvars(config.token_manager.domain),
        config.token_manager.path,
        config.token_manager.max_age
    )

    authenticator = JwtAuthenticator(
        config.app.token_renewal_path,
        token_manager
    )

    cors_middleware = CORSMiddleware()

    app = Application(middlewares=[cors_middleware, authenticator])
    app.http_router.add({'GET'}, config.app.path_prefix + '/sites', get_sites)

    uvicorn.run(app, port=config.app.port)
