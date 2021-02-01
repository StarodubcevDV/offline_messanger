from typing import List

from api.request import RequestCreateMessageDto
from db.database import DBSession
from db.exceptions import DBUserSenderNotExistsException, DBUserReceiverNotExistsException
from db.models.messages import DBMessage


def get_messages(session: DBSession, *, receiver_id: int) -> List['DBMessage']:

    db_user = session.get_user_by_id(receiver_id)

    if db_user is None:
        raise DBUserReceiverNotExistsException
    else:
        return session.get_messages_by_receiver_id(receiver_id)


def create_message(session: DBSession, message_dto: RequestCreateMessageDto, sender_id: int) -> DBMessage:

    new_message = DBMessage(
        sender_id=sender_id,
        receiver_id=message_dto.receiver_id,
        message=message_dto.message
    )

    if session.get_user_by_id(sender_id) is None:
        raise DBUserSenderNotExistsException

    if session.get_user_by_id(message_dto.receiver_id) is None:
        raise DBUserReceiverNotExistsException

    session.add_model(new_message)
    return new_message
