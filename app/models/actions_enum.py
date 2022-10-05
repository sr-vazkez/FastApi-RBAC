import enum 

class ActionName(enum.Enum):
    """Lo que hacemos es definir solo 4 opciones
    para poder crear una accion las cuales son
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
    

    def __str__(self):
        return str(self.value)
