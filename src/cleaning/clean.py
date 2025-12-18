import pandas as pd
from datetime import datetime

ruta = "~/home/tachyon/proyectos-ML/ML-web_scraping/data/raw/husing.csv"

df = pd.read_csv(ruta)

print("=" * 80)
print("DATASET ORIGINAL")
print("=" * 80)
print(f"Total de registros: {len(df)}")
print(f"\nColumnas actuales: {df.columns.tolist()}")

# 1. Eliminar columnas que no necesitamos
df = df.drop(["titulo", "fecha_scraping"], axis=1)

# 2. Traducir nombres de columnas al inglés
column_translation = {
    "precio": "price",
    "ambientes": "rooms",
    "banos": "bathrooms",
    "metros": "square_meters",
    "zona": "zone",
    "ciudad": "city",
    "precio_m2": "price_per_m2",
}
df = df.rename(columns=column_translation)

# 3. Agregar columna 'id' al inicio
df.insert(0, "id", range(1, len(df) + 1))

print("\n" + "=" * 80)
print("DATASET LIMPIO")
print("=" * 80)
print(f"\nColumnas nuevas (en inglés): {df.columns.tolist()}")
print(f"\nPrimeras filas:")
print(df.head(10))

# 4. Recuento por ZONA
print("\n" + "=" * 80)
print("DISTRIBUCIÓN POR ZONA")
print("=" * 80)
zone_counts = df["zone"].value_counts().sort_values(ascending=False)
print(zone_counts)
print(f"\nTotal de zonas: {len(zone_counts)}")

# 5. Recuento por CIUDAD
print("\n" + "=" * 80)
print("DISTRIBUCIÓN POR CIUDAD")
print("=" * 80)
city_counts = df["city"].value_counts().sort_values(ascending=False)
print(f"Total de ciudades: {len(city_counts)}")
print(f"\nTop 20 ciudades con más datos:")
print(city_counts.head(20))

# 6. GENERAR REPORTE DETALLADO
print("\n" + "=" * 80)
print("GENERANDO REPORTE DETALLADO...")
print("=" * 80)

report_filename = f"~/home/tachyon/proyectos-ML/ML-web_scraping/data/reports/data_distribution_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

with open(report_filename, "w", encoding="utf-8") as f:
    # Encabezado del reporte
    f.write("=" * 100 + "\n")
    f.write("REPORTE DE DISTRIBUCIÓN DE DATOS - PROPIEDADES BUENOS AIRES\n")
    f.write("=" * 100 + "\n")
    f.write(f"Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"Total de registros: {len(df):,}\n")
    f.write(f"Total de zonas: {len(zone_counts)}\n")
    f.write(f"Total de ciudades: {len(city_counts)}\n")
    f.write("=" * 100 + "\n\n")

    # Resumen general por zona
    f.write("RESUMEN POR ZONA\n")
    f.write("-" * 100 + "\n")
    f.write(f"{'ZONA':<40} {'REGISTROS':>15} {'% DEL TOTAL':>15} {'CIUDADES':>15}\n")
    f.write("-" * 100 + "\n")

    for zone in zone_counts.index:
        zone_df = df[df["zone"] == zone]
        num_cities = len(zone_df["city"].unique())
        pct = (len(zone_df) / len(df)) * 100
        f.write(f"{zone:<40} {len(zone_df):>15,} {pct:>14.2f}% {num_cities:>15}\n")

    f.write("=" * 100 + "\n\n\n")

    # Detalle por zona y ciudad
    f.write("DISTRIBUCIÓN DETALLADA: ZONA → CIUDAD\n")
    f.write("=" * 100 + "\n\n")

    for zone in sorted(zone_counts.index):
        zone_df = df[df["zone"] == zone]
        city_counts_zone = zone_df["city"].value_counts().sort_values(ascending=False)

        # Encabezado de la zona
        f.write("\n" + "█" * 100 + "\n")
        f.write(f"ZONA: {zone}\n")
        f.write(f"Total de registros en la zona: {len(zone_df):,}\n")
        f.write(f"Número de ciudades: {len(city_counts_zone)}\n")
        f.write("█" * 100 + "\n\n")

        # Tabla de ciudades
        f.write(
            f"{'  CIUDAD':<45} {'REGISTROS':>15} {'% DE LA ZONA':>15} {'% DEL TOTAL':>15}\n"
        )
        f.write("-" * 100 + "\n")

        for city, count in city_counts_zone.items():
            pct_zone = (count / len(zone_df)) * 100
            pct_total = (count / len(df)) * 100
            f.write(
                f"  {city:<43} {count:>15,} {pct_zone:>14.2f}% {pct_total:>14.2f}%\n"
            )

        f.write("\n")

        # Estadísticas de la zona
        f.write("  Estadísticas de esta zona:\n")
        f.write(
            f"    - Ciudad con más datos: {city_counts_zone.index[0]} ({city_counts_zone.iloc[0]:,} registros)\n"
        )
        f.write(
            f"    - Ciudad con menos datos: {city_counts_zone.index[-1]} ({city_counts_zone.iloc[-1]:,} registros)\n"
        )
        f.write(f"    - Promedio por ciudad: {city_counts_zone.mean():.1f} registros\n")
        f.write(
            f"    - Mediana por ciudad: {city_counts_zone.median():.0f} registros\n"
        )

        # Ciudades con pocos datos en esta zona
        low_data_cities = city_counts_zone[city_counts_zone < 50]
        if len(low_data_cities) > 0:
            f.write(f"    - Ciudades con < 50 registros: {len(low_data_cities)}\n")

        f.write("\n")

    # Análisis adicional al final
    f.write("\n" + "=" * 100 + "\n")
    f.write("ANÁLISIS ADICIONAL\n")
    f.write("=" * 100 + "\n\n")

    # Ciudades con pocos datos
    low_data_global = city_counts[city_counts < 100]
    f.write(f"Ciudades con menos de 100 registros: {len(low_data_global)}\n")
    f.write(f"Total de registros en estas ciudades: {low_data_global.sum():,}\n\n")

    very_low_data = city_counts[city_counts < 30]
    f.write(f"Ciudades con menos de 30 registros: {len(very_low_data)}\n")
    f.write(f"Total de registros en estas ciudades: {very_low_data.sum():,}\n\n")

    # Top ciudades
    f.write("Top 10 ciudades con más datos:\n")
    f.write("-" * 60 + "\n")
    for i, (city, count) in enumerate(city_counts.head(10).items(), 1):
        pct = (count / len(df)) * 100
        f.write(f"{i:2d}. {city:<35} {count:>8,} ({pct:5.2f}%)\n")

    f.write("\n" + "=" * 100 + "\n")
    f.write("FIN DEL REPORTE\n")
    f.write("=" * 100 + "\n")

print(f"\n✅ Reporte detallado generado: {report_filename}")

# 7. Estadísticas básicas
print("\n" + "=" * 80)
print("ESTADÍSTICAS BÁSICAS PARA MODELO PREDICTIVO")
print("=" * 80)
print("\nEstadísticas de variables numéricas:")
print(df[["price", "rooms", "bathrooms", "square_meters", "price_per_m2"]].describe())

# 8. Guardar dataset limpio
output_file = (
    "~/home/tachyon/proyectos-ML/ML-web_scraping/data/processed/housing_clean.csv"
)
df.to_csv(output_file, index=False)
print(f"\n✅ Dataset limpio guardado en: {output_file}")

print("\n" + "=" * 80)
print("ARCHIVOS GENERADOS")
print("=" * 80)
print(f"1. {output_file} - Dataset limpio con columnas en inglés")
print(f"2. {report_filename} - Reporte detallado de distribución")
print("\n¡Proceso completado!")
