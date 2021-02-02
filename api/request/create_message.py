from marshmallow import Schema, fields

from api.base import RequestDto


class RequestCreateMessageDtoSchema(Schema):
    receiver_login = fields.Str(required=True, allow_none=False)
    message = fields.Str(required=True)


class RequestCreateMessageDto(RequestDto, RequestCreateMessageDtoSchema):

    __schema__ = RequestCreateMessageDtoSchema
