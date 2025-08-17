import asyncio
import logging
import os
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.errors import ChatAdminRequiredError

from keep_alive import keep_alive

# 🔧 Config (tumhare diye gaye details)
API_ID = 25345584
API_HASH = "720f7fbca5c0153352a24db49b18db7e"
STRING_SESSION = os.getenv("STRING_SESSION")  # ye tumhe khud banana hoga
SOURCE_CHANNEL = -1001850921369
TARGET_CHANNEL = -1003048336639

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("userbot")

# keep Render alive
keep_alive()

client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)


async def copy_message(message):
    try:
        if message.media:
            data = await client.download_media(message=message, file=bytes)
            if data:
                await client.send_file(
                    TARGET_CHANNEL,
                    data,
                    caption=message.text or "",
                    entities=message.entities,
                    supports_streaming=True,
                )
                logger.info("✅ Media copied successfully")
        elif message.text:
            await client.send_message(
                TARGET_CHANNEL,
                message.text,
                entities=message.entities,
                link_preview=False,
            )
            logger.info("✅ Text copied successfully")
    except ChatAdminRequiredError:
        logger.error("❌ Bot is not admin in target channel!")
    except Exception as e:
        logger.exception(f"⚠️ Error while copying message: {e}")


@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def handler(event):
    msg = event.message
    if msg.grouped_id:  # Albums handled together
        return
    await copy_message(msg)


@client.on(events.Album(chats=SOURCE_CHANNEL))
async def handler_album(event):
    try:
        files = []
        caption = None
        for msg in event.messages:
            data = await client.download_media(message=msg, file=bytes)
            if data:
                files.append(data)
            if (msg.text or msg.message) and not caption:
                caption = msg.text
        if files:
            await client.send_file(TARGET_CHANNEL, files, caption=caption or "")
            logger.info("✅ Album copied successfully")
    except Exception as e:
        logger.exception(f"⚠️ Error handling album: {e}")


async def main():
    await client.start()
    logger.info("🚀 Userbot is live and copying messages!")
    await asyncio.Event().wait()


if __name__ == "__main__":
    try:
        client.loop.run_until_complete(main())
    except KeyboardInterrupt:
        logger.info("👋 Shutting down...")
