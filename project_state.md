Adaptive AI-Based IoT Smart Home System
Author: albi nebo
Degree: B.Sc. Computer Engineering
Status: Infrastructure Stable – Observation Mode Complete

1. Project Vision

Design and implement an adaptive AI-driven IoT smart home system capable of:

Structured real-time sensor data ingestion

Context-aware time-series storage

Per-room statistical reasoning

Autonomous decision generation

Future adaptive policy learning

The system must be:

Modular

Containerized

Extensible

Explainable

Research-ready

2. System Architecture Overview
2.1 Containerized Infrastructure (Docker Compose)

Services:

mqtt → eclipse-mosquitto:2

nodered → nodered/node-red:latest

influxdb → influxdb:2.7

ai-agent → custom Python 3.11 container

All services run in the same Docker bridge network.

Ports:

Service	Port
MQTT	1883
Node-RED	1880
InfluxDB	8086
2.2 High-Level Data Flow
Sensor Simulator
        ↓
MQTT Broker
        ↓
Node-RED
        ↓
HTTP Write (InfluxDB v2 API)
        ↓
InfluxDB (Time-Series Storage)
        ↓
AI Agent (Python – Mean & Grouping)

Important architectural decision:

Legacy influxdb out node was abandoned due to silent tag loss.

System now uses direct HTTP v2 write API (line protocol).

This ensures deterministic tag storage.

3. MQTT Layer
Topic Structure
home/{room}/sensor/{type}

Example:

home/livingroom/sensor/temperature
Payload Format
{
  "value": 24.83
}

Publishing interval:

Every 2 seconds (simulator)

4. Node-RED Layer
Flow Structure
MQTT in → JSON → Function → HTTP Request
4.1 Function Node (FINAL WORKING VERSION)
const parts = msg.topic.split("/");

const room = parts[1];
const type = parts[3];

let v = parseFloat(msg.payload.value);
if (isNaN(v)) return null;

// InfluxDB v2 line protocol
msg.payload = `sensor_data_v2,room=${room},type=${type} value=${v}`;

msg.headers = {
  "Authorization": "Token <INFLUX_TOKEN>",
  "Content-Type": "text/plain"
};

return msg;
4.2 HTTP Request Node Configuration

Method: POST

URL:

http://influxdb:8086/api/v2/write?org=smart-home&bucket=sensors&precision=s

Expected success code:

204

If not 204:

401 → wrong token

404 → wrong path

500 → invalid line protocol

5. InfluxDB Schema

Bucket:

sensors

Measurement:

sensor_data_v2

Tags:

room

type

Fields:

value (float)

Example stored point:

sensor_data_v2,room=livingroom,type=temperature value=24.83

Verified via:

import "influxdata/influxdb/schema"
schema.tagValues(...)
6. AI Agent (Python)

Language: Python 3.11
Library: influxdb-client
Containerized via Docker

6.1 Observation Mode – Mean Calculation
Single Room Query
from(bucket: "sensors")
  |> range(start: -10m)
  |> filter(fn: (r) => r._measurement == "sensor_data_v2")
  |> filter(fn: (r) => r._field == "value")
  |> filter(fn: (r) => r.room == "livingroom")
  |> filter(fn: (r) => r.type == "temperature")
  |> mean()
6.2 Per-Room Grouping
from(bucket: "sensors")
  |> range(start: -10m)
  |> filter(fn: (r) => r._measurement == "sensor_data_v2")
  |> filter(fn: (r) => r._field == "value")
  |> filter(fn: (r) => r.type == "temperature")
  |> group(columns: ["room"])
  |> mean()

Agent prints:

[AI Agent] room=livingroom mean_temp(10m)=24.52
7. Simulator

File:

simulator/sensor_simulator.py

Publishes:

Random float 20–30

Every 2 seconds

To MQTT topic above

Broker:

127.0.0.1:1883
8. Issues Encountered & Resolved
8.1 Docker Issues

Daemon not starting → resolved via Docker Desktop restart.

DNS resolution error (influxdb not found) → fixed by correct compose boot order.

8.2 Influx 401 Unauthorized

Cause:

Old token from previous machine.
Fix:

Generate new All Access token.

8.3 Python Output Not Appearing

Cause:

Buffered output inside container.
Fix:

CMD ["python", "-u", "agent.py"]

8.4 Node-RED Tag Loss (Critical Issue)

Cause:

influxdb out node silently ignoring msg.tags.
Fix:

Switched to HTTP v2 write API with line protocol.

This was the most significant architecture correction.

9. Current System Status
Component	Status
MQTT	Stable
Node-RED	Stable
InfluxDB	Stable
Tag Storage	Verified
AI Mean	Working
Per-room grouping	Working
Observation Mode	Complete
10. Next Implementation Phases
Phase 1 – Anomaly Detection

Static threshold detection

Rolling standard deviation detection

Z-score detection

Phase 2 – Decision Publishing

MQTT topic:

home/{room}/ai/decision

JSON decision payload

Log decisions to Influx (separate measurement)

Phase 3 – Context Awareness

Time-of-day modeling

Multi-sensor correlation

Occupancy inference

Phase 4 – Adaptive Policy

Reinforcement learning prototype

Reward modeling (comfort vs energy)

Policy update loop

Phase 5 – Evaluation Framework

Baseline vs AI comparison

Energy efficiency metric

Comfort deviation metric

11. Research Contributions Potential

Demonstrates clean containerized IoT-AI architecture

Shows pitfalls of legacy Influx node in v2

Implements structured tag-based contextual reasoning

Provides modular extensible AI pipeline

12. Future Expansion Ideas

Humidity sensors

Light sensors

Actuator simulation

Digital twin simulation

Explainable AI reasoning output

Multi-objective optimization

Edge deployment scenario

13. Known Technical Constraints

Currently single simulated sensor

No actuator feedback loop yet

No persistent AI model storage

No policy learning implemented yet

No security layer beyond local Docker

14. Architectural Principles Followed

Microservice separation

Clear data contracts

Explicit schema definition

Deterministic write protocol

Debug traceability

Stateless AI agent

15. Clean Restart Procedure

docker compose down -v

docker compose up -d

Start simulator

Verify HTTP 204 responses

Check Influx tags

Restart AI agent