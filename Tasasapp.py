import requests
import json
import datetime
from pyDolarVenezuela.pages import Monitor

def obtener_yadio_manual():
    """Función de respaldo que siempre se ejecutará para Yadio"""
    url = "https://api.yadio.io/json/VES"
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            return response.json()['USD']['price']
    except:
        pass
    return None

def actualizar_todo():
    resultado_final = {}
    
    # 1. Intentar obtener datos de pyDolarVenezuela
    try:
        monitor = Monitor()
        # Intentamos obtener los monitores principales
        data_pydolar = monitor.get_all_monitors()
        
        if data_pydolar:
            for key, info in data_pydolar.items():
                # Guardamos la info respetando el formato que quieres
                resultado_final[key] = {
                    "title": info.get('title', key),
                    "price": info.get('price'),
                    "last_update": info.get('last_update', '')
                }
    except Exception as e:
        print(f"Nota: pyDolar no cargó, usando respaldos: {e}")

    # 2. Tu Yadio personalizado (SIEMPRE se guarda o sobreescribe el de la librería)
    precio_yadio = obtener_yadio_manual()
    if precio_yadio:
        resultado_final["yadio"] = {
            "title": "Yadio API (Manual)",
            "price": precio_yadio,
            "last_update": datetime.datetime.now().strftime("%d/%m/%Y, %I:%M %p")
        }

    # 3. Verificación de seguridad: Si no hay nada, no sobreescribir con un archivo vacío
    if not resultado_final:
        print("❌ No se obtuvo ninguna tasa, abortando guardado para proteger datos previos.")
        return

    # 4. Guardar en tasas.json
    try:
        with open('tasas.json', 'w', encoding='utf-8') as f:
            json.dump(resultado_final, f, indent=4, ensure_ascii=False)
        print("✅ Archivo 'tasas.json' actualizado con éxito.")
        
        # Print de consola para que veas en el log de GitHub qué guardó
        if "bcv" in resultado_final:
            print(f"BCV: {resultado_final['bcv']['price']}")
        if "yadio" in resultado_final:
            print(f"Yadio: {resultado_final['yadio']['price']}")
            
    except Exception as e:
        print(f"❌ Error al escribir el archivo: {e}")

if __name__ == "__main__":
    actualizar_todo()
