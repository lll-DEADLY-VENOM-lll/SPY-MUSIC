from pyrogram import filters, enums
from pyrogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ChatPermissions,
    CallbackQuery
)
from pyrogram.errors.exceptions.bad_request_400 import (
    ChatAdminRequired,
    UserAdminInvalid,
    BadRequest
)
import random
from logging import getLogger
from Spy import LOGGER, app
from config import LOGGER_ID as LOG_GROUP_ID, OWNER_ID
from Spy.misc import SUDOERS
# Fixed the import line below
from Spy.helper.admin_check import admin_filter 

LOGGER = getLogger(__name__)

kickpic = [
    "https://graph.org/file/210751796ff48991b86a3.jpg",
    "https://graph.org/file/7b4924be4179f70abcf33.jpg",
    "https://graph.org/file/f6d8e64246bddc26b4f66.jpg",
]

button = [
    [
        InlineKeyboardButton(
            text="Ɗᴇᴠ𝘴", url="https://t.me/about_deadly_venom"
        )
    ]
]

def mention(user, name, mention=True):
    if mention:
        return f"[{name}](tg://openmessage?user_id={user})"
    else:
        return f"[{name}](https://t.me/{user})"

async def get_userid_from_username(username):
    try:
        user = await app.get_users(username)
        return [user.id, user.first_name]
    except Exception:
        return None

async def bans_user(user_id, first_name, admin_id, admin_name, chat_id, message):
    try:
        # Note: ban_chat_member followed by unban (with no duration) acts as a kick 
        # but prevents them from rejoining until they have a link. 
        # To truly ban, don't call unban immediately.
        await app.ban_chat_member(chat_id, user_id)
    except ChatAdminRequired:
        return "I need ban rights to perform this action.", False
    except UserAdminInvalid:
        return "I can't ban another admin!", False
    except Exception as e:
        if user_id == OWNER_ID:
            return "Why should I ban my owner?", False
        return f"An error occurred: {e}", False

    user_mention = mention(user_id, first_name)
    admin_mention = mention(admin_id, admin_name)
    
    try:
        await app.send_message(LOG_GROUP_ID, f"{user_mention} was banned by {admin_mention} in {message.chat.title}")
    except:
        pass

    ban_message = await message.reply_photo(
        photo=random.choice(kickpic),
        caption=f"{user_mention} was banned by {admin_mention}."
    )
    return ban_message, True

@app.on_message(filters.command("ban") & admin_filter)
async def ban_user_with_unban_button(client, message):
    chat_id = message.chat.id
    admin_id = message.from_user.id
    admin_name = message.from_user.first_name
    
    # Permission check
    member = await message.chat.get_member(admin_id)
    if member.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
        return await message.reply_text("You are not an admin.")
    
    if member.status == enums.ChatMemberStatus.ADMINISTRATOR and not member.privileges.can_restrict_members:
        return await message.reply_text("You don't have 'Restrict Members' permission.")

    if len(message.command) > 1:
        user_input = message.command[1]
        if user_input.isdigit():
            user_id = int(user_input)
            first_name = "User"
        else:
            user_obj = await get_userid_from_username(user_input)
            if user_obj is None:
                return await message.reply_text("User not found.")
            user_id, first_name = user_obj[0], user_obj[1]
    elif message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        first_name = message.reply_to_message.from_user.first_name
    else:
        return await message.reply_text("Please specify a user or reply to their message.")
        
    msg_text, result = await bans_user(user_id, first_name, admin_id, admin_name, chat_id, message)
    if not result:
        return await message.reply_text(msg_text)

    unban_button = [[InlineKeyboardButton("ƲɴʙᴀƝ ƲsᴇƦ", callback_data=f"unban_{user_id}")]]
    await message.reply_text(
        f"Click below to unban {first_name}.",
        reply_markup=InlineKeyboardMarkup(unban_button),
    )

@app.on_message(filters.command("unban") & admin_filter)
async def unban_user_cmd(client, message):
    chat_id = message.chat.id
    admin_id = message.from_user.id
    admin_name = message.from_user.first_name
    
    if len(message.command) > 1:
        user_input = message.command[1]
        try:
            if user_input.isdigit():
                user_id = int(user_input)
                first_name = "User"
            else:
                user_obj = await get_userid_from_username(user_input)
                user_id, first_name = user_obj[0], user_obj[1]
        except:
            return await message.reply_text("User not found.")
    else:
        return await message.reply_text("Please specify a user to unban.")
    
    try:
        await app.unban_chat_member(chat_id, user_id)
        user_mention = mention(user_id, first_name)
        await message.reply_text(f"Unbanned {user_mention}!")
    except Exception as e:
        await message.reply_text(f"Error: {e}")

@app.on_callback_query(filters.regex(r"unban_(\d+)"))
async def unban_button_callback(client, callback_query):
    # Verify if the person clicking the button is an admin
    user_id = int(callback_query.matches[0].group(1))
    admin_id = callback_query.from_user.id
    chat_id = callback_query.message.chat.id
    
    member = await client.get_chat_member(chat_id, admin_id)
    if member.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
        return await callback_query.answer("Only admins can use this button!", show_alert=True)

    try:
        await app.unban_chat_member(chat_id, user_id)
        await callback_query.answer("User has been unbanned!")
        await callback_query.message.edit_text("The user has been successfully unbanned.")
    except Exception as e:
        await callback_query.answer(f"Error: {e}", show_alert=True)

@app.on_message(filters.command("kickme") & filters.group)
async def kickme_command(client, message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    chat_id = message.chat.id

    try:
        await app.ban_chat_member(chat_id, user_id)
        await app.unban_chat_member(chat_id, user_id) # Unban so they can rejoin via link
        await message.reply_text(f"{user_name} has kicked themselves!")
    except Exception as e:
        await message.reply_text(f"Could not kick: {e}")
