from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

TOKEN = "8735268386:AAGzFCX4yKoTjdgSjbFId1xP4Rhc-BGJ9oo"

roulette_data = {}

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
🎡 أهلاً بك في بوت الروليت

بوت روليت مخصص للألعاب الترفيهية
والسحوبات داخل القنوات 🎉

✨ يدعم:
• روليت عادي
• روليت الأحكام
• روليت مميز

نتمنى يعجبكم البوت ❤️
"""

    keyboard = [
        [InlineKeyboardButton("🎲 روليت عادي", callback_data="normal")],
        [InlineKeyboardButton("⚖️ روليت الأحكام", callback_data="rules")],
        [InlineKeyboardButton("⭐ روليت مميز", callback_data="vip")]
    ]

    await update.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# الأزرار
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    data = query.data

    # روليت عادي
    if data == "normal":

        context.user_data.clear()
        context.user_data["type"] = "normal"

        await query.message.reply_text(
            "📌 ارسل اسم الروليت:"
        )

    # روليت الأحكام
    elif data == "rules":

        context.user_data.clear()
        context.user_data["type"] = "rules"

        await query.message.reply_text(
            "⚖️ ارسل اسم روليت الأحكام:"
        )

    # روليت مميز
    elif data == "vip":

        context.user_data.clear()
        context.user_data["type"] = "vip"

        await query.message.reply_text(
            "⭐ ارسل عنوان الروليت المميز:"
        )

    # مشاركة
    elif data.startswith("join_"):

        rid = data.split("_")[1]

        if rid not in roulette_data:
            return

        user = query.from_user.first_name

        if user not in roulette_data[rid]["players"]:
            roulette_data[rid]["players"].append(user)

        players = roulette_data[rid]["players"]
        max_players = roulette_data[rid]["max"]

        keyboard = [
            [InlineKeyboardButton(
                f"🎉 مشاركة ({len(players)})",
                callback_data=f"join_{rid}"
            )],

            [InlineKeyboardButton(
                "🎡 تدوير العجلة",
                callback_data=f"spin_{rid}"
            )],

            [InlineKeyboardButton(
                "📢 قناتنا",
                url="https://t.me/NQJNQ"
            )]
        ]

        # روليت الأحكام
        if roulette_data[rid]["type"] == "rules":

            text = f"""
⚖️ {roulette_data[rid]['title']}

👥 المشاركين: {len(players)} من أصل {max_players}

🎭 الحكم سيتم اختياره عشوائياً
"""

        # روليت عادي
        else:

            text = f"""
🎲 {roulette_data[rid]['title']}

👥 المشاركين: {len(players)} من أصل {max_players}

🏆 لم يتم اختيار الفائز بعد
"""

        await query.edit_message_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

# استقبال الرسائل
async def messages(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    # اسم الروليت
    if "title" not in context.user_data:

        context.user_data["title"] = text

        await update.message.reply_text(
            "👥 ارسل عدد المشاركين:"
        )

        return

    # عدد المشاركين
    if "max" not in context.user_data:

        context.user_data["max"] = int(text)

        await update.message.reply_text(
            "📢 ارسل يوزر القناة بدون @"
        )

        return

    # يوزر القناة
    if "channel" not in context.user_data:

        context.user_data["channel"] = text.replace("@", "")

        rid = str(len(roulette_data) + 1)

        roulette_data[rid] = {
            "title": context.user_data["title"],
            "max": context.user_data["max"],
            "channel": context.user_data["channel"],
            "players": [],
            "type": context.user_data["type"]
        }

        keyboard = [
            [InlineKeyboardButton(
                "🎉 مشاركة (0)",
                callback_data=f"join_{rid}"
            )],

            [InlineKeyboardButton(
                "🎡 تدوير العجلة",
                callback_data=f"spin_{rid}"
            )],

            [InlineKeyboardButton(
                "📢 قناتنا",
                url="https://t.me/NQJNQ"
            )]
        ]

        # روليت الأحكام
        if context.user_data["type"] == "rules":

            message_text = f"""
⚖️ {context.user_data['title']}

👥 المشاركين: 0 من أصل {context.user_data['max']}

🎭 الحكم سيتم اختياره عشوائياً
"""

        # روليت عادي + المميز
        else:

            message_text = f"""
🎲 {context.user_data['title']}

👥 المشاركين: 0 من أصل {context.user_data['max']}

🏆 لم يتم اختيار الفائز بعد
"""

        await context.bot.send_message(
            chat_id=f"@{context.user_data['channel']}",
            text=message_text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

        await update.message.reply_text(
            "✅ تم نشر الروليت بالقناة"
        )

        context.user_data.clear()

# تشغيل البوت
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, messages))

print("البوت شغال...")

app.run_polling()
