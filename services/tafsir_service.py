import requests
import logging
import re

logger = logging.getLogger(__name__)

QURAN_API = "http://api.alquran.cloud/v1"

async def get_tafsir(reference: str) -> str:
    try:
        ref = re.sub(r'[^\d:]', '', reference.replace('-', ':'))
        if ':' not in ref:
            return "⚠️ تنسيق غير صحيح (استخدم: سورة:آية)"
            
        url = f"{QURAN_API}/ayah/{ref}/ar.muyassar"
        logger.info(f"Tafsir URL: {url}")
        
        response = requests.get(url, timeout=15)
        
        if response.status_code == 404:
            return "⚠️ لا يوجد تفسير لهذه الآية"
            
        response.raise_for_status()
        data = response.json()
        
        tafsir = data.get('data', {}).get('text', '')
        if not tafsir:
            return "⚠️ لا يوجد تفسير متاح"
            
        return f"📜 تفسير الآية {ref}:\n{tafsir}"
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Tafsir API Error: {e}\nURL: {url}")
        return "❌ تعذر الاتصال بخدمة التفسير"
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return "❌ حدث خطأ غير متوقع"
