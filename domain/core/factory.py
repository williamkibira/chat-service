from typing import Tuple, Dict

from twisted.internet import protocol

from domain.chat.particpant.participant import Participant
from domain.core.protocol import ConnectedClientProtocol


class ServiceFactory(protocol.ServerFactory):
    def __init__(self):
        self.__participants: Dict = {}  # maps user names to Chat instances

    def register(self, participant: Participant):
        pass

    def remove(self, participant: Participant):
        pass

    def buildProtocol(self, address: Tuple[str, int]):
        return ConnectedClientProtocol()

    def __parse_token_claims(self, payload: bytes) -> Dict:
        pass
