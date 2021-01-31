from typing import Tuple

from configs.config import ApplicationConfig
from context import Context
from transport.sanic import endpoints


def get_routes(config: ApplicationConfig, context: Context) -> Tuple:
    return (
        endpoints.HealthEndpoint(config=config, context=context, uri='/', methods=('GET', 'POST')),
        endpoints.CreateUserEndpoint(config, context, uri='/user', methods=['POST']),
        endpoints.AuthUserEndpoint(config, context, uri='/user/auth', methods=['POST']),
        endpoints.UserEndpoint(config, context, uri='/user/<uid:int>', methods=['GET', 'PATCH'], auth_required=True),
    )
