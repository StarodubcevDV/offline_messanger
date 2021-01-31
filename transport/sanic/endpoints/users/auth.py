from sanic.request import Request
from sanic.response import BaseHTTPResponse

from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicUserNotFound, SanicPasswordHashException

from api.request import RequestCreateUserDto

from db.queries import user as user_queries
from db.exceptions import DBUserNotExistsException

from helpers.password import check_hash, CheckPasswordHashException
from helpers.auth import create_token


class AuthUserEndpoint(BaseEndpoint):

    async def method_post(self, request: Request, body: dict, session, *args, **kwargs) -> BaseHTTPResponse:

        request_model = RequestCreateUserDto(body)

        try:
            db_user = user_queries.get_user(session, login=request_model.login)
        except DBUserNotExistsException:
            raise SanicUserNotFound('User not found')

        try:
            check_hash(request_model.password, db_user.password)
        except CheckPasswordHashException:
            raise SanicPasswordHashException('Wrong password')

        payload = {
            'uid': db_user.id,
        }

        response_body = {
            'Authorization': create_token(payload)
        }

        return await self.make_response_json(
            body=response_body,
            status=200,
        )
