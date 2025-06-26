from apscheduler.schedulers.background import BackgroundScheduler
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.utils import get_peer_id
from dotenv import load_dotenv
import asyncio
import os

from cache import get_peer_id_from_cache, save_peer_id_to_cache

load_dotenv()

api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")
string_session = os.getenv("TELEGRAM_SESSION")
group_key = os.getenv("TELEGRAM_GROUP")

def actualizar_peer_id():
    print("🔁 Verificando peer_id actualizado...")

    # ✅ Crear event loop manualmente
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(ejecutar_actualizacion())

async def ejecutar_actualizacion():
    from telethon.tl.types import PeerChannel

    async with TelegramClient(StringSession(string_session), api_id, api_hash) as client:
        nuevo_entity = await client.get_input_entity(group_key)
        nuevo_id = str(get_peer_id(nuevo_entity))

        cacheado = get_peer_id_from_cache(group_key)

        if nuevo_id != cacheado:
            save_peer_id_to_cache(group_key, nuevo_id)
            print(f"✅ peer_id actualizado: {cacheado} → {nuevo_id}")
        else:
            print("✅ peer_id sin cambios.")

def iniciar_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(actualizar_peer_id, "interval", minutes=2)
    scheduler.start()
    print("🕒 Scheduler activo cada 2 minutos.")
