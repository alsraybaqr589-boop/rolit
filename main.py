# -*- coding: utf-8 -*-

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

TOKEN = "8735268386:AAFwZAjHtxosdtVczb054Ckm5mI9PpRmGKE"

# -----------------------------
# /start
# -----------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [

        [
            InlineKeyboardButton(
                "🌐 روليت عادي",
                callback_data="normal"
            ),

            InlineKeyboardButton(
                "📜 روليت أحكام",
                callback_data="rules"
            )
        ],

        [
            InlineKeyboardButton(
                "🌈 روليت مميز",
                callback_data="vip"
            )
        ],

        [
            InlineKeyboardButton(
                "📢 القناة",
                url="https://t.me/USERNAME"
            )
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

# -----------------------------
# القائمة
# -----------------------------
async def roulette_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    data = query.data

    # -------------------------
    # روليت عادي
    # -------------------------
    if data == "normal":

        keyboard = [

            [
                InlineKeyboardButton(
                    "🎭 ابدأ الآن",
                    switch_inline_query="روليت عادي"
                )
            ],

            [
                InlineKeyboardButton(
                    "📢 القناة",
                    url="https://t.me/NQJNQ"
                )
            ],

            [
                InlineKeyboardButton(
                    "🏠 خروج",
                    callback_data="back"
                )
            ]
        ]

        await query.message.reply_text(
            "🌐 تم اختيار الروليت العادي\n\nاضغط على الزر أدناه:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # -------------------------
    # روليت أحكام
    # -------------------------
    elif data == "rules":

        keyboard = [

            [
                InlineKeyboardButton(
                    "📜 ابدأ الآن",
                    switch_inline_query="روليت أحكام"
                )
            ],

            [
                InlineKeyboardButton(
                    "📢 القناة",
                    url="https://t.me/USERNAME"
                )
            ],

            [
                InlineKeyboardButton(
                    "🏠 خروج",
                    callback_data="back"
                )
            ]
        ]

        await query.message.reply_text(
            "📜 تم اختيار روليت الأحكام\n\nاضغط على الزر أدناه:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # -------------------------
    # روليت مميز
    # -------------------------
    elif data == "vip":

        await query.message.reply_text(
            "🌈 قسم الروليت المميز\n\n"
            "هذا القسم تكدر تطوره لاحقاً."
        )

    # -------------------------
    # رجوع
    # -------------------------
    elif data == "back":

        keyboard = [

            [
                InlineKeyboardButton(
                    "🌐 روليت عادي",
                    callback_data="normal"
                ),

                InlineKeyboardButton(
                    "📜 روليت أحكام",
                    callback_data="rules"
                )
            ],

            [
                InlineKeyboardButton(
                    "🌈 روليت مميز",
                    callback_data="vip"
                )
            ],

            [
                InlineKeyboardButton(
                    "📢 القناة",
                    url="https://t.me/USERNAME"
                )
            ]
        ]

        await query.message.reply_text(
            "🏠 رجعت للقائمة الرئيسية",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

# -----------------------------
# تشغيل البوت
# -----------------------------
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(
    CallbackQueryHandler(
        roulette_menu
    )
)

print("البوت شغال ✅")

app.run_polling()
