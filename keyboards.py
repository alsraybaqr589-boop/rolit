from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# القائمة الرئيسية
main_menu = InlineKeyboardMarkup(
    inline_keyboard=[

        [
            InlineKeyboardButton(
                text="🌐 روليت عادي",
                callback_data="normal"
            )
        ],

        [
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

# قائمة الروليت المميز
vip_menu = InlineKeyboardMarkup(
    inline_keyboard=[

        [
            InlineKeyboardButton(
                text="🌈 بدء إنشاء روليت",
                callback_data="create_vip"
            )
        ],

        [
            InlineKeyboardButton(
                text="⚙️ إعدادات القنوات",
                callback_data="channels"
            )
        ],

        [
            InlineKeyboardButton(
                text="🏠 العودة للقائمة",
                callback_data="back"
            )
        ]

    ]
)

# زر الإلغاء
cancel_button = InlineKeyboardMarkup(
    inline_keyboard=[

        [
            InlineKeyboardButton(
                text="❌ إلغاء",
                callback_data="cancel"
            )
        ]

    ]
)
