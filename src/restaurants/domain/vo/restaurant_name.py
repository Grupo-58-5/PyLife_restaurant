


class RestaurantName():
    def __init__(self, name: str):
        self.validate(name)
        """Initializes a RestaurantName instance."""
        self._name = name


    def validate(self, name) -> None:
        """Validates the restaurant name."""
        if not name or len(name) < 3 or len(name) > 30:
            raise ValueError("Restaurant name must be between 3 and 30 characters long")
        
    @classmethod
    def create(cls, name: str) -> "RestaurantName":
        """Factory method to create a RestaurantName instance."""
        return cls(name)
    
    def get_name(self) -> str:
        return self._name

    def __str__(self) -> str:
        return self._name

    def __eq__(self, other) -> bool:
        if not isinstance(other, RestaurantName):
            return False
        return self._name == other._name