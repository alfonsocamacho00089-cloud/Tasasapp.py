import requests
import json

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

def obtener_tasa_maestra():
    # Esta es la API de Monitor Dolar Venezuela (Súper estable)
    url = "https://pydolarvenezuela-api.vercel.app/api/v1/dollar?monitor=all"
    
    try:
        print("🕵️ Buscando en el Monitor Maestro...")
        r = requests.get(url, headers=HEADERS, timeout=15)
        if r.status_code == 200:
            data = r.json()
            # Intentamos sacar Bybit específicamente
            monitores = data.get('monitors', {})
            
            # Buscamos en 'bybit' o 'enparalelovzla' como respaldo
            bybit = monitores.get('bybit', {}).get('price')
            if bybit: return bybit
            
            # Si Bybit no está, buscamos 'binance' que siempre está
            binance = monitores.get('binance', {}).get('price')
            if binance: return binance
            
    except:
        return None

def main():
    tasa = obtener_tasa_maestra()
    if tasa:
        with open('tasas.json', 'w') as f:
            json.dump({"bybit": {"price": float(tasa)}}, f, indent=4)
        print(f"✅ ¡POR FIN! Tasa capturada: {tasa}")
    else:
        print("🚫 El servidor sigue bloqueado. Intenta de nuevo en 30 minutos.")

if __name__ == "__main__":
    main()
