import abc
from typing import Optional, Callable

from google.protobuf.message import Message

from app.domain.chat.participant.identification_pb2 import Details


class ParticipantClient(abc.ABC):
    subscription_methods = {}
    subscription_events = {}

    @abc.abstractmethod
    def fetch_details(self, identifier: str) -> Optional[Details]:
        pass

    @abc.abstractmethod
    def shutdown(self):
        pass

    @abc.abstractmethod
    def start_up(self):
        pass

    @abc.abstractmethod
    def register_subscriber(self, subject: str, event: Message, handler_callback: Callable):
        pass

