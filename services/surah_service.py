import requests
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

logger = logging.getLogger(__name__)

QURAN_API = "http://api.alquran.cloud/v1"

async def get_surah(surah_number: int, page: int = 1, per_page: int = 10):
    """جلب آيات سورة معينة مع تقسيم لصفحات"""
    try:
        url = f"{QURAN_API}/surah/{surah_number}/ar.alafasy?page={page}&limit={per_page}"
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        
        data = response.json()
        surah_data = data.get('data', {})
        
        if not surah_data:
            return None, None
        
        surah_name = surah_data.get('name', f"سورة {surah_number}")
        ayahs = surah_data.get('ayahs', [])
        
        # تجهيز النتائج
        result_text = f"📖 {surah_name}\n\n"
        for ayah in ayahs:
            result_text += f"آية {ayah['numberInSurah']}: {ayah['text']}\n\n"
        
        # تجهيز أزرار التصفح
        total_ayahs = len(surah_data.get('ayahs', []))
        total_pages = (total_ayahs + per_page - 1) // per_page
        
        keyboard = []
        if page > 1:
            keyboard.append(InlineKeyboardButton("السابق", callback_data=f"surah_{surah_number}_{page-1}"))
        if page < total_pages:
            keyboard.append(InlineKeyboardButton("التالي", callback_data=f"surah_{surah_number}_{page+1}"))
        
        reply_markup = InlineKeyboardMarkup([keyboard]) if keyboard else None
        
        return result_text, reply_markup
        
    except Exception as e:
        logger.error(f"Surah error: {str(e)}")
        return None, None
