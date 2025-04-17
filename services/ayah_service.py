import requests
import logging

logger = logging.getLogger(__name__)

QURAN_API = "http://api.alquran.cloud/v1"

async def get_ayah(reference: str) -> str:
    """جلب آية محددة برقمها أو مرجعها"""
    try:
        url = f"{QURAN_API}/ayah/{reference}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        ayah_data = data.get('data', {})
        
        if not ayah_data:
            return "⚠️ لم يتم العثور على الآية"
            
        text = ayah_data.get('text', '')
        surah = ayah_data.get('surah', {}).get('name', '')
        ayah_num = ayah_data.get('numberInSurah', '')
        
        return f"📖 {surah} (آية {ayah_num}):\n{text}"
        
    except Exception as e:
        logger.error(f"Ayah error: {str(e)}")
        return "❌ حدث خطأ أثناء جلب الآية"
