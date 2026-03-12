from flask import Flask, request
import requests

app = Flask(__name__)

# -------------------
# Menú de prueba
# -------------------
menu = {
    "hamburguesa": 12000,
    "pizza": 18000,
    "ensalada": 8000,
    "refresco": 4000
}

# -------------------
# Número de Twilio
# -------------------
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"  # número de sandbox de Twilio
TWILIO_ACCOUNT_SID = "TU_ACCOUNT_SID"
TWILIO_AUTH_TOKEN = "TU_AUTH_TOKEN"

# Función para enviar mensaje vía Twilio
def enviar_mensaje(to, mensaje):
    url = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json"
    data = {
        "From": TWILIO_WHATSAPP_NUMBER,
        "To": to,
        "Body": mensaje
    }
    requests.post(url, data=data, auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN))

# -------------------
# Endpoint para WhatsApp
# -------------------
@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    datos = request.form
    numero_cliente = datos.get("From")
    mensaje_cliente = datos.get("Body")

    mensaje_lower = mensaje_cliente.lower()

    # Buscar items del menú en el mensaje
    orden = []
    for item in menu:
        if item in mensaje_lower:
            orden.append(item)

    if not orden:
        respuesta = "No reconocí ningún plato en tu mensaje. Nuestro menú es: " + ", ".join(menu.keys())
    else:
        total = sum([menu[i] for i in orden])
        respuesta = f"Tu pedido: {', '.join(orden)}\nTotal: {total} COP\nResponde 'sí' para confirmar tu pedido."

    enviar_mensaje(numero_cliente, respuesta)
    return "OK", 200

# -------------------
# Ejecutar bot
# -------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)