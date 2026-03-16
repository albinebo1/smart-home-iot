import time
from influxdb_client import InfluxDBClient
from config import *


def query_mean_value(client):
    query = f'''
    from(bucket: "{INFLUX_BUCKET}")
      |> range(start: -{QUERY_WINDOW})
      |> filter(fn: (r) => r._measurement == "sensor_data_v2")
      |> filter(fn: (r) => r._field == "value")
      |> filter(fn: (r) => r.room == "livingroom")
      |> filter(fn: (r) => r.type == "temperature")
      |> mean()
    '''

    tables = client.query_api().query(query, org=INFLUX_ORG)

    for table in tables:
        for record in table.records:
            return record.get_value()

    return None


def main():
    print("AI Agent started (observation mode)")

    client = InfluxDBClient(
        url=INFLUX_URL,
        token=INFLUX_TOKEN,
        org=INFLUX_ORG
    )

    while True:
        value = query_mean_value(client)

        if value is not None:
            print(f"[AI Agent] Mean value (last {QUERY_WINDOW}): {value:.2f}")
        else:
            print("[AI Agent] No data available yet")

        time.sleep(QUERY_INTERVAL)


if __name__ == "__main__":
    main()
