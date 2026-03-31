import requests
import json
import datetime


# Lista de diferentes identidades (Headers) para probar
LISTA_HEADERS = [
    {   # Identidad 1: Navegador Chrome estándar
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Referer": "https://www.bybit.com/fiat/trade/otc/USDT/VES/item-list",
        "Origin": "https://www.bybit.com"
    },
    {   # Identidad 2: Navegador Firefox (a veces más permisivo)
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
        "Accept": "application/json",
        "Referer": "https://www.bybit.com/"
    },
    {   # Identidad 3: Simulación de App Móvil (La más "guerrera")
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1",
        "Referer": "https://m.bybit.com/",
        "Origin": "https://m.bybit.com"
    }
]

def obtener_bybit():
    # Lista de fuentes (APIs alternativas) para sacar el precio de Bybit
    fuentes = [
        {
            "nombre": "Exchangemonitor",
            "url": "https://p2p.exchangemonitor.net/api/v1/get/bybit/ves",
            "llave": "price"
        },
        {
            "nombre": "P2P Proxy",
            "url": "https://api.p2p.army/v1/p2p/config", # Ejemplo de ruta alterna
            "llave": "bybit_price"
        },
        {
            "nombre": "Yadio Exchanges",
            "url": "https://api.yadio.io/exchanges/ves",
            "llave": "bybit"
        }
    ]

    for fuente in fuentes:
        try:
            print(f"Probando fuente: {fuente['nombre']}...")
            response = requests.get(fuente['url'], timeout=10)
            
            if response.status_code == 200:
                datos = response.json()
                
                # Lógica especial para Yadio (porque los datos vienen dentro de 'bybit')
                if fuente['nombre'] == "Yadio Exchanges":
                    if 'bybit' in datos:
                        return datos['bybit']['price']
                
                # Lógica para otras APIs que devuelven el precio directo
                if fuente['llave'] in datos:
                    return datos[fuente['llave']]
                    
            print(f"❌ {fuente['nombre']} no respondió bien (Status: {response.status_code})")
            
        except Exception as e:
            print(f"⚠️ Error conectando a {fuente['nombre']}: {e}")
            continue # Salta a la siguiente fuente

    return "Bybit: Todas las APIs fallaron"
def obtener_yadio():
    # Yadio es más directo y no requiere payload complejo
    url = "https://api.yadio.io/json/VES"
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            res_json = response.json()
            # Usamos el precio de USDT
            return res_json['USD']['rate']
        return f"Error Yadio: {response.status_code}"
    except Exception as e:
        return f"Sin señal Yadio: {e}"

# --- EJECUCIÓN ---

precio_bybit = obtener_bybit()
precio_yadio = obtener_yadio()

# Estructura del resultado
resultado = [
    {"bank": "Bybit P2P", "precio": precio_bybit},
    {"bank": "Yadio API", "precio": precio_yadio}
]

# Guardar en tasas.json
with open("tasas.json", "w") as f:
    json.dump(resultado, f, indent=4)

print(f"Actualizado con éxito: Bybit: {precio_bybit} | Yadio: {precio_yadio}")
