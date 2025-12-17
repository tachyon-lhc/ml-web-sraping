"""
Punto de entrada del scraper con manejo de ciudades fallidas
"""

from scraper.config.config import UBICACIONES, PAGINAS_POR_CIUDAD
from scraper.scraper import scrapear_todo
from processing.processing import procesar_datos_completo, guardar_csv


def main():
    print("=" * 60)
    print("SCRAPER DE MERCADOLIBRE - CASAS EN VENTA")
    print("=" * 60)

    # Calcular estimaciones
    total_ciudades = sum(len(ciudades) for ciudades in UBICACIONES.values())
    print(f"\nCiudades a scrapear: {total_ciudades}")
    print(f"Páginas por ciudad: {PAGINAS_POR_CIUDAD}")
    print("Reintentos por ciudad: 3 (con headers diferentes)")

    # Confirmación
    respuesta = input("\n¿Desea continuar? (s/n): ")
    if respuesta.lower() != "s":
        print("Cancelado")
        return

    # Scraping
    print("\nIniciando scraping con sistema de reintentos...")
    propiedades, stats_ciudades, ciudades_fallidas = scrapear_todo(
        UBICACIONES, PAGINAS_POR_CIUDAD
    )

    print(f"\n{'=' * 60}")
    print(f"Scraping completado: {len(propiedades)} propiedades extraídas")

    # Mostrar ciudades fallidas
    if ciudades_fallidas:
        print(
            f"\n⚠ Ciudades que fallaron después de 3 intentos ({len(ciudades_fallidas)}):"
        )
        for ciudad in ciudades_fallidas:
            print(f"  - {ciudad}")

        # Guardar lista de fallidas
        with open("data/processed/ciudades_fallidas.txt", "w") as f:
            f.write("\n".join(ciudades_fallidas))
        print("\n📁 Lista guardada en: data/processed/ciudades_fallidas.txt")
    else:
        print("\n✓ Todas las ciudades scrapeadas exitosamente")

    if not propiedades:
        print("\nNo se encontraron propiedades")
        return

    # Procesamiento y reportes
    print("\nProcesando datos...")
    df = procesar_datos_completo(propiedades, stats_ciudades)

    # Guardar
    nombre_archivo = (
        "~/home/tachyon/proyectos-ML/ML-web_scraping/data/processed/husing.csv"
    )
    guardar_csv(df, nombre_archivo)

    print("\n" + "=" * 60)
    print("PROCESO COMPLETADO")
    print("=" * 60)
    print(f"\nPropiedades válidas: {len(df)}")
    print(
        f"Ciudades exitosas: {total_ciudades - len(ciudades_fallidas)}/{total_ciudades}"
    )


if __name__ == "__main__":
    main()
