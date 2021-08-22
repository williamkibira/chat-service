from typing import Tuple

from twisted.internet import protocol

from app.domain.chat.particpant.participant import ConnectedClientProtocol, ParticipantService
from app.domain.core.protocol import ConnectionRegistry
from app.core.logging.loggers import LoggerMixin


class ServiceFactory(protocol.ServerFactory, LoggerMixin):
    def __init__(self, registry: ConnectionRegistry, participant_service: ParticipantService):
        self.__registry: ConnectionRegistry = registry
        self.__participant_service = participant_service
        self._logger.info("ACTIVATED SERVICE FACTORY")

    def buildProtocol(self, address: Tuple[str, int]):
        return ConnectedClientProtocol(registry=self.__registry, participant_service=self.__participant_service)
