import telebot
from telebot.types import *
import random

TOKEN = "8735268386:AAFwZAjHtxosdtVczb054Ckm5mI9PpRmGKE"

bot = telebot.TeleBot(TOKEN)

vip_data = {}

PHOTO = "https://i.imgur.com/2uQZQ0K.jpeg"

# ---------------- START ---------------- #

@bot.message_handler(commands=['start'])
def start(message):

    markup = InlineKeyboardMarkup(row_width=1)

    normal = InlineKeyboardButton(
        "🌐 روليت عادي",
        callback_data="normal"
    )

    rules = InlineKeyboardButton(
        "🪵 روليت أحكام",
        callback_data="rules"
    )

    vip = InlineKeyboardButton(
        "🌈 روليت مميز",
        callback_data="vip"
    )

    channel = InlineKeyboardButton(
        "📢 القناة",
        url="https://t.me/NQJNQ"
    )

    markup.add(normal, rules, vip, channel)

    bot.send_photo(
        message.chat.id,
        PHOTO,
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

    share = InlineKeyboardButton(
        "📢 مشاركة",
        switch_inline_query_chosen_chat={
            "query": "روليت عادي 🎭",
            "allow_user_chats": True,
            "allow_group_chats": True,
            "allow_channel_chats": True
        }
    )

    back = InlineKeyboardButton(
        "🏠 خروج",
        callback_data="back"
    )

    markup.add(share, back)

    bot.send_message(
        call.message.chat.id,
        "🌐 تم اختيار الروليت العادي",
        reply_markup=markup
    )

# ---------------- روليت أحكام ---------------- #

@bot.callback_query_handler(func=lambda call: call.data == "rules")
def rules(call):

    markup = InlineKeyboardMarkup(row_width=1)

    share = InlineKeyboardButton(
        "📢 مشاركة",
        switch_inline_query_chosen_chat={
            "query": "روليت أحكام 🪵",
            "allow_user_chats": True,
            "allow_group_chats": True,
            "allow_channel_chats": True
        }
    )

    back = InlineKeyboardButton(
        "🏠 خروج",
        callback_data="back"
    )

    markup.add(share, back)

    bot.send_message(
        call.message.chat.id,
        "🪵 تم اختيار روليت الأحكام",
        reply_markup=markup
    )

# ---------------- روليت مميز ---------------- #

@bot.callback_query_handler(func=lambda call: call.data == "vip")
def vip(call):

    msg = bot.send_message(
        call.message.chat.id,
        "📝 ارسل عنوان الروليت:"
    )

    bot.register_next_step_handler(msg, get_title)

def get_title(message):

    vip_data[message.chat.id] = {}
    vip_data[message.chat.id]["title"] = message.text

    msg = bot.send_message(
        message.chat.id,
        "👥 ارسل عدد المشاركين:"
    )

    bot.register_next_step_handler(msg, get_members)

def get_members(message):

    vip_data[message.chat.id]["members"] = message.text

    msg = bot.send_message(
        message.chat.id,
        "🏆 ارسل عدد الفائزين:"
    )

    bot.register_next_step_handler(msg, get_winners)

def get_winners(message):

    vip_data[message.chat.id]["winners"] = message.text

    msg = bot.send_message(
        message.chat.id,
        "📢 ارسل رابط قناتك:"
    )

    bot.register_next_step_handler(msg, finish_vip)

def finish_vip(message):

    data = vip_data[message.chat.id]

    markup = InlineKeyboardMarkup(row_width=1)

    share = InlineKeyboardButton(
        "📢 مشاركة",
        switch_inline_query_chosen_chat={
            "query": f"""🌈 روليت مميز

📝 {data['title']}
👥 {data['members']}
🏆 {data['winners']}

📢 {message.text}
""",
            "allow_user_chats": True,
            "allow_group_chats": True,
            "allow_channel_chats": True
        }
    )

    markup.add(share)

    bot.send_message(
        message.chat.id,
        f"""
🌈 تم إنشاء الروليت المميز

📝 العنوان:
{data['title']}

👥 العدد:
{data['members']}

🏆 الفائزين:
{data['winners']}
""",
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
        print(e)
