"""
Sistema de reintentos con rotación de headers
"""

import time
from ..config.config import (
    obtener_headers_aleatorios,
    obtener_delay_aleatorio,
    DELAY_RETRY_MIN,
    DELAY_RETRY_MAX,
    MAX_REINTENTOS,
)


class RetryManager:
    """
    Maneja reintentos inteligentes con rotación de headers
    """

    def __init__(self):
        self.intentos_por_ciudad = {}
        self.ciudades_fallidas = []

    def intentar_scraping(self, func_scraping, zona, ciudad, *args, **kwargs):
        """
        Intenta scrapear una ciudad con múltiples estrategias.

        Args:
            func_scraping: función de scraping a ejecutar
            zona: nombre de la zona
            ciudad: nombre de la ciudad
            *args, **kwargs: argumentos para la función

        Returns:
            lista de propiedades (vacía si falló todos los intentos)
        """
        ciudad_key = f"{zona} - {ciudad}"

        for intento in range(1, MAX_REINTENTOS + 1):
            print(f"    Intento {intento}/{MAX_REINTENTOS}")

            # Rotar headers en cada intento
            headers_actuales = obtener_headers_aleatorios()
            kwargs["headers"] = headers_actuales

            # Ejecutar scraping
            propiedades = func_scraping(*args, **kwargs)

            # Si encontró propiedades, éxito
            if len(propiedades) > 0:
                print(f"    ✓ Éxito con {len(propiedades)} propiedades")
                return propiedades

            # Si no encontró nada y quedan intentos
            if intento < MAX_REINTENTOS:
                delay = obtener_delay_aleatorio(DELAY_RETRY_MIN, DELAY_RETRY_MAX)
                print(
                    f"    ⚠ 0 propiedades. Reintentando en {delay:.1f}s con nuevos headers..."
                )
                time.sleep(delay)

        # Todos los intentos fallaron
        print(f"    ✗ Falló después de {MAX_REINTENTOS} intentos")
        self.ciudades_fallidas.append(ciudad_key)
        return []

    def obtener_ciudades_fallidas(self):
        """Retorna lista de ciudades que fallaron todos los intentos"""
        return self.ciudades_fallidas

    def hay_ciudades_fallidas(self):
        """Verifica si hay ciudades que fallaron"""
        return len(self.ciudades_fallidas) > 0
