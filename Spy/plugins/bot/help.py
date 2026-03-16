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

# --- PREMIUM UI DESIGN ELEMENTS ---
# Inko aap apne hisab se customize kar sakte hain
BN = "✨" 
DV = "╼╼╼╼╼╼╼╼╼╼╼╼╼╼╼╼╼╼╼╼╼╼╼"
TOP_BORDER = "╔═══════════════════════╗"
BTM_BORDER = "╚═══════════════════════╝"

HELP_TEXT = (
    f" {TOP_BORDER}\n"
    f"    **💠 ᴘʀᴇᴍɪᴜᴍ ʜᴇʟᴘ ᴅᴀsʜʙᴏᴀʀᴅ 💠**\n"
    f" {BTM_BORDER}\n\n"
    f"{BN} **ᴄᴀᴛᴇɢᴏʀʏ:** sᴇʟᴇᴄᴛ ʙᴇʟᴏᴡ\n"
    f"{BN} **sᴛᴀᴛᴜs:** ᴀʟʟ sʏsᴛᴇᴍs ᴏɴʟɪɴᴇ ✅\n"
    f"{BN} **ᴍᴏᴅᴇ:** ᴘᴜʙʟɪᴄ ᴇᴅɪᴛɪᴏɴ\n\n"
    f"**ɢᴜɪᴅᴇ:** ᴄʟɪᴄᴋ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ᴛᴏ ᴇxᴘʟᴏʀᴇ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅs ᴀɴᴅ ғᴇᴀᴛᴜʀᴇs ᴏғ ᴛʜᴇ ʙᴏᴛ.\n\n"
    f" {DV}\n"
    f"📡 **sᴜᴘᴘᴏʀᴛ:** [ᴊᴏɪɴ ᴄʜᴀᴛ]({SUPPORT_CHAT})"
)

# --- Optimized Private & Back Handler ---
@app.on_message(filters.command(["help"]) & filters.private & ~BANNED_USERS)
@app.on_callback_query(filters.regex(pattern=r"settings_back_helper") & ~BANNED_USERS)
async def helper_private_elite(client: app, update: Union[types.Message, types.CallbackQuery]):
    is_cb = isinstance(update, types.CallbackQuery)
    chat_id = update.message.chat.id if is_cb else update.chat.id
    
    if is_cb:
        try: await update.answer("🔄 ᴏᴘᴇɴɪɴɢ ʜᴇʟᴘ ᴍᴇɴᴜ...", show_alert=False)
        except: pass
    else:
        try: await update.delete()
        except: pass

    lang = await get_lang(chat_id)
    _ = get_string(lang)
    
    # Customizing the keyboard from your utils
    keyboard = first_page(_)
    
    # Adding a Premium "VIP" Row at the top
    if hasattr(keyboard, 'inline_keyboard'):
        keyboard.inline_keyboard.insert(0, [
            InlineKeyboardButton("👑 ᴠɪᴘ ᴀᴄᴄᴇss 👑", url=f"https://t.me/Official_Dil")
        ])

    if is_cb:
        await update.edit_message_text(HELP_TEXT, reply_markup=keyboard, disable_web_page_preview=True)
    else:
        await update.reply_photo(
            photo=START_IMG_URL,
            caption=HELP_TEXT,
            reply_markup=keyboard,
        )

# --- Group Help Handler (Minimalist) ---
@app.on_message(filters.command(["help"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def help_com_group_elite(client, message: Message, _):
    keyboard = private_help_panel(_)
    await message.reply_text(
        text=f"✨ **ʜᴇʟᴘ ᴍᴇɴᴜ ɪs ɴᴏᴡ ᴀᴠᴀɪʟᴀʙʟᴇ ɪɴ ᴘʀɪᴠᴀᴛᴇ!**\n\nᴅɪʀᴇᴄᴛ ᴍᴇssᴀɢᴇ ᴍᴇ ᴛᴏ ɢᴇᴛ ᴛʜᴇ ʟɪsᴛ ᴏғ ᴄᴏᴍᴍᴀɴᴅs.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# --- Ultra-Optimized Callback Router ---
@app.on_callback_query(filters.regex("help_callback") & ~BANNED_USERS)
@languageCB
async def helper_cb_elite(client, CallbackQuery, _):
    cb_data = CallbackQuery.data.split(None, 1)[1]
    keyboard = help_back_markup(_)
    
    # Intelligent helper fetching
    help_id = cb_data.replace("hb", "")
    content = getattr(helpers, f"HELP_{help_id}", None)
    
    if content:
        final_text = (
            f"⚡ **ᴍᴏᴅᴜʟᴇ:** #{help_id}\n"
            f"{DV}\n"
            f"{content}\n"
            f"{DV}\n"
            f"✨ **ᴘᴏᴡᴇʀᴇᴅ ʙʏ:** @Official_Dil"
        )
        try:
            await CallbackQuery.edit_message_text(final_text, reply_markup=keyboard)
        except:
            pass

# --- Clean Navigation Controller ---
@app.on_callback_query(filters.regex(pattern=r"dilXaditi|Adisa|settings_back_helper_fixed") & ~BANNED_USERS)
@languageCB
async def navigation_controller(client, CallbackQuery, _):
    try:
        await CallbackQuery.answer("⚡ ᴘᴀɢᴇ ᴜᴘᴅᴀᴛᴇᴅ")
        # Switching between pages smoothly
        menu = second_page(_) if "Adisa" in CallbackQuery.data else first_page(_)
        
        # Injecting the Premium Button again for consistency
        menu.inline_keyboard.append([InlineKeyboardButton("💎 ᴜᴘɢʀᴀᴅᴇ ᴛᴏ ᴘʀᴇᴍɪᴜᴍ 💎", callback_data="premium_info")])
        
        await CallbackQuery.message.edit_text(HELP_TEXT, reply_markup=menu, disable_web_page_preview=True)
    except:
        return

# --- Hidden Premium Info Tooltip ---
@app.on_callback_query(filters.regex("premium_info") & ~BANNED_USERS)
async def premium_tooltip(client, CallbackQuery):
    await CallbackQuery.answer(
        "🌟 PREMIUM FEATURES:\n\n"
        "• No Ads / No Spam\n"
        "• 24/7 Priority Support\n"
        "• Highest Audio Quality\n"
        "• Custom Welcome Theme",
        show_alert=True
    )
