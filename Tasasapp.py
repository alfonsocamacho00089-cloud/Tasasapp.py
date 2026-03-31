import requests
import json
from pyDolarVenezuela import Monitor

# Mantener Headers para Yadio
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
}

def obtener_yadio():
    url = "https://api.yadio.io/json/VES"
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        if response.status_code == 200:
            res_json = response.json()
            return res_json['USD']['price']
        return None
    except Exception:
        return None

def actualizar_todo():
    try:
        # 1. Obtenemos datos de pyDolarVenezuela (BCV, Paralelo, Bybit, etc.)
        monitor = Monitor()

        
        # 2. Obtenemos Yadio manualmente (tu función original)
        precio_yadio = obtener_yadio()
        
        # 3. Consolidamos la información
        # Agregamos Yadio al diccionario para que todo esté en un solo lugar
        if precio_yadio:
            data['yadio_api'] = {
                "title": "Yadio API",
                "price": precio_yadio
            }
        # Obtenemos los datos y los convertimos a un formato que JSON sí entienda
        monitores = monitor.get_all_monitors()
        data = {k: (v.to_dict() if hasattr(v, 'to_dict') else v) for k, v in monitores.items()}

        # 4. Guardamos en tasas.json con el formato que ya conoces
        with open('tasas.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            
        print("✅ Tasas actualizadas correctamente (Librería + Yadio).")
        
        # Print de control para ver en la consola de GitHub Actions
        bcv = data.get('bcv', {}).get('price')
        enp = data.get('enparalelovzla', {}).get('price')
        print(f"BCV: {bcv} | Paralelo: {enp} | Yadio: {precio_yadio}")

    except Exception as e:
        print(f"❌ Error general: {e}")

if __name__ == "__main__":
    actualizar_todo()
