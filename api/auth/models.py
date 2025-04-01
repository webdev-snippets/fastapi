from sqlmodel import SQLModel
from pydantic import UUID4

class Token(SQLModel):
    access_token: str
    token_type: str

class TokenData(SQLModel):
    user_id: UUID4 | None = None
    scopes: list[str] = []
