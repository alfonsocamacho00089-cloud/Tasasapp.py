import requests
import json
from pyDolarVenezuela.pages import Monitor

def obtener_datos_venezuela():
    """
    Obtiene todas las tasas reales de Venezuela usando la librería especializada.
    """
    try:
        # Instanciamos el monitor
        monitor = Monitor()
        
        # Obtenemos todos los monitores de un solo golpe
        data = monitor.get_all_monitors()
        
        # Extraemos los precios reales (Si no existen, pone "N/A")
        # pyDolar usa nombres específicos, estos son los correctos:
        bybit_p2p = data.get('bybit', {}).get('price', "N/A")
        yadio_api = data.get('yadio', {}).get('price', "N/A")
        bcv_oficial = data.get('bcv', {}).get('price', "N/A")
        paralelo = data.get('enparalelovzla', {}).get('price', "N/A")

        # Estructura limpia para tu calculadora
        tasas_limpias = [
            {"bank": "Bybit P2P", "precio": bybit_p2p},
            {"bank": "Yadio API", "precio": yadio_api},
            {"bank": "BCV Oficial", "precio": bcv_oficial},
            {"bank": "Paralelo", "precio": paralelo}
        ]
        
        # Guardamos en el JSON (sobrescribe lo viejo con datos reales)
        with open('tasas.json', 'w', encoding='utf-8') as f:
            json.dump(tasas_limpias, f, indent=4, ensure_ascii=False)
            
        print(f"✅ ¡Éxito! Bybit: {bybit_p2p} | Yadio: {yadio_api}")
        
    except Exception as e:
        print(f"❌ Error real en la actualización: {e}")

# --- EJECUCIÓN ÚNICA ---
if __name__ == "__main__":
    obtener_datos_venezuela()
