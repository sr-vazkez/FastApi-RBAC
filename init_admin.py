#!/usr/bin/env python
# -*- coding: utf-8 -*-

from decouple import config

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


def create_roles(list_of_roles):
    """Create all roles.

    Args:
        list_of_roles (_type_): _description_
    """
    for role in list_of_roles:
        request = RoleCreate(name=role, description="Role for a system")
        role_action.create_new_role(
            db=db, request=request, current_user=None  # type: ignore
        )
    print("All roles created")


def create_super_Admin(user_email: str, user_password: str):
    """Create super user.

    Args:
        user_email (str): a valid email
        user_password (str): a strong password
    """
    super_rol = db.query(Role.id).filter_by(name="super admin").first()
    role_id = ""
    for role_id in super_rol:  # type: ignore
        type(role_id)

    request_user = UserCreate(
        email=str.encode(user_email),  # type: ignore
        password=user_password,
        role_id=role_id.__str__(),  # type: ignore
    )

    user_action.create_new_user(
        db=db, current_user=None, request=request_user  # type: ignore
    )
    user = db.query(Users.id).filter_by(email=user_email.__str__()).first()
    user_id = ""
    for user_id in user:  # type: ignore
        type(user_id)
    print("Super user ready!")
    return user_id


def create_modules_actions(user_id: str):
    """Create a modules.

    Add a string module in the varieble modulos an create all.

    Args:
        user_id (str): ID For user.
    """
    # Como crear 4 permisos sin repetirme xD?
    modulos = ["users", "roles", "actions", "modules", "permissions"]
    for modulo in modulos:
        request_module = ModuleCreate(
            name=modulo.__str__(),
            description=f"Module for {modulo.__str__()} permissions",
        )
        module_action.create_module(
            db=db, request=request_module, current_user=user_id.__str__()
        )
    modulos = db.query(Module).all()
    # como crear todas las acciones de todos los modulos sin repetirme?
    for module_item in modulos:
        action_list = ["create", "read", "update", "delete"]
        for action in action_list:
            # print(action,module_item.name)
            request_action = ActionCreate(
                action_name=action.__str__(),
                description=f"you can {action.__str__()}!",
                is_active=True,
                module_id=module_item.id.__str__(),  # type: ignore
            )
            action_operation.create_new_action(
                db=db, current_user=user_id.__str__(), request=request_action
            )


def create_permissions(user_id: str):
    """Create an assign permissions at role.

    Args:
        user_id (str): ID For user.
    """
    # Asignar todos sin repetirme el asignar uno es cambiar el query no mas xD
    # actions_ids = db.query(Actions).all()
    # Query del rol
    roles_items = db.query(Role).all()
    for role_item in roles_items:
        # print(role_item)
        if role_item.name == "super admin":
            print("asignado permisos", role_item.name)
            actions_ids = db.query(Actions).all()
            for action_id in actions_ids:
                request_permission = assigned_action(
                    role_id=role_item.id.__str__(),  # type: ignore
                    actions_id=action_id.id.__str__(),
                    description=f"role has {action_id.action_name} permission",
                )
                permission_action.assing_role_and_actions(
                    db=db, request=request_permission, current_user=user_id.__str__()
                )

        if role_item.name == "admin":
            print("asignado permisos al", role_item.name)
            admin_permissions = (
                db.query(
                    Actions.id,
                    Actions.action_name,
                    Module.id.label("module_name"),
                    Module.name,
                )
                .join(Module)
                .filter(Module.name != "modules")
                .filter(Module.name != "actions")
                .all()
            )
            # print(admin_permissions)
            for admin_permission in admin_permissions:
                request_permission = assigned_action(
                    role_id=role_item.id.__str__(),  # type: ignore
                    actions_id=admin_permission.id.__str__(),
                    description=f"role has {admin_permission.action_name} permission",
                )
                permission_action.assing_role_and_actions(
                    db=db, request=request_permission, current_user=user_id.__str__()
                )
        if role_item.name == "operator":
            operator_permissions = (
                db.query(
                    Actions.id,
                    Actions.action_name,
                    Module.id.label("module_name"),
                    Module.name,
                )
                .join(Module)
                .filter(Module.name != "modules")
                .filter(Module.name != "actions")
                .filter(Module.name != "permissions")
                .filter(Module.name != "roles")
                .filter(Module.name != "users")
                .all()
            )
            for operator_permission in operator_permissions:
                request_permission = assigned_action(
                    role_id=role_item.id.__str__(),  # type: ignore
                    actions_id=operator_permission.id.__str__(),
                    description=f"role has {operator_permission.action_name} permission",
                )
                permission_action.assing_role_and_actions(
                    db=db, request=request_permission, current_user=user_id.__str__()
                )
        if role_item.name == "viewer":
            viewer_permissions = (
                db.query(
                    Actions.id,
                    Actions.action_name,
                    Module.id.label("module_name"),
                    Module.name,
                )
                .join(Module)
                .filter(Module.name != "modules")
                .filter(Module.name != "actions")
                .filter(Module.name != "permissions")
                .filter(Module.name != "roles")
                .filter(Module.name != "users")
                .filter(Actions.action_name == "read")
                .all()
            )
            for viewer_permission in viewer_permissions:
                request_permission = assigned_action(
                    role_id=role_item.id.__str__(),  # type: ignore
                    actions_id=viewer_permission.id.__str__(),
                    description=f"role has {viewer_permission.action_name} permission",
                )
                permission_action.assing_role_and_actions(
                    db=db, request=request_permission, current_user=user_id.__str__()
                )

    print("All permissions assigned ツ")


def _print_welcome() -> None:
    """Funcion que genera una bienvenida y muestra el menu de usuario."""
    print("-" * 25)
    print("|  Welcome! (ツ)_/¯ | ")
    print("|  By @sr_vazkez :v    | ")
    print("-" * 25)


if __name__ == "__main__":
    _print_welcome()

    print("Creating user...\n")
    create_roles(list_of_roles=["super admin", "admin", "operator", "viewer"])
    user_id = create_super_Admin(
        user_email=f"{config('APP_ADMIN_USER')}",
        user_password=f"{config('APP_ADMIN_PASS')}",
    )
    create_modules_actions(user_id)
    create_permissions(user_id)
