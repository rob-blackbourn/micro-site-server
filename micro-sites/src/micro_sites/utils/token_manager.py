from bareasgi import Header
from bareutils import encode_set_cookie
import bareutils.header as header
from datetime import datetime, timedelta
import jwt
import logging
from typing import Mapping, Any, List, Optional

logger = logging.getLogger(__name__)


class TokenManager:

    def __init__(
            self,
            secret: str,
            token_expiry: timedelta,
            issuer: str,
            cookie_name: str,
            domain: str,
            path: str,
            max_age: timedelta
    ) -> None:
        self.secret = secret
        self.token_expiry = token_expiry
        self.issuer = issuer
        self.cookie_name = cookie_name.encode()
        self.domain = domain.encode()
        self.path = path.encode()
        self.max_age = max_age

    def encode(self, email: str, now: datetime, issued_at: datetime) -> bytes:
        expiry = now + self.token_expiry
        logger.debug(f"Token will expire at {expiry}")
        payload = {
            'iss': self.issuer,
            'sub': email,
            'exp': expiry,
            'iat': issued_at
        }
        return jwt.encode(payload, key=self.secret)

    def decode(self, token: bytes) -> Mapping[str, Any]:
        payload = jwt.decode(token, key=self.secret, options={'verify_exp': False})
        payload['exp'] = datetime.utcfromtimestamp(payload['exp'])
        payload['iat'] = datetime.utcfromtimestamp(payload['iat'])
        return payload

    def get_token_from_headers(self, headers: List[Header]) -> Optional[bytes]:
        tokens = header.cookie(headers).get(self.cookie_name)
        if tokens is None or len(tokens) == 0:
            return None
        if len(tokens) > 1:
            logger.warning('Multiple tokens in header - using first')
        token = tokens[0]
        return token

    def get_jwt_payload_from_headers(self, headers: List[Header]) -> Optional[Mapping[str, Any]]:
        token = self.get_token_from_headers(headers)
        payload = self.decode(token) if token is not None else None
        return payload

    def generate_cookie(self, email: str) -> bytes:
        now = datetime.utcnow()
        token = self.encode(email, now, now)
        return self.make_cookie(token)

    def make_cookie(self, token: bytes) -> bytes:
        cookie = encode_set_cookie(
            self.cookie_name,
            token,
            max_age=self.max_age,
            domain=self.domain,
            path=self.path,
            http_only=True
        )
        return cookie
