from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request import RequestCreateMessageDto
from api.response import ResponseMessageDto
from db.database import DBSession
from db.exceptions import DBUserSenderNotExistsException, DBUserReceiverNotExistsException, DBDataException, \
    DBIntegrityException
from db.queries import message as message_queries
from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicUserConflictException, SanicDBException


class CreateMessageEndpoint(BaseEndpoint):

    async def method_post(
            self,
            request: Request,
            body: dict,
            session: DBSession,
            sender_id: int,
            token: dict,
            *args, **kwargs
    ) -> BaseHTTPResponse:

        if token.get('uid') != sender_id:
            return await self.make_response_json(status=403)

        request_model = RequestCreateMessageDto(body)

        try:
            db_message = message_queries.create_message(session, request_model, sender_id=sender_id)
        except (DBUserSenderNotExistsException, DBUserReceiverNotExistsException) as e:
            raise SanicUserConflictException(str(e))

        try:
            session.commit_session()
        except (DBDataException, DBIntegrityException) as e:
            raise SanicDBException(str(e))

        response_model = ResponseMessageDto(db_message)

        return await self.make_response_json(body=response_model.dump(), status=201)
