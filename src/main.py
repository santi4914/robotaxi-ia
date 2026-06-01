import sys
import pygame
from ui.renderer import Renderer

# --- DATOS DE PRUEBA HASTA QUE SE CONECTEN LOS ALGORITMOS ---
# Matriz de prueba (basada en el ejemplo del documento)
MATRIZ_PRUEBA = [
    [4, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 1, 1, 0, 0, 0, 3, 0, 0, 0],
    [2, 1, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 3, 0, 0, 0, 3, 0],
    [0, 1, 1, 0, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 1, 1, 0, 0, 0, 5],
    [4, 1, 1, 1, 1, 1, 0, 1, 1, 1],
    [0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
    [0, 1, 0, 1, 0, 1, 1, 1, 0, 1],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 1]
]

# Camino simulado para probar la animación y la UI en esta fase frontend
CAMINO_PRUEBA = [
    (2,0), (3,0), (4,0), (5,0), (6,0), # Recoge Pasajero en (6,0)
    (5,0), (4,0), (3,0), (2,0), (1,0), (0,0), # Recoge Pasajero en (0,0)
    (1,0), (2,0), (3,0), (3,1), (3,2), (3,3), (2,3), (1,3), (1,4),
    (1,5), (2,5), (3,5), (3,6), (3,7), (4,7), (5,7), (5,8), (5,9) # Destino (5,9)
]

def main():
    # Inicialización de la ventana principal
    ANCHO, ALTO = 1050, 720
    renderer = Renderer(ANCHO, ALTO)
    reloj = pygame.time.Clock()
    FPS = 60
    
    # Estado inicial de la aplicación
    algoritmos = ["Amplitud", "Costo Uniforme", "Profundidad", "Avara", "A*"]
    indice_algo = 0
    
    # Reportes iniciales (vacíos)
    reportes = {
        "Estado": "Esperando inicio...",
        "Nodos Expandidos": "-",
        "Profundidad": "-",
        "Tiempo de Cómputo": "-",
        "Costo de Solución": "-"
    }

    # Cargar el entorno de prueba a la interfaz
    renderer.cargar_mundo(MATRIZ_PRUEBA)

    ejecutando = True
    while ejecutando:
        # Calcular delta_tiempo en segundos para la animación
        dt = reloj.tick(FPS) / 1000.0
        
        pos_raton = pygame.mouse.get_pos()
        click = False

        # --- BUCLE DE EVENTOS ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                click = True

        # --- LÓGICA DE INTERFAZ (CONTROLADOR) ---
        accion = renderer.manejar_eventos_ui(pos_raton, click)
        
        if accion == "CAMBIAR_ALGORITMO":
            indice_algo = (indice_algo + 1) % len(algoritmos)
            renderer.actualizar_texto_algoritmo(algoritmos[indice_algo])
            
        elif accion == "INICIAR":
            # Aquí en el futuro llamaremos:
            # path, nodos, prof, tiempo, costo = logic.algorithms.ejecutar(mundo, algoritmo)
            
            # Por ahora, simulamos un resultado exitoso para probar la UI
            reportes["Estado"] = "Completado"
            reportes["Nodos Expandidos"] = "142 (Simulado)"
            reportes["Profundidad"] = "28 (Simulado)"
            reportes["Tiempo de Cómputo"] = "45 ms (Simulado)"
            
            algoritmo_actual = algoritmos[indice_algo]
            if algoritmo_actual in ["Costo Uniforme", "A*"]:
                reportes["Costo de Solución"] = "42 (Simulado)"
            else:
                reportes["Costo de Solución"] = "N/A"

            # Inyectar el camino al motor gráfico
            renderer.iniciar_animacion(CAMINO_PRUEBA)
            
        elif accion == "RESET":
            renderer.cargar_mundo(MATRIZ_PRUEBA)
            reportes = { k: "-" for k in reportes }
            reportes["Estado"] = "Reseteado"

        # --- ACTUALIZAR Y DIBUJAR ---
        renderer.actualizar(dt)
        renderer.dibujar(reportes)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()