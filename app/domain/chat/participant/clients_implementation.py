import asyncio
import distutils
from asyncio import get_event_loop, get_event_loop_policy
from distutils.util import strtobool
from typing import Optional, Dict, Callable, List

from google.protobuf.message import Message
from nats.aio.client import Client
from nats.aio.errors import ErrTimeout, ErrConnectionClosed, ErrNoServers

import app.domain.chat.participant.clients
from app.core.configuration import Configuration
from app.core.logging.loggers import LoggerMixin
from app.core.utilities.helpers import SingletonMixin
from app.domain.chat.participant.clients import ParticipantClient
from app.domain.chat.participant.identification_pb2 import Details, DetailsRequest

USER_DETAILS: str = "v1/account-service/users/details"


class NATSConfiguration(object):
    def __init__(self, content_map: Dict):
        self.servers: List[str] = content_map["servers"]
        self.verbose = bool(strtobool(content_map["verbose"]))
        self.allow_reconnect = bool(strtobool(content_map["allow_reconnect"]))
        self.connect_timeout = int(content_map["connect_timeout"])
        self.reconnect_time_wait = int(content_map["reconnect_time_wait"])
        self.max_reconnect_attempts = int(content_map["max_reconnect_attempts"])


class FakeParticipantClient(ParticipantClient, LoggerMixin, SingletonMixin):
    def __init__(self):
        self.__calls: Dict = {}
        self._info("LOADED FAKE PARTICIPANT CLIENT")
        app.domain.chat.participant.clients.registry = self

    def fetch_details(self, identifier: str) -> Optional[Details]:
        pass

    def shutdown(self):
        pass

    def start_up(self):
        self._info("STARTED FAKE")
        for i, k in self.__calls:
            self._info("SUBJECT : {}", i)

    async def register_subscriber(self, subject: str, handler_callback: Callable):
        self.__calls[subject] = handler_callback
        self._info("REGISTERED A CALLBACK HANDLER")

    def __register_all_subscriptions(self):
        # TODO
        # iterate through all call backs and have a lambda function inline with protocol buffer parsing
        # await nc.subscribe("help.>", cb=message_handler)
        pass


class NATSParticipantClient(ParticipantClient, LoggerMixin, SingletonMixin):

    def __init__(self):

        self.__configuration = NATSConfiguration(content_map=Configuration.get_instance().nats_configuration())
        self.__client: Client = Client()

    def start_up(self):
        try:
            self._info("CONNECTING TO NATS CLUSTER")
            self._info("CLUSTER: {0}".format(self.__configuration.servers))
            loop = asyncio.get_running_loop()
            if loop.is_running():
                loop.create_task(name="start-nats.io", coro=self.__client.connect(
                    servers=self.__configuration.servers,
                    verbose=self.__configuration.verbose,
                    allow_reconnect=self.__configuration.allow_reconnect,
                    connect_timeout=self.__configuration.connect_timeout,
                    reconnect_time_wait=self.__configuration.reconnect_time_wait,
                    max_reconnect_attempts=self.__configuration.max_reconnect_attempts,
                    error_cb=self.__on_error_callback,
                    disconnected_cb=self.__on_disconnected_callback,
                    reconnected_cb=self.__on_reconnected_callback,
                    closed_cb=self.__on_closed_callback,
                    discovered_server_cb=self.__on_discovered_callback,
                    loop=loop
                ))
                self._info("NATS.IO CLIENT CONNECTED")
        except ErrNoServers as e:
            self._error(e)

    def shutdown(self):
        try:
            self._info("SHUTTING DOWN NATS.IO CLIENT")
            loop = asyncio.get_running_loop()
            if loop.is_running() and self.__client.is_connected():
                loop.create_task(name="start-nats.io", coro=self.__client.close())
                self._info("SHUTDOWN NATS.IO CLIENT")
        except ErrNoServers as e:
            self._error(e)

    def fetch_details(self, identifier: str) -> Optional[Details]:
        if not self.__client.is_connected:
            self._error("NATS.IO CLIENT NOT CONNECTED")
            return None
        details_request: DetailsRequest = DetailsRequest()
        details_request.identifier = identifier
        try:
            response = self.__client.request(subject=USER_DETAILS,
                                             payload=details_request.SerializeToString())
            details: Details = Details()
            details.ParseFromString(response.data)
            return details
        except ErrConnectionClosed as e:
            self._error("Connection closed prematurely. {}", e)

        except ErrTimeout as e:
            self._error("Timeout occurred when publishing msg :{}".format(e))

    def register_subscriber(self, subject: str, event: Message, handler_callback: Callable):
        self.subscription_events[subject] = event
        self.subscription_methods[subject] = handler_callback
        self._info("REGISTERED CALLS")
        # self.__client.subscribe(subject=subject, cb=lambda msg:)

    async def __on_error_callback(self, error: Exception):
        self._error("{}".format(error))

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
