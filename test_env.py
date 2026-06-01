from src.logic.environment import load_world

print("--- INICIANDO PRUEBAS DE QA ---")

archivos = [
    "data/mundo.txt",
    "data/error_dimension.txt",
    "data/error_sin_pasajero.txt"
]

for archivo in archivos:
    print(f"\nProbando archivo: {archivo}")
    try:
        mundo, inicio, pasajeros, destino = load_world(archivo)
        print("EXITO: El mapa cargó correctamente.")
        print(f"Inicio: {inicio}, Destino: {destino}, Pasajeros: {pasajeros}")
    except Exception as e:
        print(f"FALLA CONTROLADA (El validador hizo su trabajo): {e}")