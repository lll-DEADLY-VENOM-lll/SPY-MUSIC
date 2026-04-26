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
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from Spy import app
from Spy.utils.database import get_lang
from Spy.utils.decorators.language import LanguageStart, languageCB
from config import BANNED_USERS, START_IMG_URL, SUPPORT_CHAT
from strings import get_string, helpers

# ──────────────────────────────────────────────────────────────
# 1. KEYBOARD MARKUPS (Buttons Definition)
# ──────────────────────────────────────────────────────────────

def help_pannel_page1(_, is_callback=False):
    buttons = [
        [
            InlineKeyboardButton(text="Aᴅᴍɪɴ", callback_data="help_callback hb1"),
            InlineKeyboardButton(text="Aᴜᴛʜ", callback_data="help_callback hb2"),
            InlineKeyboardButton(text="Bʟᴀᴄᴋʟɪsᴛ", callback_data="help_callback hb3"),
        ],
        [
            InlineKeyboardButton(text="Bʀᴏᴀᴅᴄᴀsᴛ", callback_data="help_callback hb4"),
            InlineKeyboardButton(text="G-Bᴀɴ", callback_data="help_callback hb12"),
            InlineKeyboardButton(text="Lʏʀɪᴄs", callback_data="help_callback hb5"),
        ],
        [
            InlineKeyboardButton(text="Pʟᴀʏɪɴɢ", callback_data="help_callback hb6"),
            InlineKeyboardButton(text="Pʟᴀʏʟɪsᴛ", callback_data="help_callback hb7"),
            InlineKeyboardButton(text="Vɪᴅᴇᴏ-Cʜᴀᴛ", callback_data="help_callback hb8"),
        ],
        [
            InlineKeyboardButton(text="Sᴛᴀᴛs", callback_data="help_callback hb9"),
            InlineKeyboardButton(text="Sᴜᴅᴏ", callback_data="help_callback hb10"),
            InlineKeyboardButton(text="Sᴛᴀʀᴛ", callback_data="help_callback hb11"),
        ],
        [
            InlineKeyboardButton(text="➡", callback_data="help_page_2"),
        ],
    ]
    return InlineKeyboardMarkup(buttons)

def help_pannel_page2(_):
    buttons = [
        [
            InlineKeyboardButton(text="Mᴜᴛᴇ", callback_data="help_callback hb13"),
            InlineKeyboardButton(text="Pᴀᴜsᴇ", callback_data="help_callback hb14"),
            InlineKeyboardButton(text="Rᴇsᴜᴍᴇ", callback_data="help_callback hb15"),
        ],
        [
            InlineKeyboardButton(text="Sᴋɪᴘ", callback_data="help_callback hb16"),
            InlineKeyboardButton(text="Sᴛᴏᴘ", callback_data="help_callback hb17"),
            InlineKeyboardButton(text="Pɪɴɢ", callback_data="help_callback hb18"),
        ],
        [
            InlineKeyboardButton(text="⬅", callback_data="help_page_1"),
            InlineKeyboardButton(text="➡", callback_data="help_page_3"),
        ],
    ]
    return InlineKeyboardMarkup(buttons)

def help_pannel_page3(_):
    buttons = [
        [
            InlineKeyboardButton(text="Exᴛʀᴀ", callback_data="help_callback hb22"),
            InlineKeyboardButton(text="Gʀᴏᴜᴘ", callback_data="help_callback hb23"),
        ],
        [
            InlineKeyboardButton(text="⬅", callback_data="help_page_2"),
            InlineKeyboardButton(text="➡", callback_data="help_page_4"),
        ],
    ]
    return InlineKeyboardMarkup(buttons)

def help_pannel_page4(_):
    buttons = [
        [
            InlineKeyboardButton(text="Tᴏᴏʟs", callback_data="help_callback hb32"),
            InlineKeyboardButton(text="Aᴅᴠᴀɴᴄᴇᴅ", callback_data="help_callback hb33"),
        ],
        [
            InlineKeyboardButton(text="⬅", callback_data="help_page_3"),
        ],
    ]
    return InlineKeyboardMarkup(buttons)

def help_back_markup(_, page=1):
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(text="⬅ Bᴀᴄᴋ", callback_data=f"help_page_{page}")]]
    )

def private_help_panel(_):
    return [[InlineKeyboardButton(text="Hᴇʟᴘ", callback_data="help_page_1")]]


# ──────────────────────────────────────────────────────────────
# 2. HANDLERS (Commands and Callbacks)
# ──────────────────────────────────────────────────────────────

@app.on_message(filters.command(["help"]) & filters.private & ~BANNED_USERS)
@app.on_callback_query(filters.regex("help_page_1") & ~BANNED_USERS)
async def helper_private(client: app, update: Union[types.Message, types.CallbackQuery]):
    is_callback = isinstance(update, types.CallbackQuery)
    if is_callback:
        try:
            await update.answer()
        except:
            pass
        chat_id = update.message.chat.id
        language = await get_lang(chat_id)
        _ = get_string(language)
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

    def get_keyboard_for(cb_id):
        page1 = ["hb1", "hb2", "hb3", "hb4", "hb5", "hb6", "hb7", "hb8", "hb9", "hb10"]
        page2 = ["hb11", "hb12", "hb13", "hb14", "hb15", "hb16", "hb17", "hb18", "hb19", "hb20", "hb21"]
        page3 = ["hb22", "hb23", "hb24", "hb25", "hb26", "hb27", "hb28", "hb29", "hb30", "hb31"]
        
        if cb_id in page1:
            return help_back_markup(_, page=1)
        elif cb_id in page2:
            return help_back_markup(_, page=2)
        elif cb_id in page3:
            return help_back_markup(_, page=3)
        else:
            return help_back_markup(_, page=4)

    help_num = cb.replace("hb", "")
    content = getattr(helpers, f"HELP_{help_num}", None)

    if content:
        await CallbackQuery.edit_message_text(content, reply_markup=get_keyboard_for(cb))
    else:
        await CallbackQuery.answer("⚠️ Help Module Not Found!", show_alert=True)


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
