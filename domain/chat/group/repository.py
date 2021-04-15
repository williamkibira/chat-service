import abc
from abc import ABC
from typing import List

from domain.chat.group.contracts import GroupDetails


class GroupRepository(ABC):
    @abc.abstractmethod
    def create(self, details: GroupDetails):
        pass

    @abc.abstractmethod
    def verify_membership(self, identifier: str, participant_identifier: str):
        pass

    @abc.abstractmethod
    def register(self, identifier: str, participant_identifier: str):
        pass

    @abc.abstractmethod
    def groups(self) -> List[str]:
        pass
