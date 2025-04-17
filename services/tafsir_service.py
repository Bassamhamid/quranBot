import requests
import logging

logger = logging.getLogger(__name__)

QURAN_API = "http://api.alquran.cloud/v1"

async def get_tafsir(reference: str, tafsir_edition: str = "ar.muyassar") -> str:
    """الحصول على تفسير آية محددة"""
    try:
        url = f"{QURAN_API}/ayah/{reference}/{tafsir_edition}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        tafsir_text = data.get('data', {}).get('text', '')
        
        if not tafsir_text:
            return "⚠️ لم يتم العثور على تفسير لهذه الآية"
            
        return f"📜 تفسير الآية {reference}:\n{tafsir_text}"
        
    except Exception as e:
        logger.error(f"Tafsir error: {str(e)}")
        return "❌ حدث خطأ أثناء جلب التفسير"
