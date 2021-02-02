import datetime

import jwt

from helpers.auth.exceptions import ReadTokenException


secret = '4221'


def create_token(payload: dict) -> str:
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(days=1)
    return jwt.encode(payload, secret, algorithm='HS256')


def read_token(token: str) -> dict:
    try:
        return jwt.decode(token, secret, algorithms='HS256')
    except jwt.exceptions.PyJWTError as e:
        raise ReadTokenException(str(e))
