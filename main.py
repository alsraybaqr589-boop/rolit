from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)

TOKEN = "8735268386:AAFwZAjHtxosdtVczb054Ckm5mI9PpRmGKE"

TITLE, MEMBERS, WINNERS, CHANNEL = range(4)

roulette_data = {}
participants = {}

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("🌈 إنشاء روليت مميز", callback_data="create_vip")]
    ]

    await update.message.reply_text(
        "اختر:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# اختيار إنشاء روليت
async def create_vip(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    await query.message.reply_text("📝 ارسل عنوان الروليت:")

    return TITLE

# العنوان
async def get_title(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["title"] = update.message.text

    await update.message.reply_text("👥 ارسل عدد الأعضاء:")

    return MEMBERS

# عدد الأعضاء
async def get_members(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["members"] = update.message.text

    await update.message.reply_text("🏆 ارسل عدد الفائزين:")

    return WINNERS

# عدد الفائزين
async def get_winners(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["winners"] = update.message.text

    await update.message.reply_text("📢 ارسل رابط القناة:")

    return CHANNEL

# رابط القناة + نشر
async def publish(update: Update, context: ContextTypes.DEFAULT_TYPE):

    channel = update.message.text

    title = context.user_data["title"]
    members = context.user_data["members"]
    winners = context.user_data["winners"]

    roulette_id = len(participants) + 1000

    participants[roulette_id] = []

    text = f"""
🌈 روليت مميز

🆔 رقم الروليت:
{roulette_id}

📝 العنوان:
{title}

👥 الحد الأقصى:
{members}

🏆 عدد الفائزين:
{winners}
"""

    keyboard = [
        [InlineKeyboardButton(
            "🔴 دخول 🎉",
            url=f"https://t.me/{context.bot.username}?start=join_{roulette_id}"
        )],

        [InlineKeyboardButton("📢 القناة", url=channel)]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_markup=reply_markup
    )

    await update.message.reply_text("✅ تم نشر الروليت")

    return ConversationHandler.END

# دخول المشاركين من الكروب
async def join(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if context.args:

        data = context.args[0]

        if data.startswith("join_"):

            roulette_id = int(data.split("_")[1])

            user = update.effective_user.first_name

            if user not in participants[roulette_id]:
                participants[roulette_id].append(user)

            count = len(participants[roulette_id])

            await update.message.reply_text(
                f"✅ تم تسجيلك بنجاح\n({count}) مشارك حالياً"
            )

# تشغيل
app = Application.builder().token(TOKEN).build()

conv = ConversationHandler(
    entry_points=[CallbackQueryHandler(create_vip, pattern="create_vip")],

    states={

        TITLE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, get_title)
        ],

        MEMBERS: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, get_members)
        ],

        WINNERS: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, get_winners)
        ],

        CHANNEL: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, publish)
        ],
    },

    fallbacks=[]
)

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("start", join))
app.add_handler(conv)

print("البوت شغال 🔥")

app.run_polling()
