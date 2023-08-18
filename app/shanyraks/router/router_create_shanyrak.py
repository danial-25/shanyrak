from typing import Any, List, Optional

from fastapi import Depends, UploadFile, File
from pydantic import Field


from app.utils import AppModel

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service

from . import router




# def upload_picture(
#     file=UploadFile,
#     # svc: Service = Depends(get_service),
# ):
#     """
#     file.filename: str - Название файла
#     file.file: BytesIO - Содержимое файла
#     """
#     # url = svc.s3_service.upload_file(file.file, file.filename)
    
#     return Response(status_code=201)
# class Coordinates(AppModel):
#     longitude: float
#     latitude: float

# class createShanyrak(AppModel):
#     type: str
#     price: int
#     address: str
#     area: float
#     rooms_count: int
#     description: str
#     pic: Optional[List[str]] = []
#     location: Optional[Coordinates]

class Coordinates(AppModel):
    type: str
    coordinates: List[float]

class createShanyrak(AppModel):
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str
    pic: Optional[List[str]] = []
    location: Optional[Coordinates]
class createShanyrakResponse(AppModel):
    id: Any = Field(alias="_id")

@router.post("/", response_model=createShanyrakResponse)
def create_shanyrak(
    input:createShanyrak,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    result = svc.here_service.get_coordinates(input.address)
    # input.location=result
    input.location = Coordinates(type="Point", coordinates=[result["lng"], result["lat"]])
    shanyrak_id = svc.repository.create_shanyrak(jwt_data.user_id, input.dict())
    
    return createShanyrakResponse(id=shanyrak_id)

    
@router.post("{id}/media")
async def create_upload_file(id:str,files: List[UploadFile], svc: Service = Depends(get_service), jwt_data: JWTData = Depends(parse_jwt_user_data)):
    urls = []
    for file in files:
        url = svc.s3_service.upload_file(file.file, file.filename)
        svc.repository.update_pic(id, jwt_data.user_id, url)
        urls.append(url)
    return {"filename": urls}