from uuid import UUID


class ReservationDishVO:
    def __init__(self, menu_id: UUID, name: str):
        '''Use the create method insted of this'''
        self.menu_id = menu_id
        self.name = name

    @classmethod
    def create(cls, menu_id: UUID, name: str):
        """Factory method to create a ReservationScheReservationDishesVOdule instance."""
        return cls(menu_id, name)

    def get_menu_id(self) -> UUID:
        return self.menu_id
    
    def get_name(self) -> str:
        return self.name