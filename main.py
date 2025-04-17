import os
import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from handlers.command_handlers import (
    start,
    help_command,
    search_command,
    ayah_command,  # تمت الإضافة
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

async def post_init(app):
    """وظيفة تهيئة الويب هوك"""
    try:
        await app.bot.set_webhook(
            url=WEBHOOK_URL,
            drop_pending_updates=True,
            allowed_updates=["message", "callback_query"]
        )
        logger.info(f"✅ تم تعيين الويب هوك بنجاح على: {WEBHOOK_URL}")
    except Exception as e:
        logger.error(f"❌ فشل تعيين الويب هوك: {e}")

def main():
    # إنشاء تطبيق البوت
    app = Application.builder() \
        .token(TOKEN) \
        .post_init(post_init) \
        .build()

    # تسجيل معالجات الأوامر
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("search", search_command))
    app.add_handler(CommandHandler("ayah", ayah_command))  # تمت الإضافة
    app.add_handler(CommandHandler("tafsir", tafsir_command))

    # معالجة الرسائل العادية
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        handle_text
    ))

    # تشغيل البوت
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=WEBHOOK_URL,
        drop_pending_updates=True
    )

if __name__ == "__main__":
    main()
