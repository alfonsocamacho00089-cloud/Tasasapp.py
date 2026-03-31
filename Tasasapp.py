import json
from datetime import datetime
from pyDolarVenezuela import Monitor

def obtener_datos_venezuela():
    try:
        monitor = Monitor()
        data = monitor.get_all_monitors()
        
        # Buscamos los precios
        bybit = data.get('bybit', {}).get('price', "N/A")
        yadio = data.get('yadio', {}).get('price', "N/A")
        bcv = data.get('bcv', {}).get('price', "N/A")
        paralelo = data.get('enparalelovzla', {}).get('price', "N/A")

        # Añadimos la hora para que el archivo SIEMPRE cambie
        ahora = datetime.now().strftime("%d/%m/%Y %I:%M %p")

        resultado = {
            "ultima_actualizacion": ahora,
            "tasas": [
                {"bank": "Bybit P2P", "precio": bybit},
                {"bank": "Yadio API", "precio": yadio},
                {"bank": "BCV Oficial", "precio": bcv},
                {"bank": "Paralelo", "precio": paralelo}
            ]
        }
        
        with open('tasas.json', 'w', encoding='utf-8') as f:
            json.dump(resultado, f, indent=4, ensure_ascii=False)
            
        print(f"✅ Guardado a las {ahora}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    obtener_datos_venezuela()
