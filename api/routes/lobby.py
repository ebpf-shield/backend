from fastapi import APIRouter, Depends
from api.services.auth_service import get_current_user

router = APIRouter()

@router.get("/")
def lobby(user: str = Depends(get_current_user)):
    return {"message": f"Welcome to the lobby, {user}!"}
