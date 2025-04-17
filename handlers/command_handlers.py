from telegram import Update
from telegram.ext import ContextTypes
from services import search_service, tafsir_service, ayah_service

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

/ayah [مرجع] - جلب آية محددة
مثال: 
/ayah 1:1  - الآية 1 من سورة الفاتحة
/ayah 2:255 - آية الكرسي
/search [نص] - بحث في الآيات
/tafsir [سورة:آية] - تفسير آية
"""
    await update.message.reply_text(help_msg, parse_mode='Markdown')

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة أمر البحث /search"""
    try:
        query = ' '.join(context.args).strip()
        if not query:
            await update.message.reply_text("⚡ استخدم: /search [الكلمة]")
            return
            
        await update.message.reply_chat_action(action="typing")
        results = await search_service.search_verses(query)
        await update.message.reply_text(results)
        
    except Exception as e:
        await update.message.reply_text("❌ فشل البحث، جرب كلمات أخرى")

async def ayah(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة أمر /ayah"""
    try:
        reference = ' '.join(context.args).strip()
        if not reference:
            await update.message.reply_text("⚡ استخدم: /ayah [سورة:آية]\nمثال: /ayah 2:255")
            return
            
        await update.message.reply_chat_action(action="typing")
        result = await ayah_service.get_ayah(reference)
        await update.message.reply_text(result)
        
    except Exception as e:
        await update.message.reply_text("❌ فشل جلب الآية، تحقق من المرجع")

async def tafsir(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة أمر /tafsir"""
    try:
        reference = ' '.join(context.args).strip()
        if not reference:
            await update.message.reply_text("⚡ استخدم: /tafsir [سورة:آية]\nمثال: /tafsir 2:255")
            return
            
        await update.message.reply_chat_action(action="typing")
        tafsir = await tafsir_service.get_tafsir(reference)
        await update.message.reply_text(tafsir)
        
    except Exception as e:
        await update.message.reply_text("❌ فشل جلب التفسير، تحقق من المرجع")
