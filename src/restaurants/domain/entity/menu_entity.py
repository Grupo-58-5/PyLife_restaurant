

from uuid import UUID


class MenuEntity():
    def __init__(self, id: UUID, name: str, description: str, category: str):
        self.id = id
        self._name = name
        self._description = description
        self._category = category

    def validate(self) -> None:
        """Validates the menu item."""
        if not self._name or len(self._name) < 3 or len(self._name) > 50:
            raise ValueError("Menu name must be between 3 and 50 characters long")
        if not self._description or len(self._description) < 10 or len(self._description) > 200:
            raise ValueError("Menu description must be between 10 and 200 characters long")
        if not self._category or len(self._category) < 3 or len(self._category) > 30:
            raise ValueError("Menu category must be between 3 and 30 characters long")

    def __repr__(self):
        return f"Menu(id={self.id}, name={self._name}, description={self._description})"

    def __eq__(self, other):
        if not isinstance(other, MenuEntity):
            return False
        return self.id == other.id
    
    @classmethod
    def create(cls, id: UUID, name: str, description: str, category: str) -> "MenuEntity":
        """Factory method to create a MenuEntity instance."""
        return cls(id, name, description, category)

    def get_id(self) -> UUID:
        return self.id
    
    @property
    def name(self) -> str:
        return self._name
    
    def get_name(self) -> str:
        return self._name
    
    @property
    def description(self) -> str:
        return self._description
    
    def get_description(self) -> str:
        return self._description
    
    @property
    def category(self) -> str:
        return self._category
    
    def get_category(self) -> str:
        return self._category
    
    @name.setter
    def name(self, value: str) -> None:
        if value is not None and (len(value) < 3 or len(value) > 50):
            raise ValueError("Menu name must be between 3 and 50 characters long")
        self._name = value
    
    @description.setter
    def description(self, value: str) -> None:
        if value is not None and (len(value) < 10 or len(value) > 200):
            raise ValueError("Menu description must be between 10 and 200 characters long")
        self._description = value
    
    @category.setter
    def category(self, value: str) -> None:
        if value is not None and (len(value) < 3 or len(value) > 30):
            raise ValueError("Menu category must be between 3 and 30 characters long")
        self._category = value
