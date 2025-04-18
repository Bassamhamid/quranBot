from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import requests, os, logging

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.environ['BOT_TOKEN']
WEBHOOK_URL = os.environ['WEBHOOK_URL']
PORT = int(os.environ.get('PORT', 10000))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحبًا! أرسل /search <كلمة> للبحث في القرآن.")

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("اكتب الأمر بالشكل:\n/search كلمة")
        return

    query = " ".join(context.args)
    url = f"https://api.quran.com/api/v4/search?q={query}"
    headers = {"Accept": "application/json"}

    try:
        response = requests.get(url, headers=headers)
        data = response.json()

        if "data" in data and data["data"]["count"] > 0:
            results = data["data"]["matches"]
            message = "\n\n".join([f"{r['text']}" for r in results[:5]])  # أول 5 نتائج
        else:
            message = "❌ لم يتم العثور على نتائج."

    except Exception as e:
        logging.error(f"❌ خطأ في الاتصال بـ API: {e}")
        message = "حدث خطأ أثناء الاتصال بالخدمة."

    await update.message.reply_text(message)

if __name__ == '__main__':
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("search", search))

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=f"{WEBHOOK_URL}/webhook"
        )
