from datetime import datetime
from typing import List

from app.core.database.connection import DataSource
from app.domain.chat.messages.repository import MessageRepository


class SQLMessageRepository(MessageRepository):
    def __init__(self, data_source: DataSource):
        self.__data_source = data_source

    def add_message(self, sender: str, target: str, payload: bytearray, received_at: datetime, node: str) -> None:
        sql: str = "INSERT INTO direct_message_tb(sender_id,target_id,message,received_at, node) " \
                   "VALUES(" \
                   "SELECT id FROM identity_tb WHERE routing_identity=:sender_identifier," \
                   "SELECT id FROM identity_tb WHERE routing_identity=:target_identifier," \
                   ":payload," \
                   ":received_at," \
                   ":node)"
        with self.__data_source.session as session:
            session.execute(statement=sql,
                            params={'sender_identifier': sender,
                                    'target_identifier': target,
                                    'payload': payload,
                                    'received_at': received_at,
                                    'node': node})

    def fetch_message_group_messages(self, group_identifier: str, limit: int, offset: int) -> List:
        pass

    def fetch_participant_messages(self, participant_identifier: str, limit: int, offset: int) -> List:
        pass

    def remove_participant_message(self, participant_identifier: str, message_identifier: str) -> None:
        pass
