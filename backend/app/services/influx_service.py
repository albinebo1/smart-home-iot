from influxdb_client import InfluxDBClient

INFLUX_URL = "http://influxdb:8086"
INFLUX_TOKEN = "eLb-FIzhnLU4QWz7Ks0NUGMx89hMvaPsJsgHMoyuzir6uR9EIbabPImlK8Qc4HRrazqOnSdndAhvx_YBoWGaxQ=="
INFLUX_ORG = "smart-home"
INFLUX_BUCKET = "sensors"
INFLUX_MEASUREMENT = "sensor_data_v2"
INFLUX_FIELD = "value"


def get_client():
    return InfluxDBClient(
        url=INFLUX_URL,
        token=INFLUX_TOKEN,
        org=INFLUX_ORG
    )


def query_latest_sensor(room_id: str, sensor_type: str):
    client = get_client()
    query_api = client.query_api()

    query = f'''
    from(bucket: "{INFLUX_BUCKET}")
      |> range(start: -1h)
      |> filter(fn: (r) => r._measurement == "{INFLUX_MEASUREMENT}")
      |> filter(fn: (r) => r._field == "{INFLUX_FIELD}")
      |> filter(fn: (r) => r.room == "{room_id}")
      |> filter(fn: (r) => r.type == "{sensor_type}")
      |> last()
    '''

    try:
        tables = query_api.query(query, org=INFLUX_ORG)

        for table in tables:
            for record in table.records:
                return record.get_value()

        return None

    finally:
        client.close()

def query_sensor_history(room_id: str, sensor_type: str, minutes: int = 60):
    client = get_client()
    query_api = client.query_api()

    query = f'''
    from(bucket: "{INFLUX_BUCKET}")
      |> range(start: -{minutes}m)
      |> filter(fn: (r) => r._measurement == "{INFLUX_MEASUREMENT}")
      |> filter(fn: (r) => r._field == "{INFLUX_FIELD}")
      |> filter(fn: (r) => r.room == "{room_id}")
      |> filter(fn: (r) => r.type == "{sensor_type}")
      |> sort(columns: ["_time"])
    '''

    try:
        tables = query_api.query(query, org=INFLUX_ORG)
        points = []

        for table in tables:
            for record in table.records:
                points.append({
                    "time": record.get_time().isoformat(),
                    "value": float(record.get_value())
                })

        return points

    finally:
        client.close()