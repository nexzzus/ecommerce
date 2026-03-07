"""
Menú por consola que usa el CRUD (cliente de la API).
Al ejecutar main.py se inicia la API en segundo plano (uvicorn) y luego el menú.
"""
import sys
import threading
import time

from src.crud.permissions import list_permissions, get_permission, create_permission, update_permission, \
    delete_permission
from src.crud.roles import list_roles, get_role, create_role, delete_role, update_role, set_role_permissions

# Permitir importar desde src cuando se ejecuta desde la raíz del proyecto
sys.path.insert(0, ".")

from src.crud.users import (
    list_users,
    get_user,
    create_user,
    update_user,
    delete_user,
    set_user_roles,
)


def _format_roles(roles: list) -> str:
    """Convierte lista de roles (dict con 'name') a texto."""
    if not roles:
        return "—"
    return ", ".join(r.get("name", str(r.get("id", ""))) for r in roles)


def show_users():
    try:
        users = list_users()
        if not users:
            print("  No hay usuarios.")
            return
        for u in users:
            roles_str = _format_roles(u.get("roles", []))
            print(f"  {u['id']} | {u['first_name']} | {u['last_name']} | {u['email']} | roles: {roles_str}")
    except Exception as e:
        err = str(e)
        if "10061" in err or "Connection refused" in err or "denegó" in err.lower():
            print("  No se pudo conectar a la API. Espera unos segundos y vuelve a intentar.")
        else:
            print(f"  Error: {e}")


def show_permissions():
    try:
        permissions = list_permissions()
        if not permissions:
            print("  No hay permisos.")
            return
        for p in permissions:
            print(f"  {p['id']} | {p['name']} | {p['description']}")
    except Exception as e:
        err = str(e)
        if "10061" in err or "Connection refused" in err or "denegó" in err.lower():
            print("  No se pudo conectar a la API. Espera unos segundos y vuelve a intentar.")
        else:
            print(f"  Error: {e}")


def show_roles():
    try:
        roles = list_roles()
        if not roles:
            print("  No hay roles.")
            return
        for r in roles:
            print(f"  {r['id']} | {r['name']}")
    except Exception as e:
        err = str(e)
        if "10061" in err or "Connection refused" in err or "denegó" in err.lower():
            print("  No se pudo conectar a la API. Espera unos segundos y vuelve a intentar.")
        else:
            print(f"  Error: {e}")


def menu_users():
    while True:
        print("\n--- Usuarios ---")
        print("1. Listar  2. Ver uno  3. Crear  4. Actualizar  5. Eliminar  6. Asignar roles  0. Volver")
        op = input("Opción: ").strip()
        if op == "0":
            break
        if op == "1":
            show_users()
        elif op == "2":
            uid = input("ID usuario: ").strip()
            if uid:
                try:
                    u = get_user(uid)
                    roles_str = _format_roles(u.get("roles", []))
                    print(f"  ID: {u.get('id')}")
                    print(f"  Nombre: {u.get('first_name')} {u.get('last_name')}")
                    print(f"  Email: {u.get('email')}")
                    print(f"  Teléfono: {u.get('phone') or '—'}")
                    print(f"  Dirección: {u.get('address') or '—'}")
                    print(f"  Roles: {roles_str}")
                except Exception as e:
                    print(f"  Error: {e}")
        elif op == "3":
            first_name = input("Nombre: ").strip()
            last_name = input("Apellido: ").strip()
            email = input("Email: ").strip()
            password = input("Contraseña: ").strip()
            phone = input("Teléfono (opcional): ").strip()
            address = input("Dirección (opcional): ").strip()
            if first_name and last_name and email and password and phone and address:
                try:
                    create_user(first_name, last_name, email, password, phone, address)
                    print("  Usuario creado.")
                except Exception as e:
                    print(f"  Error: {e}")
            else:
                print("  Faltan datos.")
        elif op == "4":
            uid = input("ID usuario: ").strip()
            if not uid:
                continue
            first_name = input("Nombre (vacío=no cambiar): ").strip()
            last_name = input("Apellido (vacío=no cambiar): ").strip()
            email = input("Email (vacío=no cambiar): ").strip()
            password = input("Contraseña (vacío=no cambiar): ").strip()
            phone = input("Teléfono (vacío=no cambiar): ").strip()
            address = input("Dirección (vacío=no cambiar): ").strip()
            try:
                kwargs = {}
                if first_name:
                    kwargs["first_name"] = first_name
                if last_name:
                    kwargs["last_name"] = last_name
                if email:
                    kwargs["email"] = email
                if password:
                    kwargs["password"] = password
                if phone:
                    kwargs["phone"] = phone
                if address:
                    kwargs["address"] = address
                update_user(uid, **kwargs)
                print("  Usuario actualizado.")
            except Exception as e:
                print(f"  Error: {e}")
        elif op == "5":
            uid = input("ID usuario a eliminar: ").strip()
            if uid:
                try:
                    delete_user(uid)
                    print("  Usuario eliminado.")
                except Exception as e:
                    print(f"  Error: {e}")
        elif op == "6":
            uid = input("ID usuario: ").strip()
            if not uid:
                continue
            show_roles()
            raw = input("IDs de roles (separados por coma): ").strip()
            if not raw:
                print("  No se indicaron roles.")
                continue
            role_ids = [r.strip() for r in raw.split(",") if r.strip()]
            try:
                set_user_roles(uid, role_ids)
                print("  Roles asignados al usuario.")
            except Exception as e:
                print(f"  Error: {e}")


def menu_roles():
    while True:
        print("\n--- Roles ---")
        print("1. Listar  2. Ver uno  3. Crear  4. Actualizar  5. Eliminar  6. Asignar permisos  0. Volver")
        op = input("Opción: ").strip()
        if op == "0":
            break
        if op == "1":
            show_roles()
        elif op == "2":
            rid = input("ID rol: ").strip()
            if rid:
                try:
                    r = get_role(rid)
                    print(f"  {r}")
                except Exception as e:
                    print(f"  Error: {e}")
        elif op == "3":
            name = input("Nombre: ").strip()
            if name:
                try:
                    create_role(name)
                    print("  Rol creado.")
                except Exception as e:
                    print(f"  Error: {e}")
            else:
                print("  Faltan datos.")
        elif op == "4":
            rid = input("ID rol: ").strip()
            if not rid:
                continue
            name = input("Nombre (vacío=no cambiar): ").strip()

            try:
                kwargs = {}
                if name:
                    kwargs["name"] = name
                update_role(rid, **kwargs)
                print("  Rol actualizado.")
            except Exception as e:
                print(f"  Error: {e}")
        elif op == "5":
            uid = input("ID rol a eliminar: ").strip()
            if uid:
                try:
                    delete_role(uid)
                    print("  rol eliminado.")
                except Exception as e:
                    print(f"  Error: {e}")
        elif op == "6":
            rid = input("ID rol: ").strip()
            if not rid:
                continue
            show_permissions()
            raw = input("IDs de permisos (separados por coma): ").strip()
            if not raw:
                print("  No se indicaron permisos.")
                continue
            perm_ids = [p.strip() for p in raw.split(",") if p.strip()]
            try:
                set_role_permissions(rid, perm_ids)
                print("  Permisos asignados al rol.")
            except Exception as e:
                print(f"  Error: {e}")


def menu_permissions():
    while True:
        print("\n--- Permisos ---")
        print("1. Listar  2. Ver uno  3. Crear  4. Actualizar  5. Eliminar  0. Volver")
        op = input("Opción: ").strip()
        if op == "0":
            break
        if op == "1":
            show_permissions()
        elif op == "2":
            pid = input("ID permiso: ").strip()
            if pid:
                try:
                    r = get_permission(pid)
                    print(f"  {r}")
                except Exception as e:
                    print(f"  Error: {e}")
        elif op == "3":
            name = input("Nombre: ").strip()
            description = input("Description: ").strip()
            if name and description:
                try:
                    create_permission(name, description)
                    print("  Permiso creado.")
                except Exception as e:
                    print(f"  Error: {e}")
            else:
                print("  Faltan datos.")
        elif op == "4":
            pid = input("ID permiso: ").strip()
            if not pid:
                continue
            name = input("Nombre (vacío=no cambiar): ").strip()
            description = input("Descripción (vacío=no cambiar): ").strip()

            try:
                kwargs = {}
                if name:
                    kwargs["name"] = name
                if description:
                    kwargs["description"] = description
                update_permission(pid, **kwargs)
                print("  Permiso actualizado.")
            except Exception as e:
                print(f"  Error: {e}")
        elif op == "5":
            uid = input("ID permiso a eliminar: ").strip()
            if uid:
                try:
                    delete_permission(uid)
                    print("  permiso eliminado.")
                except Exception as e:
                    print(f"  Error: {e}")


def _start_api():
    """Ejecuta uvicorn en un hilo en segundo plano."""
    import uvicorn
    uvicorn.run("src.app:app", host="0.0.0.0", port=8000, log_level="warning")


def main():
    print("API Usuarios - Menú por consola")
    print("Iniciando API en http://localhost:8000 ...")
    server = threading.Thread(target=_start_api, daemon=True)
    server.start()
    time.sleep(1.5)
    print("API lista.\n")
    while True:
        print("\n========== MENÚ ==========")
        print("1. Usuarios  2. Roles  3. Permisos  0. Salir")
        op = input("Opción: ").strip()
        if op == "0":
            print("Hasta luego.")
            break
        if op == "1":
            menu_users()
        elif op == "2":
            menu_roles()
        elif op == "3":
            menu_permissions()
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    main()
