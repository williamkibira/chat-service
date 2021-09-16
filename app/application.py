import asyncio
import sys

from pymessagebus import CommandBus
from pymessagebus.middleware.logger import get_logger_middleware
from twisted.internet import asyncioreactor
from twisted.internet.asyncioreactor import AsyncioSelectorReactor

from app.configuration import Configuration, BuildInformation
from app.core.logging.loggers import Logger
from app.core.security.restriction import Restrictions
from app.core.service.factory import ServiceFactory
from app.domain.chat.participant.connections import ConnectionRegistry
from app.domain.chat.participant.factory import get_client
from app.domain.chat.participant.participant import ParticipantService

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncioreactor.install(asyncio.get_event_loop())


class Application(object):
    def __init__(self, configuration: Configuration):
        self.__configuration = configuration
        self.logger = Logger(__file__)
        logging_middleware = get_logger_middleware(self.logger)
        self.__event_loop = asyncio.get_event_loop()
        self.__participant_service = ParticipantService(self.__configuration)
        self.command_bus = CommandBus(middlewares=[logging_middleware])
        self.registry = ConnectionRegistry(command_bus=self.command_bus, restrictions=Restrictions())
        self.reactor = AsyncioSelectorReactor(eventloop=self.__event_loop)

    def run(self):
        build_information: BuildInformation = self.__configuration.build_information()
        return self.__initialize(name=build_information.name(), version=build_information.version())

    def __initialize(self, name: str, version: str) -> None:
        self.logger.info("Starting {0} VER: {1}".format(name, version))
        self.reactor.listenTCP(self.__configuration.port(),
                               ServiceFactory(
                                   registry=self.registry,
                                   participant_service=self.__participant_service,
                                   configuration=self.__configuration,
                                   event_loop=self.__event_loop
                               ))
        asyncio.set_event_loop(self.__event_loop)
        self.reactor.callLater(seconds=5, f=get_client().start_up)
        self.reactor.run()

    async def _initializer(self, reactor: AsyncioSelectorReactor):
        reactor.listenTCP(self.__configuration.port(),
                          ServiceFactory(
                              registry=self.registry,
                              participant_service=self.__participant_service,
                              configuration=self.__configuration,
                              event_loop=asyncio.get_event_loop()
                          ))
        asyncio.get_event_loop().create_task(coro=get_client().start_up(), name="start-nats")
        reactor.run()
