from bareasgi import Application
from bareasgi_cors import CORSMiddleware
from bareutils import json_response, response_code
from easydict import EasyDict as edict
import logging
import logging.config
import os
import pkg_resources
import uvicorn
import yaml
from ..utils.auth_middleware import JwtAuthenticator
from ..utils.token_manager import TokenManager
from ..utils.yaml_types import initialise_types

logger = logging.getLogger(__name__)


def load_config():
    initialise_types()
    with open(pkg_resources.resource_filename(__name__, 'config.yaml'), 'rt') as fp:
        return edict(yaml.load(fp, Loader=yaml.FullLoader))


# noinspection PyUnusedLocal
async def get_info1(scope, info, matches, content):
    try:
        logger.info('GET site1 info1')
        return json_response(response_code.OK, None, {'message': 'Site 1 Info 1'})
    except:
        logger.exception('Failed to get info')
        return response_code.INTERNAL_SERVER_ERROR, None, None


# noinspection PyUnusedLocal
async def get_info2(scope, info, matches, content):
    try:
        logger.info('GET site1 info2')
        return json_response(response_code.OK, None, {'message': 'Site 1 Info 2'})
    except:
        logger.exception('Failed to get info')
        return response_code.INTERNAL_SERVER_ERROR, None, None


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
    app.http_router.add({'GET'}, config.app.path_prefix + '/info1', get_info1)
    app.http_router.add({'GET'}, config.app.path_prefix + '/info2', get_info2)

    uvicorn.run(app, port=config.app.port)
