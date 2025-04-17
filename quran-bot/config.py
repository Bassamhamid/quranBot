import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    WEBHOOK_URL = os.getenv('WEBHOOK_URL')
    QURAN_API_URL = 'http://api.alquran.cloud/v1'
    
    # يمكن إضافة المزيد من الإعدادات هنا
