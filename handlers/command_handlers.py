from telegram import Update
from telegram.ext import ContextTypes
from services import search_service, tafsir_service

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
    """معالجة أمر /search (للعثور على الآيات فقط)"""
    try:
        query = ' '.join(context.args).strip()
        if not query:
            await update.message.reply_text("🔍 اكتب ما تريد البحث عنه:\n/search الرحمن")
            return
            
        await update.message.reply_chat_action(action="typing")
        results = await search_service.search_verses(query)
        await update.message.reply_text(results)
        
    except Exception as e:
        await update.message.reply_text("❌ فشل البحث، جرب لاحقاً")

async def tafsir(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة أمر /tafsir (لجلب التفسير فقط)"""
    try:
        ref = ' '.join(context.args).strip()
        if not ref:
            await update.message.reply_text("📖 اكتب رقم السورة والآية:\n/tafsir 2:255")
            return
            
        await update.message.reply_chat_action(action="typing")
        result = await tafsir_service.get_tafsir(ref)
        await update.message.reply_text(result)
        
    except Exception as e:
        await update.message.reply_text("❌ فشل جلب التفسير، تحقق من التنسيق")
