from sqlalchemy.exc import NoResultFound

from app.core.database.connection import DataSource
from app.core.logging.loggers import LoggerMixin
from app.domain.chat.participant.connections import DeviceDetails
from app.domain.chat.participant.models import Identity
from app.domain.chat.participant.repository import ParticipantRepository


class SQLParticipantRepository(ParticipantRepository, LoggerMixin):

    def __init__(self, data_source: DataSource):
        self.__data_source = data_source

    def has_identity(self, participant_identifier: str) -> bool:
        session = self.__data_source.unbound()
        query: str = "SELECT 1 AS has_identity FROM identity_tb WHERE participant_identifier=:participant_identifier"
        result = session.execute(statement=query, params={'participant_identifier': participant_identifier})
        return result[0]['has_identity']

    def create_identity(self, routing_identifier: str, participant_identifier: str) -> None:
        sql: str = "INSERT INTO identity_tb(participant_identifier, routing_identifier) " \
                   "VALUES(:participant_identifier,:routing_identifier)"
        with self.__data_source.session as session:
            session.execute(statement=sql, params={'participant_identifier': participant_identifier,
                                                   'routing_identifier': routing_identifier})

    def fetch_identity(self, participant_identifier: str) -> Identity:
        try:
            session = self.__data_source.unbound()
            return session.query(Identity).filter(Identity.participant_identity == participant_identifier).one()
        except NoResultFound as error:
            self._info("ERROR: {}".format(error))
            return None

    def add_device(self, participant_identifier: str, device: DeviceDetails) -> None:
        sql: str = "INSERT INTO device_information_tb(identity_id, information) " \
                   "VALUES((SELECT id FROM identity_tb WHERE participant_identifier=:participant_identifier), " \
                   ":information)"
        with self.__data_source.session as session:
            session.execute(statement=sql, params={'participant_identifier': participant_identifier,
                                                   'information': device.json})

