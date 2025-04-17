import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# تمكين التسجيل للتحقق من الأخطاء
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
WEBHOOK_URL = os.environ['WEBHOOK_URL']
PORT = int(os.environ.get('PORT', 10000))

async def search_quran(query: str) -> str:
    try:
        url = f"http://api.alquran.cloud/v1/search/{query}/all/ar"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if not data.get('data', {}).get('matches'):
            return "⚠️ لم يتم العثور على نتائج"
            
        results = []
        for match in data['data']['matches'][:3]:  # عرض أول 3 نتائج فقط
            surah = match['surah']['name']
            ayah = match['numberInSurah']
            text = match['text']
            results.append(f"📖 {surah} (آية {ayah}):\n{text}\n")
            
        return "\n".join(results)
        
    except Exception as e:
        logging.error(f"Search error: {e}")
        return "❌ حدث خطأ أثناء البحث، يرجى المحاولة لاحقًا"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحباً! أرسل لي أي كلمة أو عبارة للبحث عنها في القرآن الكريم")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    logging.info(f"Received query: {query}")
    
    if query.startswith('/'):
        await update.message.reply_text("⚠️ الرجاء إرسال كلمة أو عبارة للبحث فقط")
        return
        
    results = await search_quran(query)
    await update.message.reply_text(results)

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Webhook setup
    async def post_init(app):
        await app.bot.set_webhook(WEBHOOK_URL)
        logging.info(f"Webhook set to: {WEBHOOK_URL}")
    
    app.post_init = post_init
    
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=WEBHOOK_URL,
        drop_pending_updates=True
    )

if __name__ == "__main__":
    import requests
    main()
