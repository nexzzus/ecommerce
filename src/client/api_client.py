import requests

BASE_URL = "http://127.0.0.1:8002"


# ---------- ORDEN ----------


def listar_ordenes():
    r = requests.get(f"{BASE_URL}/orden")
    return r.json()


def obtener_orden(id):
    r = requests.get(f"{BASE_URL}/orden/{id}")
    return r.json()


def crear_orden(data):
    r = requests.post(f"{BASE_URL}/orden", json=data)
    return r.json()


def actualizar_orden(id, data):
    r = requests.put(f"{BASE_URL}/orden/{id}", json=data)
    return r.json()


def eliminar_orden(id):
    r = requests.delete(f"{BASE_URL}/orden/{id}")
    return r.json()


# ---------- DETALLE ORDEN ----------


def listar_detalles():
    r = requests.get(f"{BASE_URL}/detalle_orden")
    return r.json()


# ---------- PAGO ----------


def listar_pagos():
    r = requests.get(f"{BASE_URL}/pago")
    return r.json()
