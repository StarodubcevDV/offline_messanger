from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request.patch_message import RequestPatchMessageDto
from api.response import ResponseMessageDto
from db.database import DBSession
from db.exceptions import DBMessageNotExistsException, DBDataException, \
    DBIntegrityException
from db.queries import message as message_queries
from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicMessageNotFound, SanicDBException


class MessageEndpoint(BaseEndpoint):

    async def method_get(
            self,
            request: Request,
            body: dict,
            session: DBSession,
            message_id: int,
            token: dict,
            *args, **kwargs) -> BaseHTTPResponse:

        # Получение id пользователя, который отправил сообщение
        try:
            db_message = message_queries.get_message(session, message_id=message_id)
        except DBMessageNotExistsException as e:
            raise SanicMessageNotFound('Message not found')

        if (token.get('uid') != db_message.sender_id)\
                or (token.get('uid') != db_message.receiver_id):
            return await self.make_response_json(status=403)

        response_model = ResponseMessageDto(db_message)

        return await self.make_response_json(status=200, body=response_model.dump())

    async def method_patch(
            self,
            request: Request,
            body: dict,
            session: DBSession,
            message_id: int,
            token: dict,
            *args, **kwargs) -> BaseHTTPResponse:

        # Получение id пользователя, который отправил сообщение
        # Только отправитель может изменять или удалять сообщение
        try:
            check_message = message_queries.get_message(session, message_id=message_id)
        except DBMessageNotExistsException as e:
            raise SanicMessageNotFound('Message not found')

        if token.get('uid') != check_message.sender_id:
            return await self.make_response_json(status=403)

        request_model = RequestPatchMessageDto(body)

        try:
            db_message = message_queries.patch_message(session, request_model, message_id)
        except DBMessageNotExistsException as e:
            raise SanicMessageNotFound('Message not found')

        try:
            session.commit_session()
        except (DBDataException, DBIntegrityException) as e:
            raise SanicDBException(str(e))

        response_model = ResponseMessageDto(db_message)
        return await self.make_response_json(status=200, body=response_model.dump())

    async def method_delete(
            self,
            request: Request,
            body: dict,
            session: DBSession,
            message_id: int,
            token: dict,
            *args, **kwargs
    ) -> BaseHTTPResponse:

        # Получение id пользователя, который отправил сообщение
        # Только отправитель может изменять или удалять сообщение
        try:
            db_message = message_queries.get_message(session, message_id=message_id)
        except DBMessageNotExistsException as e:
            raise SanicMessageNotFound('Message not found')

        if token.get('uid') != db_message.sender_id:
            return await self.make_response_json(status=403)

        db_message.is_delete = True

        try:
            session.commit_session()
        except (DBDataException, DBIntegrityException) as e:
            raise SanicDBException(str(e))

        return await self.make_response_json(status=204)
