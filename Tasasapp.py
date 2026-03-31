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
    # INTENTO 1: Buscar Bybit en la API de PyDolar (Datos en vivo)
    try:
        url1 = "https://pydolarvenezuela-api.vercel.app/api/v1/dollar?page=cripto"
        res = requests.get(url1, timeout=10)
        if res.status_code == 200:
            monedas = res.json().get('monedas', {})
            if 'bybit' in monedas: 
                return monedas['bybit']['price']
    except:
        pass

    # INTENTO 2: Si Bybit falla, buscar Binance (que es el gemelo de Bybit)
    try:
        # Usamos el puente de Yadio para sacar Binance en vivo
        url2 = "https://api.yadio.io/exchanges/binance/ves"
        res2 = requests.get(url2, timeout=10)
        if res2.status_code == 200:
            return res2.json()['price']
    except:
        pass

    # INTENTO 3: Si todo lo anterior falla, usamos el promedio de Cripto en vivo
    try:
        url3 = "https://api.yadio.io/exchanges/ves"
        res3 = requests.get(url3, timeout=10)
        # Sacamos el promedio de todos los exchanges cripto
        return res3.json()['cryptodolar']['price']
    except:
        return "Error: Sin conexión real"
        
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
