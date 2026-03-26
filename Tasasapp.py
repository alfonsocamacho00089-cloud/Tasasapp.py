import streamlit as st
import requests
import datetime

st.set_page_config(page_title="Antena AlCambio", page_icon="📈")
st.title("📈 Antena: Señal AlCambio")

# --- FUNCIÓN ESPECÍFICA PARA ALCAMBIO ---

def obtener_alcambio_p2p():
    try:
        # Usamos el endpoint público de AlCambio
        url = "https://api.alcambio.app/public/v1/metas/rates?per_page=1"
        # Cabecera simple para que nos dejen pasar
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        res = requests.get(url, headers=headers, timeout=12)
        
        if res.status_code == 200:
            data = res.json()
            # AlCambio entrega una lista de tasas. 
            # p2p_buy es el promedio de compra en los exchanges (Bybit/Binance)
            tasa_p2p = data['data'][0]['p2p_buy']
            # parallel es la tasa del monitor/paralelo
            tasa_paralelo = data['data'][0]['parallel']
            
            return round(float(tasa_p2p), 2), round(float(tasa_paralelo), 2)
        return "Error 403", "Error 403"
    except Exception as e:
        return "Sin señal", "Sin señal"

# --- EJECUCIÓN ---

tasa_p2p, tasa_paralelo = obtener_alcambio_p2p()

hora_actual = (datetime.datetime.now() - datetime.timedelta(hours=4)).strftime("%I:%M:%S %p")

# Diseño en pantalla
st.subheader("📊 Reporte de AlCambio")
col1, col2 = st.columns(2)

with col1:
    st.metric("Promedio P2P", f"{tasa_p2p} Bs")
    st.caption("Basado en vendedores reales")

with col2:
    st.metric("Dólar Paralelo", f"{tasa_paralelo} Bs")
    st.caption("Referencia Monitor")

# --- GUARDADO PARA LA CALCULADORA ---
# Formato: P2P|PARALELO
info_alcambio = f"{tasa_p2p}|{tasa_paralelo}"

try:
    with open("tasa.txt", "w") as f:
        f.write(info_alcambio)
    st.success(f"✅ AlCambio sincronizado: `{info_alcambio}`")
except:
    st.error("Error al escribir el archivo tasa.txt")

st.write(f"🕒 **Última actualización:** {hora_actual}")
