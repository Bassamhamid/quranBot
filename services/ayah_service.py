import requests
import logging

logger = logging.getLogger(__name__)

QURAN_API = "http://api.alquran.cloud/v1"

async def get_ayah(reference: str) -> str:
    try:
        url = f"{QURAN_API}/ayah/{reference}/ar.alafasy"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        ayah = data.get('data', {})
        
        text = ayah.get('text', '')
        surah = ayah.get('surah', {}).get('name', '')
        ayah_num = ayah.get('numberInSurah', '')
        
        return f"📖 {surah} (آية {ayah_num}):\n{text}"
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Ayah API Error: {e}\nURL: {url}")
        return "❌ تعذر جلب الآية، تحقق من الاتصال بالإنترنت"
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return "❌ حدث خطأ غير متوقع"
