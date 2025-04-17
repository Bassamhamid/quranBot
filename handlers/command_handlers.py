from telegram import Update
from telegram.ext import ContextTypes
from services import search_service, tafsir_service, ayah_service

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_msg = """
🌿 *بوت القرآن الكريم* 🌿

🔍 أرسل أي كلمة مباشرة للبحث عن الآيات
/search [نص] - بحث متقدم
/ayah [سورة:آية] - جلب آية محددة  # تمت الإضافة
/tafsir [سورة:آية] - تفسير آية
/help - المساعدة
"""
    await update.message.reply_text(welcome_msg, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_msg = """
⚡ *أوامر البوت* ⚡

/ayah [مرجع] - جلب آية محددة
مثال: 
/ayah 1:1  - الآية 1 من سورة الفاتحة
/ayah 2:255 - آية الكرسي
"""
    await update.message.reply_text(help_msg, parse_mode='Markdown')

async def ayah_command(update: Update, context: ContextTypes.DEFAULT_TYPE):  # المعالج الجديد
    """جلب آية محددة"""
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
