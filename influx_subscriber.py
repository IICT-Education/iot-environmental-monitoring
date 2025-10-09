"""
influx_subscriber.py
--------------------
Subscribes to MQTT sensor topics and writes parsed data into InfluxDB.

Assumes topic pattern:
    city/sensors/<sensor-type>/data

Supported fields in payload:
    pm2_5, pm10, co2, temperature, humidity
"""

import os
import json
import time
from datetime import datetime, timezone
from dotenv import load_dotenv
import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# ---------------------------------------------------------------------
# Load environment variables
# ---------------------------------------------------------------------
# TASK: Create a respective .env file to store the environmental variables
load_dotenv()

MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "city/sensors/#")

INFLUX_URL = os.getenv("INFLUX_URL", "http://localhost:8086")
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN", "admin123")
INFLUX_ORG = os.getenv("INFLUX_ORG", "city-lab")
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET", "sensors")

# ---------------------------------------------------------------------
# Initialize InfluxDB client
# ---------------------------------------------------------------------
client_influx = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
write_api = client_influx.write_api(write_options=SYNCHRONOUS)


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------
# TASK: Create a function that returns "nan" values if values are non-existent


# ---------------------------------------------------------------------
# MQTT callbacks
# ---------------------------------------------------------------------
def on_connect(client: mqtt.Client, userdata, flags, rc, properties):
    if rc == 0:
        print(f"Connected to MQTT broker {MQTT_HOST}:{MQTT_PORT}")
        client.subscribe(MQTT_TOPIC)
        print(f"Subscribed to topic pattern: {MQTT_TOPIC}")
    else:
        print(f"Connection failed with code {rc}")

def on_message(client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
    try:
        payload: dict = json.loads(msg.payload.decode("utf-8"))
        topic_parts = msg.topic.split("/")
        if len(topic_parts) < 3:
            print(f"Skipping malformed topic: {msg.topic}")
            return
        sensor_type = topic_parts[2]
        sensor_id = payload.get("sensor_id", sensor_type)
        timestamp = payload.get("timestamp", datetime.now(timezone.utc).isoformat(timespec='seconds'))

        # TASK: Build the Influx point with all the sensor elements - use sensor_type and sensor_id as tags
        

        #TASK: Write the data point to the database
        

        print(f"Inserted data for {sensor_id} ({sensor_type}) at {timestamp}")

    except json.JSONDecodeError:
        print(f"Invalid JSON received: {msg.payload}")
    except Exception as e:
        print(f"Error processing message: {e}")

# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------
if __name__ == "__main__":
    client_mqtt = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="influx_subscriber")
    client_mqtt.on_connect = on_connect
    client_mqtt.on_message = on_message

    print(f"Connecting to MQTT broker {MQTT_HOST}:{MQTT_PORT} ...")
    client_mqtt.connect(MQTT_HOST, MQTT_PORT, keepalive=60)

    try:
        client_mqtt.loop_forever()
    except KeyboardInterrupt:
        print("\nSubscriber stopped by user.")
    finally:
        write_api.__del__()
        client_influx.close()
