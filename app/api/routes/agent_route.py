from fastapi import APIRouter

router = APIRouter()


@router.get("", description="Get all agents")
async def get_all_agents():
    return "a"
