import requests
import json
from pyDolarVenezuela.providers  # Importación específica del objeto
import monitor
def obtener_yadio_manual():
    url = "https://api.yadio.io/json/VES"
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            res_json = response.json()
            return res_json['USD']['rate'] 
        return None
    except Exception as e:
        print(f"⚠️ Error manual en Yadio: {e}")
        return None

def actualizar_todo():
    datos_finales = {}
    
    # 1. Intentar pyDolarVenezuela con el OBJETO CriptoDolar
    try:
        print("Intentando cargar pyDolarVenezuela...")
        # Aquí le pasamos el objeto importado, NO un string
        monitor = Monitor(CriptoDolar) 
        datos_pydolar = monitor.get_all_monitors()
        
        if datos_pydolar:
            datos_finales = datos_pydolar
            print("✅ pyDolarVenezuela cargado con éxito.")
    except Exception as e:
        # Aquí verás si falta algún otro argumento o si la página está caída
        print(f"❌ Error crítico en pyDolarVenezuela: {e}")

    # 2. Obtener Yadio (Tu respaldo)
    yadio_rate = obtener_yadio_manual()
    
    if yadio_rate:
        datos_finales["yadio"] = {
            "title": "Yadio API",
            "price": yadio_rate
        }
        print(f"✅ Yadio cargado: {yadio_rate}")

    # 3. Guardar el archivo
    try:
        with open('tasas.json', 'w', encoding='utf-8') as f:
            json.dump(datos_finales, f, indent=4, ensure_ascii=False)
        print("💾 Archivo 'tasas.json' actualizado.")
    except Exception as e:
        print(f"❌ Error al escribir el JSON: {e}")

if __name__ == "__main__":
    actualizar_todo()
