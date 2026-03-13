from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():

    incoming_msg = request.values.get("Body", "").lower()
    resp = MessagingResponse()
    msg = resp.message()

    if "hola" in incoming_msg:
        msg.body("Hola 👋 Bienvenido al restaurante.\n\nMenu:\n🍔 Hamburguesa - $10\n🍟 Papas - $5\n🥤 Soda - $3\n\nEscribe tu pedido.")
    else:
        msg.body("Recibimos tu mensaje 👍")

    return str(resp)

if __name__ == "__main__":
    app.run()