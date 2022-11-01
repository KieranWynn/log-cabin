from enum import Enum
import datetime as dt

from pydantic import BaseModel, Field, validator
from pydantic.generics import GenericModel

from . import helpers

from typing import List, Dict, Any, Generic, TypeVar, Optional, Tuple


class ModelType(str, Enum):
    INVERTERS = "inverters"  # Inverter details
    EIM = "eim"  # Production / Consumption details
    ACB = "acb"  # Battery details

class MeasurementType(str, Enum):
    PRODUCTION = "production"
    TOTAL_CONSUMPTION = "total-consumption"
    NET_CONSUMPTION = "net-consumption"

class State(str, Enum):
    IDLE = "idle"
    ACTIVE = "active"

class ObjectBase(BaseModel):
    type: ModelType
    activeCount: int
    readingTime: dt.datetime

    wNow: float
    whNow: Optional[float]
    whLifetime: Optional[float]
    state: Optional[State]

    @validator("readingTime", pre=True)
    def convert_ts(cls, v: int) -> dt.datetime:
        # v is an integer in seconds, convert float seconds
        return helpers.epoch_seconds_to_dt(v)

class EimInfo(ObjectBase):
    """ Envoy Integrated Meter reading: 
    Represents instantaneous information about the consuption / production of the enphase system 
    """

    measurementType: MeasurementType = Field()

    wNow: float
    whLifetime: float
    varhLeadLifetime: float
    varhLagLifetime: float
    vahLifetime: float
    rmsCurrent: float
    rmsVoltage: float
    reactPwr: float
    apprntPwr: float
    pwrFactor: float
    whToday: float
    whLastSevenDays: float
    vahToday: float
    varhLeadToday: float
    varhLagToday: float


class Production(BaseModel):
    total: EimInfo

class Consumption(BaseModel):
    total: EimInfo
    net: EimInfo

class Meters(BaseModel):
    production: Production
    consumption: Consumption

class System(BaseModel):
    inverters: ObjectBase
    storage: ObjectBase


class GatewayData(BaseModel):
    system: System
    meters: Meters

def parse_gateway_data(d: Dict) -> GatewayData:
    production_d = d["production"]
    consumption_d = d["consumption"]
    storage_d = d["storage"]

    inverters_d = production_d[0]
    if inverters_d["type"] == "inverters":
        inverters = ObjectBase(**inverters_d)
    else:
        raise TypeError("No inverters data in the production object")

    production_meter_d = production_d[1]
    if production_meter_d["type"] == "eim" and production_meter_d["measurementType"] == "production":
        total_production = EimInfo(**production_meter_d)

    total_consumption = consumption_d[0]
    net_consumption = consumption_d[1]

    storage = storage_d[0]

    return GatewayData(
        system=System(inverters=inverters, storage=storage), 
        meters=Meters(
            production=Production(total=total_production), 
            consumption=Consumption(total=EimInfo(**total_consumption), net=EimInfo(**net_consumption))
        )
    )
