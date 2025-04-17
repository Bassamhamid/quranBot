from telegram import Update
from telegram.ext import ContextTypes
from services import search_service

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة الرسائل النصية العادية"""
    try:
        user_text = update.message.text.strip()
        
        if not user_text or user_text.startswith('/'):
            return
            
        await update.message.reply_chat_action(action="typing")
        search_results = await search_service.search_verses(user_text)
        await update.message.reply_text(search_results)
        
    except Exception as e:
        await update.message.reply_text("❌ فشل البحث، يرجى المحاولة لاحقاً")
