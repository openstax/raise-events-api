import os
from starlette.requests import Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from fastapi import HTTPException
from jose import jwt, JWTError


def get_userdata(request: Request) -> str:
    return request.state.userdata


class JWTBearer(HTTPBearer):
    def __init__():
        return

    async def __call__(
        self,
        request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        credentials: HTTPAuthorizationCredentials = \
            await super().__call__(request)
        
        token = credentials.credentials

        token_claims = await self.get_verified_claims(token)

        request.state.userdata = token_claims.get("uuid")

    def get_verified_claims(self, token):
        try:
            unverified_headers = jwt.get_unverified_headers(token)
        except JWTError as error:
            raise HTTPException(
                status_code=403,
                detail=str(error)
            )
        
        kid = unverified_headers.get("kid")

        secret_map = os.environ['SECRETS_MAP']
        secret = None
        for item in secret_map:
            if item["kid"] == kid:
                secret = item["secret"]
                break
        if secret == None:
            raise HTTPException(
                status_code=403,
                detail="Invalid kid value in token"
            )

        verified_claims = self.verify_token(token, secret)
    
        return verified_claims
        
    def verify_token(self, token, secret):
        try:
            verified_claims = jwt.decode(token, secret)
        except JWTError as error:
            raise HTTPException(
                status_code=403,
                detail=str(error)
            )
        return verified_claims
