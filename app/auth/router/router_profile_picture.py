from typing import Any, List, Optional

from fastapi import Depends, UploadFile, File
from pydantic import Field


from app.utils import AppModel

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service

from . import router




@router.post("/users/avatar")
def add_pfp(
    file:UploadFile,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service)
):
    url = svc.s3_service.upload_file(file.file, file.filename)
    svc.repository.add_pfp(url,jwt_data.user_id)


@router.delete("/users/avatar")
def delete_pfp(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service)
):
    url=svc.repository.get_user_by_id(jwt_data.user_id)
    pic=url["pic"]
    parts = pic.split("/")
    bucket = parts[3]
    file_key = "/".join(parts[4:])
    svc.s3_service.delete_file(bucket, file_key)
    svc.repository.delete_pfp(jwt_data.user_id)