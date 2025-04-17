import os
import logging
import httpx
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram.ext import CallbackContext

# إعدادات السجل (Logging)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# متغيرات البيئة
TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
WEBHOOK_URL = os.environ['WEBHOOK_URL']
PORT = int(os.environ.get('PORT', 10000))

QURAN_API_URL = "https://api.quran.com/api/v4/verses/by_key"

# دالة البحث عن الآيات
async def search_verses(query: str):
    """البحث عن آية بناءً على النص"""
    try:
        if not query.strip():
            return "⚠️ الرجاء إدخال نص للبحث"
        
        # إنشاء الرابط للبحث
        search_url = f"{QURAN_API_URL}?q={query}&language=ar"
        logger.info(f"Search URL: {search_url}")
        
        # إرسال طلب للبحث
        async with httpx.AsyncClient() as client:
            response = await client.get(search_url)
        
        if response.status_code == 200:
            data = response.json()
            matches = data.get("data", {}).get("matches", [])
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
            return "❌ لم يتم العثور على نتائج"

    except httpx.RequestError as e:
        logger.error(f"API Error: {str(e)}")
        return "❌ تعذر الاتصال بخدمة البحث"
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return "❌ حدث خطأ غير متوقع"

# دالة بدء البوت
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("مرحبا! أرسل لي نصًا للبحث عن آية من القرآن.")

# دالة مساعدة
async def help(update: Update, context: CallbackContext):
    await update.message.reply_text("استخدم /search متبوعًا بالنص للبحث عن آية.")

# دالة البحث
async def search(update: Update, context: CallbackContext):
    query = " ".join(context.args)
    if query:
        result = await search_verses(query)
        await update.message.reply_text(result)
    else:
        await update.message.reply_text("⚠️ يجب إدخال نص للبحث.")

# تهيئة البوت مع Webhook
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

def main():
    # إنشاء تطبيق البوت
    app = Application.builder() \
        .token(TOKEN) \
        .post_init(post_init) \
        .build()

    # إضافة معالجات الأوامر
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("search", search))

    # تشغيل البوت
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=WEBHOOK_URL,
        drop_pending_updates=True
    )

if __name__ == "__main__":
    main()
