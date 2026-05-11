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
    InlineQueryHandler,
    ContextTypes,
)
from uuid import uuid4
import random

TOKEN = "8735268386:AAFwZAjHtxosdtVczb054Ckm5mI9PpRmGKE"

games = {}

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎯 البوت شغال")

# inline mode
async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):

    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="🎯 إنشاء روليت",
            description="اضغط لإنشاء روليت بالقناة",
            input_message_content=InputTextMessageContent(
                "🎯 روليت جديد\n\n👥 المشاركين: 0"
            ),
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "✅ دخول",
                        callback_data="join"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🎡 تدوير",
                        callback_data="spin"
                    )
                ]
            ])
        )
    ]

    await update.inline_query.answer(results, cache_time=0)

players = []

# الأزرار
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    global players

    if query.data == "join":

        user = query.from_user.first_name

        if user not in players:
            players.append(user)

        text = f"🎯 روليت جديد\n\n👥 المشاركين: {len(players)}\n\n"

        for p in players:
            text += f"• {p}\n"

        keyboard = [
            [
                InlineKeyboardButton(
                    f"✅ دخول ({len(players)})",
                    callback_data="join"
                )
            ],
            [
                InlineKeyboardButton(
                    "🎡 تدوير",
                    callback_data="spin"
                )
            ]
        ]

        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "spin":

        if len(players) < 2:
            await query.answer("❌ لازم لاعبين أكثر", show_alert=True)
            return

        winner = random.choice(players)

        await query.edit_message_text(
            f"🏆 الفائز هو:\n\n{winner}"
        )

        players = []

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(InlineQueryHandler(inline_query))
app.add_handler(CallbackQueryHandler(buttons))

print("Running...")
app.run_polling()
