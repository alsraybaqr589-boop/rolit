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

    results = []

    # روليت عادي
    keyboard_normal = [

        [InlineKeyboardButton(
            "🎉 مشاركة (0)",
            callback_data="join_normal"
        )],

        [InlineKeyboardButton(
            "🎡 تدوير العجلة",
            callback_data="spin_normal"
        )]
    ]

    normal_result = InlineQueryResultArticle(
        id=str(uuid.uuid4()),
        title="🎲 روليت عادي",
        input_message_content=InputTextMessageContent(
            """
🎲 روليت عادي

👥 المشاركين: 0 من أصل 25
🏆 عدد الفائزين: 1
"""
        ),
        reply_markup=InlineKeyboardMarkup(keyboard_normal)
    )

    results.append(normal_result)

    # روليت أحكام
    keyboard_rules = [

        [InlineKeyboardButton(
            "🎉 مشاركة (0)",
            callback_data="join_rules"
        )],

        [InlineKeyboardButton(
            "🎡 تدوير العجلة",
            callback_data="spin_rules"
        )]
    ]

    rules_result = InlineQueryResultArticle(
        id=str(uuid.uuid4()),
        title="⚖️ روليت أحكام",
        input_message_content=InputTextMessageContent(
            """
⚖️ روليت أحكام

👥 المشاركين: 0 من أصل 25
🏆 عدد الفائزين: 1
"""
        ),
        reply_markup=InlineKeyboardMarkup(keyboard_rules)
    )

    results.append(rules_result)

    await update.inline_query.answer(
        results,
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
                switch_inline_query=""
            )],

            [InlineKeyboardButton(
                "📢 القناة",
                url="https://t.me/NQJNQ"
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
                switch_inline_query=""
            )],

            [InlineKeyboardButton(
                "📢 القناة",
                url="https://t.me/NQJNQ"
            )]
        ]

        await query.message.edit_text(
            """
⚖️ روليت أحكام

اضغط بدء ثم اختر القناة
""",
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

    # مشاركة روليت عادي
    elif query.data == "join_normal":

        text = query.message.text

        try:

            current = int(
                text.split("المشاركين: ")[1]
                .split(" من")[0]
            )

            current += 1

            new_text = f"""
🎲 روليت عادي

👥 المشاركين: {current} من أصل 25
🏆 عدد الفائزين: 1
"""

            keyboard = [

                [InlineKeyboardButton(
                    f"🎉 مشاركة ({current})",
                    callback_data="join_normal"
                )],

                [InlineKeyboardButton(
                    "🎡 تدوير العجلة",
                    callback_data="spin_normal"
                )]
            ]

            await query.message.edit_text(
                new_text,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

        except:
            pass

    # مشاركة روليت أحكام
    elif query.data == "join_rules":

        text = query.message.text

        try:

            current = int(
                text.split("المشاركين: ")[1]
                .split(" من")[0]
            )

            current += 1

            new_text = f"""
⚖️ روليت أحكام

👥 المشاركين: {current} من أصل 25
🏆 عدد الفائزين: 1
"""

            keyboard = [

                [InlineKeyboardButton(
                    f"🎉 مشاركة ({current})",
                    callback_data="join_rules"
                )],

                [InlineKeyboardButton(
                    "🎡 تدوير العجلة",
                    callback_data="spin_rules"
                )]
            ]

            await query.message.edit_text(
                new_text,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

        except:
            pass

    # تدوير روليت عادي
    elif query.data == "spin_normal":

        names = [
            "Ali",
            "Ahmed",
            "Mustafa",
            "Hussein",
            "Zaid"
        ]

        winner = random.choice(names)

        await query.message.reply_text(
            f"🏆 الفائز:\n{winner}"
        )

    # تدوير روليت أحكام
    elif query.data == "spin_rules":

        names = [
            "Ali",
            "Ahmed",
            "Mustafa",
            "Hussein",
            "Zaid"
        ]

        rules = [
            "😂 غني أغنية",
            "🔥 غير صورتك",
            "🎤 سجل فويس",
            "😅 ابعت ستيكر"
        ]

        winner = random.choice(names)
        rule = random.choice(rules)

        await query.message.reply_text(
            f"🏆 الفائز:\n{winner}\n\n⚖️ الحكم:\n{rule}"
        )

    # تدوير روليت مميز
    elif query.data == "spin_vip":

        names = [
            "Ali",
            "Ahmed",
            "Mustafa",
            "Hussein",
            "Zaid"
        ]

        winner = random.choice(names)

        await query.message.reply_text(
            f"🏆 الفائز:\n{winner}"
        )

# ================= VIP =================

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
                "🎉 مشاركة (0)",
                callback_data="join_vip"
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

👥 المشاركين: 0 من أصل {members}
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
    app.add_handler(InlineQueryHandler(inline_query))
    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, messages))

    print("Bot Started")

    app.run_polling()

if __name__ == "__main__":
