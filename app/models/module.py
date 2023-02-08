import datetime
from uuid import uuid4
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.database.main import Base
from app.models.enable_uuid import BinaryUUID


class Module(Base):
    """Declaracion de la tabla Module.

    Args:
        Base (_DeclarativeBase): Objeto de SQLalchemy

    Returns:
        str: Nos regresa string con la data
    """

    __tablename__ = "modules"

    id = Column(BinaryUUID, primary_key=True, default=uuid4, index=True)
    name = Column(String(200), nullable=False, unique=True)
    description = Column(String(250), nullable=True)
    actions = relationship("Actions", back_populates="actions_module")
    is_deleted = Column(Boolean, nullable=True, default=False)
    created_on = Column(DateTime, default=datetime.datetime.now, nullable=False)
    created_by = Column(BinaryUUID, nullable=True)
    updated_on = Column(DateTime, onupdate=datetime.datetime.now, nullable=True)
    updated_by = Column(BinaryUUID, nullable=True)

    def __repr__(self) -> str:
        """Metodo representativo.

        Returns:
            str: String de la data que hemos filtrado
        """
        return f"<Modules Info> | {self.id} | {self.name} | \
            {self.is_deleted} | {self.created_on} | \
            {self.updated_on} | {self.created_by}"
