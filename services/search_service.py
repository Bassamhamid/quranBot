import requests
import logging
from urllib.parse import quote

logger = logging.getLogger(__name__)

QURAN_API = "https://api.quran.com/v4"

async def search_verses(query: str, max_results: int = 5) -> str:
    """البحث عن آيات (بدون تفسير)"""
    try:
        if not query.strip():
            return "⚠️ الرجاء إدخال نص للبحث"

        # تنظيف الاستعلام
        clean_query = ''.join([c for c in query if c.isalpha() or c.isspace() or c in [':', '-']])
        encoded_query = quote(clean_query.strip())
        
        url = f"{QURAN_API}/search?q={encoded_query}&language=ar"
        logger.info(f"Search URL: {url}")

        response = requests.get(url, timeout=15)

        if response.status_code == 404:
            return "🔍 لم يتم العثور على نتائج، جرب صيغة أخرى"

        response.raise_for_status()
        data = response.json()

        matches = data.get('data', {}).get('matches', [])
        if not matches:
            return "⚠️ لا توجد آيات تحتوي على هذه الكلمة"

        # تجهيز النتائج (آيات فقط)
        results = []
        for match in matches[:max_results]:
            verse_key = match['verse_key']
            text = match['text_uthmani']
            results.append(f"📖 {verse_key}:\n{text}\n")

        return "\n".join(results)

    except requests.exceptions.RequestException as e:
        logger.error(f"Search API Error: {str(e)}")
        return "❌ تعذر الاتصال بخدمة البحث"
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return "❌ حدث خطأ غير متوقع"
