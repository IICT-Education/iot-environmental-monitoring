"""
sensor_sim.py
-------------
Publishes simulated temperature data to an MQTT broker using a uniform
distribution. 
Intended as the base script for Sprint 1

Usage:
    python sensor_sim.py
"""

import json
import paho.mqtt.client as mqtt
import random
import time
import threading

# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------
BROKER_HOST = "localhost"
BROKER_PORT = 1883
BASE_TOPIC = "city/sensors"

# ---------------------------------------------------------------------
# MQTT Setup
# ---------------------------------------------------------------------
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="sensor01")

def on_connect(client, userdata, flags, rc, properties):
    if rc == 0:
        print("Connected to broker.")
    else:
        print(f"Connection failed with code {rc}")

client.on_connect = on_connect
client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)


def publish_temperature(sensor_id: str, interval: int):
    sensor_type = sensor_id.split("_")[0]  # extract type from id - follow standard pattern
    while True:
        payload = {
            "sensor_id": sensor_id,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "temperature": round(random.uniform(18.0, 28.0), 2)
        }
        
        msg_info = client.publish(f"{BASE_TOPIC}/{sensor_type}/data", json.dumps(payload))

        if msg_info.is_published():
            print(f"[{sensor_id}] Published: {payload}")
            time.sleep(interval)


def publish_humidity(sensor_id: str, interval: int):
    sensor_type = sensor_id.split("_")[0]
    while True:
        payload = {
            "sensor_id": sensor_id,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "humidity": round(random.uniform(30.0, 70.0), 2)
        }
        client.publish(f"{BASE_TOPIC}/{sensor_type}/data", json.dumps(payload))
        print(f"[{sensor_id}] {payload}")
        time.sleep(interval)


def publish_air_quality(sensor_id: str, interval: int):
    sensor_type = sensor_id.split("_")[0]
    while True:
        payload = {
            "sensor_id": sensor_id,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "pm2_5": round(random.uniform(5, 40), 1),
            "pm10": round(random.uniform(10, 60), 1),
            "co2": round(random.uniform(400, 1200), 1)
        }
        client.publish(f"{BASE_TOPIC}/{sensor_type}/data", json.dumps(payload))
        print(f"[{sensor_id}] {payload}")
        time.sleep(interval)


# ---------------------------------------------------------------------
# THREAD STARTUP
# ---------------------------------------------------------------------
if __name__ == "__main__":
    # list of sensor-descriptions with sensor-id, interval, function
    sensors = [
        ("temp_01", 5, publish_temperature),
        ("hum_01", 8, publish_humidity),
        ("air_01", 12, publish_air_quality),
        ("air_02", 15, publish_air_quality),
    ]

    for sensor_id, interval, func in sensors:
        t = threading.Thread(target=func, args=(sensor_id, interval), daemon=True)
        t.start()

    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("\nSimulation stopped by user.")
        client.disconnect()
