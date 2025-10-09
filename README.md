# Project: IoT-based Smart Environmental Monitoring

## Problem Statement
You are working for a smart city project tasked with deploying an air quality monitoring system across multiple urban districts.
The system must be low-cost, low-power, and scalable to hundreds of sensors. Cellular IoT would be too expensive; Wi-Fi has insufficient coverage.
Your task is to prototype a solution using LPWAN technologies that balances coverage, power consumption, and data delivery. 

## Prerequisites
To run this lab locally, you need:
- **Python 3.10+** – for running the sensor simulation and subscriber scripts  
  → [Official installation guide](https://www.python.org/downloads/)
- **Docker & Docker Compose** – for containerized setup of Mosquitto, InfluxDB, and Grafana  
  → [Docker installation guide](https://docs.docker.com/get-docker/)

> 💡 *Alternatively*, you can use the preconfigured **Virtual Machine** provided with the lab,  
> which already includes Python, Docker, and all required tools.  
> This option is recommended if you want a consistent environment across exercises.

## Getting Started
Create a virtual environment, activate it and install the requirements
```
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

## Tasks - Sprint 1 - Network and Broker Setup

**Goal:**  
Establish the MQTT communication layer and implement a basic sensor simulation.

**Main Tasks**
1. **Set up the MQTT Broker**  
   - Start a local or Docker-based Mosquitto broker.  
   - Verify it listens on port 1883 and accepts connections.

2. **Create Sensor Simulation**  
   - Write `sensor_sim.py` to publish temperature data using a uniform distribution.  
   - Include basic parameters (e.g., update interval, topic name).  

3. **Implement Console Subscriber**  
   - Subscribe to `city/sensors/<sensor-type>/data`.  
   - Print incoming messages with timestamps and sensor type information.  

4. **Extend for Multiple Sensor Types**  
   - Add functions for `temperature`, `humidity`, `CO₂`, `PM₂․₅`, and `PM₁₀`.  
   - Each sensor runs in its own thread with individual intervals and IDs.  

5. **Test and Validate Data Flow**  
   - Run the simulation and subscriber concurrently.  
   - Confirm that different sensor types publish to the correct topics and payloads.

**Expected Outcome:**  
A working MQTT data pipeline that publishes sensor readings to `city/sensors/<sensor-type>/data` and displays them on the subscriber console.


## Authors and Acknowledgment
IICT - International IoT Communication Technologies GmbH

## License
Please see the LICENSE file for more details
