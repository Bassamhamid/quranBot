import requests
import logging

logger = logging.getLogger(__name__)

QURAN_API = "http://api.alquran.cloud/v1"

async def get_tafsir(reference: str) -> str:
    """جلب تفسير آية محددة"""
    try:
        if not reference.strip():
            return "⚠️ الرجاء تحديد السورة والآية (مثال: 1:1)"
            
        url = f"{QURAN_API}/ayah/{reference.strip()}/ar.muyassar"
        logger.info(f"Tafsir URL: {url}")
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        tafsir_text = data.get('data', {}).get('text', '')
        
        if not tafsir_text:
            return "⚠️ لا يوجد تفسير متاح لهذه الآية"
            
        return f"📜 تفسير الآية {reference}:\n{tafsir_text}"
        
    except requests.exceptions.RequestException as e:
        logger.error(f"API Error: {str(e)}")
        return "❌ تعذر الاتصال بخدمة التفسير"
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return "❌ حدث خطأ غير متوقع"
