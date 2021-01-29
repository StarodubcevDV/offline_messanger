from marshmallow import Schema, fields

from api.base import RequestDto


class RequestCreateMessageDtoSchema(Schema):
    sender_id = fields.Str(required=True, allow_none=False)
    receiver_id = fields.Str(required=True, allow_none=False)
    message = fields.Str(required=True, allow_none=False)


class RequestCreateMessageDto(RequestDto):
    def __init__(self, data: dict):
        super().__init__(data)

    __schema__ = RequestCreateMessageDtoSchema
