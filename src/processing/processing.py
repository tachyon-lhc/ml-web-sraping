"""
Procesamiento y guardado de datos
"""

import pandas as pd
from datetime import datetime
from .reporte import generar_reporte_completo


def limpiar_dataset(propiedades):
    """
    Aplica limpieza adicional al dataset.

    Args:
        propiedades: lista de diccionarios con las propiedades

    Returns:
        DataFrame de pandas limpio
    """
    df = pd.DataFrame(propiedades)

    print("\nLimpieza del dataset:")
    print(f"  Registros iniciales: {len(df)}")

    # Eliminar duplicados por título
    df = df.drop_duplicates(subset=["titulo"], keep="first")
    print(f"  Después de eliminar duplicados: {len(df)}")

    # Eliminar valores nulos en columnas críticas
    columnas_criticas = ["precio", "ambientes", "banos", "metros"]
    df = df.dropna(subset=columnas_criticas)
    print(f"  Después de eliminar nulos: {len(df)}")

    # Ordenar por zona y ciudad
    df = df.sort_values(["zona", "ciudad", "precio"])

    return df


def agregar_metadatos(df):
    """
    Agrega columnas adicionales al dataset.

    Args:
        df: DataFrame de pandas

    Returns:
        DataFrame con columnas adicionales
    """
    # Fecha de scraping
    df["fecha_scraping"] = datetime.now().strftime("%Y-%m-%d")

    # Precio por metro cuadrado
    df["precio_m2"] = (df["precio"] / df["metros"]).round(0).astype(int)

    return df


def generar_reporte(df):
    """
    Genera estadísticas del dataset.

    Args:
        df: DataFrame de pandas

    Returns:
        None (imprime el reporte)
    """
    print("\n" + "=" * 60)
    print("REPORTE DEL DATASET")
    print("=" * 60)

    print(f"\nTotal de propiedades: {len(df)}")

    print("\nDistribución por zona:")
    print(df["zona"].value_counts())

    print("\nTop 10 ciudades:")
    print(df["ciudad"].value_counts().head(10))

    print("\nEstadísticas de precio (USD):")
    print(df["precio"].describe())

    print("\nEstadísticas de metros cuadrados:")
    print(df["metros"].describe())

    print("\nPromedio de ambientes por zona:")
    print(df.groupby("zona")["ambientes"].mean().round(1))

    print("\nPrecio promedio por zona:")
    print(df.groupby("zona")["precio"].mean().round(0).astype(int))


def guardar_csv(df, nombre_archivo):
    """
    Guarda el DataFrame en CSV.

    Args:
        df: DataFrame de pandas
        nombre_archivo: string con el nombre del archivo

    Returns:
        None
    """
    df.to_csv(nombre_archivo, index=False, encoding="utf-8-sig")
    print(f"\nArchivo guardado: {nombre_archivo}")


def procesar_datos_completo(propiedades, stats_ciudades):
    """
    Pipeline completo de procesamiento

    Args:
        propiedades: lista de diccionarios
        stats_ciudades: dict con stats por ciudad

    Returns:
        DataFrame procesado
    """
    df = limpiar_dataset(propiedades)
    df = agregar_metadatos(df)

    generar_reporte_completo(df, stats_ciudades)

    return df
