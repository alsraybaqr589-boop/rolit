import asyncio
import sqlite3

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.context import FSMContext

from config import TOKEN, FORCE_CHANNEL
from keyboards import main_menu, vip_menu, cancel_button
from states import CreateRoulette

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)

dp = Dispatcher()

db = sqlite3.connect("roulette.db")
cur = db.cursor()


# اشتراك اجباري
async def check_sub(user_id):

    try:

        member = await bot.get_chat_member(
            chat_id=f"@{FORCE_CHANNEL}",
            user_id=user_id
        )

        return member.status in [
            "member",
            "administrator",
            "creator"
        ]

    except:
        return False


# ستارت
@dp.message(F.text == "/start")
async def start(message: Message):

    joined = await check_sub(message.from_user.id)

    if not joined:

        await message.answer(
            "عذراً، يجب الاشتراك بالقناة أولاً.",
            reply_markup=main_menu
        )

        return

    text = """
🎮 أهلاً بك في بوت الروليت

✨ الميزات:
• إنشاء روليت
• روليت أحكام
• روليت VIP
• اشتراك إجباري
• سحب تلقائي
"""

    await message.answer(
        text,
        reply_markup=main_menu
    )


# روليت مميز
@dp.callback_query(F.data == "vip")
async def vip(callback: CallbackQuery):

    text = """
🌈 أهلاً بك في قسم الروليت المميز

يمكنك الآن إنشاء مسابقات ونشرها.
"""

    await callback.message.edit_text(
        text,
        reply_markup=vip_menu
    )


# بدء الانشاء
@dp.callback_query(F.data == "create_vip")
async def create_vip(callback: CallbackQuery, state: FSMContext):

    await state.set_state(CreateRoulette.title)

    await callback.message.edit_text(
        "📝 أرسل عنوان الروليت:",
        reply_markup=cancel_button
    )


# عنوان
@dp.message(CreateRoulette.title)
async def get_title(message: Message, state: FSMContext):

    await state.update_data(
        title=message.text
    )

    await state.set_state(
        CreateRoulette.max_users
    )

    await message.answer(
        "👥 أرسل الحد الأقصى للمشاركين:",
        reply_markup=cancel_button
    )


# عدد المشاركين
@dp.message(CreateRoulette.max_users)
async def get_max(message: Message, state: FSMContext):

    await state.update_data(
        max_users=message.text
    )

    await state.set_state(
        CreateRoulette.winners
    )

    await message.answer(
        "🏆 أرسل عدد الفائزين:",
        reply_markup=cancel_button
    )


# عدد الفائزين
@dp.message(CreateRoulette.winners)
async def get_winners(message: Message, state: FSMContext):

    await state.update_data(
        winners=message.text
    )

    await state.set_state(
        CreateRoulette.channel
    )

    await message.answer(
        "📢 أرسل معرف القناة بدون @",
        reply_markup=cancel_button
    )


# القناة
@dp.message(CreateRoulette.channel)
async def get_channel(message: Message, state: FSMContext):

    data = await state.get_data()

    title = data["title"]
    max_users = data["max_users"]
    winners = data["winners"]

    channel = message.text

    text = f"""
🎡 <b>{title}</b>

👥 المشاركين: 0 من أصل {max_users}

🏆 عدد الفائزين: {winners}
"""

    await bot.send_message(
        chat_id=f"@{channel}",
        text=text
    )

    await message.answer(
        "✅ تم نشر الروليت بنجاح",
        reply_markup=main_menu
    )

    await state.clear()


# رجوع
@dp.callback_query(F.data == "back")
async def back(callback: CallbackQuery):

    await callback.message.edit_text(
        "🏠 القائمة الرئيسية",
        reply_markup=main_menu
    )


# الغاء
@dp.callback_query(F.data == "cancel")
async def cancel(callback: CallbackQuery, state: FSMContext):

    await state.clear()

    await callback.message.edit_text(
        "❌ تم الإلغاء",
        reply_markup=main_menu
    )


# تشغيل
async def main():

    print("BOT STARTED")

    await dp.start_polling(bot)


asyncio.run(main())
