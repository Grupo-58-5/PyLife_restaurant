from fastapi import APIRouter

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])


@router.get("/")
async def get_restaurants():
    """
    Get all restaurants.
    """
    return {"message": "List of restaurants"}