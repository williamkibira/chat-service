from domain.chat.messages.contract import Message, MediaType


# This is meant to be a plain text message
class TextMessage(Message):

    def pack(self):
        pass


# This is meant to be a file share message
class FileShare(Message):

    def pack(self):
        pass


# This is meant to be a media message
class Media(Message):
    def __init__(self, media_type: MediaType, identifier: str):
        super.__init__()
        self.__identifier = identifier
        self.__type = media_type

    def pack(self):
        pass


# This is meant to be a reply to an already existing message in the chain
class Referral(Message):

    def pack(self):
        pass
