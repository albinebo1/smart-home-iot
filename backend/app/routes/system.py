from fastapi import APIRouter
from app.schemas.system import SystemMode
from app.schemas.overview import SystemOverview
from app.services.system_service import get_system_mode, get_system_overview

router = APIRouter()


@router.get("/api/system/mode", response_model=SystemMode)
def system_mode():
    return get_system_mode()

@router.get("/api/system/overview", response_model=SystemOverview)
def system_overview():
    return get_system_overview()