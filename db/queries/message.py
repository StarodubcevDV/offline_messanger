from api.request import RequestCreateMessageDto
from db.database import DBSession
from db.exceptions import DBUserSenderNotExistsException, DBUserReceiverNotExistsException
from db.models.messages import DBMessage


def create_message(session: DBSession, message: RequestCreateMessageDto, sender_id: int) -> DBMessage:

    new_message = DBMessage(
        sender_id=sender_id,
        receiver_id=message.receiver_id,
        message=message.text
    )

    if session.get_user_by_id(sender_id) is None:
        raise DBUserSenderNotExistsException

    if session.get_user_by_id(message.receiver_id) is None:
        raise DBUserReceiverNotExistsException

    session.add_model(new_message)
    return new_message
