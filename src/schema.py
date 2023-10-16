from enum import StrEnum
from pydantic import BaseModel


class MicrowaveState(StrEnum):
    on = "on"
    off = "off"


class Buttons(StrEnum):
    ON = "ON"
    OFF = "OFF"
    CANCEL = "CANCEL"
    PLUS_POWER = "PLUS_POWER"
    MINUS_POWER = "MINUS_POWER"
    PLUS_TIME = "PLUS_TIME"
    MINUS_TIME = "MINUS_TIME"


class StatusMessage(BaseModel):
    state: MicrowaveState
    power: int
    time: int


class ButtonsMessage(BaseModel):
    button: Buttons


class Claims(BaseModel):
    sub: str
    name: str
    iat: int
    aud: str
    iss: str
    exp: int
