

from uuid import UUID


class MenuEntity:
    def __init__(self, id: UUID, name: str, description: str, category: str):
        self.id = id
        self.name = name
        self.description = description
        self.category = category

    def __repr__(self):
        return f"Menu(id={self.id}, name={self.name}, description={self.description})"

    def __eq__(self, other):
        if not isinstance(other, MenuEntity):
            return False
        return self.id == other.id