import requests
import json

def obtener_binance():
    url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
    payload = {
        "asset": "USDT",
        "fiat": "VES",
        "merchantCheck": False,
        "page": 1,
        "payTypes": ["Banesco"],
        "publisherType": None,
        "rows": 1,
        "tradeType": "SELL" # SELL en la API muestra el precio al que tú compras
    }
    try:
        response = requests.post(url, json=payload, timeout=20)
        if response.status_code == 200:
            res_json = response.json()
            return res_json['data'][0]['adv']['price']
    except: return None
    return None

def obtener_bybit():
    url = "https://api2.bybit.com/fiat/otc/item/list"
    payload = {"tokenId": "USDT", "currencyId": "VES", "payment": ["Banesco"], "side": "1", "size": "1", "page": "1"}
    headers = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"}
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=20)
        if response.status_code == 200:
            items = response.json().get('result', {}).get('items', [])
            if items: return items[0]['price']
    except: return None
    return None

def obtener_yadio():
    url = "https://api.yadio.io/json/VES"
    try:
        response = requests.get(url, timeout=20)
        if response.status_code == 200:
            return response.json().get('USD', {}).get('rate')
    except: return None
    return None

def actualizar_todo():
    datos_finales = {}
    
    # Intentar obtener las 3
    p_binance = obtener_binance()
    p_bybit = obtener_bybit()
    p_yadio = obtener_yadio()

    if p_binance:
        datos_finales["binance"] = {"title": "Binance P2P", "price": float(p_binance)}
        print(f"✅ Binance: {p_binance}")

    if p_bybit:
        datos_finales["bybit"] = {"title": "Bybit P2P", "price": float(p_bybit)}
        print(f"✅ Bybit: {p_bybit}")

    if p_yadio:
        datos_finales["yadio"] = {"title": "Yadio API", "price": float(p_yadio)}
        print(f"✅ Yadio: {p_yadio}")

    # Guardar si hay algo
    if datos_finales:
        with open('tasas.json', 'w', encoding='utf-8') as f:
            json.dump(datos_finales, f, indent=4, ensure_ascii=False)
        print("💾 tasas.json actualizado con el Trío P2P.")

if __name__ == "__main__":
    actualizar_todo()
