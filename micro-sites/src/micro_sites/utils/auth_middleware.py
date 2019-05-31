from bareasgi import (
    Scope,
    Info,
    RouteMatches,
    Content,
    HttpResponse,
    HttpRequestCallback
)
from bareutils import response_code, encode_set_cookie
import bareutils.header as header
from bareclient import HttpClient
from datetime import datetime
import logging
import ssl
from .token_manager import TokenManager

logger = logging.getLogger(__name__)


class HTTPUnauthorized(Exception):
    pass


class JwtAuthenticator:

    def __init__(
            self,
            auth_host: str,
            token_renewal_path: str,
            token_manager: TokenManager
    ) -> None:
        self.auth_host = auth_host
        self.token_renewal_path = token_renewal_path
        self.token_manager = token_manager


    async def _renew_cookie(self, scope: Scope, token: bytes) -> bytes:
        scope_server_host, scope_server_port = scope['server']

        scheme = header.find(b'x-forwarded-proto', scope['headers'], scope['scheme'].encode()).decode()
        host = header.find(b'x-forwarded-host', scope['headers'], scope_server_host.encode()).decode()
        port = int(header.find(b'x-forwarded-port', scope['headers'], str(scope_server_port).encode()).decode())

        renewal_url = f'{scheme}://{self.auth_host}{self.token_renewal_path}'
        url = f'{scheme}://{host}:{port}{scope["path"]}'
        referer = header.find(b'referer', scope['headers'], url.encode('ascii'))

        headers = [
            (b'host', self.auth_host),
            (b'referer', referer),
            (b'content-length', b'0'),
            (b'connection', b'close')
        ]
        if token is not None:
            headers.extend((b'cookie', token))

        ssl_context = ssl.SSLContext() if scheme == 'https' else None

        logger.debug(f'Renewing cookie at {renewal_url} with headers {headers}')
        async with HttpClient(renewal_url, method='POST', headers=headers, ssl=ssl_context) as (response, body):

            logger.debug(f"Renew Cookie: {renewal_url}")
            if response.status_code == response_code.OK:
                logger.debug('Cookie renewed')
                set_cookies = header.set_cookie(response.headers).get(self.token_manager.cookie_name)
                if set_cookies is None:
                    raise RuntimeError('No cookie returned')
                kwargs = set_cookies[0]
                set_cookie = encode_set_cookie(**kwargs)
                return set_cookie
            elif response.status_code == response_code.UNAUTHORIZED:
                logger.debug('Cookie not renewed - client requires authentication')
                raise HTTPUnauthorized('Client requires authentication')
            else:
                logger.debug('Cookie not renewed - failed to authenticate')
                raise Exception()


    async def __call__(
            self,
            scope: Scope,
            info: Info,
            matches: RouteMatches,
            content: Content,
            handler: HttpRequestCallback
    ) -> HttpResponse:

        logger.debug(f'Jwt Authentication Request: {scope["path"]}')

        try:
            token = self.token_manager.get_token_from_headers(scope['headers'])
            if token is None:
                return response_code.UNAUTHORIZED, None, None

            now = datetime.utcnow()

            payload = self.token_manager.decode(token)
            if payload['exp'] > now:
                logger.debug('Cookie still valid')
                cookie = None
            else:
                logger.debug('Renewing cookie')
                cookie = await self._renew_cookie(scope['headers'], token)

            if info is None:
                info = dict()
            info['jwt'] = payload

            next_status, next_headers, next_content = await handler(scope, info, matches, content)

            if cookie:
                if next_headers is None:
                    next_headers = []
                next_headers.append((b"set-cookie", cookie))

            return next_status, next_headers, next_content
        except HTTPUnauthorized:
            return response_code.UNAUTHORIZED, None, None

        except:
            logger.exception("JWT authentication failed")
            return response_code.INTERNAL_SERVER_ERROR, None, None
