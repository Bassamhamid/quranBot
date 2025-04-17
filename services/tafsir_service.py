import requests
import logging
import re

logger = logging.getLogger(__name__)

QURAN_API = "http://api.alquran.cloud/v1"

async def get_tafsir(reference: str) -> str:
    """جلب تفسير آية محددة"""
    try:
        # تنظيف المرجع وتنسيقه
        ref = re.sub(r'[^\d:]', '', reference)  # إزالة جميع الأحرف غير الأرقام والنقطتين
        if ':' not in ref:
            return "⚠️ استخدم التنسيق الصحيح (مثال: 2:255)"
            
        url = f"{QURAN_API}/ayah/{ref}/ar.muyassar"
        logger.info(f"Tafsir URL: {url}")
        
        response = requests.get(url, timeout=15)
        
        if response.status_code == 404:
            return "⚠️ لم يتم العثور على تفسير لهذه الآية"
            
        response.raise_for_status()
        data = response.json()
        
        tafsir = data.get('data', {}).get('text', '')
        if not tafsir:
            return "⚠️ لا يوجد تفسير متاح لهذه الآية"
            
        return f"📜 تفسير الآية {ref}:\n{tafsir}"
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Tafsir API Error: {e}\nURL: {url}")
        return "❌ تعذر الاتصال بخدمة التفسير حالياً"
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return "❌ حدث خطأ غير متوقع أثناء جلب التفسير"
