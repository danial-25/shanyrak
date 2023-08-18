from typing import Any,List
import logging
from bson.objectid import ObjectId
from pymongo.database import Database
from pymongo.results import DeleteResult, UpdateResult
from fastapi import Response,Depends
class ShanyrakRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_shanyrak(self, user_id: str, data: dict[str, Any]):
        data["user_id"] = ObjectId(user_id)
        insert_result = self.database["shanyraks"].insert_one(data)
        return insert_result.inserted_id

    def get_shanyrak(self, shanyrak_id: str):
        # from ..service import Service, get_service
        return self.database["shanyraks"].find_one({"_id": ObjectId(shanyrak_id)})

    def serialize_location(self, location:dict):
        return {
            "type": location["type"],
            "coordinates": location["coordinates"]
        }

    def list_shanyraks(self, limit, offset, rooms_count, price_from, price_until,latitude=None, longitude=None, radius=None):
        # cursor= self.database["shanyraks"].find()
        filter_query = {}

        if rooms_count is not None:
            filter_query["rooms_count"] = {"$gt": rooms_count}
        
        if price_until is not None:
            if price_from is not None:
                filter_query["price"] = {"$gt": price_from, "$lt": price_until}
            else:
                filter_query["price"] = {"$lt": price_until}
        if price_from is not None:
            if price_until is not None:
                filter_query["price"] = {"$gt": price_from, "$lt": price_until}
            else:
                filter_query["price"] = {"$gt": price_from}
        if latitude is not None and longitude is not None and radius is not None:
            filter_query["location"] = {
                "$geoWithin": {
                    "$centerSphere": [[longitude, latitude], radius / 6371]  # Divide radius by the Earth's radius in kilometers (6371 km)
                }
            }
        logging.info(f"{longitude}, {latitude}")
        cursor = self.database["shanyraks"].find(filter_query).limit(limit).skip(offset).sort("created_at")
        shanyraks = []
        for obj in cursor:
            obj["_id"]= str(obj["_id"])  # Convert ObjectId to string
            obj["user_id"]=str(obj["user_id"])
            obj["location"] = self.serialize_location(obj["location"])
            shanyraks.append(obj)
        logging.info(f"Retrieved {len(shanyraks)} documents")
        return shanyraks


    def add_comment(self, content:dict[str, Any]):
        try:
            inserted_result = self.database["comments"].insert_one(content)
            return inserted_result.inserted_id is not None
        except Exception as e:  
            print(f"Error occurred while adding comment: {str(e)}")
            return False
    def get_comments(self, shanyrak_id:str)-> List[Any]:
        filter = {"shanyrak_id": shanyrak_id}
        objects=self.database["comments"].find(filter)
        comments = []
        for obj in objects:
            obj["_id"]= str(obj["_id"])  # Convert ObjectId to string
            comments.append(obj)
        return comments
    
    def update_comment(self, shanyrak_id:str, comment_id:str, user_id:str, content:str):
        filter={"shanyrak_id":shanyrak_id, "_id":ObjectId(comment_id)}
        if self.database["comments"].find_one(filter).get("author_id")==user_id:
            self.database["comments"].update_one(filter, update={"$set":{"content":content}})
            return Response(status_code=200)
        return Response(status_code=403)

    def delete_comment(self, shanyrak_id:str, comment_id:str, user_id:str):
        filter={"shanyrak_id":shanyrak_id, "_id":ObjectId(comment_id)}
        if self.database["comments"].find_one(filter).get("author_id")==user_id:
            self.database["comments"].delete_one(filter)
            return Response(status_code=200)
        return Response(status_code=404)






    def update_shanyrak(self, shanyrak_id: str, user_id: str, data: dict[str, Any]) -> UpdateResult:
        filter={"_id":ObjectId(shanyrak_id), "user_id":ObjectId(user_id)}
        return self.database["shanyraks"].update_one(filter, update={"$set":data},)
    
    def update_pic(self, shanyrak_id: str, user_id: str, data: str) -> UpdateResult:
        filter={"_id":ObjectId(shanyrak_id), "user_id":ObjectId(user_id)}
        return self.database["shanyraks"].update_one(filter, update={"$push":{"pic":data}})

    def delete_pic(self, shanyrak_id: str, user_id: str) -> DeleteResult:
        filter={"_id":ObjectId(shanyrak_id), "user_id":ObjectId(user_id)}
        return self.database["shanyraks"].update_one(filter, update={"$set":{"pic":[]}})

    def delete_shanyrak(self, shanyrak_id: str, user_id: str) -> DeleteResult:
        filter={"_id":ObjectId(shanyrak_id), "user_id":ObjectId(user_id)}
        return self.database["shanyraks"].delete_one(filter)
