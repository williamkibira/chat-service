import abc

from app.domain.chat.participant.connections import DeviceDetails
from app.domain.chat.participant.models import Identity


class ParticipantRepository(abc.ABC):
    @abc.abstractmethod
    def has_identity(self, participant_identifier: str) -> bool:
        pass

    @abc.abstractmethod
    def create_identity(self, routing_identifier: str, participant_identifier: str) -> None:
        pass

    @abc.abstractmethod
    def fetch_identity(self, participant_identifier: str) -> Identity:
        pass

    @abc.abstractmethod
    def add_device(self, participant_identifier: str, device: DeviceDetails) -> None:
        pass
