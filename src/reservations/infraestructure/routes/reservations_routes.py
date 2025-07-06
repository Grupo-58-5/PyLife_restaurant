import logging
from typing import Annotated, Final, List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.application.schemas.entry.user_all_schema_entry import UserAllSchemaEntry
from src.auth.infraestructure.JWT.JWT_auth_adapter import JWTAuthAdapter
from src.auth.infraestructure.JWT.dependencies.verify_scope import VerifyScope
from src.auth.infraestructure.repository.user_repository_impl import UserRepositoryImpl
from src.notifications.infraestructure.notifier.notifier import Notifier
from src.reservations.application.schemas.entry.cancel_reservation_schema_entry import CancelReservationSchemaEntry
from src.reservations.application.schemas.entry.get_application_schema_entry import GetReservationsSchemaEntry
from src.reservations.application.schemas.entry.get_reservations_by_user_schema_entry import GetReservationsByUserSchemaEntry
from src.reservations.application.schemas.entry.reservation_schema_entry import ChangeStatusSchemaEntry, ReservationSchemaEntry, ReservationStatus
from src.reservations.application.schemas.response.get_reservations_by_user_schema_response import GetReservationsByUserSchemaResponse
from src.reservations.application.schemas.response.reservation_schema_response import AllReservationsResponse, ReservationResponse, ReservationSchemaResponse
from src.reservations.application.services.command.cancel_reservation_service import CancelReservationService
from src.reservations.application.services.command.change_status_reservation_service import ChangeReservationStatusApplicationService
from src.reservations.application.services.command.create_reservation_service import CreateReservationService
from src.reservations.application.services.query.get_active_reservations_user_service import GetActiveReservationsUserService
from src.reservations.application.services.query.get_reservations_filtered_service import GetReservationsFilteredApplicationService
from src.reservations.infraestructure.repository.reservation_repository_impl import ReservationRepositoryImpl
from src.reservations.infraestructure.schemas.entry.create_reservation_schema_entry import CreateReservationSchemaEntry
from src.restaurants.infraestructure.repository.menu_repository_impl import MenuRepositoryImpl
from src.restaurants.infraestructure.repository.restaurant_repository_impl import RestaurantRepositoryImpl
from src.restaurants.infraestructure.repository.table_repository_impl import TableRepositoryImpl
from src.shared.db.database import get_session
from src.shared.utils.result import Result
from src.shared.utils.event_bus import EventBus

async def get_repository_client(session: AsyncSession = Depends(get_session)) -> UserRepositoryImpl:
    """Get an instance of the UserRepositoryImpl. """
    return UserRepositoryImpl(db=session)

async def get_repository_restaurant(session: AsyncSession = Depends(get_session)) -> RestaurantRepositoryImpl:
    """Get an instance of the RestaurantRepositoryImpl. """
    return RestaurantRepositoryImpl(db=session)

async def get_repository_table(session: AsyncSession = Depends(get_session)) -> TableRepositoryImpl:
    """Get an instance of the TableRepositoryImpl. """
    return TableRepositoryImpl(db=session)

async def get_repository_menu(session: AsyncSession = Depends(get_session)) -> MenuRepositoryImpl:
    """Get an instance of the MenuRepositoryImpl. """
    return MenuRepositoryImpl(db=session)

async def get_repository_reservation(session: AsyncSession = Depends(get_session)) -> ReservationRepositoryImpl:
    """Get an instance of the ReservationRepositoryImpl. """
    return ReservationRepositoryImpl(db=session)

router: Final = APIRouter(
    prefix="/reservation",
    tags=["Reservation"]
)

auth: Final = JWTAuthAdapter()
event_bus = EventBus()
notifier = Notifier(logger=logging.getLogger("uvicorn"))
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

    async def handler(message: str):
        await notifier.notify_info(message)

    await event_bus.subscribe("ReservationCreated", handler)

    service = CreateReservationService(
        reservation_repository=repo_reservation,
        restaurant_repository=repo_restaurant,
        event_bus=event_bus
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

    async def handler(message: str):
        await notifier.notify_info(message)

    await event_bus.subscribe("ReservationCanceled", handler)

    service = CancelReservationService(
        repo_reservation=repo_reservation,
        event_bus=event_bus
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

@router.get(
    '/admin/{restaurant_id}',
    response_model=AllReservationsResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(VerifyScope(["admin:read","admin:write"],JWTAuthAdapter()))],
    description="Get all reservations with filter options and pagination",
)
async def get_restaurant_reservations(
    restaurant_id: UUID,
    info: Annotated[Result[dict],Depends(auth.decode)],
    repo_reservation: ReservationRepositoryImpl = Depends(get_repository_reservation),
    repo_restaurant: RestaurantRepositoryImpl = Depends(get_repository_restaurant),
    query: GetReservationsSchemaEntry = Depends(),
):
    service = GetReservationsFilteredApplicationService(restaurant_repo=repo_restaurant, reservation_repo=repo_reservation)
    response: Result[AllReservationsResponse] = await service.execute(
        data=[restaurant_id, query]
    )
    if response.is_error():
        raise HTTPException(status_code=response.get_error_code(), detail=response.get_error_message())
    else:
        return response.result()

@router.patch(
    '/admin/change_status/{reservation_id}',
    response_model=ReservationSchemaResponse,
    status_code=status.HTTP_202_ACCEPTED,
    dependencies=[Depends(VerifyScope(["admin:read","admin:write"],JWTAuthAdapter()))],
    description="Change the status of a reservation",
    responses={
        400: {"description": "Invalid data"},
        403: {"description": "Forbidden"},
        500: {"description": "Internal Error"}
    }
)
async def change_status_reservation(
    info: Annotated[Result[dict], Depends(auth.decode)],
    reservation_id: UUID,
    query: ChangeStatusSchemaEntry = Depends(),
    repo_reservation: ReservationRepositoryImpl = Depends(get_repository_reservation),
):
    
    service = ChangeReservationStatusApplicationService(repo_reservation)
    res: Result[ReservationSchemaResponse] = await service.execute(
        data=[reservation_id, query]
    )
    if res.is_error():
        raise HTTPException(status_code=res.get_error_code(), detail=res.get_error_message())
    else:
        return res.result()

