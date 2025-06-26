from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.types import PeerChannel
from telethon.utils import get_peer_id
from dotenv import load_dotenv
import os

from cache import init_cache, get_peer_id_from_cache, save_peer_id_to_cache
from scheduler import iniciar_scheduler

load_dotenv()
init_cache()
iniciar_scheduler()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")
string_session = os.getenv("TELEGRAM_SESSION")
group_key = os.getenv("TELEGRAM_GROUP")
default_limit = int(os.getenv("TELEGRAM_MSG_LIMIT", 2))

@app.get("/messages")
async def get_messages(request: Request):
    limit_param = request.query_params.get("limit")
    try:
        limit = int(limit_param) if limit_param else default_limit
    except ValueError:
        limit = default_limit

    async with TelegramClient(StringSession(string_session), api_id, api_hash) as client:
        cached = get_peer_id_from_cache(group_key)

        if cached:
            entity = PeerChannel(int(cached))
            print("✅ Using cached peer_id:", cached)
        else:
            print("🔍 Resolving group...")
            entity = await client.get_input_entity(group_key)
            peer_id = get_peer_id(entity)
            save_peer_id_to_cache(group_key, str(peer_id))
            print("✅ Cached:", peer_id)

        messages = await client.get_messages(entity, limit=limit)
        results = []

        for msg in messages:
            media_type = None
            if msg.photo:
                media_type = "image"
            elif msg.document:
                media_type = "file"

            results.append({
                "id": msg.id,
                "text": msg.text,
                "user": msg.sender_id,
                "date": msg.date.isoformat(),
                "media_type": media_type
            })

        return results
