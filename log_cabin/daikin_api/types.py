from enum import Enum
from pydantic import BaseModel, Field

from typing import Optional

class PowerState(str, Enum):
    OFF = "0"
    ON = "1"

class OperatingMode(Enum):
    AUTO_0 = "0" # not used
    AUTO_1 = "1" # not used
    DRY = "2"
    COOL = "3"
    HEAT = "4"
    FAN = "6"
    AUTO = "7"


class FanSpeed(str, Enum):
    QUIET = "B"
    LOW = "3"
    LOW_MED = "4"
    MED = "5"
    MED_HIGH = "6"
    HIGH = "7"
    AUTO = "A"

class SwingMode(str, Enum):
    OFF = "0"
    H = "2"
    V = "1"
    HV = "3"


class ModelInfo(BaseModel):
    """ Represents information about the Daikin aircon model """
    pass

class SensorInfo(BaseModel):
    """ Represents instantaneous information about the Daikin aircon sensor state """
    indoor_temp: str = Field(alias="htemp")
    indoor_humidity: str = Field(alias="hhum")
    outdoor_temp: str = Field(alias="otemp")
    compressor_freq: str = Field(alias="cmpfreq")
    power_consumption: str = Field(alias="mompow") # in multiples of 0.1kW


class ControlInfo(BaseModel):
    """ Represents instantaneous information about the Daikin aircon control state """
    power_state: PowerState = Field(alias="pow")
    temp_setpoint: str = Field(alias="stemp")
    humidity_setpoint: str = Field(alias="shum")
    operating_mode: OperatingMode = Field(alias="mode")
    fan_speed: FanSpeed = Field(alias="f_rate")
    swing_mode: SwingMode = Field(alias="f_dir")

    # Saved settings
    last_temp_setpoint_dry_mode: str = Field(alias="dt2", )
    last_temp_setpoint_cool_mode: str = Field(alias="dt3")
    last_temp_setpoint_heat_mode: str = Field(alias="dt4")
    last_temp_setpoint_auto_mode: str = Field(alias="dt7")

    last_humidity_setpoint_dry_mode: str = Field(alias="dh2")
    last_humidity_setpoint_cool_mode: str = Field(alias="dh3")
    last_humidity_setpoint_heat_mode: str = Field(alias="dh4")
    last_humidity_setpoint_auto_mode: str = Field(alias="dh7")

    last_fan_speed_dry_mode: FanSpeed = Field(alias="dfr2")
    last_fan_speed_cool_mode: FanSpeed = Field(alias="dfr3")
    last_fan_speed_heat_mode: FanSpeed = Field(alias="dfr4")
    last_fan_speed_fan_mode: FanSpeed = Field(alias="dfr6")
    last_fan_speed_auto_mode: FanSpeed = Field(alias="dfr7")

    last_swing_mode_dry_mode: SwingMode = Field(alias="dfd2")
    last_swing_mode_cool_mode: SwingMode = Field(alias="dfd3")
    last_swing_mode_heat_mode: SwingMode = Field(alias="dfd4")
    last_swing_mode_fan_mode: SwingMode = Field(alias="dfd6")
    last_swing_mode_auto_mode: SwingMode = Field(alias="dfd7")


