from beanie import Document
from pydantic import BaseModel


class User(BaseModel):
    name: str
    age: int
    email: str
    password: str


class UserDocument(Document, User):
    pass

    class Settings:
        name = "users"
