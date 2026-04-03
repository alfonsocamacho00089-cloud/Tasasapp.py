import requests
import json
import time

# --- TUS DATOS DE TELEGRAM ---
TOKEN_BOT = "8317000492:AAHBidIMBFqAdH4t4GufKzeTfiF7TmJuhts"
MI_CHAT_ID = "8320121552"

# Headers de camuflaje
HEADERS = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Mobile/15E148 Safari/604.1",
    "Accept": "application/json",
    "Referer": "https://www.google.com/"
}

def enviar_alerta_telegram(mensaje):
def enviar_alerta_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TOKEN_BOT}/sendMessage"
    
    # Estos links son más directos y estables para Bybit USDT
    payload = {
        "chat_id": MI_CHAT_ID,
        "text": mensaje,
        "reply_markup": {
            "inline_keyboard": [
                [
                    # Este link suele saltarse mejor los bloqueos
                    {"text": "🚀 BYBIT USDT (Directo)", "url": "https://pydolarvenezuela-api.vercel.app/api/v1/dollar?monitor=bybit"},
                ],
                [
                    # Una alternativa que siempre carga
                    {"text": "📊 Ver en Telegram (DolarToday)", "url": "https://t.me/DolarToday"}
                ],
                [
                    # Tu propia App para que entres a actualizarla
                    {"text": "🏠 Ir a mi App TuPropina", "url": "https://alfonsocamacho00089.github.io/TuPropina/"}
                ]
            ]
        }
    }
    try:
        requests.post(url, json=payload, timeout=10)
    except:
        print("❌ Error al enviar el menú.")
        
def barrido_total():
    fuentes = [
        {"n": "CriptoDolar", "u": "https://api.monedasvenezuela.com/v1/dollar/criptodolar", "p": ["price"]},
        {"n": "PyDolar Bybit", "u": "https://pydolarvenezuela-api.vercel.app/api/v1/dollar?monitor=bybit", "p": ["price"]},
        {"n": "MonedasVZLA", "u": "https://api.monedasvenezuela.com/v1/dollar/bybit", "p": ["price"]},
        {"n": "DolarToday", "u": "https://s3.amazonaws.com/dolartoday/data.json", "p": ["USD", "dolartoday"]}
    ]

    for f in fuentes:
        try:
            print(f"📡 Probando {f['n']}...")
            r = requests.get(f['u'], headers=HEADERS, timeout=12)
            if r.status_code == 200:
                data = r.json()
                valor = data
                for clave in f['p']:
                    valor = valor.get(clave, {})
                if isinstance(valor, (int, float, str)):
                    return float(valor), f['n']
        except:
            continue
    return None, None

def main():
    print("🚀 Iniciando actualización...")
    tasa, fuente = barrido_total()
    
    if tasa:
        resultado = {
            "bybit": {
                "title": f"Bybit (via {fuente})",
                "price": tasa,
                "update": time.strftime("%H:%M:%S")
            }
        }
        with open('tasas.json', 'w', encoding='utf-8') as f:
            json.dump(resultado, f, indent=4, ensure_ascii=False)
        print(f"✅ ÉXITO: {tasa} desde {fuente}")
    else:
        print("🚫 Bloqueo total detectado. Enviando alerta...")
        link_manual = "https://criptodolar.net/cotizacion/dolar/p2p/bybit"
        mensaje = f"🚨 ¡Alerta TuPropina!\n\nGitHub está bloqueado y no pudo actualizar Bybit.\n\nRevisa la tasa manual aquí:\n{link_manual}"
        enviar_alerta_telegram(mensaje)

if __name__ == "__main__":
    main()
