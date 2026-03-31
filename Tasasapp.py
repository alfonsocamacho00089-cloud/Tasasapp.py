import requests
import json
import datetime
from pyDolarVenezuela.pages import Monitor

# Mantenemos tus headers por seguridad
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    "Content-Type": "application/json"
}

def obtener_yadio_manual():
    """Tu función original de Yadio como respaldo"""
    url = "https://api.yadio.io/json/VES"
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            return response.json()['USD']['price']
        return None
    except:
        return None

def actualizar_todo():
    resultado_final = {}
    
    # 1. Intentar obtener todo vía pyDolarVenezuela
    try:
        monitor = Monitor()
        data_pydolar = monitor.get_all_monitors()
        
        # Mapeamos los datos que nos interesan de la librería
        for key, info in data_pydolar.items():
            resultado_final[key] = {
                "title": info.get('title'),
                "price": info.get('price'),
                "last_update": info.get('last_update')
            }
    except Exception as e:
        print(f"⚠️ pyDolarVenezuela falló: {e}")

    # 2. Refuerzo de Yadio (Si no está en pyDolar o para asegurar actualización)
    precio_yadio = obtener_yadio_manual()
    if precio_yadio:
        resultado_final["yadio"] = {
            "title": "Yadio API",
            "price": precio_yadio,
            "last_update": datetime.datetime.now().strftime("%I:%M %p")
        }

    # 3. Guardar en tasas.json
    try:
        with open('tasas.json', 'w', encoding='utf-8') as f:
            json.dump(resultado_final, f, indent=4, ensure_ascii=False)
        print("✅ Archivo 'tasas.json' actualizado con éxito.")
    except Exception as e:
        print(f"❌ Error al escribir el archivo: {e}")

if __name__ == "__main__":
    actualizar_todo()
