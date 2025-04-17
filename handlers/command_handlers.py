from telegram import Update
from telegram.ext import ContextTypes
from services import search_service, tafsir_service

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_msg = """
🌿 *بوت القرآن الكريم* 🌿

🔍 أرسل أي كلمة مباشرة للبحث عن الآيات
/search [نص] - بحث متقدم
/tafsir [سورة:آية] - تفسير آية
/help - المساعدة
"""
    await update.message.reply_text(welcome_msg, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_msg = """
⚡ *طريقة الاستخدام* ⚡

1. البحث المباشر:
   - اكتب أي كلمة (مثال: الرحمن)
   
2. الأوامر:
   - /search [نص] - بحث في الآيات
   - /tafsir [سورة:آية] - تفسير آية
   - مثال: /tafsir 1:1
"""
    await update.message.reply_text(help_msg, parse_mode='Markdown')

async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة أمر /search"""
    try:
        query = ' '.join(context.args).strip()
        
        if not query:
            await update.message.reply_text("⚡ استخدم: /search [الكلمة]")
            return
            
        await update.message.reply_chat_action(action="typing")
        results = await search_service.search_verses(query, max_results=10)
        await update.message.reply_text(results)
        
    except Exception as e:
        await update.message.reply_text("❌ فشل البحث، جرب كلمات أخرى")

async def tafsir_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة أمر /tafsir"""
    try:
        reference = ' '.join(context.args).strip()
        
        if not reference or ':' not in reference:
            await update.message.reply_text("⚡ استخدم: /tafsir [سورة:آية]\nمثال: /tafsir 2:255")
            return
            
        await update.message.reply_chat_action(action="typing")
        tafsir = await tafsir_service.get_tafsir(reference)
        await update.message.reply_text(tafsir)
        
    except Exception as e:
        await update.message.reply_text("❌ فشل جلب التفسير، تحقق من المرجع")
