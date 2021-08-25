import abc
from typing import Optional, Callable, T, Type

from app.domain.chat.participant.identification_pb2 import Details


class ParticipantClient(abc.ABC):
    subscription_methods = {}
    subscription_events = {}
    subscribers = {}
    subscription_classes = {}

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
    def register_subscription_handler(
            self,
            subject: str,
            event_type: Type[T],
            handler_callback: Callable,
            subscriber: str):
        pass

    def register_subscriber(self, subscriber: T = None) -> None:
        self.subscribers[str(subscriber.__class__.__name__)] = subscriber
