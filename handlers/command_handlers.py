from telegram import Update
from telegram.ext import ContextTypes
from services import search_service, ayah_service, tafsir_service
import logging

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_msg = """
🌿 *بوت القرآن الكريم* 🌿

🔍 أرسل أي كلمة مباشرة للبحث عن الآيات
/search [نص] - بحث متقدم
/ayah [سورة:آية] - جلب آية محددة
/tafsir [سورة:آية] - تفسير آية
/help - المساعدة
"""
    await update.message.reply_text(welcome_msg, parse_mode='Markdown')

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_msg = """
⚡ *أوامر البوت* ⚡

/ayah [سورة:آية] - جلب آية محددة
مثال: 
/ayah 1:1 - الآية 1 من سورة الفاتحة
/ayah 2:255 - آية الكرسي

/search [نص] - بحث في الآيات
/tafsir [سورة:آية] - تفسير آية
"""
    await update.message.reply_text(help_msg, parse_mode='Markdown')

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        query = ' '.join(context.args).strip()
        if not query:
            await update.message.reply_text("🔍 اكتب ما تريد البحث عنه:\n/search الرحمن")
            return
            
        await update.message.reply_chat_action(action="typing")
        results = await search_service.search_verses(query)
        await update.message.reply_text(results)
        
    except Exception as e:
        logger.error(f"Search error: {e}")
        await update.message.reply_text("❌ فشل البحث، جرب لاحقاً")

async def ayah(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        reference = ' '.join(context.args).strip()
        if not reference:
            await update.message.reply_text("📖 اكتب رقم السورة والآية:\n/ayah 2:255")
            return
            
        await update.message.reply_chat_action(action="typing")
        result = await ayah_service.get_ayah(reference)
        await update.message.reply_text(result)
        
    except Exception as e:
        logger.error(f"Ayah error: {e}")
        await update.message.reply_text("❌ فشل جلب الآية، تحقق من التنسيق")

async def tafsir(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        ref = ' '.join(context.args).strip()
        if not ref:
            await update.message.reply_text("📜 اكتب رقم السورة والآية:\n/tafsir 1:1")
            return
            
        await update.message.reply_chat_action(action="typing")
        result = await tafsir_service.get_tafsir(ref)
        await update.message.reply_text(result)
        
    except Exception as e:
        logger.error(f"Tafsir error: {e}")
        await update.message.reply_text("❌ فشل جلب التفسير، تحقق من التنسيق")
