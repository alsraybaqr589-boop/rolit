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

# البداية
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
🎡 أهلاً بك في بوت الروليت

بوت مخصص للسحوبات والألعاب
داخل قنوات التليجرام 🎉
"""

    keyboard = [

        [InlineKeyboardButton(
            "🎲 روليت عادي",
            callback_data="normal"
        )],

        [InlineKeyboardButton(
            "⚖️ روليت الأحكام",
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

        keyboard = [

            [InlineKeyboardButton(
                "▶️ بدء",
                callback_data="start_normal"
            )],

            [InlineKeyboardButton(
                "🔙 رجوع",
                callback_data="back"
            )]
        ]

        await query.message.edit_text(
            "🎲 روليت عادي",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # روليت الأحكام
    elif data == "rules":

        keyboard = [

            [InlineKeyboardButton(
                "▶️ بدء",
                callback_data="start_rules"
            )],

            [InlineKeyboardButton(
                "🔙 رجوع",
                callback_data="back"
            )]
        ]

        await query.message.edit_text(
            "⚖️ روليت الأحكام",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # روليت مميز
    elif data == "vip":

        context.user_data.clear()
        context.user_data["type"] = "vip"

        await query.message.reply_text(
            "📌 ارسل اسم الروليت:"
        )

    # رجوع
    elif data == "back":

        await start(update, context)

    # بدء العادي
    elif data == "start_normal":

        context.user_data.clear()
        context.user_data["type"] = "normal"

        await query.message.reply_text(
            "📢 ارسل يوزر القناة بدون @"
        )

    # بدء الأحكام
    elif data == "start_rules":

        context.user_data.clear()
        context.user_data["type"] = "rules"

        await query.message.reply_text(
            "📢 ارسل يوزر القناة بدون @"
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

        keyboard = [
            [InlineKeyboardButton(
                f"🎉 مشاركة ({len(players)})",
                callback_data=f"join_{rid}"
            )],

            [InlineKeyboardButton(
                "🎡 تدوير العجلة",
                callback_data=f"spin_{rid}"
            )]
        ]

        # روليت الأحكام
        if roulette_data[rid]["type"] == "rules":

            text = f"""
⚖️ روليت الأحكام

👥 المشاركين: {len(players)}
🎭 الحكم عشوائي
"""

        # روليت عادي
        elif roulette_data[rid]["type"] == "normal":

            text = f"""
🎲 روليت عادي

👥 المشاركين: {len(players)}
🏆 سيتم اختيار الفائز عشوائياً
"""

        # روليت مميز
        else:

            text = f"""
⭐ {roulette_data[rid]['title']}

👥 المشاركين: {len(players)} من أصل {roulette_data[rid]['max']}

🏆 عدد الفائزين:
{roulette_data[rid]['wins']}
"""

        await query.edit_message_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

# استقبال الرسائل
async def messages(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    # روليت عادي
    if context.user_data.get("type") == "normal":

        keyboard = [
            [InlineKeyboardButton(
                "🎉 مشاركة (0)",
                callback_data="join_1"
            )],

            [InlineKeyboardButton(
                "🎡 تدوير العجلة",
                callback_data="spin_1"
            )]
        ]

        roulette_data["1"] = {
            "players": [],
            "type": "normal"
        }

        await context.bot.send_message(
            chat_id=f"@{text}",
            text="""
🎲 روليت عادي

👥 المشاركين: 0
🏆 سيتم اختيار الفائز عشوائياً
""",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

        await update.message.reply_text(
            "✅ تم نشر الروليت"
        )

        context.user_data.clear()

    # روليت الأحكام
    elif context.user_data.get("type") == "rules":

        keyboard = [
            [InlineKeyboardButton(
                "🎉 مشاركة (0)",
                callback_data="join_2"
            )],

            [InlineKeyboardButton(
                "🎡 تدوير العجلة",
                callback_data="spin_2"
            )]
        ]

        roulette_data["2"] = {
            "players": [],
            "type": "rules"
        }

        await context.bot.send_message(
            chat_id=f"@{text}",
            text="""
⚖️ روليت الأحكام

👥 المشاركين: 0
🎭 الحكم عشوائي
""",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

        await update.message.reply_text(
            "✅ تم نشر روليت الأحكام"
        )

        context.user_data.clear()

    # روليت مميز
    elif context.user_data.get("type") == "vip":

        if "title" not in context.user_data:

            context.user_data["title"] = text

            await update.message.reply_text(
                "👥 ارسل عدد المشاركين:"
            )

            return

        if "max" not in context.user_data:

            context.user_data["max"] = text

            await update.message.reply_text(
                "🏆 ارسل عدد الفائزين:"
            )

            return

        if "wins" not in context.user_data:

            context.user_data["wins"] = text

            await update.message.reply_text(
                "📢 ارسل يوزر القناة بدون @"
            )

            return

        rid = "3"

        roulette_data[rid] = {
            "title": context.user_data["title"],
            "max": context.user_data["max"],
            "wins": context.user_data["wins"],
            "players": [],
            "type": "vip"
        }

        keyboard = [
            [InlineKeyboardButton(
                "🎉 مشاركة (0)",
                callback_data=f"join_{rid}"
            )],

            [InlineKeyboardButton(
                "🎡 تدوير العجلة",
                callback_data=f"spin_{rid}"
            )]
        ]

        await context.bot.send_message(
            chat_id=f"@{text}",
            text=f"""
⭐ {context.user_data['title']}

👥 المشاركين: 0 من أصل {context.user_data['max']}

🏆 عدد الفائزين:
{context.user_data['wins']}
""",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

        await update.message.reply_text(
            "✅ تم نشر الروليت المميز"
        )

        context.user_data.clear()

# تشغيل
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, messages))

print("البوت شغال...")

app.run_polling()
