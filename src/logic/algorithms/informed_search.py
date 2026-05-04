import heapq
from utils.heuristics import calcular_heuristica

def avara(mundo, inicio, pasajeros_totales, destino):
    h_inicial = calcular_heuristica(inicio, pasajeros_totales, [], destino)
    # cola: (prioridad_h, r, c, recogidos, camino)
    cola_prioridad = [(h_inicial, inicio[0], inicio[1], tuple(), [])]
    
    # Estructura para el árbol gráfico
    arbol_expansion = { (inicio[0], inicio[1], tuple()): {'parent': None, 'h': h_inicial} }
    nodos_expandidos = 0

    while cola_prioridad:
        h, r, c, recogidos, camino = heapq.heappop(cola_prioridad)
        estado_actual = (r, c, recogidos)
        nodos_expandidos += 1

        # Lógica de pasajeros [cite: 17, 52]
        nuevos_recogidos = list(recogidos)
        if mundo[r][c] == 4 and (r, c) not in nuevos_recogidos:
            nuevos_recogidos.append((r, c))
        recogidos_tupla = tuple(sorted(nuevos_recogidos))

        # Meta [cite: 8, 26]
        if len(recogidos_tupla) == len(pasajeros_totales) and mundo[r][c] == 5:
            return camino + [(r, c)], nodos_expandidos, arbol_expansion

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]: # [cite: 16]
            nr, nc = r + dr, c + dc
            if 0 <= nr < 10 and 0 <= nc < 10 and mundo[nr][nc] != 1: # [cite: 22]
                nuevo_estado = (nr, nc, recogidos_tupla)
                if nuevo_estado not in arbol_expansion:
                    prioridad_h = calcular_heuristica((nr, nc), pasajeros_totales, nuevos_recogidos, destino)
                    arbol_expansion[nuevo_estado] = {'parent': estado_actual, 'h': prioridad_h}
                    heapq.heappush(cola_prioridad, (prioridad_h, nr, nc, recogidos_tupla, camino + [(r, c)]))
    return None


def a_estrella(mundo, inicio, pasajeros_totales, destino):
    h_ini = calcular_heuristica(inicio, pasajeros_totales, [], destino)
    # cola: (f, g, r, c, recogidos, camino)
    cola_prioridad = [(h_ini, 0, inicio[0], inicio[1], tuple(), [])]
    
    # arbol_expansion guarda el costo real g y el padre
    arbol_expansion = { (inicio[0], inicio[1], tuple()): {'parent': None, 'g': 0, 'f': h_ini} }
    nodos_expandidos = 0

    while cola_prioridad:
        f, g, r, c, recogidos, camino = heapq.heappop(cola_prioridad)
        estado_actual = (r, c, recogidos)
        
        # Si ya encontramos un camino mejor a este estado, saltamos
        if estado_actual in arbol_expansion and arbol_expansion[estado_actual]['g'] < g:
            continue
            
        nodos_expandidos += 1

        nuevos_recogidos = list(recogidos)
        if mundo[r][c] == 4 and (r, c) not in nuevos_recogidos:
            nuevos_recogidos.append((r, c))
        recogidos_tupla = tuple(sorted(nuevos_recogidos))

        # Meta [cite: 8, 26]
        if len(recogidos_tupla) == len(pasajeros_totales) and mundo[r][c] == 5:
            return camino + [(r, c)], nodos_expandidos, g, arbol_expansion

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]: # [cite: 16]
            nr, nc = r + dr, c + dc
            if 0 <= nr < 10 and 0 <= nc < 10 and mundo[nr][nc] != 1: # [cite: 22]
                costo_paso = 7 if mundo[nr][nc] == 3 else 1 # [cite: 17, 24]
                nuevo_g = g + costo_paso
                h_n = calcular_heuristica((nr, nc), pasajeros_totales, nuevos_recogidos, destino)
                nuevo_f = nuevo_g + h_n
                
                nuevo_estado = (nr, nc, recogidos_tupla)
                if nuevo_estado not in arbol_expansion or nuevo_g < arbol_expansion[nuevo_estado]['g']:
                    arbol_expansion[nuevo_estado] = {'parent': estado_actual, 'g': nuevo_g, 'f': nuevo_f}
                    heapq.heappush(cola_prioridad, (nuevo_f, nuevo_g, nr, nc, recogidos_tupla, camino + [(r, c)]))
    return None

