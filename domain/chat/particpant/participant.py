from domain.chat.messages.contract import Message
from domain.core.claims import Claims


class Participant(object):
    def __init__(self):
        self.__identifier = ""
        self.__nickname = ""

    def on_direct_message_data_received(self, data: bytes) -> None:
        # Persist the message, then send it off
        pass

    def on_group_message_received(self, identifier: str, message: Message) -> None:
        pass

    @property
    def nickname(self):
        return self.__nickname

    @property
    def identifier(self):
        return self.__identifier
