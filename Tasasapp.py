import requests
import json
from pyDolarVenezuela import Monitor

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
        # 1. Inicializar Monitor
        monitor = Monitor()
        
        # 2. Obtener datos de la librería PRIMERO
        monitores = monitor.get_all_monitors()
        
        # 3. Crear el diccionario 'data' (Convertir a dict si es necesario)
        data = {k: (v.to_dict() if hasattr(v, 'to_dict') else v) for k, v in monitores.items()}

        # 4. AHORA sí, obtener Yadio y agregarlo a 'data'
        precio_yadio = obtener_yadio()
        if precio_yadio:
            data['yadio_api'] = {
                "title": "Yadio API",
                "price": precio_yadio
            }
        
        # 5. Guardar en el archivo
        import os
        ruta_archivo = 'tasas.json'
        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            
        print(f"✅ Tasas actualizadas correctamente.")
        print(f"📁 Archivo guardado en: {os.path.abspath(ruta_archivo)}")
        
        # Debug para GitHub Actions
        bcv = data.get('bcv', {}).get('price', 'N/A')
        enp = data.get('enparalelovzla', {}).get('price', 'N/A')
        print(f"BCV: {bcv} | Paralelo: {enp} | Yadio: {precio_yadio}")

    except Exception as e:
        print(f"❌ Error general: {e}")

if __name__ == "__main__":
    actualizar_todo()
