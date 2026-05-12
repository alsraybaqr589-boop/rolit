from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = "8735268386:AAFwZAjHtxosdtVczb054Ckm5mI9PpRmGKE"

user_data_store = {}

# ================= START =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("🌐 روليت عادي", callback_data="normal"),
            InlineKeyboardButton("📜 روليت أحكام", callback_data="rules")
        ],
        [
            InlineKeyboardButton("🌈 روليت مميز", callback_data="vip")
        ],
        [
            InlineKeyboardButton("📢 قناتنا", url="https://t.me/NQJNQ")
        ]
    ]

    text = """
🎮 أهلاً بك في بوت الروليت

✨ الأقسام:
• روليت عادي
• روليت أحكام
• روليت VIP
"""

    await update.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ================= اختيار النوع =================

async def roulette_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    roulette_type = query.data
    user_id = query.from_user.id

    user_data_store[user_id] = {
        "type": roulette_type
    }

    names = {
        "normal": "🌐 روليت عادي",
        "rules": "📜 روليت أحكام",
        "vip": "🌈 روليت VIP"
    }

    keyboard = [
        [InlineKeyboardButton("🎭 ابدأ الآن", callback_data="create_roulette")],
        [InlineKeyboardButton("🏠 رجوع", callback_data="back_home")]
    ]

    await query.message.reply_text(
        f"تم اختيار {names[roulette_type]}\n\nاضغط على الزر أدناه لبدء اللعب:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ================= إنشاء الروليت =================

async def create_roulette(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    user_data_store[user_id]["step"] = "title"

    keyboard = [
        [InlineKeyboardButton("إلغاء", callback_data="cancel")]
    ]

    await query.message.reply_text(
        "📝 أرسل الآن عنوان المسابقة:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ================= استقبال البيانات =================

async def messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if user_id not in user_data_store:
        return

    data = user_data_store[user_id]

    if "step" not in data:
        return

    text = update.message.text

    # عنوان
    if data["step"] == "title":
        data["title"] = text
        data["step"] = "members"

        await update.message.reply_text(
            "👥 أرسل الحد الأقصى للمشاركين:"
        )
        return

    # المشاركين
    if data["step"] == "members":
        data["members"] = text
        data["step"] = "winners"

        await update.message.reply_text(
            "🏆 أرسل عدد الفائزين:"
        )
        return

    # الفائزين
    if data["step"] == "winners":
        data["winners"] = text
        data["step"] = "channel"

        await update.message.reply_text(
            "📢 أرسل الآن معرف القناة فقط\n\nمثال:\nNQJNQ\n\nتأكد من رفع البوت أدمن بالقناة"
        )
        return

    # القناة
    if data["step"] == "channel":

        channel = text.replace("@", "").replace("https://t.me/", "")

        roulette_id = str(user_id)[-4:]

        roulette_name = {
            "normal": "🌐 روليت عادي",
            "rules": "📜 روليت أحكام",
            "vip": "🌈 روليت VIP"
        }

        keyboard = [
            [
                InlineKeyboardButton(
                    "🎉 دخول",
                    url=f"https://t.me/{context.bot.username}?start=join_{roulette_id}"
                )
            ]
        ]

        message = f"""
{roulette_name[data['type']]}

🆔 رقم الروليت:
{roulette_id}

📝 العنوان:
{data['title']}

👥 الحد الأقصى:
{data['members']}

🏆 عدد الفائزين:
{data['winners']}
"""

        try:
            await context.bot.send_message(
                chat_id=f"@{channel}",
                text=message,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

            await update.message.reply_text(
                "✅ تم نشر الروليت بالقناة بنجاح"
            )

        except Exception as e:
            await update.message.reply_text(
                f"❌ فشل النشر\n\nتأكد أن البوت أدمن بالقناة\n\n{e}"
            )

        data["step"] = None

# ================= رجوع =================

async def back_home(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [
            InlineKeyboardButton("🌐 روليت عادي", callback_data="normal"),
            InlineKeyboardButton("📜 روليت أحكام", callback_data="rules")
        ],
        [
            InlineKeyboardButton("🌈 روليت مميز", callback_data="vip")
        ],
        [
            InlineKeyboardButton("📢 قناتنا", url="https://t.me/NQJNQ")
        ]
    ]

    await query.message.reply_text(
        "🏠 القائمة الرئيسية",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ================= إلغاء =================

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.message.reply_text("❌ تم الإلغاء")

# ================= تشغيل =================

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(CallbackQueryHandler(roulette_type, pattern="^(normal|rules|vip)$"))

app.add_handler(CallbackQueryHandler(create_roulette, pattern="^create_roulette$"))

app.add_handler(CallbackQueryHandler(back_home, pattern="^back_home$"))

app.add_handler(CallbackQueryHandler(cancel, pattern="^cancel$"))

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, messages))

print("Bot Started")

app.run_polling()
