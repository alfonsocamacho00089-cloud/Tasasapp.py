import streamlit as st
import requests
import datetime

# Configuración de la página
st.set_page_config(page_title="TuPropina P2P - Multi-Antena", page_icon="📡")
st.title("📡 Antena Multi-Tasas (Binance, Yadio, Bit)")

# --- FUNCIONES DE OBTENCIÓN ---

def obtener_p2p_alto():
    st.cache_data.clear()
    url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
    payload = {
        "asset": "USDT",
        "fiat": "VES",
        "tradeType": "SELL", 
        "bank": ["Banesco"],
        "rows": 1,
        "page": 1,
        "publisherType": "merchant"
    }
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        if response.status_code == 200:
            return response.json()['data'][0]['adv']['price']
        return "Error Binance"
    except:
        return "Sin señal Binance"

def obtener_yadio():
    try:
        # API de Yadio para USDT en Venezuela
        url = "https://api.yadio.io/json/USDT"
        res = requests.get(url, timeout=10)
        return res.json()['USDT']['price']
    except:
        return "Sin señal Yadio"

def obtener_bityadio():
    try:
        # API de BitYadio (Precio de mercado)
        url = "https://api.bityadio.com/v1/ticker/usdtves"
        res = requests.get(url, timeout=10)
        return res.json()['last_price']
    except:
        return "Sin señal Bit"

# --- EJECUCIÓN ---

# Obtenemos las 3 tasas
p_binance = obtener_p2p_alto()
p_yadio = obtener_yadio()
p_bit = obtener_bityadio()

hora_actual = (datetime.datetime.now() - datetime.timedelta(hours=4)).strftime("%I:%M:%S %p")

# Mostrar en pantalla (Métrica)
col1, col2, col3 = st.columns(3)
col1.metric("Binance (P2P)", f"{p_binance} Bs")
col2.metric("Yadio", f"{p_yadio} Bs")
col3.metric("BitYadio", f"{p_bit} Bs")

# --- GUARDADO PARA EL HTML ---

# Creamos la cadena que leerá tu Calculadora TuPropina
# Formato: Binance|Yadio|Bit
info_integrada = f"{p_binance}|{p_yadio}|{p_bit}"

try:
    with open("tasa.txt", "w") as f:
        f.write(info_integrada)
    st.success(f"✅ Datos sincronizados en GitHub: `{info_integrada}`")
except Exception as e:
    st.error(f"Error al escribir archivo: {e}")

st.info("💡 Tu HTML ahora recibirá tres valores. Asegúrate de separarlos con un `.split('|')` en tu JavaScript.")
st.write(f"🕒 **Última actualización:** {hora_actual}")
