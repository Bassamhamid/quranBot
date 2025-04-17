import requests
from telegram import Update

QURAN_API = "http://api.alquran.cloud/v1"

async def search_in_quran(query: str) -> str:
    try:
        url = f"{QURAN_API}/search/{query}/all/ar"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        matches = data.get('data', {}).get('matches', [])
        
        if not matches:
            return "⚠️ لم يتم العثور على نتائج"
            
        return "\n".join(
            f"سورة {m['surah']['name']} - الآية {m['numberInSurah']}:\n{m['text']}\n"
            for m in matches[:5]  # أول 5 نتائج فقط
        )
        
    except requests.exceptions.RequestException as e:
        return f"❌ خطأ في الاتصال بالخادم: {str(e)}"
    except Exception as e:
        return f"❌ خطأ غير متوقع: {str(e)}"
