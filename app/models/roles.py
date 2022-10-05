import datetime
from uuid import uuid4
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.database.main import Base
from app.models.enable_uuid import BinaryUUID

class Role(Base):

    __tablename__ = 'roles'

    id = Column(BinaryUUID, primary_key=True, default=uuid4)
    name = Column(String(200), nullable=False, unique=True)
    description = Column(String(250),nullable=True)
    user_assigned = relationship('Users', back_populates="role_assigned")
    is_deleted = Column(Boolean, nullable=True, default=False)
    created_on = Column(DateTime, default=datetime.datetime.now, nullable=False)
    created_by = Column(BinaryUUID, nullable=True)    
    updated_on = Column(DateTime, onupdate=datetime.datetime.now, nullable=True)
    updated_by = Column(BinaryUUID, nullable=True)
    
    actions_role = relationship(
        "Actions",
        secondary="role_actions",
        lazy="dynamic",
        back_populates="associeted_role"
    )

    def __repr__(self):
        return f"<Roles Info> | {self.id} | {self.name} | {self.is_deleted} | {self.created_on} | {self.updated_on} | {self.created_by}"
