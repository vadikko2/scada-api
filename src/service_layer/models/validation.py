import functools

import pydantic

IdFieldParams = dict(
    description="Уникальный идентификатор",
    json_schema_extra={"nullable": False},
    frozen=True,
)


IdField = functools.partial(pydantic.Field, **IdFieldParams)
