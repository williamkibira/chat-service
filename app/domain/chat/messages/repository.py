import abc
from datetime import datetime
from typing import List


class MessageRepository(abc.ABC):

    @abc.abstractmethod
    def add_message(self, sender: str, target: str, payload: bytearray, received_at: datetime, node: str) -> None:
        pass

    @abc.abstractmethod
    def fetch_message_group_messages(self, group_identifier: str, limit: int, offset: int) -> List:
        pass

    @abc.abstractmethod
    def fetch_participant_messages(self, participant_identifier: str, limit: int, offset: int) -> List:
        pass

    @abc.abstractmethod
    def remove_participant_message(self, participant_identifier: str, message_identifier: str) -> None:
        pass
