# Copyright (c) 2026 Kiru <Kiru_OP>
# Location: Varanasi, Uttar Pradesh, India
#
# All rights reserved.
#
# This code is the intellectual property of Kiru Sanatani.
# Unauthorized use, copying, modification, or distribution of this
# code, in whole or in part, is strictly prohibited without prior
# written permission from the owner.
#
# Permissions:
# - Allowed for personal learning and educational purposes only
# - Contributions are welcome via pull requests with proper credit
#
# Restrictions:
# - Do not claim this code as your own
# - Do not re-upload or redistribute without permission
# - Commercial use is strictly prohibited
#
# For permissions or inquiries:
# Email: np564605@gmail.com

from pyrogram.types import InlineKeyboardButton
import config
from Spy import app

def start_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_1"], url=f"https://t.me/{app.username}?startgroup=true"
            ),
        ],
        [
            InlineKeyboardButton(text=_["S_B_2"], url=config.SUPPORT_CHAT),
            InlineKeyboardButton(text=_["S_B_3"], url=config.SUPPORT_CHAT), # Yahan apna channel link daal sakte hain
        ],
    ]
    return buttons

def private_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_1"],
                url=f"https://t.me/{app.username}?startgroup=true",
            )
        ],
        [
            InlineKeyboardButton(text=_["S_B_5"], callback_data="settings_helper"),
        ],
        [
            InlineKeyboardButton(text=_["S_B_2"], url=config.SUPPORT_CHAT),
            InlineKeyboardButton(text=_["S_B_9"], url=config.SUPPORT_CHAT),
        ],
        [
            InlineKeyboardButton(text=_["S_B_6"], url=config.UPSTREAM_REPO),
        ],
    ]
    return buttons

# ╔══════════════════════════════════════╗
#        ©️ 2026 𝙆𝙞𝙧𝙪 𝙎𝙖𝙣𝙖𝙩𝙖𝙣𝙞 (@Kiru_OP)
# ╚══════════════════════════════════════╝
#
# 🔗 GitHub Repository :
# https://github.com/lll-DEADLY-VENOM-lll/SPY-MUSIC
#
# 📢 Telegram Channel :
# https://t.me/about_deadly_venom
#
# ──────────────────────────────────────
# ❤️ Powered By 𝙎𝙥𝙮 𝙈𝙪𝙨𝙞𝙘 | 𝙆𝙞𝙧𝙪 𝙊𝙋
# ──────────────────────────────────────
