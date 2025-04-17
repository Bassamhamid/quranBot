from telegram import Update
from telegram.ext import ContextTypes
from services.quran_service import search_in_quran

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    # سننفذ لاحقاً البحث التلقائي عندما يكتب المستخدم نصاً بدون أمر
    results = await search_in_quran(user_text)
    await update.message.reply_text(results[:4000])  # الحد الأقصى لطول رسالة التليجرام
