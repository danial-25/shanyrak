from typing import Any, Optional, List

from fastapi import Depends, Response
from pydantic import Field

from app.utils import AppModel

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service

from . import router

class Coordinates(AppModel):
    longitude: float
    latitude: float

class changeShanyrak(AppModel):
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str
    pic: Optional[List[str]] = []
    location: Optional[Coordinates]
@router.patch("/{shanyrak_id:str}")
def change_shanyrak(
    shanyrak_id:str,
    input:changeShanyrak,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    result = svc.here_service.get_coordinates(input.address)
    input.location=result
    update_result= svc.repository.update_shanyrak(shanyrak_id, jwt_data.user_id, input.dict())
    if update_result.modified_count==1:
        return Response(status_code=200)
    return Response(status_code=404)