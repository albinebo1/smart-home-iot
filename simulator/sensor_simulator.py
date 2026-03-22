import json
import time
import random
import paho.mqtt.client as mqtt

BROKER = "127.0.0.1"
PORT = 1883
INTERVAL_SEC = 2

ROOMS = ["livingroom", "bedroom", "kitchen", "bathroom", "hallway"]

client = mqtt.Client()
client.connect(BROKER, PORT, 60)
client.loop_start()

print("Sensor simulator running...")

def pub(room: str, sensor: str, value):
    topic = f"home/{room}/sensor/{sensor}"
    payload = {"value": value}
    client.publish(topic, json.dumps(payload))
    print(f"Published {topic}: {payload}")

while True:
    # Temperature for all rooms
    for room in ROOMS:
        temp = float(round(random.uniform(20, 30), 2))
        pub(room, "temperature", temp)

    # Bathroom humidity (demo-friendly)
    humidity = int(round(random.uniform(45, 85)))
    pub("bathroom", "humidity", humidity)

    # Motion sensors (hallway/kitchen/bathroom) - 1 means motion detected
    for room in ["hallway", "kitchen", "bathroom"]:
        motion = 1 if random.random() < 0.25 else 0  # 25% chance each cycle
        pub(room, "motion", motion)

    # Kitchen smoke (rare spike)
    smoke = 1 if random.random() < 0.5 else 0  # 3% chance spike
    pub("kitchen", "smoke", smoke)

    time.sleep(INTERVAL_SEC)