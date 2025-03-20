from typing import Optional
from beanie import Document, PydanticObjectId
from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    _id: Optional[PydanticObjectId] = Field(alias="_id")
    name: str
    email: EmailStr
    password: str


class UserRegister(BaseModel):
    name: str = Field(min_length=4, max_length=50)
    password: str = Field(min_length=8, max_length=50)
    email: EmailStr = Field(min_length=8, max_length=50)


class UserLogin(BaseModel):
    email: EmailStr = Field(min_length=8, max_length=50)
    password: str = Field(min_length=8, max_length=50)


class UserDocument(Document, User):
    pass

    class Settings:
        name = "users"
