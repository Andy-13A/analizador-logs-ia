import os
from google import genai

def procesar_logs(ruta_archivo):
    print(f"--- Iniciando análisis del archivo: {ruta_archivo} ---")

    # Abrimos el archivo en modo lectura ('r') y especificamos la codificación UTF-8
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        # Leemos el archivo línea por línea
        for linea in archivo:
            # Limpiamos los saltos de línea al final
            linea = linea.strip()

            # Filtramos: si la línea continene [ERROR] o [CRITICAL], la procesamos
            if "[ERROR]" in linea or "[CRITICAL]" in linea:
                print(f"Alerta detectada: {linea}")

# Bloque principal para ejecutar nuestro script
if __name__ == "__main__":
    ruta = "servidor.log"
    procesar_logs(ruta)
    