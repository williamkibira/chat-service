from sqlalchemy.orm import Session
from twisted.internet import threads


def to_thread(f):
    def wrapper(*args, **kwargs):
        return threads.deferToThread(f, *args, **kwargs)
    return wrapper


class Transaction(object):
    def __init__(self, dsn, session: Session):
        self.__session = session

    def __call__(self, func):
        @to_thread
        def wrapper(*args, **kwargs):
            try:
                return func(session=self.__session, *args, **kwargs)
            except Exception:
                self.__session.rollback()
                raise
            finally:
                self.__session.close()
        return wrapper
