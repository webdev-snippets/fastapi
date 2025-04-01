from fastapi import Depends, Security, status, HTTPException, APIRouter
from typing import Annotated
from sqlmodel import Session
from pydantic import ValidationError

from .. import get_session, get_settings, Settings
from ..auth.utils import verify_token
from .models import *
from .utils import *


router = APIRouter(
    tags=["user"],
    prefix="/user"
)

@router.post("", response_model=PublicUser, description="Create user", status_code=status.HTTP_201_CREATED)
async def post_user(*, new_user: CreateUser, s: Annotated[Session, Depends(get_session)], settings: Annotated[Settings, Depends(get_settings)]):
    try:
        new_user = User.model_validate(new_user, update={"password": hash_password(new_user.password)})
        s.add(new_user)
        s.commit()
        s.refresh(new_user)
        return new_user
    except ValidationError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    

@router.patch("", response_model=PublicUser, description="Update user", status_code=status.HTTP_200_OK)
async def update_user(*, update_user: UpdateUser, s: Annotated[Session, Depends(get_session)], settings: Annotated[Settings, Depends(get_settings)], user: Annotated[User, Security(verify_token, scopes=["user", "user:write"])]):
    try:
        db_user: User = s.get(User, user.id)
        update_user: User = User.model_validate(update_user, update={"password": hash_password(update_user.password)})
        db_user = db_user.sqlmodel_update(update_user)
        s.add(db_user)
        s.commit()
        s.refresh(db_user)
        return db_user
    except ValidationError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

@router.get("", response_model=PublicUser, description="get user", status_code=status.HTTP_200_OK)
async def update_user(*,s: Annotated[Session, Depends(get_session)], settings: Annotated[Settings, Depends(get_settings)], user: Annotated[User, Security(verify_token, scopes=["user"])]):
    try:
        return s.get(User, user.id)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.delete("", description="delete user", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(*,s: Annotated[Session, Depends(get_session)], user: Annotated[User, Security(verify_token, scopes=["user", "user:write", "user:delete"])]):
    try:
        u = s.get(User, user.id)
        s.delete(u)
        s.commit()
        return
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User doesn't exists")
