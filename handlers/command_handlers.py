from telegram import Update
from telegram.ext import ContextTypes
from services import search_service, tafsir_service, ayah_service

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_msg = """
🌿 *بوت القرآن الكريم* 🌿

أرسل أي كلمة أو عبارة وسأجدها لك في القرآن.

الأوامر المتاحة:
/search [نص] - بحث متقدم
/ayah [سورة:آية] - جلب آية محددة
/tafsir [سورة:آية] - تفسير آية
/help - المساعدة
"""
    await update.message.reply_text(welcome_msg, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_msg = """
🕌 *أوامر البوت* 🕌

🔍 أرسل أي كلمة مباشرة للبحث عن الآيات التي تحتويها

🔍 /search [نص]
- بحث متقدم مع نتائج أدق
- مثال: `/search الرحمن علم القرآن`

📖 /ayah [مرجع]
- جلب آية محددة
- مثال: `/ayah 2:255` أو `/ayah 112`

📜 /tafsir [مرجع]
- تفسير آية محددة
- مثال: `/tafsir 18:10`
"""
    await update.message.reply_text(help_msg, parse_mode='Markdown')

async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """بحث متقدم عن الآيات"""
    query = ' '.join(context.args)
    if not query:
        await update.message.reply_text("⚠️ الرجاء إدخال نص للبحث\nمثال: /search الرحمن")
        return
        
    results = await search_service.search_verses(query, max_results=10)  # نتائج أكثر
    await update.message.reply_text(results)

async def ayah_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """جلب آية محددة"""
    reference = ' '.join(context.args)
    if not reference:
        await update.message.reply_text("⚠️ الرجاء إدخال مرجع الآية\nمثال: /ayah 2:255")
        return
        
    result = await ayah_service.get_ayah(reference)
    await update.message.reply_text(result)

async def tafsir_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """جلب تفسير آية"""
    reference = ' '.join(context.args)
    if not reference:
        await update.message.reply_text("⚠️ الرجاء إدخال مرجع الآية\nمثال: /tafsir 2:255")
        return
        
    result = await tafsir_service.get_tafsir(reference)
    await update.message.reply_text(result)
