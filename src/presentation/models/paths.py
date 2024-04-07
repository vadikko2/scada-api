import functools

import fastapi

from service_layer.models import validation

IdPath = functools.partial(
    fastapi.Path,
    **validation.IdFieldParams,
)
