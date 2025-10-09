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
        # TASK: Publish the serialized JSON-message to the Broker using QoS Level 0


        # TASK: Print the published message to the console if it has been published successfuly


# TASK: Create funtions that publish humidity and air-quality data


# ---------------------------------------------------------------------
# THREAD STARTUP
# ---------------------------------------------------------------------
if __name__ == "__main__":
    # TASK: add remaining sensor types (hum_<id>, air_<id>) with sending interval and respective functions to the sensor list
    sensors = [
        ("temp_01", 5, publish_temperature)
    ]

    for sensor_id, interval, func in sensors:
        t = threading.Thread(target=func, args=(sensor_id, interval), daemon=True)
        t.start()

    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("\nSimulation stopped by user.")
        client.disconnect()
