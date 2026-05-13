import random
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import BOT_TOKEN

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()

participants = {}

rules_list = [
    "غني أغنية 🎤",
    "غير صورتك يوم كامل 😂",
    "ابعث رسالة صوتية 🎙",
    "قل نكتة 🤣",
    "سوي تحدي 😈"
]


def main_menu():
    kb = InlineKeyboardBuilder()

    kb.button(text="🎲 روليت عادي", callback_data="normal")
    kb.button(text="⚖️ روليت أحكام", callback_data="rules")
    kb.button(text="⭐ روليت مميز", callback_data="premium")

    kb.adjust(1)
    return kb.as_markup()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "اهلًا بك في بوت الروليت 🎉",
        reply_markup=main_menu()
    )


@dp.callback_query(F.data == "normal")
async def normal(call: CallbackQuery):

    kb = InlineKeyboardBuilder()

    kb.button(text="✅ بدء", callback_data="start_normal")
    kb.button(text="🔙 رجوع", callback_data="back")
