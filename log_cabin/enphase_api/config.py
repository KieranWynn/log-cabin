from pydantic import BaseModel

class GatewayDevice(BaseModel):
    """ Configuration detail to describe a Enphase Envoy/ Gateway Device """
    ip: str
    serial_number: int