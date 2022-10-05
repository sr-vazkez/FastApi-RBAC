import datetime
import sys
import uuid 
from uuid import uuid4

from decouple import config
from getpass import getpass
from passlib.context import CryptContext
from sqlalchemy import create_engine, Column, ForeignKey, String, Boolean, DateTime
from sqlalchemy.dialects.mysql import BINARY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship,sessionmaker
from sqlalchemy.types import TypeDecorator
"""
#! El script debe de ser capaz de crear un usuario con todos los permisos 
debemos de contemplar el softdelete por cualquier cosa.
Si ya estan creados los permisos simplemente asignarlos.
"""
#! Se genera string de conexion a la base de datos
# ? No se deberia de volver a realizar , por que ya fue realizado
#SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{config('DATABASE_USER')}:{config('DATABASE_PASSWORD')}@{config('DATABASE_HOSTNAME')}:{config('DATABASE_PORT')}/{config('DATABASE_NAME')}"
SQLALCHEMY_DATABASE_URL = "sqlite:///database.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_recycle=3600)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

#! Se hacen nuestros modelos que no deberia hacerlos otra vez, porque ya los hice


class BinaryUUID(TypeDecorator):
    '''Optimize UUID keys. Store as 16 bit binary, retrieve as uuid.
    inspired by:
        http://mysqlserverteam.com/storing-uuid-values-in-mysql-tables/
    '''
    
    impl = BINARY(16)
    cache_ok = True
    def process_bind_param(self, value, dialect):
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
                
    def process_result_value(self, value, dialect):
        try:
            return uuid.UUID(bytes=value)
        except:
            return None                


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


class Role(Base):

    __tablename__ = 'roles'

    id = Column(BinaryUUID, primary_key=True, default=uuid4)
    name = Column(String(200), nullable=False, unique=True)
    description = Column(String(250),nullable=True, default=None)
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

    def __repr__(self) -> str:
        return f"<Roles Info> | {self.id} | {self.name} | {self.is_deleted} | {self.created_on} | {self.updated_on} | {self.created_by}"


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

    def __repr__(self) -> str:
        return f"<Roles_Actions Info> | {self.id} | {self.role_id} | {self.actions_id} | {self.is_deleted} | {self.created_on} | {self.updated_on} | {self.created_by}"


class Module(Base):

    __tablename__ = 'modules'

    id = Column(BinaryUUID, primary_key=True, default=uuid4)
    name = Column(String(200), nullable=False, unique=True)
    description = Column(String(250),nullable=True)
    actions = relationship('Actions', back_populates='actions_module')
    is_deleted = Column(Boolean, nullable=True, default=False)
    created_on = Column(DateTime, default=datetime.datetime.now, nullable=False)
    created_by = Column(BinaryUUID, nullable=True)    
    updated_on = Column(DateTime, onupdate=datetime.datetime.now, nullable=True)
    updated_by = Column(BinaryUUID, nullable=True)
    def __repr__(self) -> str:
        return f"<Modules Info> | {self.id} | {self.name} | {self.is_deleted} | {self.created_on} | {self.updated_on} | {self.created_by}"


class Actions(Base):

    __tablename__ = 'actions'

    id = Column(BinaryUUID, primary_key=True, default=uuid4)
    action_name = Column(String(200), nullable=False)
    value = Column(Boolean, nullable=False)
    description = Column(String(250),nullable=True)
    module_id = Column(BinaryUUID, ForeignKey('modules.id', onupdate='CASCADE'))
    actions_module = relationship('Module', back_populates='actions')
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
        return f"<Actions Info> | {self.id} | {self.action_name} | {self.is_deleted} | {self.created_on} | {self.updated_on} | {self.created_by}"


#! pwd_contex es para hashear la contraseña pero no deberia de hacerlo de nuevo porque ya lo hice
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#! Clase hash que no debi copiarla porque ya la hice


class Hash():
    """ 
    Se crea una clase Hash 
    que tiene dos metodos para hashear y verificar contraseñas
    """
    @staticmethod
    def bcrypt(password):
        return pwd_context.hash(password)

    @staticmethod
    def verify(hashed_password, plain_password):
        return pwd_context.verify(plain_password, hashed_password)


def create_user(user_email: str, user_password: str) -> None:
    """
    create_user
    Esta función lo que hace es crear un usuario en la app, 
    con permisos de administrador
    """
    new_user = session.query(Users).filter(Users.email == user_email)\
        .filter_by(is_deleted=False)\
        .first()
    role = session.query(Role).first()
    if new_user:
        print("\nUse another email")
    else:
        # El que se encarga de crear usuarios
        user = Users(
                    email=user_email,
                    password=Hash.bcrypt(user_password),
                    status=True,
                    role_id=role.id.__str__(),
                    is_deleted=False,
                    created_on=datetime.datetime.now()
                    )
        session.add(user)
        session.commit()
        session.close()
        print("\nUser created successfully")


#! No deberia de repetir esta funcion xd


def _get_user_email():
    """ Se obtiene el email del usuario para poder crearlo 
    y se utiliza en la funcion create_user

    Returns:
        user_email: Un string con el email del usuario
    """
    user_email = None

    while not user_email:
        user_email = input("\nWhat is the user email?: ")
        print(f"Email: {user_email}")
        if "@" not in user_email:
            print("\nEmail must contain an @ ")
            user_email = None
            continue

        if user_email == "exit":
            print("\nOperation cancelated for the user ")
            user_email = None
            break

    if not user_email:
        sys.exit()

    return user_email

#! No deberia de repetir esta funcion xd


def _get_user_password():
    """Se obtiene la contraseña del usuario para poder crearlo
    y se utiliza en la funcion create_user


    Returns:
        input_password: Un string con la contraseña del usuario sin Hashear
    """
    input_password = None

    while not input_password:
        input_password = getpass(prompt="\nWhat is the user password?: ", stream=None)

        caracteres = len(input_password)
        if caracteres < 8:
            print("\nPassword must be at least 8 characters")
            input_password = None
            continue

        if input_password == "exit":
            print("\nOperation cancelated for the user")
            input_password = None
            break

    if not input_password:
        sys.exit()

    return input_password


def create_role() -> None:
    #! Verificar si el rol no existe
    #! Si no existe crearlo
    role_name='admin'
    role_name.encode('utf-8')

    role_exist = session.query(Role).filter(Role.name==role_name).first()
    
    if role_exist:
        print("Este rol ya fue creado")
    else:
        new_role = Role(
            name=role_name,
            description=None,
            created_on=datetime.datetime.now()
        )
        session.add(new_role)
        session.commit()
        session.close()


def create_modules(user_email: str) -> None:
    #? Debemos primero preguntar si hay modulos registrados
    find_module = session.query(Module).all()
    if find_module:
        pass
    else:
        #! No olvidar que debe de ir pegado el id del user pa crear los demas
        new_user = session.query(Users).filter_by(email=user_email).first()
        # Recursos
        #! Hacer un insert en la tabla modules
        module_list = ['users','roles','permissions','modules','actions']
        for module in module_list:
            new_module = Module(
                name = module,
                created_on=datetime.datetime.now(),
                created_by=new_user.id,
                description=None
            )
            session.add(new_module)
            session.commit()
            session.refresh(new_module)


def create_actions(user_email: str) -> None:
    #? Debemos primero preguntar si hay acciones registradas
    find_actions = session.query(Actions).all()
    if find_actions:
        pass
    else:
        #! No olvidar que debe de ir pegado el id del user pa crear los demas
        new_user = session.query(Users).filter_by(email=user_email).first()
        #print(new_user.id)
        #! Hacer Insert en la tabla actions
        modules = session.query(Module).filter_by(is_deleted=False).all()
        #print(modules)
        for module in modules:
            #print(module.id)
            actions_list = ['create','read','update','delete']
            for action in actions_list:
                #print(action)
                new_action = Actions(
                    action_name=action,
                    value=True,
                    module_id=module.id,
                    created_on=datetime.datetime.now(),
                    created_by=new_user.id,
                    description=None
                )
                session.add(new_action)
                session.commit()
                session.refresh(new_action)


def create_role_Actions(user_email: str) -> None:
    #? Debemos de preguntar si no hay acciones atadas a los roles xD
    find_role_actions = session.query(Role_Actions).all()
    if find_role_actions:
        pass
    else:
    #! Atar las acciones a los roles como chingaos no
    #! No olvidar que debe de ir pegado el id del user pa crear los demas
        new_user = session.query(Users).filter_by(email=user_email).first()
        roles = session.query(Role).filter_by(is_deleted=False).all()
        for role in roles:
            actions = session.query(Actions).filter_by(is_deleted=False).all()
            for action in actions:
                assing_action = Role_Actions(
                    role_id=role.id,
                    actions_id=action.id,
                    created_by=new_user.id,
                    description=None
                )
                session.add(assing_action)
                session.commit()


def _print_welcome() -> None:
    """
    Funcion que genera una bienvenida y muestra el menu de usuario
    """
    print("-" * 25)
    print("|  Welcome! ¯\_(ツ)_/¯ | ")
    print("-" * 25)
    print("\nDo you want to add a new super user?")
    print("\n[C]reate user\n")


if __name__ == "__main__":
    _print_welcome()
    command = input()
    command = command.upper()

    if command == "C":
        """ Se crea un usuario con permisos de administrador """
        print("Creating user...\n")
        user_email = _get_user_email()
        user_password = _get_user_password()
        create_role()
        create_user(user_email, user_password)  # type: ignore
        create_modules(user_email)  # type: ignore
        create_actions(user_email)  # type: ignore
        create_role_Actions(user_email)  # type: ignore
    else:
        print("invalid command\n")
