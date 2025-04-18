from telegram import Update
from telegram.ext import ContextTypes
from services import search_service
import logging

logger = logging.getLogger(__name__)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        query = update.message.text.strip()
        
        if not query or query.startswith('/'):
            return
            
        await update.message.reply_chat_action(action="typing")
        results = await search_service.search_verses(query)
        await update.message.reply_text(results)
        
    except Exception as e:
        logger.error(f"Message handling error: {e}")
        await update.message.reply_text("🔍 جرب استخدام /search للبحث بدقة أكبر")
