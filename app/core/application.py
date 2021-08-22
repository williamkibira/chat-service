import asyncio
import sys

from decouple import config
from pymessagebus import CommandBus
from pymessagebus.middleware.logger import get_logger_middleware
from twisted.internet import asyncioreactor
from twisted.internet.asyncioreactor import AsyncioSelectorReactor
from twisted.internet.defer import ensureDeferred
from twisted.internet.task import react

from app.domain.chat.particpant.participant import ParticipantService
from app.domain.core.protocol import ConnectionRegistry
from app.core.configuration import Configuration, BuildInformation
from app.core.database.provider import SQLProvider
from app.core.logging.loggers import Logger
from app.core.security.restriction import Restrictions
from app.core.service.factory import ServiceFactory

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncioreactor.install(asyncio.get_event_loop())


class Application(object):
    def __init__(self, configuration: Configuration):
        self.__configuration = configuration
        self.logger = Logger(__file__)
        logging_middleware = get_logger_middleware(self.logger)
        self.__participant_service = ParticipantService()
        self.command_bus = CommandBus(middlewares=[logging_middleware])
        self.registry = ConnectionRegistry(command_bus=self.command_bus, restrictions=Restrictions())

    def run(self):
        build_information: BuildInformation = self.__configuration.build_information()
        return self.__initialize(name=build_information.name(), version=build_information.version())

    def __initialize(self, name: str, version: str) -> None:
        self.logger.info("Starting {0} VER: {1}".format(name, version))
        database_provider = SQLProvider(
            uri=self.__configuration.database_uri(),
            debug=config('DEBUG', default=True, cast=bool))
        database_provider.initialize()

        return react(
            lambda reactor: ensureDeferred(
                self._initializer(reactor)
            )
        )

    async def _initializer(self, reactor: AsyncioSelectorReactor):
        reactor.listenTCP(self.__configuration.port(),
                          ServiceFactory(registry=self.registry, participant_service=self.__participant_service))
        self.logger.info("Service Activated")
        reactor.run()
