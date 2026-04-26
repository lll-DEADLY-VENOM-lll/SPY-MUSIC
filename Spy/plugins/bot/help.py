from typing import Union
from pyrogram import filters, types
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from Spy import app
from Spy.utils import first_page, second_page
from Spy.utils.database import get_lang
from Spy.utils.decorators.language import LanguageStart, languageCB
from Spy.utils.inline.help import help_back_markup, private_help_panel
from config import BANNED_USERS, START_IMG_URL, SUPPORT_CHAT
from strings import get_string, helpers

# --- Normal Clean Text ---
HELP_TEXT = (
    "**💡 Help Menu**\n\n"
    "Select the category you want to learn about from the buttons below.\n\n"
    "• **Status:** All systems functional\n"
    "• **Mode:** Public\n\n"
    "If you face any issues, feel free to join our support chat."
)

# --- Private Help & Back Handler ---
@app.on_message(filters.command(["help"]) & filters.private & ~BANNED_USERS)
@app.on_callback_query(filters.regex(pattern=r"settings_back_helper") & ~BANNED_USERS)
async def help_private(client: app, update: Union[types.Message, types.CallbackQuery]):
    is_cb = isinstance(update, types.CallbackQuery)
    chat_id = update.message.chat.id if is_cb else update.chat.id
    
    if is_cb:
        try: await update.answer()
        except: pass

    lang = await get_lang(chat_id)
    _ = get_string(lang)
    keyboard = first_page(_)

    if is_cb:
        await update.edit_message_text(HELP_TEXT, reply_markup=keyboard)
    else:
        await update.reply_photo(
            photo=START_IMG_URL,
            caption=HELP_TEXT,
            reply_markup=keyboard,
        )

# --- Group Help Handler ---
@app.on_message(filters.command(["help"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def help_group(client, message: Message, _):
    keyboard = private_help_panel(_)
    await message.reply_text(
        "Help menu has been sent to your Private Messages.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# --- Module Commands Handler ---
@app.on_callback_query(filters.regex("help_callback") & ~BANNED_USERS)
@languageCB
async def helper_cb(client, CallbackQuery, _):
    cb_data = CallbackQuery.data.split(None, 1)[1]
    keyboard = help_back_markup(_)
    
    help_id = cb_data.replace("hb", "")
    content = getattr(helpers, f"HELP_{help_id}", None)
    
    if content:
        # Normal formatting for modules
        final_text = f"**Category: {help_id}**\n\n{content}"
        try:
            await CallbackQuery.edit_message_text(final_text, reply_markup=keyboard)
        except:
            pass

# --- Page Navigation ---
@app.on_callback_query(filters.regex(pattern=r"dilXaditi|Adisa") & ~BANNED_USERS)
@languageCB
async def nav_handler(client, CallbackQuery, _):
    try:
        menu = second_page(_) if "Adisa" in CallbackQuery.data else first_page(_)
        await CallbackQuery.message.edit_reply_markup(reply_markup=menu)
    except:
        return
