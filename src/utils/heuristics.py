def Manhattan(pos1, pos2):
    """Calcula la distancia de Manhattan entre dos puntos (r1, c1) y (r2, c2)."""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def calcular_heuristica(pos_actual, pasajeros_totales, recogidos, destino):
    faltantes = [p for p in pasajeros_totales if p not in recogidos]

    if not faltantes:
        return Manhattan(pos_actual, destino)
    
    # El costo mínimo absoluto que le tomará al taxi es llegar al menos 
    # al pasajero que tiene más cerca.
    return min(Manhattan(pos_actual, p) for p in faltantes)
