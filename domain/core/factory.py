from typing import Tuple

from twisted.internet import protocol

from domain.chat.particpant.helper import ParticipantService
from domain.core.logging import Logger
from domain.core.protocol import ConnectedClientProtocol, ConnectionRegistry


class ServiceFactory(protocol.ServerFactory):
    def __init__(self, registry: ConnectionRegistry, participant_service: ParticipantService):
        self.__log = Logger(__file__)
        self.__registry: ConnectionRegistry = registry
        self.__participant_service = participant_service
        self.__log.info("ACTIVATED SERVICE FACTORY")

    def buildProtocol(self, address: Tuple[str, int]):
        return ConnectedClientProtocol(registry=self.__registry, participant_service=self.__participant_service)
