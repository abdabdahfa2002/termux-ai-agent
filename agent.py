import os
import json
import google.generativeai as genai
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from prompt_toolkit import prompt
from prompt_toolkit.styles import Style
from config import GEMINI_API_KEY, DEFAULT_MODEL, ADVANCED_MODEL, SYSTEM_PROMPT
from tools import execute_shell, read_file, write_file, search_web, get_termux_info

console = Console()

# إعداد Gemini
genai.configure(api_key=GEMINI_API_KEY)

class TermuxAgent:
    def __init__(self):
        self.tools = {
            "execute_shell": execute_shell,
            "read_file": read_file,
            "write_file": write_file,
            "search_web": search_web,
            "get_termux_info": get_termux_info
        }
        self.history = []
        self.style = Style.from_dict({'prompt': '#00ff00 bold'})
        
        # إعداد النماذج
        self.flash_model = genai.GenerativeModel(
            model_name=DEFAULT_MODEL,
            tools=list(self.tools.values()),
            system_instruction=SYSTEM_PROMPT
        )
        self.pro_model = genai.GenerativeModel(
            model_name=ADVANCED_MODEL,
            tools=list(self.tools.values()),
            system_instruction=SYSTEM_PROMPT
        )
        
        self.chat = self.flash_model.start_chat(enable_automatic_function_calling=True)

    def select_model(self, user_input):
        """نظام ذكي لاختيار النموذج بناءً على طول وتعقيد المدخلات"""
        complex_keywords = ["برمج", "كود", "حلل", "مشروع", "تطبيق", "بناء", "صمم"]
        is_complex = len(user_input.split()) > 20 or any(kw in user_input for kw in complex_keywords)
        
        if is_complex:
            console.print("[blue]ℹ️ تم تفعيل وضع الأداء العالي للمهمة المعقدة...[/blue]")
            return self.pro_model
        return self.flash_model

    def run(self):
        console.print(Panel.fit(
            "[bold green]Termux AI Agent (Gemini Edition)[/bold green]\n"
            "[cyan]تم التحديث لدعم Gemini مع إدارة ذكية للموارد.[/cyan]", 
            border_style="green"
        ))
        
        while True:
            try:
                user_input = prompt("Termux-AI > ", style=self.style)
                if user_input.lower() in ['exit', 'quit', 'خروج']:
                    break
                
                if not user_input.strip():
                    continue

                # اختيار النموذج المناسب للمهمة
                current_model = self.select_model(user_input)
                
                # إرسال الرسالة ومعالجة الرد تلقائياً (بفضل enable_automatic_function_calling)
                response = self.chat.send_message(user_input)
                
                # عرض الرد
                console.print(Markdown(response.text))

            except KeyboardInterrupt:
                break
            except Exception as e:
                if "429" in str(e):
                    console.print("[red]⚠️ تم تجاوز حد الاستهلاك المجاني. يرجى الانتظار قليلاً.[/red]")
                else:
                    console.print(f"[red]حدث خطأ: {e}[/red]")

if __name__ == "__main__":
    if not GEMINI_API_KEY:
        console.print("[red]❌ خطأ: لم يتم العثور على GEMINI_API_KEY في ملف .env[/red]")
    else:
        agent = TermuxAgent()
        agent.run()
