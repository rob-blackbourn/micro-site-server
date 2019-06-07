from bareasgi import (
    Application,
    Scope,
    Info,
    RouteMatches,
    Content,
    HttpResponse,
    text_response,
    text_reader,
    json_response
)
import bareutils.header as header
from bareutils import response_code
from bareasgi.middleware import mw
import bareasgi_jinja2
from datetime import datetime, timedelta
import jwt
import logging
from typing import Mapping, Any
from urllib.parse import parse_qs, urlparse
from .auth_service import AuthService
from micro_services.utils.auth_middleware import JwtAuthenticator
from micro_services.utils.token_manager import TokenManager

logger = logging.getLogger(__name__)


class HTTPUnauthorized(Exception):
    pass


class HTTPForbidden(Exception):
    pass


# noinspection PyUnusedLocal
class AuthController:

    def __init__(
            self,
            path_prefix: str,
            login_expiry: timedelta,
            token_manager: TokenManager,
            auth_service: AuthService,
            authenticator: JwtAuthenticator
    ) -> None:
        self.path_prefix = path_prefix
        self.login_expiry = login_expiry
        self.token_manager = token_manager
        self.auth_service = auth_service
        self.authenticator = authenticator

    def add_routes(self, app: Application) -> Application:
        app.http_router.add({'GET'}, self.path_prefix + '/login', self.login_view)
        app.http_router.add({'POST'}, self.path_prefix + '/login', self.login_post)
        app.http_router.add({'GET'}, self.path_prefix + '/register', self.register_view)
        app.http_router.add({'POST'}, self.path_prefix + '/register', self.register_post)
        app.http_router.add({'POST'}, self.path_prefix + '/renew_token', self.renew_token)

        app.http_router.add(
            {'GET'},
            self.path_prefix + '/whoami',
            mw(self.authenticator, handler=self.who_am_i))

        return app

    @bareasgi_jinja2.template('login.html')
    async def login_view(self, scope: Scope, info: Info, matches: RouteMatches, content: Content) -> Mapping[str, Any]:
        query_string = scope["query_string"].decode()
        action = f'{self.path_prefix}/login?{query_string}'
        register = f'{self.path_prefix}/register?{query_string}'
        return {
            'action': action,
            'register': register
        }

    async def login_post(self, scope: Scope, info: Info, matches: RouteMatches, content: Content) -> HttpResponse:
        try:
            query = parse_qs(scope['query_string'])
            redirect = query.get(b'redirect')
            if not redirect:
                logger.debug('No redirect')
                return text_response(response_code.NOT_FOUND, None, 'No redirect')
            redirect = redirect[0]

            text = await text_reader(content)
            body = parse_qs(text)
            username = body['username'][0]
            password = body['password'][0]

            if not await self.auth_service.is_password_for_user(username, password):
                raise RuntimeError('Invalid username or password')

            now = datetime.utcnow()
            token = self.token_manager.encode(username, now, now)

            logger.debug(f'Sending token: {token}')
            urlparts = urlparse(redirect)
            if urlparts.scheme is None or len(urlparts.scheme) == 0:
                raise RuntimeError('The redirect URL has no scheme')

            set_cookie = self.token_manager.make_cookie(token)

            return response_code.FOUND, [(b'set-cookie', set_cookie), (b'location', redirect)], None

        except:
            logger.exception('Failed to log in')
            return response_code.FOUND, [(b'location', header.find(b'referer', scope['headers']))], None

    @bareasgi_jinja2.template('register.html')
    async def register_view(self, scope: Scope, info: Info, matches: RouteMatches, content: Content) -> Mapping[
        str, Any]:
        query_string = scope["query_string"].decode()
        action = f'{self.path_prefix}/register?{query_string}'
        login = f'{self.path_prefix}/login?{query_string}'
        return {
            'action': action,
            'login': login
        }

    async def register_post(self, scope: Scope, info: Info, matches: RouteMatches, content: Content) -> HttpResponse:
        try:
            query = parse_qs(scope['query_string'])
            redirect = query.get(b'redirect')
            if not redirect:
                logger.debug('No redirect')
                return text_response(response_code.NOT_FOUND, None, 'No redirect')
            redirect = redirect[0]

            text = await text_reader(content)
            body = parse_qs(text)
            username = body['username'][0]
            password = body['password'][0]

            if not await self.auth_service.register(username, password):
                raise RuntimeError('Failed to register user')

            now = datetime.utcnow()
            token = self.token_manager.encode(username, now, now)

            logger.debug(f'Sending token: {token}')
            urlparts = urlparse(redirect)
            if urlparts.scheme is None or len(urlparts.scheme) == 0:
                raise RuntimeError('The redirect URL has no scheme')

            set_cookie = self.token_manager.make_cookie(token)

            return response_code.FOUND, [(b'set-cookie', set_cookie), (b'location', redirect)], None

        except:
            logger.exception('Failed to log in')
            return response_code.FOUND, [(b'location', header.find(b'referer', scope['headers']))], None

    async def who_am_i(self, scope: Scope, info: Info, matches: RouteMatches, content: Content) -> HttpResponse:
        try:
            token = self.token_manager.get_token_from_headers(scope['headers'])
            if token is None:
                return text_response(401, [], 'Client requires authentication')

            payload = self.token_manager.decode(token)

            return json_response(response_code.OK, [], {'username': payload['sub']})
        except (jwt.exceptions.ExpiredSignature, PermissionError) as error:
            logger.debug(f'JWT encoding failed: {error}')
            return response_code.UNAUTHORIZED, None, None
        except:
            logger.exception(f'Failed to re-sign the token')
            return response_code.INTERNAL_SERVER_ERROR, None, None

    async def renew_token(self, scope: Scope, info: Info, matches: RouteMatches, content: Content) -> HttpResponse:
        try:
            token = self.token_manager.get_token_from_headers(scope['headers'])
            if not token:
                # Unauthorised
                return text_response(response_code.UNAUTHORIZED, None, 'Client requires authentication')

            payload = self.token_manager.decode(token)

            user = payload['sub']
            issued_at = payload['iat']

            logger.debug(f'Token renewal request: user={user}, iat={issued_at}')

            utc_now = datetime.utcnow()

            authentication_expiry = issued_at + self.login_expiry
            if utc_now > authentication_expiry:
                logger.debug(f'Token expired for user {user} issued at {issued_at} expired at {authentication_expiry}')
                return text_response(response_code.UNAUTHORIZED, None, 'Authentication expired')

            if not self.auth_service.is_valid(user):
                return response_code.FORBIDDEN, None, None

            logger.debug(f'Token renewed for {user}')
            token = self.token_manager.encode(user, utc_now, issued_at)
            logger.debug(f'Sending token {token}')

            set_cookie = self.token_manager.make_cookie(token)

            return response_code.NO_CONTENT, [(b'set-cookie', set_cookie)], None

        except:
            logger.exception('Failed to renew token')
            return response_code.INTERNAL_SERVER_ERROR, None, None
