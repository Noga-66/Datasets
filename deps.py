import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from backend.core.security import decode_token

bearer = HTTPBearer()


def current_user(cred: HTTPAuthorizationCredentials = Depends(bearer)) -> dict:
    try:
        return decode_token(cred.credentials)
    except jwt.PyJWTError:
        raise HTTPException(401, "invalid or expired token")


def require_role(*roles: str):
    def dep(user: dict = Depends(current_user)) -> dict:
        if user["role"] not in roles:
            raise HTTPException(403, "forbidden for this role")
        return user
    return dep
