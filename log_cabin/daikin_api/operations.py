import logging
from typing import Dict, Any

import httpx

from .types import SensorInfo, ControlInfo
from .helpers import parse_string_response, pretty_dict
from .config import DaikinDevice

logger = logging.getLogger(__name__)

def get_model_info(aircon: DaikinDevice) -> Dict[str, Any]:
    url = f"https://{aircon.ip}/aircon/get_model_info"
    headers = {
        "X-Daikin-uuid": f"{aircon.uuid}"
    }
    logger.info(f"{aircon.name}: Fetching {url}")
    r = httpx.get(url, headers=headers, verify=False)
    d = parse_string_response(r.text)
    # print(pretty_dict(d))
    return d

def get_sensor_info(aircon: Dict[str, Any]) -> SensorInfo:
    url = f"https://{aircon.ip}/aircon/get_sensor_info"
    headers = {
        "X-Daikin-uuid": f"{aircon.uuid}"
    }
    logger.info(f"{aircon.name}: Fetching {url}")
    r = httpx.get(url, headers=headers, verify=False)
    d = parse_string_response(r.text)
    # print(pretty_dict(d))
    return SensorInfo(**d)

def get_control_info(aircon: Dict[str, Any]) -> ControlInfo:
    url = f"https://{aircon.ip}/aircon/get_control_info"
    headers = {
        "X-Daikin-uuid": f"{aircon.uuid}"
    }
    logger.info(f"{aircon.name}: Fetching {url}")
    r = httpx.get(url, headers=headers, verify=False)
    d = parse_string_response(r.text)
    # print(pretty_dict(d))
    return ControlInfo(**d)