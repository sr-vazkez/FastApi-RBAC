import enum


class ActionName(enum.Enum):
    """Definimos solo 4 opciones.

    Para poder crear una accion las cuales son
    - create
    - read
    - delete
    - update

    Args:
        enum (enum): Clase enum de python
    """

    create = "create"
    read = "read"
    delete = "delete"
    update = "update"

    def __str__(self) -> str:
        """Metodo para retornar strings.

        Returns:
            str: Texto de algun enum seleccionado
        """
        return str(self.value)
