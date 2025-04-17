import os
import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from handlers.command_handlers import (
    start, help_command,
    search_command, ayah_command,
    tafsir_command
)
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

def main():
    app = Application.builder().token(TOKEN).build()
    
    # تسجيل معالجات الأوامر
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("search", search_command))
    app.add_handler(CommandHandler("ayah", ayah_command))
    app.add_handler(CommandHandler("tafsir", tafsir_command))
    
    # معالجة الرسائل العادية (بحث تلقائي)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    # إعداد Webhook
    async def post_init(app):
        await app.bot.set_webhook(
            url=WEBHOOK_URL,
            drop_pending_updates=True
        )
        logger.info(f"✅ تم تهيئة الويب هوك بنجاح: {WEBHOOK_URL}")
    
    app.post_init = post_init
    
    # تشغيل البوت
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=WEBHOOK_URL,
    )

if __name__ == "__main__":
    main()
