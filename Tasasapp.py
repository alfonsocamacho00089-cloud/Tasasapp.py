import streamlit as st
import requests
import datetime

st.set_page_config(page_title="Antena Bybit-Yadio", page_icon="📡")
st.title("📡 Antena: Señal Bybit & Yadio")

# --- FUNCIONES ANTI-BLOQUEO ---

def obtener_yadio():
    try:
        # Usamos el conversor directo, es menos probable que lo bloqueen
        url = "https://api.yadio.io/convert/1/USDT/VES"
        headers = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15"}
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200:
            return res.json()['rate']
        return "Error 403"
    except:
        return "Sin señal"

def obtener_bybit():
    try:
        # Cambiamos a la API de V3 que a veces tiene menos restricciones que la V5
        url = "https://api.bybit.com/derivatives/v3/public/tickers?symbol=USDT-VES"
        # O probamos con el ticker de moneda estable directamente
        url_alt = "https://api.bybit.com/v5/market/tickers?category=spot&symbol=USDTVEF"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Referer": "https://www.bybit.com/"
        }
        res = requests.get(url_alt, headers=headers, timeout=10)
        
        if res.status_code == 200:
            return res.json()['result']['list'][0]['lastPrice']
        # Si falla, intentamos una tercera vía (API de instrumentos)
        return f"Bloqueo {res.status_code}"
    except:
        return "Sin señal"

# --- EJECUCIÓN ---

tasa_yadio = obtener_yadio()
tasa_bybit = obtener_bybit()

hora_actual = (datetime.datetime.now() - datetime.timedelta(hours=4)).strftime("%I:%M:%S %p")

col1, col2 = st.columns(2)
col1.metric("📍 Yadio", f"{tasa_yadio} Bs")
col2.metric("🪙 Bybit", f"{tasa_bybit} Bs")

# --- EL PLAN B ---
# Si sigue dando 403, avísame. Podríamos usar una API puente como "ExchangeRate" 
# que ya trae los precios de los exchanges sin que ellos nos bloqueen.

info_txt = f"{tasa_yadio}|{tasa_bybit}"
with open("tasa.txt", "w") as f:
    f.write(info_txt)

st.success(f"Sincronizado: {info_txt}")
st.write(f"🕒 **Hora:** {hora_actual}")
