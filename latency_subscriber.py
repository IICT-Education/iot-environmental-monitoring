# latency_subscriber.py
import json, time, csv, os
from datetime import datetime, timezone
import paho.mqtt.client as mqtt

CSV_PATH = os.getenv("LAT_CSV", "latency_log.csv")

class Stats:
    def __init__(self):
        self.count=0; self.sum_ms=0.0; self.max_ms=0.0
    def add(self, ms):
        self.count += 1
        self.sum_ms += ms
        self.max_ms = max(self.max_ms, ms)
    def avg(self): return (self.sum_ms/self.count) if self.count else 0.0

stats = Stats()
csv_file = open(CSV_PATH, "w", newline="")
writer = csv.writer(csv_file)
writer.writerow(["ts_recv_iso","topic","sensor_id","latency_ms"])

def on_message(client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
    try:
        now = datetime.now(timezone.utc)
        payload = json.loads(msg.payload.decode("utf-8"))
        sensor_id = payload.get("sensor_id","unknown")
        latency_ms = 0
        # TASK: calculate the latency of the message
        
        print(f"adding latency: {latency_ms}")
        writer.writerow([now.isoformat(), msg.topic, sensor_id, round(latency_ms,1)])
        
        # TASK: Add the latency to the stats object and print out the statistics for every 100 messages
        
    except Exception as e:
        print("latency parse error:", e)

def main():
    c = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="latency_probe")
    c.on_message = on_message
    c.connect(os.getenv("MQTT_HOST","localhost"), int(os.getenv("MQTT_PORT",1883)), 60)
    c.subscribe("city/sensors/#", qos=0)
    c.loop_forever()

if __name__ == "__main__":
    try: main()
    finally:
        csv_file.close()
