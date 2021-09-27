import abc
from typing import Optional, Callable, T, Type

from app.domain.chat.participant.node_pb2 import ParticipantPassOver


class ParticipantClient(abc.ABC):
    subscription_methods = {}
    subscription_events = {}
    subscribers = {}
    subscription_classes = {}

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

    @abc.abstractmethod
    def fetch_last_known_node(self, target_identifier) -> Optional[str]:
        pass

    @abc.abstractmethod
    def register_participant(self, routing_identifier: str) -> None:
        pass

    @abc.abstractmethod
    def passover_direct_message_to(self, node: str, passover: ParticipantPassOver) -> None:
        pass
