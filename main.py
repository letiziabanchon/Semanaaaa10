# main.py
from services.inventario_service import InventarioService

def mostrar_inventario(svc: InventarioService) -> None:
    ok, _, productos = svc.listar()
    if not ok or not productos:
        print("Inventario vacío.")
        return

    print("\n INVENTARIO:")
    for p in productos:
        print(f"- {p.nombre}: {p.cantidad}")
    print()

def main() -> None:
    svc = InventarioService()
    ok, msg = svc.cargar()
    print(msg)

    while True:
        print("\n=== SISTEMA DE INVENTARIO ===")
        print("1. Mostrar inventario")
        print("2. Agregar o sumar producto")
        print("3. Eliminar producto")
        print("4. Salir")
        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            mostrar_inventario(svc)

        elif opcion == "2":
            nombre = input("Nombre del producto: ")
            cantidad = input("Cantidad a agregar: ")
            ok, msg = svc.agregar_producto(nombre, cantidad)
            print(msg)

        elif opcion == "3":
            nombre = input("Nombre del producto a eliminar: ")
            ok, msg = svc.eliminar_producto(nombre)
            print(msg)

        elif opcion == "4":
            print("Saliendo del sistema...")
            break

        else:
            print("Opción inválida. Intente de nuevo.")

if __name__ == "__main__":
    main()