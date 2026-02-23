# models/producto.py
from dataclasses import dataclass

@dataclass
class Producto:
    nombre: str
    cantidad: int = 0

    def __post_init__(self):
        if not isinstance(self.cantidad, int) or self.cantidad < 0:
            raise ValueError("La cantidad debe ser un entero >= 0.")
        # Normalización simple del nombre
        self.nombre = self.nombre.strip()