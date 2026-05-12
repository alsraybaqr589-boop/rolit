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
    ContextTypes,
    filters
)

import random

TOKEN = "8735268386:AAFwZAjHtxosdtVczb054Ckm5mI9PpRmGKE"

# تخزين بيانات الروليتات
roulette_data = {}

# تخزين حالة المستخدم
user_state = {}


# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton("🌐 روليت عادي", callback_data="normal")
        ],
        [
            InlineKeyboardButton("📜 روليت أحكام", callback_data="rules")
        ],
        [
            InlineKeyboardButton("🌈 روليت مميز", callback_data="vip")
        ]
    ]

    await update.message.reply_text(
        "🎮 أهلاً بك في بوت الروليت\n\nاختر نوع الروليت:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# الأزرار
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    data = query.data
    user_id = query.from_user.id

    # روليت عادي
    if data == "normal":

        user_state[user_id] = {
            "type": "normal",
            "step": "title"
        }

        await query.message.reply_text(
            "✏️ أرسل عنوان الروليت:"
        )

    # روليت أحكام
    elif data == "rules":

        user_state[user_id] = {
            "type": "rules",
            "step": "title"
        }

        await query.message.reply_text(
            "✏️ أرسل عنوان روليت الأحكام:"
        )

    # روليت VIP
    elif data == "vip":

        user_state[user_id] = {
            "type": "vip",
            "step": "title"
        }

        await query.message.reply_text(
            "🌈 أرسل عنوان الروليت المميز:"
        )

    # مشاركة
    elif data.startswith("join_"):

        roulette_id = data.split("_")[1]

        if roulette_id not in roulette_data:
            return

        user = query.from_user

        if user.id not in roulette_data[roulette_id]["participants"]:

            roulette_data[roulette_id]["participants"].append(user.id)

        count = len(roulette_data[roulette_id]["participants"])

        text = (
            f"🎮 {roulette_data[roulette_id]['title']}\n\n"
            f"👥 المشاركين: {count} من أصل {roulette_data[roulette_id]['max']}\n"
            f"🏆 عدد الفائزين: {roulette_data[roulette_id]['winners']}"
        )

        keyboard = [
            [
                InlineKeyboardButton(
                    f"🎉 مشاركة ({count})",
                    callback_data=f"join_{roulette_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    "🎡 تدوير العجلة",
                    callback_data=f"spin_{roulette_id}"
                )
            ]
        ]

        await query.message.edit_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # تدوير
    elif data.startswith("spin_"):

        roulette_id = data.split("_")[1]

        if roulette_id not in roulette_data:
            return

        users = roulette_data[roulette_id]["participants"]

        if len(users) == 0:

            await query.answer(
                "لا يوجد مشاركين!",
                show_alert=True
            )

            return

        winners_count = roulette_data[roulette_id]["winners"]

        if winners_count > len(users):
            winners_count = len(users)

        winners = random.sample(users, winners_count)

        result = "🏆 الفائزين:\n\n"

        for w in winners:
            result += f"• {w}\n"

        await query.message.reply_text(result)


# استقبال الرسائل
async def messages(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.from_user.id

    if user_id not in user_state:
        return

    state = user_state[user_id]

    text = update.message.text

    # العنوان
    if state["step"] == "title":

        state["title"] = text
        state["step"] = "max"

        await update.message.reply_text(
            "👥 أرسل الحد الأقصى للمشاركين:"
        )

    # الحد الأقصى
    elif state["step"] == "max":

        state["max"] = int(text)
        state["step"] = "winners"

        await update.message.reply_text(
            "🏆 أرسل عدد الفائزين:"
        )

    # عدد الفائزين
    elif state["step"] == "winners":

        state["winners"] = int(text)
        state["step"] = "channel"

        await update.message.reply_text(
            "📢 أرسل معرف القناة مثال:\n@channel"
        )

    # القناة
    elif state["step"] == "channel":

        channel = text

        roulette_id = str(random.randint(1000, 9999))

        roulette_data[roulette_id] = {
            "title": state["title"],
            "max": state["max"],
            "winners": state["winners"],
            "participants": []
        }

        message_text = (
            f"🎮 {state['title']}\n\n"
            f"👥 المشاركين: 0 من أصل {state['max']}\n"
            f"🏆 عدد الفائزين: {state['winners']}"
        )

        keyboard = [
            [
                InlineKeyboardButton(
                    "🎉 مشاركة (0)",
                    callback_data=f"join_{roulette_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    "🎡 تدوير العجلة",
                    callback_data=f"spin_{roulette_id}"
                )
            ]
        ]

        try:

            await context.bot.send_message(
                chat_id=channel,
                text=message_text,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

            await update.message.reply_text(
                "✅ تم نشر الروليت بالقناة بنجاح!"
            )

        except:

            await update.message.reply_text(
                "❌ فشل النشر\n\n"
                "تأكد رفعت البوت مشرف بالقناة"
            )

        del user_state[user_id]


# تشغيل البوت
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))
app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, messages)
)

print("Bot Started...")
app.run_polling()
