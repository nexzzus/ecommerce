"""
Menú por consola para la API de usuarios, roles, permisos, producto, categoría y carrito.

Al ejecutar main.py se inicia la API (uvicorn) en segundo plano y luego
se muestra el menú interactivo que usa el cliente CRUD contra la API.
Debe ejecutarse desde la raíz del proyecto.
"""

import sys
import threading
import time

# Permitir importar desde src cuando se ejecuta desde la raíz del proyecto.
sys.path.insert(0, ".")

from src.crud.permissions import (  # noqa: E402
    list_permissions,
    get_permission,
    create_permission,
    update_permission,
    delete_permission,
)
from src.crud.roles import (  # noqa: E402
    list_roles,
    get_role,
    create_role,
    delete_role,
    update_role,
    set_role_permissions,
)
from src.crud.users import (  # noqa: E402
    list_users,
    get_user,
    create_user,
    update_user,
    delete_user,
    set_user_roles, register_user,
)
from src.crud.discounts import (  # noqa: E402
    list_discounts,
    get_discount,
    create_discount,
    update_discount,
    delete_discount,
)
from src.crud.category import (  # noqa: E402
    list_categories,
    get_category,
    create_category,
    update_category,
    delete_category,
)
from src.crud.products import (  # noqa: E402
    list_products,
    get_product,
    create_product,
    update_product,
    delete_product,
    set_product_categories,
)
from src.crud.cart_items import (  # noqa: E402
    list_cart_items,
    get_cart_item,
    create_cart_item,
    update_cart_item,
    delete_cart_item,
)


#
def _format_roles(roles: list) -> str:
    """
    Convierte una lista de roles (dict con 'name' o 'id') a texto.

    Args:
        roles: Lista de diccionarios con al menos 'name' o 'id'.

    Returns:
        Nombres separados por coma, o "—" si la lista está vacía.
    """
    if not roles:
        return "—"
    return ", ".join(r.get("name", str(r.get("id", ""))) for r in roles)


def show_users() -> None:
    """
    Lista todos los usuarios por consola con sus roles.

    Muestra id, nombre, apellido, email y roles. Captura errores de conexión
    y muestra un mensaje amigable.
    """
    try:
        users = list_users()
        if not users:
            print("  No hay usuarios.")
            return
        for u in users:
            roles_str = _format_roles(u.get("roles", []))
            print(
                f"  {u['id']} | {u['first_name']} | {u['last_name']} | "
                f"{u['email']} | roles: {roles_str}"
            )
    except Exception as e:
        err = str(e)
        if "10061" in err or "Connection refused" in err or "denegó" in err.lower():
            print(
                "  No se pudo conectar a la API. Espera unos segundos y vuelve a intentar."
            )
        else:
            print(f"  Error: {e}")


def show_permissions() -> None:
    """Lista todos los permisos por consola. Maneja errores de conexión."""
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
            print(
                "  No se pudo conectar a la API. Espera unos segundos y vuelve a intentar."
            )
        else:
            print(f"  Error: {e}")


def show_roles() -> None:
    """Lista todos los roles por consola. Maneja errores de conexión."""
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
            print(
                "  No se pudo conectar a la API. Espera unos segundos y vuelve a intentar."
            )
        else:
            print(f"  Error: {e}")


def show_discounts() -> None:
    """Lista todos los descuentos por consola. Maneja errores de conexión."""
    try:
        discounts = list_discounts()
        if not discounts:
            print("  No hay descuentos.")
            return
        for d in discounts:
            print(f"  {d['id']} | {d['code']} | value={d['value']} | {d['status']}")
    except Exception as e:
        err = str(e)
        if "10061" in err or "Connection refused" in err or "denegó" in err.lower():
            print(
                "  No se pudo conectar a la API. Espera unos segundos y vuelve a intentar."
            )
        else:
            print(f"  Error: {e}")


def show_categories() -> None:
    """Lista todas las categorías por consola. Maneja errores de conexión."""
    try:
        categories = list_categories()
        if not categories:
            print("  No hay categorías.")
            return
        for c in categories:
            print(f"  {c['id']} | {c['name']}")
    except Exception as e:
        err = str(e)
        if "10061" in err or "Connection refused" in err or "denegó" in err.lower():
            print(
                "  No se pudo conectar a la API. Espera unos segundos y vuelve a intentar."
            )
        else:
            print(f"  Error: {e}")


def _format_categories(categories: list) -> str:
    """Convierte lista de categorías (dict con 'name' o 'id') a texto."""
    if not categories:
        return "—"
    return ", ".join(c.get("name", str(c.get("id", ""))) for c in categories)


def show_cart_items() -> None:
    """Lista líneas del carrito por consola."""
    try:
        items = list_cart_items()
        if not items:
            print("  No hay líneas en el carrito.")
            return
        for it in items:
            uid = it.get("id_user") or "—"
            print(
                f"  {it['id']} | user={uid} | product={it['id_product']} | "
                f"qty={it['quantity']}"
            )
    except Exception as e:
        err = str(e)
        if "10061" in err or "Connection refused" in err or "denegó" in err.lower():
            print(
                "  No se pudo conectar a la API. Espera unos segundos y vuelve a intentar."
            )
        else:
            print(f"  Error: {e}")


def menu_cart_items() -> None:
    """Menú interactivo del carrito: listar, ver una, crear, actualizar, eliminar."""
    while True:
        print("\n--- Carrito (cart items) ---")
        print("1. Listar  2. Ver uno  3. Crear  4. Actualizar  5. Eliminar  0. Volver")
        op = input("Opción: ").strip()
        if op == "0":
            break
        if op == "1":
            show_cart_items()
        elif op == "2":
            cid = input("ID línea carrito: ").strip()
            if cid:
                try:
                    it = get_cart_item(cid)
                    print(f"  ID: {it.get('id')}")
                    print(f"  Usuario: {it.get('user') or '—'}")
                    print(f"  Producto: {it.get('product')}")
                    print(f"  Cantidad: {it.get('quantity')}")
                except Exception as e:
                    print(f"  Error: {e}")
        elif op == "3":
            id_product = input("ID producto: ").strip()
            qty_raw = input("Cantidad: ").strip()
            id_user = input("ID usuario (opcional, vacío=anónimo): ").strip() or None
            if not id_product or not qty_raw.isdigit():
                print("  Producto y cantidad numérica son obligatorios.")
                continue
            try:
                create_cart_item(id_product, int(qty_raw), id_user)
                print("  Línea creada.")
            except Exception as e:
                print(f"  Error: {e}")
        elif op == "4":
            cid = input("ID línea: ").strip()
            if not cid:
                continue
            qty_raw = input("Cantidad (vacío=no cambiar): ").strip()
            id_user_raw = input(
                "ID usuario (vacío=no cambiar, 'n'=quitar usuario): "
            ).strip()
            try:
                kwargs: dict = {}
                if qty_raw.isdigit():
                    kwargs["quantity"] = int(qty_raw)
                if id_user_raw == "n":
                    kwargs["clear_user"] = True
                elif id_user_raw:
                    kwargs["id_user"] = id_user_raw
                if not kwargs:
                    print("  Indica cantidad o usuario a cambiar.")
                    continue
                update_cart_item(cid, **kwargs)
                print("  Línea actualizada.")
            except Exception as e:
                print(f"  Error: {e}")
        elif op == "5":
            cid = input("ID línea a eliminar: ").strip()
            if cid:
                try:
                    delete_cart_item(cid)
                    print("  Línea eliminada.")
                except Exception as e:
                    print(f"  Error: {e}")


def show_products() -> None:
    """Lista todos los productos por consola. Maneja errores de conexión."""
    try:
        products = list_products()
        if not products:
            print("  No hay productos.")
            return
        for p in products:
            cats = _format_categories(p.get("categories", []))
            disc = p.get("discount")
            disc_str = disc.get("code", str(disc.get("id", ""))) if disc else "—"
            print(
                f"  {p['id']} | {p['name']} | {p['price']} | stock={p['stock']} | "
                f"discount={disc_str} | categories: {cats}"
            )
    except Exception as e:
        err = str(e)
        if "10061" in err or "Connection refused" in err or "denegó" in err.lower():
            print(
                "  No se pudo conectar a la API. Espera unos segundos y vuelve a intentar."
            )
        else:
            print(f"  Error: {e}")


def menu_users() -> None:
    """
    Menú interactivo de usuarios.

    Opciones: listar, ver uno, crear, actualizar, eliminar, asignar roles.
    """
    while True:
        print("\n--- Usuarios ---")
        print(
            "1. Listar  2. Ver uno  3. Crear  4. Actualizar  "
            "5. Eliminar  6. Asignar roles  7. Registro 0. Volver"
        )
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
            phone = input("Teléfono: ").strip()
            address = input("Dirección: ").strip()
            if not (first_name and last_name and email and password):
                print(
                    "  Faltan datos (nombre, apellido, email y contraseña son obligatorios)."
                )
                continue
            show_roles()
            raw_roles = input("IDs de roles (opcional, separados por coma): ").strip()
            role_ids = [r.strip() for r in raw_roles.split(",") if r.strip()] or None
            try:
                create_user(
                    first_name,
                    last_name,
                    email,
                    password,
                    phone or None,
                    address or None,
                    role_ids=role_ids,
                )
                print("  Usuario creado.")
            except Exception as e:
                print(f"  Error: {e}")
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
        elif op == "7":
            first_name = input("Nombre: ").strip()
            last_name = input("Apellido: ").strip()
            email = input("Email: ").strip()
            password = input("Contraseña: ").strip()
            phone = input("Teléfono: ").strip()
            address = input("Dirección: ").strip()
            if not (first_name and last_name and email and password):
                print(
                    "  Faltan datos (nombre, apellido, email y contraseña son obligatorios)."
                )
                continue
            try:
                register_user(
                    first_name,
                    last_name,
                    email,
                    password,
                    phone or None,
                    address or None,
                )
                print("  Usuario registrado.")
            except Exception as e:
                print(f"  Error: {e}")


def menu_roles() -> None:
    """
    Menú interactivo de roles.

    Opciones: listar, ver uno, crear, actualizar, eliminar, asignar permisos.
    """
    while True:
        print("\n--- Roles ---")
        print(
            "1. Listar  2. Ver uno  3. Crear  4. Actualizar  "
            "5. Eliminar  6. Asignar permisos  0. Volver"
        )
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


def menu_permissions() -> None:
    """Menú interactivo de permisos: listar, ver uno, crear, actualizar, eliminar."""
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


def menu_discounts() -> None:
    """Menú interactivo de descuentos: listar, ver uno, crear, actualizar, eliminar."""
    while True:
        print("\n--- Descuentos ---")
        print("1. Listar  2. Ver uno  3. Crear  4. Actualizar  5. Eliminar  0. Volver")
        op = input("Opción: ").strip()
        if op == "0":
            break
        if op == "1":
            show_discounts()
        elif op == "2":
            did = input("ID descuento: ").strip()
            if did:
                try:
                    d = get_discount(did)
                    print(f"  {d}")
                except Exception as e:
                    print(f"  Error: {e}")
        elif op == "3":
            value = input("Valor: ").strip()
            code = input("Código: ").strip()
            status = input("Estado (vacío=active): ").strip() or "active"
            if value and code:
                try:
                    create_discount(value, code, status)
                    print("  Descuento creado.")
                except Exception as e:
                    print(f"  Error: {e}")
            else:
                print("  Faltan datos (valor y código).")
        elif op == "4":
            did = input("ID descuento: ").strip()
            if not did:
                continue
            value = input("Valor (vacío=no cambiar): ").strip()
            code = input("Código (vacío=no cambiar): ").strip()
            status = input("Estado (vacío=no cambiar): ").strip()
            try:
                kwargs = {}
                if value:
                    kwargs["value"] = value
                if code:
                    kwargs["code"] = code
                if status:
                    kwargs["status"] = status
                update_discount(did, **kwargs)
                print("  Descuento actualizado.")
            except Exception as e:
                print(f"  Error: {e}")
        elif op == "5":
            did = input("ID descuento a eliminar: ").strip()
            if did:
                try:
                    delete_discount(did)
                    print("  Descuento eliminado.")
                except Exception as e:
                    print(f"  Error: {e}")


def menu_categories() -> None:
    """Menú interactivo de categorías: listar, ver una, crear, actualizar, eliminar."""
    while True:
        print("\n--- Categorías ---")
        print("1. Listar  2. Ver una  3. Crear  4. Actualizar  5. Eliminar  0. Volver")
        op = input("Opción: ").strip()
        if op == "0":
            break
        if op == "1":
            show_categories()
        elif op == "2":
            cid = input("ID categoría: ").strip()
            if cid:
                try:
                    c = get_category(cid)
                    print(f"  {c}")
                except Exception as e:
                    print(f"  Error: {e}")
        elif op == "3":
            name = input("Nombre: ").strip()
            if name:
                try:
                    create_category(name)
                    print("  Categoría creada.")
                except Exception as e:
                    print(f"  Error: {e}")
            else:
                print("  Faltan datos.")
        elif op == "4":
            cid = input("ID categoría: ").strip()
            if not cid:
                continue
            name = input("Nombre (vacío=no cambiar): ").strip()
            try:
                kwargs = {}
                if name:
                    kwargs["name"] = name
                update_category(cid, **kwargs)
                print("  Categoría actualizada.")
            except Exception as e:
                print(f"  Error: {e}")
        elif op == "5":
            cid = input("ID categoría a eliminar: ").strip()
            if cid:
                try:
                    delete_category(cid)
                    print("  Categoría eliminada.")
                except Exception as e:
                    print(f"  Error: {e}")


def menu_products() -> None:
    """
    Menú interactivo de productos: listar, ver uno, crear,
    actualizar, eliminar, asignar categorías.
    """
    while True:
        print("\n--- Productos ---")
        print(
            "1. Listar  2. Ver uno  3. Crear  4. Actualizar  "
            "5. Eliminar  6. Asignar categorías  0. Volver"
        )
        op = input("Opción: ").strip()
        if op == "0":
            break
        if op == "1":
            show_products()
        elif op == "2":
            pid = input("ID producto: ").strip()
            if pid:
                try:
                    p = get_product(pid)
                    cats = _format_categories(p.get("categories", []))
                    print(
                        f"  ID: {p.get('id')} | {p.get('name')} | {p.get('price')} "
                        f"| stock={p.get('stock')}"
                    )
                    print(f"  Descripción: {p.get('description') or '—'}")
                    print(f"  Descuento: {p.get('discount') or '—'}")
                    print(f"  Categorías: {cats}")
                except Exception as e:
                    print(f"  Error: {e}")
        elif op == "3":
            name = input("Nombre: ").strip()
            price = input("Precio: ").strip()
            description = input("Descripción (opcional): ").strip()
            stock = input("Stock (vacío=0): ").strip()
            stock = int(stock) if stock.isdigit() else 0
            if not (name and price):
                print("  Faltan datos (nombre y precio son obligatorios).")
                continue
            show_discounts()
            id_discount = input("ID descuento (opcional): ").strip() or None
            show_categories()
            raw_cats = input(
                "IDs de categorías (opcional, separados por coma): "
            ).strip()
            category_ids = [c.strip() for c in raw_cats.split(",") if c.strip()] or None
            try:
                create_product(
                    name, price, description or None, stock, id_discount, category_ids
                )
                print("  Producto creado.")
            except Exception as e:
                print(f"  Error: {e}")
        elif op == "4":
            pid = input("ID producto: ").strip()
            if not pid:
                continue
            name = input("Nombre (vacío=no cambiar): ").strip()
            price = input("Precio (vacío=no cambiar): ").strip()
            description = input("Descripción (vacío=no cambiar): ").strip()
            stock = input("Stock (vacío=no cambiar): ").strip()
            id_discount = input("ID descuento (vacío=no cambiar, 'n'=quitar): ").strip()
            try:
                kwargs = {}
                if name:
                    kwargs["name"] = name
                if price:
                    kwargs["price"] = price
                if description:
                    kwargs["description"] = description
                if stock.isdigit():
                    kwargs["stock"] = int(stock)
                if id_discount == "n":
                    kwargs["id_discount"] = None
                elif id_discount:
                    kwargs["id_discount"] = id_discount
                update_product(pid, **kwargs)
                print("  Producto actualizado.")
            except Exception as e:
                print(f"  Error: {e}")
        elif op == "5":
            pid = input("ID producto a eliminar: ").strip()
            if pid:
                try:
                    delete_product(pid)
                    print("  Producto eliminado.")
                except Exception as e:
                    print(f"  Error: {e}")
        elif op == "6":
            pid = input("ID producto: ").strip()
            if not pid:
                continue
            show_categories()
            raw = input("IDs de categorías (separados por coma): ").strip()
            if not raw:
                print("  No se indicaron categorías.")
                continue
            category_ids = [c.strip() for c in raw.split(",") if c.strip()]
            try:
                set_product_categories(pid, category_ids)
                print("  Categorías asignadas al producto.")
            except Exception as e:
                print(f"  Error: {e}")


def _start_api() -> None:
    """Ejecuta uvicorn en un hilo en segundo plano (host 0.0.0.0, puerto 8000)."""
    import uvicorn

    uvicorn.run("src.app:app", host="0.0.0.0", port=8000, log_level="warning")


def main() -> None:
    """Punto de entrada: inicia la API en segundo plano y el menú por consola."""
    print("API Usuarios - Menú por consola")
    print("Iniciando API en http://localhost:8000 ...")
    server = threading.Thread(target=_start_api, daemon=True)
    server.start()
    time.sleep(1.5)
    print("API lista.\n")
    while True:
        print("\n========== MENÚ ==========")
        print(
            "1. Usuarios  2. Roles  3. Permisos  4. Descuentos  "
            "5. Categorías  6. Productos  7. Carrito  0. Salir"
        )
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
        elif op == "4":
            menu_discounts()
        elif op == "5":
            menu_categories()
        elif op == "6":
            menu_products()
        elif op == "7":
            menu_cart_items()
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    main()
