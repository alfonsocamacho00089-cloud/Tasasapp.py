import streamlit as st
import requests
import datetime
import json

st.set_page_config(page_title="Antena P2P Paralelo", page_icon="📡")
st.title("📡 Antena: Paralelo P2P")

# --- FUNCIÓN CON TÚNEL PARA EVITAR BLOQUEOS ---

def obtener_paralelo_p2p(fuente):
    """
    fuente: 'bybit' o 'yadio'
    """
    # Usamos el puente AllOrigins para que Streamlit no sea bloqueado
    # Apuntamos a la API de PyDolar que resume el P2P de cada exchange
    target = f"https://pydolarvenezuela-api.vercel.app/api/v1/dollar/unit/{fuente}"
    proxy = f"https://api.allorigins.win/get?url={target}"
    
    try:
        res = requests.get(proxy, timeout=20)
        if res.status_code == 200:
            datos = json.loads(res.json()['contents'])
            return round(float(datos['price']), 2)
        return "Bloqueo 403"
    except:
        return "Sin señal"

# --- EJECUCIÓN ---

# Buscamos el paralelo de cada una
p_bybit = obtener_paralelo_p2p("bybit")
p_yadio = obtener_paralelo_p2p("yadio")

hora_actual = (datetime.datetime.now() - datetime.timedelta(hours=4)).strftime("%I:%M:%S %p")

# Mostrar en pantalla
st.subheader("📊 Cotización P2P (Paralelo)")
col1, col2 = st.columns(2)

with col1:
    st.metric("Bybit P2P", f"{p_bybit} Bs")
    st.caption("Promedio vendedores Bybit")

with col2:
    st.metric("Yadio P2P", f"{p_yadio} Bs")
    st.caption("Promedio mercado Yadio")

# --- GUARDADO PARA TU CALCULADORA ---
# Formato: BYBIT|YADIO
info_p2p = f"{p_bybit}|{p_yadio}"

if "Bloqueo" not in str(p_bybit) and "Sin" not in str(p_bybit):
    with open("tasa.txt", "w") as f:
        f.write(info_p2p)
    st.success(f"✅ Señal P2P sincronizada: {info_p2p}")
else:
    st.warning("La señal está inestable, intentando reconectar por el túnel...")

st.write(f"🕒 **Sincronizado a las:** {hora_actual}")
