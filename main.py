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
    btn2 = InlineKeyboardButton("🪵 روليت أحكام", callback_data="rules")
    btn3 = InlineKeyboardButton("🌈 روليت مميز", callback_data="vip")
    btn4 = InlineKeyboardButton("📢 القناة", url="https://t.me/NQJNQ")

    markup.add(btn1, btn2, btn3, btn4)

    bot.send_photo(
        message.chat.id,
        "https://i.imgur.com/2uQZQ0K.jpeg",
        caption="""
🎮 أهلاً بك في بوت الروليت

✨ الأقسام:
• روليت عادي
• روليت أحكام
• روليت مميز
""",
        reply_markup=markup
    )

# ---------------- روليت عادي ---------------- #

@bot.callback_query_handler(func=lambda call: call.data == "normal")
def normal(call):

    markup = InlineKeyboardMarkup(row_width=1)

    start_btn = InlineKeyboardButton("🎭 ابدأ الآن", switch_inline_query="روليت عادي")
    ch_btn = InlineKeyboardButton("📢 القناة", url="https://t.me/NQJNQ")
    back_btn = InlineKeyboardButton("🏠 خروج", callback_data="back")

    markup.add(start_btn, ch_btn, back_btn)

    bot.send_message(
        call.message.chat.id,
        "🌐 تم اختيار الروليت العادي\n\nاضغط على الزر أدناه:",
        reply_markup=markup
    )

# ---------------- روليت أحكام ---------------- #

@bot.callback_query_handler(func=lambda call: call.data == "rules")
def rules(call):

    markup = InlineKeyboardMarkup(row_width=1)

    start_btn = InlineKeyboardButton("🎭 ابدأ الآن", switch_inline_query="روليت أحكام")
    ch_btn = InlineKeyboardButton("📢 القناة", url="https://t.me/NQJNQ")
    back_btn = InlineKeyboardButton("🏠 خروج", callback_data="back")

    markup.add(start_btn, ch_btn, back_btn)

    bot.send_message(
        call.message.chat.id,
        "🪵 تم اختيار روليت الأحكام\n\nاضغط على الزر أدناه:",
        reply_markup=markup
    )

# ---------------- روليت مميز ---------------- #

@bot.callback_query_handler(func=lambda call: call.data == "vip")
def vip(call):

    msg = bot.send_message(call.message.chat.id, "📝 ارسل عنوان الروليت:")
    bot.register_next_step_handler(msg, get_title)

def get_title(message):

    vip_data[message.chat.id] = {}
    vip_data[message.chat.id]['title'] = message.text

    msg = bot.send_message(message.chat.id, "👥 ارسل عدد المشاركين:")
    bot.register_next_step_handler(msg, get_members)

def get_members(message):

    vip_data[message.chat.id]['members'] = message.text

    msg = bot.send_message(message.chat.id, "🏆 ارسل عدد الفائزين:")
    bot.register_next_step_handler(msg, get_winners)

def get_winners(message):

    vip_data[message.chat.id]['winners'] = message.text

    msg = bot.send_message(
        message.chat.id,
        "📢 ارسل رابط قناتك وارفع البوت ادمن"
    )

    bot.register_next_step_handler(msg, send_vip)

def send_vip(message):

    data = vip_data[message.chat.id]

    markup = InlineKeyboardMarkup(row_width=1)

    join_btn = InlineKeyboardButton(
        "🎉 مشاركة",
        url=message.text
    )

    markup.add(join_btn)

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

print("BOT IS RUNNING...")

while True:
    try:
        bot.infinity_polling(skip_pending=True)
    except Exception as e:
        print("ERROR:", e)
