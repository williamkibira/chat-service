from domain.chat.messages.contract import Message
from domain.chat.messages.repository import MessageRepository


class Participant(object):
    def __init__(self, repository: MessageRepository):
        self.__identifier = ""
        self.__nickname = ""
        self.__repository = repository

    def on_direct_message_data_received(self, data: bytes):
        # Persist the message, then send it off
        pass

    def on_group_message_received(self, identifier: str, message: Message):
        pass

    @property
    def nickname(self):
        return self.__nickname

    @property
    def identifier(self):
        return self.__identifier
