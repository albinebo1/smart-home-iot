import paho.mqtt.client as mqtt

MQTT_HOST = "mqtt"
MQTT_PORT = 1883


def publish(topic: str, payload: str):
    client = mqtt.Client()

    client.connect(MQTT_HOST, MQTT_PORT, 60)

    client.publish(topic, payload)

    client.disconnect()