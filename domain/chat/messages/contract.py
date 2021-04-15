import abc
import enum
from timestamp import timestamp


class Message(abc.ABC):
    def __init__(self):
        self.__created_by: str = None
        self.__created_at: str = None
        self.__index: str = None

    @abc.abstractmethod
    def pack(self):
        pass

    @classmethod
    def parse(cls, data: bytes):
        pass


class MediaType(enum.Enum):
    GIF = 0
    AUDIO = 1
    IMAGE = 2
    EMOTICON = 3


class Entry(object):
    def __init__(self, identifier: str, content: str, created_at: timestamp, index: int):
        self.index = index
        self.content = content
        self.identifier = identifier
        self.created_at = created_at

    @property
    def value(self):
        return {
            'identifier': self.identifier,
            'content': self.content,
            'created_at': self.created_at,
            'index': self.index
        }
