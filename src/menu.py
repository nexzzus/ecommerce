import requests

BASE_URL = "http://127.0.0.1:8001"


def listar_ordenes():
    r = requests.get(f"{BASE_URL}/orden")
    print(r.json())


def crear_orden():
    fecha = input("Fecha (YYYY-MM-DD): ")
    total = float(input("Total: "))

    data = {
        "fecha": fecha,
        "total": total
    }

    r = requests.post(f"{BASE_URL}/orden", json=data)
    print(r.json())


def obtener_orden():
    orden_id = input("ID de la orden: ")

    r = requests.get(f"{BASE_URL}/orden/{orden_id}")
    print(r.json())


def actualizar_orden():
    orden_id = input("ID de la orden: ")
    fecha = input("Nueva fecha (YYYY-MM-DD): ")
    total = float(input("Nuevo total: "))

    data = {
        "fecha": fecha,
        "total": total
    }

    r = requests.put(f"{BASE_URL}/orden/{orden_id}", json=data)
    print(r.json())


def eliminar_orden():
    orden_id = input("ID de la orden: ")

    r = requests.delete(f"{BASE_URL}/orden/{orden_id}")
    print(r.json())


def menu():
    while True:
        print("\nMENU ORDEN")
        print("1. Listar ordenes")
        print("2. Crear orden")
        print("3. Ver orden")
        print("4. Actualizar orden")
        print("5. Eliminar orden")
        print("6. Salir")

        opcion = input("Seleccione una opcion: ")

        if opcion == "1":
            listar_ordenes()

        elif opcion == "2":
            crear_orden()

        elif opcion == "3":
            obtener_orden()

        elif opcion == "4":
            actualizar_orden()

        elif opcion == "5":
            eliminar_orden()

        elif opcion == "6":
            break


if __name__ == "__main__":
    menu()