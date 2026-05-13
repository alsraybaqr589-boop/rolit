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

        [InlineKeyboardButton(
            "📢 القناة",
            url="https://t.me/NQJNQ"
        )]
    ]

    await update.message.reply_text(
        WELCOME,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ================= INLINE SHARE =================

async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.inline_query.query

    # روليت عادي
    if "عادي" in query:

        keyboard = [

            [InlineKeyboardButton(
                "🎉 مشاركة (0)",
                callback_data="join_normal"
            )],

            [InlineKeyboardButton(
                "🎡 تدوير العجلة",
                callback_data="spin_normal"
            )]
        ]

        result = InlineQueryResultArticle(
            id=str(uuid.uuid4()),
            title="🎲 نشر روليت عادي",
            input_message_content=InputTextMessageContent(
                """
🎲 روليت عادي

👥 المشاركين: 0
🏆 سيتم اختيار الفائز عشوائياً
"""
            ),
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

        await update.inline_query.answer(
            [result],
            cache_time=1
        )

    # روليت أحكام
    elif "احكام" in query:

        keyboard = [

            [InlineKeyboardButton(
                "🎉 مشاركة (0)",
                callback_data="join_rules"
            )],

            [InlineKeyboardButton(
                "🎡 تدوير العجلة",
                callback_data="spin_rules"
            )]
        ]

        result = InlineQueryResultArticle(
            id=str(uuid.uuid4()),
            title="⚖️ نشر روليت أحكام",
            input_message_content=InputTextMessageContent(
                """
⚖️ روليت أحكام

👥 المشاركين: 0
🎭 الحكم عشوائي
"""
            ),
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

        await update.inline_query.answer(
            [result],
            cache_time=1
        )

# ================= BUTTONS =================

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    # روليت عادي
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
                switch_inline_query="روليت احكام"
            )],

            [InlineKeyboardButton(
                "🔙 رجوع",
                callback_data="back"
            )]
        ]

        await query.message.edit_text(
            """
⚖️ روليت أحكام

اضغط بدء ثم اختر القناة
""",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # رجوع
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

    # روليت مميز
    elif query.data == "vip":

        await query.message.edit_text(
            "⭐ روليت مميز قيد التطوير"
        )

    # مشاركة عادي
    elif query.data == "join_normal":

        if "normal" not in joined_users:
            joined_users["normal"] = []

        if query.from_user.id not in joined_users["normal"]:
            joined_users["normal"].append(query.from_user.id)

        count = len(joined_users["normal"])

        keyboard = [

            [InlineKeyboardButton(
                f"🎉 مشاركة ({count})",
                callback_data="join_normal"
            )],

            [InlineKeyboardButton(
                "🎡 تدوير العجلة",
                callback_data="spin_normal"
            )]
        ]

        await query.message.edit_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # مشاركة أحكام
    elif query.data == "join_rules":

        if "rules" not in joined_users:
            joined_users["rules"] = []

        if query.from_user.id not in joined_users["rules"]:
            joined_users["rules"].append(query.from_user.id)

        count = len(joined_users["rules"])

        keyboard = [

            [InlineKeyboardButton(
                f"🎉 مشاركة ({count})",
                callback_data="join_rules"
            )],

            [InlineKeyboardButton(
                "🎡 تدوير العجلة",
                callback_data="spin_rules"
            )]
        ]

        await query.message.edit_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # تدوير عادي
    elif query.data == "spin_normal":

        if "normal" not in joined_users or len(joined_users["normal"]) == 0:

            await query.answer(
                "❌ لا يوجد مشاركين",
                show_alert=True
            )

            return

        winner = random.choice(joined_users["normal"])

        await query.message.reply_text(
            f"🏆 الفائز:\n[{winner}](tg://user?id={winner})",
            parse_mode="Markdown"
        )

    # تدوير أحكام
    elif query.data == "spin_rules":

        if "rules" not in joined_users or len(joined_users["rules"]) == 0:

            await query.answer(
                "❌ لا يوجد مشاركين",
                show_alert=True
            )

            return

        winner = random.choice(joined_users["rules"])

        punishments = [
            "😂 غني أغنية",
            "🔥 غير صورتك يوم كامل",
            "😅 ابعت ستيكر مضحك",
            "🎤 سجل فويس",
        ]

        rule = random.choice(punishments)

        await query.message.reply_text(
            f"🏆 الفائز:\n[{winner}](tg://user?id={winner})\n\n⚖️ الحكم:\n{rule}",
            parse_mode="Markdown"
        )

# ================= MAIN =================

def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(InlineQueryHandler(inline_query))

    print("Bot Started")

    app.run_polling()

if __name__ == "__main__":
    main()
