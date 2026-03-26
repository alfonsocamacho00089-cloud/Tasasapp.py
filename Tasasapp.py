import streamlit as st
import requests
import datetime
import re

st.set_page_config(page_title="Antena Telegram", page_icon="📲")
st.title("📲 Antena: Señal Telegram (Paralelo)")

# --- FUNCIÓN PARA EXTRAER DE TELEGRAM (MÉTODO PÚBLICO) ---

def obtener_precio_telegram(canal):
    """
    Lee la vista pública de un canal de Telegram y busca el patrón de precio.
    Canales comunes: 'monitordolarvla', 'enparalelovzla', etc.
    """
    try:
        # Usamos la vista web pública de Telegram (no necesita API de Bot)
        url = f"https://t.me/s/{canal}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        res = requests.get(url, headers=headers, timeout=15)
        
        if res.status_code == 200:
            # Buscamos números que parezcan precios (ejemplo: 39,45 o 40.10)
            # Buscamos el último mensaje que contenga "Bs" o decimales
            texto = res.text
            # Esta expresión busca números con coma o punto seguidos de "Bs"
            encontrados = re.findall(r"(\d+[\.,]\d+)\s?Bs", texto)
            
            if encontrados:
                # El último precio publicado suele ser el final de la lista
                precio_raw = encontrados[-1].replace(",", ".")
                return round(float(precio_raw), 2)
        return "Buscando..."
    except:
        return "Sin señal"

# --- EJECUCIÓN ---

# Probamos con dos canales populares que reportan Bybit y Paralelo
p_monitor = obtener_precio_telegram("monitordolarvla")
p_bybit_tele = obtener_precio_telegram("EnParaleloVzlaVip") # Ejemplo de canal

hora_actual = (datetime.datetime.now() - datetime.timedelta(hours=4)).strftime("%I:%M:%S %p")

st.subheader("📊 Precios extraídos de Telegram")
col1, col2 = st.columns(2)

with col1:
    st.metric("Monitor Paralelo", f"{p_monitor} Bs")
    st.caption("Fuente: @monitordolarvla")

with col2:
    st.metric("Bybit/P2P Ref", f"{p_bybit_tele} Bs")
    st.caption("Fuente: @EnParaleloVzla")

# --- GUARDADO ---
info_tele = f"{p_monitor}|{p_bybit_tele}"

# Solo guardamos si capturó números reales
if isinstance(p_monitor, float):
    with open("tasa.txt", "w") as f:
        f.write(info_tele)
    st.success(f"✅ ¡Señal de Telegram capturada!: {info_tele}")
else:
    st.warning("Telegram está tardando en responder. Refresca la antena.")

st.write(f"🕒 **Sincronizado:** {hora_actual}")
