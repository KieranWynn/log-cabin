import os
import time
import datetime as dt
import logging

from typing import Tuple, Dict, Any

import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS


import daikin_api
from daikin_api.helpers import as_float
from influx import write_point, as_snake_case
from timer import Timer

logging.basicConfig(format='%(asctime)s %(levelname)s: %(name)s %(message)s')
logging.getLogger().setLevel(logging.INFO)

def run():
    config = {
        "aircons": [
            {
                "uuid": "4a57d57016b346ecb716b491bc94660f",
                "ip": "10.0.4.36",
                "name": "Living Room"
            },
            {
                "uuid": "c823ed7ff55a44e082ac2e8a7866df53",
                "ip": "10.0.4.37",
                "name": "Main Bedroom"
            },
            {
                "uuid": "79f8b52d55404a30bdc6bb2ddf13f0bc",
                "ip": "10.0.4.38",
                "name": "Spare Bedroom"
            },
            {
                "uuid": "74e52819a12e4d54b7496dbe2b4aaea7",
                "ip": "10.0.4.39",
                "name": "Office"
            },
        ]
    }

    influx_client = influxdb_client.InfluxDBClient(
        url="https://ap-southeast-2-1.aws.cloud2.influxdata.com",
        token=os.getenv("INFLUXDB_TOKEN"),
        org="kieranwynn@gmail.com"
    )

    for aircon_config in config.get("aircons"):
        aircon = daikin_api.config.DaikinDevice(**aircon_config)

        control_time = dt.datetime.utcnow()
        control_info = daikin_api.operations.get_control_info(aircon)

        sensor_time = dt.datetime.utcnow()
        sensor_info = daikin_api.operations.get_sensor_info(aircon)

        sensor_fields = {
            "indoor_temp": as_float(sensor_info.indoor_temp),
            "outdoor_temp": as_float(sensor_info.outdoor_temp),
            "indoor_humidity": as_float(sensor_info.indoor_humidity),
            "compressor_freq": as_float(sensor_info.compressor_freq),
            "power_consumption": None if as_float(sensor_info.power_consumption) is None else as_float(sensor_info.power_consumption) * 100.0,
        }
        
        control_fields = {
            "power_state": int(control_info.power_state.value),
            "temp_setpoint": as_float(control_info.temp_setpoint),
            "humidity_setpoint": as_float(control_info.humidity_setpoint),
            "operating_mode": control_info.operating_mode.name if control_info.power_state is daikin_api.types.PowerState.ON else "OFF"
        }

        with influx_client.write_api() as write_api:
            write_point(api=write_api, measurement="aircon_sensor", tags={"room": as_snake_case(aircon.name)}, fields=sensor_fields, timestamp=sensor_time)
            write_point(api=write_api, measurement="aircon_state", tags={"room": as_snake_case(aircon.name)}, fields=control_fields, timestamp=control_time)
            write_point(api=write_api, measurement="aircon", tags={"room": as_snake_case(aircon.name)}, fields=dict(**sensor_fields, **control_fields), timestamp=control_time)


def main():
    interval_seconds = float(os.getenv("INTERVAL_SECONDS", "60"))

    while True:
        timer = Timer(logger=None)
        
        with timer:
            run()
        
        wait_time = interval_seconds - timer.elapsed_time
        logging.info(f"Waiting {wait_time:0.4f}s for next run")
        time.sleep(max(0, wait_time))



if __name__ == "__main__":
    main()