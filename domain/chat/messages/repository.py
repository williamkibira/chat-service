import abc
from typing import List

from domain.chat.messages.contract import Message


class MessageRepository(abc.ABC):

    @abc.abstractmethod
    def add_message(self, message: Message):
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
