# InfluxDB connection
INFLUX_URL = "http://influxdb:8086"
INFLUX_TOKEN = "eLb-FIzhnLU4QWz7Ks0NUGMx89hMvaPsJsgHMoyuzir6uR9EIbabPImlK8Qc4HRrazqOnSdndAhvx_YBoWGaxQ=="
INFLUX_ORG = "smart-home"
INFLUX_BUCKET = "sensors"

# Data model
MEASUREMENT = "sensor_data_v2"
FIELD = "value"

# Observation behavior
QUERY_WINDOW = "10m"    # last 10 minutes
QUERY_INTERVAL = 30     # seconds
