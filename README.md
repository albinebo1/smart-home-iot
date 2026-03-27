# Adaptive AI-Based IoT Smart Home System

A containerized, software-simulated smart home platform that combines MQTT messaging, Node-RED orchestration, InfluxDB time-series storage, a FastAPI backend, a React frontend, and an AI-agent layer for future adaptive control.

## Project Goal

Traditional smart-home systems usually rely on fixed rules and do not adapt well when user behavior changes. This project aims to build a smart-home environment that starts with manual and static automation, then evolves toward AI-supported adaptive control while remaining explainable, testable, and modular.

## Current Architecture

Sensor Simulator  
→ MQTT Broker  
→ Node-RED  
→ InfluxDB  
→ FastAPI Backend  
→ React Frontend  
→ AI Agent (currently separate / partially integrated)

### Current role of each layer

- **Sensor Simulator** publishes virtual room sensor data.
- **MQTT Broker** carries sensor data, actuator commands, and actuator state messages.
- **Node-RED** handles orchestration, baseline automation, and internal control logic.
- **InfluxDB** stores time-series sensor data.
- **FastAPI Backend** exposes application endpoints, reads sensor/history data, publishes actuator commands, and listens for confirmed actuator states.
- **React Frontend** is the main user-facing dashboard.
- **AI Agent** currently runs separately and is planned to be merged more deeply into the architecture for adaptive behavior.

## Important Architecture Rules

- **Node-RED is not the final frontend.**
- **Requested actuator action and actual actuator state are separate.**
- **Internal IDs should remain stable.** Human-friendly names should be handled in the frontend only.

## Current Stack

- Python
- FastAPI
- React
- Vite
- Tailwind CSS
- Recharts
- Node-RED
- Eclipse Mosquitto (MQTT)
- InfluxDB 2.x
- Docker / Docker Compose

## Repository Structure

```text
smart-home-iot/
├── ai-agent/
├── backend/
├── frontend/
├── docker-compose.yml
└── ...
```

## MQTT Topic Design

### Sensors
```text
home/{room}/sensor/{type}
```

Example:
```text
home/livingroom/sensor/temperature
```

Payload:
```json
{ "value": 24.83 }
```

### Actuator commands
```text
home/{room}/actuator/{device}/set
```

Payload:
```json
{ "state": "ON" }
```

### Actuator state
```text
home/{room}/actuator/{device}/state
```

Payload:
```json
{ "state": "ON", "ts": 1739999999 }
```

## InfluxDB Design

- **Bucket:** `sensors`
- **Measurement:** `sensor_data_v2`
- **Tags:** `room`, `type`
- **Field:** `value`

Important note: the project moved away from the older Node-RED Influx node and now uses direct InfluxDB v2 HTTP line protocol writes because tag handling was more reliable.

## Current Room Model

### Living Room
- Sensors: temperature
- Actuators: light, ac, fan

### Bedroom
- Sensors: temperature
- Actuators: light, ac, fan

### Kitchen
- Sensors: temperature, motion, smoke
- Actuators: light, exhaust_fan

### Bathroom
- Sensors: temperature, humidity, motion
- Actuators: light, ventilation_fan

### Hallway
- Sensors: motion
- Actuators: light

## Backend Status

### Main backend features already working
- Read latest room sensor values from InfluxDB
- Read room history from InfluxDB
- Publish actuator commands to MQTT
- Listen to actuator `/state` topics and cache latest confirmed states
- Expose dashboard/system overview
- Expose system mode endpoints

### Main endpoints
- `GET /`
- `GET /health`
- `GET /api/rooms`
- `GET /api/rooms/{room_id}`
- `GET /api/rooms/{room_id}/history?sensor_type=temperature&minutes=60`
- `POST /api/rooms/{room_id}/actuators/{device}?state=ON|OFF`
- `GET /api/system/mode`
- `POST /api/system/mode?mode=Manual|Static|AI`
- `GET /api/system/overview`

## Frontend Status

The React dashboard is now the main user-facing interface.

### Current frontend features
- Dark smart-home dashboard UI
- System mode controls
- Room cards with room-specific sensors and controls
- Real actuator-state-based button styling
- Active alerts card
- Recent activity feed
- Room detail modal
- Modal open/close animations
- Functional actuator controls inside modal
- Temperature history chart in room modal
- Chart time-range selector (15 / 60 / 180 min)
- PWA setup started

### Important frontend design direction
The UI is being shaped toward a **tablet-style smart-home application** rather than a long scrolling web page.

## PWA Status

The frontend has started being converted into a **Progressive Web App (PWA)** so it can behave more like a tablet application without rewriting the entire frontend as a native Android app.

### PWA work completed
- Added `vite-plugin-pwa`
- Updated Vite config
- Added manifest + icons
- Registered service worker
- Verified service worker and manifest in Chrome DevTools
- Preview/PWA testing works after development CORS adjustments

### Important current note
The frontend API base still uses `localhost`, which is fine on the same machine but will need to be changed to a local network IP or environment-based config for real tablet testing on another device.

## AI Agent Status

The AI agent currently exists as a separate service/container and can observe/query smart-home data from InfluxDB. It is not yet fully merged into the new FastAPI + React architecture.

The next major phase is to merge the AI work more carefully into:
- backend endpoints
- frontend AI status/decision panels
- mode handling
- event/decision logging

## Problems Already Faced and Important Fixes

### 1. InfluxDB tag/write reliability
The old Node-RED Influx node was unreliable for tags.
**Fix:** switched to direct HTTP line protocol writes.

### 2. AC and Fan control overlap
AC and Fan were previously behaving as if they shared the same key.
**Fix:** separated device keys and mappings.

### 3. Button delay / sluggish control feedback
The control pipeline looked slow, but detailed logging showed that backend/MQTT/Node-RED were fast.
**Conclusion:** most visible delay came from polling cadence and confirmed-state architecture.
**Fixes:** improved button loading style, tuned polling, and preserved confirmed-state logic.

### 4. Alert count not updating
Frontend initially assumed nested sensor objects.
**Fix:** adapted alert logic to the actual flat backend room shape.

### 5. PWA preview fetch failures
Preview ran on a different port and backend CORS blocked it.
**Fix:** adjusted development CORS and rebuilt backend.

## Current Limitations

- System mode is not yet persisted across restart
- Backend `active_alerts` is still placeholder
- No backend event feed endpoint yet
- No WebSocket/live push yet
- Actuator state cache is only in memory
- AI decisions are not yet integrated into backend/frontend
- Frontend still needs final jury/exhibition polish
- Real tablet testing still needs a proper configurable backend API base

## Next Steps

### Short term
- Merge AI-agent work carefully
- Add backend mode persistence
- Add backend-generated alerts/events
- Improve tablet-first layout
- Improve room-detail analytics
- Add AI status/decision panels

### Medium term
- Add more charts and analytics
- Add dedicated alerts/analytics pages
- Add explainability for AI decisions
- Improve installable PWA/tablet experience

## Running the Project

### Start infrastructure
```bash
docker compose up -d --build
```

### Check services
```bash
docker compose ps
```

### Run frontend
```bash
cd frontend
npm install
npm run dev
```

### Useful logs
```bash
docker compose logs -f backend
docker compose logs -f nodered
docker compose logs -f influxdb
docker compose logs -f ai-agent
```

## Notes for Future Contributors / Chatbots

- Preserve the `/set` vs `/state` distinction.
- Do not turn Node-RED back into the final frontend.
- Keep internal room/device IDs stable.
- Recheck frontend assumptions carefully because some earlier iterations assumed nested room sensor data.
- Be careful during AI merge so the work is not blocked by conflicting architecture changes.

## Project Positioning

This project is a containerized, software-simulated smart-home IoT platform with MQTT messaging, Node-RED orchestration, InfluxDB time-series storage, a FastAPI backend, a React/PWA frontend, and an AI-agent layer being merged for adaptive control. It already supports multi-room monitoring, confirmed-state actuator control, alerts, recent activity, modal room details, and temperature history analytics, and is currently transitioning from static automation toward AI-integrated adaptive behavior.
