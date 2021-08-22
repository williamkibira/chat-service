from asyncio import AbstractEventLoop
from typing import Tuple

from decouple import config
from twisted.internet import protocol

from app.core.configuration import Configuration
from app.core.database.provider import SQLProvider
from app.domain.chat.particpant.participant import ConnectedClientProtocol, ParticipantService
from app.domain.core.protocol import ConnectionRegistry
from app.core.logging.loggers import LoggerMixin


class ServiceFactory(protocol.ServerFactory, LoggerMixin):
    def __init__(
            self,
            registry: ConnectionRegistry,
            participant_service: ParticipantService,
            configuration: Configuration,
            event_loop: AbstractEventLoop
    ):
        self.__event_loop = event_loop
        self.__registry: ConnectionRegistry = registry
        self.__configuration: Configuration = configuration
        self.__participant_service = participant_service
        self._logger.info("ACTIVATED SERVICE FACTORY")
        self.__database_provider = SQLProvider(
            uri=self.__configuration.database_uri(),
            debug=config('DEBUG', default=True, cast=bool))

    def buildProtocol(self, address: Tuple[str, int]):
        return ConnectedClientProtocol(registry=self.__registry, participant_service=self.__participant_service)

    def startFactory(self):
        self.__database_provider.initialize()

    def stopFactory(self):
        pass
