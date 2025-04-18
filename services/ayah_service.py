import requests
import logging

logger = logging.getLogger(__name__)

QURAN_API = "http://api.alquran.cloud/v1"

async def get_ayah(reference: str) -> str:
    try:
        # تنظيف المرجع من أي أحرف غير رقمية
        cleaned_ref = ''.join(c for c in reference if c.isdigit() or c == ':')
        
        if ':' not in cleaned_ref:
            return "⚠️ الرجاء استخدام التنسيق الصحيح (مثال: 1:1 أو 2:255)"
            
        url = f"http://api.alquran.cloud/v1/ayah/{cleaned_ref}/ar.alafasy"
        logger.info(f"Fetching ayah from: {url}")
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 404:
            return "⚠️ لم يتم العثور على الآية، تحقق من رقم السورة والآية"
            
        response.raise_for_status()
        data = response.json()
        
        ayah_data = data.get('data', {})
        text = ayah_data.get('text', '')
        surah = ayah_data.get('surah', {}).get('name', '')
        ayah_num = ayah_data.get('numberInSurah', '')
        
        return f"📖 {surah} (آية {ayah_num}):\n{text}"
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Ayah API Error: {e}\nURL: {url}")
        return "❌ تعذر الاتصال بخدمة الآيات، حاول لاحقاً"
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return "❌ حدث خطأ غير متوقع"
