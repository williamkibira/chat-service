import abc
from asyncio import AbstractEventLoop, coroutine
from typing import Optional, List, Dict
from nats.aio.client import Client
from nats.aio.errors import ErrTimeout, ErrNoServers

from app.core.logging.loggers import LoggerMixin
from app.domain.core.identification_pb2 import Details


class ParticipantClient(abc.ABC):
    @abc.abstractmethod
    def fetch_details(self, identifier: str) -> Optional[Details]:
        pass

    @abc.abstractmethod
    def shutdown(self):
        pass

    @abc.abstractmethod
    def start_up(self):
        pass


class NATSConfiguration(object):
    def __init__(self, content_map: Dict):
        self.name = content_map["nats"]["name"]
        self.servers = content_map["nats"]["servers"]
        self.verbose = bool(content_map["nats"]["verbose"])
        self.allow_reconnect = bool(content_map["nats"]["reconnect"])
        self.connect_timeout = int(content_map["nats"]["connect_timeout"])
        self.reconnect_time_wait = int(content_map["nats"]["reconnect_time_wait"])
        self.max_reconnect_attempts = int(content_map["nats"]["max_reconnect_attempts"])
        self.tls = bool(content_map["nats"]["tls"])
        self.tls_hostname = content_map["nats"]["tls_hostname"]


class NATSParticipantClient(ParticipantClient, LoggerMixin):
    def __init__(self, event_loop: AbstractEventLoop, configuration: NATSConfiguration):
        self.__event_loop = event_loop
        self.__configuration = configuration
        self.__client: Client = Client()

    def start_up(self):
        self.__client.connect(
            name=self.__configuration.name,
            servers=self.__configuration.servers,
            verbose=self.__configuration.verbose,
            allow_reconnect=self.__configuration.allow_reconnect,
            connect_timeout=self.__configuration.connect_timeout,
            reconnect_time_wait=self.__configuration.reconnect_time_wait,
            max_reconnect_attempts=self.__configuration.max_reconnect_attempts,
            tls=self.__configuration.tls,
            tls_hostname=self.__configuration.tls_hostname,
            error_cb=self.__on_error_callback,
            disconnected_cb=self.__on_disconnected_callback,
            reconnected_cb=self.__on_reconnected_callback,
            closed_cb=self.__on_closed_callback,
            discovered_server_cb=self.__on_discovered_callback,
            loop=self.__event_loop
        )

    async def shutdown(self):
        await self.__client.close()

    def fetch_details(self, identifier: str) -> Optional[Details]:
        if not self.__client.is_connected:
            self._error("NATS.IO CLIENT NOT CONNECTED")
            return None
        pass

    @staticmethod
    async def __on_error_callback(error: Exception):
        pass

    @staticmethod
    async def __on_disconnected_callback():
        pass

    @staticmethod
    async def __on_closed_callback():
        pass

    @staticmethod
    async def __on_reconnected_callback():
        pass

    @staticmethod
    async def __on_discovered_callback():
        pass
