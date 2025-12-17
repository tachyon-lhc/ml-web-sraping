"""
Lógica principal del scraper
"""

import requests
from bs4 import BeautifulSoup
import time


from config.config import (
    obtener_headers_aleatorios,
    obtener_delay_aleatorio,
    LIMITES,
    DELAY_ENTRE_PAGINAS_MIN,
    DELAY_ENTRE_PAGINAS_MAX,
    DELAY_ENTRE_CIUDADES_MIN,
    DELAY_ENTRE_CIUDADES_MAX,
)

from utils.utils import (
    es_valor_exacto,
    extraer_numero,
    validar_rango,
    limpiar_precio,
    construir_url_pagina,
)


import random


def obtener_html(url, headers=None):
    """
    Hace una petición HTTP GET y retorna el HTML.

    Args:
        url: string con la URL a consultar
        headers: dict con headers (si None, usa aleatorios)

    Returns:
        string con HTML o None si hubo error
    """
    if headers is None:
        headers = obtener_headers_aleatorios()

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            return response.text
        else:
            print(f"  Error HTTP: {response.status_code}")
            return None

    except requests.RequestException as e:
        print(f"  Error de conexión: {e}")
        return None


def extraer_propiedad(card, zona, ciudad):
    """
    Extrae datos de UNA propiedad desde su card HTML.

    Args:
        card: objeto BeautifulSoup con el div de la propiedad
        zona: string con la zona
        ciudad: string con la ciudad

    Returns:
        dict con los datos o None si no es válida
    """

    # Extraer título
    titulo_elem = card.find("h2", class_="poly-component__title-wrapper")
    titulo = titulo_elem.text.strip() if titulo_elem else None

    if not titulo:
        return None

    # Extraer precio
    precio_texto = None
    contenedor_precio = card.find("div", class_="poly-component__price")
    if contenedor_precio:
        precio_elem = contenedor_precio.find(
            "span", class_="andes-money-amount__fraction"
        )
        if precio_elem:
            precio_texto = precio_elem.text.strip()

    precio = limpiar_precio(precio_texto)
    if not precio or not validar_rango(precio, "precio", LIMITES):
        return None

    # Extraer atributos
    ambientes_raw = None
    banos_raw = None
    metros_raw = None

    contenedor_atributos = card.find("div", class_="poly-component__attributes-list")
    if contenedor_atributos:
        lista = contenedor_atributos.find("ul", class_="poly-attributes_list")
        if lista:
            items = lista.find_all("li", class_="poly-attributes_list__item")

            for item in items:
                texto = item.text.strip()

                if "amb" in texto.lower() or "dormitorio" in texto.lower():
                    ambientes_raw = texto
                elif "baño" in texto.lower():
                    banos_raw = texto
                elif "m²" in texto or "m2" in texto:
                    metros_raw = texto

    # Validar que sean valores exactos (no rangos)
    if not es_valor_exacto(ambientes_raw):
        return None
    if not es_valor_exacto(banos_raw):
        return None
    if not metros_raw:
        return None

    # Extraer números
    ambientes = extraer_numero(ambientes_raw)
    banos = extraer_numero(banos_raw)
    metros = extraer_numero(metros_raw)

    # Validar rangos razonables
    if not validar_rango(ambientes, "ambientes", LIMITES):
        return None
    if not validar_rango(banos, "banos", LIMITES):
        return None
    if not validar_rango(metros, "metros", LIMITES):
        return None

    return {
        "titulo": titulo,
        "precio": precio,
        "ambientes": ambientes,
        "banos": banos,
        "metros": metros,
        "zona": zona,
        "ciudad": ciudad,
    }


def extraer_pagina(html, zona, ciudad):
    """
    Extrae todas las propiedades de una página HTML.

    Args:
        html: string con el HTML completo
        zona: string con la zona
        ciudad: string con la ciudad

    Returns:
        tuple: (lista de propiedades, cantidad descartada)
    """
    soup = BeautifulSoup(html, "html.parser")
    cards = soup.find_all("div", class_="poly-card__content")

    propiedades = []
    descartadas = 0

    for card in cards:
        propiedad = extraer_propiedad(card, zona, ciudad)

        if propiedad:
            propiedades.append(propiedad)
        else:
            descartadas += 1

    return propiedades, descartadas


def scrapear_ciudad(zona, ciudad, url_base, num_paginas, headers=None):
    """
    Scrapea múltiples páginas de una ciudad.

    Args:
        zona: string con la zona
        ciudad: string con la ciudad
        url_base: URL base de la ciudad
        num_paginas: cantidad máxima de páginas a scrapear
        headers: dict con headers (si None, usa aleatorios)

    Returns:
        lista con todas las propiedades de la ciudad
    """
    propiedades_ciudad = []

    for pagina in range(1, num_paginas + 1):
        url = construir_url_pagina(url_base, pagina)

        html = obtener_html(url, headers)
        if not html:
            break

        propiedades, descartadas = extraer_pagina(html, zona, ciudad)
        propiedades_ciudad.extend(propiedades)

        print(
            f"    Página {pagina}: {len(propiedades)} válidas, {descartadas} descartadas"
        )

        # Si hay menos de 20, probablemente no hay más páginas
        if len(propiedades) < 20:
            break

        # Delay aleatorio entre páginas
        delay = obtener_delay_aleatorio(
            DELAY_ENTRE_PAGINAS_MIN, DELAY_ENTRE_PAGINAS_MAX
        )
        time.sleep(delay)

    return propiedades_ciudad


def scrapear_todo(ubicaciones, paginas_por_ciudad):
    from retry_manager import RetryManager

    todas_propiedades = []
    stats_ciudades = {}
    retry_manager = RetryManager()
    total_ciudades = sum(len(ciudades) for ciudades in ubicaciones.values())
    ciudad_actual = 0
    for zona, ciudades in ubicaciones.items():
        print(f"\n{'=' * 60}")
        print(f"ZONA: {zona}")
        print(f"{'=' * 60}")

        for ciudad, url in ciudades.items():
            ciudad_actual += 1
            print(f"\n[{ciudad_actual}/{total_ciudades}] {ciudad}")

            # Usar retry manager
            propiedades = retry_manager.intentar_scraping(
                scrapear_ciudad, zona, ciudad, zona, ciudad, url, paginas_por_ciudad
            )

            todas_propiedades.extend(propiedades)
            stats_ciudades[f"{zona} - {ciudad}"] = len(propiedades)

            print(f"  Total {ciudad}: {len(propiedades)}")
            print(f"  Total acumulado: {len(todas_propiedades)}")

            # Delay aleatorio entre ciudades
            delay = obtener_delay_aleatorio(
                DELAY_ENTRE_CIUDADES_MIN, DELAY_ENTRE_CIUDADES_MAX
            )
            time.sleep(delay)

    ciudades_fallidas = retry_manager.obtener_ciudades_fallidas()

    return todas_propiedades, stats_ciudades, ciudades_fallidas
