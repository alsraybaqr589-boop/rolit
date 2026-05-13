from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InputTextMessageContent,
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    InlineQueryHandler,
    ContextTypes,
    filters,
)

import random
import uuid
import os

TOKEN = "8735268386:AAGzFCX4yKoTjdgSjbFId1xP4Rhc-BGJ9oo"

users_data = {}
joined_users = {}

WELCOME = """
🎲 بـوت رولـيـت مخصص للألعاب الترفيهية والسحوبات بالقنوات

✨ البوت يدعم:
• روليت عادي
• روليت أحكام
• روليت مميز
"""

# ================= START =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [

        [InlineKeyboardButton(
            "🎲 روليت عادي",
            callback_data="normal"
        )],

        [InlineKeyboardButton(
            "⚖️ روليت أحكام",
            callback_data="rules"
        )],

        [InlineKeyboardButton(
            "⭐ روليت مميز",
            callback_data="vip"
        )],

        [InlineKeyboardButton(
            "📢 القناة",
            url="https://t.me/NQJNQ"
        )]
    ]

    await update.message.reply_text(
        WELCOME,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ================= INLINE =================

async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.inline_query.query

    # روليت عادي
    if "عادي" in query:

        keyboard = [

            [InlineKeyboardButton(
                "🎉 مشاركة",
                switch_inline_query=""
            )],

            [InlineKeyboardButton(
                "🎡 تدوير العجلة",
                callback_data="spin_normal"
            )]
        ]

        result = InlineQueryResultArticle(
            id=str(uuid.uuid4()),
            title="🎲 روليت عادي",
            input_message_content=InputTextMessageContent(
                """
🎲 روليت عادي

👥 عدد الأعضاء: 25
🏆 عدد الفائزين: 1
"""
            ),
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

        await update.inline_query.answer(
            [result],
            cache_time=1
        )

    # روليت أحكام
    elif "احكام" in query:

        keyboard = [

            [InlineKeyboardButton(
                "🎉 مشاركة",
                switch_inline_query=""
            )],

            [InlineKeyboardButton(
                "🎡 تدوير العجلة",
                callback_data="spin_rules"
            )]
        ]

        result = InlineQueryResultArticle(
            id=str(uuid.uuid4()),
            title="⚖️ روليت أحكام",
            input_message_content=InputTextMessageContent(
                """
⚖️ روليت أحكام

👥 عدد الأعضاء: 25
🏆 عدد الفائزين: 1
"""
            ),
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

        await update.inline_query.answer(
            [result],
            cache_time=1
        )

# ================= BUTTONS =================

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    # روليت عادي
    if query.data == "normal":

        keyboard = [

            [InlineKeyboardButton(
                "✅ بدء",
                switch_inline_query="روليت عادي"
            )],

            [InlineKeyboardButton(
                "🔙 رجوع",
                callback_data="back"
            )]
        ]

        await query.message.edit_text(
            """
🎲 روليت عادي

اضغط بدء ثم اختر القناة
""",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # روليت أحكام
    elif query.data == "rules":

        keyboard = [

            [InlineKeyboardButton(
                "✅ بدء",
                switch_inline_query="روليت احكام"
            )],

            [InlineKeyboardButton(
                "🔙 رجوع",
                callback_data="back"
            )]
        ]

        await query.message.edit_text(
            """
⚖️ روليت أحكام

اضغط بدء ثم اختر القناة
""",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # رجوع
    elif query.data == "back":

        keyboard = [

            [InlineKeyboardButton(
                "🎲 روليت عادي",
                callback_data="normal"
            )],

            [InlineKeyboardButton(
                "⚖️ روليت أحكام",
                callback_data="rules"
            )],

            [InlineKeyboardButton(
                "⭐ روليت مميز",
                callback_data="vip"
            )],

            [InlineKeyboardButton(
                "📢 القناة",
                url="https://t.me/NQJNQ"
            )]
        ]

        await query.message.edit_text(
            WELCOME,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # روليت مميز
    elif query.data == "vip":

        users_data[user_id] = {
            "step": "title"
        }

        await query.message.edit_text(
            "📝 ارسل اسم الروليت:"
        )

    # تدوير عادي
    elif query.data == "spin_normal":

        winners = [
            "Ali",
            "Ahmed",
            "Mustafa",
            "Hussein"
        ]

        winner = random.choice(winners)

        await query.message.reply_text(
            f"🏆 الفائز:\n{winner}"
        )

    # تدوير أحكام
    elif query.data == "spin_rules":

        winners = [
            "Ali",
            "Ahmed",
            "Mustafa",
            "Hussein"
        ]

        rules = [
            "😂 غني أغنية",
            "🔥 غير صورتك",
            "🎤 سجل فويس",
            "😅 ابعت ستيكر"
        ]

        winner = random.choice(winners)
        rule = random.choice(rules)

        await query.message.reply_text(
            f"🏆 الفائز:\n{winner}\n\n⚖️ الحكم:\n{rule}"
        )

# ================= VIP MESSAGES =================

async def messages(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.from_user.id

    if user_id not in users_data:
        return

    step = users_data[user_id]["step"]

    # اسم الروليت
    if step == "title":

        users_data[user_id]["title"] = update.message.text
        users_data[user_id]["step"] = "members"

        await update.message.reply_text(
            "👥 ارسل عدد الأعضاء:"
        )

    # عدد الأعضاء
    elif step == "members":

        users_data[user_id]["members"] = update.message.text
        users_data[user_id]["step"] = "winners"

        await update.message.reply_text(
            "🏆 ارسل عدد الفائزين:"
        )

    # عدد الفائزين
    elif step == "winners":

        users_data[user_id]["winners"] = update.message.text
        users_data[user_id]["step"] = "channel"

        await update.message.reply_text(
            "📢 ارسل يوزر القناة بدون @"
        )

    # القناة
    elif step == "channel":

        title = users_data[user_id]["title"]
        members = users_data[user_id]["members"]
        winners = users_data[user_id]["winners"]
        channel = update.message.text

        keyboard = [

            [InlineKeyboardButton(
                "🎉 مشاركة",
                switch_inline_query=""
            )],

            [InlineKeyboardButton(
                "🎡 تدوير العجلة",
                callback_data="spin_vip"
            )]
        ]

        await context.bot.send_message(
            chat_id=f"@{channel}",
            text=f"""
⭐ {title}

👥 عدد الأعضاء: {members}
🏆 عدد الفائزين: {winners}
""",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

        await update.message.reply_text(
            "✅ تم نشر الروليت المميز"
        )

        del users_data[user_id]

# ================= MAIN =================

def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(InlineQueryHandler(inline_query))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, messages))

    print("Bot Started")

    app.run_polling()

if __name__ == "__main__":
    main()
