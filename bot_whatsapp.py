# bot_whatsapp.py

import os
import json
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- Configuración de Google Sheets ---
# Leer credenciales desde la variable de entorno en Render
credentials_json = os.environ.get("GOOGLE_CREDENTIALS_JSON")
if not credentials_json:
    raise ValueError("No se encontró la variable de entorno GOOGLE_CREDENTIALS_JSON")

creds_dict = json.loads(credentials_json)
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Abrir tu hoja de Google Sheets (debe llamarse exactamente así)
sheet = client.open("Citas Bot").sheet1

# --- Configuración de Flask ---
app = Flask(__name__)

# --- Función para guardar cita ---
def guardar_cita(nombre, fecha, hora):
    sheet.append_row([nombre, fecha, hora])

# --- Ruta de WhatsApp ---
@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.values.get("Body", "").strip()
    resp = MessagingResponse()
    msg = resp.message()

    # Ejemplo simple: esperar "Hola"
    if incoming_msg.lower() == "hola":
        msg.body("Hola! Para agendar tu cita, envía: NOMBRE, FECHA, HORA")
    else:
        # Intentar parsear mensaje como cita: "Nombre, YYYY-MM-DD, HH:MM"
        try:
            partes = [p.strip() for p in incoming_msg.split(",")]
            if len(partes) == 3:
                nombre, fecha, hora = partes
                guardar_cita(nombre, fecha, hora)
                msg.body(f"Cita guardada correctamente:\n{nombre} - {fecha} {hora}")
            else:
                msg.body("Formato inválido. Envía: NOMBRE, FECHA, HORA")
        except Exception as e:
            msg.body("Ocurrió un error al guardar la cita. Intenta de nuevo.")

    return str(resp)

# --- Ejecutar Flask ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
