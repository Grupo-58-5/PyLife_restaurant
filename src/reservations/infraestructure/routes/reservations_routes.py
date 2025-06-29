from typing import Annotated, Final, List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.application.schemas.entry.user_all_schema_entry import UserAllSchemaEntry
from src.auth.infraestructure.JWT.JWT_auth_adapter import JWTAuthAdapter
from src.auth.infraestructure.JWT.dependencies.verify_scope import VerifyScope
from src.auth.infraestructure.repository.user_repository_impl import UserRepositoryImpl
from src.reservations.application.schemas.entry.cancel_reservation_schema_entry import CancelReservationSchemaEntry
from src.reservations.application.schemas.entry.get_reservations_by_user_schema_entry import GetReservationsByUserSchemaEntry
from src.reservations.application.schemas.entry.reservation_schema_entry import ReservationSchemaEntry
from src.reservations.application.schemas.response.get_reservations_by_user_schema_response import GetReservationsByUserSchemaResponse
from src.reservations.application.schemas.response.reservation_schema_response import ReservationSchemaResponse
from src.reservations.application.services.command.cancel_reservation_service import CancelReservationService
from src.reservations.application.services.command.create_reservation_service import CreateReservationService
from src.reservations.application.services.query.get_active_reservations_user_service import GetActiveReservationsUserService
from src.reservations.infraestructure.repository.reservation_repository_impl import ReservationRepositoryImpl
from src.reservations.infraestructure.schemas.entry.create_reservation_schema_entry import CreateReservationSchemaEntry
from src.restaurants.infraestructure.repository.menu_repository_impl import MenuRepositoryImpl
from src.restaurants.infraestructure.repository.restaurant_repository_impl import RestaurantRepositoryImpl
from src.restaurants.infraestructure.repository.table_repository_impl import TableRepositoryImpl
from src.shared.db.database import get_session
from src.shared.utils.result import Result

async def get_repository_client(session: AsyncSession = Depends(get_session)) -> UserRepositoryImpl:
    """Get an instance of the UserRepositoryImpl. """
    print("Session utilizado: ",session)
    return UserRepositoryImpl(db=session)

async def get_repository_restaurant(session: AsyncSession = Depends(get_session)) -> RestaurantRepositoryImpl:
    """Get an instance of the RestaurantRepositoryImpl. """
    print("Session utilizado: ",session)
    return RestaurantRepositoryImpl(db=session)

async def get_repository_table(session: AsyncSession = Depends(get_session)) -> TableRepositoryImpl:
    """Get an instance of the TableRepositoryImpl. """
    print("Session utilizado: ",session)
    return TableRepositoryImpl(db=session)

async def get_repository_menu(session: AsyncSession = Depends(get_session)) -> MenuRepositoryImpl:
    """Get an instance of the MenuRepositoryImpl. """
    print("Session utilizado: ",session)
    return MenuRepositoryImpl(db=session)

async def get_repository_reservation(session: AsyncSession = Depends(get_session)) -> ReservationRepositoryImpl:
    """Get an instance of the ReservationRepositoryImpl. """
    print("Session utilizado: ",session)
    return ReservationRepositoryImpl(db=session)

router: Final = APIRouter(
    prefix="/reservation",
    tags=["Reservation"]
)

auth: Final = JWTAuthAdapter()

#NOTE: Endpoints para el cliente
@router.post(
    '/',
    response_model=ReservationSchemaResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(VerifyScope(["client:read","client:write"],JWTAuthAdapter()))],
    description="Made a reservation",
    responses={
        400: {"description": "Invalid data"},
        409: {"description": "Table already reserved at that time"}
    }
)
async def create_reservation(
    info: Annotated[Result[dict],Depends(auth.decode)],
    body: CreateReservationSchemaEntry,
    repo_reservation: ReservationRepositoryImpl = Depends(get_repository_reservation),
    repo_restaurant: RestaurantRepositoryImpl = Depends(get_repository_restaurant)
):
    client_id: str = info.value.get("id")
    data = ReservationSchemaEntry.model_validate({**body.model_dump(), "client_id": client_id})

    service = CreateReservationService(
        reservation_repository=repo_reservation,
        restaurant_repository=repo_restaurant
    )

    result = await service.execute(data)

    if result.is_error():
        raise HTTPException(status_code=result.get_error_code(),detail={'msg':str(result.get_error_message())})

    return result.value

@router.patch(
    '/cancel',
    response_model=str,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(VerifyScope(["client:read","client:write"],JWTAuthAdapter()))],
    description="Cancel a reservation",
    responses={
        403: {"description": "Forbidden"},
        500: {"description": "Internal Error"}
    }
)
async def cancel_reservation(
    info: Annotated[Result[dict],Depends(auth.decode)],
    reservation_id: str,
    repo_reservation: ReservationRepositoryImpl = Depends(get_repository_reservation)
):
    client_id: str = info.value.get("id")
    data = CancelReservationSchemaEntry.model_validate({"reservation_id": reservation_id, "client_id": client_id})

    service = CancelReservationService(
        repo_reservation=repo_reservation,
    )

    result = await service.execute(data)

    if result.is_error():
        raise HTTPException(status_code=result.get_error_code(),detail={'msg':str(result.get_error_message())})

    return result.value

@router.get(
    '/user/active',
    response_model=List[GetReservationsByUserSchemaResponse],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(VerifyScope(["client:read","client:write"],JWTAuthAdapter()))],
    description="Get active reservations per current user",
    responses={
        500: {"description": "Internal Error"}
    }
)
async def get_client_reservations(
    info: Annotated[Result[dict],Depends(auth.decode)],
    query: UserAllSchemaEntry = Depends(),
    repo_reservation: ReservationRepositoryImpl = Depends(get_repository_reservation),
    repo_restaurant: RestaurantRepositoryImpl = Depends(get_repository_restaurant),
    repo_table: TableRepositoryImpl = Depends(get_repository_table)
):
    client_id: str = info.value.get("id")
    data = GetReservationsByUserSchemaEntry.model_validate({
        **query.model_dump(), "client_id": client_id
    })

    service = GetActiveReservationsUserService(
        repo_reservation=repo_reservation,
        repo_restaurant=repo_restaurant,
        repo_table=repo_table
    )

    result = await service.execute(data)

    if result.is_error():
        raise HTTPException(status_code=result.get_error_code(),detail={'msg':str(result.get_error_message())})

    return result.value

#NOTE: Endpoints para el administrador
async def get_all_reservations():
    pass

async def cancel_any_reservation():
    pass

async def get_filter_reservations():
    pass
