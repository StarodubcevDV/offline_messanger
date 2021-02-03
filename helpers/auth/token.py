import datetime

import jwt

from helpers.auth.exceptions import ReadTokenException


secret = '4221'


def create_token(data: dict, *, lifetime: int = 1) -> str:
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(lifetime)
    }
    payload.update(data)
    return jwt.encode(payload, secret, algorithm='HS256')


def read_token(token: str) -> dict:
    try:
        return jwt.decode(token, secret, algorithms='HS256')
    except jwt.exceptions.PyJWTError as e:
        raise ReadTokenException(str(e))
