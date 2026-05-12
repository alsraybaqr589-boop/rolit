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
# قنوات الاشتراك الاجباري
# -----------------------------
CHANNELS = [
    ("قناتنا 1", "https://t.me/NQJNQ"),
    ("قناتنا 2", "https://t.me/KRATEX112"),
]

# -----------------------------
# ستارت
# -----------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton("🌐 روليت عادي", callback_data="normal"),
            InlineKeyboardButton("📜 روليت احكام", callback_data="rules"),
        ],
        [
            InlineKeyboardButton("🌈 روليت مميز", callback_data="vip")
        ],
        [
            InlineKeyboardButton("📢 قناتنا", url="https://t.me/username1")
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
# اختيار نوع الروليت
# -----------------------------
async def roulette_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    mode = query.data

    if mode == "normal":
        title = "🌐 تم اختيار الروليت العادي"
    elif mode == "rules":
        title = "📜 تم اختيار روليت الأحكام"
    else:
        title = "🌈 تم اختيار الروليت المميز"

    keyboard = [
        [
            InlineKeyboardButton("🎭 ابدأ الآن", callback_data=f"join_{mode}")
        ],
        [
            InlineKeyboardButton("🏠 رجوع", callback_data="back")
        ]
    ]

    await query.message.reply_text(
        f"{title}\n\nاضغط على الزر أدناه لبدء اللعب:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# -----------------------------
# الاشتراك الاجباري
# -----------------------------
async def join_channels(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    mode = query.data.replace("join_", "")

    buttons = []

    # ازرار القنوات
    for name, link in CHANNELS:
        buttons.append(
            [InlineKeyboardButton(f"📢 {name}", url=link)]
        )

    # زر تحقق
    buttons.append([
        InlineKeyboardButton("✅ تحققت من الاشتراك", callback_data=f"check_{mode}")
    ])

    await query.message.reply_text(
        "📌 اشترك بالقنوات أولاً ثم اضغط تحقق:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# -----------------------------
# تحقق الاشتراك
# -----------------------------
async def check_sub(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    user_id = query.from_user.id

    mode = query.data.replace("check_", "")

    subscribed = True

    for _, link in CHANNELS:

        username = link.split("/")[-1]

        try:
            member = await context.bot.get_chat_member(
                chat_id=f"@{username}",
                user_id=user_id
            )

            if member.status in ["left", "kicked"]:
                subscribed = False

        except:
            subscribed = False

    if not subscribed:

        await query.answer(
            "❌ لازم تشترك بكل القنوات أولاً",
            show_alert=True
        )
        return

    await query.answer()

    # -------------------------
    # تشغيل الروليت
    # -------------------------
    if mode == "normal":

        keyboard = [
            [
                InlineKeyboardButton("🎡 تدوير العجلة", callback_data="spin_normal")
            ]
        ]

        await query.message.reply_text(
            "🌐 بدأ الروليت العادي!",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif mode == "rules":

        keyboard = [
            [
                InlineKeyboardButton("🎡 تدوير العجلة", callback_data="spin_rules")
            ]
        ]

        await query.message.reply_text(
            "📜 بدأ روليت الأحكام!",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    else:

        keyboard = [
            [
                InlineKeyboardButton("🎡 تدوير عجلة VIP", callback_data="spin_vip")
            ]
        ]

        await query.message.reply_text(
            "🌈 بدأ الروليت المميز!",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

# -----------------------------
# رجوع
# -----------------------------
async def back(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    keyboard = [
        [
            InlineKeyboardButton("🌐 روليت عادي", callback_data="normal"),
            InlineKeyboardButton("📜 روليت احكام", callback_data="rules"),
        ],
        [
            InlineKeyboardButton("🌈 روليت مميز", callback_data="vip")
        ],
        [
            InlineKeyboardButton("📢 قناتنا", url="https://t.me/NQJNQ")
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

app.add_handler(CallbackQueryHandler(roulette_menu, pattern="^(normal|rules|vip)$"))

app.add_handler(CallbackQueryHandler(join_channels, pattern="^join_"))

app.add_handler(CallbackQueryHandler(check_sub, pattern="^check_"))

app.add_handler(CallbackQueryHandler(back, pattern="^back$"))

print("البوت اشتغل ✅")

app.run_polling()
