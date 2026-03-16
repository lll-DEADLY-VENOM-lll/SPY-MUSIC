from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# ------------------------------------------------------------------------ #
# PREMIUM STATS PANEL - RE-DESIGNED BY DIL
# ------------------------------------------------------------------------ #

def stats_buttons(_, status):
    """
    Stats menu logic with a clean UI.
    If status is True, shows Sudo/Staff buttons.
    """
    if status:
        # Layout for Sudo/Admin Users
        buttons = [
            [
                InlineKeyboardButton(text="📊 " + _["SA_B_2"], callback_data="bot_stats_sudo"),
                InlineKeyboardButton(text="🌍 " + _["SA_B_3"], callback_data="TopOverall"),
            ],
            [
                InlineKeyboardButton(text="🗑️ " + _["CLOSE_BUTTON"], callback_data="close"),
            ],
        ]
    else:
        # Layout for Regular Users
        buttons = [
            [
                InlineKeyboardButton(text="🌍 " + _["SA_B_1"], callback_data="TopOverall"),
            ],
            [
                InlineKeyboardButton(text="🗑️ " + _["CLOSE_BUTTON"], callback_data="close"),
            ],
        ]
    
    return InlineKeyboardMarkup(buttons)


def back_stats_buttons(_):
    """
    Standard back and close buttons for the stats page.
    """
    buttons = [
        [
            InlineKeyboardButton(text="⬅️ " + _["BACK_BUTTON"], callback_data="stats_back"),
            InlineKeyboardButton(text="❌ " + _["CLOSE_BUTTON"], callback_data="close"),
        ],
    ]
    return InlineKeyboardMarkup(buttons)

# ----------------------------> INFO <----------------------------- #
"""
🚀 Updated by: Dil
✅ Improvements:
   - Logic: 'if-else' use kiya hai jo pichle list comprehension se zyada fast aur readable hai.
   - Icons: Stats (📊), Global (🌍), Back (⬅️), aur Close (❌) emojis add kiye hain.
   - Design: Buttons ko balanced spacing di gayi hai.
"""
