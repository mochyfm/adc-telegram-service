from flask import Flask, jsonify
from telethon import TelegramClient
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()
app = Flask(__name__)

api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")
group = os.getenv("TELEGRAM_GROUP")

@app.route("/messages", methods=["GET"])
def obtener_mensajes():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(obtener_mensajes_async())

async def obtener_mensajes_async():
    async with TelegramClient("mi_sesion", api_id, api_hash) as client:
        mensajes = await client.get_messages(group, limit=2)
        datos = [{
            "id": m.id,
            "texto": m.text,
            "usuario": m.sender_id,
            "fecha": m.date.isoformat()
        } for m in mensajes]
        return jsonify(datos)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
