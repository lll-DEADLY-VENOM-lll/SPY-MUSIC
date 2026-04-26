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

from typing import Union
from pyrogram import filters, types
from pyrogram.types import InlineKeyboardMarkup, Message

from Spy import app
from Spy.utils.database import get_lang
from Spy.utils.decorators.language import LanguageStart, languageCB
from Spy.utils.inline.help import (
    help_back_markup,
    private_help_panel,
    help_pannel_page1,
    help_pannel_page2,
    help_pannel_page3,
    help_pannel_page4,
)
from config import BANNED_USERS, START_IMG_URL, SUPPORT_CHAT
from strings import get_string, helpers

# =========================================================
# --- PRIVATE HELP HANDLER ---
# =========================================================

@app.on_message(filters.command(["help"]) & filters.private & ~BANNED_USERS)
@app.on_callback_query(filters.regex("help_page_1") & ~BANNED_USERS)
async def helper_private(client: app, update: Union[types.Message, types.CallbackQuery]):
    """
    Handles the /help command in private and also acts as the 
    handler for 'Page 1' of the help menu.
    """
    is_callback = isinstance(update, types.CallbackQuery)
    
    if is_callback:
        try:
            await update.answer()
        except:
            pass
        chat_id = update.message.chat.id
    else:
        try:
            await update.delete()
        except:
            pass
        chat_id = update.chat.id

    language = await get_lang(chat_id)
    _ = get_string(language)
    
    # Page 1 Keyboard
    keyboard = help_pannel_page1(_, iterate=is_callback)
    help_text = _["help_1"].format(SUPPORT_CHAT)

    if is_callback:
        await update.edit_message_text(help_text, reply_markup=keyboard)
    else:
        await update.reply_photo(
            photo=START_IMG_URL,
            caption=help_text,
            reply_markup=keyboard,
        )

# =========================================================
# --- GROUP HELP HANDLER ---
# =========================================================

@app.on_message(filters.command(["help"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def help_com_group(client, message: Message, _):
    """
    In groups, it sends a simple button directing the user to PM.
    """
    keyboard = private_help_panel(_)
    await message.reply_text(
        _["help_2"], 
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# =========================================================
# --- DYNAMIC MODULE HELP HANDLER ---
# =========================================================

@app.on_callback_query(filters.regex("help_callback") & ~BANNED_USERS)
@languageCB
async def helper_cb(client, CallbackQuery, _):
    """
    Dynamic handler for all module buttons (hb1, hb2...hb39).
    It automatically fetches the content from strings/helpers.py
    """
    callback_data = CallbackQuery.data.strip()
    cb = callback_data.split(None, 1)[1] # e.g., 'hb5'

    # Logic to decide which 'Back' button page to show
    def get_keyboard_for(cb_id):
        try:
            num = int(cb_id.replace("hb", ""))
            if 1 <= num <= 10:
                return help_back_markup(_, page=1)
            elif 11 <= num <= 21:
                return help_back_markup(_, page=2)
            elif 22 <= num <= 31:
                return help_back_markup(_, page=3)
            elif 32 <= num <= 40:
                return help_back_markup(_, page=4)
        except:
            pass
        return help_back_markup(_, page=1)

    # Fetching HELP_X from helpers file dynamically
    help_num = cb.replace("hb", "")
    content = getattr(helpers, f"HELP_{help_num}", None)

    if content:
        await CallbackQuery.edit_message_text(
            text=content, 
            reply_markup=get_keyboard_for(cb)
        )
    else:
        await CallbackQuery.answer(
            "⚠️ Help content for this module is missing!", 
            show_alert=True
        )

# =========================================================
# --- PAGE NAVIGATION HANDLER ---
# =========================================================

@app.on_callback_query(filters.regex(pattern=r"help_page_(2|3|4)") & ~BANNED_USERS)
@languageCB
async def nav_handler(client, CallbackQuery, _):
    """
    Switches between the help menu pages.
    """
    page_num = CallbackQuery.data.split("_")[-1]
    
    if page_num == "2":
        keyboard = help_pannel_page2(_)
    elif page_num == "3":
        keyboard = help_pannel_page3(_)
    elif page_num == "4":
        keyboard = help_pannel_page4(_)
    else:
        keyboard = help_pannel_page1(_)

    try:
        await CallbackQuery.edit_message_reply_markup(reply_markup=keyboard)
    except:
        pass

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
