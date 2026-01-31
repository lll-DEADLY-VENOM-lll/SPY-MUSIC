import re
from os import getenv
from dotenv import load_dotenv
from pyrogram import filters

# .env file load karein
load_dotenv()

# --------------------------
#    API & BOT CREDENTIALS
# --------------------------
API_ID = int(getenv("API_ID", "25610347"))
API_HASH = getenv("API_HASH", "c421be09ee9b9af3d13dbf9abb03483c")
BOT_TOKEN = getenv("BOT_TOKEN", "")  # .env mein bharein
MONGO_DB_URI = getenv("MONGO_DB_URI", "")  # .env mein bharein

# --------------------------
#    OWNER & LOGS
# --------------------------
LOGGER_ID = int(getenv("LOGGER_ID", "-1002512951867"))
OWNER_ID = int(getenv("OWNER_ID", "8140988754"))
BOT_USERNAME = getenv("BOT_USERNAME", "Annu_Music_Robot")

# --------------------------
#    COMMAND & REPO
# --------------------------
COMMAND_HANDLER = getenv("COMMAND_HANDLER", "! / .").split()
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
HEROKU_API_KEY = getenv("HEROKU_API_KEY")

UPSTREAM_REPO = getenv("UPSTREAM_REPO", "https://github.com/stkeditz/SpyMusic")
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "SPY")
GIT_TOKEN = getenv("GIT_TOKEN", None)

SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/about_deadly_venom")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/NOBITA_SUPPORT")

# --------------------------
#    DURATION & LIMITS
# --------------------------
def time_to_seconds(time_str):
    try:
        return sum(int(x) * 60**i for i, x in enumerate(reversed(str(time_str).split(":"))))
    except Exception:
        return 0

DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 54000))
SONG_DOWNLOAD_DURATION = int(getenv("SONG_DOWNLOAD_DURATION_LIMIT", "54000"))

DURATION_LIMIT = time_to_seconds(f"{DURATION_LIMIT_MIN}:00")
SONG_DOWNLOAD_DURATION_LIMIT = time_to_seconds(f"{SONG_DOWNLOAD_DURATION}:00")

# File size limits (Default 2GB)
TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", 2147483648))
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", 2147483648))

# --------------------------
#    SESSIONS (STRING)
# --------------------------
STRING1 = getenv("STRING_SESSION", "")
STRING2 = getenv("STRING_SESSION2", None)
STRING3 = getenv("STRING_SESSION3", None)
STRING4 = getenv("STRING_SESSION4", None)
STRING5 = getenv("STRING_SESSION5", None)

# --------------------------
#    BOT FEATURES
# --------------------------
AUTO_LEAVING_ASSISTANT = getenv("AUTO_LEAVING_ASSISTANT", "False").lower() == "true"
AUTO_SUGGESTION_MODE = getenv("AUTO_SUGGESTION_MODE", "True").lower() == "true"
AUTO_SUGGESTION_TIME = int(getenv("AUTO_SUGGESTION_TIME", "500"))
CLEANMODE_DELETE_MINS = int(getenv("CLEANMODE_MINS", "5"))
PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", 25))

# Spotify
SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", None)
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", None)

# --------------------------
#    IMAGES & UI
# --------------------------
# Ek hi image sab jagah use karne ke liye default link
BASE_URL = "https://files.catbox.moe/r1yejw.jpg"

START_IMG_URL = getenv("START_IMG_URL", "https://files.catbox.moe/r1yejw.jpg")
PING_IMG_URL = getenv("PING_IMG_URL", "https://files.catbox.moe/r1yejw.jpg")
PLAYLIST_IMG_URL = getenv("PLAYLIST_IMG_URL", "https://files.catbox.moe/r1yejw.jpg")
STATS_IMG_URL = getenv("STATS_IMG_URL", "https://files.catbox.moe/r1yejw.jpg")
TELEGRAM_AUDIO_URL = getenv("TELEGRAM_AUDIO_URL", "https://files.catbox.moe/r1yejw.jpg")
TELEGRAM_VIDEO_URL = getenv("TELEGRAM_VIDEO_URL", "https://files.catbox.moe/r1yejw.jpg")
STREAM_IMG_URL = getenv("STREAM_IMG_URL", "https://files.catbox.moe/r1yejw.jpg")
SOUNCLOUD_IMG_URL = getenv("SOUNCLOUD_IMG_URL", "https://files.catbox.moe/r1yejw.jpg")
YOUTUBE_IMG_URL = getenv("YOUTUBE_IMG_URL", "https://files.catbox.moe/r1yejw.jpg")
SPOTIFY_ARTIST_IMG_URL = getenv("SPOTIFY_ARTIST_IMG_URL", "https://files.catbox.moe/r1yejw.jpg")
SPOTIFY_ALBUM_IMG_URL = getenv("SPOTIFY_ALBUM_IMG_URL", "https://files.catbox.moe/r1yejw.jpg")
SPOTIFY_PLAYLIST_IMG_URL = getenv("SPOTIFY_PLAYLIST_IMG_URL", "https://files.catbox.moe/r1yejw.jpg")

# --------------------------
#    GLOBAL DICTIONARIES
# --------------------------
BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}
chatstats = {}
userstats = {}
clean = {}

# --------------------------
#    VALIDATION LOGIC
# --------------------------
if SUPPORT_CHANNEL and not re.match(r"(?:http|https)://", SUPPORT_CHANNEL):
    print("[ERROR] - SUPPORT_CHANNEL URL galat hai. Https se shuru hona chahiye.")

if SUPPORT_CHAT and not re.match(r"(?:http|https)://", SUPPORT_CHAT):
    print("[ERROR] - SUPPORT_CHAT URL galat hai. Https se shuru hona chahiye.")
