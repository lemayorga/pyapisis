from fastapi import APIRouter, Depends, Path , status
from typing import Annotated
from dependency_injector.wiring import inject, Provide

from infra.database.setting_db import Database, get_db
from application.auth.services.auth_service import get_current_user

from config.container import Dependencies
from resources.strings import RECORD_DOES_NOT_EXIST, SUCCESSFUL_OPERATION
from application.commun.schemas.catalogue_schema import CatalogueCreateDto, CatalogueSchema, CatalogueUpdateDto
from application.commun.services.catalougue_service import CatalougueService
from application.response_base import ResponseBase, ResponseBaseBool

router = APIRouter(
     prefix='/api/catalogue',
     tags=['Catalogue'],
)

table_name = router.tags[0]
serv_catalougue = Dependencies.catalougue_service




# @router.get('/fff', summary="Create access and refresh tokens for user")
# @inject
# async def ddd(session1: Database = Depends(Provide[Dependencies.db]),  session2: Session = Depends(get_db)):
#     # r1 = session1.query(Catalogue).all()
#     r2 = session2.query(Catalogue).all()


@router.get("/",  response_model=ResponseBase[list[CatalogueSchema]],
        status_code=status.HTTP_200_OK,
        summary=f"List records from {table_name}.")
@inject
async def get(service: CatalougueService =  Depends(Provide[serv_catalougue])):
    record = service.get_all()
    return ResponseBase[list[CatalogueSchema]](success = True, data = record, message = SUCCESSFUL_OPERATION)


@router.get("/{id}",  response_model=ResponseBase[CatalogueSchema], 
        status_code= status.HTTP_200_OK,
        summary=f"Get the {table_name} record by identifier.", 
        responses={404: {"description": "Store not found"}})
@inject
async def get(id: Annotated[int, Path(title="The ID of the item to get")], service: CatalougueService = Depends(Provide[serv_catalougue])):
    record = service.get_by_id(id)
    if record is None:
        return ResponseBase[CatalogueSchema](success = False, message = RECORD_DOES_NOT_EXIST)

    return ResponseBase[CatalogueSchema](success = True, data = record, message = SUCCESSFUL_OPERATION)   


@router.post("/", response_model=ResponseBase[CatalogueSchema], 
        status_code=status.HTTP_201_CREATED,
        summary=f"Create a record for {table_name} ." , 
        responses={409: {"description": "Conflict Error"}})
@inject
async def create(data: CatalogueCreateDto, service: CatalougueService = Depends(Provide[serv_catalougue])):
    record =  service.create(data)
    return ResponseBase[CatalogueSchema](success = True, data = record, message = SUCCESSFUL_OPERATION)
    

@router.patch("/{id}", response_model=ResponseBase[CatalogueSchema],
        status_code=status.HTTP_200_OK,
        summary=f"Update record for {table_name} by identifier.")
@inject
async def update(id: int, data: CatalogueUpdateDto, service: CatalougueService = Depends(Provide[serv_catalougue])):
    record = service.update(id, data)
    if record is None:
        return ResponseBase[CatalogueSchema](success = False, message = RECORD_DOES_NOT_EXIST)
    
    return ResponseBase[CatalogueSchema](success = True, data = record, message = SUCCESSFUL_OPERATION)


@router.delete("/{id}", response_model=ResponseBaseBool,
        status_code=status.HTTP_200_OK,
        summary=f"Delete a record from {table_name} by identifier.")
@inject
async def delete(id: int, service: CatalougueService = Depends(Provide[serv_catalougue])):
    record =  service.delete(id)
    if record is None:
        return ResponseBaseBool(success = False, message = RECORD_DOES_NOT_EXIST)
    
    return ResponseBaseBool(success = True, data = record, message = SUCCESSFUL_OPERATION)

