from twisted.application import service, internet
from domain.core.factory import ServiceFactory


class Application(object):
    def __init__(self, port: int):
        self.__port = port
        self.__app = service.Application("chat-server")

    def run(self):
        internet.TCPServer(self.__port, ServiceFactory()).setServiceParent(self.__app)
