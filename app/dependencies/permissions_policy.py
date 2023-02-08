from app.dependencies.permissions import RoleChecker

"""Aqui definimos la politica de permisos y a que modulo pertenecen
Ya esto se define de forma en crudo :D.
Tambien puedes usar los GUUIDS pero ya sera a tu criterio 
Recuerda importarlo y usalo como dependencia para que funcione.
"""


users_create = RoleChecker({"module": "users", "permission": "create"})

users_read = RoleChecker({"module": "users", "permission": "read"})

users_update = RoleChecker({"module": "users", "permission": "update"})

users_delete = RoleChecker({"module": "users", "permission": "delete"})

roles_create = RoleChecker({"module": "roles", "permission": "create"})

roles_read = RoleChecker({"module": "roles", "permission": "read"})

roles_update = RoleChecker({"module": "roles", "permission": "update"})

roles_delete = RoleChecker({"module": "roles", "permission": "delete"})

modules_create = RoleChecker({"module": "modules", "permission": "create"})

modules_read = RoleChecker({"module": "modules", "permission": "read"})

modules_update = RoleChecker({"module": "modules", "permission": "update"})

modules_delete = RoleChecker({"module": "modules", "permission": "delete"})

actions_create = RoleChecker({"module": "actions", "permission": "create"})

actions_read = RoleChecker({"module": "actions", "permission": "read"})

actions_update = RoleChecker({"module": "actions", "permission": "update"})

actions_delete = RoleChecker({"module": "actions", "permission": "delete"})

permissions_create = RoleChecker({"module": "permissions", "permission": "create"})

permissions_read = RoleChecker({"module": "permissions", "permission": "read"})

permissions_update = RoleChecker({"module": "permissions", "permission": "update"})

permissions_delete = RoleChecker({"module": "permissions", "permission": "delete"})
