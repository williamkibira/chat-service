from sqlalchemy import Column, String

from app.core.database.base import BaseModel


class Identity(BaseModel):
    __tablename__ = 'identity_tb'
    participant_identity = Column('participant_identity', String)
    routing_identity = Column('routing_identity', String)


class DeviceInformation(BaseModel):
    __tablename__ = 'device_information_tb'
