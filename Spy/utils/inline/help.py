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


@app.on_message(filters.command(["help"]) & filters.private & ~BANNED_USERS)
@app.on_callback_query(filters.regex("help_page_1") & ~BANNED_USERS)
async def helper_private(
    client: app, update: Union[types.Message, types.CallbackQuery]
):
    is_callback = isinstance(update, types.CallbackQuery)
    if is_callback:
        try:
            await update.answer()
        except:
            pass
        chat_id = update.message.chat.id
        language = await get_lang(chat_id)
        _ = get_string(language)
        # Using Page 1 logic from your Srishti style
        keyboard = help_pannel_page1(_, True)
        await update.edit_message_text(
            _["help_1"].format(SUPPORT_CHAT), reply_markup=keyboard
        )
    else:
        try:
            await update.delete()
        except:
            pass
        language = await get_lang(update.chat.id)
        _ = get_string(language)
        keyboard = help_pannel_page1(_)
        await update.reply_photo(
            photo=START_IMG_URL,
            caption=_["help_1"].format(SUPPORT_CHAT),
            reply_markup=keyboard,
        )


@app.on_message(filters.command(["help"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def help_com_group(client, message: Message, _):
    keyboard = private_help_panel(_)
    await message.reply_text(_["help_2"], reply_markup=InlineKeyboardMarkup(keyboard))


@app.on_callback_query(filters.regex("help_callback") & ~BANNED_USERS)
@languageCB
async def helper_cb(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    cb = callback_data.split(None, 1)[1]

    # Helper function matching your Srishti Music logic
    def get_keyboard_for(cb_id):
        page1 = ["hb1", "hb2", "hb3", "hb4", "hb5", "hb6", "hb7", "hb8", "hb9", "hb10"]
        page2 = ["hb11", "hb12", "hb13", "hb14", "hb15", "hb16", "hb17", "hb18", "hb19", "hb20", "hb21"]
        page3 = ["hb22", "hb23", "hb24", "hb25", "hb26", "hb27", "hb28", "hb29", "hb30", "hb31"]
        page4 = ["hb32", "hb33", "hb34", "hb35", "hb36", "hb37", "hb38", "hb39"]

        if cb_id in page1:
            return help_back_markup(_, page=1)
        elif cb_id in page2:
            return help_back_markup(_, page=2)
        elif cb_id in page3:
            return help_back_markup(_, page=3)
        elif cb_id in page4:
            return help_back_markup(_, page=4)
        else:
            return help_back_markup(_, page=1)

    # Dynamic help content fetcher (optimized version of hb1...hb39)
    help_num = cb.replace("hb", "")
    content = getattr(helpers, f"HELP_{help_num}", None)

    if content:
        await CallbackQuery.edit_message_text(
            content, 
            reply_markup=get_keyboard_for(cb)
        )
    else:
        await CallbackQuery.answer("⚠️ Help Module Not Found!", show_alert=True)

# Navigation for Pages 2, 3, and 4
@app.on_callback_query(filters.regex(pattern=r"help_page_(2|3|4)") & ~BANNED_USERS)
@languageCB
async def nav_handler(client, CallbackQuery, _):
    page_num = CallbackQuery.data.split("_")[-1]
    if page_num == "2":
        keyboard = help_pannel_page2(_)
    elif page_num == "3":
        keyboard = help_pannel_page3(_)
    elif page_num == "4":
        keyboard = help_pannel_page4(_)
    else:
        keyboard = help_pannel_page1(_, True)
    
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
