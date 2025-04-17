import os
import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from handlers.command_handlers import (
    start,
    help,
    search,
    ayah,
    tafsir
)
from handlers.message_handlers import handle_text

# إعداد نظام التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# قراءة المتغيرات البيئية
TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
WEBHOOK_URL = os.environ['WEBHOOK_URL']
PORT = int(os.environ.get('PORT', 10000))

def main():
    # إنشاء التطبيق
    app = Application.builder() \
        .token(TOKEN) \
        .build()

    # تعيين معالجات الأوامر
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("search", search))
    app.add_handler(CommandHandler("ayah", ayah))
    app.add_handler(CommandHandler("tafsir", tafsir))

    # معالج للرسائل النصية العادية
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        handle_text
    ))

    # وظيفة تعيين الويب هوك عند بدء التشغيل
    async def set_webhook(app):
        try:
            await app.bot.set_webhook(
                url=WEBHOOK_URL,
                drop_pending_updates=True,
                allowed_updates=["message", "callback_query"]
            )
            logger.info(f"✅ تم تعيين الويب هوك بنجاح: {WEBHOOK_URL}")
        except Exception as e:
            logger.error(f"❌ فشل تعيين الويب هوك: {str(e)}")
            raise

    # تشغيل السيرفر مع تعيين الويب هوك
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=WEBHOOK_URL,
        drop_pending_updates=True,
        on_startup=set_webhook
    )

if __name__ == "__main__":
    main()
