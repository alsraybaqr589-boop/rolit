import asyncio
import random

from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

TOKEN = "8735268386:AAFwZAjHtxosdtVczb054Ckm5mI9PpRmGKE"

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)

dp = Dispatcher()

# تخزين مؤقت للروليتات
roulettes = {}


# القائمة الرئيسية
menu = InlineKeyboardMarkup(
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


# قوائم الأقسام
normal_menu = InlineKeyboardMarkup(
    inline_keyboard=[

        [
            InlineKeyboardButton(
                text="🎮 إنشاء روليت عادي",
                callback_data="create_normal"
            )
        ],

        [
            InlineKeyboardButton(
                text="🏠 رجوع",
                callback_data="back_main"
            )
        ]
    ]
)

rules_menu = InlineKeyboardMarkup(
    inline_keyboard=[

        [
            InlineKeyboardButton(
                text="📜 إنشاء روليت أحكام",
                callback_data="create_rules"
            )
        ],

        [
            InlineKeyboardButton(
                text="🏠 رجوع",
                callback_data="back_main"
            )
        ]
    ]
)

vip_menu = InlineKeyboardMarkup(
    inline_keyboard=[

        [
            InlineKeyboardButton(
                text="🌈 إنشاء روليت VIP",
                callback_data="create_vip"
            )
        ],

        [
            InlineKeyboardButton(
                text="🏠 رجوع",
                callback_data="back_main"
            )
        ]
    ]
)


# رسالة البداية
start_text = """
🎮 أهلاً بك في بوت الروليت

✨ الأقسام:
• روليت عادي
• روليت أحكام
• روليت VIP
"""


# ستارت
@dp.message(CommandStart())
async def start(message: Message):

    await message.answer(
        start_text,
        reply_markup=menu
    )


# الروليت العادي
@dp.callback_query(F.data == "normal")
async def normal(callback: CallbackQuery):

    await callback.message.edit_text(
        "🌐 قسم الروليت العادي",
        reply_markup=normal_menu
    )


# الأحكام
@dp.callback_query(F.data == "rules")
async def rules(callback: CallbackQuery):

    await callback.message.edit_text(
        "📜 قسم روليت الأحكام",
        reply_markup=rules_menu
    )


# VIP
@dp.callback_query(F.data == "vip")
async def vip(callback: CallbackQuery):

    await callback.message.edit_text(
        "🌈 قسم الروليت المميز",
        reply_markup=vip_menu
    )


# إنشاء روليت عادي
@dp.callback_query(F.data == "create_normal")
async def create_normal(callback: CallbackQuery):

    roulette_id = random.randint(1000, 9999)

    roulettes[roulette_id] = []

    buttons = InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="🎯 دخول",
                    callback_data=f"join_{roulette_id}"
                )
            ],

            [
                InlineKeyboardButton(
                    text="🏆 اختيار فائز",
                    callback_data=f"winner_{roulette_id}"
                )
            ]
        ]
    )

    await callback.message.edit_text(
        f"""
🎮 روليت عادي جديد

🆔 رقم الروليت:
{roulette_id}

👥 عدد المشاركين:
0
""",
        reply_markup=buttons
    )


# إنشاء روليت أحكام
@dp.callback_query(F.data == "create_rules")
async def create_rules(callback: CallbackQuery):

    roulette_id = random.randint(1000, 9999)

    roulettes[roulette_id] = []

    buttons = InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="📜 دخول للروليت",
                    callback_data=f"join_{roulette_id}"
                )
            ],

            [
                InlineKeyboardButton(
                    text="⚖️ اختيار شخص",
                    callback_data=f"winner_{roulette_id}"
                )
            ]
        ]
    )

    await callback.message.edit_text(
        f"""
📜 روليت أحكام جديد

🆔 رقم الروليت:
{roulette_id}

👥 عدد المشاركين:
0
""",
        reply_markup=buttons
    )


# إنشاء VIP
@dp.callback_query(F.data == "create_vip")
async def create_vip(callback: CallbackQuery):

    roulette_id = random.randint(1000, 9999)

    roulettes[roulette_id] = []

    buttons = InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="🌈 دخول للروليت",
                    callback_data=f"join_{roulette_id}"
                )
            ],

            [
                InlineKeyboardButton(
                    text="🏆 سحب فائز VIP",
                    callback_data=f"winner_{roulette_id}"
                )
            ]
        ]
    )

    await callback.message.edit_text(
        f"""
🌈 روليت VIP جديد

🆔 رقم الروليت:
{roulette_id}

👥 عدد المشاركين:
0
""",
        reply_markup=buttons
    )


# دخول للروليت
@dp.callback_query(F.data.startswith("join_"))
async def join(callback: CallbackQuery):

    roulette_id = int(callback.data.split("_")[1])

    user = callback.from_user.first_name

    if user in roulettes[roulette_id]:

        await callback.answer(
            "❌ أنت مشارك بالفعل",
            show_alert=True
        )

        return

    roulettes[roulette_id].append(user)

    count = len(roulettes[roulette_id])

    await callback.answer(
        "✅ تم دخولك للروليت"
    )

    await callback.message.edit_text(
        f"""
🎯 تم تحديث الروليت

🆔 رقم الروليت:
{roulette_id}

👥 عدد المشاركين:
{count}
""",
        reply_markup=callback.message.reply_markup
    )


# اختيار فائز
@dp.callback_query(F.data.startswith("winner_"))
async def winner(callback: CallbackQuery):

    roulette_id = int(callback.data.split("_")[1])

    users = roulettes[roulette_id]

    if len(users) == 0:

        await callback.answer(
            "❌ لا يوجد مشاركين",
            show_alert=True
        )

        return

    winner_user = random.choice(users)

    await callback.message.answer(
        f"""
🏆 تم اختيار الفائز

🎉 الفائز:
{winner_user}
"""
    )


# رجوع
@dp.callback_query(F.data == "back_main")
async def back_main(callback: CallbackQuery):

    await callback.message.edit_text(
        start_text,
        reply_markup=menu
    )


# تشغيل
async def main():

    print("BOT STARTED")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
