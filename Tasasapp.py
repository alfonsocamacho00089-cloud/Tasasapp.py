import requests
import json
import datetime


# Lista de diferentes identidades (Headers) para probar
LISTA_HEADERS = [
    {   # Identidad 1: Navegador Chrome estándar
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Referer": "https://www.bybit.com/fiat/trade/otc/USDT/VES/item-list",
        "Origin": "https://www.bybit.com"
    },
    {   # Identidad 2: Navegador Firefox (a veces más permisivo)
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
        "Accept": "application/json",
        "Referer": "https://www.bybit.com/"
    },
    {   # Identidad 3: Simulación de App Móvil (La más "guerrera")
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1",
        "Referer": "https://m.bybit.com/",
        "Origin": "https://m.bybit.com"
    }
]
def obtener_bybit():
    # INTENTO 1: PyDolar (La más completa)
    try:
        url1 = "https://pydolarvenezuela-api.vercel.app/api/v1/dollar?page=cripto"
        res1 = requests.get(url1, timeout=10)
        if res1.status_code == 200:
            datos = res1.json()
            # Buscamos Bybit, si no Binance (que es el mismo precio)
            monedas = datos.get('monedas', {})
            if 'bybit' in monedas: return monedas['bybit']['price']
            if 'binance' in monedas: return monedas['binance']['price']
    except:
        pass # Si falla, salta al siguiente

    # INTENTO 2: Exchangemonitor (Directo al grano)
    try:
        url2 = "https://p2p.exchangemonitor.net/api/v1/get/bybit/ves"
        res2 = requests.get(url2, timeout=10)
        if res2.status_code == 200:
            return res2.json().get('price')
    except:
        pass

    # INTENTO 3: Yadio Exchanges (La vieja confiable)
    try:
        url3 = "https://api.yadio.io/exchanges/ves"
        res3 = requests.get(url3, timeout=10)
        if res3.status_code == 200:
            datos3 = res3.json()
            if 'bybit' in datos3: return datos3['bybit']['price']
    except:
        pass

    # SI TODO FALLA: Usamos el precio de Yadio General para no dejar el hueco
    try:
        res_final = requests.get("https://api.yadio.io/json/VES", timeout=10)
        return res_final.json()['USD']['rate']
    except:
        return "655.80" # Un valor de emergencia por si el internet explota
def obtener_yadio():
    # Yadio es más directo y no requiere payload complejo
    url = "https://api.yadio.io/json/VES"
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            res_json = response.json()
            # Usamos el precio de USDT
            return res_json['USD']['rate']
        return f"Error Yadio: {response.status_code}"
    except Exception as e:
        return f"Sin señal Yadio: {e}"

# --- EJECUCIÓN ---

precio_bybit = obtener_bybit()
precio_yadio = obtener_yadio()

# Estructura del resultado
resultado = [
    {"bank": "Bybit P2P", "precio": precio_bybit},
    {"bank": "Yadio API", "precio": precio_yadio}
]

# Guardar en tasas.json
with open("tasas.json", "w") as f:
    json.dump(resultado, f, indent=4)

print(f"Actualizado con éxito: Bybit: {precio_bybit} | Yadio: {precio_yadio}")
