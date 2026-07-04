from datetime import datetime
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
    # Verificamos si el archivo existe antes de intentar abrirlo
    if not os.path.exists(ruta_archivo):
        print(f"Error: El archivo en la ruta '{ruta_archivo}' no existe.")
        return
    
    # Creamos la carpeta de reportes si no existe
    carpeta_reportes = "reportes"
    if not os.path.exists(carpeta_reportes):
        os.makedirs(carpeta_reportes)
        print(f"Carpeta '{carpeta_reportes}' creada para almacenar los reportes.")

    print(f"--- Iniciando análisis del archivo: {ruta_archivo} ---")

    alertas_encontradas = 0
    # Abrimos el archivo en modo lectura ('r') y especificamos la codificación UTF-8
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        # Leemos el archivo línea por línea
        for linea in archivo:
            # Limpiamos los saltos de línea al final
            linea = linea.strip()

            # Filtramos: si la línea continene [ERROR] o [CRITICAL], la procesamos
            if "[ERROR]" in linea or "[CRITICAL]" in linea:
                alertas_encontradas += 1
                print(f"Alerta detectada: {linea}")
                print("Consultando con el analista de IA...")

                # Obtenemos el análisis de la IA
                reporte_ia = analizar_con_ia(linea)

                print("\n === REPORTE DE LA IA ===")
                print(reporte_ia)

                # Generamos una marca de tiempo única (AñoMesDía_HoraMinutoSegundo)
                marca_tiempo = datetime.now().strftime("%Y%m%d_%H%M%S")

                # Construimos la ruta apuntando a la carpeta especídfica con el nombre único
                nombre_archivo = f"reporte_{marca_tiempo}_alerta_{alertas_encontradas}.md"
                ruta_final_reporte = os.path.join(
                    carpeta_reportes, nombre_archivo
                )

                # Guardamos el reporte de la IA en su ubicación correspondiente
                try:
                    with open(
                        ruta_final_reporte, "w", encoding="utf-8"
                    ) as archivo_alerta:
                        archivo_alerta.write(
                            f"# Reporte de Auditoría de Seguridad\n\n"
                        )
                        archivo_alerta.write(
                            f"**Línea de log analizada:**\n`{linea}`\n\n"
                        )
                        archivo_alerta.write(f"## Análisis de la IA:\n")
                        archivo_alerta.write(reporte_ia)
                    print(
                        f"💾 ¡Reporte guardado con éxito en: {ruta_final_reporte}!"
                    )
                except Exception as e_file:
                    print(
                        f"⚠️ No se pudo guardar el archivo del reporte: {e_file}"
                    )

                print("-" * 60 + "\n")

    if alertas_encontradas == 0:
        print("No se encontraron alertas críticas o de error en el archivo de logs.")
    
    print(f"--- Análisis completado. Total de alertas encontradas: {alertas_encontradas} ---")

# Bloque principal para ejecutar nuestro script
if __name__ == "__main__":
    print("==================================================================")
    print("      ========= ANALIZADOR DE LOGS INTELIGENTE =========")
    print("==================================================================")

    # Solicitamos la ruta al usuario de forma dinámica
    ruta_usuario = input("Por favor, ingresa la ruta del archivo de logs a analizar (por ejemplo, 'servidor.log'): ").strip()

    # Limpiamos posibles comillas que el usuario pueda haber agregadoue se añaden al arrastraar archivos a la terminal
    ruta_usuario = ruta_usuario.strip("'\'")

    procesar_logs(ruta_usuario)
    