"""
load_sim.py – Scalable IoT Sensor Simulator
-------------------------------------------
Simulates many virtual environmental sensors publishing MQTT data.

Usage examples:
    python3 load_sim.py --total 50 --min-interval 2 --max-interval 10
    python3 load_sim.py --total 100 --payload-pad 200 --qos 1
"""

import argparse
import json
import random
import string
import threading
import time
from datetime import datetime, timezone
import paho.mqtt.client as mqtt

# ---------------------------------------------------------
# Sensor configuration
# ---------------------------------------------------------
SENSOR_TYPES = ["temperature", "humidity", "co2", "pm2_5", "pm10", "air"]

# ---------------------------------------------------------
# Helper: build random payload
# ---------------------------------------------------------
def generate_payload(sensor_type: str, sensor_id: str, pad: int = 0) -> dict:
    data = {
        "sensor_id": sensor_id,
        "sensor_type": sensor_type,
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="milliseconds"),
    }

    # realistic random ranges
    if sensor_type == "temperature":
        data["temperature"] = round(random.uniform(15, 35), 2)
    elif sensor_type == "humidity":
        data["humidity"] = round(random.uniform(30, 90), 2)
    elif sensor_type == "co2":
        data["co2"] = round(random.uniform(400, 1800), 1)
    elif sensor_type == "pm2_5":
        data["pm2_5"] = round(random.uniform(5, 120), 1)
    elif sensor_type == "pm10":
        data["pm10"] = round(random.uniform(10, 160), 1)
    elif sensor_type == "air":
        data["air"] = {
            "co2": round(random.uniform(400, 1800), 1),
            "pm2_5": round(random.uniform(5, 120), 1),
            "pm10": round(random.uniform(10, 160), 1)
        }

    # optional payload padding to simulate larger messages
    if pad > 0:
        data["pad"] = "".join(random.choices(string.ascii_letters, k=pad))

    return data


# ---------------------------------------------------------
# Delay Simulation
# ---------------------------------------------------------
def delay(delay_mean=0.0, delay_jitter=0.0) -> float:
    # TASK: Create a uniformly distributed delay using the function `def delay(delay_mean=0.0, delay_jitter=0.0):``
    pass

# ---------------------------------------------------------
# Loss Simulation
# ---------------------------------------------------------
def loss(loss_rate=0.0) -> bool:
    """return 1 if packet is to be dropped"""
    # TASK: Randomly drop a packet base on loss_rate - consider the loss_rate as the thresgold
    pass

# ---------------------------------------------------------
# Worker thread: one simulated sensor
# ---------------------------------------------------------
def sensor_thread(
    broker: str,
    port: int,
    sensor_type: str,
    sensor_id: str,
    interval_s: float,
    qos: int,
    payload_pad: int,
    delay_mean: float = 0.0,
    delay_jitter: float = 0.0,
    loss_rate: float = 0.0
):
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=f"pub_{sensor_id}")
    try:
        client.connect(broker, port, keepalive=60)
        client.loop_start()
        topic = f"city/sensors/{sensor_type}/data"
        while True:
            used_delay = 0
            payload = generate_payload(sensor_type, sensor_id, pad=payload_pad)
            if loss(loss_rate):
                print(f"[LOSS] Dropped packet for {topic}")
            else:
                used_delay = delay(delay_mean, delay_jitter)
                client.publish(topic, json.dumps(payload), qos=qos, retain=False)
            time.sleep(interval_s-used_delay)

    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"[{sensor_id}] error: {e}")
    finally:
        client.loop_stop()
        client.disconnect()


# ---------------------------------------------------------
# Main entry point
# ---------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Scalable MQTT sensor simulator")
    parser.add_argument("--host", default="localhost", help="MQTT broker host")
    parser.add_argument("--port", type=int, default=1883, help="MQTT broker port")
    parser.add_argument("--total", type=int, default=50, help="Total number of sensors")
    parser.add_argument("--min-interval", type=float, default=2.0, help="Shortest send interval (s)")
    parser.add_argument("--max-interval", type=float, default=10.0, help="Longest send interval (s)")
    parser.add_argument("--qos", type=int, default=0, choices=[0, 1], help="MQTT QoS level")
    parser.add_argument("--delay-mean", type=float, default=0.0, help="Average artificial delay before publishing (seconds)")
    parser.add_argument("--delay-jitter", type=float, default=0.0, help="Random jitter added/subtracted from delay_mean (seconds)")
    parser.add_argument("--loss-rate", type=float, default=0.0, help="Rate at which packets are to be dropped (value between 0 and 1)")
    parser.add_argument("--payload-pad", type=int, default=0, help="Extra characters in payload")
    args = parser.parse_args()

    threads = []
    # TASK: Start new sensor threads based on the arguments supplied - use a uniform distributed interval
    
    print(
        f"Started {len(threads)} simulated sensors "
        f"(broker: {args.host}:{args.port}, QoS={args.qos})"
    )

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        print("Simulation stopped.")


if __name__ == "__main__":
    main()
