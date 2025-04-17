from telegram import Update
from telegram.ext import ContextTypes
from services import search_service, ayah_service, tafsir_service

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج أمر /start"""
    welcome_msg = """
🌿 *بوت القرآن الكريم* 🌿

اختر أحد الأوامر التالية:

🔍 /search [نص] - بحث في آيات القرآن
📖 /ayah [سورة:آية] - جلب آية محددة
📜 /tafsir [سورة:آية] - تفسير آية محددة
ℹ️ /help - عرض المساعدة
"""
    await update.message.reply_text(welcome_msg, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج أمر /help"""
    help_msg = """
🕌 *أوامر البوت* 🕌

🔍 */search [نص]*
- ابحث عن أي كلمة أو عبارة في القرآن
- مثال: `/search الرحمن`

📖 */ayah [مرجع]*
- جلب آية محددة برقمها
- مثال: `/ayah 2:255` أو `/ayah 112`

📜 */tafsir [مرجع]*
- تفسير آية محددة
- مثال: `/tafsir 18:10`

📚 */surah [رقم]*
- عرض سورة كاملة
- مثال: `/surah 1`
"""
    await update.message.reply_text(help_msg, parse_mode='Markdown')

async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج أمر /search"""
    query = ' '.join(context.args)
    if not query:
        await update.message.reply_text("⚠️ الرجاء إدخال نص للبحث")
        return
        
    results = await search_service.search_verses(query)
    await update.message.reply_text(results)

async def ayah_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج أمر /ayah"""
    reference = ' '.join(context.args)
    if not reference:
        await update.message.reply_text("⚠️ الرجاء إدخال مرجع الآية (مثال: 2:255)")
        return
        
    result = await ayah_service.get_ayah(reference)
    await update.message.reply_text(result)

async def tafsir_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج أمر /tafsir"""
    reference = ' '.join(context.args)
    if not reference:
        await update.message.reply_text("⚠️ الرجاء إدخال مرجع الآية (مثال: 2:255)")
        return
        
    result = await tafsir_service.get_tafsir(reference)
    await update.message.reply_text(result)
