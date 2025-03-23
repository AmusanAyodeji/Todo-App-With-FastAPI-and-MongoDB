from serializers import todo as serializer
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from bson.objectid import ObjectId
from schemas.todo import TodoCreate, TodoUpdate
from database import todo_collection


class TodoCrud:

    @staticmethod
    def create_todo(todo_data: TodoCreate):
        if todo_data.priority.lower() not in ["low","medium","high"]:
            raise HTTPException(status_code=400, detail="Invalid Priority Input")
        todo_data.priority = todo_data.priority.lower()
        todo_data = jsonable_encoder(todo_data)
        todo_document_data = todo_collection.insert_one(todo_data)
        todo_id = todo_document_data.inserted_id
        todo = todo_collection.find_one({"_id": ObjectId(todo_id)})
        return serializer.todo_serializer(todo)
    
    @staticmethod
    def get_todos():
        todos = todo_collection.find()
        return serializer.todos_serializer(todos)
    
    @staticmethod
    def get_todo_by_id(id: str):
        if todo_collection.count_documents({"_id": ObjectId(id)}) == 0:
            raise HTTPException(status_code=400, detail=f"No todo with id:{id}")
        todo = todo_collection.find_one({"_id": ObjectId(id)})
        return serializer.todo_serializer(todo)

    @staticmethod
    def remove_todo(id: str):
        if todo_collection.count_documents({"_id": ObjectId(id)}) == 0:
            raise HTTPException(status_code=400, detail=f"No todo with id:{id}")
        
        todo_collection.delete_one({"_id": ObjectId(id)})
        return {"Message":"Todo Successfully Deleted"}

    @staticmethod
    def filter_by_priority(priority: str):
        if priority.lower() not in ["low","medium","high"]:
            raise HTTPException(status_code=400, detail="Invalid Priority Input")
        
        todos = todo_collection.find({"priority": priority})

        if todo_collection.count_documents({"priority": priority}) == 0:
            raise HTTPException(status_code=400, detail=f"No todo with {priority.lower()} priority level")
        
        return serializer.todos_serializer(todos)

    @staticmethod
    def edit_todo(id: str, updated_todo: TodoUpdate):
        if todo_collection.count_documents({"_id": ObjectId(id)}) == 0:
            raise HTTPException(status_code=400, detail=f"No todo with id:{id}")
        updated_data = {
            "user_id": updated_todo.user_id,
            "title": updated_todo.title,
            "description": updated_todo.description,
            "is_completed": updated_todo.is_completed,
            "priority": updated_todo.priority
        }
        todo_collection.update_one({"_id": ObjectId(id)}, {"$set":updated_data})

        return "Todo Successfully Edited"

    @staticmethod
    def mark_as_complete(id: str):
        if todo_collection.count_documents({"_id": ObjectId(id)}) == 0:
            raise HTTPException(status_code=400, detail=f"No todo with id:{id}")
        
        todo_collection.update_one({"_id": ObjectId(id)}, {"$set":{"is_completed": True}})
        return "Todo marked as complete"


todo_crud = TodoCrud()
