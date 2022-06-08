from rich.console import Console 
from rich.markdown import Markdown
from rich.padding import Padding
from rich.text import Text
from rich.panel import Panel

console = Console()

def print_header(text, style="bold white"):
    header = Panel(Text(text, justify="left"))
    console.print(header, style=style)

def print_step(text, style="bold red"):
    step = Padding(Markdown(text), 1)
    console.print(step, style=style)

def print_substep(text, style="bold blue"):
    console.print(text, style=style)

def print_error(text, style="bold red underline on white"):
    error = Padding(Markdown(text), 1)
    console.print(error, style=style)