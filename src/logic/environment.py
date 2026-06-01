# src/logic/environment.py
import os

def load_world(file_path):
    """Lee un archivo .txt y devuelve (mundo, inicio, pasajeros, destino)."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Error: El archivo '{file_path}' no existe.")

    matrix = []
    with open(file_path, 'r') as file:
        for line in file:
            row_data = line.strip().split()
            if not row_data:
                continue
            try:
                int_row = [int(cell) for cell in row_data]
                matrix.append(int_row)
            except ValueError:
                raise ValueError("Error de validación: la matriz contiene caracteres no enteros.")

    validate_matrix(matrix)
    return extract_entities(matrix)


def validate_matrix(matrix):
    """Valida reglas del proyecto: tamaño, valores y conteos esperados."""
    if len(matrix) != 10:
        raise ValueError(f"Error de validación: la matriz debe tener exactamente 10 filas. Encontradas {len(matrix)}.")

    start_count = 0
    dest_count = 0
    passenger_count = 0
    valid_values = {0, 1, 2, 3, 4, 5}

    for r_idx, row in enumerate(matrix):
        if len(row) != 10:
            raise ValueError(f"Error de validación: la fila {r_idx} debe tener 10 columnas. Encontradas {len(row)}.")
        for c_idx, cell in enumerate(row):
            if cell not in valid_values:
                raise ValueError(f"Error de validación: valor inválido '{cell}' en ({r_idx}, {c_idx}). Permitidos: 0-5.")
            if cell == 2:
                start_count += 1
            elif cell == 5:
                dest_count += 1
            elif cell == 4:
                passenger_count += 1

    if start_count != 1:
        raise ValueError(f"Error de validación: debe haber exactamente 1 inicio (2). Encontrados {start_count}.")
    if dest_count != 1:
        raise ValueError(f"Error de validación: debe haber exactamente 1 destino (5). Encontrados {dest_count}.")
    if passenger_count < 1:
        raise ValueError(f"Error de validación: debe haber al menos 1 pasajero (4). Encontrados {passenger_count}.")


def extract_entities(matrix):
    """Extrae coordenadas de inicio, pasajeros y destino."""
    start = None
    destination = None
    passengers = []

    for r in range(10):
        for c in range(10):
            if matrix[r][c] == 2:
                start = (r, c)
            elif matrix[r][c] == 5:
                destination = (r, c)
            elif matrix[r][c] == 4:
                passengers.append((r, c))

    return matrix, start, passengers, destination