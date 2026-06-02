import pygame
from typing import List, Tuple, Dict, Optional, Set

from pygame import surface

# --- CONSTANTES DE DISEÑO (MATERIAL DESIGN) ---
COLOR_BG = (245, 245, 245)          # Fondo general (Gris muy claro)
COLOR_PRIMARY = (33, 150, 243)      # Azul primario
COLOR_ERROR = (244, 67, 54)         # Rojo para errores
COLOR_SUCCESS = (76, 175, 80)       # Verde para éxito
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
COLOR_BTN_GREEN = (76, 175, 80)
COLOR_BTN_GREEN_HOVER = (67, 160, 71)

class BotonUI:
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        text: str,
        font: pygame.font.Font,
        color_idle=COLOR_BTN_IDLE,
        color_hover=COLOR_BTN_HOVER
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.is_hovered = False

        self.color_idle = color_idle
        self.color_hover = color_hover
   
    def dibujar(self, surface: pygame.Surface):
        color = self.color_hover if self.is_hovered else self.color_idle

        pygame.draw.rect(surface, color, self.rect, border_radius=8)

        text_surf = self.font.render(self.text, True, COLOR_BTN_TEXT)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)


    def chequear_hover(self, pos_raton: Tuple[int, int]):
        self.is_hovered = self.rect.collidepoint(pos_raton)


class SelectorAlgoritmo:
    """Selector jerárquico de algoritmos: Tipo → Algoritmo específico."""
    
    def __init__(self, x: int, y: int, width: int, font_boton, font_pequena):
        self.x = x
        self.y = y
        self.width = width
        self.font_boton = font_boton
        self.font_pequena = font_pequena
        
        # Estados
        self.tipo_seleccionado: Optional[str] = None  # "Informada" o "No Informada"
        self.algoritmo_seleccionado: Optional[str] = None
        
        # Opciones
        self.tipos = ["Búsqueda Informada", "Búsqueda No Informada"]
        self.algoritmos_informados = ["Avara", "A*"]
        self.algoritmos_no_informados = ["Amplitud", "Costo Uniforme", "Profundidad"]
        
        # Estados de UI
        self.mostrando_tipos = False
        self.mostrando_algoritmos = False
        self.mensaje_error: Optional[str] = None
        
        # Botones
        self.boton_tipo = BotonUI(x, y, width, 45, "Elegir tipo...", font_boton)
        self.boton_algoritmo = BotonUI(x, y + 65, width, 45, "Elegir algoritmo...", font_boton)
    
    def manejar_eventos(self, pos_raton: Tuple[int, int], click: bool) -> Optional[str]:
        """Retorna una acción o None."""
        self.boton_tipo.chequear_hover(pos_raton)
        self.boton_algoritmo.chequear_hover(pos_raton)
        
        if not click:
            return None
        
        # Click en botón tipo
        if self.boton_tipo.is_hovered:
            self.mostrando_tipos = not self.mostrando_tipos
            self.mostrando_algoritmos = False
            return None
        
        # En manejar_eventos de SelectorAlgoritmo:
        # Si "mostrando_tipos" es True, ignora por completo cualquier interacción con el botón de algoritmo inferior
        if self.mostrando_tipos:
            for i, tipo in enumerate(self.tipos):
                item_rect = pygame.Rect(self.x, self.y + 50 + 5 + i * 40, self.width, 35)
                if item_rect.collidepoint(pos_raton):
                    self.tipo_seleccionado = tipo
                    self.algoritmo_seleccionado = None
                    self.mostrando_tipos = False
                    self._actualizar_boton_tipo()
                    self._actualizar_boton_algoritmo()
                    return None
            return None # Evita que el clic pase a los componentes de abajo mientras la lista está abierta

        # Click en botón algoritmo
        if self.boton_algoritmo.is_hovered:
            if not self.tipo_seleccionado:
                self.mensaje_error = "Debes elegir un tipo de algoritmo primero"
                self.mostrando_algoritmos = False
            else:
                self.mostrando_algoritmos = not self.mostrando_algoritmos
                self.mensaje_error = None
            return None
        
        # Click en items de algoritmo
        if self.mostrando_algoritmos:
            algoritmos = self.algoritmos_informados if self.tipo_seleccionado == "Búsqueda Informada" else self.algoritmos_no_informados
            for i, algo in enumerate(algoritmos):
                item_rect = pygame.Rect(self.x, self.y + 130 + 5 + i * 40, self.width, 35)
                if item_rect.collidepoint(pos_raton):
                    self.algoritmo_seleccionado = algo
                    self.mostrando_algoritmos = False
                    self.mensaje_error = None
                    self._actualizar_boton_algoritmo()
                    return None
        
        return None
    
    def _actualizar_boton_tipo(self):
        """Actualiza el texto del botón tipo."""
        if self.tipo_seleccionado:
            self.boton_tipo.text = self.tipo_seleccionado
        else:
            self.boton_tipo.text = "Elegir tipo..."
    
    def _actualizar_boton_algoritmo(self):
        """Actualiza el texto del botón algoritmo."""
        if self.algoritmo_seleccionado:
            self.boton_algoritmo.text = self.algoritmo_seleccionado
        else:
            self.boton_algoritmo.text = "Elegir algoritmo..."
    
    def obtener_algoritmo(self) -> Optional[str]:
        """Retorna el algoritmo seleccionado o muestra error."""
        if not self.tipo_seleccionado:
            self.mensaje_error = "Debes elegir un tipo de algoritmo"
            return None
        if not self.algoritmo_seleccionado:
            self.mensaje_error = "Debes elegir un algoritmo"
            return None
        return self.algoritmo_seleccionado
    
    def dibujar(self, surface: pygame.Surface):
        """Dibuja el selector y sus opciones de manera fluida."""
        # 1. Siempre dibujamos el botón del tipo de algoritmo
        self.boton_tipo.dibujar(surface)
        
        # 2. Solo si NO estamos desplegando los tipos, mostramos el botón de algoritmo específico
        if not self.mostrando_tipos:
            if not self.tipo_seleccionado:
                # Botón deshabilitado si no hay tipo seleccionado
                pygame.draw.rect(surface, (200, 200, 200), self.boton_algoritmo.rect, border_radius=8)
                txt = self.font_boton.render(self.boton_algoritmo.text, True, (100, 100, 100))
                txt_rect = txt.get_rect(center=self.boton_algoritmo.rect.center)
                surface.blit(txt, txt_rect)
            else:
                self.boton_algoritmo.dibujar(surface)
                
            # Lista de algoritmos específicos (se dibuja encima de todo si está abierta)
            if self.mostrando_algoritmos:
                algoritmos = self.algoritmos_informados if self.tipo_seleccionado == "Búsqueda Informada" else self.algoritmos_no_informados
                self._dibujar_lista(surface, algoritmos, self.y + 130)
        else:
            # Lista de tipos (se dibuja si está abierta, ocultando limpiamente lo que estaría abajo)
            self._dibujar_lista(surface, self.tipos, self.y + 50)
        
        # 3. Mostrar error si existe
        if self.mensaje_error:
            error_txt = self.font_pequena.render(self.mensaje_error, True, COLOR_ERROR)
            error_bg = pygame.Rect(self.x, self.y + 120, self.width, 30) # Ajustado el Y para que no choque
            pygame.draw.rect(surface, (255, 240, 240), error_bg, border_radius=4)
            surface.blit(error_txt, (error_bg.left + 10, error_bg.top + 7))
    
    def _dibujar_lista(self, surface: pygame.Surface, items: List[str], y_inicio: int):
        """Dibuja una lista desplegable de opciones."""
        # Altura dinámica según cantidad de items (máximo 4 visible)
        max_visible = 4
        items_a_mostrar = items[:max_visible]
        altura_lista = len(items_a_mostrar) * 40 + 10
        
        lista_rect = pygame.Rect(self.x - 5, y_inicio, self.width + 10, altura_lista)
        pygame.draw.rect(surface, (255, 255, 255), lista_rect, border_radius=6)
        pygame.draw.rect(surface, COLOR_PRIMARY, lista_rect, 2, border_radius=6)
        
        # Items
        for i, item in enumerate(items_a_mostrar):
            item_y = y_inicio + 5 + i * 40
            item_rect = pygame.Rect(self.x, item_y, self.width, 35)
            
            # Hover effect
            if item_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(surface, (220, 240, 255), item_rect, border_radius=3)
            
            # Renderizar texto truncado si es necesario
            item_txt = self.font_pequena.render(item, True, COLOR_TEXT)
            surface.blit(item_txt, (item_rect.left + 12, item_rect.top + 8))


class WelcomeScreen:
    """Pantalla de bienvenida para selección de mapas con validación."""
    
    def __init__(self, ancho: int, alto: int):
        self.ancho = ancho
        self.alto = alto
        self.mapas_disponibles: List[str] = []
        self.mapa_seleccionado: Optional[str] = None
        self.error_mensaje: Optional[str] = None
        self.mostrando_lista = False
        self.scroll_offset = 0
        
        # Cargar imagen de fondo
        try:
            import os
            ruta_imagen = os.path.join(os.path.dirname(__file__), '../../public/robotaxi.jpg')
            self.imagen_fondo = pygame.image.load(ruta_imagen)
            self.imagen_fondo = pygame.transform.scale(self.imagen_fondo, (ancho, alto))
        except Exception as e:
            print(f"Advertencia: No se pudo cargar la imagen de fondo: {e}")
            self.imagen_fondo = None
        
        # Fuentes
        self.fuente_titulo = pygame.font.SysFont('segoeui, roboto, arial', 42, bold=True)
        self.fuente_subtitulo = pygame.font.SysFont('segoeui, roboto, arial', 24)
        self.fuente_texto = pygame.font.SysFont('segoeui, roboto, arial', 18)
        self.fuente_pequena = pygame.font.SysFont('segoeui, roboto, arial', 14)
        
        # Botones
        self.boton_elegir = BotonUI(
            ancho // 2 - 150,
            alto // 2 + 100,
            300,
            50,
            "Elegir Mapa",
            self.fuente_subtitulo
        )

        self.boton_continuar = BotonUI(
            ancho // 2 - 150,
            alto // 2 + 170,
            300,
            50,
            "Continuar",
            self.fuente_subtitulo,
            COLOR_BTN_GREEN,
            COLOR_BTN_GREEN_HOVER
        )   
        self.botones = [self.boton_elegir, self.boton_continuar]
    
    def set_mapas_disponibles(self, mapas: List[str]):
        """Establece la lista de mapas disponibles."""
        self.mapas_disponibles = sorted(mapas)
    
    def validar_mapa(self, validate_func) -> bool:
        """Valida el mapa seleccionado usando la función de validación."""
        if not self.mapa_seleccionado:
            self.error_mensaje = "Debes seleccionar un mapa primero"
            return False
        
        try:
            validate_func(self.mapa_seleccionado)
            self.error_mensaje = None
            return True
        except Exception as e:
            self.error_mensaje = f"Error: {str(e)}"
            return False
    
    def manejar_eventos(self, pos_raton: Tuple[int, int], click: bool) -> Optional[str]:
        """Retorna una acción basada en los eventos del usuario."""
        for btn in self.botones:
            btn.chequear_hover(pos_raton)
        
        if not click:
            return None
        
        # Click en botón Elegir Mapa
        if self.boton_elegir.is_hovered:
            self.mostrando_lista = not self.mostrando_lista
            return None
        
        # Click en elemento de lista
        if self.mostrando_lista:
            lista_y = self.alto // 2 - 100
            for i, mapa in enumerate(self.mapas_disponibles):
                mapa_rect = pygame.Rect(self.ancho // 2 - 150, lista_y + i * 35, 300, 30)
                if mapa_rect.collidepoint(pos_raton):
                    self.mapa_seleccionado = mapa
                    self.mostrando_lista = False
                    self.error_mensaje = None
                    return None
        
        # Click en botón Continuar
        if self.boton_continuar.is_hovered:
            if self.mapa_seleccionado:
                return "CONTINUAR"
            else:
                self.error_mensaje = "Debes seleccionar un mapa para continuar"
        
        return None
    
    def dibujar(self, surface: pygame.Surface):
        """Renderiza la pantalla de bienvenida."""
        # Dibujar fondo
        if self.imagen_fondo:
            surface.blit(self.imagen_fondo, (0, 0))
        else:
            surface.fill(COLOR_BG)
        
        # Overlay semi-transparente oscuro para mejorar legibilidad
        overlay = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))  # Negro con 120 de opacidad (0-255)
        surface.blit(overlay, (0, 0))
        
        # Título
        titulo = self.fuente_titulo.render("Robotaxi Zoox", True, (255, 255, 255))
        surface.blit(titulo, (self.ancho // 2 - titulo.get_width() // 2, 80))
        
        # Subtítulo
        subtitulo = self.fuente_subtitulo.render("Selecciona un mapa para comenzar", True, (255, 255, 255))
        surface.blit(subtitulo, (self.ancho // 2 - subtitulo.get_width() // 2, 160))
        
        # Mapa seleccionado
        if self.mapa_seleccionado:
            mapa_txt = self.fuente_texto.render(f"Mapa: {self.mapa_seleccionado}", True, (76, 175, 80))
        else:
            mapa_txt = self.fuente_texto.render("Mapa: No seleccionado", True, (200, 200, 200))
        surface.blit(mapa_txt, (self.ancho // 2 - mapa_txt.get_width() // 2, self.alto // 2 - 20))
        
        # Botón Elegir
        self.boton_elegir.dibujar(surface)
        
        # Lista de mapas (si está abierta)
        if self.mostrando_lista and self.mapas_disponibles:
            self._dibujar_lista_mapas(surface)
        
        # Botón Continuar (deshabilitado si no hay mapa)
        if not self.mapa_seleccionado:
            pygame.draw.rect(surface, (200, 200, 200), self.boton_continuar.rect, border_radius=8)
            txt = self.boton_continuar.font.render(self.boton_continuar.text, True, (100, 100, 100))
        else:
            self.boton_continuar.dibujar(surface)
        
        # Mostrar error si existe
        if self.error_mensaje:
            error_txt = self.fuente_pequena.render(self.error_mensaje, True, COLOR_ERROR)
            error_bg = pygame.Rect(self.ancho // 2 - error_txt.get_width() // 2 - 15, 
                                   self.alto - 80, error_txt.get_width() + 30, 40)
            pygame.draw.rect(surface, (255, 240, 240), error_bg, border_radius=6)
            pygame.draw.rect(surface, COLOR_ERROR, error_bg, 2, border_radius=6)
            surface.blit(error_txt, (error_bg.left + 15, error_bg.top + 10))
        
        pygame.display.flip()
    
    def _dibujar_lista_mapas(self, surface: pygame.Surface):
        """Dibuja la lista desplegable de mapas disponibles."""
        lista_y = self.alto // 2 - 100
        max_visible = 5
        mapas_a_mostrar = self.mapas_disponibles[self.scroll_offset:self.scroll_offset + max_visible]
        
        # Fondo de lista
        lista_rect = pygame.Rect(self.ancho // 2 - 160, lista_y - 10, 320, len(mapas_a_mostrar) * 35 + 20)
        pygame.draw.rect(surface, (255, 255, 255), lista_rect, border_radius=8)
        pygame.draw.rect(surface, COLOR_PRIMARY, lista_rect, 2, border_radius=8)
        
        # Items
        for i, mapa in enumerate(mapas_a_mostrar):
            item_y = lista_y + i * 35
            item_rect = pygame.Rect(self.ancho // 2 - 150, item_y, 300, 30)
            
            # Hover effect
            if item_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(surface, (220, 240, 255), item_rect)
            
            mapa_txt = self.fuente_pequena.render(mapa, True, COLOR_TEXT)
            surface.blit(mapa_txt, (item_rect.left + 15, item_rect.top + 7))


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
        self.ancho_panel = 480
        
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

        # --- CÓDIGO MODIFICADO CON NUEVAS POSICIONES Y ---
        btn_x = ancho - self.ancho_panel + 25
        
        # El selector se queda en su lugar (y = 140)
        self.selector_algoritmo = SelectorAlgoritmo(btn_x, 140, 300, self.fuente_boton, self.fuente_texto)
        
        # Botones al lado derecho del selector
        # Iniciar Simulación al lado del botón "Elegir tipo" (y=140)
        self.boton_iniciar = BotonUI(btn_x + 310, 140, 120, 45, "Iniciar", self.fuente_boton)
        
        # Resetear Mapa al lado del botón "Elegir algoritmo" (y=205)
        self.boton_reset = BotonUI(btn_x + 310, 205, 120, 45, "Resetear", self.fuente_boton)
        
        self.botones = [self.boton_iniciar, self.boton_reset]
        self.boton_ver_arbol = BotonUI(btn_x, alto - 65, 300, 45, "Mostrar árbol de búsqueda", self.fuente_boton)
        self.botones.append(self.boton_ver_arbol) # Lo sumamos a la lista de eventos genéricos
        self.arbol_disponible = False # Flag de control

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
        self.selector_algoritmo.manejar_eventos(pos_raton, click)
        
        for btn in self.botones:
            btn.chequear_hover(pos_raton)
            if click and btn.is_hovered:
                if btn == self.boton_iniciar:
                    if not self.selector_algoritmo.obtener_algoritmo():
                        return None
                    return "INICIAR"
                if btn == self.boton_reset: 
                    self.arbol_disponible = False # Bloquear árbol al resetear
                    return "RESET"
                if btn == self.boton_ver_arbol:
                    if self.arbol_disponible:
                        return "VER_ARBOL"
        return None
    
    def obtener_algoritmo_seleccionado(self) -> Optional[str]:
        """Retorna el algoritmo seleccionado o None."""
        return self.selector_algoritmo.algoritmo_seleccionado
    
    def limpiar_selector_algoritmo(self):
        """Limpia la selección de algoritmo para una nueva simulación."""
        self.selector_algoritmo.tipo_seleccionado = None
        self.selector_algoritmo.algoritmo_seleccionado = None
        self.selector_algoritmo.mensaje_error = None
        self.selector_algoritmo._actualizar_boton_tipo()
        self.selector_algoritmo._actualizar_boton_algoritmo()

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
        
        # 1. Fondo panel
        pygame.draw.rect(self.pantalla, (250, 250, 250), panel_rect)
        pygame.draw.line(self.pantalla, (200, 200, 200), (panel_rect.left, 0), (panel_rect.left, alto), 2)

        # 2. Título principal
        tit = self.fuente_titulo.render("Panel de Control", True, COLOR_TEXT)
        self.pantalla.blit(tit, (panel_rect.left + 25, 40))

        # 3. Dibujar Botones normales (Iniciar y Reset)
        # Evitamos dibujar el botón del árbol aquí de forma automática para controlarlo abajo
        for btn in self.botones:
            if btn != self.boton_ver_arbol:
                btn.dibujar(self.pantalla)

        # 4. Título Reportes y Datos de Reportes (Sin duplicados)
        rep_tit = self.fuente_titulo.render("Reporte de Ejecución", True, COLOR_TEXT)
        self.pantalla.blit(rep_tit, (panel_rect.left + 25, 410))

        y_offset = 470
        for clave, valor in reportes.items():
            txt = self.fuente_texto.render(f"{clave}: {valor}", True, COLOR_TEXT)
            self.pantalla.blit(txt, (panel_rect.left + 25, y_offset))
            y_offset += 30

        # 5. Dibujar de manera especial el botón "Mostrar árbol de búsqueda"
        if not self.arbol_disponible:
            # Si NO está disponible: lo dibujamos como un rectángulo gris estático y texto apagado
            pygame.draw.rect(self.pantalla, (220, 220, 220), self.boton_ver_arbol.rect, border_radius=8)
            txt = self.boton_ver_arbol.font.render(self.boton_ver_arbol.text, True, (160, 160, 160))
            self.pantalla.blit(txt, txt.get_rect(center=self.boton_ver_arbol.rect.center))
        else:
            # Si SÍ está disponible: llamamos a su método interactivo normal (cambiará de color al pasar el mouse)
            self.boton_ver_arbol.dibujar(self.pantalla)

        # 6. El Selector de Algoritmo AL FINAL para que flote sobre todo lo demás al desplegarse
        self.selector_algoritmo.dibujar(self.pantalla)