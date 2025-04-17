import requests
import logging
from urllib.parse import quote

logger = logging.getLogger(__name__)

QURAN_API = "http://api.alquran.cloud/v1"

async def search_verses(query: str, max_results: int = 5) -> str:
    """البحث عن آيات تحتوي على النص"""
    try:
        if not query.strip():
            return "⚠️ الرجاء إدخال نص للبحث"

        # ترميز الاستعلام وتنظيفه
        encoded_query = quote(query.strip())
        url = f"{QURAN_API}/search/{encoded_query}/all/ar"
        
        logger.info(f"Search URL: {url}")
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 404:
            return "🔍 لم يتم العثور على نتائج، جرب كلمات أخرى"
        
        response.raise_for_status()
        data = response.json()
        
        matches = data.get('data', {}).get('matches', [])
        if not matches:
            return "⚠️ لا توجد آيات تحتوي على هذه الكلمة"
            
        # تجهيز النتائج
        results = []
        for match in matches[:max_results]:
            surah_name = match['surah']['name']
            ayah_num = match['numberInSurah']
            ayah_text = match['text']
            results.append(f"📖 {surah_name} (آية {ayah_num}):\n{ayah_text}\n")
        
        return "\n".join(results)
        
    except requests.exceptions.RequestException as e:
        logger.error(f"API Error: {str(e)}")
        return "❌ تعذر الاتصال بخدمة القرآن"
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return "❌ حدث خطأ غير متوقع"
