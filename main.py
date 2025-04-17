import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import httpx
from urllib.parse import quote

# إعدادات السجل
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# قراءة القيم من المتغيرات البيئية
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = int(os.getenv("PORT", 10000))
API_KEY = os.getenv("QURAN_API_KEY")  # المفتاح الذي حصلت عليه من مؤسسة القرآن الكريم
BASE_URL = "https://oauth2.quran.foundation/api/v4"  # نقطة النهاية للإنتاج

# دالة البحث عن آيات باستخدام API
async def search_verses(query: str, max_results: int = 5):
    """البحث عن آيات القرآن الكريم"""
    try:
        encoded_query = quote(query.strip())
        url = f"{BASE_URL}/search?q={encoded_query}&language=ar&limit={max_results}"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers={"Authorization": f"Bearer {API_KEY}"})

        if response.status_code == 200:
            data = response.json()
            matches = data.get('data', {}).get('matches', [])
            if not matches:
                return "⚠️ لا توجد آيات تحتوي على هذه العبارة"
            
            results = []
            for match in matches:
                surah = match['verse']['surah_name']
                ayah_num = match['verse']['verse_number']
                text = match['verse']['text_uthmani']
                results.append(f"📖 {surah} (آية {ayah_num}):\n{text}\n")

            return "\n".join(results)
        else:
            return "❌ لم يتم العثور على نتائج أو حدث خطأ في الاتصال."

    except httpx.RequestError as e:
        logger.error(f"Search API Error: {str(e)}")
        return "❌ حدث خطأ أثناء الاتصال بالـ API."

# دالة بدء البوت
async def start(update: Update, context: CallbackContext):
    """إرسال رسالة ترحيب عند بدء البوت"""
    await update.message.reply_text("السلام عليكم! كيف يمكنني مساعدتك في البحث عن آيات القرآن؟")

# دالة البحث باستخدام الكلمة المفتاحية
async def search(update: Update, context: CallbackContext):
    """تنفيذ البحث عن آية بناءً على النص المدخل"""
    if context.args:
        query = " ".join(context.args)
        result = await search_verses(query)
        await update.message.reply_text(result)
    else:
        await update.message.reply_text("⚠️ الرجاء إدخال نص البحث بعد الأمر.")

# دالة تهيئة الويب هوك
async def post_init(app):
    """تهيئة الويب هوك عند التشغيل"""
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

# دالة لتشغيل البوت
def main():
    """إعداد البوت وتشغيله"""
    application = Application.builder().token(TOKEN).post_init(post_init).build()

    # إضافة معالجات الأوامر
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("search", search))

    # تشغيل البوت
    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=WEBHOOK_URL,
        drop_pending_updates=True
    )

if __name__ == "__main__":
    main()
