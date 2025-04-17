import requests
import logging

logger = logging.getLogger(__name__)

QURAN_API = "http://api.alquran.cloud/v1"

async def get_ayah(reference: str) -> str:
    """جلب آية محددة برقمها"""
    try:
        url = f"{QURAN_API}/ayah/{reference}/ar.alafasy"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        ayah = data.get('data', {})
        
        if not ayah:
            return "⚠️ لم يتم العثور على الآية"
            
        text = ayah.get('text', '')
        surah = ayah.get('surah', {}).get('name', '')
        ayah_num = ayah.get('numberInSurah', '')
        
        return f"📖 {surah} (آية {ayah_num}):\n{text}"
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {str(e)}")
        return "❌ تعذر الاتصال بخدمة القرآن"
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return "❌ حدث خطأ غير متوقع"
