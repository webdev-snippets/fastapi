from fastapi import Depends, Security, status, HTTPException, APIRouter
from typing import Annotated
from datetime import timedelta
from sqlmodel import Session
from pydantic import ValidationError
from fastapi.security import OAuth2PasswordRequestFormStrict

from .. import get_session, get_settings, Settings, SCOPES
from .models import *
from .utils import *

router = APIRouter(
    tags=["auth"],
    prefix="/auth"
)

ACCESS_TOKEN_EXPIRE_MINUTES: int = int(get_settings().expire_time)

@router.post("/token", response_model=Token, description="generate a short  lived jwt for authentication", status_code=status.HTTP_200_OK)
async def post_token(
    form_data: Annotated[OAuth2PasswordRequestFormStrict, Depends()],
    s: Annotated[Session, Depends(get_session)],
    settings: Annotated[Settings, Depends(get_settings)]
  ):
    user: User = await authenticate_user(s, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    scopes: str = verify_scopes(form_data.scopes, SCOPES)
    token: str = create_access_token(data={
        "sub": str(user.id),
        "scopes": scopes
    }, expires_delta=access_token_expires)
    return Token(access_token=token, token_type="bearer")