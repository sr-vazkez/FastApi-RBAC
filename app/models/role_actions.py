import datetime
from uuid import uuid4
from sqlalchemy import Column, ForeignKey, Boolean, DateTime, String
from app.database.main import Base
from app.models.enable_uuid import BinaryUUID


class Role_Actions(Base):
    """Declaracion de la tabla Role_Actions.

    Igual conocida como permisos.

    Args:
        Base (_DeclarativeBase): Objeto de SQLalchemy

    Returns:
        str: Nos regresa string con la data
    """

    __tablename__ = "role_actions"

    id = Column(BinaryUUID, primary_key=True, default=uuid4, index=True)
    role_id = Column(BinaryUUID, ForeignKey("roles.id", onupdate="CASCADE"))
    actions_id = Column(BinaryUUID, ForeignKey("actions.id", onupdate="CASCADE"))
    description = Column(String(250), nullable=True)
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
        return f"<Roles_Actions Info> | {self.id} | {self.role_id} \
            | {self.actions_id} | {self.is_deleted} \
            | {self.created_on} | {self.updated_on} \
            | {self.created_by}"
