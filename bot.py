from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN = "8735268386:AAFwZAjHtxosdtVczb054Ckm5mI9PpRmGKE"

games = {}

# بدء البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("🎯 إنشاء روليت", callback_data="create")]
    ]

    await update.message.reply_text(
        "اهلا بك في بوت الروليت 🎰",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# اختيار العدد
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "create":

        keyboard = [
            [
                InlineKeyboardButton("10", callback_data="players_10"),
                InlineKeyboardButton("25", callback_data="players_25"),
                InlineKeyboardButton("50", callback_data="players_50"),
            ]
        ]

        await query.message.reply_text(
            "اختر عدد اللاعبين:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data.startswith("players_"):

        count = int(query.data.split("_")[1])

        game_id = str(query.message.message_id)

        games[game_id] = {
            "count": count,
            "players": []
        }

        keyboard = [
            [InlineKeyboardButton("✅ مشاركة", switch_inline_query_choose_chat="roulette")],
            [InlineKeyboardButton("🎮 دخول", callback_data=f"join_{game_id}")],
            [InlineKeyboardButton("🎡 تدوير العجلة", callback_data=f"spin_{game_id}")]
        ]

        text = f"""
🎯 روليت جديد

👥 المشاركين: 0 / {count}

اضغط دخول للمشاركة
"""

        await query.message.reply_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data.startswith("join_"):

        game_id = query.data.split("_")[1]

        user = query.from_user.first_name

        if user not in games[game_id]["players"]:
            games[game_id]["players"].append(user)

        players = games[game_id]["players"]
        count = games[game_id]["count"]

        keyboard = [
            [InlineKeyboardButton("🎮 مشاركة", switch_inline_query_choose_chat="roulette")],
            [InlineKeyboardButton(f"✅ مشاركة ({len(players)})", callback_data=f"join_{game_id}")],
            [InlineKeyboardButton("🎡 تدوير العجلة", callback_data=f"spin_{game_id}")]
        ]

        text = f"""
🎯 روليت جديد

👥 المشاركين: {len(players)} / {count}

اللاعبين:
{', '.join(players)}
"""

        await query.message.edit_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data.startswith("spin_"):

        import random

        game_id = query.data.split("_")[1]

        players = games[game_id]["players"]

        if len(players) < 2:
            await query.answer("لازم لاعبين اكثر", show_alert=True)
            return

        winner = random.choice(players)

        await query.message.reply_text(
            f"🏆 الفائز هو:\n\n{winner}"
        )

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))

print("Bot Running...")
app.run_polling()
