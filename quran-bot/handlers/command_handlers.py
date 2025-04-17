from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج أمر /start مع رسالة ترحيبية معدلة"""
    welcome_message = """
🌿 *مرحبًا بك في بوت القرآن الكريم* 🌿

📚 يمكنك استخدام الأوامر التالية:

🔍 /search [نص] - للبحث عن آيات
🔢 /count [كلمة] - لمعرفة تكرار الكلمة في القرآن
📖 /tafsir [سورة:آية] - للحصول على تفسير الآية

أو اكتب جزءًا من الآية مباشرة وسأساعدك في العثور عليها.
    """
    await update.message.reply_text(welcome_message, parse_mode='Markdown')

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج أمر /help مع تنسيق محسن"""
    help_text = """
🕌 *مساعدة بوت القرآن الكريم* 🕌

🔍 */search [نص]*
- ابحث عن آيات تحتوي على النص
- مثال: `/search والسماء ذات البروج`

🔢 */count [كلمة]*
- عدد مرات ذكر الكلمة في القرآن
- مثال: `/count الصبر`

📖 */tafsir [سورة:آية]*
- تفسير آية معينة
- مثال: `/tafsir 18:10`
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')
