import requests

QURAN_API = "http://api.alquran.cloud/v1"

async def search_in_quran(query: str) -> str:
    try:
        response = requests.get(f"{QURAN_API}/search/{query}/all/ar", timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if not data.get('data', {}).get('matches'):
            return "لم يتم العثور على نتائج"
            
        results = []
        for match in data['data']['matches'][:5]:  # أول 5 نتائج فقط
            surah = match['surah']['name']
            ayah = match['numberInSurah']
            text = match['text']
            results.append(f"سورة {surah} الآية {ayah}:\n{text}\n")
            
        return "\n".join(results)
        
    except requests.exceptions.RequestException:
        return "تعذر الاتصال بخدمة القرآن"
    except Exception as e:
        return f"حدث خطأ غير متوقع: {str(e)}"
