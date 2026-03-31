import requests
import json

def obtener_bybit():
    url = "https://api2.bybit.com/fiat/otc/item/list"
    payload = {
        "tokenId": "USDT",
        "currencyId": "VES",
        "payment": ["Banesco"],
        "side": "1",
        "size": "1",
        "page": "1"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=20)
        if response.status_code == 200:
            res_json = response.json()
            items = res_json.get('result', {}).get('items', [])
            if items:
                return items[0]['price']
    except:
        return None
    return None

def obtener_yadio():
    url = "https://api.yadio.io/json/VES"
    try:
        response = requests.get(url, timeout=20)
        if response.status_code == 200:
            res_json = response.json()
            # Usamos 'rate' que es el que te funcionó
            return res_json.get('USD', {}).get('rate')
    except:
        return None
    return None

def actualizar_todo():
    datos_finales = {}
    
    # 1. Obtener Bybit
    precio_bybit = obtener_bybit()
    if precio_bybit:
        datos_finales["bybit"] = {"title": "Bybit P2P", "price": precio_bybit}
        print(f"✅ Bybit cargado: {precio_bybit}")

    # 2. Obtener Yadio
    precio_yadio = obtener_yadio()
    if precio_yadio:
        datos_finales["yadio"] = {"title": "Yadio API", "price": precio_yadio}
        print(f"✅ Yadio cargado: {precio_yadio}")

    # 3. Guardar el archivo tasas.json
    if datos_finales:
        try:
            with open('tasas.json', 'w', encoding='utf-8') as f:
                json.dump(datos_finales, f, indent=4, ensure_ascii=False)
            print("💾 Archivo 'tasas.json' actualizado con éxito.")
        except Exception as e:
            print(f"❌ Error al escribir el archivo: {e}")
    else:
        print("🚫 No se pudo obtener ninguna tasa, el archivo no se actualizó.")

if __name__ == "__main__":
    actualizar_todo()
