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

## Sprint 3 – Dashboard & Visualization

**Goal:**  
Integrate **Grafana** with **InfluxDB** to visualize sensor data and configure alerts for key environmental parameters.

**Main Tasks**
1. **Add Grafana to Docker Compose**  
   - Extend the existing setup with a Grafana service connected to InfluxDB.  
   - Expose port `3001` and mount provisioning folders for datasources and dashboards.
   - Create a named volume `grafana-data`

2. **Create Dashboards**  
   - Design dashboards for temperature, humidity, CO₂, PM₂․₅, and PM₁₀.  
   - Use Flux queries to show live and historical data.  
   - Ensure panels are grouped per sensor type and include time filters.

3. **Configure Alerts**  
   - Add thresholds such as:  
     - CO₂ > 1000 ppm  
     - PM₂․₅ > 35 µg/m³  
     - Temperature > 35 °C  
   - Verify alerts

4. **Persist Configuration**  
   - Version-control provisioning files under `grafana/provisioning/`.  
   - Exclude Grafana runtime data (`grafana/data/`, `grafana/logs/`) in `.gitignore`.

5. **Test End-to-End Data Flow**  
   - Run `sensor_sim.py` → MQTT → InfluxDB → Grafana.  
   - Verify dashboards update in real time and alerts trigger as expected.

**Expected Outcome:**  
A complete visualization pipeline where environmental data from simulated sensors is displayed and monitored in Grafana, with automatic alerting on critical values.


## Authors and Acknowledgment
IICT - International IoT Communication Technologies GmbH

## License
Please see the LICENSE file for more details
