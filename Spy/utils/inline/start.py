from pyrogram.types import InlineKeyboardButton
import config
from Spy import app

# ------------------------------------------------------------------------ #
# PREMIUM START & PRIVATE PANELS
# ------------------------------------------------------------------------ #

def start_panel(_):
    """
    Groups ke liye ek balanced 2-column layout.
    """
    buttons = [
        [
            InlineKeyboardButton(
                text=f"➕ {_['S_B_1']}", 
                url=f"https://t.me/{app.username}?startgroup=true"
            ),
            InlineKeyboardButton(
                text=f"💬 {_['S_B_2']}", 
                url=config.SUPPORT_CHAT
            ),
        ],
    ]
    return buttons


def private_panel(_):
    """
    Private Chat ke liye Full-Width aur Grid mix layout.
    Isme buttons zyada attractive aur clean dikhte hain.
    """
    buttons = [
        [
            InlineKeyboardButton(
                text=f"✨ {_['S_B_3']}",
                url=f"https://t.me/{app.username}?startgroup=true",
            )
        ],
        [
            InlineKeyboardButton(
                text=f"🛡️ {_['S_B_2']}", 
                callback_data="shiv_aarumi"
            ),
            InlineKeyboardButton(
                text="🎬 ʏᴛ-ᴀᴘɪ", 
                callback_data="bot_info_data"
            ),
        ],
        [
            InlineKeyboardButton(
                text=f"📖 {_['S_B_4']}", 
                callback_data="settings_back_helper"
            )
        ],
    ]
    return buttons

# ------------------------------------------------------------------------ #
# DESIGN NOTES:
# 1. 1st Row: 'Add Me' button ko full width rakha hai focus ke liye.
# 2. 2nd Row: Grid system (2 buttons) taaki screen space bache.
# 3. 3rd Row: Help/Commands ko alag se highlight kiya hai.
# 4. Logic: Callback data (shiv_aarumi, bot_info_data) ko touch nahi kiya.
# ----------------------------> BY DIL <---------------------------------- #
