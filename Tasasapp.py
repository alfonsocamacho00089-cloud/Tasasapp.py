import requests
import json

# Headers para que Bybit no bloquee la petición
HEADERS_BYBIT = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    "Content-Type": "application/json",
    "Referer": "https://m.bybit.com/",
    "Origin": "https://m.bybit.com"
}

def obtener_bybit():
    url = "https://api2.bybit.com/fiat/otc/item/list"
    payload = {
        "tokenId": "USDT",
        "currencyId": "VES",
        "payment": ["Banesco"],
        "side": "1", # 1 es vender USDT
        "size": "1",
        "page": "1"
    }
    try:
        response = requests.post(url, json=payload, headers=HEADERS_BYBIT, timeout=20)
        if response.status_code == 200:
            res_json = response.json()
            return res_json['result']['items'][0]['price']
        return None
    except Exception as e:
        print(f"⚠️ Error Bybit: {e}")
        return None

def obtener_yadio():
    url = "https://api.yadio.io/json/VES"
    try:
        response = requests.get(url, timeout=20)
        if response.status_code == 200:
            res_json = response.json()
            # Usamos 'rate' como habías verificado
            return res_json['USD']['rate']
        return None
    except Exception as e:
        print(f"⚠️ Error Yadio: {e}")
        return None

def actualizar_todo():
    datos_finales = {}

    # 1. Obtener datos
    precio_bybit = obtener_bybit()
    precio_yadio = obtener_yadio()

    # 2. Construir diccionario para el JSON
    if precio_bybit:
        datos_finales["bybit"] = {"title": "Bybit P2P", "price": precio_bybit}
        print(f"✅ Bybit: {precio_bybit}")

    if precio_yadio:
        datos_finales["yadio"] = {"title": "Yadio API", "price": precio_yadio}
        print(f"✅ Yadio: {precio_yadio}")

    # 3. Guardar solo si hay algún dato
    if datos_finales:
        try:
            with open('tasas.json', 'w', encoding='utf-8') as f:
                json.dump(datos_finales, f, indent=4, ensure_ascii=False)
            print("💾 Archivo 'tasas.json' actualizado con éxito.")
        except Exception as e:
            print(f"❌ Error al escribir: {e}")
    else:
        print("🚫 No se pudo obtener ninguna tasa.")

if __name__ == "__main__":
    actualizar_todo()
