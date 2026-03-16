import math
from pyrogram.types import InlineKeyboardButton
from Spy.utils.formatters import time_to_seconds

# ------------------------------------------------------------------------ #
# PLAYER MARKUPS WITH DOWNLOAD OPTIONS - DESIGNED BY DIL
# ------------------------------------------------------------------------ #

def track_markup(_, videoid, user_id, channel, fplay):
    """Buttons for Streaming and Downloading."""
    buttons = [
        [
            InlineKeyboardButton(text="🎵 ᴘʟᴀʏ ᴀᴜᴅɪᴏ", callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}"),
            InlineKeyboardButton(text="🎥 ᴘʟᴀʏ ᴠɪᴅᴇᴏ", callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}")
        ],
        [
            InlineKeyboardButton(text="📥 ᴅᴏᴡɴʟᴏᴀᴅ ᴀᴜᴅɪᴏ", callback_data=f"MusicDownload {videoid}|{user_id}|a"),
            InlineKeyboardButton(text="📥 ᴅᴏᴡɴʟᴏᴀᴅ ᴠɪᴅᴇᴏ", callback_data=f"MusicDownload {videoid}|{user_id}|v")
        ],
        [
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data=f"forceclose {videoid}|{user_id}")
        ],
    ]
    return buttons


def stream_markup_timer(_, chat_id, played, dur):
    """Main player with timer, original icons, and Download option."""
    played_sec = time_to_seconds(played)
    duration_sec = time_to_seconds(dur)
    
    percentage = (played_sec / duration_sec) * 100
    umm = math.floor(percentage)
    
    # Heart Bar Logic
    bar_length = 10
    filled_pos = int((umm / 100) * (bar_length - 1))
    bar = "".join(["╌" if i != filled_pos else "♡" for i in range(bar_length)])
    
    buttons = [
        [
            InlineKeyboardButton(text=f"{played} {bar} {dur}", callback_data="GetTimer")
        ],
        [
            InlineKeyboardButton(text="▷", callback_data=f"ADMIN Resume|{chat_id}"),
            InlineKeyboardButton(text="II", callback_data=f"ADMIN Pause|{chat_id}"),
            InlineKeyboardButton(text="‣‣I", callback_data=f"ADMIN Skip|{chat_id}"),
            InlineKeyboardButton(text="▢", callback_data=f"ADMIN Stop|{chat_id}"),
        ],
        [
            InlineKeyboardButton(text="↻ ʀᴇᴘʟᴀʏ", callback_data=f"ADMIN Replay|{chat_id}"),
            InlineKeyboardButton(text="📥 ᴅʟ", callback_data=f"add_playlist {chat_id}"), # Yahan aap download menu link kar sakte hain
            InlineKeyboardButton(text="✗ ᴄʟᴏsᴇ", callback_data="close")
        ],
    ]
    return buttons


def stream_markup(_, chat_id):
    """Simple player controls."""
    buttons = [
        [
            InlineKeyboardButton(text="▷", callback_data=f"ADMIN Resume|{chat_id}"),
            InlineKeyboardButton(text="II", callback_data=f"ADMIN Pause|{chat_id}"),
            InlineKeyboardButton(text="↻", callback_data=f"ADMIN Replay|{chat_id}"),
            InlineKeyboardButton(text="‣‣I", callback_data=f"ADMIN Skip|{chat_id}"),
            InlineKeyboardButton(text="▢", callback_data=f"ADMIN Stop|{chat_id}"),
        ],
        [InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close")],
    ]
    return buttons


def playlist_markup(_, videoid, user_id, ptype, channel, fplay):
    """Playlist selection markup."""
    buttons = [
        [
            InlineKeyboardButton(text=_["P_B_1"], callback_data=f"SagarPlaylists {videoid}|{user_id}|{ptype}|a|{channel}|{fplay}"),
            InlineKeyboardButton(text=_["P_B_2"], callback_data=f"SagarPlaylists {videoid}|{user_id}|{ptype}|v|{channel}|{fplay}"),
        ],
        [
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data=f"forceclose {videoid}|{user_id}"),
        ],
    ]
    return buttons


def livestream_markup(_, videoid, user_id, mode, channel, fplay):
    """Live stream markup."""
    buttons = [
        [
            InlineKeyboardButton(text=_["P_B_3"], callback_data=f"LiveStream {videoid}|{user_id}|{mode}|{channel}|{fplay}"),
        ],
        [
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data=f"forceclose {videoid}|{user_id}"),
        ],
    ]
    return buttons


def slider_markup(_, videoid, user_id, query, query_type, channel, fplay):
    """Slider markup with Stream and Download buttons."""
    query = f"{query[:20]}"
    buttons = [
        [
            InlineKeyboardButton(text="🎵 ᴀᴜᴅɪᴏ", callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}"),
            InlineKeyboardButton(text="🎥 ᴠɪᴅᴇᴏ", callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}"),
        ],
        [
            InlineKeyboardButton(text="📥 ᴅʟ ᴀᴜᴅɪᴏ", callback_data=f"MusicDownload {videoid}|{user_id}|a"),
            InlineKeyboardButton(text="📥 ᴅʟ ᴠɪᴅᴇᴏ", callback_data=f"MusicDownload {videoid}|{user_id}|v")
        ],
        [
            InlineKeyboardButton(text="◁", callback_data=f"slider B|{query_type}|{query}|{user_id}|{channel}|{fplay}"),
            InlineKeyboardButton(text="🗑️", callback_data=f"forceclose {query}|{user_id}"),
            InlineKeyboardButton(text="▷", callback_data=f"slider F|{query_type}|{query}|{user_id}|{channel}|{fplay}"),
        ],
    ]
    return buttons

# ----------------------------> INFO <----------------------------- #
"""
✅ Added: Audio & Video Download buttons.
✅ Symbols: Restored ▷, II, ‣‣I, ▢, ◁, ▷.
💎 Design: Premium Grid Layout by Dil.
"""
