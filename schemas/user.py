from pydantic import BaseModel
from datetime import datetime
from typing import Union


class UserBase(BaseModel):
    username: str


class User(UserBase):
    id: str
    created_at: Union[datetime, str] = datetime.now()


class UserCreate(UserBase):
    pass