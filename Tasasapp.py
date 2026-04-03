import requests
import json
import time

# TU ESTRATEGIA: Camuflaje extremo de iPhone
HEADERS = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Mobile/15E148 Safari/604.1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "es-ES,es;q=0.9",
    "Referer": "https://www.google.com/",
    "DNT": "1"
}

def barrido_total_camuflado():
    # Metemos todas las URLs que conocemos en una sola lista
    fuentes = [
        {"n": "CriptoDolar", "u": "https://api.monedasvenezuela.com/v1/dollar/criptodolar", "p": ["price"]},
        {"n": "PyDolar Bybit", "u": "https://pydolarvenezuela-api.vercel.app/api/v1/dollar?monitor=bybit", "p": ["price"]},
        {"n": "MonedasVZLA", "u": "https://api.monedasvenezuela.com/v1/dollar/bybit", "p": ["price"]},
        {"n": "ExchangeMonitor", "u": "https://api.exchangemonitor.net/all", "p": ["bybit", "price"]},
        {"n": "DolarToday", "u": "https://s3.amazonaws.com/dolartoday/data.json", "p": ["USD", "dolartoday"]}
    ]

    print("🕵️ Iniciando asalto camuflado a todas las fuentes...")

    for f in fuentes:
        try:
            print(f"📱 Probando {f['n']}...")
            # Usamos tus headers reforzados
            r = requests.get(f['u'], headers=HEADERS, timeout=15)
            
            if r.status_code == 200:
                data = r.json()
                # Extraemos el valor según el camino (path)
                valor = data
                for clave in f['p']:
                    valor = valor.get(clave, {})
                
                if isinstance(valor, (int, float, str)):
                    print(f"✅ {f['n']} respondió con éxito.")
                    return float(valor), f['n']
            else:
                print(f"⚠️ {f['n']} rechazó la entrada (Status: {r.status_code})")
        except:
            print(f"❌ Error de conexión en {f['n']}")
        
        # Esperamos un poquito entre una y otra para que no sospechen
        time.sleep(2)
    
    return None, None

def main():
    tasa, fuente = barrido_total_camuflado()
    
    if tasa:
        resultado = {
            "bybit": {
                "title": f"Bybit (via {fuente})",
                "price": tasa,
                "metodo": "Camuflaje iPhone"
            }
        }
        with open('tasas.json', 'w', encoding='utf-8') as f:
            json.dump(resultado, f, indent=4, ensure_ascii=False)
        print(f"💾 ¡LO LOGRAMOS! Guardado {tasa} desde {fuente}")
    else:
        print("🚫 Ni con camuflaje de iPhone entramos. El muro de IPs de GitHub es fuerte hoy.")

if __name__ == "__main__":
    main()
