import typing

from orjson import orjson
from starlette.responses import JSONResponse


class ORJSONResponse(JSONResponse):
    media_type = "application/json"

    def render(self, content: typing.Any) -> bytes:
        return orjson.dumps(content)
