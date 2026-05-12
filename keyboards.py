from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

# القائمة الرئيسية
main_menu = InlineKeyboardMarkup(
    inline_keyboard=[

        [
            InlineKeyboardButton(
                text="🌐 روليت عادي",
                callback_data="normal"
            ),

            InlineKeyboardButton(
                text="📜 روليت أحكام",
                callback_data="rules"
            )
        ],

        [
            InlineKeyboardButton(
                text="🌈 روليت مميز",
                callback_data="vip"
            )
        ],

        [
            InlineKeyboardButton(
                text="📢 قناتنا",
                url="https://t.me/NQJNQ"
            )
        ]
    ]
)

# زر الرجوع
back_menu = InlineKeyboardMarkup(
    inline_keyboard=[

        [
            InlineKeyboardButton(
                text="🏠 رجوع",
                callback_data="back"
            )
        ]
    ]
)
