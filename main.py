import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import requests

# تكوين التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# قراءة المتغيرات من البيئة على ريندر
TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
WEBHOOK_URL = os.environ['WEBHOOK_URL']
PORT = int(os.environ.get('PORT', 10000))
QURAN_API_KEY = os.environ['QURAN_API_KEY']

# الدوال الخاصة بالمعالجات
async def start(update: Update, context: CallbackContext) -> None:
    """أمر البداية"""
    await update.message.reply_text('👋 مرحبًا! أنا بوت القرآن الكريم. كيف يمكنني مساعدتك اليوم؟')

async def help(update: Update, context: CallbackContext) -> None:
    """أمر المساعدة"""
    await update.message.reply_text('💡 يمكنك استخدام الأوامر التالية:\n'
                                    '/start - لبدء المحادثة\n'
                                    '/help - للحصول على المساعدة\n'
                                    '/search <الكلمة> - للبحث عن آية تحتوي على الكلمة\n'
                                    '/ayah <رقم الآية> - للحصول على نص الآية\n'
                                    '/tafsir <رقم الآية> - للحصول على تفسير الآية')

async def search(update: Update, context: CallbackContext) -> None:
    """البحث عن آية"""
    query = ' '.join(context.args)
    if not query:
        await update.message.reply_text('⚠️ الرجاء إدخال الكلمة التي تريد البحث عنها.')
        return

    # استخدام API للبحث
    url = f'https://api.quran.com:443/api/v4/search?q={query}&language=ar&limit=5'
    headers = {
        'Authorization': f'Bearer {QURAN_API_KEY}'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        matches = data.get('data', {}).get('matches', [])
        if matches:
            results = []
            for match in matches:
                surah = match['verse']['surah_name']
                ayah_num = match['verse']['verse_number']
                text = match['verse']['text_uthmani']
                results.append(f"📖 {surah} (آية {ayah_num}):\n{text}\n")
            await update.message.reply_text("\n".join(results))
        else:
            await update.message.reply_text('🔍 لم يتم العثور على نتائج.')
    else:
        await update.message.reply_text('❌ حدث خطأ أثناء الاتصال بمصادر البحث.')

async def ayah(update: Update, context: CallbackContext) -> None:
    """الحصول على نص الآية"""
    try:
        ayah_number = int(context.args[0])
        url = f'https://api.quran.com:443/api/v4/verses/{ayah_number}?language=ar'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            surah = data['data']['verse']['surah_name']
            ayah_text = data['data']['verse']['text_uthmani']
            await update.message.reply_text(f"📖 {surah} (آية {ayah_number}):\n{ayah_text}")
        else:
            await update.message.reply_text('❌ لم يتم العثور على الآية.')
    except (IndexError, ValueError):
        await update.message.reply_text('⚠️ الرجاء إدخال رقم الآية بشكل صحيح.')

async def tafsir(update: Update, context: CallbackContext) -> None:
    """الحصول على تفسير الآية"""
    try:
        ayah_number = int(context.args[0])
        url = f'https://api.quran.com:443/api/v4/tafsirs/{ayah_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            tafsir_text = data['data']['tafsir']
            await update.message.reply_text(f"📝 تفسير الآية: {tafsir_text}")
        else:
            await update.message.reply_text('❌ لم يتم العثور على التفسير.')
    except (IndexError, ValueError):
        await update.message.reply_text('⚠️ الرجاء إدخال رقم الآية بشكل صحيح.')

async def handle_text(update: Update, context: CallbackContext) -> None:
    """معالجة الرسائل العادية"""
    text = update.message.text
    await update.message.reply_text(f"👀 لقد تلقيت الرسالة: {text}")

# تهيئة الويب هوك
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

    # تسجيل معالجات الأوامر
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("search", search))
    app.add_handler(CommandHandler("ayah", ayah))
    app.add_handler(CommandHandler("tafsir", tafsir))

    # معالجة الرسائل العادية
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    # تشغيل البوت
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=WEBHOOK_URL,
        drop_pending_updates=True
    )

if __name__ == "__main__":
    main()
