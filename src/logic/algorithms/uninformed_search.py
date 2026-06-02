import heapq
from collections import deque

import heapq
from collections import deque

def amplitud(mundo, inicio, pasajeros_totales, destino):
    estado_inicial = (inicio[0], inicio[1], tuple())
    # cola: (estado_actual, camino)
    cola = deque([(estado_inicial, [])])
    visitados = {estado_inicial: {'parent': None, 'cost': 0}}
    nodos_expandidos = 0

    while cola:
        (r, c, recogidos), camino = cola.popleft()
        nodos_expandidos += 1
        
        # Lógica de pasajeros [cite: 17, 19]
        nuevos_recogidos = list(recogidos)
        if mundo[r][c] == 4 and (r, c) not in nuevos_recogidos:
            nuevos_recogidos.append((r, c))
        recogidos_tupla = tuple(sorted(nuevos_recogidos))
        estado_actual = (r, c, recogidos_tupla)

        # Meta: Todos recogidos y en destino (5) [cite: 7, 26]
        if len(recogidos_tupla) == len(pasajeros_totales) and mundo[r][c] == 5:
            return camino + [(r, c)], nodos_expandidos, visitados, None

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]: # [cite: 16]
            nr, nc = r + dr, c + dc
            if 0 <= nr < 10 and 0 <= nc < 10 and mundo[nr][nc] != 1: # [cite: 22]
                nuevo_estado = (nr, nc, recogidos_tupla)
                if nuevo_estado not in visitados:
                    # Guardamos la relación para el árbol gráfico
                    visitados[nuevo_estado] = {'parent': (r, c, recogidos), 'cost': len(camino) + 1}
                    cola.append((nuevo_estado, camino + [(r, c)]))
    return None

def costo_uniforme(mundo, inicio, pasajeros_totales, destino):
    estado_inicial = (inicio[0], inicio[1], tuple())
    # heap: (g, r, c, recogidos, camino)
    cola_prioridad = [(0, inicio[0], inicio[1], tuple(), [])]
    # visitados guarda el costo y el padre para el gráfico
    visitados = {estado_inicial: {'parent': None, 'cost': 0}}
    nodos_expandidos = 0

    while cola_prioridad:
        g, r, c, recogidos, camino = heapq.heappop(cola_prioridad)
        estado_actual = (r, c, recogidos)
        nodos_expandidos += 1

        nuevos_recogidos = list(recogidos)
        if mundo[r][c] == 4 and (r, c) not in nuevos_recogidos:
            nuevos_recogidos.append((r, c))
        recogidos_tupla = tuple(sorted(nuevos_recogidos))

        if len(recogidos_tupla) == len(pasajeros_totales) and mundo[r][c] == 5:
            return camino + [(r, c)], nodos_expandidos, visitados, g

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]: # [cite: 16]
            nr, nc = r + dr, c + dc
            if 0 <= nr < 10 and 0 <= nc < 10 and mundo[nr][nc] != 1: # [cite: 22]
                costo_mov = 7 if mundo[nr][nc] == 3 else 1 # [cite: 17, 24]
                nuevo_g = g + costo_mov
                nuevo_estado = (nr, nc, recogidos_tupla)
                
                if nuevo_estado not in visitados or nuevo_g < visitados[nuevo_estado]['cost']:
                    visitados[nuevo_estado] = {'parent': estado_actual, 'cost': nuevo_g}
                    heapq.heappush(cola_prioridad, (nuevo_g, nr, nc, recogidos_tupla, camino + [(r, c)]))
    return None


def profundidad_evitando_ciclos(mundo, inicio, pasajeros_totales, destino):
    # Estado inicial: (fila, columna, tupla_pasajeros_recogidos)
    estado_inicial = (inicio[0], inicio[1], tuple())
    
    # La pila almacena: (estado_actual, camino_recorrido)
    pila = [(estado_inicial, [])]
    
    # visitados ahora es un diccionario para construir el árbol gráfico
    # Almacena: { estado_hijo: {'parent': estado_padre, 'cost': pasos} }
    visitados = {estado_inicial: {'parent': None, 'cost': 0}}
    nodos_expandidos = 0

    while pila:
        (r, c, recogidos), camino = pila.pop() # LIFO [cite: 16]
        nodos_expandidos += 1

        # 1. Verificar si hay un pasajero en la celda actual [cite: 17]
        nuevos_recogidos = list(recogidos)
        if mundo[r][c] == 4 and (r, c) not in nuevos_recogidos:
            nuevos_recogidos.append((r, c))
        
        recogidos_tupla = tuple(sorted(nuevos_recogidos))
        estado_actual = (r, c, recogidos_tupla)

        # 2. Condición de meta: pasajeros completos y posición en destino (valor 5) [cite: 26, 52]
        if len(recogidos_tupla) == len(pasajeros_totales) and mundo[r][c] == 5:
            return camino + [(r, c)], nodos_expandidos, visitados, None

        # 3. Explorar sucesores (Arriba, Abajo, Izquierda, Derecha) [cite: 16]
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            
            # Validar límites y evitar muros (valor 1) [cite: 22]
            if 0 <= nr < 10 and 0 <= nc < 10 and mundo[nr][nc] != 1:
                nuevo_estado = (nr, nc, recogidos_tupla)
                
                if nuevo_estado not in visitados:
                    # Registramos el nodo en el árbol de expansión
                    visitados[nuevo_estado] = {
                        'parent': (r, c, recogidos), 
                        'cost': len(camino) + 1
                    }
                    pila.append((nuevo_estado, camino + [(r, c)]))
                    
    return None
