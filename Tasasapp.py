import json
from pyDolarVenezuela import Monitor

def obtener_datos_venezuela():
    try:
        monitor = Monitor()
        # Intentamos obtener los datos de la página principal (puedes cambiar 'enparalelovzla' por 'criptodolar' si prefieres)
        data = monitor.get_all_monitors()
        
        # Función interna para buscar el precio sin fallar por nombres
        def buscar_precio(nombre):
            for clave, valor in data.items():
                if nombre.lower() in clave.lower():
                    return valor.get('price', "N/A")
            return "N/A"

        # Buscamos los que te interesan para la calculadora
        bybit = buscar_precio('bybit')
        yadio = buscar_precio('yadio')
        bcv = buscar_precio('bcv')
        paralelo = buscar_precio('enparalelovzla')

        resultado = [
            {"bank": "Bybit P2P", "precio": bybit},
            {"bank": "Yadio API", "precio": yadio},
            {"bank": "BCV Oficial", "precio": bcv},
            {"bank": "Paralelo", "precio": paralelo}
        ]
        
        with open('tasas.json', 'w', encoding='utf-8') as f:
            json.dump(resultado, f, indent=4, ensure_ascii=False)
            
        print(f"✅ ¡LISTO! Bybit: {bybit} | Yadio: {yadio}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    obtener_datos_venezuela()
