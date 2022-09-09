from domain.service import NotificationService
from ...schema import EventSchema
from .base import BaseConsumer
from .error import error_handler


class EventConsumer(BaseConsumer):
    def __init__(self, service: NotificationService):
        super().__init__()
        self._service = service
        self._schema = EventSchema()

    @error_handler
    def process(self, message: any):
        event = self._schema.loads(message.value())
        self._service.notify(event)
