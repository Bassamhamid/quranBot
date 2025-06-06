import os
import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from handlers.command_handlers import start, help, search, ayah, tafsir
from handlers.message_handlers import handle_text

# تكوين التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
WEBHOOK_URL = os.environ['WEBHOOK_URL']
PORT = int(os.environ.get('PORT', 10000))

async def post_init(app):
    """تهيئة الويب هوك"""
    try:
        await app.bot.set_webhook(
            url=WEBHOOK_URL,
            drop_pending_updates=True,
            allowed_updates=["message"]
        )
        logger.info(f"✅ تم تعيين الويب هوك: {WEBHOOK_URL}")
    except Exception as e:
        logger.error(f"❌ فشل تعيين الويب هوك: {e}")
        raise

def main():
    app = Application.builder().token(TOKEN).post_init(post_init).build()
    
    # تسجيل معالجات الأوامر
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("search", search))
    app.add_handler(CommandHandler("ayah", ayah))
    app.add_handler(CommandHandler("tafsir", tafsir))
    
    # معالجة الرسائل العادية
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    # تشغيل البوت
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=WEBHOOK_URL,
        drop_pending_updates=True
    )

if __name__ == "__main__":
    main()
