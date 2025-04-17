import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from handlers.command_handlers import start, help
from handlers.message_handlers import handle_text

TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
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
        try:
            await app.bot.set_webhook(
                url=WEBHOOK_URL,
                allowed_updates=Update.ALL_TYPES
            )
            print(f"✅ Webhook configured: {WEBHOOK_URL}")
        except Exception as e:
            print(f"❌ Webhook error: {e}")
    
    app.post_init = post_init
    
    # التشغيل
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=WEBHOOK_URL,
        drop_pending_updates=True,
        allowed_updates=Update.ALL_TYPES
    )

if __name__ == "__main__":
    main()
