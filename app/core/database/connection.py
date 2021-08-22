from sqlalchemy.orm import Session


class SmartSession:
    def __init__(self, session: Session):
        self.__session = session

    def __enter__(self) -> Session:
        return self.__session

    def __exit__(self, type, value, traceback):
        try:
            self.__session.commit()
        except Exception as e:
            self.__session.rollback()
            raise e


class DataSource:
    def __init__(self, session: Session):
        self.__session = session

    @property
    def session(self) -> SmartSession:
        return SmartSession(session=self.__session)

    def unbound(self) -> Session:
        return self.__session
