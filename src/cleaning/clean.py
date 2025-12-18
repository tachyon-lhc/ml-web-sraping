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
print("\n¡Proceso completado!")
