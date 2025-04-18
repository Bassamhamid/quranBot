import os
import logging
import requests
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

# إعداد اللوجات
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# إعداد التوكن وبيانات الويب هوك من متغيرات البيئة
BOT_TOKEN = os.environ['BOT_TOKEN']
WEBHOOK_URL = os.environ['WEBHOOK_URL']
PORT = int(os.environ.get('PORT', 10000))

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحبًا! أرسل /search متبوعًا بالكلمة للبحث في القرآن.")

# أمر /search
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = ' '.join(context.args)
    if not query:
        await update.message.reply_text("❌ من فضلك أرسل كلمة بعد الأمر.")
        return

    url = f"https://api.quran.com/api/v4/search?q={query}&language=ar"
    try:
        response = requests.get(url)
        logger.info(f"Response Text: {response.text}")  # طباعة استجابة API

        data = response.json()
        logger.info(f"استجابة API: {data}")

        if 'data' in data and 'matches' in data['data'] and data['data']['matches']:
            results = data['data']['matches']
            result_text = "تم العثور على النتائج:\n\n"
            for result in results[:5]:
                result_text += f"الآية {result['verse_key']}:\n{result['text']}\n\n"
            await update.message.reply_text(result_text)
        else:
            await update.message.reply_text("❌ لم يتم العثور على نتائج.")
    except Exception as e:
        logger.error(f"❌ خطأ في الاتصال بـ API: {e}")
        await update.message.reply_text("❌ حدث خطأ أثناء الاتصال بـ API.")

# دالة تشغيل البوت
def main():
    application = Application.builder().token(BOT_TOKEN).build()

    # أوامر البوت
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("search", search))

    # تشغيل الويب هوك
    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=WEBHOOK_URL,
    )

if __name__ == "__main__":
    main()
