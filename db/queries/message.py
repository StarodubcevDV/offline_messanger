from typing import List

from api.request import RequestCreateMessageDto, RequestPatchMessageDto
from db.database import DBSession
from db.exceptions import DBUserSenderNotExistsException, DBUserReceiverNotExistsException, DBMessageNotExistsException
from db.models.messages import DBMessage


def get_receiver_messages(session: DBSession, *, receiver_id: int) -> List['DBMessage']:

    db_user = session.get_user_by_id(receiver_id)

    if db_user is None:
        raise DBUserReceiverNotExistsException
    else:
        return session.get_messages_by_receiver_id(receiver_id)


def get_sender_messages(session: DBSession, *, sender_id: int) -> List['DBMessage']:

    db_user = session.get_user_by_id(sender_id)

    if db_user is None:
        raise DBUserReceiverNotExistsException
    else:
        return session.get_messages_by_sender_id(sender_id)


def get_message(session: DBSession, *, message_id: int) -> DBMessage:

    db_message = session.get_message_by_id(message_id)

    if db_message is None:
        raise DBMessageNotExistsException
    else:
        return db_message


def create_message(session: DBSession, message_dto: RequestCreateMessageDto, sender_id: int) -> DBMessage:

    if session.get_user_by_id(sender_id) is None:
        raise DBUserSenderNotExistsException

    db_receiver = session.get_user_by_login(message_dto.receiver_login)

    if db_receiver is None:
        raise DBUserReceiverNotExistsException

    new_message = DBMessage(
        sender_id=sender_id,
        receiver_id=db_receiver.id,
        message=message_dto.message
    )

    session.add_model(new_message)
    return new_message


def patch_message(session: DBSession, message_dto: RequestPatchMessageDto, message_id: int) -> DBMessage:

    db_message = get_message(session, message_id=message_id)

    for attr in message_dto.fields:
        if hasattr(message_dto, attr):
            setattr(db_message, attr, getattr(message_dto, attr))
    return db_message
