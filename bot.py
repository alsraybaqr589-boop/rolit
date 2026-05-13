import random
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

# حط توكن البوت هنا
BOT_TOKEN = "8735268386:AAGzFCX4yKoTjdgSjbFId1xP4Rhc-BGJ9oo"

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

    # أزرار كبار
    kb.button(text="🎲 روليت عادي", callback_data="normal")
    kb.button(text="⚖️ روليت أحكام", callback_data="rules")
    kb.button(text="⭐ روليت مميز", callback_data="premium")
    kb.button(text="📢 NQJNQ", url="https://t.me/NQJNQ")

    # كل زر بسطر
    kb.adjust(1)

    return kb.as_markup()


@dp.message(CommandStart())
async def start(message: Message):

    await message.answer(
        "🎉 اهلًا بك في بوت الروليت",
        reply_markup=main_menu()
    )


# روليت عادي
@dp.callback_query(F.data == "normal")
async def normal(call: CallbackQuery):

    kb = InlineKeyboardBuilder()

    kb.button(text="✅ بدء", callback_data="start_normal")
    kb.button(text="🔙 رجوع", callback_data="back")

    kb.adjust(1)

    await call.message.edit_text(
        "🎲 روليت عادي",
        reply_markup=kb.as_markup()
    )


# روليت أحكام
@dp.callback_query(F.data == "rules")
async def rules(call: CallbackQuery):

    kb = InlineKeyboardBuilder()

    kb.button(text="✅ بدء", callback_data="start_rules")
    kb.button(text="🔙 رجوع", callback_data="back")

    kb.adjust(1)

    await call.message.edit_text(
        "⚖️ روليت أحكام",
        reply_markup=kb.as_markup()
    )


# روليت مميز
@dp.callback_query(F.data == "premium")
async def premium(call: CallbackQuery):

    await call.message.edit_text(
        "⭐ روليت مميز\n\nقيد التطوير"
    )


# رجوع
@dp.callback_query(F.data == "back")
async def back(call: CallbackQuery):

    await call.message.edit_text(
        "🎉 القائمة الرئيسية",
        reply_markup=main_menu()
    )


# نشر روليت عادي
@dp.callback_query(F.data == "start_normal")
async def start_normal(call: CallbackQuery):

    kb = InlineKeyboardBuilder()

    # زر مشاركة حقيقي
    kb.button(
        text="🎉 مشاركة",
        switch_inline_query="تعال شارك بالروليت 🎲"
    )

    kb.button(text="🎯 دخول", callback_data="join_normal")
    kb.button(text="🏆 اختيار فائز", callback_data="pick_normal")

    kb.adjust(1)

    msg = await call.message.answer(
        """
🎲 روليت عادي

👥 المشاركين: 0

اضغط دخول للمشاركة
        """,
        reply_markup=kb.as_markup()
    )

    participants[msg.message_id] = []


# دخول روليت عادي
@dp.callback_query(F.data == "join_normal")
async def join_normal(call: CallbackQuery):

    users = participants.get(call.message.message_id, [])

    if call.from_user.id in users:
        return await call.answer(
            "أنت مشارك مسبقًا",
            show_alert=True
        )

    users.append(call.from_user.id)

    participants[call.message.message_id] = users

    await call.answer("تم دخولك 🎉")


# اختيار فائز
@dp.callback_query(F.data == "pick_normal")
async def pick_normal(call: CallbackQuery):

    users = participants.get(call.message.message_id, [])

    if not users:
        return await call.answer(
            "لا يوجد مشاركين",
            show_alert=True
        )

    winner = random.choice(users)

    user = await bot.get_chat(winner)

    await call.message.answer(
        f"🏆 الفائز هو @{user.username}"
    )


# نشر روليت أحكام
@dp.callback_query(F.data == "start_rules")
async def start_rules(call: CallbackQuery):

    kb = InlineKeyboardBuilder()

    # زر مشاركة حقيقي
    kb.button(
        text="🎉 مشاركة",
        switch_inline_query="تعال شارك بروليت الأحكام ⚖️"
    )

    kb.button(text="🎯 دخول", callback_data="join_rules")
    kb.button(text="⚖️ اختيار", callback_data="pick_rules")

    kb.adjust(1)

    msg = await call.message.answer(
        """
⚖️ روليت أحكام

👥 المشاركين: 0

اضغط دخول للمشاركة
        """,
        reply_markup=kb.as_markup()
    )

    participants[msg.message_id] = []


# دخول روليت أحكام
@dp.callback_query(F.data == "join_rules")
async def join_rules(call: CallbackQuery):

    users = participants.get(call.message.message_id, [])

    if call.from_user.id in users:
        return await call.answer(
            "أنت مشارك مسبقًا",
            show_alert=True
        )

    users.append(call.from_user.id)

    participants[call.message.message_id] = users

    await call.answer("تم دخولك 🎉")


# اختيار حكم
@dp.callback_query(F.data == "pick_rules")
async def pick_rules(call: CallbackQuery):

    users = participants.get(call.message.message_id, [])

    if not users:
        return await call.answer(
            "لا يوجد مشاركين",
            show_alert=True
        )

    winner = random.choice(users)

    user = await bot.get_chat(winner)

    rule = random.choice(rules_list)

    await call.message.answer(
        f"""
⚖️ روليت أحكام

🏆 الشخص المختار:
@{user.username}

📜 الحكم:
{rule}
        """
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
