from typing import List, Optional

from pydantic import BaseModel, EmailStr
from graphene_sqlalchemy import SQLAlchemyObjectType

from . import models

class Line(BaseModel):
    id: int

    created_at: str
    modified_at: str
    
    user_id: int
    line: str

    class Config:
        orm_mode = True


class Area(BaseModel):
    id: int

    created_at: str
    modified_at: str
    
    user_id: int
    area: str

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    email: EmailStr
    token: str

    class Config:
        orm_mode = True


class User(UserBase):
    id: int
    
    lines: List[Line] = []
    areas: List[Area] = []

    class Config:
        orm_mode = True


class UserSchema(SQLAlchemyObjectType):
    class Meta:
        model = models.User

