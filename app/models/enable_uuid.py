from typing import Optional
import uuid
from sqlalchemy.dialects.mysql import BINARY
from sqlalchemy.types import TypeDecorator


class BinaryUUID(TypeDecorator):
    """Optimize UUID keys.

    Store as 16 bit binary, retrieve as uuid.
    inspired by:
        http://mysqlserverteam.com/storing-uuid-values-in-mysql-tables/
    """

    impl = BINARY(16)
    cache_ok = True

    def process_bind_param(self, value, dialect):
        """Procesamos el parametro y generamos el uuid.

        Args:
            value (_type_): valor generado
            dialect (_type_): Opcional si elijes otro tipo de BD

        Returns:
            value: Generamos un GUUID valido
        """
        try:
            return value.bytes
        except AttributeError:
            try:
                return uuid.UUID(value).bytes
            except TypeError:
                # for some reason we ended up with the bytestring
                # ¯\_(ツ)_/¯
                # I'm not sure why you would do that,
                # but here you go anyway.
                return value

    def process_result_value(self, value, dialect) -> Optional[uuid.UUID]:
        """Procesamos el valor del resultado.

        Args:
            value (_type_): valor generado
            dialect (_type_): Opcional si elijes otro tipo de BD

        Returns:
            Optional[uuid.UUID]: Nos regresa un UUID en caso contrario
             no regresa nada
        """
        try:
            return uuid.UUID(bytes=value)
        except:  # noqa
            return None
