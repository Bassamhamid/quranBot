import requests
from config import Config

async def search_in_quran(query: str):
    try:
        url = f"{Config.QURAN_API_URL}/search/{query}/all/ar"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if data.get('code') == 200 and data.get('data'):
            matches = data['data']['matches']
            if not matches:
                return "لم يتم العثور على نتائج لبحثك."
            
            # تنسيق النتائج
            formatted_results = []
            for match in matches[:5]:  # نحدد بعدد النتائج لعرضها
                surah = match['surah']['name']
                ayah_num = match['numberInSurah']
                text = match['text']
                formatted_results.append(f"سورة {surah} - الآية {ayah_num}:\n{text}\n")
            
            return "\n".join(formatted_results)
        else:
            return "حدث خطأ أثناء البحث، يرجى المحاولة لاحقاً."
    except Exception as e:
        return f"حدث خطأ: {str(e)}"
