import json
from openai import OpenAI
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from prompt_toolkit import prompt
from prompt_toolkit.styles import Style
from config import API_KEY, MODEL_NAME, SYSTEM_PROMPT
from tools import execute_shell, read_file, write_file, TOOLS_DEFINITION

console = Console()
client = OpenAI(api_key=API_KEY)

class TermuxAgent:
    def __init__(self):
        self.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        self.style = Style.from_dict({
            'prompt': '#00ff00 bold',
        })

    def call_llm(self):
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=self.messages,
                tools=TOOLS_DEFINITION,
                tool_choice="auto"
            )
            return response.choices[0].message
        except Exception as e:
            console.print(f"[red]خطأ في الاتصال بالنموذج: {e}[/red]")
            return None

    def handle_tool_calls(self, tool_calls):
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            
            console.print(f"[yellow]جاري تنفيذ الأداة: {function_name}...[/yellow]")
            
            if function_name == "execute_shell":
                result = execute_shell(arguments.get("command"))
            elif function_name == "read_file":
                result = read_file(arguments.get("path"))
            elif function_name == "write_file":
                result = write_file(arguments.get("path"), arguments.get("content"))
            elif function_name == "search_web":
                result = search_web(arguments.get("query"))
            elif function_name == "get_termux_info":
                result = get_termux_info()
            else:
                result = "أداة غير معروفة"

            self.messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": function_name,
                "content": str(result)
            })

    def run(self):
        console.print(Panel.fit("[bold green]Termux AI Agent[/bold green]\n[cyan]مرحباً بك! أنا مساعدك الذكي في تيرمكس.[/cyan]", border_style="green"))
        
        while True:
            try:
                user_input = prompt("Termux-AI > ", style=self.style)
                if user_input.lower() in ['exit', 'quit', 'خروج']:
                    break
                
                if not user_input.strip():
                    continue

                self.messages.append({"role": "user", "content": user_input})
                
                while True:
                    response_message = self.call_llm()
                    if not response_message:
                        break

                    self.messages.append(response_message)

                    if response_message.tool_calls:
                        self.handle_tool_calls(response_message.tool_calls)
                    else:
                        console.print(Markdown(response_message.content or ""))
                        break

            except KeyboardInterrupt:
                break
            except Exception as e:
                console.print(f"[red]حدث خطأ غير متوقع: {e}[/red]")

if __name__ == "__main__":
    agent = TermuxAgent()
    agent.run()
