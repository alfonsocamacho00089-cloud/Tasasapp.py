import requests
import json

def obtener_tasas_pydolar():
    # Usamos su API oficial directa
    url = "https://pydolarvenezuela-api.vercel.app/api/v1/dollar?page=criptodolar"
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            res_json = response.json()
            # La API devuelve una lista de monitores en 'monitors'
            return res_json.get('monitors', {})
        return {}
    except Exception as e:
        print(f"❌ Error consultando la API de pyDolar: {e}")
        return {}

def obtener_yadio_manual():
    url = "https://api.yadio.io/json/VES"
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            res_json = response.json()
            return res_json['USD']['rate']
        return None
    except Exception as e:
        print(f"⚠️ Error manual en Yadio: {e}")
        return None

def actualizar_todo():
    # 1. Obtenemos los datos de la página de pyDolar vía API
    print("Consultando API de pyDolar...")
    datos_finales = obtener_tasas_pydolar()

    # 2. Obtenemos Yadio (Tu respaldo)
    yadio_rate = obtener_yadio_manual()
    
    if yadio_rate:
        datos_finales["yadio"] = {
            "title": "Yadio API",
            "price": yadio_rate
        }
        print(f"✅ Yadio cargado: {yadio_rate}")

    # 3. Guardar el archivo tasas.json
    if datos_finales:
        try:
            with open('tasas.json', 'w', encoding='utf-8') as f:
                json.dump(datos_finales, f, indent=4, ensure_ascii=False)
            print("💾 Archivo 'tasas.json' actualizado con éxito.")
        except Exception as e:
            print(f"❌ Error al escribir el JSON: {e}")
    else:
        print("🚫 No se obtuvieron datos de ninguna fuente.")

if __name__ == "__main__":
    actualizar_todo()
