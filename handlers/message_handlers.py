from telegram import Update
from telegram.ext import ContextTypes
from services import search_service

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة الرسائل العادية (بحث تلقائي)"""
    try:
        query = update.message.text.strip()
        
        if not query or query.startswith('/'):
            return
            
        await update.message.reply_chat_action(action="typing")
        results = await search_service.search_verses(query)
        await update.message.reply_text(results)
        
    except Exception as e:
        await update.message.reply_text("🔍 جرب استخدام /search للبحث بدقة أكبر")
