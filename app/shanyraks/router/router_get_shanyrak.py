from typing import Any, Optional, List

from fastapi import Depends
from pydantic import Field

from fastapi import Response
from app.utils import AppModel

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service

from . import router

# class Coordinates(AppModel):
#     lat: float
#     lng: float

# class getShanyrak(AppModel):
#     type: str
#     price: int
#     address: str
#     area: float
#     rooms_count: int
#     description: str
#     pic: Optional[List[str]] = []
#     location:Coordinates
class Coordinates(AppModel):
    type: str
    coordinates: List[float]

class getShanyrak(AppModel):
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str
    pic: Optional[List[str]] = []
    location: Optional[Coordinates]
class listShanyraks(AppModel):
    total:int
    objects:List[getShanyrak]


@router.get("/{shanyrak_id:str}", response_model=getShanyrak)
def get_shanyrak(
    shanyrak_id:str,
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    shanyrak = svc.repository.get_shanyrak(shanyrak_id)
    if shanyrak is None:
        return Response(status_code=404)
    return getShanyrak(**shanyrak)


@router.get("/")
def list_shanyraks(
    limit: int,
    offset: int,
    rooms_count: Optional[int] = None,
    price_from: Optional[int]=None,
    price_until:Optional[int]=None,
    latitude:Optional[float]=None,
    longitude:Optional[float]=None,
    radius:Optional[float]=None,
    svc: Service = Depends(get_service),
    ):
    result =svc.repository.list_shanyraks(limit, offset, rooms_count, price_from, price_until,latitude,longitude, radius)
    return {"total": len(result), "objects": result}