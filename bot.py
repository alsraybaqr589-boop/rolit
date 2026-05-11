from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InputTextMessageContent,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    InlineQueryHandler,
    ContextTypes,
)
from uuid import uuid4
import random

games = {}

# لما الشخص يكتب /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎯 البوت شغال!")

# إنشاء منشور الروليت بالقنوات
async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    game_id = str(uuid4())

    games[game_id] = {
        "players": [],
        "max_players": 10
    }

    keyboard = [
        [InlineKeyboardButton("🎮 مشاركة (0)", callback_data=f"join_{game_id}")],
        [InlineKeyboardButton("🎡 تدوير العجلة", callback_data=f"spin_{game_id}")]
    ]

    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="🎯 إنشاء روليت",
            input_message_content=InputTextMessageContent(
                f"🎯 روليت عادي\n\n👥 المشاركين: 0 من أصل 10\n🏆 لم يتم اختيار الفائز بعد"
            ),
            reply_markup=InlineKeyboardMarkup(keyboard),
            description="اضغط لإنشاء لعبة روليت"
        )
    ]

    await update.inline_query.answer(results, cache_time=0)

# دخول لاعب
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data.startswith("join_"):
        game_id = data.split("_")[1]

        user = query.from_user.first_name

        if user not in games[game_id]["players"]:
            games[game_id]["players"].append(user)

        count = len(games[game_id]["players"])

        keyboard = [
            [InlineKeyboardButton(f"🎮 مشاركة ({count})", callback_data=f"join_{game_id}")],
            [InlineKeyboardButton("🎡 تدوير العجلة", callback_data=f"spin_{game_id}")]
        ]

        await query.edit_message_text(
            f"🎯 روليت عادي\n\n👥 المشاركين: {count} من أصل 10\n🏆 لم يتم اختيار الفائز بعد",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data.startswith("spin_"):
        game_id = data.split("_")[1]

        players = games[game_id]["players"]

        if len(players) < 2:
            await query.answer("❌ لازم لاعبين أكثر", show_alert=True)
            return

        winner = random.choice(players)

        keyboard = [
            [InlineKeyboardButton(f"🎮 مشاركة ({len(players)})", callback_data=f"join_{game_id}")]
        ]

        await query.edit_message_text(
            f"🏆 الفائز هو: {winner}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

app = ApplicationBuilder().token("8735268386:AAFwZAjHtxosdtVczb054Ckm5mI9PpRmGKE").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(InlineQueryHandler(inline_query))
app.add_handler(CallbackQueryHandler(button))

print("Bot is running...")
app.run_polling()
