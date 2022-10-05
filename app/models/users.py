import datetime
from uuid import uuid4
from sqlalchemy import Column, ForeignKey, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.database.main import Base
from app.models.enable_uuid import BinaryUUID


class Users(Base):

    __tablename__ = 'users'

    id = Column(BinaryUUID, primary_key=True, default=uuid4)
    email = Column(String(200), nullable=False, unique=True)
    password = Column(String(200), nullable=False)
    status = Column(Boolean, nullable=False, default=True)
    
    role_id = Column(BinaryUUID, ForeignKey('roles.id', onupdate='CASCADE'), nullable=True)

    role_assigned=relationship('Role', back_populates='user_assigned')

    is_deleted = Column(Boolean, nullable=True, default=False)
    created_on = Column(DateTime, default=datetime.datetime.now, nullable=False)
    created_by = Column(BinaryUUID, nullable=True)    
    updated_on = Column(DateTime, onupdate=datetime.datetime.now, nullable=True)
    updated_by = Column(BinaryUUID, nullable=True)


    def __repr__(self):
        return f"<Users Info> | {self.id} | {self.email} | {self.password} | {self.status} | {self.is_deleted} | {self.created_on} | {self.updated_on} | {self.created_by}|"
