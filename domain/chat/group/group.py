from typing import Dict, List
import simplejson as json

from domain.chat.messages.repository import MessageRepository
from domain.chat.particpant.participant import Participant
from domain.chat.types import MessageType


class Group(object):
    def __init__(self, name: str, repository: MessageRepository):
        self.__repository = repository
        self.__name = name
        self.__participants: Dict = {}

    def broadcast(self, message_type: MessageType, payload: bytes):
        for identifier, participant in self.__participants:
            participant.on_group_message_received(identifier=identifier, payload=payload)

    def process_message(self, message_type: MessageType, payload: bytes):
        pass

    def join(self, participant: Participant):
        self.__participants[participant.identifier] = participant

    def leave(self, identifier):
        self.__participants.pop(identifier)

    def fetch_participants(self):
        identifier_name_pairs: List = []
        for identifier, participant in self.__participants.items():
            identifier_name_pairs.append({'identifier': identifier, 'nickname': participant.nickname})
        return json.dump(identifier_name_pairs)
