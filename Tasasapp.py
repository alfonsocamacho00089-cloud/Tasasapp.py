import requests
import json

# HEADERS REFORZADOS: Con Referer y Origin para máxima compatibilidad
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Referer": "https://www.bybit.com/fiat/trade/otc/USDT/VES",
    "Origin": "https://www.bybit.com"
}

def obtener_bybit_blindado():
    """
    Consulta las 4 fuentes más potentes que ya extraen Bybit,
    usando los headers de simulación oficial.
    """
    fuentes = [
        {
            "nombre": "PyDolar API",
            "url": "https://pydolarvenezuela-api.vercel.app/api/v1/dollar?monitor=bybit",
            "key": "price"
        },
        {
            "nombre": "Monedas Venezuela",
            "url": "https://api.monedasvenezuela.com/v1/dollar/bybit",
            "key": "price"
        },
        {
            "nombre": "CriptoDolar (Bybit Mirror)",
            "url": "https://api.monedasvenezuela.com/v1/dollar/criptodolar",
            "key": "price"
        },
        {
            "nombre": "Exchange Monitor Proxy",
            "url": "https://pydolarvenezuela-api.vercel.app/api/v1/dollar?monitor=exchangemonitor",
            "key": "price"
        }
    ]

    for f in fuentes:
        try:
            print(f"🚀 Intentando Bybit vía {f['nombre']}...")
            # Usamos los headers reforzados con Referer y Origin aquí
            response = requests.get(f['url'], headers=HEADERS, timeout=12)
            
            if response.status_code == 200:
                data = response.json()
                precio = data.get(f['key'])
                
                if precio:
                    print(f"✅ ¡CONSEGUIDO! Tasa: {precio} desde {f['nombre']}")
                    return float(precio)
        except Exception as e:
            print(f"❌ {f['nombre']} falló: {e}")
            continue
            
    return None

def actualizar_repositorio_pruebas():
    tasa_final = obtener_bybit_blindado()
    
    if tasa_final:
        # Formato limpio para tu JSON
        resultado = {
            "bybit": {
                "title": "Bybit P2P (Optimizado)",
                "price": tasa_final,
                "status": "Actualizado"
            }
        }
        
        # Guardamos en el archivo que tu YAML debe estar rastreando
        with open('tasas.json', 'w', encoding='utf-8') as f:
            json.dump(resultado, f, indent=4, ensure_ascii=False)
            
        print("💾 Archivo 'tasas.json' actualizado y listo para subir.")
    else:
        print("🚫 Todas las fuentes fallaron. Bybit tiene la seguridad muy alta hoy.")

if __name__ == "__main__":
    actualizar_repositorio_pruebas()
