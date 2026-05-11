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
