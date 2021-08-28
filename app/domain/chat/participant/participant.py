import struct
import uuid
from typing import Optional

from twisted.internet.protocol import connectionDone
from twisted.python import failure

from app.core.logging.loggers import LoggerMixin
from app.domain.chat.messages.contract import Message
from app.domain.chat.participant.connections import ClientConnection, ConnectionRegistry, DeviceDetails
from app.domain.chat.participant.listeners import ParticipantPassOverListener, EventListener
from app.domain.chat.participant.node_pb2 import ParticipantPassOver
from app.domain.chat.types import MESSAGE_HEADER, RequestType, ResponseType


class Participant(object):
    def __init__(self):
        self.__identifier = ""
        self.__nickname = ""

    def on_direct_message_data_received(self, data: bytes) -> None:
        # Persist the message, then send it off
        pass

    def on_group_message_received(self, identifier: str, message: Message) -> None:
        pass

    @property
    def nickname(self):
        return self.__nickname

    @property
    def identifier(self):
        return self.__identifier


class ParticipantService(LoggerMixin):
    def __init__(self):
        self._info("GOT LOADED")

    def fetch(self, identifier) -> Participant:
        pass

    @EventListener(subject="v1/node/participants/pass-over", event_type=ParticipantPassOver)
    def on_external_participant_event(self, event: ParticipantPassOver) -> None:
        self._info("CRACKERS WAS CALLED")
        self._info("NICKNAME          : {0}".format(event.nickname))
        self._info("SENDER            : {0}".format(event.sender_identifier))
        self._info("TARGET            : {0}".format(event.target_identifier))
        self._info("ORIGINATING NODE  : {0}".format(event.originating_node))


class ConnectedClientProtocol(ClientConnection, LoggerMixin):

    def __init__(self, registry: ConnectionRegistry, participant_service: ParticipantService):
        self.registry: ConnectionRegistry = registry
        self.__participant_service = participant_service
        self.__unique_identifier: str = str(uuid.uuid4())
        self.__participant_identifier: Optional[str] = None
        self.__device_information: Optional[DeviceDetails] = None

    def dataReceived(self, data: bytearray):
        self._info("GOT A CONTROL MESSAGE")
        header = data[0:MESSAGE_HEADER]
        (message_type_value, message_size) = struct.unpack("!HL", header)
        self._info("CTRL -> {0} SIZE -> {1}".format(message_type_value, message_size))
        payload: bytes = data[MESSAGE_HEADER: message_size + MESSAGE_HEADER]
        self.__process_message(message_type=RequestType(message_type_value), payload=payload)

    def connectionMade(self):
        # Send a request for identification information
        self._info("CONNECTION RECEIVED")
        self.registry.add_to_pending_identification(self)
        self.send_message(response_type=ResponseType.REQUEST_IDENTITY, payload="".encode())

    def connectionLost(self, reason: failure.Failure = connectionDone):
        self._info("CONNECTION HAS BEEN LOST")
        self.registry.remove(self)

    def __process_message(self, message_type: RequestType, payload: bytes) -> None:
        self._info("PROCESSING CONTROL MESSAGE: {0} {1}".format(message_type, payload))
        if message_type == RequestType.IDENTITY:
            self._info("CONTROL MESSAGE IS IDENTITY")
            self.registry.register(connection=self, payload=payload)
        elif message_type == RequestType.DISCONNECT:
            self._info("CONTROL MESSAGE IS DISCONNECT")
            self.registry.remove(self)

    def send_message(self, response_type: ResponseType, payload: bytearray) -> None:
        self._info("SENDING CONTROL MESSAGE: {} {}".format(response_type, payload))
        packet = struct.pack("!HL", response_type.value, len(payload)) + payload
        self.transport.write(data=packet)

    def resolve_participant(self, identifier: str, device_information: DeviceDetails) -> bool:
        self.__participant_identifier = identifier
        self.__device_information = device_information

    def participant_identifier(self) -> Optional[str]:
        return self.__participant_identifier

    def device(self) -> Optional[DeviceDetails]:
        return self.__device_information

    def unique_identifier(self):
        return self.__unique_identifier

    def nickname(self):
        return ""
