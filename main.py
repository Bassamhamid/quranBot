import logging
import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# إعداد السجل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# قراءة المتغيرات من البيئة
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحبًا بك! ارسل /search ثم الكلمة التي تريد البحث عنها في القرآن.")

# أمر /search
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = ' '.join(context.args)
    if not query:
        await update.message.reply_text("❌ من فضلك أرسل كلمة بعد الأمر.")
        return

    url = f"https://api.quran.com/api/v4/search?q={query}&language=ar"
    try:
        response = requests.get(url)
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

def main():
    app = Application.builder().token(TOKEN).build()

    # إضافة أوامر
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("search", search))

    # تشغيل الويب هوك
    app.run_webhook(
        listen="0.0.0.0",
        port=10000,
        webhook_url=WEBHOOK_URL,
        drop_pending_updates=True
    )

if __name__ == "__main__":
    main()
