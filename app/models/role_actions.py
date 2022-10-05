import datetime
from uuid import uuid4
from sqlalchemy import Column, ForeignKey, Boolean, DateTime, String
from app.database.main import Base
from app.models.enable_uuid import BinaryUUID

class Role_Actions(Base):
    
    __tablename__ = 'role_actions'

    id = Column(BinaryUUID, primary_key=True, default=uuid4)
    role_id = Column(BinaryUUID, ForeignKey('roles.id', onupdate='CASCADE'))
    actions_id = Column(BinaryUUID, ForeignKey('actions.id', onupdate='CASCADE'))
    description = Column(String(250),nullable=True)
    is_deleted = Column(Boolean, nullable=True, default=False)
    created_on = Column(DateTime, default=datetime.datetime.now, nullable=False)
    created_by = Column(BinaryUUID, nullable=True)    
    updated_on = Column(DateTime, onupdate=datetime.datetime.now, nullable=True)
    updated_by = Column(BinaryUUID, nullable=True)

    def __repr__(self):
        return f"<Roles_Actions Info> | {self.id} | {self.role_id} | {self.actions_id} | {self.is_deleted} | {self.created_on} | {self.updated_on} | {self.created_by}"

