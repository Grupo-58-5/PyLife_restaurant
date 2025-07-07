from typing import Awaitable, Callable, Dict, List

class SingletonMeta(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class EventBus(metaclass=SingletonMeta):
    
    def __init__(self):
        self.subscribers: Dict[str, List[Callable[[str], Awaitable[None]]]] = {}

    async def publish(self, message: str,name: str) -> None:
        subscribers = self.subscribers.get(name, [])
        for subscriber in subscribers:
            await subscriber(message)

    async def subscribe(self, event_name: str, callback: Callable[[str], Awaitable[None]]):
        if event_name not in self.subscribers:
            self.subscribers[event_name] = []
        self.subscribers[event_name].append(callback)

