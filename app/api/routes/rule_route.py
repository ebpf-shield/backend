from fastapi import APIRouter


router = APIRouter(tags=["rules"])


@router.get("", description="Get all rules")
async def get_all_rules():
    return "a"
