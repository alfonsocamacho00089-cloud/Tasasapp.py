import streamlit as st
import requests
import datetime

# Configuración de la Antena
st.set_page_config(page_title="Antena Bybit-Yadio", page_icon="📡")
st.title("📡 Antena: Señal Bybit & Yadio")

# --- FUNCIONES DE SEÑAL CORREGIDAS ---

def obtener_yadio():
    """ Obtiene el precio de Yadio.io (USDT/VES) """
    try:
        # Endpoint público y directo
        url = "https://api.yadio.io/json/USDT"
        # Cabecera para parecer un navegador normal
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        res = requests.get(url, headers=headers, timeout=10)
        
        if res.status_code == 200:
            # Buscamos el precio en la estructura del JSON
            return res.json()['USDT']['price']
        return "Error Yadio"
    except:
        return "Sin señal Yadio"

def obtener_bybit():
    """ Obtiene el precio de Bybit (USDT/VES) """
    try:
        # Endpoint de Bybit para el mercado Spot (Tasa de referencia)
        url = "https://api.bybit.com/v5/market/tickers?category=spot&symbol=USDT-VES"
        # Cabecera reforzada para evitar bloqueos
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
            "Accept": "application/json"
        }
        res = requests.get(url, headers=headers, timeout=10)
        
        if res.status_code == 200:
            data = res.json()
            # 'lastPrice' es el último precio transado (la tasa actual)
            return data['result']['list'][0]['lastPrice']
        return f"Error Bybit ({res.status_code})"
    except:
        return "Sin señal Bybit"

# --- EJECUCIÓN Y PANTALLA ---

# Traemos las señales corregidas
tasa_yadio = obtener_yadio()
tasa_bybit = obtener_bybit()

# Ajuste de hora (Venezuela es UTC-4)
hora_actual = (datetime.datetime.now() - datetime.timedelta(hours=4)).strftime("%I:%M:%S %p")

# Diseño de la Antena en Streamlit
col1, col2 = st.columns(2)

with col1:
    st.metric(label="📍 Yadio (USDT)", value=f"{tasa_yadio} Bs")
    
with col2:
    st.metric(label="🪙 Bybit (Spot)", value=f"{tasa_bybit} Bs")

# --- GUARDADO PARA TU CALCULADORA ---
# Formato compatible en tasa.txt: YADIO|BYBIT
# Ejemplo: 39.50|39.42
info_txt = f"{tasa_yadio}|{tasa_bybit}"

try:
    with open("tasa.txt", "w") as f:
        f.write(info_txt)
    st.success(f"✅ Señal enviada a GitHub: `{info_txt}`")
except Exception as e:
    st.error(f"Fallo al guardar: {e}")

st.write(f"🕒 **Sincronizado a las:** {hora_actual}")
