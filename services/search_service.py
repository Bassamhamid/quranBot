import requests
import logging
from urllib.parse import quote

logger = logging.getLogger(__name__)

QURAN_API = "http://api.alquran.cloud/v1"

async def search_verses(query: str, max_results: int = 5) -> str:
    """البحث عن آيات تحتوي على النص"""
    try:
        # تنظيف الاستعلام وإزالة التشكيل إذا وجد
        cleaned_query = ''.join([char for char in query if not (0x064B <= ord(char) <= 0x0652)])
        encoded_query = quote(cleaned_query)
        
        url = f"{QURAN_API}/search/{encoded_query}/all/ar"
        logger.info(f"Search URL: {url}")
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 404:
            return "⚠️ لم يتم العثور على نتائج، جرب كلمات أقل أو بدون تشكيل"
            
        response.raise_for_status()
        data = response.json()
        
        matches = data.get('data', {}).get('matches', [])
        if not matches:
            return "⚠️ لم يتم العثور على آيات تحتوي على هذه الكلمة"
            
        results = []
        for match in matches[:max_results]:
            surah = match['surah']['name']
            ayah_num = match['numberInSurah']
            text = match['text']
            results.append(f"📖 {surah} (آية {ayah_num}):\n{text}\n")
        
        return "\n".join(results)
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {str(e)}")
        return "❌ تعذر الاتصال بخدمة القرآن"
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return "❌ حدث خطأ غير متوقع"
