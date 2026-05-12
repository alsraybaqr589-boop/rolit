from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

TOKEN = "8735268386:AAFwZAjHtxosdtVczb054Ckm5mI9PpRmGKE"


# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton("🌐 روليت عادي", callback_data="normal_roulette"),
            InlineKeyboardButton("📜 روليت أحكام", callback_data="rules_roulette")
        ],
        [
            InlineKeyboardButton("🌈 روليت مميز", callback_data="vip_roulette")
        ],
        [
            InlineKeyboardButton("📢 قناتنا", url="https://t.me/USERNAME")
        ]
    ]

    text = (
        "🎮 أهلاً بك في بوت الروليت\n\n"
        "✨ الأقسام:\n"
        "• روليت عادي\n"
        "• روليت أحكام\n"
        "• روليت VIP"
    )

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
    if data == "normal_roulette":

        keyboard = [
            [
                InlineKeyboardButton(
                    "🎭 ابدأ الآن",
                    callback_data="start_normal"
                )
            ],
            [
                InlineKeyboardButton(
                    "🏠 رجوع",
                    callback_data="back_main"
                )
            ]
        ]

        await query.message.reply_text(
            "🌐 تم اختيار روليت العادي\n\n"
            "اضغط على الزر أدناه لبدء اللعب:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # روليت أحكام
    elif data == "rules_roulette":

        keyboard = [
            [
                InlineKeyboardButton(
                    "🎭 ابدأ الآن",
                    callback_data="start_rules"
                )
            ],
            [
                InlineKeyboardButton(
                    "🏠 رجوع",
                    callback_data="back_main"
                )
            ]
        ]

        await query.message.reply_text(
            "📜 تم اختيار روليت الأحكام\n\n"
            "اضغط على الزر أدناه لبدء اللعب:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # روليت مميز
    elif data == "vip_roulette":

        await query.message.reply_text(
            "🌈 إنشاء روليت مميز\n\n"
            "✏️ أرسل العنوان:"
        )

    # رجوع
    elif data == "back_main":

        keyboard = [
            [
                InlineKeyboardButton("🌐 روليت عادي", callback_data="normal_roulette"),
                InlineKeyboardButton("📜 روليت أحكام", callback_data="rules_roulette")
            ],
            [
                InlineKeyboardButton("🌈 روليت مميز", callback_data="vip_roulette")
            ],
            [
                InlineKeyboardButton("📢 قناتنا", url="https://t.me/USERNAME")
            ]
        ]

        text = (
            "🎮 أهلاً بك في بوت الروليت\n\n"
            "✨ الأقسام:\n"
            "• روليت عادي\n"
            "• روليت أحكام\n"
            "• روليت VIP"
        )

        await query.message.reply_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # بدء الروليت العادي
    elif data == "start_normal":

        await query.message.reply_text(
            "🎭 بدأ الروليت العادي!"
        )

    # بدء روليت الأحكام
    elif data == "start_rules":

        await query.message.reply_text(
            "📜 بدأ روليت الأحكام!"
        )


# تشغيل البوت
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))

print("Bot is running...")
app.run_polling()
