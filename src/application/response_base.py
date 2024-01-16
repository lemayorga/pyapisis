from typing import Generic, Optional, TypeVar
from pydantic.generics import GenericModel

DataType = TypeVar("DataType")

class ResponseBase(GenericModel, Generic[DataType]):
    message: str = ""
    success: bool = True
    data: Optional[DataType] = None

class ResponseBaseBool(GenericModel):
    message: str = ""
    success: bool = True
    data: bool = True

# https://stackoverflow.com/questions/69507122/fastapi-custom-response-model