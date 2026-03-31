import requests
import json
import datetime
from pyDolarVenezuela import Monitor

# Mantener tu lógica de Yadio original como respaldo
def obtener_yadio_manual():
    url = "https://api.yadio.io/json/VES"
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            res_json = response.json()
            return res_json['USD']['price']
        return None
    except Exception:
        return None

def actualizar_todo():
    # 1. Intentar obtener todo desde pyDolarVenezuela
    try:
        monitor = Monitor()
        data_pydolar = monitor.get_all_monitors()
    except Exception as e:
        print(f"Error con pyDolarVenezuela: {e}")
        data_pydolar = {}

    # 2. Obtener Yadio con tu lógica (por si pydolar no carga o quieres asegurar ese dato)
    yadio_respaldo = obtener_yadio_manual()
    
    # 3. Construir el diccionario final para el JSON
    # Si pyDolar trae yadio, lo usamos; si no, usamos el manual
    if yadio_respaldo and "yadio" not in data_pydolar:
        data_pydolar["yadio"] = {"title": "Yadio API", "price": yadio_respaldo}
    elif yadio_respaldo:
        # Sobrescribimos el precio de yadio con tu función manual para mayor seguridad
        data_pydolar["yadio"]["price"] = yadio_respaldo

    # 4. Guardar en tasas.json con el formato que ya conoces
    try:
        with open('tasas.json', 'w', encoding='utf-8') as f:
            json.dump(data_pydolar, f, indent=4, ensure_ascii=False)
        print("✅ Tasas actualizadas correctamente en tasas.json")
    except Exception as e:
        print(f"❌ Error al escribir el archivo: {e}")

if __name__ == "__main__":
    actualizar_todo()
