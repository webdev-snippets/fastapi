from sqlmodel import Session, select
from datetime import timedelta, datetime, timezone
from argon2 import PasswordHasher
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
import jwt
import uuid

from ..user.models import User
from .models import *
from ..user.utils import hash_password
from .. import get_settings, get_session, SCOPES
ph = PasswordHasher()

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/token", scopes=SCOPES)



async def authenticate_user(s: Session, username: str, password: str) -> User:
    user = s.exec(select(User).where(User.username == username)).first()
    if not user:
        return False
    if not await verify_password(s, password, user.password):
        return False
    return user


async def verify_password(s: Session, ptxt: str, ctxt: str) -> bool:
    if ph.verify(ctxt, ptxt):
        if ph.check_needs_rehash(ctxt):
            user: User = s.exec(select(User).where(User.password == ctxt))
            user.password = hash_password(ptxt)
        return True
    return False

def verify_scopes(requested_scopes: list, allowed_scopes: dict) -> str:
    allowed_scopes: list = allowed_scopes.keys()
    scopes: list = []

    for scope in requested_scopes:
        if scope in allowed_scopes:
            scopes.append(scope)
    
    return ' '.join(scopes)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire,
    "iss": get_settings().issuer
    })
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: Annotated[str, Depends(oauth2_scheme)], security_scopes: SecurityScopes,session: Annotated[Session, Depends(get_session)]) -> User:
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = uuid.UUID(payload.get("sub"))
        issuer = payload.get('iss')
        scopes = str(payload.get('scopes')) # have to type cast to string otherwise validation errors
        if user_id is None:
            raise credentials_exception
        if issuer is None:
            raise credentials_exception
        if issuer != get_settings().issuer:
            raise credentials_exception
        token_data = TokenData(user_id=user_id,scopes=[scopes])
        user: User = session.get(User, user_id)
        if user is None:
            raise credentials_exception
        print(str(token_data.scopes))
        for scope in security_scopes.scopes:
            print(scope)
            if scope not in token_data.scopes[0]:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not enough permissions",
                    headers={"WWW-Authenticate": authenticate_value},
                )
    except jwt.InvalidTokenError:
        raise credentials_exception
    return user