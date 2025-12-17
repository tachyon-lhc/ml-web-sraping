import requests
import time

HEADERS_BASICOS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}

HEADERS_COMPLETOS = {
    "user-agent": "mozilla/5.0 (x11; linux x86_64) applewebkit/537.36 (khtml, like gecko) chrome/120.0.0.0 safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "accept-language": "es-es,es;q=0.5",
    "accept-encoding": "gzip, deflate, br, zstd",
    "connection": "keep-alive",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-site",
}

url = "https://inmuebles.mercadolibre.com.ar/casas/venta/bsas-gba-oeste/moron/"

print("Probando con headers básicos...")
r1 = requests.get(url, headers=HEADERS_BASICOS)
tiene_login_1 = "inicia sesión" in r1.text.lower() or "login" in r1.text.lower()
print(f"Status: {r1.status_code}")
print(f"Requiere login: {tiene_login_1}")
print(f"Tamaño HTML: {len(r1.text)}")

time.sleep(3)

print("\nProbando con headers completos...")
r2 = requests.get(url, headers=HEADERS_COMPLETOS)
tiene_login_2 = "inicia sesión" in r2.text.lower() or "login" in r2.text.lower()
print(f"Status: {r2.status_code}")
print(f"Requiere login: {tiene_login_2}")
print(f"Tamaño HTML: {len(r2.text)}")

time.sleep(3)

print("\nProbando con sesión + warmup...")
session = requests.Session()
session.headers.update(HEADERS_COMPLETOS)
session.get("https://www.mercadolibre.com.ar")
time.sleep(2)
r3 = session.get(url)
tiene_login_3 = "inicia sesión" in r3.text.lower() or "login" in r3.text.lower()
print(f"Status: {r3.status_code}")
print(f"Requiere login: {tiene_login_3}")
print(f"Tamaño HTML: {len(r3.text)}")
