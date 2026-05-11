from telegram import *
from telegram.ext import *
import random
import uuid

TOKEN = "8735268386:AAFwZAjHtxosdtVczb054Ckm5mI9PpRmGKE"
CHANNEL = "https://t.me/NQJNQ"

# تخزين الألعاب
roulette_games = {}
ahkam_games = {}
vip_games = {}

# تحقق اشتراك
async def check_sub(bot, user_id):
    try:
        member = await bot.get_chat_member(CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("🌐 روليت عادي", callback_data="normal")],
        [InlineKeyboardButton("📜 روليت أحكام", callback_data="ahkam")],
        [InlineKeyboardButton("👑 روليت مميز", callback_data="vip")],
        [InlineKeyboardButton("📢 قناتنا", url=f"https://t.me/{CHANNEL.replace('@','')}")]
    ]

    text = """
🎮 أهلاً بك في بوت الروليت

✨ المميزات:
• مشاركة بالقنوات
• اختيار عدد اللاعبين
• سحب تلقائي
• سحب يدوي
• اشتراك إجباري
• روليت أحكام
• روليت VIP
"""

    await update.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# الأزرار الرئيسية
async def menu_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "normal":

        keyboard = [
            [InlineKeyboardButton("5 لاعبين", switch_inline_query="roulette_5")],
            [InlineKeyboardButton("10 لاعبين", switch_inline_query="roulette_10")],
            [InlineKeyboardButton("20 لاعبين", switch_inline_query="roulette_20")],
        ]

        await query.message.reply_text(
            "🎯 اختر عدد اللاعبين",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data == "ahkam":

        keyboard = [
            [InlineKeyboardButton("📜 إنشاء أحكام", switch_inline_query="ahkam")]
        ]

        await query.message.reply_text(
            "📜 اضغط لإنشاء روليت أحكام",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data == "vip":

        keyboard = [
            [InlineKeyboardButton("👑 إنشاء VIP", switch_inline_query="vip")]
        ]

        await query.message.reply_text(
            "👑 روليت VIP",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

# الانلاين
async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.inline_query.query
    results = []

    # روليت عادي
    if query.startswith("roulette"):

        max_players = int(query.split("_")[1])

        game_id = str(uuid.uuid4())[:8]

        roulette_games[game_id] = {
            "players": [],
            "max": max_players,
            "ended": False
        }

        keyboard = [
            [InlineKeyboardButton("✅ مشاركة (0)", callback_data=f"join_{game_id}")],
            [InlineKeyboardButton("🎡 تدوير", callback_data=f"spin_{game_id}")]
        ]

        results.append(
            InlineQueryResultArticle(
                id=game_id,
                title=f"🎯 روليت {max_players} لاعب",
                description="اضغط للإرسال",
                input_message_content=InputTextMessageContent(
                    f"🎯 روليت جديد\n\n👥 العدد المطلوب: {max_players}"
                ),
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        )

    # أحكام
    elif query == "ahkam":

        game_id = str(uuid.uuid4())[:8]

        ahkam_games[game_id] = {
            "players": []
        }

        keyboard = [
            [InlineKeyboardButton("📜 دخول", callback_data=f"ahkamjoin_{game_id}")],
            [InlineKeyboardButton("🎲 اختيار", callback_data=f"ahkamspin_{game_id}")]
        ]

        results.append(
            InlineQueryResultArticle(
                id=game_id,
                title="📜 روليت أحكام",
                description="إنشاء لعبة أحكام",
                input_message_content=InputTextMessageContent(
                    "📜 روليت أحكام جديد"
                ),
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        )

    # VIP
    elif query == "vip":

        game_id = str(uuid.uuid4())[:8]

        vip_games[game_id] = {
            "players": []
        }

        keyboard = [
            [InlineKeyboardButton("👑 دخول VIP", callback_data=f"vipjoin_{game_id}")],
            [InlineKeyboardButton("🎡 سحب", callback_data=f"vipspin_{game_id}")]
        ]

        results.append(
            InlineQueryResultArticle(
                id=game_id,
                title="👑 روليت VIP",
                description="إنشاء VIP",
                input_message_content=InputTextMessageContent(
                    "👑 روليت VIP جديد"
                ),
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        )

    await update.inline_query.answer(results, cache_time=1)

# أزرار اللعب
async def game_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    data = query.data

    # روليت عادي
    if data.startswith("join_"):

        game_id = data.split("_")[1]
        game = roulette_games[game_id]

        if game["ended"]:
            return

        user = query.from_user.first_name

        subbed = await check_sub(context.bot, query.from_user.id)

        if not subbed:
            await query.answer("❌ اشترك بالقناة أولاً", show_alert=True)
            return

        if user not in game["players"]:
            game["players"].append(user)

        count = len(game["players"])

        keyboard = [
            [InlineKeyboardButton(f"✅ مشاركة ({count})", callback_data=f"join_{game_id}")],
            [InlineKeyboardButton("🎡 تدوير", callback_data=f"spin_{game_id}")]
        ]

        players_text = "\n".join([f"• {p}" for p in game["players"]])

        await query.edit_message_text(
            f"🎯 روليت جديد\n\n👥 {count}/{game['max']}\n\n{players_text}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data.startswith("spin_"):

        game_id = data.split("_")[1]
        game = roulette_games[game_id]

        if len(game["players"]) < 2:
            await query.answer("❌ لازم لاعبين أكثر", show_alert=True)
            return

        winner = random.choice(game["players"])

        game["ended"] = True

        keyboard = [
            [InlineKeyboardButton("🔄 إعادة اللعب", switch_inline_query="roulette_10")]
        ]

        await query.edit_message_text(
            f"🏆 الفائز هو:\n\n👑 {winner}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # أحكام
    elif data.startswith("ahkamjoin_"):

        game_id = data.split("_")[1]
        user = query.from_user.first_name

        if user not in ahkam_games[game_id]["players"]:
            ahkam_games[game_id]["players"].append(user)

        count = len(ahkam_games[game_id]["players"])

        keyboard = [
            [InlineKeyboardButton(f"📜 دخول ({count})", callback_data=f"ahkamjoin_{game_id}")],
            [InlineKeyboardButton("🎲 اختيار", callback_data=f"ahkamspin_{game_id}")]
        ]

        await query.edit_message_text(
            f"📜 روليت أحكام\n\n👥 المشاركين: {count}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data.startswith("ahkamspin_"):

        game_id = data.split("_")[1]
        players = ahkam_games[game_id]["players"]

        if len(players) < 2:
            await query.answer("❌ لازم لاعبين أكثر", show_alert=True)
            return

        winner = random.choice(players)
        loser = random.choice(players)

        while loser == winner:
            loser = random.choice(players)

        await query.edit_message_text(
            f"📜 الأحكام\n\n👑 الحاكم: {winner}\n😂 المحكوم: {loser}"
        )

# تشغيل
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(InlineQueryHandler(inline_query))
app.add_handler(CallbackQueryHandler(menu_buttons, pattern="^(normal|ahkam|vip)$"))
app.add_handler(CallbackQueryHandler(game_buttons))

print("البوت شغال ✅")

app.run_polling()
