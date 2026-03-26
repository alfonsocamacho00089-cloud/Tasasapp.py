import streamlit as st
import requests
import datetime

st.set_page_config(page_title="Antena Multi-Tasas", page_icon="💰")
st.title("💰 Tasas: AlCambio & ApiDolar")

# --- FUNCIONES DE AGREGADORES (MÁS ESTABLES) ---

def obtener_alcambio():
    try:
        # Endpoint de AlCambio para paralelo/promedio
        url = "https://api.alcambio.app/public/v1/metas/rates?per_page=1"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200:
            # Buscamos la tasa del paralelo o promedio USDT
            data = res.json()
            # Esta ruta puede variar un poco según su JSON, ajustamos al valor principal
            tasa = data['data'][0]['p2p_buy'] # O 'parallel'
            return round(float(tasa), 2)
        return "Error 403"
    except:
        return "Sin señal"

def obtener_apidolar():
    try:
        # ApiDolar es muy buena para promedios de Venezuela
        url = "https://pydolarvenezuela-api.vercel.app/api/v1/dollar/unit/promedio"
        res = requests.get(url, timeout=10)
        if res.status_code == 200:
            return round(float(res.json()['price']), 2)
        return "Error Red"
    except:
        return "Sin señal"

# --- EJECUCIÓN ---

tasa_alcambio = obtener_alcambio()
tasa_apidolar = obtener_apidolar()

hora_actual = (datetime.datetime.now() - datetime.timedelta(hours=4)).strftime("%I:%M:%S %p")

# Visualización
col1, col2 = st.columns(2)

with col1:
    st.metric("📊 AlCambio", f"{tasa_alcambio} Bs")
    st.caption("Promedio P2P / Paralelo")

with col2:
    st.metric("💵 ApiDolar", f"{tasa_apidolar} Bs")
    st.caption("Monitor Promedio")

# --- GUARDADO ---
# Mantenemos el formato para tu calculadora
# Formato: ALCAMBIO|APIDOLAR
info_final = f"{tasa_alcambio}|{tasa_apidolar}"

try:
    with open("tasa.txt", "w") as f:
        f.write(info_final)
    st.success(f"✅ ¡Señal activa!: {info_final}")
except:
    st.error("Error al escribir tasa.txt")

st.write(f"🕒 **Actualizado:** {hora_actual}")
