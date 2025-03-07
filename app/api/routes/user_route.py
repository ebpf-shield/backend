from fastapi import APIRouter


router = APIRouter()


@router.get("", description="Get all users")
async def get_all_users():
    return "a"
