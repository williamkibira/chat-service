from collections import Callable
from functools import wraps

from google.protobuf.message import Message

from app.core.logging.loggers import LoggerMixin
from app.domain.chat.participant.factory import get_client


class ParticipantPassOverListener(LoggerMixin):
    def __init__(self, event: Message):
        self.__subject = "v1/node/participants/pass-over"
        self.__event = event

    def __call__(self, fn: Callable):

        get_client().register_subscriber(
            subject="v1/node/participants/pass-over",
            event=self.__event,
            handler_callback=fn,
        )

        @wraps(fn)
        def wrapper(*args, **kwargs):
            return fn(*args, **kwargs)

        return wrapper


class NodeJoinedListener:
    def __init__(self, event: Message):
        self.__subject = "v1/node/joined"
        self.__event = event

    def __call__(self, fn: Callable):
        get_client().register_subscriber(
            subject=self.__subject,
            event=self.__event,
            handler_callback=fn,
        )

        @wraps(fn)
        def wrapper(*args, **kwargs):
            return fn(*args, **kwargs)

        return wrapper
