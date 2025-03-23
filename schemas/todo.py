from pydantic import BaseModel


class TodoBase(BaseModel):
    user_id: str
    title: str
    description: str


class Todo(TodoBase):
    id: str


class TodoCreate(TodoBase):
    is_completed: bool = False
    priority: str

class TodoUpdate(TodoBase):
    is_completed: bool = False
    priority: str