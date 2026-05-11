import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

players = []
max_players = 10
game_started = False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global players, game_started

    players = []
    game_started = False

    if context.args:
        try:
            num = int(context.args[0])
            if 10 <= num <= 50:
                global max_players
                max_players = num
        except:
            pass

    keyboard = [
        [InlineKeyboardButton("🎡 دخول", callback_data="join")],
        [InlineKeyboardButton("▶️ بدء", callback_data="spin")]
    ]

    await update.message.reply_text(
        f"🎯 عجلة الحذف بدأت!\n\nالعدد المطلوب: {max_players}\n\nاضغط دخول للمشاركة.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global players, game_started

    query = update.callback_query
    await query.answer()

    user = query.from_user

    if query.data == "join":
        if game_started:
            return

        if user.first_name not in players:
            players.append(user.first_name)

        await query.message.reply_text(
            f"✅ {user.first_name} دخل اللعبة\n👥 العدد الحالي: {len(players)}/{max_players}"
        )

    elif query.data == "spin":
        if game_started:
            return

        if len(players) < 2:
            await query.message.reply_text("❌ لازم لاعبين اكثر.")
            return

        game_started = True

        current = players.copy()

        while len(current) > 1:
            loser = random.choice(current)
            current.remove(loser)

            await query.message.reply_text(
                f"🎡 العجلة دارت...\n\n❌ خرج: {loser}\n👥 الباقين: {len(current)}"
            )

        await query.message.reply_text(
            f"🏆 الفائز النهائي: {current[0]}"
        )

app = ApplicationBuilder().token("8735268386:AAFwZAjHtxosdtVczb054Ckm5mI9PpRmGKE").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

print("Bot Running...")
app.run_polling()
