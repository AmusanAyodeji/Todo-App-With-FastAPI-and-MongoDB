from serializers import user as serializer
from datetime import datetime
from fastapi.encoders import jsonable_encoder
from bson.objectid import ObjectId
from schemas.user import UserCreate
from database import user_collection
from fastapi import HTTPException


class UserCrud:

    @staticmethod
    def create_user(user_data: UserCreate):
        if user_collection.count_documents({"username": user_data.username}) > 0:
            raise HTTPException(status_code=400, detail=f"Username Taken")
        user_data = jsonable_encoder(user_data)
        user_data["created_at"] = datetime.now()
        user_document_data = user_collection.insert_one(user_data)
        user_id = user_document_data.inserted_id
        user = user_collection.find_one({"_id": ObjectId(user_id)})
        return serializer.user_serializer(user)

    @staticmethod
    def delete_user(id: str):
        if user_collection.count_documents({"_id": ObjectId(id)}) == 0:
            raise HTTPException(status_code=400, detail=f"No user with id:{id}")
        
        user_collection.delete_one({"_id": ObjectId(id)})
        return "User Successfully deleted"

    @staticmethod
    def show_users():
        users = user_collection.find()
        return serializer.users_serializer(users)
    
    @staticmethod
    def get_user_by_id(id: str):
        if user_collection.count_documents({"_id": ObjectId(id)}) == 0:
            raise HTTPException(status_code=400, detail=f"No user with id:{id}")
        user = user_collection.find_one({"_id": ObjectId(id)})
        return serializer.user_serializer(user)

user_crud = UserCrud()
