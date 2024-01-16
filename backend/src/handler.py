import random
from fastapi import HTTPException
from src.cooldown import CooldownManager
from src.models import IncomingEvent, Event, OutgoingAction, Action
from typing import Callable, TypeVar, Awaitable
from src.queue import Queue
from src.config import global_config

T = TypeVar("T", bound=IncomingEvent)


class EventHandler:
    def __init__(self):
        self._handlers: dict[Event, Callable[[T], OutgoingAction]] = {}
        self._cd_manager = CooldownManager()
        self._queue = Queue()

    def register(
            self, event: Event
    ) -> Callable[[Callable[[T], OutgoingAction]], Callable[[T], OutgoingAction]]:
        def decorator(func: Callable[[T], OutgoingAction]) -> Callable[[T], OutgoingAction]:
            self._handlers[event] = func
            return func

        return decorator

    def handle(self, event: IncomingEvent) -> OutgoingAction:
        handler = self._handlers.get(event.event)
        if not handler:
            raise HTTPException(status_code=404, detail="Evento não encontrado")

        outgoing_action = handler(event)
        self._queue.put(outgoing_action.data["text"])

        if self._cd_manager.check_all_cooldown(event.event):
            return OutgoingAction(
                action=Action.IGNORE,
                data={"text": "Aguardando cooldown"},
            )

        outgoing_action.data["text"] = "\n".join(self._queue.all())
        print(self._queue.all())
        self._queue.clear()

        self._cd_manager.add_cooldown(
            event.event,
            global_config.cooldown_individual * 60,
        )  # Individual cd, 5 min

        self._cd_manager.add_cooldown(
            "GLOBAL_COOLDOWN", global_config.cooldown_global + random.randint(0, 30)
        )  # Global cd, 30 sec to 1 min

        return outgoing_action


event_handler = EventHandler()
