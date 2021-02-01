from marshmallow import Schema, fields

from api.base import RequestDto


class RequestCreateMessageDtoSchema(Schema):
    receiver_id = fields.Str(required=True, allow_none=False)
    text = fields.Str(required=True, allow_none=False)


class RequestCreateMessageDto(RequestDto, RequestCreateMessageDtoSchema):

    __schema__ = RequestCreateMessageDtoSchema
