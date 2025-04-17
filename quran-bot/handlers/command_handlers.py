from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = """
    🌹 السلام عليكم ورحمة الله وبركاته 🌹
    
    أهلًا بك في بوت القرآن الكريم!
    
    يمكنك استخدام الأوامر التالية:
    /search [نص] - للبحث عن آيات
    /count [كلمة] - لمعرفة عدد مرات ذكر كلمة
    /tafsir [سورة:آية] - للحصول على تفسير الآية
    
    أو فقط اكتب جزء من الآية وسأحاول العثور عليها.
    """
    await update.message.reply_text(welcome_message)

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
    📖 مساعدة بوت القرآن الكريم:
    
    /search [نص] - ابحث عن آيات تحتوي على النص
    مثال: /search الرحمن علم القرآن
    
    /count [كلمة] - عدد مرات ذكر الكلمة في القرآن
    مثال: /count الصلاة
    
    /tafsir [سورة:آية] - تفسير آية معينة
    مثال: /tafsir 2:255
    """
    await update.message.reply_text(help_text)
