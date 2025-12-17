"""
Generación de reportes detallados
"""

import pandas as pd


def generar_reporte_ciudades(stats_ciudades):
    """
    Genera reporte de ciudades ordenadas por cantidad de propiedades

    Args:
        stats_ciudades: dict con {ciudad: cantidad}

    Returns:
        None (imprime el reporte)
    """
    print("\n" + "=" * 70)
    print("REPORTE POR CIUDAD")
    print("=" * 70)

    # Convertir a DataFrame para facilitar análisis
    df = pd.DataFrame(list(stats_ciudades.items()), columns=["Ciudad", "Propiedades"])
    df = df.sort_values("Propiedades", ascending=False)

    total = df["Propiedades"].sum()

    print(f"\nTotal de propiedades: {total}")
    print(f"Ciudades scrapeadas: {len(df)}")
    print(f"Promedio por ciudad: {df['Propiedades'].mean():.1f}")

    # Ciudades con más propiedades
    print("\n" + "-" * 70)
    print("TOP 10 - CIUDADES CON MÁS PROPIEDADES")
    print("-" * 70)
    top10 = df.head(10)
    for idx, row in top10.iterrows():
        porcentaje = (row["Propiedades"] / total) * 100
        print(f"{row['Ciudad']:45} {row['Propiedades']:4} ({porcentaje:5.1f}%)")

    # Ciudades con MENOS propiedades (posibles problemas)
    print("\n" + "-" * 70)
    print("BOTTOM 10 - CIUDADES CON MENOS PROPIEDADES")
    print("-" * 70)
    bottom10 = df.tail(10).sort_values("Propiedades")
    for idx, row in bottom10.iterrows():
        if row["Propiedades"] == 0:
            status = "⚠️  CERO"
        elif row["Propiedades"] < 5:
            status = "⚠️  BAJO"
        else:
            status = "✓"
        print(f"{status} {row['Ciudad']:45} {row['Propiedades']:4}")

    # Ciudades con 0 propiedades
    cero = df[df["Propiedades"] == 0]
    if len(cero) > 0:
        print("\n" + "-" * 70)
        print(f"⚠️  CIUDADES SIN PROPIEDADES ({len(cero)})")
        print("-" * 70)
        for idx, row in cero.iterrows():
            print(f"  - {row['Ciudad']}")

    # Guardar reporte en CSV
    df.to_csv("data/processed/reporte_ciudades.csv", index=False, encoding="utf-8-sig")
    print("\n📁 Reporte guardado: data/processed/reporte_ciudades.csv")


def generar_reporte_completo(df, stats_ciudades):
    """
    Genera todos los reportes: dataset y ciudades

    Args:
        df: DataFrame con las propiedades
        stats_ciudades: dict con stats por ciudad
    """
    from .processing import generar_reporte

    # Reporte del dataset
    generar_reporte(df)

    # Reporte por ciudad
    generar_reporte_ciudades(stats_ciudades)
