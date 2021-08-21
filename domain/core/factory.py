from typing import Tuple, Dict

from twisted.internet import protocol

from domain.core.protocol import ConnectedClientProtocol, ConnectionRegistry


class ServiceFactory(protocol.ServerFactory):
    def __init__(self, registry: ConnectionRegistry):
        self.__registry: ConnectionRegistry = registry

    def buildProtocol(self, address: Tuple[str, int]):
        return ConnectedClientProtocol(registry=self.__registry)
