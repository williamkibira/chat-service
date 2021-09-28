from typing import NamedTuple


class NodeJoinedEvent(NamedTuple):
    identifier: str


class ParticipantEvent(NamedTuple):
    sender_identifier: str
    target_identifier: str
    payload: bytearray
    originating_node: str
