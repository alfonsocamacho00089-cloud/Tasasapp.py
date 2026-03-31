import requests
import json
import os
from pyDolarVenezuela import Monitor

def actualizar_todo():
    data = {}

    # 1. Intentar Yadio (Que sabemos que te funcionaba antes)
    try:
        url = "https://api.yadio.io/json/VES"
        res = requests.get(url, timeout=10)
        if res.status_code == 200:
            data['yadio_api'] = {
                "title": "Yadio API",
                "price": res.json()['USD']['price']
            }
            print("✅ Yadio cargado.")
    except Exception as e:
        print(f"⚠️ Error en Yadio: {e}")

    # 2. Intentar Monitor (El que está dando problemas)
    try:
        # Ponemos un try/except muy cerrado aquí para que no rompa el script
        monitor = Monitor()
        monitores = monitor.get_all_monitors()
        for k, v in monitores.items():
            data[k] = v.to_dict() if hasattr(v, 'to_dict') else v
        print("✅ Monitor Venezuela cargado.")
    except Exception as e:
        print(f"❌ Falló Monitor Venezuela pero seguiremos adelante: {e}")

    # 3. Guardar SIEMPRE lo que hayamos conseguido
    if data:
        with open('tasas.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print("💾 Archivo guardado con éxito.")
    else:
        print("🚫 No se pudo obtener ninguna información.")

if __name__ == "__main__":
    actualizar_todo()
