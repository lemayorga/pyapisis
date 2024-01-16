
from pydantic import BaseModel

class CatalogueBaseDto(BaseModel):
    group: str
    value: str
    description: str | None = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True

class CatalogueCreateDto(CatalogueBaseDto):
    isActive: bool = True

class CatalogueUpdateDto(CatalogueBaseDto):
    isActive: bool = True

class CatalogueSchema(CatalogueBaseDto):
    id: int
    isActive: bool = False

    class Config:
        orm_mode = True

