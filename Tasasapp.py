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
        # Bybit a veces se pone pesado, intentamos con un timeout largo
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        if response.status_code == 200:
            items = response.json().get('result', {}).get('items', [])
            if items:
                return items[0]['price']
        return None
    except:
        return None

def obtener_datos_yadio():
    # Yadio tiene una API que da TODO: P2P, BCV y Paralelo
    url = "https://api.yadio.io/json/VES"
    try:
        response = requests.get(url, timeout=25)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def actualizar_todo():
    datos_finales = {}
    
    # 1. Intentar Bybit
    p_bybit = obtener_bybit()
    if p_bybit:
        datos_finales["bybit"] = {"title": "Bybit P2P", "price": float(p_bybit)}
        print(f"✅ Bybit: {p_bybit}")

    # 2. Intentar Yadio (Trae todo)
    yadio_data = obtener_datos_yadio()
    if yadio_data:
        # Guardamos el Yadio normal que ya usabas
        datos_finales["yadio"] = {"title": "Yadio API", "price": yadio_data['USD']['rate']}
        
        # AGREGAMOS BCV Y PARALELO DESDE YADIO (Para no extrañar a pyDolar)
        datos_finales["bcv"] = {"title": "Banco Central", "price": yadio_data['dtp']['bcv']['price']}
        datos_finales["enparalelovzla"] = {"title": "EnParaleloVzla", "price": yadio_data['dtp']['ppub']['price']}
        
        print(f"✅ Yadio y Tasas BCV/Paralelo cargadas.")

    # 3. Guardar el archivo
    if datos_finales:
        with open('tasas.json', 'w', encoding='utf-8') as f:
            json.dump(datos_finales, f, indent=4, ensure_ascii=False)
        print("💾 tasas.json actualizado con éxito.")

if __name__ == "__main__":
    actualizar_todo()
