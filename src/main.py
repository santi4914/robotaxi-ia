import sys
import pygame
import os
from ui.renderer import Renderer, WelcomeScreen
from logic.environment import load_world
from logic.algorithms.uninformed_search import amplitud, costo_uniforme, profundidad_evitando_ciclos
from logic.algorithms.informed_search import avara, a_estrella
from utils.stats_logger import StatsTracker
from ui.tree_viewer import TreeViewer

# --- Mapeo de algoritmos ---
ALGORITMOS = {
    "Amplitud": amplitud,
    "Costo Uniforme": costo_uniforme,
    "Profundidad": profundidad_evitando_ciclos,
    "Avara": avara,
    "A*": a_estrella
}

def cargar_mundos_disponibles(data_dir):
    """Retorna lista de archivos .txt disponibles en la carpeta data."""
    mundos = []
    if os.path.exists(data_dir):
        for archivo in os.listdir(data_dir):
            if archivo.endswith('.txt'):
                mundos.append(archivo)
    return sorted(mundos)

def validar_y_cargar_mapa(data_dir, nombre_mapa):
    """Valida y carga un mapa. Retorna (éxito, mundo, inicio, pasajeros, destino, error_msg)."""
    try:
        ruta_mapa = os.path.join(data_dir, nombre_mapa)
        mundo, inicio, pasajeros, destino = load_world(ruta_mapa)
        return True, mundo, inicio, pasajeros, destino, None
    except Exception as e:
        return False, None, None, None, None, str(e)

def main():
    # Inicialización de pygame
    pygame.init()
    
    # Inicialización de la ventana principal
    ANCHO, ALTO = 1150, 720
    screen = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Robotaxi Zoox - Simulador IA")
    reloj = pygame.time.Clock()
    FPS = 60
    
    # Rutas
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    
    # Crear pantalla de bienvenida
    welcome_screen = WelcomeScreen(ANCHO, ALTO)
    
    datos_ultimo_arbol = None
    nombre_ultimo_algo = ""
    camino_ultimo = []

    # Cargar lista de mundos disponibles
    mundos_disponibles = cargar_mundos_disponibles(data_dir)
    if not mundos_disponibles:
        print("Error: No hay archivos .txt en la carpeta data/")
        return
    
    welcome_screen.set_mapas_disponibles(mundos_disponibles)
    
    # Variables de estado
    en_pantalla_bienvenida = True
    renderer = None
    mundo_actual = None
    inicio = None
    pasajeros = None
    destino = None
    
    # Estado de la simulación
    indice_algo = 0
    tracker = StatsTracker()
    reportes = {
        "Algoritmo": "-",
        "Nodos Expandidos": "-",
        "Profundidad del Árbol": "-",
        "Tiempo de Cómputo": "-",
        "Costo de Solución": "-",
        "Estado": "Esperando inicio..."
    }

    ejecutando = True
    while ejecutando:
        dt = reloj.tick(FPS) / 1000.0
        pos_raton = pygame.mouse.get_pos()
        click = False

        # --- BUCLE DE EVENTOS ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                click = True

        # --- LÓGICA DE PANTALLA DE BIENVENIDA ---
        if en_pantalla_bienvenida:
            accion = welcome_screen.manejar_eventos(pos_raton, click)
            
            if accion == "CONTINUAR":
                # Validar el mapa seleccionado
                exito, mundo_actual, inicio, pasajeros, destino, error = validar_y_cargar_mapa(
                    data_dir, welcome_screen.mapa_seleccionado
                )
                
                if exito:
                    # Crear renderer ahora que tenemos un mapa válido
                    renderer = Renderer(ANCHO, ALTO)
                    renderer.cargar_mundo(mundo_actual)
                    en_pantalla_bienvenida = False
                else:
                    # Mostrar error en la pantalla de bienvenida
                    welcome_screen.error_mensaje = error
            
            welcome_screen.dibujar(screen)
        
        # --- LÓGICA DE SIMULACIÓN ---
        else:
            if renderer is None:
                continue
            
            accion = renderer.manejar_eventos_ui(pos_raton, click)
            
            if accion == "INICIAR":
                # Obtener el algoritmo seleccionado del selector
                algo_nombre = renderer.obtener_algoritmo_seleccionado()
                
                # Verificar que hay un algoritmo seleccionado
                if not algo_nombre:
                    reportes["Estado"] = "Error: Selecciona un algoritmo primero"
                    continue
                
                # Verificar que hay un mapa cargado
                if mundo_actual is None:
                    reportes["Estado"] = "Error: Carga un mapa primero"
                    reportes["Algoritmo"] = algo_nombre
                else:
                    # Ejecutar el algoritmo seleccionado
                    algoritmo_func = ALGORITMOS[algo_nombre]
                    
                    try:
                        # Medir tiempo de ejecución
                        tracker.start_timer()
                        resultado = algoritmo_func(mundo_actual, inicio, pasajeros, destino)
                        tracker.stop_timer()
                        
                        if resultado is None:
                            reportes["Estado"] = "No hay solución"
                            reportes["Algoritmo"] = algo_nombre
                            reportes["Nodos Expandidos"] = "0"
                            reportes["Profundidad del Árbol"] = "0"
                            reportes["Tiempo de Cómputo"] = f"{tracker.get_elapsed_time_ms():.3f} ms"
                            reportes["Costo de Solución"] = "N/A"
                        else:
                            camino, nodos_expandidos, arbol_expansion, costo_final = resultado
                            
                            # Guardamos los datos para la ventana del árbol
                            datos_ultimo_arbol = arbol_expansion
                            nombre_ultimo_algo = algo_nombre
                            camino_ultimo = camino
                            renderer.arbol_disponible = True # Activamos el botón en la UI
                            
                            report = tracker.generate_report(algo_nombre, nodos_expandidos, arbol_expansion, costo_final)
                            reportes.update(report)
                            reportes["Estado"] = "Completado"
                            renderer.iniciar_animacion(camino)
                    
                    except Exception as e:
                        reportes["Estado"] = f"Error: {str(e)}"
                        reportes["Algoritmo"] = algo_nombre
                        print(f"Error durante ejecución: {e}")
            
            elif accion == "RESET":
                renderer.cargar_mundo(mundo_actual)
                renderer.limpiar_selector_algoritmo()
                reportes = {
                    "Algoritmo": "-",
                    "Nodos Expandidos": "-",
                    "Profundidad del Árbol": "-",
                    "Tiempo de Cómputo": "-",
                    "Costo de Solución": "-",
                    "Estado": "Reseteado"
                }

            elif accion == "VER_ARBOL":
                if datos_ultimo_arbol:
                    # Instanciamos el visualizador externo y lanzamos su ventana síncrona
                    viewer = TreeViewer(datos_ultimo_arbol, nombre_ultimo_algo, camino_ultimo)
                    viewer.mostrar_ventana()
                    
                    # CORRECCIÓN: Quitamos el "self." porque estamos en main()
                    pygame.display.set_mode((ANCHO, ALTO)) 
                    pygame.display.set_caption("Robotaxi Zoox - Simulador IA")
            
            # --- ACTUALIZAR Y DIBUJAR SIMULACIÓN ---
            renderer.actualizar(dt)
            renderer.dibujar(reportes)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()