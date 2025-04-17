import httpx
import logging
from urllib.parse import quote

logger = logging.getLogger(__name__)

QURAN_API = "https://api.quran.com/api/v4"

async def search_verses(query: str, max_results: int = 5) -> str:
    """البحث عن آيات"""
    try:
        if not query.strip():
            return "⚠️ الرجاء إدخال نص للبحث"

        encoded_query = quote(query.strip())
        url = f"{QURAN_API}/search?q={encoded_query}&language=ar&limit={max_results}"
        logger.info(f"Search URL: {url}")

        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=15)

        if response.status_code == 404:
            return "🔍 لم يتم العثور على نتائج، جرب صيغة أخرى"

        response.raise_for_status()
        data = response.json()

        matches = data.get('data', {}).get('matches', [])
        if not matches:
            return "⚠️ لا توجد آيات تحتوي على هذه العبارة"

        results = []
        for match in matches:
            surah = match['verse']['surah_name']
            ayah_num = match['verse']['verse_number']
            text = match['verse']['text_uthmani']  # نص الآية مشكّل
            results.append(f"📖 {surah} (آية {ayah_num}):\n{text}\n")

        return "\n".join(results)

    except httpx.RequestError as e:
        logger.error(f"Search API Error: {str(e)}")
        return "❌ تعذر الاتصال بخدمة البحث"
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return "❌ حدث خطأ غير متوقع"
