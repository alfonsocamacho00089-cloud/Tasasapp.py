import json
from pyDolarVenezuela import Monitor

def obtener_datos_venezuela():
    try:
        # La forma correcta en la versión actual es llamar a Monitor() directamente
        monitor = Monitor()
        
        # Obtenemos los datos (Bybit, Yadio, BCV, etc.)
        # Nota: La librería usa 'enparalelovzla' para el paralelo
        data = monitor.get_all_monitors()
        
        # Extraemos los precios con pinzas
        bybit = data.get('bybit', {}).get('price', "N/A")
        yadio = data.get('yadio', {}).get('price', "N/A")
        bcv = data.get('bcv', {}).get('price', "N/A")
        paralelo = data.get('enparalelovzla', {}).get('price', "N/A")

        resultado = [
            {"bank": "Bybit P2P", "precio": bybit},
            {"bank": "Yadio API", "precio": yadio},
            {"bank": "BCV Oficial", "precio": bcv},
            {"bank": "Paralelo", "precio": paralelo}
        ]
        
        with open('tasas.json', 'w', encoding='utf-8') as f:
            json.dump(resultado, f, indent=4, ensure_ascii=False)
            
        print(f"✅ ¡LISTO! Bybit: {bybit} | Paralelo: {paralelo}")
        
    except Exception as e:
        print(f"❌ Error en el último paso: {e}")

if __name__ == "__main__":
    obtener_datos_venezuela()
