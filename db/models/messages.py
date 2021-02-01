from sqlalchemy import Column, VARCHAR, Integer, BOOLEAN

from db.models import BaseModel


class DBMessage(BaseModel):

    __tablename__ = 'messages'

    sender_id = Column(Integer, nullable=False)
    receiver_id = Column(Integer, nullable=False)
    message = Column(VARCHAR(150), nullable=False)
    is_delete = Column(BOOLEAN(), nullable=False, default=False)
