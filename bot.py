from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

players = []

@dp.message_handler(commands=['start'])
async def start(message: types.Message):

    buttons = InlineKeyboardMarkup(row_width=1)
    
    join = InlineKeyboardButton(
        "🎮 مشاركة",
        callback_data="join"
    )

    spin = InlineKeyboardButton(
        "🎡 تدوير العجلة",
        callback_data="spin"
    )

    buttons.add(join, spin)

    await message.answer(
        "🎰 اهلاً بك في روليت التليگرام\n\nاضغط مشاركة للدخول.",
        reply_markup=buttons
    )

@dp.callback_query_handler(lambda c: c.data == "join")
async def join_game(callback: types.CallbackQuery):

    user = callback.from_user.first_name

    if user not in players:
        players.append(user)

    await callback.answer("تمت المشاركة ✅", show_alert=True)

@dp.callback_query_handler(lambda c: c.data == "spin")
async def spin(callback: types.CallbackQuery):

    if len(players) < 2:
        await callback.answer("لا يوجد مشاركين كافيين", show_alert=True)
        return

    loser = players.pop(0)

    text = f"❌ الخاسر: {loser}\n\n👥 المتبقين: {len(players)}"

    if len(players) == 1:
        text += f"\n\n🏆 الفائز: {players[0]}"

    await callback.message.answer(text)

    await callback.answer()

if __name__ == "__main__":
    executor.start_polling(dp)
