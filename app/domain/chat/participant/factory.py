from app.core.configuration import Configuration
from app.domain.chat.participant.clients import ParticipantClient
from app.domain.chat.participant.clients_implementation import FakeParticipantClient, NATSParticipantClient


def get_client() -> ParticipantClient:
    configuration: Configuration = Configuration.get_instance()
    if configuration.is_in_test_mode():
        return FakeParticipantClient.instance()
    return NATSParticipantClient.instance()

