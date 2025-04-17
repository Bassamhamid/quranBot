import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
WEBHOOK_URL = os.environ['WEBHOOK_URL']
PORT = int(os.environ.get('PORT', 10000))

# استيراد الدوال من الملفات الأخرى
from handlers.command_handlers import start, help
from services.quran_service import search_in_quran

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        results = await search_in_quran(update.message.text)
        await update.message.reply_text(results[:4000])
    except Exception as e:
        await update.message.reply_text(f"حدث خطأ: {str(e)}")

async def post_init(app):
    await app.bot.set_webhook(WEBHOOK_URL)
    print(f"✅ Webhook configured: {WEBHOOK_URL}")

def main():
    app = Application.builder().token(TOKEN).post_init(post_init).build()
    
    # تسجيل ال handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    # التشغيل
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=WEBHOOK_URL,
        drop_pending_updates=True
    )

if __name__ == "__main__":
    main()
