from twisted.application import service, internet
from twisted.application.internet import TCPServer
from twisted.internet import reactor

from domain.core.factory import ServiceFactory
from domain.core.protocol import ConnectionRegistry


class Application(object):
    def __init__(self, port: int):
        self.port = port
        self.registry = ConnectionRegistry()
        # reactor.listenTCP(port, ServiceFactory())
        # self.__server: TCPServer = internet.TCPServer(reactor=reactor)
        # self.__server.setServiceParent(service.Application("chat-server"))

    def run(self):
        reactor.listenTCP(self.port, ServiceFactory(registry=self.registry))
        reactor.run()
        # self.__server.startService()

