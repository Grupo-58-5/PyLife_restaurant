


from datetime import date, timedelta
from typing import Annotated, Final, List
from fastapi import APIRouter, Depends
from fastapi import HTTPException
from uuid import UUID

from src.auth.infraestructure.JWT.JWT_auth_adapter import JWTAuthAdapter
from src.auth.infraestructure.JWT.dependencies.verify_scope import VerifyScope
from src.dashboard.application.schemas.entry.get_top_dishes_entry_schema import GetTopDishesEntrySchema
from src.dashboard.application.schemas.entry.reservations_per_day_entry import ReservationsPerDayEntry
from src.dashboard.application.schemas.response.occupancy_restaurant_response import OccupancyItemResponse
from src.dashboard.application.schemas.response.reservations_per_day_response import ReservationsPerDayItemResponse
from src.dashboard.application.schemas.response.top_dishes_response_schema import TopDishesResponseSchema
from src.dashboard.application.services.query.get_occupancy_by_restaurant_id_application_service import GetOccupancyByRestaurantIdApplicationService
from src.dashboard.application.services.query.get_reservations_per_day_application_service import GetReservationsPerDayApplicationService
from src.dashboard.application.services.query.get_top_dishes_preorder_service import GetTopDishesPreorderService
from src.reservations.infraestructure.repository.reservation_repository_impl import ReservationRepositoryImpl
from src.restaurants.infraestructure.repository.restaurant_repository_impl import RestaurantRepositoryImpl
from src.shared.db.database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession

from src.shared.utils.result import Result


async def get_restaurant_repository(session: AsyncSession = Depends(get_session)) -> RestaurantRepositoryImpl:
    """Get an instance of the RestaurantRepositoryImpl. """
    return RestaurantRepositoryImpl(db=session)

async def get_repository_reservation(session: AsyncSession = Depends(get_session)) -> ReservationRepositoryImpl:
    """Get an instance of the ReservationRepositoryImpl. """
    print("Session utilizado: ",session)
    return ReservationRepositoryImpl(db=session)

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])
auth: Final = JWTAuthAdapter()

@router.get(
    "/top-dishes-preorder",
    summary="Get Top Dishes Preorder",
    response_model=List[TopDishesResponseSchema],
    status_code=200,
    dependencies=[Depends(VerifyScope(["admin:read","admin:write"], JWTAuthAdapter()))]
)
async def get_top_dishes_preorder(
    info: Annotated[Result[dict], Depends(auth.decode)],
    query: GetTopDishesEntrySchema = Depends(),
    repo_reservation: ReservationRepositoryImpl = Depends(get_repository_reservation),
    repo_restaurant: RestaurantRepositoryImpl = Depends(get_restaurant_repository)
):
    """
    Retrieve the top dishes preordered for a specific restaurant within a date range.
    """
    service = GetTopDishesPreorderService(repo_reservation, repo_restaurant)
    res = await service.execute(query)
    
    if res.is_succes():
        return res.result()
    else:
        raise HTTPException(status_code=res.get_error_code(),detail={'msg':str(res.get_error_message())})

@router.get(
    "/reservations",
    summary="Get reservations per day",
    response_model=List[ReservationsPerDayItemResponse],
    status_code=200,
    dependencies=[Depends(VerifyScope(["admin:read"], auth))]
)
async def get_reservations_per_day(
    info: Annotated[Result[dict], Depends(auth.decode)],
    query: ReservationsPerDayEntry = Depends(),
    reservation_repo: ReservationRepositoryImpl = Depends(get_repository_reservation)
):
    service = GetReservationsPerDayApplicationService(reservation_repo)
    res = await service.execute((query.start_date, query.end_date, query.group_by))

    if res.is_error():
        raise HTTPException(status_code=res.get_error_code(), detail={"msg": res.get_error_message()})
    return res.result()

@router.get(
    "/occupancy/{restaurant_id}",
    summary="Get occupancy percentage for a specific restaurant",
    response_model=OccupancyItemResponse,
    status_code=200,
    dependencies=[Depends(VerifyScope(["admin:read", "admin:write"], auth))]
)
async def occupancy_restaurant_admin(
    restaurant_id: UUID,
    info: Annotated[Result[dict], Depends(auth.decode)],
    restaurant_repo: RestaurantRepositoryImpl = Depends(get_restaurant_repository)
):
    service = GetOccupancyByRestaurantIdApplicationService(restaurant_repo)
    res = await service.execute(restaurant_id)

    if res.is_error():
        raise HTTPException(
            status_code=res.get_error_code(), detail={"msg": str(res.get_error_message())})
    return res.result()
