import pygame
from typing import List, Tuple, Dict, Optional, Set

# --- CONSTANTES DE DISEÑO (MATERIAL DESIGN) ---
COLOR_BG = (245, 245, 245)          # Fondo general (Gris muy claro)
COLOR_GRID_BG = (255, 255, 255)     # Fondo de la grilla (Blanco)
COLOR_WALL = (74, 74, 74)           # Muro 1 (Gris oscuro)
COLOR_TRAFFIC = (255, 138, 128)     # Tráfico Alto 3 (Rojo suave)
COLOR_DEST = (129, 199, 132)        # Destino 5 (Verde suave)
COLOR_TAXI = (253, 216, 53)         # Taxi 2 (Amarillo)
COLOR_PASSENGER = (186, 104, 200)   # Pasajero 4 (Púrpura suave)
COLOR_LINE = (224, 224, 224)        # Líneas de la grilla
COLOR_TEXT = (33, 33, 33)           # Texto principal
COLOR_BTN_IDLE = (33, 150, 243)     # Botón normal (Azul)
COLOR_BTN_HOVER = (30, 136, 229)    # Botón hover
COLOR_BTN_TEXT = (255, 255, 255)    # Texto botón

class BotonUI:
    """Clase auxiliar para manejar botones interactivos en la interfaz."""
    def __init__(self, x: int, y: int, width: int, height: int, text: str, font: pygame.font.Font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.is_hovered = False

    def dibujar(self, surface: pygame.Surface):
        color = COLOR_BTN_HOVER if self.is_hovered else COLOR_BTN_IDLE
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        
        text_surf = self.font.render(self.text, True, COLOR_BTN_TEXT)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def chequear_hover(self, pos_raton: Tuple[int, int]):
        self.is_hovered = self.rect.collidepoint(pos_raton)


class Renderer:
    """
    Motor gráfico encargado de renderizar la simulación del Robotaxi Zoox.
    Maneja el dibujo de la grilla, UI y las interpolaciones matemáticas para la animación.
    """
    def __init__(self, ancho: int, alto: int, tamano_celda: int = 60):
        pygame.init()
        self.pantalla = pygame.display.set_mode((ancho, alto))
        pygame.display.set_caption("Robotaxi Zoox - Simulador IA")
        
        # Fuentes (Tipografías limpias sin serifa)
        self.fuente_titulo = pygame.font.SysFont('segoeui, roboto, arial', 28, bold=True)
        self.fuente_texto = pygame.font.SysFont('segoeui, roboto, arial', 20)
        self.fuente_boton = pygame.font.SysFont('segoeui, roboto, arial', 18, bold=True)
        self.fuente_celda = pygame.font.SysFont('segoeui, roboto, arial', 14)

        # Configuraciones de diseño
        self.tamano_celda = tamano_celda
        self.offset_x = 50
        self.offset_y = 80
        self.ancho_panel = 350
        
        # Estado de la Simulación
        self.matriz: List[List[int]] = []
        self.camino: List[Tuple[int, int]] = []
        self.pasajeros_iniciales: Set[Tuple[int, int]] = set()
        self.pasajeros_recogidos: Set[Tuple[int, int]] = set()
        
        # Variables para la interpolación (lerp) de la animación
        self.animando = False
        self.paso_actual = 0
        self.progreso_animacion = 0.0
        self.velocidad_animacion = 3.0  # Celdas por segundo
        self.pos_taxi_visual: Tuple[float, float] = (0.0, 0.0)

        # Botones del Panel
        btn_x = ancho - self.ancho_panel + 25
        self.boton_algoritmo = BotonUI(btn_x, 150, 300, 45, "Algoritmo: Amplitud", self.fuente_boton)
        self.boton_iniciar = BotonUI(btn_x, 210, 300, 45, "Iniciar Simulación", self.fuente_boton)
        self.boton_reset = BotonUI(btn_x, 270, 300, 45, "Resetear Mapa", self.fuente_boton)
        self.botones = [self.boton_algoritmo, self.boton_iniciar, self.boton_reset]

    def cargar_mundo(self, matriz: List[List[int]]):
        """Carga la matriz inicial y extrae pasajeros y el inicio para resetear la vista."""
        self.matriz = matriz
        self.camino = []
        self.animando = False
        self.pasajeros_iniciales.clear()
        self.pasajeros_recogidos.clear()
        
        for r in range(10):
            for c in range(10):
                if matriz[r][c] == 2:
                    self.pos_taxi_visual = (r, c)
                elif matriz[r][c] == 4:
                    self.pasajeros_iniciales.add((r, c))

    def iniciar_animacion(self, camino: List[Tuple[int, int]]):
        """Inicia la secuencia de animación pasándole el camino resuelto por la IA."""
        if not camino:
            return
        self.camino = camino
        self.paso_actual = 0
        self.progreso_animacion = 0.0
        self.pasajeros_recogidos.clear()
        self.pos_taxi_visual = (self.camino[0][0], self.camino[0][1])
        self.animando = True

    def actualizar(self, delta_tiempo: float):
        """Lógica matemática de actualización de frames (independiente del framerate)."""
        if self.animando and self.paso_actual < len(self.camino) - 1:
            self.progreso_animacion += delta_tiempo * self.velocidad_animacion
            
            # Si el progreso supera 1.0, el taxi llegó a la siguiente celda
            if self.progreso_animacion >= 1.0:
                self.progreso_animacion = 0.0
                self.paso_actual += 1
                
                # Checkear si recoge pasajero
                pos_actual = self.camino[self.paso_actual]
                if pos_actual in self.pasajeros_iniciales and pos_actual not in self.pasajeros_recogidos:
                    self.pasajeros_recogidos.add(pos_actual)
                
                if self.paso_actual >= len(self.camino) - 1:
                    self.animando = False
                    return

            # Interpolación lineal (lerp) para suavizar movimiento
            p1 = self.camino[self.paso_actual]
            p2 = self.camino[self.paso_actual + 1]
            r_visual = p1[0] + (p2[0] - p1[0]) * self.progreso_animacion
            c_visual = p1[1] + (p2[1] - p1[1]) * self.progreso_animacion
            self.pos_taxi_visual = (r_visual, c_visual)

    def manejar_eventos_ui(self, pos_raton: Tuple[int, int], click: bool) -> Optional[str]:
        """Maneja el hover y click de los botones de la interfaz."""
        for btn in self.botones:
            btn.chequear_hover(pos_raton)
            if click and btn.is_hovered:
                if btn == self.boton_algoritmo: return "CAMBIAR_ALGORITMO"
                if btn == self.boton_iniciar: return "INICIAR"
                if btn == self.boton_reset: return "RESET"
        return None

    def actualizar_texto_algoritmo(self, nombre: str):
        self.boton_algoritmo.text = f"Algoritmo: {nombre}"

    def dibujar(self, reportes: Dict[str, str]):
        """Renderiza todo el pipeline gráfico frame por frame."""
        self.pantalla.fill(COLOR_BG)
        self._dibujar_grilla()
        self._dibujar_panel_lateral(reportes)
        pygame.display.flip()

    def _dibujar_grilla(self):
        """Renderiza las celdas del mundo, con bordes redondeados para estética moderna."""
        if not self.matriz: return

        for r in range(10):
            for c in range(10):
                x = self.offset_x + c * self.tamano_celda
                y = self.offset_y + r * self.tamano_celda
                rect = pygame.Rect(x, y, self.tamano_celda - 2, self.tamano_celda - 2) # Margen de 2px
                
                valor = self.matriz[r][c]
                color = COLOR_GRID_BG
                
                if valor == 1: color = COLOR_WALL
                elif valor == 3: color = COLOR_TRAFFIC
                elif valor == 5: color = COLOR_DEST
                
                # Dibujar fondo de celda
                pygame.draw.rect(self.pantalla, color, rect, border_radius=6)
                
                # Dibujar pasajero si existe y no ha sido recogido
                if (r, c) in self.pasajeros_iniciales and (r, c) not in self.pasajeros_recogidos:
                    pygame.draw.circle(self.pantalla, COLOR_PASSENGER, rect.center, self.tamano_celda // 3)
                    # Dibujar una letra 'P' adentro para claridad visual (opcional)
                    txt = self.fuente_celda.render("P", True, (255,255,255))
                    self.pantalla.blit(txt, txt.get_rect(center=rect.center))

        # Dibujar Taxi (entidad dinámica)
        taxi_x = self.offset_x + self.pos_taxi_visual[1] * self.tamano_celda
        taxi_y = self.offset_y + self.pos_taxi_visual[0] * self.tamano_celda
        taxi_rect = pygame.Rect(int(taxi_x) + 4, int(taxi_y) + 4, self.tamano_celda - 10, self.tamano_celda - 10)
        pygame.draw.rect(self.pantalla, COLOR_TAXI, taxi_rect, border_radius=10)
        # Ícono T
        txt = self.fuente_boton.render("T", True, COLOR_TEXT)
        self.pantalla.blit(txt, txt.get_rect(center=taxi_rect.center))

    def _dibujar_panel_lateral(self, reportes: Dict[str, str]):
        """Renderiza el panel lateral a la derecha."""
        ancho = self.pantalla.get_width()
        alto = self.pantalla.get_height()
        panel_rect = pygame.Rect(ancho - self.ancho_panel, 0, self.ancho_panel, alto)
        
        # Fondo panel con sombra simulada mediante borde gris suave
        pygame.draw.rect(self.pantalla, (250, 250, 250), panel_rect)
        pygame.draw.line(self.pantalla, (200, 200, 200), (panel_rect.left, 0), (panel_rect.left, alto), 2)

        # Título
        tit = self.fuente_titulo.render("Panel de Control", True, COLOR_TEXT)
        self.pantalla.blit(tit, (panel_rect.left + 25, 40))

        # Botones
        for btn in self.botones:
            btn.dibujar(self.pantalla)

        # Título Reportes
        rep_tit = self.fuente_titulo.render("Reporte de Ejecución", True, COLOR_TEXT)
        self.pantalla.blit(rep_tit, (panel_rect.left + 25, 360))

        # Datos de Reportes (Iteración dinámica)
        y_offset = 420
        for clave, valor in reportes.items():
            txt = self.fuente_texto.render(f"{clave}: {valor}", True, COLOR_TEXT)
            self.pantalla.blit(txt, (panel_rect.left + 25, y_offset))
            y_offset += 30

        # Espacio final del panel (puede usarse para indicadores adicionales)