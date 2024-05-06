import pandas as pd

def obtener_coords_manim(puntos: pd.DataFrame, dims: int) -> list:
    """
    Obtiene las coordenadas de los puntos de un DataFrame de Pandas x, y, z.

    Args:
    puntos (pd.DataFrame): DataFrame con las columnas x, y, z.
    dims (int): Número de dimensiones, 0 si no está en dim.

    Returns:
    list: Lista de listas de 3 diomensiones con las coordenadas de los puntos para manim.
    """
    lista_puntos = []
    for i in range(len(puntos)):
        punto = []
        for j in range(3):
            if j >= dims:
                punto.append(0)
            else:
                punto.append(puntos.iloc[i, j])
        lista_puntos.append(punto)
    return lista_puntos

def lista2coords(lista: list) -> list:
    """
    Convierte una lista de listas de 2 dimensiones en una lista de coordenadas para manim.

    Args:
    lista (list): Lista de listas.

    Returns:
    list: Lista de coordenadas para manim.
    """
    return [[lista[i][0], lista[i][1], 0] for i in range(len(lista))]