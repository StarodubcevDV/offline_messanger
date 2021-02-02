from typing import List

from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy.orm import sessionmaker, Session

from db.exceptions import DBIntegrityException, DBDataException
from db.models import BaseModel, DBUser, DBMessage


class DBSession:
    _session: Session

    def __init__(self, session: Session):
        self._session = session

    def query(self, *args, **kwargs):
        return self._session.query(*args, **kwargs)

    def close_session(self):
        self._session.close()

    def add_model(self, model: BaseModel):
        try:
            self._session.add(model)
        except IntegrityError as e:
            raise DBIntegrityException(e)
        except DataError as e:
            raise DBDataException(e)

    def get_user_by_login(self, login: str) -> DBUser:
        return self._session.query(DBUser).filter(DBUser.login == login, DBUser.is_delete != 1).first()

    def get_user_by_id(self, eid: int) -> DBUser:
        return self._session.query(DBUser).filter(DBUser.id == eid, DBUser.is_delete != 1).first()

    def get_message_by_id(self, mid: int) -> DBMessage:
        return self._session.query(DBMessage).filter(DBMessage.id == mid, DBMessage.is_delete != 1).first()

    def get_messages_by_receiver_id(self, receiver_id: int) -> List['DBMessage']:
        return self._session.query(DBMessage).filter(DBMessage.receiver_id == receiver_id, DBMessage.is_delete != 1).all()

    def get_messages_by_sender_id(self, sender_id: int) -> List['DBMessage']:
        return self._session.query(DBMessage).filter(DBMessage.sender_id == sender_id, DBMessage.is_delete != 1).all()

    def commit_session(self, need_close: bool = False):
        try:
            self._session.commit()
        except IntegrityError as e:
            raise DBIntegrityException(e)
        except DataError as e:
            raise DBDataException(e)

        if need_close:
            self.close_session()


class DataBase:
    connection: Engine
    session_factory: sessionmaker
    _test_query = 'SELECT 1'

    def __init__(self, connection: Engine):
        self.connection = connection
        self.session_factory = sessionmaker(bind=self.connection)

    def check_connection(self):
        self.connection.execute(self._test_query).fetchone()

    def make_session(self) -> DBSession:
        session = self.session_factory()
        return DBSession(session)
