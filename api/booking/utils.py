from .models import *
from sqlmodel import Session, select


def get_booking(session: Session, booking_id: UUID4, user_id: UUID4):
    return session.exec(select(Booking).where(Booking.id == booking_id).where(Booking.user_id == user_id)).first()
