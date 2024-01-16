from fastapi import APIRouter, Depends, Path , status
from typing import Annotated
from dependency_injector.wiring import inject, Provide
from application.security.schemas.user_schema import UserDto, UserCreate
from resources.strings import RECORD_DOES_NOT_EXIST, SUCCESSFUL_OPERATION
from application.security.services.user_service import UserService
from config.container import Dependencies
from application.response_base import ResponseBase, ResponseBaseBool

router = APIRouter(
     prefix='/api/security',
     tags=['Users']
)
table_name = router.tags[0]


@router.get("/",  response_model=ResponseBase[list[UserDto]],
        status_code=status.HTTP_200_OK,
        summary=f"List records from {table_name}.")
@inject
async def get(service: UserService = Depends(Provide[Dependencies.user_service])): 
    try:
        record = service.get_all()
        return ResponseBase[list[UserDto]](success = True, data = record, message = SUCCESSFUL_OPERATION)
    
    except Exception as error:
        return ResponseBase[UserDto](success= False, message= str(error) )
    

# @router.get("/{id}",  response_model=ResponseBase[CatalogueSchema], 
#         status_code= status.HTTP_200_OK,
#         summary=f"Get the {table_name} record by identifier.", 
#         responses={404: {"description": "Store not found"}})
# @inject
# async def get(id: Annotated[int, Path(title="The ID of the item to get")], service: CatalougueService = Depends(Provide[serv_catalougue])):
#     try:
#         record = service.get_by_id(id)
#         if record is None:
#             return ResponseBase[CatalogueSchema](success = False, message = RECORD_DOES_NOT_EXIST)

#         return ResponseBase[CatalogueSchema](success = True, data = record, message = SUCCESSFUL_OPERATION)   
#     except Exception as error:
#         return ResponseBase[CatalogueSchema](success= False, message= str(error) )
    

@router.post("/", response_model=ResponseBase[UserDto], 
        status_code=status.HTTP_201_CREATED,
        summary=f"Create a record for {table_name} ." , 
        responses={409: {"description": "Conflict Error"}})
@inject
async def create(data: UserCreate, service: UserService = Depends(Provide[Dependencies.user_service])):
    try:
        record: UserDto =  service.create(data)
        return ResponseBase[UserDto](success = True, data = record, message = SUCCESSFUL_OPERATION)
    
    except Exception as error:
        return ResponseBase[UserDto](success= False, message= str(error) )


# @router.patch("/{id}", response_model=ResponseBase[CatalogueSchema],
#         status_code=status.HTTP_200_OK,
#         summary=f"Update record for {table_name} by identifier.")
# @inject
# async def update(id: int, data: CatalogueUpdateDto, service: CatalougueService = Depends(Provide[serv_catalougue])):
#     try:
#         record = service.update(id, data)
#         if record is None:
#             return ResponseBase[CatalogueSchema](success = False, message = RECORD_DOES_NOT_EXIST)
        
#         return ResponseBase[CatalogueSchema](success = True, data = record, message = SUCCESSFUL_OPERATION)
#     except Exception as error:
#         return ResponseBase[CatalogueSchema](success= False, message= str(error) )


# @router.delete("/{id}", response_model=ResponseBaseBool,
#         status_code=status.HTTP_200_OK,
#         summary=f"Delete a record from {table_name} by identifier.")
# @inject
# async def delete(id: int, service: CatalougueService = Depends(Provide[serv_catalougue])):
#     try:
#         record =  service.delete(id)
#         if record is None:
#             return ResponseBaseBool(success = False, message = RECORD_DOES_NOT_EXIST)
        
#         return ResponseBaseBool(success = True, data = record, message = SUCCESSFUL_OPERATION)
#     except Exception as error:
#         return ResponseBaseBool(success= False, message= str(error) )

