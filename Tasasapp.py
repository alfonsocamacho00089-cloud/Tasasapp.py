import json
import os
from datetime import datetime
from pyDolarVenezuela import Monitor

def obtener_datos_venezuela():
    try:
        monitor = Monitor()
        data = monitor.get_all_monitors()
        
        # Sacamos los precios
        bybit = data.get('bybit', {}).get('price', "N/A")
        yadio = data.get('yadio', {}).get('price', "N/A")
        bcv = data.get('bcv', {}).get('price', "N/A")
        paralelo = data.get('enparalelovzla', {}).get('price', "N/A")

        ahora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        # Estructura de lista para tu calculadora
        resultado = [
            {"bank": "Bybit P2P", "precio": bybit, "fecha": ahora},
            {"bank": "Yadio API", "precio": yadio, "fecha": ahora},
            {"bank": "BCV Oficial", "precio": bcv, "fecha": ahora},
            {"bank": "Paralelo", "precio": paralelo, "fecha": ahora}
        ]
        
        # Forzamos la ruta absoluta para que GitHub no se pierda
        ruta_archivo = os.path.join(os.getcwd(), 'tasas.json')
        
        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            json.dump(resultado, f, indent=4, ensure_ascii=False)
            
        print(f"✅ ARCHIVO CREADO EN: {ruta_archivo}")
        print(f"✅ CONTENIDO: {resultado}") # Esto es para que lo veas en el log
        
    except Exception as e:
        print(f"❌ ERROR CRÍTICO: {e}")

if __name__ == "__main__":
    obtener_datos_venezuela()
