from uuid import UUID
from src.auth.application.schemas.entry.user_all_schema_entry import UserAllSchemaEntry


class GetReservationsByUserSchemaEntry(UserAllSchemaEntry):
    """Schema to get all active reservations by a user in the database."""

    client_id: UUID