import requests
import json

# Headers de un navegador real de Android (para que parezca que entras desde el cel)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.119 Mobile Safari/537.36",
    "Referer": "https://www.google.com/"
}

def obtener_bybit_secreto():
    # RUTA A: El "Espejo" de ExchangeMonitor (Muy resistente)
    # Esta URL extrae los datos procesados de varios monitores
    url_mirror = "https://api.exchangemonitor.net/all" 
    
    # RUTA B: CriptoDolar (API alternativa que rara vez bloquea)
    url_cripto = "https://api.monedasvenezuela.com/v1/dollar/criptodolar"

    try:
        print("🕵️ Intentando entrar por el espejo de ExchangeMonitor...")
        r = requests.get(url_mirror, headers=HEADERS, timeout=15)
        if r.status_code == 200:
            # Buscamos la sección de Bybit dentro de su respuesta masiva
            data = r.json()
            # A veces viene como 'bybit' o dentro de 'cripto'
            precio = data.get('bybit', {}).get('price')
            if precio: return precio

        print("🕵️ Intentando por CriptoDolar...")
        r = requests.get(url_cripto, headers=HEADERS, timeout=15)
        if r.status_code == 200:
            return r.json().get('price')
            
    except:
        return None

def main():
    tasa = obtener_bybit_secreto()
    
    if tasa:
        resultado = {"bybit": {"price": float(tasa), "fuente": "Mirror Externa"}}
        with open('tasas.json', 'w') as f:
            json.dump(resultado, f, indent=4)
        print(f"✅ ¡POR FIN! Bybit: {tasa}")
    else:
        # Si esto falla, es que GitHub Actions está bajo un bloqueo total de IPs hoy
        print("🚫 El muro de Bybit sigue en pie. Mañana tendrá otra IP y quizás pase.")

if __name__ == "__main__":
    main()    actualizar_repositorio_pruebas()
