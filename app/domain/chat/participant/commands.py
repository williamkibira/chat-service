from typing import NamedTuple

from app.domain.chat.types import ResponseType


class DeviceBroadcastCommand(NamedTuple):
    participant_identifier: str
    unique_identifier: str
    response_type: ResponseType
    payload: bytearray


class MessageDispatchCommand(NamedTuple):
    participant_identifier: str
    payload: bytearray
    response_type: ResponseType
