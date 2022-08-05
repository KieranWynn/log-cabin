import os
import logging
import datetime as dt
from typing import Tuple, Dict, Any

import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

logger = logging.getLogger(__name__)

influx_bucket = "South Crescent"

influx_tags = {
    "room": {
        "living_room",
        "main_bedroom",
        "office",
        "spare_bedroom"
    }
}

influx_fields = {
    "aircon_sensor": {
        "indoor_temp",
        "outdoor_temp",
        "indoor_humidity",
        "compressor_freq",
        "power_consumption"
    },
    "aircon_state": {
        "power_state",
        "temp_setpoint",
        "humidity_setpoint",
        "operating_mode"
    },
    "aircon": {
        "indoor_temp",
        "outdoor_temp",
        "indoor_humidity",
        "compressor_freq",
        "power_consumption",
        "power_state",
        "temp_setpoint",
        "humidity_setpoint",
        "operating_mode"
    }
}

def make_measurement(s: str) -> str:
    if s in influx_fields:
        return s
    else:
        raise ValueError(f"{s} is not a valid measurement for bucket '{influx_bucket}'. Options are: {list(influx_fields.keys())}")

def make_tag(k: str, v: str) -> Tuple[str, str]:
    if k in influx_tags:
        if v in influx_tags[k]:
            return (k, v)
        else: 
            raise ValueError(f"{v} is not a valid tag value for key: '{k}'. Options are: {influx_tags[k]}")
    else:
        raise ValueError(f"{k} is not a valid tag key for bucket '{influx_bucket}'. Options are: {influx_tags}")

def make_field(measurement:str, k: str, v: Any) -> Tuple[str, Any]:
    if measurement in influx_fields:
        if k in influx_fields[measurement]:
            return (k, v)
        else: 
            raise ValueError(f"{v} is not a valid field key for measurement: '{measurement}'. Options are: {influx_fields[measurement]}")
    else:
        raise ValueError(f"{measurement} is not a valid measurement for bucket '{influx_bucket}'. Options are: {list(influx_fields.keys())}")

def write_point(api: influxdb_client.WriteApi, measurement: str, tags: Dict[str, str], fields: Dict[str, Any], timestamp: dt.datetime, bucket: str = influx_bucket):
    p = influxdb_client.Point(make_measurement(measurement))
    for tag_k, tag_v in tags.items():
        p.tag(*make_tag(k=tag_k, v=tag_v))
    for field_k, field_v in fields.items():
        p.field(*make_field(measurement=measurement, k=field_k, v=field_v))
    p.time(timestamp, write_precision=influxdb_client.WritePrecision.MS)
    logger.info(f"writing: {p}")
    api.write(bucket=bucket, record=p)

def make_point(d: Dict[str, Any]):
    measurement = make_measurement(measurement)
    return influxdb_client.Point(
        d,
        measurement=make_measurement(measurement),
        record_tag_keys=list(influx_tags.keys()),
        record_field_keys=influx_fields[measurement]
    )

def as_snake_case(s: str) -> str:
    return "_".join(s.split()).lower()