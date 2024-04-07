import pydantic

from service_layer.event_driven import response as res
from service_layer.event_driven.events import event


class DispatchResult(pydantic.BaseModel):
    response: res.Response | None = pydantic.Field(default=None)
    events: list[event.Event] = pydantic.Field(default_factory=list)
