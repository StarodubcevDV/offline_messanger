from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request import RequestPatchUserDto
from api.response import ResponseUserDto
from db.database import DBSession
from db.exceptions import DBUserNotExistsException, DBDataException, DBIntegrityException
from db.queries import user as user_queries
from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicUserNotFound, SanicDBException


class UserEndpoint(BaseEndpoint):

    async def method_get(
            self,
            request: Request,
            body: dict,
            session: DBSession,
            uid: int,
            token: dict,
            *args, **kwargs) -> BaseHTTPResponse:

        if token.get('uid') != uid:
            return await self.make_response_json(status=403)

        try:
            db_user = user_queries.get_user(session, user_id=uid)
        except DBUserNotExistsException as e:
            raise SanicUserNotFound('User not found')

        response_model = ResponseUserDto(db_user)

        return await self.make_response_json(status=200, body=response_model.dump())

    async def method_patch(
            self,
            request: Request,
            body: dict,
            session: DBSession,
            uid: int,
            token: dict,
            *args, **kwargs
    ) -> BaseHTTPResponse:

        if token.get('uid') != uid:
            return await self.make_response_json(status=403)

        request_model = RequestPatchUserDto(body)

        try:
            db_user = user_queries.patch_user(session, request_model, uid)
        except DBUserNotExistsException as e:
            raise SanicUserNotFound('User not found')

        try:
            session.commit_session()
        except (DBDataException, DBIntegrityException) as e:
            raise SanicDBException(str(e))

        response_model = ResponseUserDto(db_user)
        return await self.make_response_json(status=200, body=response_model.dump())

    async def method_delete(
            self,
            request: Request,
            body: dict,
            session: DBSession,
            uid: int,
            token: dict,
            *args, **kwargs
    ) -> BaseHTTPResponse:

        if token.get('uid') != uid:
            return await self.make_response_json(status=403)

        try:
            db_user = user_queries.delete_user(session, user_id=uid)
        except DBUserNotExistsException as e:
            raise SanicUserNotFound('User not found')

        try:
            session.commit_session()
        except (DBDataException, DBIntegrityException) as e:
            raise SanicDBException(str(e))

        return await self.make_response_json(status=204)
