def Manhattan(pos1, pos2):
    """Calcula la distancia de Manhattan entre dos puntos (r1, c1) y (r2, c2)."""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def calcular_heuristica(pos_actual, pasajeros_totales, recogidos, destino):
    """
    pos_actual: (r, c)
    pasajeros_totales: lista de coordenadas de todos los pasajeros [(r,c), (r,c)...]
    recogidos: lista o tupla de coordenadas de pasajeros ya en el taxi
    destino: (r, c)
    """
    # Identificar pasajeros que faltan por recoger
    faltantes = [p for p in pasajeros_totales if p not in recogidos]

    if not faltantes:
        # Ya tiene a todos, solo importa la distancia al destino
        return Manhattan(pos_actual, destino)
    
    # Heurística para múltiples objetivos:
    # Tomamos el máximo de (distancia al pasajero + distancia de ese pasajero al destino)
    # Esto asegura que sea admisible y más informada que solo el más cercano.
    return max(Manhattan(pos_actual, p) + Manhattan(p, destino) for p in faltantes)
