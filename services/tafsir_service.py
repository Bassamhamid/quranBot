import requests
import logging
import re

logger = logging.getLogger(__name__)

QURAN_API = "http://api.alquran.cloud/v1"

async def get_tafsir(reference: str) -> str:
    """جلب التفسير فقط (بدون الآية)"""
    try:
        # تنظيف المرجع
        ref = re.sub(r'[^\d:]', '', reference.replace('-', ':'))
        if ':' not in ref:
            return "⚠️ تنسيق غير صحيح (استخدم: سورة:آية)"
            
        url = f"{QURAN_API}/ayah/{ref}/ar.muyassar"
        logger.info(f"Tafsir URL: {url}")
        
        response = requests.get(url, timeout=15)
        
        if response.status_code == 404:
            return "⚠️ لا يوجد تفسير لهذه الآية"
            
        response.raise_for_status()
        data = response.json()
        
        tafsir_text = data.get('data', {}).get('text', '')
        if not tafsir_text:
            return "⚠️ لا يوجد تفسير متاح"
            
        return f"📜 تفسير الآية {ref}:\n{tafsir_text}"
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Tafsir API Error: {str(e)}")
        return "❌ تعذر الاتصال بخدمة التفسير"
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return "❌ حدث خطأ غير متوقع"
