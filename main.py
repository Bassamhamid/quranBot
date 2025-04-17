import os
import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# تكوين التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
WEBHOOK_URL = os.environ['WEBHOOK_URL']
PORT = int(os.environ.get('PORT', 10000))

async def search_quran(query: str) -> str:
    try:
        # تسجيل الاستعلام للتحقق
        logger.info(f"Searching for: {query}")
        
        url = f"http://api.alquran.cloud/v1/search/{query}/all/ar"
        response = requests.get(url, timeout=10)
        
        # تسجيل تفاصيل الاستجابة
        logger.info(f"API Response: {response.status_code}")
        logger.info(f"Response content: {response.text[:200]}...")
        
        response.raise_for_status()
        data = response.json()
        
        if not data.get('data', {}).get('matches'):
            return "⚠️ لم يتم العثور على نتائج"
            
        results = []
        for match in data['data']['matches'][:3]:  # أول 3 نتائج
            surah = match['surah']['name']
            ayah = match['numberInSurah']
            text = match['text']
            results.append(f"📖 {surah} (آية {ayah}):\n{text}\n")
            
        return "\n".join(results)
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {str(e)}")
        return "❌ تعذر الاتصال بخدمة القرآن"
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return "❌ حدث خطأ غير متوقع"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحباً! أرسل لي أي كلمة أو عبارة للبحث عنها في القرآن الكريم")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        query = update.message.text
        logger.info(f"Received message: {query}")
        
        # تجاهل الأوامر التي تبدأ ب /
        if query.startswith('/'):
            return
            
        results = await search_quran(query)
        logger.info(f"Sending results: {results[:50]}...")
        
        await update.message.reply_text(results)
    except Exception as e:
        logger.error(f"Message handling error: {str(e)}")
        await update.message.reply_text("❌ حدث خطأ في معالجة طلبك")

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # إعداد Webhook
    async def post_init(app):
        await app.bot.set_webhook(
            url=WEBHOOK_URL,
            drop_pending_updates=True
        )
        logger.info(f"Webhook configured at: {WEBHOOK_URL}")
    
    app.post_init = post_init
    
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=WEBHOOK_URL,
    )

if __name__ == "__main__":
    main()
