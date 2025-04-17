import os
import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# تكوين التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# قراءة التوكن من البيئة
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# رابط الويب هوك (تأكد من ضبطه في متغيرات البيئة على ريندر)
WEBHOOK_URL = os.getenv('WEBHOOK_URL')

# دالة التعامل مع الأوامر
async def start(update: Update, context):
    await update.message.reply_text("أهلاً بك! يمكنني مساعدتك في البحث عن آيات القرآن الكريم. اكتب أي كلمة للبحث.")

async def search(update: Update, context):
    # الحصول على النص من المستخدم
    query = ' '.join(context.args)
    if not query:
        await update.message.reply_text("❌ من فضلك أرسل كلمة للبحث.")
        return

    # تنفيذ البحث في واجهة برمجة التطبيقات
    url = f"https://api.quran.com/api/v4/search?q={query}"
    try:
        response = requests.get(url)
        data = response.json()

        if data['data']:
            results = data['data']
            # تحديد عدد النتائج لإظهارها
            result_text = "تم العثور على النتائج التالية:\n"
            for result in results[:5]:  # عرض أول 5 نتائج
                result_text += f"الآية {result['verse_key']} : {result['text']}\n"
            await update.message.reply_text(result_text)
        else:
            await update.message.reply_text("❌ لم يتم العثور على نتائج.")
    except Exception as e:
        logger.error(f"❌ خطأ في الاتصال بـ API: {e}")
        await update.message.reply_text("❌ حدث خطأ أثناء الاتصال بـ API.")

# تكوين الويب هوك
async def post_init(app):
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

# دالة تشغيل البوت
def main():
    # إنشاء تطبيق البوت
    app = Application.builder() \
        .token(TOKEN) \
        .post_init(post_init) \
        .build()

    # تسجيل معالجات الأوامر
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("search", search))

    # تشغيل البوت
    app.run_webhook(
        listen="0.0.0.0",
        port=10000,
        webhook_url=WEBHOOK_URL,
        drop_pending_updates=True
    )

if __name__ == "__main__":
    main()
