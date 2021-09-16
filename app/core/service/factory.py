from asyncio import AbstractEventLoop
from threading import Thread
from typing import Tuple

from decouple import config
from twisted.internet import protocol

from app.configuration import Configuration
from app.core.database.provider import SQLProvider
from app.core.logging.loggers import LoggerMixin
from app.domain.chat.participant.connections import ConnectionRegistry
from app.domain.chat.participant.factory import get_client
from app.domain.chat.participant.participant import ConnectedClientProtocol, ParticipantService


class ServiceFactory(protocol.ServerFactory, LoggerMixin):
    thread: Thread

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
        get_client().register_subscriber(subscriber=self.__participant_service)
        self.__database_provider = SQLProvider(
            uri=self.__configuration.database_uri(),
            debug=config('DEBUG', default=True, cast=bool))

    def buildProtocol(self, address: Tuple[str, int]):
        return ConnectedClientProtocol(registry=self.__registry, participant_service=self.__participant_service)

    def startFactory(self):
        self._logger.info("ACTIVATED SERVICE RESOURCES")
        self.__database_provider.initialize()

    def stopFactory(self):
        self.__database_provider.close()
        get_client().shutdown()
