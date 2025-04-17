import os
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from handlers.command_handlers import start, help
from handlers.message_handlers import handle_text

TOKEN = os.environ['TELEGRAM_BOT_TOKEN']  # سيؤدي لخطأ إذا لم يتم تعيينه
WEBHOOK_URL = os.environ['WEBHOOK_URL']
PORT = int(os.environ.get('PORT', 10000))

def main():
    # إنشاء التطبيق مع إعدادات إضافية
    app = Application.builder() \
        .token(TOKEN) \
        .post_init(post_init) \
        .build()
    
    # تسجيل ال handlers مع معالجة الأخطاء
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, 
        handle_text
    ))
    
    # التشغيل مع إعدادات Webhook
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=WEBHOOK_URL,
        drop_pending_updates=True,
        allowed_updates=Update.ALL_TYPES
    )

async def post_init(app):
    """وظيفة ما بعد التهيئة لضبط Webhook"""
    try:
        await app.bot.set_webhook(
            url=WEBHOOK_URL,
            allowed_updates=["message", "callback_query"]
        )
        print(f"✅ Webhook configured successfully at: {WEBHOOK_URL}")
    except Exception as e:
        print(f"❌ Failed to set webhook: {e}")

if __name__ == "__main__":
    main()
