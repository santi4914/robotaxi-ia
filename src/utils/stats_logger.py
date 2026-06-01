# src/utils/stats_logger.py
import time
from typing import Dict, Any, Optional, Set

class StatsTracker:
    """Encargado de medir y formatear estadísticas de ejecución.

    Métricas: tiempo, nodos expandidos, profundidad del árbol y costo de solución.
    """
    
    def __init__(self):
        self.start_time: float = 0.0
        self.end_time: float = 0.0

    def start_timer(self) -> None:
        """Registra el tiempo de inicio usando un contador de alta resolución."""
        self.start_time = time.perf_counter()

    def stop_timer(self) -> None:
        """Registra el tiempo de fin del algoritmo."""
        self.end_time = time.perf_counter()

    def get_elapsed_time_ms(self) -> float:
        """Devuelve el tiempo transcurrido en milisegundos."""
        return (self.end_time - self.start_time) * 1000.0

    def calculate_tree_depth(self, tree: Dict[Any, Dict[str, Any]]) -> int:
        """Calcula la profundidad máxima del árbol de expansión.

        El árbol se espera como: estado -> {'parent': estado_padre, ...}.
        Usa memoización y detección de ciclos para evitar RecursionError.
        """
        if not tree:
            return 0
            
        depths: Dict[Any, int] = {}
        
        def get_depth(node: Any, current_path: Set[Any]) -> int:
            # Caso base: nodo sin padre (raíz)
            if node not in tree or tree[node]['parent'] is None:
                return 0
                
            # Memoización: devolver profundidad ya calculada
            if node in depths:
                return depths[node]
                
            # Detección de ciclos (medida de robustez)
            if node in current_path:
                return 0 
                
            # Cálculo recursivo de profundidad
            current_path.add(node)
            parent = tree[node]['parent']
            depths[node] = 1 + get_depth(parent, current_path)
            current_path.remove(node)
            
            return depths[node]

        max_depth = 0
        for state in tree:
            depth = get_depth(state, set())
            if depth > max_depth:
                max_depth = depth
        return max_depth

    def generate_report(self, algo_name: str, nodes_expanded: int, tree: Dict[Any, Dict[str, Any]], cost: Optional[int] = None) -> Dict[str, str]:
        """Genera un diccionario formateado con las métricas para el panel lateral.

        Los valores son cadenas listas para mostrarse en la interfaz.
        """
        depth = self.calculate_tree_depth(tree)
        elapsed_ms = self.get_elapsed_time_ms()
        
        report = {
            "Algoritmo": algo_name,
            "Nodos Expandidos": str(nodes_expanded),
            "Profundidad del Árbol": str(depth),
            "Tiempo de Cómputo": f"{elapsed_ms:.3f} ms"
        }
        
        # Regla: sólo cuando se provee costo se muestra, en caso contrario "N/A"
        if cost is not None:
            report["Costo de Solución"] = str(cost)
        else:
            report["Costo de Solución"] = "N/A"
            
        return report