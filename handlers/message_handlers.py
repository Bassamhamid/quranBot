import requests
import logging
from urllib.parse import quote

logger = logging.getLogger(__name__)

QURAN_API = "http://api.alquran.cloud/v1"

async def search_verses(query: str, max_results: int = 5) -> str:
    """البحث عن آيات تحتوي على النص (بدون تفسير)"""
    try:
        encoded_query = quote(query)
        url = f"{QURAN_API}/search/{encoded_query}/all/ar"
        response = requests.get(url, timeout=10)
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
        
    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        return "❌ حدث خطأ أثناء البحث، يرجى المحاولة لاحقاً"
