from bareasgi import (
    Scope,
    Header,
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
from typing import List, Optional
from .token_manager import TokenManager

logger = logging.getLogger(__name__)


class JwtAuthenticator:

    def __init__(
            self,
            token_renewal_path: str,
            token_manager: TokenManager
    ) -> None:
        self.token_renewal_path = token_renewal_path
        self.token_manager = token_manager

    async def _renew_cookie(self, scope: Scope, token: bytes) -> Optional[bytes]:
        scope_server_host, scope_server_port = scope['server']

        scheme = header.find(b'x-forwarded-proto', scope['headers'], scope['scheme'].encode()).decode()
        host = header.find(b'x-forwarded-host', scope['headers'], scope_server_host.encode()).decode()
        port = int(header.find(b'x-forwarded-port', scope['headers'], str(scope_server_port).encode()).decode())

        renewal_url = f'{scheme}://{host}{self.token_renewal_path}'
        url = f'{scheme}://{host}:{port}{scope["path"]}'
        referer = header.find(b'referer', scope['headers'], url.encode('ascii'))

        headers: List[Header] = [
            (b'host', host.encode()),
            (b'referer', referer),
            (b'content-length', b'0'),
            (b'connection', b'close')
        ]
        if token is not None:
            cookie = self.token_manager.cookie_name + b'=' + token
            headers.append((b'cookie', cookie))

        ssl_context = ssl.SSLContext() if scheme == 'https' else None

        logger.debug(f'Renewing cookie at {renewal_url} with headers {headers}')
        async with HttpClient(renewal_url, method='POST', headers=headers, ssl=ssl_context) as (response, body):

            if response.status_code == response_code.NO_CONTENT:
                logger.debug('Cookie renewed')
                set_cookies = header.set_cookie(response.headers).get(self.token_manager.cookie_name)
                if set_cookies is None:
                    raise RuntimeError('No cookie returned')
                kwargs = set_cookies[0]
                set_cookie = encode_set_cookie(**kwargs)
                return set_cookie
            elif response.status_code == response_code.UNAUTHORIZED:
                logger.debug('Cookie not renewed - client requires authentication')
                return None
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
                cookie = await self._renew_cookie(scope, token)
                if cookie is None:
                    return response_code.UNAUTHORIZED, None, None

            if info is None:
                info = dict()
            info['jwt'] = payload

            next_status, next_headers, next_content = await handler(scope, info, matches, content)

            if cookie:
                if next_headers is None:
                    next_headers = []
                next_headers.append((b"set-cookie", cookie))

            return next_status, next_headers, next_content

        except:
            logger.exception("JWT authentication failed")
            return response_code.INTERNAL_SERVER_ERROR, None, None
