import requests
import json

def obtener_tasa_reserva():
    # Usamos el JSON de DolarToday alojado en Amazon S3
    # Es extremadamente estable y GitHub tiene permiso total para leerlo
    url = "https://s3.amazonaws.com/dolartoday/data.json"
    
    try:
        print("📡 Conectando con el servidor de reserva...")
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            # Sacamos el promedio que ellos manejan para el paralelo/P2P
            precio = data.get('USD', {}).get('dolartoday')
            return precio
    except:
        return None

def actualizar():
    tasa = obtener_tasa_reserva()
    
    if tasa:
        # Guardamos el resultado con el nombre que espera tu App
        resultado = {
            "bybit": {
                "title": "Tasa Referencial P2P",
                "price": float(tasa)
            }
        }
        with open('tasas.json', 'w', encoding='utf-8') as f:
            json.dump(resultado, f, indent=4, ensure_ascii=False)
        print(f"✅ ¡LOGRADO! Tasa capturada: {tasa}")
    else:
        print("🚫 Error de conexión con el servidor de reserva.")

if __name__ == "__main__":
    actualizar()
