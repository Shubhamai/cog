import secrets
from typing import Any, Dict, Union

from attrs import define, field, validators

from .. import schema
from ..types import PYDANTIC_V2


# From worker parent process
#
@define
class PredictionInput:
    payload: Dict[str, Any]
    id: str = field(factory=lambda: secrets.token_hex(4))

    @classmethod
    def from_request(cls, request: schema.PredictionRequest) -> "PredictionInput":
        assert request.id, "PredictionRequest must have an id"
        if PYDANTIC_V2:
            payload = request.model_dump()["input"]
            print("PAYLOAD", payload)
        else:
            payload = request.dict()["input"]
        instance = cls(payload=payload, id=request.id)
        print("INSTANCE", instance)
        return instance


@define
class Cancel:
    id: str


@define
class Shutdown:
    pass


# From predictor child process
#
@define
class Log:
    message: str
    source: str = field(validator=validators.in_(["stdout", "stderr"]))


@define
class PredictionMetric:
    name: str
    value: "float | int"


@define
class PredictionOutput:
    payload: Any


@define
class PredictionOutputType:
    multi: bool = False


@define
class Done:
    canceled: bool = False
    error: bool = False
    error_detail: str = ""


@define
class Heartbeat:
    pass


PublicEventType = Union[Done, Heartbeat, Log, PredictionOutput, PredictionOutputType]
