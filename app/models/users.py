import datetime
from uuid import uuid4
from sqlalchemy import Column, ForeignKey, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.database.main import Base
from app.models.enable_uuid import BinaryUUID


class Users(Base):
    """Declaracion de la tabla Users.

    Args:
        Base (_DeclarativeBase): Objeto de SQLalchemy

    Returns:
        str: Nos regresa string con la data
    """

    __tablename__ = "users"

    id = Column(BinaryUUID, primary_key=True, default=uuid4, index=True)
    email = Column(String(200), nullable=False, unique=True)
    password = Column(String(200), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

    role_id = Column(
        BinaryUUID, ForeignKey("roles.id", onupdate="CASCADE"), nullable=True
    )

    role_assigned = relationship("Role", back_populates="user_assigned")

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
        return f"<Users Info> | {self.id} | {self.email} \
            | {self.password} | {self.status} \
            | {self.is_deleted} | {self.created_on} \
            | {self.updated_on} | {self.created_by}|"
