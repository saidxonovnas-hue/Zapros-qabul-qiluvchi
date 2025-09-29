import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ChatJoinRequestHandler

# Loglarni (xatoliklarni) ko'rsatib turish uchun sozlash
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Bot Token'ni Render'ning o'zidan olish
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    logging.error("BOT_TOKEN topilmadi! Uni Render'da Environment bo'limiga qo'shing.")
    exit()

# /start komandasi uchun funksiya
async def start(update: Update, context):
    await update.message.reply_html(
        "Salom! Men kanal yoki gruppaga yuborilgan a'zolik so'rovlarini avtomatik qabul qilaman.\n\n"
        "Meni kanalingizga qo'shish uchun /add buyrug'ini yuboring."
    )

# YANGI FUNKSIYA: /add komandasi uchun
async def add_to_chat(update: Update, context):
    bot_username = context.bot.username
    # Botga kerakli admin huquqini so'rash uchun maxsus havola
    admin_rights_url = f"https://t.me/{bot_username}?startgroup=true&admin=can_invite_users"
    
    text = (
        "Meni guruh yoki kanalingizga administrator qilish uchun quyidagi tugmani bosing.\n\n"
        "❗️ **DIQQAT:** Men a'zolik so'rovlarini muvaffaqiyatli qabul qila olishim uchun, "
        "menga administratorlik huquqini berayotganingizda **\"Invite Users via Link\"** "
        "(Foydalanuvchilarni havola orqali taklif qilish) huquqi yoqilganligiga ishonch hosil qiling."
    )
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Guruh/Kanalga qo'shish", url=admin_rights_url)]
    ])
    
    await update.message.reply_text(text, reply_markup=keyboard)


# Yangi a'zolik so'rovlarini qabul qiluvchi funksiya
async def approve_join_request(update: Update, context):
    try:
        await update.chat_join_request.approve()
        logging.info(f"Foydalanuvchi {update.chat_join_request.from_user.id} ning so'rovi qabul qilindi.")
    except Exception as e:
        logging.error(f"So'rovni qabul qilishda xatolik: {e}")

# Botni ishga tushiruvchi asosiy funksiya
def main():
    application = Application.builder().token(BOT_TOKEN).build()

    # Komanda va so'rovlarni qaysi funksiya bajarishini belgilash
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("add", add_to_chat))  # YAngi komanda qo'shildi
    application.add_handler(ChatJoinRequestHandler(callback=approve_join_request))

    logging.info("Bot ishga tushdi (Join Request rejimi)...")
    
    application.run_polling()

if __name__ == '__main__':
    main()
