from app.schemas.room import Room
from app.services.influx_service import query_latest_sensor
from app.services.influx_service import query_latest_sensor, query_sensor_history
from app.services.mqtt_service import publish

ROOM_IDS = [
    "livingroom",
    "bedroom",
    "kitchen",
    "bathroom",
    "hallway"
]


def build_room(room_id: str) -> Room:
    temperature = query_latest_sensor(room_id, "temperature")
    humidity = query_latest_sensor(room_id, "humidity")
    motion = query_latest_sensor(room_id, "motion")
    smoke = query_latest_sensor(room_id, "smoke")

    return Room(
        room_id=room_id,
        temperature=float(temperature) if temperature is not None else 0.0,
        humidity=int(humidity) if humidity is not None else 0,
        motion=int(motion) if motion is not None else 0,
        smoke=int(smoke) if smoke is not None else 0,
        actuators={
            "light": "UNKNOWN",
            "fan": "UNKNOWN"
        }
    )


def get_all_rooms() -> list[Room]:
    return [build_room(room_id) for room_id in ROOM_IDS]


def get_room_by_id(room_id: str) -> Room | None:
    if room_id not in ROOM_IDS:
        return None

    return build_room(room_id)

def get_room_history(room_id: str, sensor_type: str, minutes: int = 60):
    if room_id not in ROOM_IDS:
        return None

    return query_sensor_history(room_id, sensor_type, minutes)

def set_actuator(room_id: str, device: str, state: str):
    topic = f"home/{room_id}/actuator/{device}/set"

    publish(topic, state)

    return {
        "room": room_id,
        "device": device,
        "state": state
    }