"""
Configuración del scraper
Contiene URLs, headers y constantes
"""

import random

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
]


def obtener_headers_aleatorios():
    """Genera un conjunto de headers aleatorios"""
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "es-ES,es;q=0.5",
    }


# Headers por defecto (se usarán si no se especifica rotación)
HEADERS = obtener_headers_aleatorios()


# Delays aleatorios
def obtener_delay_aleatorio(min_seg, max_seg):
    """Genera un delay aleatorio entre min y max segundos"""
    return random.uniform(min_seg, max_seg)


# Configuración de delays
DELAY_ENTRE_PAGINAS_MIN = 2
DELAY_ENTRE_PAGINAS_MAX = 4
DELAY_ENTRE_CIUDADES_MIN = 3
DELAY_ENTRE_CIUDADES_MAX = 6
DELAY_RETRY_MIN = 5
DELAY_RETRY_MAX = 10

# Configuración de scraping
PAGINAS_POR_CIUDAD = 2
MAX_REINTENTOS = 3  # Intentos con diferentes headers si falla# Estructura jerárquica: zona -> ciudades -> URL

UBICACIONES = {
    "GBA Norte": {
        "Pilar": "https://inmuebles.mercadolibre.com.ar/casas/venta/bsas-gba-norte/pilar/",
        "Escobar": "https://inmuebles.mercadolibre.com.ar/casas/venta/bsas-gba-norte/escobar/",
        "Tigre": "https://inmuebles.mercadolibre.com.ar/casas/venta/bsas-gba-norte/tigre/",
        "San Isidro": "https://inmuebles.mercadolibre.com.ar/casas/venta/bsas-gba-norte/san-isidro/",
        "San Miguel": "https://inmuebles.mercadolibre.com.ar/casas/venta/bsas-gba-norte/san-miguel/",
        "General San Martin": "https://inmuebles.mercadolibre.com.ar/casas/venta/bsas-gba-norte/general-san-martin/",
        "Vicente Lopez": "https://inmuebles.mercadolibre.com.ar/casas/venta/bsas-gba-norte/vicente-lopez/",
        "Malvinas Argentina": "https://inmuebles.mercadolibre.com.ar/casas/venta/bsas-gba-norte/malvinas-argentina/",
        "San Fernando": "https://inmuebles.mercadolibre.com.ar/casas/venta/bsas-gba-norte/san-fernando/",
    },
    "GBA Oeste": {
        "La Matanza": "https://inmuebles.mercadolibre.com.ar/casas/venta/bsas-gba-oeste/la-matanza/",
        "Moron": "https://inmuebles.mercadolibre.com.ar/casas/venta/bsas-gba-oeste/moron/",
        "Ituzaingo": "https://inmuebles.mercadolibre.com.ar/casas/venta/bsas-gba-oeste/ituzaingo/",
        "Moreno": "https://inmuebles.mercadolibre.com.ar/casas/venta/bsas-gba-oeste/moreno/",
        "Merlo": "https://inmuebles.mercadolibre.com.ar/casas/venta/bsas-gba-oeste/merlo/",
        "Castelar": "https://inmuebles.mercadolibre.com.ar/casas/venta/bsas-gba-oeste/castelar/",
        "Tres de Febrero": "https://inmuebles.mercadolibre.com.ar/casas/venta/bsas-gba-oeste/tres-de-febrero/",
        "Hurlingham": "https://inmuebles.mercadolibre.com.ar/casas/venta/bsas-gba-oeste/hurlingham/",
    },
    "GBA Sur": {
        "La Plata": "https://inmuebles.mercadolibre.com.ar/casas/venta/bsas-gba-sur/la-plata/",
        "Esteban Echeverria": "https://inmuebles.mercadolibre.com.ar/casas/venta/bsas-gba-sur/esteban-echeverria/",
        "Quilmes": "https://inmuebles.mercadolibre.com.ar/casas/venta/bsas-gba-sur/quilmes/",
        "Lomas de Zamora": "https://inmuebles.mercadolibre.com.ar/casas/venta/bsas-gba-sur/lomas-de-zamora/",
        "Ezeiza": "https://inmuebles.mercadolibre.com.ar/casas/venta/bsas-gba-sur/ezeiza/",
        "Berazategui": "https://inmuebles.mercadolibre.com.ar/casas/venta/bsas-gba-sur/berazategui/",
        "Lanus": "https://inmuebles.mercadolibre.com.ar/casas/venta/bsas-gba-sur/lanus/",
        "Almirante Brown": "https://inmuebles.mercadolibre.com.ar/casas/venta/bsas-gba-sur/almirante-brown/",
        "Avellaneda": "https://inmuebles.mercadolibre.com.ar/casas/venta/bsas-gba-sur/avellaneda/",
    },
    "Córdoba": {
        "Córdoba": "https://inmuebles.mercadolibre.com.ar/casas/venta/cordoba/cordoba/",
        "Punilla": "https://inmuebles.mercadolibre.com.ar/casas/venta/cordoba/punilla/",
        "Colon": "https://inmuebles.mercadolibre.com.ar/casas/venta/cordoba/colon/",
        "Villa Carlos Paz": "https://inmuebles.mercadolibre.com.ar/casas/venta/cordoba/villa-carlos-paz/",
        "Santa Maria": "https://inmuebles.mercadolibre.com.ar/casas/venta/cordoba/santa-maria/",
    },
    "Costa Atlántica": {
        "Mar del Plata": "https://inmuebles.mercadolibre.com.ar/casas/venta/bsas-costa-atlantica/mar-del-plata/",
        "Costa Esmeralda": "https://inmuebles.mercadolibre.com.ar/casas/venta/bsas-costa-atlantica/costa-esmeralda/",
        "Pinamar": "https://inmuebles.mercadolibre.com.ar/casas/venta/bsas-costa-atlantica/pinamar/",
        "Mar del Tuyu": "https://inmuebles.mercadolibre.com.ar/casas/venta/bsas-costa-atlantica/mar-del-tuyu/",
        "Villa Gesell": "https://inmuebles.mercadolibre.com.ar/casas/venta/bsas-costa-atlantica/villa-gesell/",
        "Mar de Ajo": "https://inmuebles.mercadolibre.com.ar/casas/venta/bsas-costa-atlantica/mar-de-ajo/",
    },
    "Buenos Aires Interior": {
        "Lujan": "https://inmuebles.mercadolibre.com.ar/casas/venta/venta/buenos-aires-interior/lujan/",
        "San Vicente": "https://inmuebles.mercadolibre.com.ar/casas/venta/venta/buenos-aires-interior/san-vicente/",
    },
}

# Límites de validación
LIMITES = {
    "ambientes": {"min": 1, "max": 20},
    "banos": {"min": 1, "max": 10},
    "metros": {"min": 20, "max": 5000},
    "precio": {"min": 10000, "max": 10000000},
}
