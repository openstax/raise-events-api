import json
import os
from starlette.requests import Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from fastapi import HTTPException
from jose import jwt, JWTError


def get_userdata(request: Request) -> str:
    return request.state.userdata


class JWTBearer(HTTPBearer):
    def __init__(self):
        super().__init__(auto_error=True)

    async def __call__(
        self,
        request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        credentials: HTTPAuthorizationCredentials = \
            await super().__call__(request)

        token = credentials.credentials
        token_claims = self.get_verified_claims(token)
        request.state.userdata = token_claims.get("sub")

    def get_verified_claims(self, token):
        try:
            unverified_headers = jwt.get_unverified_headers(token)
        except JWTError as error:
            raise HTTPException(
                status_code=403,
                detail=str(error)
            )

        kid = unverified_headers.get("kid")
        secret_map = json.loads(os.environ['AUTH_KEYS'])

        secret = None
        for item in secret_map:
            if item["kid"] == kid:
                secret = item["secret"]
                break
        if secret is None:
            raise HTTPException(
                status_code=403,
                detail="Invalid kid value in token"
            )

        return self.verify_token(token, secret)

    def verify_token(self, token, secret):
        try:
            verified_claims = jwt.decode(token, secret, algorithms=['HS256'])
        except JWTError as error:
            raise HTTPException(
                status_code=403,
                detail=str(error)
            )
        return verified_claims
