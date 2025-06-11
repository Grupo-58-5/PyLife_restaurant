


class RestaurantAddress():
    def __init__(self, address: str):
        """Validates and initializes a RestaurantAddress instance."""
        self.validate(address)
        """Initializes a RestaurantAddress instance."""
        self._address = address

    @classmethod
    def create(cls, address: str) -> "RestaurantAddress":
        """Factory method to create a RestaurantAddress instance."""
        return cls(address)
    
    def get_address(self) -> str:
        """Returns the address."""
        return self._address

    def validate(self, address: str) -> None:
        """Validates the restaurant address."""
        if not address or len(address) < 3 or len(address) > 200:
            raise ValueError("Restaurant address must be between 3 and 200 characters long")
    
    def __str__(self):
        return f"{self._address}"

    def __eq__(self, other):
        if not isinstance(other, RestaurantAddress):
            return False
        return (self._address == other._address)