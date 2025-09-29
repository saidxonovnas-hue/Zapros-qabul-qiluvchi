import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import yt_dlp

# Loglarni (xatoliklarni) ko'rsatib turish uchun sozlash
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Bot Token'ni Render'ning o'zidan olish
# Bu xavfsiz usul, tokenni kod ichida yozib qoldirmang!
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    logging.error("BOT_TOKEN topilmadi! Uni Render'da Environment bo'limiga qo'shing.")
    exit()

# /start komandasi uchun funksiya
async def start(update: Update, context):
    await update.message.reply_html(
        f"Salom, {update.effective_user.first_name}!\n\n"
        "Menga Instagram, YouTube, Pinterest yoki boshqa saytlardan video yoki rasm havolasini (linkini) yuboring, men uni sizga yuklab beraman."
    )

# Havola yuborilganda ishlaydigan asosiy funksiya
async def download_media(update: Update, context):
    url = update.message.text
    
    # Foydalanuvchiga kutish haqida xabar berish
    message_to_edit = await update.message.reply_text("⏳ Havola qabul qilindi. Yuklanmoqda, iltimos kuting...")

    try:
        # yt-dlp sozlamalari
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best', # Eng yaxshi formatni tanlash
            'outtmpl': '%(id)s.%(ext)s',  # Faylni ID raqami bilan saqlash
            'noplaylist': True, # Playlist yuklamaslik
            'quiet': True, # Konsolga kamroq ma'lumot chiqarish
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)

            # Yuklangan faylni yuborish
            if os.path.exists(file_path):
                # Fayl turini aniqlash (video yoki rasm)
                if info.get('ext') in ['mp4', 'mkv', 'webm', 'mov']:
                    await update.message.reply_video(video=open(file_path, 'rb'), caption="✅ Marhamat, videongiz!")
                else:
                    await update.message.reply_photo(photo=open(file_path, 'rb'), caption="✅ Marhamat, rasmingiz!")
                
                # Yuborilgandan keyin faylni o'chirish (serverda joy to'lib qolmasligi uchun)
                os.remove(file_path)
            else:
                await message_to_edit.edit_text("❌ Xatolik: Faylni yuklab bo'lmadi.")

    except Exception as e:
        logging.error(f"Xatolik: {e}")
        await message_to_edit.edit_text("❌ Kechirasiz, bu havolani qayta ishlab bo'lmadi. Iltimos, boshqa havolani tekshirib yuboring.")

# Botni ishga tushiruvchi asosiy funksiya
def main():
    application = Application.builder().token(BOT_TOKEN).build()

    # Komanda va xabarlarni qaysi funksiya bajarishini belgilash
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_media))
    
    logging.info("Bot ishga tushdi...")
    
    # Botni doimiy ishlab turadigan qilish
    application.run_polling()

if __name__ == '__main__':
    main()
