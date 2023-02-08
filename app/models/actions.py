import datetime
from uuid import uuid4
from sqlalchemy import Column, ForeignKey, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.database.main import Base
from app.models.enable_uuid import BinaryUUID


class Actions(Base):
    """Declaracion de la tabla Actions.

    Args:
        Base (_DeclarativeBase): Objeto de SQLalchemy

    Returns:
        str: Nos regresa string con la data
    """

    __tablename__ = "actions"

    id = Column(BinaryUUID, primary_key=True, default=uuid4, index=True)
    action_name = Column(String(200), nullable=False)
    is_active = Column(Boolean, nullable=False)
    description = Column(String(250), nullable=True)
    module_id = Column(BinaryUUID, ForeignKey("modules.id", onupdate="CASCADE"))
    actions_module = relationship("Module", back_populates="actions")
    is_deleted = Column(Boolean, nullable=True, default=False)
    created_on = Column(DateTime, default=datetime.datetime.now, nullable=False)
    created_by = Column(BinaryUUID, nullable=True)
    updated_on = Column(DateTime, onupdate=datetime.datetime.now, nullable=True)
    updated_by = Column(BinaryUUID, nullable=True)
    associeted_role = relationship(
        "Role",
        secondary="role_actions",
        lazy="dynamic",
        back_populates="actions_role",
    )

    def __repr__(self) -> str:
        """Metodo representativo.

        Returns:
            str: String de la data que hemos filtrado
        """
        return f"<Actions Info> | {self.id} | {self.action_name} \
            | {self.is_deleted} | {self.created_on} \
            | {self.updated_on} | {self.created_by}"
