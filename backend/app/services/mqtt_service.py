import json
import threading
import paho.mqtt.client as mqtt
import time

MQTT_HOST = "mqtt"
MQTT_PORT = 1883

ACTUATOR_STATES = {}


def _on_connect(client, userdata, flags, rc, properties=None):
    print(f"[MQTT] Connected with result code {rc}")
    client.subscribe("home/+/actuator/+/state")


def _on_message(client, userdata, msg):
    try:
        
        payload = json.loads(msg.payload.decode())
        state = payload.get("state", "UNKNOWN")

        topic_parts = msg.topic.split("/")
        room_id = topic_parts[1]
        device = topic_parts[3]

        if room_id not in ACTUATOR_STATES:
            ACTUATOR_STATES[room_id] = {}

        ACTUATOR_STATES[room_id][device] = state
        print(f"[MQTT] State update: {room_id} {device} = {state}")
        print("MQTT_STATE_RECEIVED", msg.topic, msg.payload.decode(), time.time())

    except Exception as e:
        print(f"[MQTT] Error processing message: {e}")


def start_mqtt_listener():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = _on_connect
    client.on_message = _on_message
    client.connect(MQTT_HOST, MQTT_PORT, 60)

    thread = threading.Thread(target=client.loop_forever, daemon=True)
    thread.start()


def publish(topic: str, payload: dict):
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.connect(MQTT_HOST, MQTT_PORT, 60)
    client.loop_start()

    print("MQTT_PUBLISH_SET", topic, payload, time.time())
    result = client.publish(topic, json.dumps(payload))
    result.wait_for_publish()

    client.loop_stop()
    client.disconnect()


def get_actuator_state(room_id: str, device: str) -> str:
    return ACTUATOR_STATES.get(room_id, {}).get(device, "UNKNOWN")