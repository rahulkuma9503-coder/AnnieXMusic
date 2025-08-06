from ANNIEMUSIC.core.bot import JARVIS
from ANNIEMUSIC.core.dir import dirr
from ANNIEMUSIC.core.git import git
from ANNIEMUSIC.core.userbot import Userbot
from ANNIEMUSIC.misc import dbb, heroku

from .logging import LOGGER

# Initialize core components
dirr()       # Directory setup
git()        # Git version check
dbb()        # Database setup
heroku()     # Heroku config (if applicable)

# Create bot instances
app = JARVIS()
userbot = Userbot()

# Add this new function for health checks
def check_health():
    """Simple health check for Render"""
    return "OK" if app and userbot else "Initializing"

# Import platform APIs
from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()

# Critical addition for Render port binding
import os
if os.getenv('RENDER'):
    # Ensure immediate port binding happens first
    from ANNIEMUSIC import immediate_port_binder
