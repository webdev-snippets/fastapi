from sqlmodel import SQLModel

class Status(SQLModel):
    status: str


class Health(Status):
    debug_level: str
    db_url: str
    issuer: str
    expire_time: int