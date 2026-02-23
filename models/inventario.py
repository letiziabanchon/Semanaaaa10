# models/inventario.py
from typing import Dict, List
from .producto import Producto

class Inventario:
    """
    Inventario: contiene productos en memoria y expone operaciones
    de negocio puras (sin leer/escribir archivos).
    """
    def __init__(self) -> None:
        self._items: Dict[str, Producto] = {}

    # ---- Consultas ----
    def listar(self) -> List[Producto]:
        return list(self._items.values())

    def existe(self, nombre: str) -> bool:
        return nombre in self._items

    def obtener(self, nombre: str) -> Producto | None:
        return self._items.get(nombre)

    def esta_vacio(self) -> bool:
        return len(self._items) == 0

    # ---- Comandos ----
    def agregar_o_sumar(self, nombre: str, cantidad: int) -> Producto:
        if cantidad <= 0:
            raise ValueError("La cantidad a agregar debe ser > 0.")
        if nombre in self._items:
            p = self._items[nombre]
            p.cantidad += cantidad
            return p
        nuevo = Producto(nombre=nombre, cantidad=cantidad)
        self._items[nombre] = nuevo
        return nuevo

    def eliminar(self, nombre: str) -> bool:
        if nombre in self._items:
            del self._items[nombre]
            return True
        return False