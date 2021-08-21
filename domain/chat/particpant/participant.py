from domain.chat.messages.contract import Message
from domain.chat.messages.repository import MessageRepository
from domain.core.claims import Claims


class Participant(object):
    def __init__(self, repository: MessageRepository):
        self.__identifier = ""
        self.__nickname = ""
        self.__repository = repository

    def on_direct_message_data_received(self, data: bytes) -> None:
        # Persist the message, then send it off
        pass

    def on_group_message_received(self, identifier: str, message: Message) -> None:
        pass

    def update_identity(self, claims: Claims) -> None:
        self.__identifier = claims.id()

    @property
    def nickname(self):
        return self.__nickname

    @property
    def identifier(self):
        return self.__identifier
