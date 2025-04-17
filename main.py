import os
import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# إعداد التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# قراءة المتغيرات من البيئة
TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
WEBHOOK_URL = os.environ['WEBHOOK_URL']
PORT = int(os.environ.get('PORT', 10000))
API_URL = os.environ['API_URL_PRELIVE']
CLIENT_ID = os.environ['CLIENT_ID_PRELIVE']
CLIENT_SECRET = os.environ['CLIENT_SECRET_PRELIVE']

# دالة بدء البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً بك! أرسل أي كلمة أو آية للبحث عنها.")

# دالة البحث
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    if not query:
        await update.message.reply_text("الرجاء إدخال نص للبحث.")
        return

    try:
        response = requests.get(
            f"{API_URL}/v1/quran/verses",
            params={"filter": query},
            auth=(CLIENT_ID, CLIENT_SECRET)
        )
        if response.status_code == 200:
            data = response.json()
            if data.get("data"):
                ayat = data["data"]
                result_text = "\n\n".join(f"{ayah['text']}" for ayah in ayat)
                await update.message.reply_text(result_text)
            else:
                await update.message.reply_text("❌ لم يتم العثور على نتائج.")
        else:
            await update.message.reply_text("❌ حدث خطأ أثناء الاتصال.")
    except Exception as e:
        logger.error(f"خطأ في البحث: {e}")
        await update.message.reply_text("❌ حدث خطأ أثناء الاتصال.")

# تهيئة الويب هوك
async def post_init(app):
    try:
        await app.bot.set_webhook(
            url=WEBHOOK_URL,
            drop_pending_updates=True,
            allowed_updates=["message"]
        )
        logger.info(f"✅ تم تعيين الويب هوك: {WEBHOOK_URL}")
    except Exception as e:
        logger.error(f"❌ تعيين الويب هوك فشل: {str(e)}")
        raise

def main():
    app = Application.builder().token(TOKEN).post_init(post_init).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search))

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=WEBHOOK_URL,
        drop_pending_updates=True
    )

if __name__ == "__main__":
    main()
