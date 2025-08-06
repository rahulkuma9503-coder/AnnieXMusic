# ABSOLUTE FIRST LINES - CRITICAL FOR RENDER
import os
os.environ["PYTHONUNBUFFERED"] = "1"  # Force real-time logging
import ANNIEMUSIC._render_port_fast  # MUST BE FIRST IMPORT

# REST OF EXISTING CODE
from ANNIEMUSIC.core.bot import JARVIS
from ANNIEMUSIC.core.dir import dirr
from ANNIEMUSIC.core.git import git
from ANNIEMUSIC.core.userbot import Userbot
from ANNIEMUSIC.misc import dbb, heroku

from .logging import LOGGER

# Initialize core components
dirr()
git()
dbb()
heroku()

# Create bot instances
app = JARVIS()
userbot = Userbot()

# Health check function
def health_status():
    """Simple health check for monitoring"""
    return "Operational" if app and userbot else "Initializing"

# Import platform APIs
from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()

# Startup message
print("✅ Bot core initialized - Port binding active")
