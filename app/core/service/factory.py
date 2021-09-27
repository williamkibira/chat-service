from asyncio import AbstractEventLoop
from threading import Thread
from typing import Tuple

from decouple import config
from pymessagebus import CommandBus
from pymessagebus.middleware.logger import get_logger_middleware
from twisted.internet import protocol

from app.configuration import Configuration
from app.core.database.provider import SQLProvider
from app.core.logging.loggers import LoggerMixin, Logger
from app.core.security.restriction import Restrictions
from app.domain.chat.messages.repository import MessageRepository
from app.domain.chat.messages.sql_repository import SQLMessageRepository
from app.domain.chat.participant.connections import ConnectionRegistry
from app.domain.chat.participant.factory import get_client
from app.domain.chat.participant.participant import ConnectedClientProtocol, ParticipantService
from app.domain.chat.participant.repository import ParticipantRepository
from app.domain.chat.participant.sql_repository import SQLParticipantRepository


class ServiceFactory(protocol.ServerFactory, LoggerMixin):
    thread: Thread

    def __init__(
            self,
            configuration: Configuration,
            event_loop: AbstractEventLoop
    ):
        self.logger = Logger(__file__)
        self.__event_loop = event_loop
        self.__participant_repository: ParticipantRepository = None
        self.__message_repository: MessageRepository = None
        self.__configuration: Configuration = configuration
        logging_middleware = get_logger_middleware(self.logger)
        self.__command_bus: CommandBus = CommandBus(middlewares=[logging_middleware])
        self.__registry = ConnectionRegistry(command_bus=self.__command_bus, restrictions=Restrictions())
        self.__participant_service: ParticipantService = None
        self.__database_provider = SQLProvider(
            uri=self.__configuration.database_uri(),
            debug=config('DEBUG', default=True, cast=bool))

    def buildProtocol(self, address: Tuple[str, int]):
        return ConnectedClientProtocol(registry=self.__registry, participant_service=self.__participant_service)

    def startFactory(self):
        self._logger.info("ACTIVATED SERVICE RESOURCES")
        self.__database_provider.initialize()
        self.initialize_repositories()
        self.initialize_services()

    def stopFactory(self):
        self.__database_provider.close()
        get_client().shutdown()

    def initialize_services(self) -> None:
        self.__participant_service = ParticipantService(configuration=self.__configuration,
                                                        command_bus=self.__command_bus,
                                                        participant_repository=self.__participant_repository,
                                                        message_repository=self.__message_repository)
        get_client().register_subscriber(subscriber=self.__participant_service)

    def initialize_repositories(self) -> None:
        self.__participant_repository = SQLParticipantRepository(data_source=self.__database_provider.provider())
        self.__message_repository = SQLMessageRepository(data_source=self.__database_provider.provider())
