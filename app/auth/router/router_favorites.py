from typing import Any

from fastapi import Depends,Response
from pydantic import Field

from app.utils import AppModel

from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data







@router.post("/users/favorites/shanyraks/{id}")
def add_to_favorites(
    id:str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service)):
    return svc.repository.add_to_favorites(id,jwt_data.user_id)


@router.get("/users/favorites/shanyraks/")
def get_favorites(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service)):
    return svc.repository.get_favorites(jwt_data.user_id)


@router.delete("/users/favorites/shanyraks/{id}")
def delete_favorite(
    id:str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service)):
    if svc.repository.delete_favorite(id,jwt_data.user_id):
        return Response(status_code=200)
