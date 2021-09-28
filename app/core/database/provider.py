from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session

from app.core.database.base import BaseModel
from app.core.database.connection import DataSource


class SQLProvider(object):
    def __init__(self, uri: str, debug: bool = False) -> None:
        self.__engine: Engine = create_engine(
            uri,
            echo=debug
        )
        self.__session: Optional[Session] = None

    def initialize(self):
        session_factory = sessionmaker(bind=self.__engine)
        self.__session = scoped_session(session_factory=session_factory)
        BaseModel.set_session(session=self.__session)
        BaseModel.prepare(self.__engine, reflect=True)

    def provider(self) -> DataSource:
        return DataSource(session=self.__session)

    def close(self):
        if self.__session is not None:
            self.__session.close()
        self.__engine.dispose()
