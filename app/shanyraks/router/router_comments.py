from typing import Any

from fastapi import Depends, Response
from pydantic import Field

from app.utils import AppModel

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service

from . import router
from datetime import datetime
from bson.objectid import ObjectId

class Comment(AppModel):
    # _id:str
    content: str
    created_at: str
    author_id: str
    shanyrak_id:str
# class Property(Appmodel):
#     # Other fields of the property model
#     comments: List[Comment]



#comments are added but are returned empty
@router.post("/{shanyrak_id}/comments")
def add_comment(
    shanyrak_id:str, 
    content:str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service)):
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    comment = Comment(
        # _id=str(ObjectId()),
        content=content,
        created_at=created_at,
        author_id=jwt_data.user_id,
        shanyrak_id=shanyrak_id
    )
    svc.repository.add_comment(comment.dict(by_alias=True))
    # if svc.repository.add_comment(comment.dict()):
    #     return {"message": "Comment added successfully"}
    # else:
    #     return {"message": "Failed to add comment"}

@router.get("/{shanyrak_id}/comments")
def get_comments(
    shanyrak_id:str,
    svc: Service = Depends(get_service)):
    return svc.repository.get_comments(shanyrak_id)

@router.patch("/{shanyrak_id}/comments/{comment_id}")
def update_comment(
    shanyrak_id:str,
    comment_id:str,
    content:str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service)):
    return svc.repository.update_comment(shanyrak_id, comment_id, jwt_data.user_id,content)

@router.delete("/{shanyrak_id}/comments/{comment_id}")
def delete_comment(
    shanyrak_id:str,
    comment_id:str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service)):
    return svc.repository.delete_comment(shanyrak_id, comment_id, jwt_data.user_id)