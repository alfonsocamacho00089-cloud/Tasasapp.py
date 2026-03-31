import requests
import json
import os
from pyDolarVenezuela import Monitor

def obtener_yadio():
    url = "https://api.yadio.io/json/VES"
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            return response.json()['USD']['price']
    except:
        return None
    return None

def actualizar_todo():
    data = {}
    
    # Obtenemos los monitores (BCV, Paralelo, etc.)
    try:
        monitor = Monitor()
        monitores = monitor.get_all_monitors()
        for k, v in monitores.items():
            data[k] = v.to_dict() if hasattr(v, 'to_dict') else v
    except Exception as e:
        print(f"Error en Monitor: {e}")

    # Agregamos Yadio siempre que responda la API
    precio_yadio = obtener_yadio()
    if precio_yadio:
        data['yadio_api'] = {"title": "Yadio API", "price": precio_yadio}

    # GUARDADO FORZOSO
    if data:
        ruta = os.path.join(os.getcwd(), 'tasas.json')
        with open(ruta, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"✅ Archivo tasas.json escrito con {len(data)} monitores.")
    else:
        print("❌ No se obtuvieron datos.")

if __name__ == "__main__":
    actualizar_todo()
