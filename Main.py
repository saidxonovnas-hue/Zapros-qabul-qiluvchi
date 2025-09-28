9import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Telegram bot tokenini muhit o'zgaruvchisidan (Environment Variable) olish
TOKEN = os.getenv("BOT_TOKEN")

# /start komandasi uchun funksiya
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Assalomu alaykum! Menga biror xabar yuboring, men uni qaytaraman.')

# Har qanday matnli xabarga javob beradigan funksiya (echo)
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(update.message.text)

def main() -> None:
    # Aplikatsiyani yaratish
    application = Application.builder().token(TOKEN).build()

    # Komandalarni ro'yxatdan o'tkazish
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Botni ishga tushirish
    print("Bot ishga tushdi...")
    application.run_polling()

if __name__ == '__main__':
    main()
  
