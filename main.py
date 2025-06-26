from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from telethon import TelegramClient
from telethon.sessions import StringSession
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# ✅ CORS habilitado
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")
group = os.getenv("TELEGRAM_GROUP")
string_session = os.getenv("TELEGRAM_SESSION")

@app.get("/messages")
async def obtener_mensajes():
    async with TelegramClient(StringSession(string_session), api_id, api_hash) as client:
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

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
