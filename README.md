# Robotaxi IA - Simulador de Búsqueda de Rutas

Simulador interactivo que implementa algoritmos de búsqueda **informada** y **no informada** para que un RobotTaxi Zoox navegue a través de una cuadrícula de 10×10 recogiendo pasajeros.

## 🎯 Características

- **Algoritmos Informados**: Búsqueda Avara y A\*
- **Algoritmos No Informados**: Búsqueda por Amplitud, Costo Uniforme, Profundidad Evitando Ciclos
- **Interfaz Gráfica**: UI moderna con Pygame
- **Pantalla de Selección de Mapas**: Carga mapas desde archivos `.txt`
- **Reporte de Ejecución**: Visualiza métricas (nodos expandidos, profundidad, tiempo, costo)
- **Animación Visual**: Observa el RobotTaxi recorrer la ruta encontrada

## 📋 Requisitos

- Python 3.12+
- Pygame 2.6.1
- Los paquetes especificados en `requirements.txt`

## 🚀 Instalación y Ejecución

### 1. Clonar o descargar el proyecto

```bash
git clone <repositorio>
cd robotaxi-ia
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Ejecutar la aplicación

```bash
python src/main.py
```

La ventana del simulador se abrirá mostrando la **Pantalla de Bienvenida** con el fondo del RobotTaxi Zoox.

---

## 📖 Guía de Uso

### Pantalla de Bienvenida

1. **Seleccionar Mapa**
   - Haz clic en el botón **"Elegir Mapa"**
   - Se abrirá una lista con todos los mapas disponibles en la carpeta `data/`
   - Selecciona el mapa que deseas cargar

2. **Continuar a la Simulación**
   - Una vez seleccionado un mapa válido, haz clic en **"Continuar"**
   - Se cargará la simulación

### Panel de Simulación

El panel derecho contiene:

#### 1️⃣ Selector de Algoritmo (Jerárquico)

**Paso 1 - Elegir Tipo de Búsqueda:**

- Haz clic en **"Elegir tipo"**
- Elige entre:
  - **Búsqueda Informada** (Avara, A\*)
  - **Búsqueda No Informada** (Amplitud, Costo Uniforme, Profundidad)

**Paso 2 - Elegir Algoritmo Específico:**

- Haz clic en **"Elegir algoritmo"**
- Selecciona el algoritmo deseado
- El botón se actualizará mostrando tu selección

#### 2️⃣ Controles de Simulación

- **Iniciar**: Ejecuta el algoritmo seleccionado y muestra el camino en la grilla
- **Resetear**: Limpia la simulación y permite seleccionar otro algoritmo

#### 3️⃣ Reporte de Ejecución

Después de ejecutar un algoritmo, se mostrará:

- **Algoritmo**: Nombre del algoritmo utilizado
- **Nodos Expandidos**: Cantidad de nodos explorados
- **Profundidad del Árbol**: Profundidad máxima alcanzada
- **Tiempo de Cómputo**: Segundos tardados en encontrar la solución
- **Costo de Solución**: Costo total del camino (si aplica)
- **Estado**: Mensaje de estado actual

### Elementos de la Grilla

| Símbolo | Significado                  |
| ------- | ---------------------------- |
| 🟡      | RobotTaxi (Posición inicial) |
| 🟣      | Pasajero                     |
| 🟢      | Destino                      |
| 🔴      | Tráfico Alto (Costo 7)       |
| ⬛      | Muro                         |
| ⬜      | Celda vacía                  |
| 🟦      | Ruta encontrada              |

---

## 📁 Agregar Mapas Personalizados

### Formato de Archivo

Los archivos de mapa deben ser `.txt` y contener una matriz de 10×10 con los siguientes valores:

```
0 = Celda vacía
1 = Muro (obstáculo)
2 = Posición inicial del RobotTaxi
3 = Tráfico Alto (costo de movimiento: 7)
4 = Pasajero
5 = Destino
```

### Ejemplo de Mapa

```txt
0 0 0 0 0 0 0 0 0 0
0 1 1 0 0 0 1 1 0 0
0 1 0 0 3 0 1 0 0 0
0 0 0 1 0 1 0 0 0 0
0 1 0 0 0 0 0 1 0 0
2 0 0 1 0 1 0 0 4 0
0 1 0 0 0 0 1 0 0 0
0 0 1 0 1 0 0 0 1 0
0 0 0 0 0 0 0 0 0 3
0 1 0 0 0 1 0 1 0 5
```

### Pasos para Cargar tu Mapa

1. Crea un archivo `.txt` con tu matriz de 10×10 (puede ser cualquier nombre)
2. Colócalo en la carpeta `data/`
3. Reinicia la aplicación
4. En la **Pantalla de Bienvenida**, haz clic en **"Elegir Mapa"**
5. Tu mapa aparecerá en la lista
6. ¡Selecciona y prueba tu mapa!

### Validación de Mapas

El simulador validará automáticamente:

- ✅ Que sea una matriz de 10×10
- ✅ Que contenga exactamente 1 RobotTaxi (2)
- ✅ Que contenga al menos 1 pasajero (4)
- ✅ Que contenga exactamente 1 destino (5)
- ✅ Que solo contenga valores válidos (0-5)

Si hay un error, verás un mensaje de error en la pantalla de bienvenida.

---

## 📊 Estructura del Proyecto

```
robotaxi-ia/
├── src/
│   ├── main.py                    # Punto de entrada principal
│   ├── ui/
│   │   ├── renderer.py            # Motor gráfico Pygame
│   │   └── assets/
│   ├── logic/
│   │   ├── environment.py         # Carga y validación de mapas
│   │   ├── search_node.py         # Nodo para búsqueda
│   │   └── algorithms/
│   │       ├── informed_search.py # A*, Avara
│   │       └── uninformed_search.py # BFS, UCS, DFS
│   └── utils/
│       ├── heuristics.py          # Heurísticas (Manhattan)
│       └── stats_logger.py        # Rastreador de estadísticas
├── data/                          # Carpeta con mapas (.txt)
├── public/                        # Recursos (imágenes)
├── requirements.txt               # Dependencias Python
└── README.md                      # Este archivo
```

---

## ⚙️ Tecnologías Utilizadas

- **Python 3.12**: Lenguaje principal
- **Pygame 2.6.1**: Renderización gráfica
- **Algoritmos IA**: Búsqueda informada y no informada

---

## 📝 Notas Importantes

- La heurística utilizada es la **distancia Manhattan** para los algoritmos informados
- El simulador soporta rutas con múltiples pasajeros
- Los costos de movimiento son 1 (normal) y 7 (tráfico alto)
- El tiempo de ejecución se mide en segundos con precisión de milisegundos

---

## 🐛 Solución de Problemas

### La aplicación no inicia

- Verifica que Python 3.12+ esté instalado: `python --version`
- Asegúrate de instalar las dependencias: `pip install -r requirements.txt`

### No aparecen mapas en la lista

- Verifica que haya archivos `.txt` en la carpeta `data/`
- Comprueba que los nombres de archivo no tengan espacios especiales

### El mapa es rechazado

- Verifica que sea una matriz exacta de 10×10
- Asegúrate de que contenga exactamente 1 RobotTaxi (2), al menos 1 pasajero (4), y exactamente 1 destino (5)
- Verifica que solo contenga valores 0-5

---
