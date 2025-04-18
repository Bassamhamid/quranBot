import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests

# إعداد اللوق
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# قراءة المتغيرات من البيئة بطريقة آمنة
BOT_TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
PORT = int(os.environ.get("PORT", "10000"))

# تحقق من وجود التوكن
if not BOT_TOKEN:
    logging.error("❌ BOT_TOKEN غير موجود في متغيرات البيئة")
    exit(1)

# دالة start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحبًا! أرسل لي أي كلمة للبحث عنها في القرآن.")

# دالة البحث
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    url = f"https://api.quran.com/api/v4/search?q={query}"
    try:
        response = requests.get(url)
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

# التطبيق
app = Application.builder().token(BOT_TOKEN).build()

# الهاندلرز
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search))

# تشغيل البوت بالويب هوك
app.run_webhook(
    listen="0.0.0.0",
    port=PORT,
    webhook_url=WEBHOOK_URL
)
