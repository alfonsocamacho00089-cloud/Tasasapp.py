import json
from datetime import datetime
from pyDolarVenezuela import Monitor

def obtener_datos_venezuela():
    try:
        monitor = Monitor()
        data = monitor.get_all_monitors()
        
        # Sacamos los datos
        bybit = data.get('bybit', {}).get('price', "N/A")
        yadio = data.get('yadio', {}).get('price', "N/A")
        
        # LA CLAVE: Guardar la hora exacta
        ahora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        resultado = {
            "fecha_actualizacion": ahora,
            "tasas": [
                {"bank": "Bybit P2P", "precio": bybit},
                {"bank": "Yadio API", "precio": yadio}
            ]
        }
        
        with open('tasas.json', 'w', encoding='utf-8') as f:
            json.dump(resultado, f, indent=4, ensure_ascii=False)
        print(f"✅ Archivo generado con éxito a las {ahora}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    obtener_datos_venezuela()
