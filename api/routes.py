from . import get_session, get_settings
from fastapi import APIRouter, status, Depends
from typing import Annotated

from .models import *
from .config import Settings

router = APIRouter(
    tags=["status"]
)




@router.get("/status", description="simple heath check endpoint", response_model=Status)
async def get_status() -> Status:
    return Status(
        status="ok"
    )


@router.get("/health", description="heath endpoint giving more metrics", response_model=Health)
async def get_health(settings: Annotated[Settings, Depends(get_settings)]) -> Health:
    return Health(
        status="ok",
        db_url = settings.db_url,
        debug_level = settings.debug_level,
        issuer = settings.issuer,
        expire_time = settings.expire_time
    )