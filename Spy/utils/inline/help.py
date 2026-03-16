# Importing important modules & bot
from Spy import app
from typing import Union
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# ------------------------------------------------------------------------ #
# MODERN HELP MENU - DESIGNED BY DIL
# ------------------------------------------------------------------------ #

def first_page(_):
    # Original callback_data preserved: Adisa, settingsback_helper, dilXaditi
    controll_button = [
        InlineKeyboardButton(text="❮", callback_data="Adisa"), 
        InlineKeyboardButton(text="🏠 HOME", callback_data="settingsback_helper"), 
        InlineKeyboardButton(text="❯", callback_data="dilXaditi")
    ]
    
    first_page_menu = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text=_["H_B_1"], callback_data="help_callback hb1"), 
                InlineKeyboardButton(text=_["H_B_2"], callback_data="help_callback hb2"),
                InlineKeyboardButton(text=_["H_B_3"], callback_data="help_callback hb3")
            ],
            [
                InlineKeyboardButton(text=_["H_B_4"], callback_data="help_callback hb4"), 
                InlineKeyboardButton(text=_["H_B_5"], callback_data="help_callback hb5"),
                InlineKeyboardButton(text=_["H_B_6"], callback_data="help_callback hb6")
            ],
            [
                InlineKeyboardButton(text=_["H_B_7"], callback_data="help_callback hb7"), 
                InlineKeyboardButton(text=_["H_B_8"], callback_data="help_callback hb8"),
                InlineKeyboardButton(text=_["H_B_9"], callback_data="help_callback hb9")
            ],
            controll_button,
        ]
    )
    return first_page_menu


def second_page(_):
    # Original callback_data preserved: settings_back_helper_fixed, settingsback_helper, settings_back_helper
    controll_button = [
        InlineKeyboardButton(text="❮", callback_data="settings_back_helper_fixed"), 
        InlineKeyboardButton(text="🏠 HOME", callback_data="settingsback_helper"), 
        InlineKeyboardButton(text="❯", callback_data="settings_back_helper")
    ]
    
    second_page_menu = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text=_["H_B_10"], callback_data="help_callback hb10"), 
                InlineKeyboardButton(text=_["H_B_11"], callback_data="help_callback hb11"), 
                InlineKeyboardButton(text=_["H_B_12"], callback_data="help_callback hb12")
            ],
            [
                InlineKeyboardButton(text=_["H_B_13"], callback_data="help_callback hb13"), 
                InlineKeyboardButton(text=_["H_B_14"], callback_data="help_callback hb14"), 
                InlineKeyboardButton(text=_["H_B_15"], callback_data="help_callback hb15")
            ],
            [
                InlineKeyboardButton(text=_["H_B_16"], callback_data="help_callback hb16")
            ],
            controll_button,
        ]
    )
    return second_page_menu


def help_back_markup(_):
    """Common button to go back to the main help menu"""
    upl = InlineKeyboardMarkup(
        [[InlineKeyboardButton(text="🔙 " + _["BACK_BUTTON"], callback_data="settings_back_helper")]]
    )
    return upl


def private_help_panel(_):
    """Deep-link button for PM help"""
    buttons = [
        [InlineKeyboardButton(text="✨ " + _["S_B_4"], url=f"https://t.me/{app.username}?start=help")]
    ]
    return buttons

# ----------------------------> NOTE <----------------------------- #
"""
✨ Modified & Enhanced by Dil.
✅ Fixed: Callback connections restored.
🎨 Added: Professional Emojis and Padding.
"""
