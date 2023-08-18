from datetime import datetime
from typing import Optional

from bson.objectid import ObjectId
from pymongo.database import Database

from ..utils.security import hash_password


class AuthRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_user(self, user: dict):
        payload = {
            "email": user["email"],
            "password": hash_password(user["password"]),
            "created_at": datetime.utcnow(),
        }

        self.database["users"].insert_one(payload)

    def get_user_by_id(self, user_id: str) -> Optional[dict]:
        user = self.database["users"].find_one(
            {
                "_id": ObjectId(user_id),
            }
        )
        return user

    def get_user_by_email(self, email: str) -> Optional[dict]:
        user = self.database["users"].find_one(
            {
                "email": email,
            }
        )
        return user
    def update_user(self, user_id: str, data: dict):
        self.database["users"].update_one(
            filter={"_id": ObjectId(user_id)},
            update={
                "$set": {
                    "phone": data["phone"],
                    "name": data["name"],
                    "city": data["city"],
                }
            },
        )
    def add_to_favorites(self, id:str, user_id:str):
        shanyraks=self.database["shanyraks"].find_one({"_id": ObjectId(id)})
        self.database["users"].update_one(
            filter={"_id": ObjectId(user_id)}, 
            update={"$addToSet": {
                "shanyraks":shanyraks}
            })
        
    def get_favorites(self,user_id:str):
        a=self.database["users"].find_one({"_id": ObjectId(user_id)})
        shanyraks= a["shanyraks"]  
        shanyraks = [
            {
            "_id": str(shanyrak["_id"]),
            "address": shanyrak["address"]
            }
            for shanyrak in shanyraks
        ]
        return shanyraks
    def delete_favorite(self, id:str, user_id:str):
        self.database["users"].update_one(
        filter={"_id": ObjectId(user_id)},
        update={"$pull": {"shanyraks": {"_id": ObjectId(id)}}}
    )
        

    def add_pfp(self, pic_url:str, user_id:str):
        filter={"_id":ObjectId(user_id)}
        self.database["users"].update_one(filter, update={"$set":{"pic":pic_url}})
    def delete_pfp(self, user_id:str):
        filter={"_id":ObjectId(user_id)}
        self.database["users"].update_one(filter, update={"$set":{"pic":""}}) 