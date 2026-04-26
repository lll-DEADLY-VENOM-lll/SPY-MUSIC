import time
from typing import Set, Dict, Tuple
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatType, ChatMemberStatus

# --- CONFIGURATION ---
SUDO_USERS: Set[int] = {12345678, 87654321}  # Add actual IDs here
USE_AS_BOT: bool = True

# Cache to prevent hitting Telegram API limits on every message
# Format: {(chat_id, user_id): (is_admin, expiry_timestamp)}
ADMIN_CACHE: Dict[Tuple[int, int], Tuple[bool, float]] = {}
CACHE_TTL = 300  # 5 minutes


async def is_admin_logic(client: Client, message: Message) -> bool:
    """Checks if a user is an administrator in the current chat."""
    
    # 1. Private chats: The user is always the "admin" of their own DM
    if message.chat.type == ChatType.PRIVATE:
        return True

    # 2. Handle Anonymous Admins or Post-as-Channel
    if message.sender_chat:
        # If sending as the chat itself, they are effectively an admin
        return message.sender_chat.id == message.chat.id

    if not message.from_user:
        return False

    user_id = message.from_user.id
    chat_id = message.chat.id

    # 3. Handle Special Telegram IDs
    if user_id in [777000, 1087968824]:
        return True

    # 4. Check Cache
    now = time.time()
    if (chat_id, user_id) in ADMIN_CACHE:
        is_adm, expiry = ADMIN_CACHE[(chat_id, user_id)]
        if now < expiry:
            return is_adm

    # 5. Fetch from API
    try:
        member = await client.get_chat_member(chat_id, user_id)
        is_admin = member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]
        
        # Save to cache
        ADMIN_CACHE[(chat_id, user_id)] = (is_admin, now + CACHE_TTL)
        return is_admin
    except Exception:
        return False


# --- CUSTOM FILTERS ---

async def f_sudo_filter(_, client: Client, message: Message):
    if message.edit_date:
        return False
        
    user_id = message.from_user.id if message.from_user else None
    sender_id = message.sender_chat.id if message.sender_chat else None
    
    return (user_id in SUDO_USERS) or (sender_id in SUDO_USERS)


async def f_owner_filter(_, client: Client, message: Message):
    if message.edit_date:
        return False
        
    if USE_AS_BOT:
        # If in bot mode, 'owner' usually refers to sudoers
        user_id = message.from_user.id if message.from_user else None
        return user_id in SUDO_USERS
    else:
        # In Userbot mode, check if the message is from yourself
        return message.from_user and message.from_user.is_self


async def f_admin_filter(_, client: Client, message: Message):
    # Only process new messages
    if message.edit_date:
        return False
    return await is_admin_logic(client, message)


# --- EXPORTABLE FILTERS ---

sudo_filter = filters.create(f_sudo_filter, name="SudoFilter")
owner_filter = filters.create(f_owner_filter, name="OwnerFilter")
admin_filter = filters.create(f_admin_filter, name="AdminFilter")
