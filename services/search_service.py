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

        # تنظيف الاستعلام من علامات التشكيل والأحرف الخاصة
        clean_query = ''.join([c for c in query if c.isalpha() or c.isspace() or c.isnumeric()])
        encoded_query = quote(clean_query.strip())
        
        url = f"{QURAN_API}/search/{encoded_query}/all/ar"
        logger.info(f"Request URL: {url}")
        
        response = requests.get(url, timeout=15)
        
        # معالجة الاستجابة بشكل دقيق
        if response.status_code == 404:
            return "🔍 لم يتم العثور على نتائج، جرب صيغة أخرى للكلمة"
        
        response.raise_for_status()
        data = response.json()
        
        matches = data.get('data', {}).get('matches', [])
        if not matches:
            return "⚠️ لا توجد آيات تحتوي على هذه الكلمة بالصيغة المدخلة"
            
        # تجهيز النتائج
        results = []
        for match in matches[:max_results]:
            surah = match['surah']['name']
            ayah = match['numberInSurah']
            text = match['text']
            results.append(f"📖 {surah} (آية {ayah}):\n{text}\n")
        
        return "\n".join(results) if results else "⚠️ لا توجد نتائج"
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}\nURL: {url}")
        return "❌ تعذر الاتصال بخدمة البحث حالياً"
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return "❌ حدث خطأ غير متوقع أثناء البحث"
