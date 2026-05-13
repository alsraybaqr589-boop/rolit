from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

import random
import os

TOKEN = os.getenv("8735268386:AAGzFCX4yKoTjdgSjbFId1xP4Rhc-BGJ9oo")

users_data = {}
joined_users = {}

WELCOME = """
🎲 بـوت رولـيـت مخصص للألعاب الترفيهية والسحوبات بالقنوات

✨ البوت يدعم:
• روليت عادي
• روليت أحكام
• روليت مميز

📢 شارك الروليت بقناتك وخلي الأعضاء يشاركون بسهولة
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

        # زر القناة بالقائمة الرئيسية
        [InlineKeyboardButton(
            "📢 القناة",
            url="https://t.me/NQJNQ"
        )]
    ]

    await update.message.reply_text(
        WELCOME,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ================= BUTTONS =================

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    # ================= روليت عادي =================

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

        text = """
🎲 روليت عادي

اضغط بدء ثم اختر القناة حتى يتم نشر الروليت داخل القناة
"""

        await query.message.edit_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # ================= روليت أحكام =================

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

        text = """
⚖️ روليت أحكام

اضغط بدء ثم اختر القناة حتى يتم نشر الروليت داخل القناة
"""

        await query.message.edit_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # ================= رجوع =================

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

    # ================= روليت مميز =================

    elif query.data == "vip":

        users_data[user_id] = {"step": "title"}

        await query.message.edit_text(
            "📝 أرسل اسم الروليت:"
        )

    # ================= مشاركة =================

    elif query.data.startswith("join_"):

        rid = query.data.split("_")[1]

        if rid not in joined_users:
            joined_users[rid] = []

        if user_id not in joined_users[rid]:
            joined_users[rid].append(user_id)

        count = len(joined_users[rid])

        keyboard = [

            [InlineKeyboardButton(
                f"🎉 مشاركة ({count})",
                callback_data=f"join_{rid}"
            )],

            [InlineKeyboardButton(
                "🎡 تدوير العجلة",
                callback_data=f"spin_{rid}"
            )]
        ]

        await query.message.edit_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # ================= تدوير =================

    elif query.data.startswith("spin_"):

        rid = query.data.split("_")[1]

        if rid not in joined_users or len(joined_users[rid]) == 0:

            await query.answer(
                "❌ لا يوجد مشاركين",
                show_alert=True
            )

            return

        winner = random.choice(joined_users[rid])

        await query.message.reply_text(
            f"🏆 الفائز:\n[{winner}](tg://user?id={winner})",
            parse_mode="Markdown"
        )

# ================= الرسائل =================

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
            "👥 أرسل عدد الأعضاء:"
        )

    # عدد الأعضاء
    elif step == "members":

        users_data[user_id]["members"] = update.message.text
        users_data[user_id]["step"] = "winners"

        await update.message.reply_text(
            "🏆 أرسل عدد الفائزين:"
        )

    # عدد الفائزين
    elif step == "winners":

        users_data[user_id]["winners"] = update.message.text
        users_data[user_id]["step"] = "channel"

        await update.message.reply_text(
            "📢 أرسل يوزر القناة بدون @"
        )

    # القناة
    elif step == "channel":

        title = users_data[user_id]["title"]
        members = users_data[user_id]["members"]
        winners = users_data[user_id]["winners"]
        channel = update.message.text

        rid = str(random.randint(1000, 999999))

        joined_users[rid] = []

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

        text = f"""
⭐ {title}

👥 المشاركين: 0 من أصل {members}

🏆 عدد الفائزين:
{winners}
"""

        await update.message.reply_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

        del users_data[user_id]

# ================= MAIN =================

def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, messages))

    print("Bot Started")

    app.run_polling()

if __name__ == "__main__":
    main()
