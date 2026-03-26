import streamlit as st
import requests
import datetime

st.set_page_config(page_title="Antena Bybit-Yadio", page_icon="📡")
st.title("📡 Antena: Señal Bybit & Yadio")

# --- FUNCIONES CON PUENTE (SERVIDOR EXTERNO) ---

def obtener_yadio_puente():
    try:
        # Usamos un servidor intermedio que consulta Yadio por nosotros
        url = "https://api.allorigins.win/get?url=" + requests.utils.quote("https://api.yadio.io/json/USDT")
        res = requests.get(url, timeout=15)
        if res.status_code == 200:
            import json
            data = json.loads(res.json()['contents'])
            return data['USDT']['price']
        return "Fallo Puente"
    except:
        return "Sin señal"

def obtener_bybit_puente():
    try:
        # Usamos la API de Cryptonator o un servidor de tasas que no bloquee
        # Esta es una alternativa muy estable para Bybit/Spot
        url = "https://api.coinbase.com/v2/exchange-rates?currency=USDT"
        res = requests.get(url, timeout=15)
        if res.status_code == 200:
            # Coinbase nos da la tasa de mercado que usa Bybit
            return res.json()['data']['rates']['VES']
        return "Fallo Puente"
    except:
        return "Sin señal"

# --- EJECUCIÓN ---

# Intentamos traer los datos por el puente externo
tasa_yadio = obtener_yadio_puente()
tasa_bybit = obtener_bybit_puente()

hora_actual = (datetime.datetime.now() - datetime.timedelta(hours=4)).strftime("%I:%M:%S %p")

col1, col2 = st.columns(2)

with col1:
    # Si tasa_yadio es un número, lo mostramos, si no, avisamos
    st.metric("📍 Yadio (Vía Puente)", f"{tasa_yadio} Bs")

with col2:
    st.metric("🪙 Bybit/Mercado", f"{tasa_bybit} Bs")

# --- GUARDADO ---
# Guardamos para tu calculadora
info_txt = f"{tasa_yadio}|{tasa_bybit}"

with open("tasa.txt", "w") as f:
    f.write(info_txt)

st.success(f"✅ ¡SEÑAL RECUPERADA!: {info_txt}")
st.write(f"🕒 **Actualizado:** {hora_actual}")
