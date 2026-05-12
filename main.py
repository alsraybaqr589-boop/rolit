import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8735268386:AAGzFCX4yKoTjdgSjbFId1xP4Rhc-BGJ9oo"

bot = telebot.TeleBot(TOKEN)

vip_data = {}

# ---------------- START ---------------- #

@bot.message_handler(commands=['start'])
def start(message):

    markup = InlineKeyboardMarkup(row_width=1)

    normal = InlineKeyboardButton(
        "🌐 روليت عادي",
        callback_data="normal"
    )

    ahkam = InlineKeyboardButton(
        "🪵 روليت أحكام",
        callback_data="ahkam"
    )

    vip = InlineKeyboardButton(
        "🌈 روليت مميز",
        callback_data="vip"
    )

    channel = InlineKeyboardButton(
        "📢 القناة",
        url="https://t.me/NQJNQ"
    )

    markup.add(normal)
    markup.add(ahkam)
    markup.add(vip)
    markup.add(channel)

PHOTO = "https://i.imgur.com/2uQZQ0K.jpeg"

bot.send_photo(
    message.chat.id,
    PHOTO,
    caption=text,
    reply_markup=markup
)
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

    start_btn = InlineKeyboardButton(
        "🎭 ابدأ الآن",
        switch_inline_query_chosen_chat={
            "query": "روليت عادي 🎭",
            "allow_user_chats": True,
            "allow_group_chats": True,
            "allow_channel_chats": True
        }
    )

    back_btn = InlineKeyboardButton(
        "🏠 رجوع",
        callback_data="back"
    )

    markup.add(start_btn)
    markup.add(back_btn)

    bot.send_message(
        call.message.chat.id,
        "🌐 تم اختيار الروليت العادي",
        reply_markup=markup
    )

# ---------------- روليت أحكام ---------------- #

@bot.callback_query_handler(func=lambda call: call.data == "ahkam")
def ahkam(call):

    markup = InlineKeyboardMarkup(row_width=1)

    start_btn = InlineKeyboardButton(
        "🪵 ابدأ الآن",
        switch_inline_query_chosen_chat={
            "query": "روليت أحكام 🪵",
            "allow_user_chats": True,
            "allow_group_chats": True,
            "allow_channel_chats": True
        }
    )

    back_btn = InlineKeyboardButton(
        "🏠 رجوع",
        callback_data="back"
    )

    markup.add(start_btn)
    markup.add(back_btn)

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
        "👥 ارسل عدد الأعضاء:"
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
        "📢 ارسل رابط القناة:"
    )

    bot.register_next_step_handler(msg, finish_vip)

def finish_vip(message):

    data = vip_data[message.chat.id]

    markup = InlineKeyboardMarkup(row_width=1)

    share_btn = InlineKeyboardButton(
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

    back_btn = InlineKeyboardButton(
        "🏠 رجوع",
        callback_data="back"
    )

    markup.add(share_btn)
    markup.add(back_btn)

    bot.send_message(
        message.chat.id,
        "✅ تم إنشاء الروليت المميز",
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
