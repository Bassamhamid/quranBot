from telegram import Update
from telegram.ext import ContextTypes, CallbackContext
from services import search_service, ayah_service, tafsir_service, surah_service

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة الرسائل النصية العادية (بحث تلقائي عن آيات)"""
    query = update.message.text.strip()
    
    if not query:
        await update.message.reply_text("🔍 أرسل كلمة أو عبارة للبحث عنها في القرآن")
        return
        
    # تجاهل إذا كانت الرسالة أمراً
    if query.startswith('/'):
        return
        
    results = await search_service.search_verses(query)
    await update.message.reply_text(results)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة الرسائل النصية العادية"""
    text = update.message.text
    
    # إذا بدأ النص برقم (يفترض أنه رقم سورة)
    if text.isdigit():
        surah_num = int(text)
        if 1 <= surah_num <= 114:
            result, _ = await surah_service.get_surah(surah_num)
            if result:
                await update.message.reply_text(result)
            else:
                await update.message.reply_text("⚠️ تعذر جلب السورة، يرجى المحاولة لاحقاً")
        else:
            await update.message.reply_text("⚠️ رقم السورة يجب أن يكون بين 1 و 114")
    else:
        # إذا كان النص طويلاً يفترض أنه بحث
        if len(text.split()) > 2:
            result = await search_service.search_verses(text)
            await update.message.reply_text(result)
        else:
            await update.message.reply_text("""
🔍 للبحث أرسل نصاً طويلاً أو استخدم الأوامر:
/search [نص] - للبحث في القرآن
/ayah [رقم] - لجلب آية
/surah [رقم] - لجلب سورة
""")

async def button_callback(update: Update, context: CallbackContext):
    """معالجة ضغطات الأزرار (لتصفح السور)"""
    query = update.callback_query
    await query.answer()
    
    if query.data.startswith('surah_'):
        _, surah_num, page = query.data.split('_')
        surah_num = int(surah_num)
        page = int(page)
        
        result, reply_markup = await surah_service.get_surah(surah_num, page)
        
        if result:
            await query.edit_message_text(result, reply_markup=reply_markup)
        else:
            await query.edit_message_text("⚠️ تعذر تحميل الصفحة التالية")
