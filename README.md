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

## Tasks - Sprint 2

1. Set up Docker Compose

- Add services for Mosquitto + InfluxDB
- Verify both containers run and are reachable.

2. Adjust Publisher & Subscriber
- Update environment variables (.env) for host, port, and topic.

3. Implement InfluxDB Subscriber
- Parse incoming MQTT messages.
- Write sensor values (PM₂․₅, PM₁₀, CO₂, Temperature, Humidity) into InfluxDB.

4. Verify Data Flow
- Start the simulation → confirm points appear in InfluxDB (influx query or UI).
- Check correct timestamps and sensor tags.

### Expected Outcome
Running `docker compose up -d` starts the full backend.

## Authors and Acknowledgment
IICT - International IoT Communication Technologies GmbH

## License
Please see the LICENSE file for more details
