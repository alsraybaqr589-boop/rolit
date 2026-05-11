import asyncio

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


# القائمة الرئيسية
menu = InlineKeyboardMarkup(
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


# قائمة VIP
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


# ستارت
@dp.message(CommandStart())
async def start(message: Message):

    text = """
🎮 أهلاً بك في بوت الروليت

✨ المميزات:
• روليت عادي
• روليت أحكام
• روليت VIP
• نشر بالقنوات
• سحب تلقائي
"""

    await message.answer(
        text,
        reply_markup=menu
    )


# روليت عادي
@dp.callback_query(F.data == "normal")
async def normal(callback: CallbackQuery):

    await callback.answer(
        "🚧 سيتم إضافة الروليت العادي قريباً",
        show_alert=True
    )


# روليت أحكام
@dp.callback_query(F.data == "rules")
async def rules(callback: CallbackQuery):

    await callback.answer(
        "🚧 سيتم إضافة روليت الأحكام قريباً",
        show_alert=True
    )


# روليت VIP
@dp.callback_query(F.data == "vip")
async def vip(callback: CallbackQuery):

    text = """
🌈 أهلاً بك في قسم التحكم بالروليت المميز

يمكنك الآن إنشاء مسابقات مخصصة ونشرها في قناتك مباشرة.
"""

    await callback.message.edit_text(
        text,
        reply_markup=vip_menu
    )


# إنشاء روليت
@dp.callback_query(F.data == "create_vip")
async def create_vip(callback: CallbackQuery):

    await callback.message.answer(
        "📝 أرسل الآن عنوان المسابقة:"
    )


# إعدادات القنوات
@dp.callback_query(F.data == "channels")
async def channels(callback: CallbackQuery):

    await callback.message.edit_text(
        "⚙️ إدارة القنوات\n\nلا توجد قنوات مضافة حالياً.",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[

                [
                    InlineKeyboardButton(
                        text="➕ إضافة قناة جديدة",
                        callback_data="add_channel"
                    )
                ],

                [
                    InlineKeyboardButton(
                        text="رجوع",
                        callback_data="vip"
                    )
                ]
            ]
        )
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
• نشر بالقنوات
• سحب تلقائي
"""

    await callback.message.edit_text(
        text,
        reply_markup=menu
    )


# تشغيل البوت
async def main():

    print("BOT STARTED")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
