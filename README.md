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

## Sprint 4 – Scalability & Testing

**Goal:**  
Evaluate the performance, reliability, and scalability of the IoT Environmental Monitoring System under varying load and network conditions. Optimize MQTT and InfluxDB settings for better stability and throughput.

**Main Tasks**
1. **Increase Sensor Simulation Scale**  
   - Adjust the file `load_sim.py` to simulate at least 50 virtual sensors with different types.  
   - Vary message intervals and payload sizes to create diverse traffic patterns.
   - Observe CPU and memory usage with docker stats during simulation.

2. **Measure System Performance**  
   - Implement `latency_subscriber.py` that calculates the latency and stores the results into a csv file
   - Monitor MQTT message throughput via the Broker statistics (`$SYS/#`) and store it to a log file

3. **Test Network Stability**  
   - Introduce application layer network impairments to simulate LPWAN behavior
      - Add unifromly distributed delay inside the application
      - Drop packets based on a loss_rate

4. **Optional: Optimize Reliability and Performance**  
   - Adjust MQTT parameters such as QoS level (--qos 0 or --qos 1) and keepalive interval.
   - Experiment with InfluxDB write modes (synchronous vs asynchronous).
   - Tune client buffer sizes or batching behavior to reduce latency.

5. **Analyze Results**  
   - Record metrics in a table, as below:
   
| Test Case | Delay (ms) | Loss (%) | QoS | Data Loss (%) | Observation |
|------------|-------------|----------|-----|----------------|-------------|
| Baseline | 0 | 0 | 0 | 0 | Stable operation |
| Stress | 200 | 5 | 0 | 15 |  |
| Optimized | 200 | 5 | 1 | 2 |  |


**Expected Outcome:**  
A scaled-up and resilient prototype capable of handling tens of simulated sensors while maintaining consistent data delivery to InfluxDB and Grafana.
Performance metrics and test observations demonstrate the system’s behavior under load, identify bottlenecks, and show measurable improvements after optimization


## Authors and Acknowledgment
IICT - International IoT Communication Technologies GmbH

## License
Please see the LICENSE file for more details
