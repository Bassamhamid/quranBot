from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import Config
import handlers.command_handlers as command_handlers
import handlers.message_handlers as message_handlers

def main():
    # إنشاء تطبيق البوت
    application = Application.builder().token(Config.TOKEN).build()
    
    # تسجيل معالجات الأوامر
    application.add_handler(CommandHandler("start", command_handlers.start))
    application.add_handler(CommandHandler("help", command_handlers.help))
    
    # معالجة الرسائل العادية
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handlers.handle_text))
    
    # تشغيل البوت
    application.run_polling()  # للتنمية المحلية، سنستخدم Webhook لاحقاً

if __name__ == "__main__":
    main()
