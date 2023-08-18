from typing import Any

from fastapi import Depends, Response
from pydantic import Field

from app.utils import AppModel

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service

from . import router





@router.delete("/{shanyrak_id:str}")
def change_shanyrak(
    shanyrak_id:str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    delete_result= svc.repository.delete_shanyrak(shanyrak_id, jwt_data.user_id,)
    if delete_result.deleted_count==1:
        return Response(status_code=200)
    return Response(status_code=404)


@router.delete("{id}/media")
async def delete_files(id:str,svc: Service = Depends(get_service), jwt_data: JWTData = Depends(parse_jwt_user_data)):
    svc.repository.delete_pic(id, jwt_data.user_id)
    return Response(status_code=200)