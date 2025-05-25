from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    CallbackQueryHandler,
    filters
)
import logging

# --- تنظیمات ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = "7703859575:AAEVEwgvR75zLyqvGjhZLe3NnZYQ4rV0VvY"
CHANNEL_USERNAME = "arideveloper"  # بدون @
CHANNEL_LINK = "https://t.me/arideveloper"
CHANNEL_ID = -1002425950691  # آیدی عددی کانال

# --- دیکشنری تبدیل خطوط ---
# دیکشنری های نگاشت برای خطوط مختلف

## خط میخی فارسی باستان (Old Persian Cuneiform)
CUNEIFORM_MAP = {
    'a': '𐎠', 'b': '𐎲', 'c': '𐎨', 'd': '𐎭', 'e': '𐎡',
    'f': '𐎳', 'g': '𐎥', 'h': '𐏃', 'i': '𐎡', 'j': '𐎪',
    'k': '𐎤', 'l': '𐎾', 'm': '𐎶', 'n': '𐎴', 'o': '𐎤',
    'p': '𐎱', 'q': '𐎤', 'r': '𐎼', 's': '𐎿', 't': '𐎫',
    'u': '𐎢', 'v': '𐎠', 'w': '𐎠', 'x': '𐎤𐎿', 'y': '𐎹',
    'z': '𐏀',
    'ا': '𐎠', 'آ': '𐎠', 'ب': '𐎲', 'پ': '𐎱', 'ت': '𐎫', 'ث': '𐎰',
    'ج': '𐎪', 'چ': '𐎨', 'ح': '𐏃', 'خ': '𐏃', 'د': '𐎭',
    'ذ': '𐏀', 'ر': '𐎼', 'ز': '𐏀', 'ژ': '𐏀', 'س': '𐎿',
    'ش': '𐏁', 'ص': '𐎿', 'ض': '𐏀', 'ط': '𐎫', 'ظ': '𐏀',
    'ع': '𐎠', 'غ': '𐏃', 'ف': '𐎳', 'ق': '𐎤', 'ک': '𐎤',
    'گ': '𐎥', 'ل': '𐎾', 'م': '𐎶', 'ن': '𐎴', 'و': '𐎢',
    'ه': '𐏃', 'ی': '𐎹',
    ' ': ' ', '\n': '\n'
}

## خط اوستایی (Avestan)
AVESTAN_MAP = {
    'a': '𐬀', 'b': '𐬠', 'c': '𐬗', 'd': '𐬛', 'e': '𐬈',
    'f': '𐬟', 'g': '𐬔', 'h': '𐬵', 'i': '𐬌', 'j': '𐬘',
    'k': '𐬐', 'l': '𐬮', 'm': '𐬨', 'n': '𐬥', 'o': '𐬊',
    'p': '𐬞', 'q': '𐬑', 'r': '𐬭', 's': '𐬯', 't': '𐬙',
    'u': '𐬎', 'v': '𐬬', 'w': '𐬡', 'x': '𐬑𐭀', 'y': '𐬫',
    'z': '𐬰',
    'ا': '𐬀', 'آ': '𐬀', 'ب': '𐬠', 'پ': '𐬞', 'ت': '𐬙', 'ث': '𐬚',
    'ج': '𐬘', 'چ': '𐬗', 'ح': '𐬵', 'خ': '𐬑', 'د': '𐬛',
    'ذ': '𐬜', 'ر': '𐬭', 'ز': '𐬰', 'ژ': '𐬲', 'س': '𐬯',
    'ش': '𐬱', 'ص': '𐬯', 'ض': '𐬰', 'ط': '𐬙', 'ظ': '𐬰',
    'ع': '𐬀', 'غ': '𐬑', 'ف': '𐬟', 'ق': '𐬑', 'ک': '𐬐',
    'گ': '𐬔', 'ل': '𐬮', 'م': '𐬨', 'ن': '𐬥', 'و': '𐬡',
    'ه': '𐬵', 'ی': '𐬫',
    ' ': ' ', '\n': '\n'
}

## خط پهلوی کتابی (Inscriptional Pahlavi)
PAHLAVI_MAP = {
    'a': '𐭠', 'b': '𐭡', 'c': '𐭢', 'd': '𐭣', 'e': '𐭠',
    'f': '𐭯', 'g': '𐭢', 'h': '𐭤', 'i': '𐭩', 'j': '𐭦',
    'k': '𐭪', 'l': '𐭫', 'm': '𐭬', 'n': '𐭭', 'o': '𐭥',
    'p': '𐭯', 'q': '𐭪', 'r': '𐭧', 's': '𐭮', 't': '𐭲',
    'u': '𐭥', 'v': '𐭥', 'w': '𐭥', 'x': '𐭪𐭮', 'y': '𐭩',
    'z': '𐭦',
    'ا': '𐭠', 'آ': '𐭠', 'ب': '𐭡', 'پ': '𐭯', 'ت': '𐭲', 'ث': '𐭮',
    'ج': '𐭢', 'چ': '𐭰', 'ح': '𐭤', 'خ': '𐭧', 'د': '𐭣',
    'ذ': '𐭦', 'ر': '𐭧', 'ز': '𐭦', 'ژ': '𐭰', 'س': '𐭮',
    'ش': '𐭱', 'ص': '𐭮', 'ض': '𐭦', 'ط': '𐭲', 'ظ': '𐭦',
    'ع': '𐭠', 'غ': '𐭢', 'ف': '𐭯', 'ق': '𐭪', 'ک': '𐭪',
    'گ': '𐭢', 'ل': '𐭫', 'م': '𐭬', 'ن': '𐭭', 'و': '𐭥',
    'ه': '𐭤', 'ی': '𐭩',
    ' ': ' ', '\n': '\n'
}


# --- توابع کمکی ---
def convert_text(text: str, mapping: dict) -> str:
    return ''.join([mapping.get(char, char) for char in text])


async def is_member(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        logger.error(f"خطا در بررسی عضویت: {e}")
        return False


# --- هندلرها ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    user_id = update.message.from_user.id
    if await is_member(user_id, context):
        await show_main_menu(update.message)
    else:
        await ask_to_join(update.message)


async def ask_to_join(message):
    keyboard = [
        [InlineKeyboardButton("عضویت در کانال", url=CHANNEL_LINK)],
        [InlineKeyboardButton("✅ عضو شدم", callback_data='check_membership')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await message.reply_text(
        "⚠️ برای استفاده از ربات باید در کانال ما عضو باشید:",
        reply_markup=reply_markup
    )


async def check_membership(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if await is_member(query.from_user.id, context):
        await query.edit_message_text("✅ عضویت شما تایید شد!")
        await show_main_menu(query.message)
    else:
        await query.answer("❌ هنوز در کانال عضو نشده‌اید!", show_alert=True)


async def show_main_menu(message):
    menu = (
        "🔮 ربات تبدیل متن به خطوط باستانی\n\n"
        "🔸 /cuneiform - خط میخی\n"
        "🔸 /avestan - خط اوستایی\n"
        "🔸 /pahlavi - خط پهلوی\n\n"
        "متن خود را بعد از انتخاب دستور ارسال کنید."
    )
    await message.reply_text(menu)


async def set_conversion_type(update: Update, context: ContextTypes.DEFAULT_TYPE, script_type: str):
    if not update.message:
        return

    user_id = update.message.from_user.id
    if not await is_member(user_id, context):
        await ask_to_join(update.message)
        return

    script_names = {
        'cuneiform': 'میخی',
        'avestan': 'اوستایی',
        'pahlavi': 'پهلوی'
    }

    context.user_data['script'] = script_type
    await update.message.reply_text(
        f"📝 لطفاً متن را برای تبدیل به خط {script_names[script_type]} ارسال کنید:"
    )


async def convert_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    user_id = update.message.from_user.id
    if not await is_member(user_id, context):
        await ask_to_join(update.message)
        return

    script_type = context.user_data.get('script')
    if not script_type:
        await update.message.reply_text("⚠️ لطفاً ابتدا نوع خط را انتخاب کنید.")
        return

    mappings = {
        'cuneiform': CUNEIFORM_MAP,
        'avestan': AVESTAN_MAP,
        'pahlavi': PAHLAVI_MAP
    }
    script_names = {
        'cuneiform': 'میخی',
        'avestan': 'اوستایی',
        'pahlavi': 'پهلوی'
    }

    converted = convert_text(update.message.text, mappings[script_type])
    await update.message.reply_text(
        f"🔮 متن تبدیل شده به خط {script_names[script_type]}:\n\n{converted}"
    )


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("خطا:", exc_info=context.error)
    if update and isinstance(update, Update) and update.effective_message:
        await update.effective_message.reply_text("⚠️ خطایی در پردازش درخواست رخ داد.")


# --- تنظیمات ربات ---
def main():
    app = Application.builder().token(TOKEN).build()

    # دستورات
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("cuneiform", lambda u, c: set_conversion_type(u, c, 'cuneiform')))
    app.add_handler(CommandHandler("avestan", lambda u, c: set_conversion_type(u, c, 'avestan')))
    app.add_handler(CommandHandler("pahlavi", lambda u, c: set_conversion_type(u, c, 'pahlavi')))

    # پردازش پیام‌ها
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, convert_message))

    # پردازش اینلاین
    app.add_handler(CallbackQueryHandler(check_membership, pattern="^check_membership$"))

    # مدیریت خطاها
    app.add_error_handler(error_handler)

    # اجرای ربات
    app.run_polling()


if __name__ == "__main__":
    main()
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)