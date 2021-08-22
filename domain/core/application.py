import asyncio
import sys

from pymessagebus import CommandBus
from pymessagebus.middleware.logger import get_logger_middleware
from twisted.internet import asyncioreactor

from twisted.internet.asyncioreactor import AsyncioSelectorReactor
from twisted.internet.defer import ensureDeferred
from twisted.internet.task import react

from domain.chat.particpant.helper import ParticipantService
from domain.core.factory import ServiceFactory
from domain.core.logging import Logger
from domain.core.protocol import ConnectionRegistry

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncioreactor.install(asyncio.get_event_loop())


class Application(object):
    def __init__(self, port: int):
        self.logger = Logger("command-bus")
        self.port = port
        logging_middleware = get_logger_middleware(self.logger)
        self.__participant_service = ParticipantService()
        self.command_bus = CommandBus(middlewares=[logging_middleware])
        self.registry = ConnectionRegistry(command_bus=self.command_bus)
        # reactor.listenTCP(port, ServiceFactory())
        # self.__server: TCPServer = internet.TCPServer(reactor=reactor)
        # self.__server.setServiceParent(service.Application("chat-server"))

    def run(self):
        # reactor.listenTCP(self.port, ServiceFactory(registry=self.registry))
        # reactor.run()
        # self.__server.startService()
        return react(
            lambda reactor: ensureDeferred(
                self._initializer(reactor)
            )
        )

    async def _initializer(self, reactor: AsyncioSelectorReactor):
        reactor.listenTCP(self.port,
                          ServiceFactory(registry=self.registry, participant_service=self.__participant_service))
        print("Service Activated")
        reactor.run()
