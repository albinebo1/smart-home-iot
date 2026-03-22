import { useEffect, useState } from "react"
import { getSystemOverview, controlActuator, setSystemMode } from "./services/api"

const ROOM_CONFIG = {
  livingroom: {
    sensors: ["temperature"],
    controls: [
      { key: "light", label: "Light", onColor: "bg-amber-500 hover:bg-amber-400" },
      { key: "ac", label: "AC", onColor: "bg-sky-600 hover:bg-sky-500" },
      { key: "fan", label: "Fan", onColor: "bg-cyan-600 hover:bg-cyan-500" },
    ],
  },
  bedroom: {
    sensors: ["temperature"],
    controls: [
      { key: "light", label: "Light", onColor: "bg-amber-500 hover:bg-amber-400" },
      { key: "ac", label: "AC", onColor: "bg-sky-600 hover:bg-sky-500" },
      { key: "fan", label: "Fan", onColor: "bg-cyan-600 hover:bg-cyan-500" },
    ],
  },
  kitchen: {
    sensors: ["temperature", "motion", "smoke"],
    controls: [
      { key: "light", label: "Light", onColor: "bg-amber-500 hover:bg-amber-400" },
      { key: "exhaust_fan", label: "Exhaust Fan", onColor: "bg-cyan-600 hover:bg-cyan-500" },
    ],
  },
  bathroom: {
    sensors: ["temperature", "humidity", "motion"],
    controls: [
      { key: "light", label: "Light", onColor: "bg-amber-500 hover:bg-amber-400" },
      { key: "ventilation_fan", label: "Ventilation Fan", onColor: "bg-cyan-600 hover:bg-cyan-500" },
    ],
  },
  hallway: {
    sensors: ["motion"],
    controls: [
      { key: "light", label: "Light", onColor: "bg-amber-500 hover:bg-amber-400" },
    ],
  },
}

const SENSOR_LABELS = {
  temperature: "Temperature",
  humidity: "Humidity",
  motion: "Motion",
  smoke: "Smoke",
}

function formatSensorValue(sensorKey, value) {
  if (sensorKey === "temperature") return `${value} °C`
  if (sensorKey === "humidity") return `${value} %`
  return value
}

export default function App() {
  const [overview, setOverview] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")
  const [actionLoading, setActionLoading] = useState("")

  async function loadOverview() {
    try {
      const data = await getSystemOverview()
      setOverview(data)
      setError("")
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadOverview()

    const interval = setInterval(() => {
      loadOverview()
    }, 700)

    return () => clearInterval(interval)
  }, [])

  async function handleActuator(roomId, device, state) {
  const actionKey = `${roomId}-${device}-${state}`
  setActionLoading(actionKey)

  try {
    await controlActuator(roomId, device, state)

    // short visual feedback only
    await new Promise((resolve) => setTimeout(resolve, 150))

    // stop loading quickly
    setActionLoading("")

    // refresh once, but don't block the button on it
    loadOverview()
  } catch (err) {
    setError(err.message)
    setActionLoading("")
  }
}

  async function handleModeChange(mode) {
  try {
    await setSystemMode(mode)
    await loadOverview()
  } catch (err) {
    setError(err.message)
  }
}

  function getOnButtonClass(currentState, loadingKey, expectedKey, colorClass) {
    const active = currentState === "ON"
    const loading = loadingKey === expectedKey

    if (loading) {
      return "flex-1 rounded-xl bg-slate-700 px-4 py-2 font-medium"
    }

    return `flex-1 rounded-xl px-4 py-2 font-medium ${
      active ? colorClass : "bg-slate-700 hover:bg-slate-600"
    }`
  }

  function getOffButtonClass(currentState, loadingKey, expectedKey) {
    const active = currentState === "OFF"
    const loading = loadingKey === expectedKey

    if (loading) {
      return "flex-1 rounded-xl bg-slate-700 px-4 py-2 font-medium"
    }

    return `flex-1 rounded-xl px-4 py-2 font-medium ${
      active ? "bg-rose-600 hover:bg-rose-500" : "bg-slate-700 hover:bg-slate-600"
    }`
  }

  if (loading) {
    return (
      <div className="w-full min-h-screen bg-slate-950 text-white px-6 py-8">
        <p className="text-xl">Loading dashboard...</p>
      </div>
    )
  }

  if (error && !overview) {
    return (
      <div className="min-h-screen bg-slate-950 text-red-400 flex items-center justify-center">
        <p className="text-xl">{error}</p>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-slate-950 text-white px-6 py-8 flex justify-center">
      <div className="max-w-6xl mx-auto">
        <header className="mb-8">
          <h1 className="text-4xl font-bold mb-2 text-yellow-400 !text-yellow-400">
            Smart Home Dashboard
          </h1>
          <p className="text-slate-400">Adaptive AI-Based IoT Smart Home System</p>
        </header>

        {error && (
          <div className="mb-6 bg-red-900/40 border border-red-700 text-red-300 rounded-2xl p-4">
            {error}
          </div>
        )}

        <section className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          <div className="bg-slate-900 rounded-2xl p-5 shadow-lg">
            <p className="text-slate-400 text-sm mb-2">System Mode</p>

            <div className="flex gap-2">
              {["Manual", "Static", "AI"].map((mode) => (
                <button
                  key={mode}
                  onClick={() => handleModeChange(mode)}
                  className={`flex-1 rounded-xl px-3 py-2 text-sm font-medium ${overview.mode === mode
                      ? "bg-yellow-500 text-black"
                      : "bg-slate-700 hover:bg-slate-600"
                    }`}
                >
                  {mode}
                </button>
              ))}
            </div>
          </div>

          <div className="bg-slate-900 rounded-2xl p-5 shadow-lg">
            <p className="text-slate-400 text-sm mb-2">Total Rooms</p>
            <p className="text-2xl font-semibold">{overview.total_rooms}</p>
          </div>

          <div className="bg-slate-900 rounded-2xl p-5 shadow-lg">
            <p className="text-slate-400 text-sm mb-2">Active Alerts</p>
            <p className="text-2xl font-semibold">{overview.active_alerts}</p>
          </div>
</section>

        <section>
          <h2 className="text-2xl font-semibold mb-4">Rooms</h2>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {overview.rooms.map((room) => {
              const config = ROOM_CONFIG[room.room_id]

              return (
                <div
                  key={room.room_id}
                  className="bg-slate-900 rounded-2xl p-5 shadow-lg border border-slate-800"
                >
                  <h3 className="text-xl font-semibold mb-4 capitalize text-center tracking-wide">
                    {room.room_id}
                  </h3>

                  <div className="space-y-2 text-slate-300 mb-6 text-center text-sm">
                    {config.sensors.map((sensorKey) => (
                      <p key={sensorKey}>
                        {SENSOR_LABELS[sensorKey]}:{" "}
                        {formatSensorValue(sensorKey, room[sensorKey])}
                      </p>
                    ))}

                    {config.controls.map((control, index) => (
                      <p key={`${control.label}-${index}`}>
                        {control.label}: {room.actuators[control.key]}
                      </p>
                    ))}
                  </div>

                  <div className="space-y-4">
                    {config.controls.map((control, index) => {
                      const currentState = room.actuators[control.key]

                      return (
                        <div key={`${control.label}-${index}`}>
                          <p className="text-sm text-slate-400 mb-2 text-center">
                            {control.label} Control
                          </p>

                          <div className="flex gap-2">
                            <button
                              onClick={() =>
                                handleActuator(room.room_id, control.key, "ON")
                              }
                              disabled={actionLoading !== ""}
                              className={getOnButtonClass(
                                currentState,
                                actionLoading,
                                `${room.room_id}-${control.key}-ON`,
                                control.onColor
                              )}
                            >
                              {actionLoading === `${room.room_id}-${control.key}-ON`
                                ? "Sending..."
                                : `${control.label} ON`}
                            </button>

                            <button
                              onClick={() =>
                                handleActuator(room.room_id, control.key, "OFF")
                              }
                              disabled={actionLoading !== ""}
                              className={getOffButtonClass(
                                currentState,
                                actionLoading,
                                `${room.room_id}-${control.key}-OFF`
                              )}
                            >
                              {actionLoading === `${room.room_id}-${control.key}-OFF`
                                ? "Sending..."
                                : `${control.label} OFF`}
                            </button>
                          </div>
                        </div>
                      )
                    })}
                  </div>
                </div>
              )
            })}
          </div>
        </section>
      </div>
    </div>
  )
}