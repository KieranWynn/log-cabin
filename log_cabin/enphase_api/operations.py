import json
import logging
import httpx
from pydantic import parse_obj_as

from typing import Dict, Any

from .types import Production, parse_gateway_data, GatewayData
from .config import GatewayDevice

logger = logging.getLogger(__name__)

def get_gateway_data(gateway: GatewayDevice) -> GatewayData:
    url = f"http://{gateway.ip}/production.json"
    headers = {}
    logger.info(f"{gateway}: Fetching {url}")
    r = httpx.get(url, headers=headers, verify=False)
    # d = Production.parse_raw(r.text)
    p = parse_gateway_data(json.loads(r.text))
    # print(pretty_dict(d))
    return p