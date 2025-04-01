from fastapi import Depends, Security, status, HTTPException, APIRouter
from typing import Annotated
from sqlmodel import Session
from pydantic import ValidationError

from .. import get_session, get_settings, Settings
from ..user.models import User
from ..auth.utils import verify_token
from .models import *
from .utils import *


router = APIRouter(
    tags=["booking"],
    prefix="/booking"
)


@router.post("", response_model=PublicBooking, description="Create booking", status_code=status.HTTP_201_CREATED)
async def post_booking(*, new_booking: CreateBooking, s: Annotated[Session, Depends(get_session)], settings: Annotated[Settings, Depends(get_settings)], user: Annotated[User, Security(verify_token, scopes=["booking", "booking:write"])]):
    try:
        new_booking = Booking.model_validate(
            new_booking, update={"user_id": user.id})
        s.add(new_booking)
        s.commit()
        s.refresh(new_booking)
        return new_booking
    except ValidationError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.patch("/{booking_id}", response_model=PublicBooking, description="Update a users booking", status_code=status.HTTP_200_OK)
async def update_booking(*, booking_id: UUID4, update_booking: UpdateBooking, s: Annotated[Session, Depends(get_session)], settings: Annotated[Settings, Depends(get_settings)], user: Annotated[User, Security(verify_token, scopes=["booking", "booking:write"])]):
    try:
        db_booking: Booking = get_booking(s, booking_id, user.id)
        db_booking = db_booking.sqlmodel_update(update_booking)
        s.add(db_booking)
        s.commit()
        s.refresh(db_booking)
        return db_booking
    except ValidationError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.get("", response_model=list[PublicBooking], description="get bookings", status_code=status.HTTP_200_OK)
async def get_bookings(*, s: Annotated[Session, Depends(get_session)], settings: Annotated[Settings, Depends(get_settings)], user: Annotated[User, Security(verify_token, scopes=["user"])]):
    try:
        return s.exec(select(Booking).where(Booking.user_id == user.id)).all()
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.delete("/{booking_id}", description="delete booking", status_code=status.HTTP_204_NO_CONTENT)
async def delete_booking(*, booking_id: UUID4, s: Annotated[Session, Depends(get_session)], user: Annotated[User, Security(verify_token, scopes=["user", "user:write", "user:delete"])]):
    try:
        u = s.get(Booking, booking_id)
        s.delete(u)
        s.commit()
        return
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User doesn't exists")
