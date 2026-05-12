import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random

TOKEN = "8735268386:AAFwZAjHtxosdtVczb054Ckm5mI9PpRmGKE"
bot = telebot.TeleBot(TOKEN)

vip_data = {}

# ---------------- START ---------------- #

@bot.message_handler(commands=['start'])
def start(message):

    markup = InlineKeyboardMarkup(row_width=1)

    btn1 = InlineKeyboardButton("🌐 روليت عادي", callback_data="normal")
    btn2 = InlineKeyboardButton("📜 روليت أحكام", callback_data="rules")
    btn3 = InlineKeyboardButton("🌈 روليت مميز", callback_data="vip")
    btn4 = InlineKeyboardButton("📢 القناه", url="https://t.me/USERNAME")

    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    markup.add(btn4)

    text = """
🎮 أهلاً بك في بوت الروليت

✨ الأقسام:
• روليت عادي
• روليت أحكام
• روليت VIP
"""

    with open("photo.jpg", "rb") as photo:
        bot.send_photo(
            message.chat.id,
            photo,
            caption=text,
            reply_markup=markup
        )

# ---------------- روليت عادي ---------------- #

@bot.callback_query_handler(func=lambda call: call.data == "normal")
def normal(call):

    markup = InlineKeyboardMarkup(row_width=1)

    start_btn = InlineKeyboardButton(
        "🎭 ابدأ الآن",
        switch_inline_query="روليت عادي"
    )

    back_btn = InlineKeyboardButton(
        "🏠 رجوع",
        callback_data="back"
    )

    channel_btn = InlineKeyboardButton(
        "📢 القناه",
        url="https://t.me/NQJNQ"
    )

    markup.add(start_btn)
    markup.add(back_btn)
    markup.add(channel_btn)

    bot.send_message(
        call.message.chat.id,
        "🌐 تم اختيار الروليت العادي\n\nاضغط على الزر أدناه لبدء اللعب:",
        reply_markup=markup
    )

# ---------------- روليت أحكام ---------------- #

@bot.callback_query_handler(func=lambda call: call.data == "rules")
def rules(call):

    markup = InlineKeyboardMarkup(row_width=1)

    start_btn = InlineKeyboardButton(
        "📜 ابدأ الآن",
        switch_inline_query="روليت احكام"
    )

    back_btn = InlineKeyboardButton(
        "🏠 رجوع",
        callback_data="back"
    )

    channel_btn = InlineKeyboardButton(
        "📢 القناه",
        url="https://t.me/NQJNQ"
    )

    markup.add(start_btn)
    markup.add(back_btn)
    markup.add(channel_btn)

    bot.send_message(
        call.message.chat.id,
        "📜 تم اختيار روليت الأحكام\n\nاضغط على الزر أدناه:",
        reply_markup=markup
    )

# ---------------- روليت VIP ---------------- #

@bot.callback_query_handler(func=lambda call: call.data == "vip")
def vip(call):

    msg = bot.send_message(
        call.message.chat.id,
        "📝 ارسل عنوان الروليت:"
    )

    bot.register_next_step_handler(msg, vip_title)

def vip_title(message):

    vip_data[message.chat.id] = {}
    vip_data[message.chat.id]["title"] = message.text

    msg = bot.send_message(
        message.chat.id,
        "👥 ارسل عدد الاعضاء:"
    )

    bot.register_next_step_handler(msg, vip_members)

def vip_members(message):

    vip_data[message.chat.id]["members"] = message.text

    msg = bot.send_message(
        message.chat.id,
        "🏆 ارسل عدد الفائزين:"
    )

    bot.register_next_step_handler(msg, vip_winners)

def vip_winners(message):

    vip_data[message.chat.id]["winners"] = message.text

    msg = bot.send_message(
        message.chat.id,
        "📢 ارسل معرف القناة بدون @\n\nوتأكد رافع البوت ادمن"
    )

    bot.register_next_step_handler(msg, vip_channel)

def vip_channel(message):

    vip_data[message.chat.id]["channel"] = message.text

    data = vip_data[message.chat.id]

    markup = InlineKeyboardMarkup(row_width=1)

    share_btn = InlineKeyboardButton(
        "🎉 مشاركة",
        switch_inline_query=data["title"]
    )

    channel_btn = InlineKeyboardButton(
        "📢 القناه",
        url=f"https://t.me/NQJNQ{data['channel']}"
    )

    markup.add(share_btn)
    markup.add(channel_btn)

    text = f"""
🌈 روليت مميز

📝 العنوان:
{data['title']}

👥 العدد:
{data['members']}

🏆 الفائزين:
{data['winners']}
"""

    bot.send_message(
        message.chat.id,
        text,
        reply_markup=markup
    )

# ---------------- رجوع ---------------- #

@bot.callback_query_handler(func=lambda call: call.data == "back")
def back(call):
    start(call.message)

# ---------------- تشغيل ---------------- #

printprint("BOT IS RUNNING...")

while True:
    try:
        bot.infinity_polling(skip_pending=True)
    except Exception as e:
        print(e)
