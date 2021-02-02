from typing import List

from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.response import ResponseMessageDto
from db.database import DBSession
from db.exceptions import DBUserReceiverNotExistsException, DBUserSenderNotExistsException
from db.queries import message as message_queries
from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicUserNotFound


class AllReceivedMessagesEndpoint(BaseEndpoint):

    async def method_get(
            self,
            request: Request,
            body: dict,
            session: DBSession,
            receiver_id: int,
            token: dict,
            *args, **kwargs
    ) -> BaseHTTPResponse:

        if token.get('uid') != receiver_id:
            return await self.make_response_json(status=403)

        try:
            db_messages = message_queries.get_receiver_messages(session, receiver_id=receiver_id)
        except DBUserReceiverNotExistsException as e:
            raise SanicUserNotFound(str(e))

        response_model = ResponseMessageDto(db_messages, many=True)

        return await self.make_response_json(status=200, body=response_model.dump())


class AllSentMessagesEndpoint(BaseEndpoint):

    async def method_get(
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

        try:
            db_messages = message_queries.get_sender_messages(session, sender_id=sender_id)
        except DBUserSenderNotExistsException as e:
            raise SanicUserNotFound(str(e))

        response_model = ResponseMessageDto(db_messages, many=True)

        return await self.make_response_json(status=200, body=response_model.dump())


class AllMessagesEndpoint(BaseEndpoint):
    async def method_get(
            self,
            request: Request,
            body: dict,
            session: DBSession,
            user_id: int,
            token: dict,
            *args, **kwargs
    ) -> BaseHTTPResponse:

        if token.get('uid') != user_id:
            return await self.make_response_json(status=403)

        try:
            db_sent_messages = message_queries.get_sender_messages(session, sender_id=user_id)
            db_received_messages = message_queries.get_receiver_messages(session, receiver_id=user_id)
        except DBUserSenderNotExistsException as e:
            raise SanicUserNotFound(str(e))

        db_messages = db_sent_messages + db_received_messages

        response_model = ResponseMessageDto(db_messages, many=True)

        return await self.make_response_json(status=200, body=response_model.dump())
