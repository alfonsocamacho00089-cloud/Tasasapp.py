import requests
import json
import datetime

# Configuración de Headers para evitar bloqueos
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    "Content-Type": "application/json",
    "Referer": "https://m.bybit.com/",
    "Origin": "https://m.bybit.com"
}

def obtener_bybit():
def obtener_bybit():
    # Nueva URL para peticiones GET (más estable)
    url = "https://api2.bybit.com/fiat/otc/item/list"
    
    # Parámetros para la URL
    params = {
        "tokenId": "USDT",
        "currencyId": "VES",
        "payment": "9", # 9 suele ser el ID de Banesco en Bybit
        "side": "1",
        "size": "1",
        "page": "1",
        "authMaker": "false",
        "canTrade": "false"
    }
    
    try:
        # Cambiamos .post por .get
        response = requests.get(url, params=params, headers=HEADERS, timeout=15)
        
        if response.status_code == 200:
            res_json = response.json()
            # Accedemos a la estructura de la respuesta
            return res_json['result']['items'][0]['price']
        
        return f"Error Bybit: {response.status_code}"
    except Exception as e:
        return f"Sin señal Bybit: {e}"
    try:
        # Bybit suele usar POST o GET según la versión de API, esta es la de su web
        response = requests.post(url, json=payload, headers=HEADERS, timeout=15)
        if response.status_code == 200:
            res_json = response.json()
            return res_json['result']['items'][0]['price']
        return f"Error Bybit: {response.status_code}"
    except Exception as e:
        return f"Sin señal Bybit: {e}"

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
