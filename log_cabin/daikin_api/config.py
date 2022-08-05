from pydantic import BaseModel

class DaikinDevice(BaseModel):
    """ Configuration detail to describe a Daikin Aircon Device """
    name: str
    ip: str
    uuid: str