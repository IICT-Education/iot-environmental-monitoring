"""
console_subscriber.py
---------------------
Subscribes to all sensor topics and prints formatted output to the console.
Automatically identifies the sensor type based on the MQTT topic.
"""

import json
import paho.mqtt.client as mqtt

# ---------------------------------------------------------------------
# MQTT CONFIGURATION
# ---------------------------------------------------------------------
BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC = "city/sensors/#"    # subscribe to all sensors

# ---------------------------------------------------------------------
# CALLBACKS
# ---------------------------------------------------------------------
def on_connect(client: mqtt.Client, userdata, flags, rc, properties):
    if rc == 0:
        print(f"Connected to broker at {BROKER_HOST}:{BROKER_PORT}")
        client.subscribe(TOPIC)
        print(f"Subscribed to topic pattern: {TOPIC}")
    else:
        print(f"Connection failed with code {rc}")

def on_message(client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
    try:
        payload: dict = json.loads(msg.payload.decode("utf-8"))
        sensor_id = payload.get("sensor_id", "unknown")
        topic_parts = msg.topic.split("/")
        sensor_type = topic_parts[2] if len(topic_parts) > 2 else "unknown"

        print("\n--- New Message ---")
        print(f"Topic:       {msg.topic}")
        print(f"Sensor Type: {sensor_type}")
        print(f"Sensor ID:   {sensor_id}")
        print(f"Timestamp:   {payload.get('timestamp', 'n/a')}")

        if sensor_type.startswith("temp"):
            print(f"Temperature: {payload.get('temperature', 'n/a')} °C")

        elif sensor_type.startswith("hum"):
            print(f"Humidity:    {payload.get('humidity', 'n/a')} %")

        elif sensor_type.startswith("air"):
            print(f"PM2.5:       {payload.get('pm2_5', 'n/a')} µg/m³")
            print(f"PM10:        {payload.get('pm10', 'n/a')} µg/m³")
            print(f"CO2:         {payload.get('co2', 'n/a')} ppm")
            print(f"Temp:        {payload.get('temperature', 'n/a')} °C")
            print(f"Humidity:    {payload.get('humidity', 'n/a')} %")

        else:
            print("Payload (unrecognized sensor type):")
            print(json.dumps(payload, indent=2))

        

    except json.JSONDecodeError:
        print(f"Received invalid JSON on topic {msg.topic}: {msg.payload}")

# ---------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------
if __name__ == "__main__":
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="console_subscriber")
    client.on_connect = on_connect
    client.on_message = on_message

    print(f"Connecting to broker {BROKER_HOST}:{BROKER_PORT} ...")
    client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)

    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("\nSubscriber stopped by user.")
        client.disconnect()
