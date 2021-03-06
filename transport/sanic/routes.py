from typing import Tuple

from configs.config import ApplicationConfig
from context import Context
from transport.sanic import endpoints


def get_routes(config: ApplicationConfig, context: Context) -> Tuple:
    return (
        endpoints.HealthEndpoint(
            config=config, context=context, uri='/', methods=('GET', 'POST')
        ),
        endpoints.CreateUserEndpoint(
            config, context, uri='/user', methods=['POST']
        ),
        endpoints.AuthUserEndpoint(
            config, context, uri='/user/auth', methods=['POST']
        ),
        endpoints.UserEndpoint(
            config, context, uri='/user/<uid:int>', methods=['GET', 'PATCH', 'DELETE'], auth_required=True
        ),
        endpoints.CreateMessageEndpoint(
            config, context, uri='/msg/<sender_id:int>', methods=['POST'], auth_required=True
        ),
        # Чтение всех полученных сообщений
        endpoints.AllReceivedMessagesEndpoint(
            config, context, uri='/msg/received/<receiver_id:int>', methods=['GET'], auth_required=True
        ),
        # Чтение всех отправленных сообщений
        endpoints.AllSentMessagesEndpoint(
            config, context, uri='/msg/sent/<sender_id:int>', methods=['GET'], auth_required=True
        ),
        # Чтение всех сообщений пользователя (отправленных и полученных)
        endpoints.AllMessagesEndpoint(
            config, context, uri='/msg/all/<user_id:int>', methods=['GET'], auth_required=True
        ),
        endpoints.MessageEndpoint(
            config, context, uri='/msg/<message_id:int>', methods=['GET', 'PATCH', 'DELETE'], auth_required=True
        ),
    )
