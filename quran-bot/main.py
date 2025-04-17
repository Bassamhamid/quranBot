import os
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from handlers.command_handlers import start, help
from handlers.message_handlers import handle_text

TOKEN = os.environ['TELEGRAM_BOT_TOKEN']  # سيؤدي لخطأ إذا لم يتم تعيينه
WEBHOOK_URL = os.environ['WEBHOOK_URL']
PORT = int(os.environ.get('PORT', 10000))

def main():
    app = Application.builder().token(TOKEN).build()
    
    # تسجيل ال handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    # Webhook setup
    async def post_init(app):
        await app.bot.set_webhook(f"{WEBHOOK_URL}")
        print(f"✅ Webhook configured: {WEBHOOK_URL}")
    
    app.post_init = post_init
    
    # التشغيل
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=WEBHOOK_URL,
        drop_pending_updates=True
    )

if __name__ == "__main__":
    main()
