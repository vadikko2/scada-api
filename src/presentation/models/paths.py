import functools

import fastapi

from service_layer.models import validation

HolderIdPath = functools.partial(
    fastapi.Path,
    **validation.IdFieldParams,
)
