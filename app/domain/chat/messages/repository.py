import abc
from datetime import datetime
from typing import List


class MessageRepository(abc.ABC):

    @abc.abstractmethod
    def save(self, sender: str, target: str, payload: bytearray, received_at: datetime, node: str, marker: str) -> None:
        pass

    @abc.abstractmethod
    def fetch_for_group(self, group_identifier: str, limit: int, offset: int) -> List:
        pass

    @abc.abstractmethod
    def fetch_for_participant(self, participant_identifier: str, limit: int, offset: int) -> List:
        pass

    @abc.abstractmethod
    def remove_for_participant(self, participant_identifier: str, message_identifier: str) -> None:
        pass
