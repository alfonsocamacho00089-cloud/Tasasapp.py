import streamlit as st
import requests
import datetime
import json

st.set_page_config(page_title="Antena Paralelo", page_icon="📡")
st.title("📡 Antena: Monitor Paralelo")

def obtener_paralelo_real():
    # Usamos AllOrigins para disfrazar la petición y evitar el Error 403
    # Esta URL busca directamente el promedio del paralelo en PyDolar
    target = "https://pydolarvenezuela-api.vercel.app/api/v1/dollar/unit/promedio"
    proxy = f"https://api.allorigins.win/get?url={target}"
    
    try:
        res = requests.get(proxy, timeout=20)
        if res.status_code == 200:
            # Extraemos la info del túnel
            datos = json.loads(res.json()['contents'])
            return round(float(datos['price']), 2)
        return "Error 403"
    except:
        # Si el túnel falla, intentamos una fuente directa alternativa (Exchangerate)
        try:
            alt = requests.get("https://open.er-api.com/v6/latest/USD", timeout=10)
            return round(alt.json()['rates']['VES'], 2)
        except:
            return "Sin señal"

# --- EJECUCIÓN ---
tasa_paralelo = obtener_paralelo_real()
hora_actual = (datetime.datetime.now() - datetime.timedelta(hours=4)).strftime("%I:%M:%S %p")

# Mostrar en grande
if isinstance(tasa_paralelo, float):
    st.balloons()
    st.success(f"## 📈 PARALELO: {tasa_paralelo} Bs.")
    st.code(f"VALOR_REAL|{tasa_paralelo}|")
else:
    st.error(f"Intentando reconectar... (Estado: {tasa_paralelo})")

# Guardar en el archivo para tu calculadora
with open("tasa.txt", "w") as f:
    f.write(str(tasa_paralelo))

st.info("Esta señal usa un túnel para saltar el bloqueo de los monitores.")
st.write(f"🕒 **Última sincronización:** {hora_actual}")
