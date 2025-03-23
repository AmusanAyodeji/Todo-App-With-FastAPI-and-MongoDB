from fastapi import APIRouter
from crud.user import user_crud
from schemas import user as user_schema

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/")
def create_user_endpoint(user: user_schema.UserCreate):
    return user_crud.create_user(user)

@router.get("/show")
def show_users():
    return user_crud.show_users()

@router.get("/show/{id}")
def get_user_by_id(id: str):
    return user_crud.get_user_by_id(id)

@router.delete("/delete/{id}")
def delete_user(id: str):
    return user_crud.delete_user(id)