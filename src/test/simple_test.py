"""
Test simple para verificar que todo funciona
"""

import sys

sys.path.append("src")

from ..scraper.scraper import obtener_html, extraer_pagina

# URL que sabemos que funciona
url = "https://inmuebles.mercadolibre.com.ar/casas/venta/bsas-gba-norte/pilar/"

print("Probando scraper básico...")
print(f"URL: {url}\n")

# Obtener HTML
print("1. Obteniendo HTML...")
html = obtener_html(url)

if not html:
    print("ERROR: No se pudo obtener HTML")
    sys.exit(1)

print(f"   HTML recibido: {len(html):,} caracteres")

# Parsear
print("\n2. Extrayendo propiedades...")
propiedades, descartadas = extraer_pagina(html, "GBA Norte", "Pilar")

print(f"   Válidas: {len(propiedades)}")
print(f"   Descartadas: {descartadas}")

if len(propiedades) == 0:
    print("\nERROR: No se encontraron propiedades válidas")
    print("El problema está en la extracción, no en los headers")
else:
    print("\n✓ Scraper funcionando correctamente")
    print("\nPrimera propiedad:")
    prop = propiedades[0]
    for key, value in prop.items():
        print(f"   {key}: {value}")
