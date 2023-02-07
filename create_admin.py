#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
from getpass import getpass

from app import main  # noqa
from app.database.main import SessionLocal

from app.internal.roles import RoleActions
from app.internal.users import UsersActions
from app.internal.module import ModuleActions
from app.internal.actions import ActionsOperations
from app.internal.role_action import RoleActions as PermissionActions

from app.models.roles import Role
from app.models.users import Users
from app.models.module import Module
from app.models.actions import Actions

from app.schemas.role_schemas import RoleCreate
from app.schemas.user_schemas import UserCreate
from app.schemas.module_schemas import ModuleCreate
from app.schemas.action_schemas import ActionCreate
from app.schemas.role_actions_schemas import assigned_action

db = SessionLocal()

role_action = RoleActions()
user_action = UsersActions()
module_action = ModuleActions()
action_operation = ActionsOperations()
permission_action = PermissionActions()


def _get_user_email() -> str:
    """Se obtiene el email del usuario para poder crearlo.

    Se utiliza la funcion get_email

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


def _get_user_password() -> str:
    """Se obtiene la contraseña del usuario para poder crearlo.

    se utiliza en la funcion create_user

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


def create_all(user_email: str, user_password: str) -> None:
    """Create all items.

    Args:
        user_email (str): a valid email
        user_password (str): a strong password
    """
    request = RoleCreate(name="admin", description="all access in the system")
    role_action.create_new_role(
        db=db, request=request, current_user=None  # type: ignore
    )
    role = db.query(Role.id).filter_by(name=request.name).first()

    role_id = ""
    for role_id in role:  # type: ignore
        type(role_id)

    request_user = UserCreate(
        email=user_email,  # type: ignore
        password=user_password,
        role_id=role_id,  # type: ignore
    )

    user_action.create_new_user(
        db=db, current_user=None, request=request_user  # type: ignore
    )
    user = db.query(Users.id).filter_by(email=request_user.email).first()

    user_id = ""
    for user_id in user:  # type: ignore
        type(user_id)

    # Como crear 4 permisos sin repetirme xD?
    modulos = ["users", "roles", "actions", "modules", "permissions"]
    for modulo in modulos:
        request_module = ModuleCreate(
            name=modulo, description=f"module for {modulo} permissions"
        )
        module_action.create_module(db=db, request=request_module, current_user=user_id)

    # como crear todas las acciones de todos los modulos sin repetirme?
    module_list = db.query(Module).all()
    for module_item in module_list:
        action_list = ["create", "read", "update", "delete"]
        for action in action_list:
            # print(action,module_item.name)
            request_action = ActionCreate(
                action_name=action,
                description=f"you can {action} in this module",
                is_active=True,
                module_id=module_item.id,  # type: ignore
            )
            action_operation.create_new_action(
                db=db, current_user=user_id, request=request_action
            )

    # Asignar todos sin repetirme el asignar uno es cambiar el query no mas xD
    actions_ids = db.query(Actions).all()
    for action_id in actions_ids:
        request_permission = assigned_action(
            role_id=role_id,  # type: ignore
            actions_id=action_id.id,
            description=f"role admin has {action_id.action_name} permission in this module",
        )
        permission_action.assing_role_and_actions(
            db=db, request=request_permission, current_user=user_id
        )
    print("User Created ツ")


def _print_welcome() -> None:
    """Funcion que genera una bienvenida y muestra el menu de usuario."""
    print("-" * 25)
    print("|  Welcome! (ツ)_/¯ | ")
    print("|  By @sr_vazkez :v    | ")
    print("-" * 25)
    print("\nDo you want to add a new super user?")
    print("\n Type: [C]reate user\n")


if __name__ == "__main__":
    _print_welcome()
    command = input()
    command = command.upper()

    if command == "C":
        """Se crea un usuario con permisos de administrador"""
        print("Creating user...\n")
        user_email = _get_user_email()
        user_password = _get_user_password()
        create_all(user_email, user_password)
    else:
        print("invalid command\n")
