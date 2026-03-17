from app.schemas.system import SystemMode
from app.schemas.overview import SystemOverview
from app.services.room_service import get_all_rooms

CURRENT_MODE = SystemMode(mode="Manual")


def get_system_mode() -> SystemMode:
    return CURRENT_MODE


def get_system_overview() -> SystemOverview:
    rooms = get_all_rooms()

    return SystemOverview(
        mode=CURRENT_MODE.mode,
        total_rooms=len(rooms),
        active_alerts=0,
        rooms=rooms
    )