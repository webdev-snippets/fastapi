
import uuid
from sqlmodel import SQLModel, Field, Column
from pydantic import UUID4, EmailStr
from typing import Optional

class BaseUser(SQLModel):
    username: str = Field(index=True)
    email: EmailStr

class User(BaseUser, table=True):
    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)
    password: str

class CreateUser(BaseUser):
    password: str

class PublicUser(BaseUser):
    id: UUID4

class UpdateUser(SQLModel):
    username: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
