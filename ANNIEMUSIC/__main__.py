import os
os.environ["PYTHONUNBUFFERED"] = "1"  # Force real-time logging
os.environ["PORT"] = os.getenv("PORT", "10000")  # Ensure PORT is set

# IMMEDIATE PORT BINDING - CRITICAL FOR RENDER
import sys
import socket
import threading

PORT = int(os.environ["PORT"])

def bind_port_immediately():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('0.0.0.0', PORT))
        s.listen(5)
        print(f"✅ [PORT BINDER] Successfully bound to 0.0.0.0:{PORT}")
        sys.stdout.flush()
        
        while True:
            try:
                conn, addr = s.accept()
                # Minimal HTTP response to satisfy Render
                response = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/plain\r\n"
                    "Connection: close\r\n\r\n"
                    "Annie Music Bot is starting..."
                )
                conn.send(response.encode())
                conn.close()
            except Exception as e:
                print(f"⚠️ [PORT BINDER] Connection error: {str(e)}")
                sys.stdout.flush()
    except Exception as e:
        print(f"❌ [PORT BINDER CRITICAL] Failed to bind port: {str(e)}")
        sys.stdout.flush()
        # Attempt restart after delay
        threading.Timer(2.0, bind_port_immediately).start()

# Start binding in a separate thread immediately
threading.Thread(target=bind_port_immediately, daemon=True).start()

# REST OF YOUR APPLICATION
import asyncio
import importlib
import time
from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall
import config
from ANNIEMUSIC import LOGGER, app, userbot
from ANNIEMUSIC.core.call import JARVIS
from ANNIEMUSIC.misc import sudo
from ANNIEMUSIC.plugins import ALL_MODULES
from ANNIEMUSIC.utils.database import get_banned_users, get_gbanned
from ANNIEMUSIC.utils.cookie_handler import fetch_and_store_cookies 
from config import BANNED_USERS

# Proper health check server (starts after bot initializes)
def start_health_server():
    from flask import Flask
    health_app = Flask(__name__)
    
    @health_app.route('/')
    def root_check():
        return "Annie Music Bot is fully operational", 200
    
    @health_app.route('/live')
    def live_status():
        return "Bot is running smoothly", 200
    
    health_app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

async def init():
    # Indicate that bot initialization has started
    print("🚀 Starting Annie Music Bot initialization...")
    
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("Assistant sessions not filled!")
        exit()

    # Try to fetch cookies at startup
    try:
        await fetch_and_store_cookies()
        LOGGER("ANNIEMUSIC").info("YouTube cookies loaded ✅")
    except Exception as e:
        LOGGER("ANNIEMUSIC").warning(f"Cookie error: {e}")

    await sudo()

    # Load banned users
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except Exception as e:
        LOGGER("ANNIEMUSIC").warning(f"Ban list error: {e}")

    # Start the main bot
    await app.start()
    
    # Load plugins
    for all_module in ALL_MODULES:
        importlib.import_module("ANNIEMUSIC.plugins" + all_module)
    LOGGER("ANNIEMUSIC.plugins").info("Modules loaded...")

    # Start userbot and core
    await userbot.start()
    await JARVIS.start()

    # Test voice call
    try:
        await JARVIS.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("ANNIEMUSIC").error("Voice chat not enabled in log group!")
        exit()
    except Exception as e:
        LOGGER("ANNIEMUSIC").warning(f"Stream test error: {e}")

    # Final initialization
    await JARVIS.decorators()
    LOGGER("ANNIEMUSIC").info("Annie Music Bot Started Successfully")
    
    # Start proper health server
    health_thread = threading.Thread(target=start_health_server)
    health_thread.daemon = True
    health_thread.start()
    print("✅ Health server started on port 5000")
    
    # Keep the bot running
    await idle()
    
    # Cleanup on stop
    await app.stop()
    await userbot.stop()
    LOGGER("ANNIEMUSIC").info("Stopping Annie Music Bot...")

if __name__ == "__main__":
    # Add startup delay if needed for Render
    if os.getenv('RENDER'):
        print("⏳ Initializing on Render - adding 5s startup delay...")
        time.sleep(5)
    
    asyncio.get_event_loop().run_until_complete(init())
