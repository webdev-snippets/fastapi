import uuid
from sqlmodel import SQLModel, Field, String
from pydantic import UUID4
from typing import Optional, Literal


class BaseBooking(SQLModel):
    time: str
    location: str
    notes: str | None = None
    booking_type: Literal["installation", "consulation"] = Field(
        index=True, sa_type=String)


class Booking(BaseBooking, table=True):
    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: UUID4 = Field(foreign_key="user.id")


class CreateBooking(BaseBooking):
    pass


class PublicBooking(BaseBooking):
    id: UUID4


class UpdateBooking(SQLModel):
    time: Optional[str]
    location: Optional[str]
    notes: Optional[str]
