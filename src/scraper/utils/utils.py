"""
Funciones auxiliares para validación y extracción de datos
"""

import re


def es_valor_exacto(texto):
    """
    Determina si un texto representa un valor exacto o un rango.

    Args:
        texto: string con el valor a validar

    Returns:
        bool: True si es exacto, False si es rango o inválido
    """
    if not texto:
        return False

    # Detectar rangos ("1 a 3")
    if " a " in texto.lower():
        return False

    # Contar números en el texto
    numeros = re.findall(r"\d+", texto)

    # Más de un número indica rango
    if len(numeros) > 1:
        return False

    # Un solo número es válido
    if len(numeros) == 1:
        return True

    # Caso especial: monoambiente sin número
    if "mono" in texto.lower() and len(numeros) == 0:
        return True

    return False


def extraer_numero(texto):
    """
    Extrae el número de un texto limpio.

    Args:
        texto: string con el valor

    Returns:
        int o None: número extraído
    """
    if not texto:
        return None

    # Caso especial: monoambiente
    if "mono" in texto.lower():
        return 1

    # Extraer primer número encontrado
    match = re.search(r"\d+", texto)
    if match:
        return int(match.group())

    return None


def validar_rango(valor, campo, limites):
    """
    Valida que un valor esté dentro de un rango razonable.

    Args:
        valor: número a validar
        campo: nombre del campo ('ambientes', 'banos', etc.)
        limites: diccionario con límites por campo

    Returns:
        bool: True si es válido, False si no
    """
    if not valor:
        return False

    if campo not in limites:
        return True

    min_val = limites[campo]["min"]
    max_val = limites[campo]["max"]

    return min_val <= valor <= max_val


def limpiar_precio(precio_texto):
    """
    Convierte precio de string a número entero.

    Args:
        precio_texto: string con el precio (ej: "100.000")

    Returns:
        int o None: precio como número
    """
    if not precio_texto:
        return None

    try:
        # Quitar puntos y comas
        precio_limpio = precio_texto.replace(".", "").replace(",", "")
        return int(precio_limpio)
    except (ValueError, AttributeError):
        return None


def construir_url_pagina(url_base, numero_pagina):
    """
    Construye la URL de una página específica.

    Args:
        url_base: URL base de la ciudad
        numero_pagina: número de página (1, 2, 3...)

    Returns:
        string: URL completa con paginación
    """
    if numero_pagina == 1:
        return url_base
    else:
        desde = (numero_pagina - 1) * 50 + 1
        return url_base.rstrip("/") + f"_Desde_{desde}"
