from fastapi import APIRouter
from crud.todo import todo_crud
from schemas import todo as todo_schema

router = APIRouter(prefix="/todos", tags=["Todos"])


@router.post("/create")
def create_todo(todo: todo_schema.TodoCreate):
    return todo_crud.create_todo(todo)


@router.get("/show")
def get_todo():
    return todo_crud.get_todos()

@router.get("/show/{id}")
def get_todo_by_id(id: str):
    return todo_crud.get_todo_by_id(id)

@router.post("/delete/{id}")
def delete_todo(id: str):
    return todo_crud.remove_todo(id)

@router.post("/show/{priority}")
def filter_todo_by_priority(priority: str):
    return todo_crud.filter_by_priority(priority)

@router.put("/edit_todo/{id}")
def edit_todo(id: str, updated_data: todo_schema.TodoUpdate):
    return todo_crud.edit_todo(id, updated_data)

@router.post("/mark_complete/{id}")
def mark_as_complete(id: str):
    return todo_crud.mark_as_complete(id)