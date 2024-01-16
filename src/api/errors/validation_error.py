from typing import Union
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.constants import REF_PREFIX
from fastapi.openapi.utils import validation_error_response_definition
from pydantic import ValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY


async def http422_error_handler(
    request: Request,
    exc: Union[RequestValidationError, ValidationError],
) -> JSONResponse:
     
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    return JSONResponse(status_code=HTTP_422_UNPROCESSABLE_ENTITY, content={"message": f"{base_error_message}. Detail errors: { exc.errors()}"})

    # return JSONResponse(
    #     {"errors": exc.errors()},
    #     status_code=HTTP_422_UNPROCESSABLE_ENTITY,
    # )


validation_error_response_definition["properties"] = {
    "errors": {
        "title": "Errors",
        "type": "array",
        "items": {"$ref": "{0}ValidationError".format(REF_PREFIX)},
    },
}