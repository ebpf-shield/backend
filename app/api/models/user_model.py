from beanie import Document
from pydantic import BaseModel, Field


class User(BaseModel):
    name: str
    email: str
    password: str


class UserRegister(BaseModel):
    name: str = Field(min_length=4, max_length=50)
    password: str = Field(min_length=8, max_length=50)
    email: str = Field(min_length=8, max_length=50)


class UserLogin(BaseModel):
    email: str = Field(min_length=8, max_length=50)
    password: str = Field(min_length=8, max_length=50)


class UserDocument(Document, User):
    pass

    class Settings:
        name = "users"
