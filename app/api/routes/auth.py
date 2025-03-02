from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.api.services.auth_service import authenticate_user, create_access_token
from pydantic import BaseModel

router = APIRouter()


class UserRegister(BaseModel):
    email: str
    password: str


@router.post("/register")
def register(user: UserRegister):
    # Placeholder for user registration logic
    return {"message": "User registered successfully"}


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    access_token = create_access_token({"sub": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}
