from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from telethon import TelegramClient
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# ✅ CORS habilitado
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Reemplaza por tu dominio en producción si quieres
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")
group = os.getenv("TELEGRAM_GROUP")

@app.get("/messages")
async def obtener_mensajes():
    async with TelegramClient("mi_sesion", api_id, api_hash) as client:
        mensajes = await client.get_messages(group, limit=2)
        return [
            {
                "id": m.id,
                "texto": m.text,
                "usuario": m.sender_id,
                "fecha": m.date.isoformat(),
            }
            for m in mensajes
        ]

# ✅ Arranque condicional
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))  # usa el puerto del entorno o 8000 por defecto
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
