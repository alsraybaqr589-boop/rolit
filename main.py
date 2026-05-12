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

from config import BOT_TOKEN
from keyboards import main_menu, back_menu
from database import create_db

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)

dp = Dispatcher()

# تخزين الروليتات
roulettes = {}


# ستارت
@dp.message(CommandStart())
async def start(message: Message):

    text = """
🎮 أهلاً بك في بوت الروليت

✨ المميزات:
• روليت عادي
• روليت أحكام
• روليت VIP
• اختيار فائز
• دخول مشاركين
"""

    await message.answer(
        text,
        reply_markup=main_menu
    )


# الروليت العادي
@dp.callback_query(F.data == "normal")
async def normal(callback: CallbackQuery):

    buttons = InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="🎮 إنشاء روليت",
                    callback_data="create_normal"
                )
            ],

            [
                InlineKeyboardButton(
                    text="🏠 رجوع",
                    callback_data="back"
                )
            ]
        ]
    )

    await callback.message.edit_text(
        "🌐 قسم الروليت العادي",
        reply_markup=buttons
    )


# روليت الأحكام
@dp.callback_query(F.data == "rules")
async def rules(callback: CallbackQuery):

    buttons = InlineKeyboardMarkup(
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
                    callback_data="back"
                )
            ]
        ]
    )

    await callback.message.edit_text(
        "📜 قسم روليت الأحكام",
        reply_markup=buttons
    )


# روليت VIP
@dp.callback_query(F.data == "vip")
async def vip(callback: CallbackQuery):

    buttons = InlineKeyboardMarkup(
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
                    callback_data="back"
                )
            ]
        ]
    )

    await callback.message.edit_text(
        "🌈 قسم الروليت المميز",
        reply_markup=buttons
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
🎮 روليت جديد

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
                    text="📜 دخول",
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
📜 روليت أحكام

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
                    text="🌈 دخول",
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
🌈 روليت VIP

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

    roulette_id = int(
        callback.data.split("_")[1]
    )

    user = callback.from_user.first_name

    if user in roulettes[roulette_id]:

        await callback.answer(
            "❌ أنت مشارك بالفعل",
            show_alert=True
        )

        return

    roulettes[roulette_id].append(user)

    count = len(
        roulettes[roulette_id]
    )

    await callback.answer(
        "✅ تم دخولك"
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


# اختيار الفائز
@dp.callback_query(F.data.startswith("winner_"))
async def winner(callback: CallbackQuery):

    roulette_id = int(
        callback.data.split("_")[1]
    )

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
@dp.callback_query(F.data == "back")
async def back(callback: CallbackQuery):

    text = """
🎮 أهلاً بك في بوت الروليت

✨ المميزات:
• روليت عادي
• روليت أحكام
• روليت VIP
• اختيار فائز
• دخول مشاركين
"""

    await callback.message.edit_text(
        text,
        reply_markup=main_menu
    )


# تشغيل
async def main():

    await create_db()

    print("BOT STARTED")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
