import requests
import json

def obtener_tasas_pydolar():
def obtener_tasas_pydolar():
    # Esta es la URL directa de la data de CriptoDolar (la que usa pyDolar)
    url = "https://pydolarvenezuela-api.vercel.app/api/v1/dollar?page=criptodolar"
    
    # Añadimos Headers para que la API no nos rechace por ser un script
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        print(f"Status API: {response.status_code}") # Esto nos dirá si dio 200, 403 o 404
        
        if response.status_code == 200:
            res_json = response.json()
            # La API de CriptoDolar guarda todo dentro de 'monitors'
            monitores = res_json.get('monitors', {})
            if monitores:
                print(f"✅ Se encontraron {len(monitores)} monitores en pyDolar.")
                return monitores
        
        print("⚠️ La API respondió pero 'monitors' vino vacío.")
        return {}
    except Exception as e:
        print(f"❌ Error de conexión con la API: {e}")
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
