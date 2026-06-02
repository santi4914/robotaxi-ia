import pygame
from typing import Dict, Any, Tuple, List

class TreeViewer:
    def __init__(self, arbol_datos: Dict[Tuple, Any], algoritmo_nombre: str, camino_solucion: List[Tuple[int, int]]):
        self.arbol_raw = arbol_datos
        self.algoritmo_nombre = algoritmo_nombre
        self.camino_solucion = set(camino_solucion)  # Para resaltar la solución en otro color
        
        # Configuración de ventana
        self.ANCHO, self.ALTO = 1200, 800
        self.COLOR_BG = (240, 240, 245)
        self.COLOR_NODO = (255, 255, 255)
        self.COLOR_NODO_SOLUCION = (76, 175, 80)  # Verde
        self.COLOR_LINEA = (150, 150, 150)
        self.COLOR_TEXTO = (33, 33, 33)
        
        # Estructura procesada para niveles
        self.niveles: Dict[int, List[Tuple]] = {}
        self.posiciones_nodos: Dict[Tuple, Tuple[int, int]] = {}
        
        self.procesar_arbol()

    def procesar_arbol(self):
        """Asigna a cada nodo un nivel (profundidad) basándose en las relaciones de parentesco."""
        # Encontrar la raíz (el nodo que no tiene padre o cuyo parent es None)
        raiz = None
        for estado, info in self.arbol_raw.items():
            if info.get('parent') is None:
                raiz = estado
                break
        
        if not raiz:
            return

        # Reconstrucción por anchura simple para calcular niveles reales
        cola = [(raiz, 0)]
        visitados_local = {raiz}
        
        # Construir relaciones de hijos
        hijos: Dict[Tuple, List[Tuple]] = {nodo: [] for nodo in self.arbol_raw}
        for estado, info in self.arbol_raw.items():
            padre = info.get('parent')
            if padre in hijos:
                hijos[padre].append(estado)
        
        while cola:
            nodo_actual, prof = cola.pop(0)
            if prof not in self.niveles:
                self.niveles[prof] = []
            self.niveles[prof].append(nodo_actual)
            
            for h in hijos.get(nodo_actual, []):
                if h not in visitados_local:
                    visitados_local.add(h)
                    cola.append((h, prof + 1))
        
        # Calcular posiciones X e Y fijas en base a la cuadrícula de niveles
        # Limitamos los niveles o nodos visuales si es extremadamente denso
        distancia_y = 90
        for nivel, nodos in self.niveles.items():
            y = 100 + nivel * distancia_y
            total_nodos = len(nodos)
            ancho_disponible = self.ANCHO - 100
            distancia_x = ancho_disponible / max(1, total_nodos + 1)
            
            for i, nodo in enumerate(nodos):
                x = 50 + int((i + 1) * distancia_x)
                self.posiciones_nodos[nodo] = (x, y)

    def mostrar_ventana(self):
        """Abre una ventana secundaria síncrona para visualizar el flujo."""
        ventana_arbol = pygame.display.set_mode((self.ANCHO, self.ALTO))
        pygame.display.set_caption(f"Árbol de Expansión - {self.algoritmo_nombre}")
        fuente_nodo = pygame.font.SysFont('arial', 11)
        fuente_titulo = pygame.font.SysFont('arial', 20, bold=True)
        
        reloj = pygame.font.get_default_font() # Placeholder
        reloj_interno = pygame.time.Clock()
        
        viendo_arbol = True
        offset_x, offset_y = 0, 0
        arrastrando = False
        pos_inicio_arrastre = (0, 0)

        while viendo_arbol:
            ventana_arbol.fill(self.COLOR_BG)
            pos_raton = pygame.mouse.get_pos()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    viendo_arbol = False
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:  # Cerrar con ESC
                        viendo_arbol = False
                # Permitir arrastrar el árbol si es muy grande (Pan)
                elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    arrastrando = True
                    pos_inicio_arrastre = evento.pos
                elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
                    arrastrando = False
                elif evento.type == pygame.MOUSEMOTION and arrastrando:
                    dx = evento.pos[0] - pos_inicio_arrastre[0]
                    dy = evento.pos[1] - pos_inicio_arrastre[1]
                    offset_x += dx
                    offset_y += dy
                    pos_inicio_arrastre = evento.pos

            # 1. Dibujar conexiones (Aristas/Flechas) primero para que queden detrás
            for estado, info in self.arbol_raw.items():
                padre = info.get('parent')
                # Mapeo especial para unificar el formato de tuplas de padres de los informados vs no informados
                if padre and len(padre) == 2:  # Si guardó solo (r, c) aproximamos al estado padre
                    padre = next((k for k in self.posiciones_nodos if k[0] == padre[0] and k[1] == padre[1]), None)
                
                if padre in self.posiciones_nodos and estado in self.posiciones_nodos:
                    p_x, p_y = self.posiciones_nodos[padre]
                    h_x, h_y = self.posiciones_nodos[estado]
                    pygame.draw.line(ventana_arbol, self.COLOR_LINEA, 
                                     (p_x + offset_x, p_y + offset_y), 
                                     (h_x + offset_x, h_y + offset_y), 2)

            # 2. Dibujar nodos
            for estado, pos in self.posiciones_nodos.items():
                x, y = pos[0] + offset_x, pos[1] + offset_y
                
                # Determinar color: ¿Es parte de la solución final?
                es_solucion = (estado[0], estado[1]) in self.camino_solucion
                color = self.COLOR_NODO_SOLUCION if es_solucion else self.COLOR_NODO
                
                pygame.draw.circle(ventana_arbol, color, (x, y), 18)
                pygame.draw.circle(ventana_arbol, self.COLOR_TEXTO, (x, y), 18, 1) # Borde
                
                # Texto descriptivo dentro del nodo: Coordenada (F, C)
                lbl = f"{estado[0]},{estado[1]}"
                txt_surf = fuente_nodo.render(lbl, True, self.COLOR_TEXTO if not es_solucion else (255,255,255))
                ventana_arbol.blit(txt_surf, txt_surf.get_rect(center=(x, y)))

            # Título e instrucciones fijas en pantalla
            tit = fuente_titulo.render(f"Flujo del espacio de estados: {self.algoritmo_nombre}", True, self.COLOR_TEXTO)
            ventana_arbol.blit(tit, (20, 20))
            instrucciones = fuente_nodo.render("Arrastra con el clic izquierdo para mover el árbol. Presiona ESC para volver.", True, (100,100,100))
            ventana_arbol.blit(instrucciones, (20, 50))

            pygame.display.flip()
            reloj_interno.tick(60)