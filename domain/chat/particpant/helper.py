import abc
from typing import Optional

from domain.chat.particpant.participant import Participant
from domain.core.identification_pb2 import Details


class ParticipantClient(abc.ABC):
    @abc.abstractmethod
    def fetch_details(self, identifier: str) -> Optional[Details]:
        pass

    @abc.abstractmethod
    def shutdown(self):
        pass


class NATSParticipantClient(ParticipantClient):

    def shutdown(self):
        pass

    def fetch_details(self, identifier: str) -> Optional[Details]:
        pass




class ParticipantService(object):

    def fetch(self, identifier) -> Participant:
        pass
