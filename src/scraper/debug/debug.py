"""
Script de debugging para una ciudad específica
Muestra paso a paso qué encuentra y qué falla
"""

import requests
from bs4 import BeautifulSoup
from .config.config import HEADERS
from .utils.utils import es_valor_exacto, extraer_numero, limpiar_precio


def debug_ciudad(url):
    """
    Debuggea una ciudad específica mostrando todo el proceso
    """
    print("=" * 70)
    print("DEBUG DE CIUDAD")
    print("=" * 70)
    print(f"\nURL: {url}")

    # Paso 1: Obtener HTML
    print("\n[PASO 1] Obteniendo HTML...")
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        print(f"Status Code: {response.status_code}")

        if response.status_code != 200:
            print(f"ERROR: Status code no es 200")
            return

        html = response.text
        print(f"Tamaño del HTML: {len(html):,} caracteres")

    except Exception as e:
        print(f"ERROR en la petición: {e}")
        return

    # Paso 2: Parsear HTML
    print("\n[PASO 2] Parseando HTML...")
    soup = BeautifulSoup(html, "html.parser")

    # Buscar cards
    cards = soup.find_all("div", class_="poly-card__content")
    print(f"Cards encontradas: {len(cards)}")

    if len(cards) == 0:
        print("\nERROR: No se encontraron cards")
        print("Intentando buscar con otros selectores...")

        # Intentar otros selectores comunes
        alternativas = [
            ("li", "ui-search-layout__item"),
            ("div", "ui-search-result__content"),
            ("article", None),
        ]

        for tag, clase in alternativas:
            if clase:
                items = soup.find_all(tag, class_=clase)
            else:
                items = soup.find_all(tag)
            print(f"  {tag} class='{clase}': {len(items)} encontrados")

        # Guardar HTML para inspección manual
        with open("debug_html.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("\nHTML guardado en 'debug_html.html' para inspección manual")
        return

    # Detectar si hay contenido dinámico
    print("\n[DIAGNÓSTICO ADICIONAL]")

    # Buscar scripts de React/JavaScript
    scripts = soup.find_all("script")
    print(f"Scripts en la página: {len(scripts)}")

    # Buscar indicadores de contenido dinámico
    indicadores = [
        "react",
        "vue",
        "angular",
        "__NEXT_DATA__",
        "window.__PRELOADED_STATE__",
        "application/json",
    ]

    for script in scripts[:10]:
        script_text = script.string if script.string else ""
        for indicador in indicadores:
            if indicador.lower() in script_text.lower():
                print(f"  Detectado: {indicador}")
                break

    # Buscar divs con id que sugieren contenido dinámico
    root_divs = soup.find_all("div", id=True)
    print(f"\nDivs con ID: {len(root_divs)}")
    for div in root_divs[:5]:
        print(f"  - {div.get('id')}")

    # Buscar meta tags que indican la estructura
    meta_tags = soup.find_all("meta")
    for meta in meta_tags:
        if "property" in meta.attrs and "og:" in meta.get("property", ""):
            print(f"  Meta: {meta.get('property')} = {meta.get('content', '')[:50]}")

    # Paso 3: Analizar primera card en detalle
    print("\n[PASO 3] Analizando primera card en detalle...")
    print("-" * 70)

    card = cards[0]

    # Título
    print("\n1. TÍTULO:")
    titulo_elem = card.find("h2", class_="poly-component__title-wrapper")
    if titulo_elem:
        print(f"   Encontrado: {titulo_elem.text.strip()[:60]}...")
    else:
        print("   NO ENCONTRADO")
        # Buscar títulos alternativos
        h2_all = card.find_all("h2")
        print(f"   Otros h2 en la card: {len(h2_all)}")
        for h2 in h2_all:
            print(f"     - class: {h2.get('class')}")
            print(f"       texto: {h2.text.strip()[:40]}")

    # Precio
    print("\n2. PRECIO:")
    contenedor_precio = card.find("div", class_="poly-component__price")
    if contenedor_precio:
        print("   Contenedor encontrado")
        precio_elem = contenedor_precio.find(
            "span", class_="andes-money-amount__fraction"
        )
        if precio_elem:
            precio_texto = precio_elem.text.strip()
            print(f"   Precio texto: {precio_texto}")
            precio_limpio = limpiar_precio(precio_texto)
            print(f"   Precio limpio: {precio_limpio}")
        else:
            print("   NO se encontró el span del precio")
            # Mostrar todos los spans
            spans = contenedor_precio.find_all("span")
            print(f"   Spans en el contenedor: {len(spans)}")
            for span in spans[:3]:
                print(f"     - class: {span.get('class')}")
                print(f"       texto: {span.text.strip()}")
    else:
        print("   Contenedor NO encontrado")
        # Buscar alternativas
        precio_divs = card.find_all(
            "div", class_=lambda x: x and "price" in str(x).lower()
        )
        print(f"   Divs con 'price' en la clase: {len(precio_divs)}")
        for div in precio_divs[:2]:
            print(f"     - class: {div.get('class')}")

    # Atributos
    print("\n3. ATRIBUTOS:")
    contenedor_atributos = card.find("div", class_="poly-component__attributes-list")
    if contenedor_atributos:
        print("   Contenedor encontrado")
        lista = contenedor_atributos.find("ul", class_="poly-attributes_list")
        if lista:
            print("   Lista encontrada")
            items = lista.find_all("li", class_="poly-attributes_list__item")
            print(f"   Items: {len(items)}")

            for i, item in enumerate(items, 1):
                texto = item.text.strip()
                print(f"\n   Item {i}: {texto}")
                print(f"     Es exacto: {es_valor_exacto(texto)}")
                if es_valor_exacto(texto):
                    print(f"     Número extraído: {extraer_numero(texto)}")

        else:
            print("   Lista NO encontrada")
    else:
        print("   Contenedor NO encontrado")
        # Buscar alternativas
        ul_all = card.find_all("ul")
        print(f"   ULs en la card: {len(ul_all)}")
        for ul in ul_all:
            print(f"     - class: {ul.get('class')}")
            lis = ul.find_all("li")
            print(f"       lis: {len(lis)}")
            if lis:
                print(f"       ejemplo: {lis[0].text.strip()[:30]}")

    # Paso 4: Resumen de todas las cards
    print("\n" + "=" * 70)
    print("[PASO 4] Resumen de todas las cards")
    print("=" * 70)

    validas = 0
    sin_titulo = 0
    sin_precio = 0
    sin_atributos = 0
    atributos_rango = 0

    for card in cards:
        # Verificar título
        titulo = card.find("h2", class_="poly-component__title-wrapper")
        if not titulo:
            sin_titulo += 1
            continue

        # Verificar precio
        contenedor_precio = card.find("div", class_="poly-component__price")
        if not contenedor_precio:
            sin_precio += 1
            continue
        precio_elem = contenedor_precio.find(
            "span", class_="andes-money-amount__fraction"
        )
        if not precio_elem:
            sin_precio += 1
            continue

        # Verificar atributos
        contenedor_atributos = card.find(
            "div", class_="poly-component__attributes-list"
        )
        if not contenedor_atributos:
            sin_atributos += 1
            continue

        lista = contenedor_atributos.find("ul", class_="poly-attributes_list")
        if not lista:
            sin_atributos += 1
            continue

        items = lista.find_all("li", class_="poly-attributes_list__item")
        if len(items) < 3:
            sin_atributos += 1
            continue

        # Verificar que no sean rangos
        es_valido = True
        for item in items[:3]:
            texto = item.text.strip()
            if not es_valor_exacto(texto):
                atributos_rango += 1
                es_valido = False
                break

        if es_valido:
            validas += 1

    print(f"\nTotal cards: {len(cards)}")
    print(f"Válidas: {validas}")
    print(f"Descartadas por falta de título: {sin_titulo}")
    print(f"Descartadas por falta de precio: {sin_precio}")
    print(f"Descartadas por falta de atributos: {sin_atributos}")
    print(f"Descartadas por atributos con rango: {atributos_rango}")

    if validas == 0:
        print("\n" + "=" * 70)
        print("DIAGNÓSTICO:")
        print("=" * 70)
        if sin_titulo > 0:
            print("- Problema con selector de título")
            print("  Revisar: h2 class='poly-component__title-wrapper'")
        if sin_precio > 0:
            print("- Problema con selector de precio")
            print("  Revisar estructura del precio en debug_html.html")
        if sin_atributos > 0:
            print("- Problema con selector de atributos")
            print("  Revisar: div class='poly-component__attributes-list'")
        if atributos_rango > 0:
            print("- Muchas propiedades tienen rangos (múltiples unidades)")


def main():
    """
    Interfaz para debuggear una ciudad
    """
    print("Script de Debugging de Ciudad")
    print("=" * 70)

    # URLs de ejemplo para testear
    urls_ejemplo = {
        "1": (
            "Moron",
            "https://inmuebles.mercadolibre.com.ar/casas/venta/bsas-gba-oeste/moron/",
        ),
        "2": ("Mendoza", "https://inmuebles.mercadolibre.com.ar/casas/venta/mendoza/"),
        "3": (
            "Pilar",
            "https://inmuebles.mercadolibre.com.ar/casas/venta/bsas-gba-norte/pilar/",
        ),
        "4": ("Custom", None),
    }

    print("\nCiudades predefinidas:")
    for key, (nombre, url) in urls_ejemplo.items():
        print(f"{key}. {nombre}")

    opcion = input("\nSelecciona una opción (o escribe la URL completa): ")

    if opcion in urls_ejemplo:
        if opcion == "4":
            url = input("Ingresa la URL completa: ")
        else:
            nombre, url = urls_ejemplo[opcion]
            print(f"\nDebuggeando: {nombre}")
    else:
        url = opcion

    debug_ciudad(url)


if __name__ == "__main__":
    main()
