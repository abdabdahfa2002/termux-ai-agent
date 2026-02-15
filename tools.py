import subprocess
import os
import requests
from bs4 import BeautifulSoup

def execute_shell(command):
    """تنفيذ أمر في تيرمكس وإعادة النتيجة"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exit_code": result.returncode
        }
    except Exception as e:
        return {"error": str(e)}

def read_file(path):
    """قراءة محتوى ملف"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return str(e)

def write_file(path, content):
    """كتابة محتوى إلى ملف"""
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"تم حفظ الملف بنجاح في {path}"
    except Exception as e:
        return str(e)

def search_web(query):
    """البحث في الويب وجلب النتائج"""
    try:
        search_url = f"https://www.google.com/search?q={query}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        return text[:2000] # إرجاع أول 2000 حرف لتجنب تجاوز حدود النموذج
    except Exception as e:
        return f"خطأ في البحث: {str(e)}"

def get_termux_info():
    """جلب معلومات الجهاز عبر Termux API"""
    battery = execute_shell("termux-battery-status")
    wifi = execute_shell("termux-wifi-connectioninfo")
    return {
        "battery": battery.get("stdout"),
        "wifi": wifi.get("stdout")
    }

# قائمة الأدوات المتاحة للنموذج (Function Calling)
TOOLS_DEFINITION = [
    {
        "type": "function",
        "function": {
            "name": "execute_shell",
            "description": "تنفيذ أوامر Terminal في بيئة Termux",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "الأمر المراد تنفيذه"}
                },
                "required": ["command"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "قراءة محتوى ملف من الذاكرة",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "مسار الملف"}
                },
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "إنشاء أو تعديل ملف",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "مسار الملف"},
                    "content": {"type": "string", "description": "المحتوى الجديد"}
                },
                "required": ["path", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "البحث في الإنترنت للحصول على معلومات حديثة",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "كلمات البحث"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_termux_info",
            "description": "جلب معلومات البطارية والواي فاي من جهاز الأندرويد",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]
