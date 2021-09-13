import struct
import uuid
from typing import Optional, Dict

import requests
from pymessagebus import CommandBus
from twisted.internet.protocol import connectionDone
from twisted.python import failure

from app.core.configuration import Configuration
from app.core.logging.loggers import LoggerMixin
from app.domain.chat.messages.contract import Message
from app.domain.chat.messages.messages_pb2 import DirectMessage
from app.domain.chat.participant.commands import MessageDispatchCommand
from app.domain.chat.participant.connections import ClientConnection, ConnectionRegistry, DeviceDetails
from app.domain.chat.participant.contacts_pb2 import BatchContactMatchRequest, BatchContactMatchResponse, \
    ContactRequest, Contact
from app.domain.chat.participant.listeners import EventListener
from app.domain.chat.participant.node_pb2 import ParticipantPassOver
from app.domain.chat.types import MESSAGE_HEADER, RequestType, ResponseType


class Participant(object):
    def __init__(self, content_map: Dict):
        self.__identifier: str = content_map["identifier"]
        self.__nickname: str = content_map["nickname"]
        self.__email_address: str = content_map["email_address"]
        self.__photo_identifier: str = content_map["photo_identifier"]

    def on_direct_message_data_received(self, data: bytearray) -> None:
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
    def __init__(self, configuration: Configuration, command_bus: CommandBus) -> None:
        self._info("GOT LOADED")
        self.__configuration = configuration
        self.__online_participants: Dict[Participant] = {}
        self.__contact_pairing: Dict[str] = {}
        self.__command_bus: CommandBus = command_bus

    def fetch(self, identifier) -> Participant:
        if identifier != self.__online_participants:
            self.__fetch_details(identifier=identifier)
        return self.__online_participants[identifier]

    @EventListener(subject="v1/node/participants/pass-over", event_type=ParticipantPassOver)
    def on_external_participant_event(self, event: ParticipantPassOver) -> None:
        self._info("CRACKERS WAS CALLED")
        self._info("NICKNAME          : {0}".format(event.nickname))
        self._info("SENDER            : {0}".format(event.sender_identifier))
        self._info("TARGET            : {0}".format(event.target_identifier))
        self._info("ORIGINATING NODE  : {0}".format(event.originating_node))

    def resolve_contacts(self, content: bytearray) -> bytearray:
        contact_batch_request = BatchContactMatchRequest()
        contact_batch_request.ParseFromString(content)
        resolved_contact_batch = self.__resolve_contacts(contact_batch_request=contact_batch_request)
        return resolved_contact_batch.SerializeToString()

    def __resolve_contacts(self, contact_batch_request: BatchContactMatchRequest) -> BatchContactMatchResponse:
        response = BatchContactMatchResponse()
        for contact_request in contact_batch_request.requests:
            if contact_request.type is ContactRequest.ContactType.EMAIL and \
                    contact_request.value in self.__contact_pairing:
                participant: Participant = self.__online_participants[self.__contact_pairing[contact_request.value]]
                response.contacts.append(Contact(
                    profile_picture_url="{0}/{1}".format(),
                    nickname=participant.nickname,
                    identifier=participant.identifier
                ))

        return response

    def __fetch_details(self, identifier: str) -> None:
        url: str = "{0}/{1}/{2}".format(
            self.__configuration.authorization_url(),
            "/api/v1/account-service/users/details",
        )
        response: requests.Response = requests.get(url=url)
        if response.status_code is not 200:
            self._error("FAILED TO FETCH USER: {}".format(response.text))
        else:
            self.__online_participants[identifier] = Participant(content_map=response.json())
            self.__contact_pairing[response.json()["email"]] = identifier
            self._info("ADDED PARTICIPANT ENTRY FOR: {}".format(identifier))

    def relay_direct_message(self, sender_identifier: str, payload: bytearray) -> None:
        direct_message = DirectMessage()
        direct_message.ParseFromString(payload)

        if direct_message.target_identifier in self.__online_participants:
            participant = self.__online_participants[sender_identifier]
            self.__command_bus.handle(MessageDispatchCommand(
                participant_identifier=participant.identifier,
                payload=payload,
                response_type=ResponseType.RECEIVE_DIRECT_MESSAGE
            ))
        # TODO: If participant is not on the current node, send this out as an event instead


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

    def __process_message(self, message_type: RequestType, payload: bytearray) -> None:
        self._info("PROCESSING CONTROL MESSAGE: {0} {1}".format(message_type, payload))
        if message_type == RequestType.IDENTITY:
            self._info("CONTROL MESSAGE IS IDENTITY")
            self.registry.register(connection=self, payload=payload)
        elif message_type == RequestType.DISCONNECT:
            self._info("CONTROL MESSAGE IS DISCONNECT")
            self.registry.remove(self)
        elif message_type == RequestType.MATCH_CONTACTS:
            self._info("MATCHING YOUR CONTACTS")
            response: bytearray = self.__participant_service.resolve_contacts(content=payload)
            self.send_message(response_type=ResponseType.CONTACT_BATCH, payload=response)
        elif message_type == RequestType.DIRECT_MESSAGE:
            self._info("SENDING DIRECT MESSAGE")
            self.__participant_service.relay_direct_message(
                sender_identifier=self.__participant_identifier,
                payload=payload
            )

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
        return self.__participant_service.fetch(identifier=self.__participant_identifier).nickname
