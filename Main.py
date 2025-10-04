// Kerakli kutubxonalarni import qilish
const { Telegraf, Markup } = require('telegraf');

// Loglarni (xatoliklarni) ko'rsatib turish uchun sozlash
console.log('Bot ishga tushirilmoqda...');

// Bot Token'ni Render'ning o\'zidan (yoki .env faylidan) olish
// Environment o\'zgaruvchisi nomi Python dagi kabi "BOT_TOKEN" bo\'lishi kerak.
const BOT_TOKEN = process.env.BOT_TOKEN;

if (!BOT_TOKEN) {
    console.error("BOT_TOKEN topilmadi! Uni Render'da Environment bo'limiga qo'shing.");
    process.exit(1);
}

// Telegraf botini ishga tushirish
const bot = new Telegraf(BOT_TOKEN);

// --- Komandalar va hodisalar uchun funksiyalar ---

// /start komandasi uchun funksiya
bot.start(async (ctx) => {
    // Telegraf Markup.html funksiyasi orqali HTML formatlashni qo\'llab-quvvatlash
    await ctx.replyWithHTML(
        "Salom! Men kanal yoki gruppaga yuborilgan a'zolik so'rovlarini avtomatik qabul qilaman.\n\n" +
        "Meni kanalingizga qo'shish uchun /add buyrug'ini yuboring."
    );
});

// /add komandasi uchun funksiya
bot.command('add', async (ctx) => {
    // Botning to\'g\'ri ismiga kirish
    const botUsername = ctx.botInfo.username;
    
    // Botga kerakli admin huquqini (can_invite_users) so\'rash uchun maxsus havola
    // 'can_invite_users' Telegram botining a\'zolik so\'rovlarini qabul qilish huquqini bildiradi.
    const adminRightsUrl = `https://t.me/${botUsername}?startgroup=true&admin=can_invite_users`;
    
    const text = (
        "Meni guruh yoki kanalingizga administrator qilish uchun quyidagi tugmani bosing.\n\n" +
        "❗️ <b>DIQQAT:</b> Men a'zolik so'rovlarini muvaffaqiyatli qabul qila olishim uchun, " +
        "menga administratorlik huquqini berayotganingizda <b>\"Invite Users via Link\"</b> " +
        "(Foydalanuvchilarni havola orqali taklif qilish) huquqi yoqilganligiga ishonch hosil qiling."
    );
    
    const keyboard = Markup.inlineKeyboard([
        Markup.button.url("➕ Guruh/Kanalga qo'shish", adminRightsUrl)
    ]);
    
    await ctx.replyWithHTML(text, keyboard);
});

// Yangi a\'zolik so\'rovlarini (chat_join_request) qabul qiluvchi funksiya
bot.on('chat_join_request', async (ctx) => {
    const userId = ctx.chatJoinRequest.from.id;
    const chatId = ctx.chatJoinRequest.chat.id;

    try {
        // So\'rovni avtomatik ravishda qabul qilish
        await ctx.approveChatJoinRequest(chatId, userId);
        console.log(`Foydalanuvchi ${userId} ning so'rovi qabul qilindi. Chat ID: ${chatId}`);
    } catch (e) {
        console.error(`So\'rovni qabul qilishda xatolik (User: ${userId}, Chat: ${chatId}):`, e);
    }
});

// Botni ishga tushirish
bot.launch()
    .then(() => {
        console.log("Bot muvaffaqiyatli ishga tushdi (Join Request rejimi)...");
    })
    .catch((err) => {
        console.error("Botni ishga tushirishda xatolik yuz berdi:", err);
    });

// Serverni to\'xtatish signallarini (SIGINT, SIGTERM) qayta ishlash
process.once('SIGINT', () => bot.stop('SIGINT'));
process.once('SIGTERM', () => bot.stop('SIGTERM'));
