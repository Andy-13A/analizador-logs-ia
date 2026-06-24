import os
from google import genai

"""
Esta función toma una línea de log "peligrosa", se la envía a Gemini y devuelve el análisis de la IA
"""
def analizar_con_ia(linea_log):
    # 1. Inicializamos el cliente de Google GenAI
    # Automáticamente leerá la clave desde el entorno/consola
    client = genai.Client()

    # 2. Diseñamos el "prompt" que le enviaremos a la IA
    prompt = f"""
    Actúa como un experto en ciberseguridad y administrador de sistemas.
    Analiza la siguiente línea de log que ha generado una alerta en nuestro servidor:
    "{linea_log}"

    Por favor, porporciona una respuesta clara yb concisa en formato texto con los siguientes puntos:
    1. Explicación de qué está ocurriendo (de forma sencilla y comprensible).
    2. Nivel de peligro real (Bajo, MNedio, Alto, Crítico).
    3. Recomendaciones de acción inmediata que debe tomar el equipo técnico para mitigar el riesgo.
    4. Cualquier otra información relevante que pueda ayudar a entender la situación.
    """

    # 3. Hacemos la llamada al modelo de IA
    try:
        respuesta = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        #Devolvemos el texto que nos ha respondido la IA
        return respuesta.text
    except Exception as e:
        print(f"Modelo 2.5 saturado o no disponible. Probando modelo de respaldo...")
        
        try:
            respuesta = client.models.generate_content(
                model='gemini-1.5-flash',  # Modelo de respaldo
                contents=prompt,
            )
            return respuesta.text
        except Exception as e_backup:
            return f"Error crítico: Ambos modelos de IA están inaccesibles. Detalles: {e_backup}"

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
                print("Consultando con el analista de IA...")

                reporte_ia = analizar_con_ia(linea)

                print("\n === REPORTE DE LA IA ===")
                print(reporte_ia)
                print("-" * 60 + "\n")

# Bloque principal para ejecutar nuestro script
if __name__ == "__main__":
    ruta = "servidor.log"
    procesar_logs(ruta)
    