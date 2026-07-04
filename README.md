# Analizador de Logs Inteligente con IA

Herramienta automatizada en Python que simula la auditoría de seguridad de un servidor a través de logs reales o de prueba (incluidos en el proyecto). El script lee archivos de registro (logs), filtra alertas críticas (`ERROR` y `CRITICAL`), utiliza la API de Google Gemini para generar reportes automáticos de ciberseguridad con recomendaciones de mitigación y, finalmente, guarda los reportes automáticamente en archivos .md.

## Características
* **Modo Interactivo (Bajo Demanda):** el usuario puede introducir dinámicamente la ruta de cualquier archivo de log del sistema que desee auditar.
* **Filtrado en tiempo real:** detección de anomalías y eventos críticos.
* **Integración con IA:** conexión con los modelos de última generación de Google GenAI.
* **Resiliencia (Fallback):** sistema de respaldo automático que conmuta entre 'gemini-2.5-flash' y 'gemini-1.5-flash' en caso de saturación del servicio.
* **Seguridad:** gestión de credenciales mediante variables de entorno.

## Instalación y Uso

Si quiere probar este proyecto localmente, siga estos pasos:

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/Andy-13A/analizador-logs-ia.git
   cd analizador-logs-ia
   ```


2. **Crear y activar el entorno virtual:**
   ```bash
   python -m venv env
   # En Windows:
   source env/Scripts/activate
   # En Mac/Linux:
   source env/bin/activate
   ```

3. **Instalar las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar las credenciales:**
- Renombre el archivo .env.example a .env.
- Consiga una API KEY gratuita en Google AI Studio.
- Coloque su clave dentro del archivo .env: GEMINI_API_KEY=tu_clave_real.

5. **Generar logs de prueva(Opcional):**
Si desea probar la herramienta con logs reales de su propio sistema, puede generar 
un volcado de su historial de Git ejecutando:
```bash
   git log --graph --oneline > historial_git.log
```

6. **Ejecutar el analizador**
   ```bash
    export $(cat .env | xargs)
    python main.py
    ```