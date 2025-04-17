from telegram import Update
from telegram.ext import ContextTypes
from services.quran_service import search_in_quran

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        results = await search_in_quran(update.message.text)
        await update.message.reply_text(results[:4000])
    except Exception as e:
        await update.message.reply_text(f"حدث خطأ: {str(e)}")
