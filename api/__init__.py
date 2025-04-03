import logging
from fastapi import FastAPI
from sqlmodel import Session, create_engine, SQLModel
from functools import lru_cache

from .config import *
from .models import *


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

logger = logging.getLogger("uvicorn.error")
logger.setLevel(settings.debug_level)

engine = create_engine(f"{settings.db_url}")

SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    with Session(engine) as s:
        yield s


from .product.routes import router as product_router
from .booking.routes import router as booking_router
from .auth.routes import router as auth_router
from .user.routes import router as user_router
from .routes import router as health_router

app = FastAPI(
    debug=settings.debug_level,
)

app.include_router(health_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(booking_router)
app.include_router(product_router)
