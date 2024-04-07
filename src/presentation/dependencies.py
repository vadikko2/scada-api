import functools
from service_layer import bootstrap, event_driven


@functools.lru_cache
def inject_mediator() -> event_driven.Mediator:
    return bootstrap.bootstrap()
