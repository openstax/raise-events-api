from starlette.requests import Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from fastapi import HTTPException
from jose import jwt, JWTError


def get_user_uuid(request: Request) -> str:
    return request.state.user_uuid


class JWTBearer(HTTPBearer):
    def __init__(self, auth_keys):
        super().__init__(auto_error=True)
        self.auth_keys = auth_keys

    async def __call__(
        self,
        request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        credentials: HTTPAuthorizationCredentials = \
            await super().__call__(request)

        token = credentials.credentials
        token_claims = self.get_verified_claims(token)
        request.state.user_uuid = token_claims.get("sub")

    def get_verified_claims(self, token):
        try:
            unverified_headers = jwt.get_unverified_headers(token)
        except JWTError as error:
            raise HTTPException(
                status_code=403,
                detail=str(error)
            )
        kid = unverified_headers.get("kid")

        secret = None
        for item in self.auth_keys:
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
            options = {
                "verify_exp": True,
                "require_exp": True
            }
            verified_claims = jwt.decode(token, secret, options=options)
        except JWTError as error:
            raise HTTPException(
                status_code=403,
                detail=str(error)
            )
        return verified_claims
