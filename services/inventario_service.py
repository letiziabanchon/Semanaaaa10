# services/inventario_service.py
import os
from typing import Tuple
from models.inventario import Inventario
from models.producto import Producto

class InventarioService:
    """
    Capa de servicio:
      - Se encarga de cargar/guardar desde/ hacia archivo de texto.
      - Maneja excepciones de E/S y valida entradas externas.
      - Expone métodos de alto nivel que usa la interfaz (main).
    """
    def __init__(self, ruta_archivo: str = "data/inventario.txt") -> None:
        self.ruta = ruta_archivo
        self.inv = Inventario()

    # ----------------- Persistencia -----------------
    def _asegurar_directorio(self) -> None:
        base = os.path.dirname(self.ruta) or "."
        os.makedirs(base, exist_ok=True)

    def cargar(self) -> Tuple[bool, str]:
        """Carga el inventario desde disco. Crea el archivo si no existe."""
        try:
            self._asegurar_directorio()
            if not os.path.exists(self.ruta):
                # Crear archivo vacío
                open(self.ruta, "w", encoding="utf-8").close()
                return True, "Inventario vacío creado."

            with open(self.ruta, "r", encoding="utf-8") as f:
                for i, linea in enumerate(f, start=1):
                    linea = linea.strip()
                    if not linea:
                        continue
                    # Formato esperado: nombre,cantidad
                    partes = linea.split(",")
                    if len(partes) != 2:
                        # Línea corrupta: se ignora pero se informa
                        print(f"Línea {i} ignorada (formato inválido): {linea}")
                        continue
                    nombre, cantidad_txt = partes[0].strip(), partes[1].strip()
                    try:
                        cantidad = int(cantidad_txt)
                        self.inv.agregar_o_sumar(nombre, cantidad)
                    except ValueError:
                        print(f"Línea {i} ignorada (cantidad no entera): {linea}")
                        continue

            return True, "Inventario cargado correctamente."
        except PermissionError:
            return False, "Permiso denegado al leer el archivo de inventario."
        except FileNotFoundError:
            # Teóricamente cubierto por exists, pero por robustez:
            try:
                open(self.ruta, "w", encoding="utf-8").close()
                return True, "Archivo de inventario no existía. Se creó uno nuevo."
            except Exception as e:
                return False, f"No se pudo crear el archivo: {e}"
        except Exception as e:
            return False, f"Error inesperado al cargar inventario: {e}"

    def _guardar_total(self) -> Tuple[bool, str]:
        """Escribe todo el inventario actual a disco (modo seguro: sobrescribe)."""
        try:
            self._asegurar_directorio()
            with open(self.ruta, "w", encoding="utf-8") as f:
                for p in self.inv.listar():
                    f.write(f"{p.nombre},{p.cantidad}\n")
            return True, "Cambios guardados en disco."
        except PermissionError:
            return False, "Permiso denegado al escribir el archivo."
        except Exception as e:
            return False, f"Error inesperado al guardar: {e}"

    # ----------------- API de alto nivel -----------------
    def agregar_producto(self, nombre: str, cantidad_str: str) -> Tuple[bool, str]:
        try:
            nombre = (nombre or "").strip()
            if not nombre:
                return False, "El nombre no puede estar vacío."

            cantidad = int(cantidad_str)
            self.inv.agregar_o_sumar(nombre, cantidad)
            ok, msg = self._guardar_total()
            if ok:
                return True, f"Producto '{nombre}' agregado/actualizado (+{cantidad})."
            return False, msg
        except ValueError:
            return False, "La cantidad debe ser un número entero > 0."
        except Exception as e:
            return False, f"Error al agregar producto: {e}"

    def eliminar_producto(self, nombre: str) -> Tuple[bool, str]:
        nombre = (nombre or "").strip()
        if not nombre:
            return False, "Debes indicar un nombre."
        try:
            if self.inv.eliminar(nombre):
                ok, msg = self._guardar_total()
                if ok:
                    return True, f"Producto '{nombre}' eliminado."
                return False, msg
            return False, "El producto no existe."
        except Exception as e:
            return False, f"Error al eliminar: {e}"

    def listar(self) -> Tuple[bool, str, list[Producto]]:
        try:
            return True, "OK", self.inv.listar()
        except Exception as e:
            return False, f"Error al listar: {e}", []