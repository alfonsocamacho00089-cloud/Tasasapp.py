import requests
import json
from pyDolarVenezuela import Monitor

def obtener_yadio_manual():
    url = "https://api.yadio.io/json/VES"
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            res_json = response.json()
            # Cambiado a 'rate' según tu corrección
            return res_json['USD']['rate'] 
        return None
    except Exception as e:
        print(f"⚠️ Error manual en Yadio: {e}")
        return None

def actualizar_todo():
    datos_finales = {}
    
    # 1. Intentar pyDolarVenezuela con reporte de error
    try:
        print("Intentando cargar pyDolarVenezuela...")
        monitor = Monitor()
        datos_pydolar = monitor.get_all_monitors()
        if datos_pydolar:
            datos_finales = datos_pydolar
            print("✅ pyDolarVenezuela cargado con éxito.")
    except Exception as e:
        # Esto te dirá en el log de GitHub por qué falló (falta de librería, error de red, etc.)
        print(f"❌ Error crítico en pyDolarVenezuela: {e}")

    # 2. Obtener Yadio (Tu lógica que ya probaste)
    yadio_rate = obtener_yadio_manual()
    
    if yadio_rate:
        # Lo insertamos o sobrescribimos en el diccionario
        datos_finales["yadio"] = {
            "title": "Yadio API",
            "price": yadio_rate  # Guardamos como 'price' para mantener consistencia en tu JSON
        }
        print(f"✅ Yadio cargado: {yadio_rate}")
    else:
        print("⚠️ No se pudo obtener el dato de Yadio.")

    # 3. Guardar el archivo pase lo que pase
    if datos_finales:
        try:
            with open('tasas.json', 'w', encoding='utf-8') as f:
                json.dump(datos_finales, f, indent=4, ensure_ascii=False)
            print("💾 Archivo 'tasas.json' actualizado.")
        except Exception as e:
            print(f"❌ Error al escribir el JSON: {e}")
    else:
        print("🚫 No hay datos para guardar. El JSON no se actualizó.")

if __name__ == "__main__":
    actualizar_todo()
