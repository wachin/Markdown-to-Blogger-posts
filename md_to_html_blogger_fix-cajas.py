import tkinter as tk
from tkinter import filedialog, ttk
import markdown
import re
from bs4 import BeautifulSoup
import os
import json

# Función para cargar la configuración
def load_config():
    default_config = {
        "code_box": '<pre class="linux-code" style="background: url(https://lh3.googleusercontent.com/-E2WZ-k5ArbU/VnnAeX-_qmI/AAAAAAAABDU/i1aaUUYLZh8/s540-Ic42/lincodewachin.gif) 0px 0px no-repeat scroll rgb(231, 232, 233); border-color: rgb(214, 73, 55); border-style: solid; border-width: 1px 1px 1px 20px; font-family: "UbuntuBeta Mono", "Ubuntu Mono", "Courier New", Courier, monospace; font-size: medium; line-height: 22.4px; margin: 10px; max-height: 500px; min-height: 16px; overflow: auto; padding: 28px 10px 10px; z-index: 10000;"><code>{code}</code></pre>'
    }
    try:
        with open('save.json', 'r') as f:
            content = f.read().strip()
            if not content:
                raise ValueError("El archivo está vacío.")
            return json.loads(content)
    except (FileNotFoundError, ValueError):
        with open('save.json', 'w') as f:
            json.dump(default_config, f)
        return default_config

# Clase para manejar la conversión de Markdown
def convert_markdown_to_blogger():
    class MarkdownConverter:
        def __init__(self, config):
            self.config = config

        def process_code_blocks(self, markdown_content):
            """Procesa los bloques de código con un manejo más robusto"""
            def extract_and_format_code(match):
                code = match.group(1).strip()
                lines = code.split('\n')
                formatted_lines = []

                for i, line in enumerate(lines):
                    line = line.rstrip()
                    line = (line.replace('&', '&amp;')
                               .replace('<', '&lt;')
                               .replace('>', '&gt;')
                               .replace('"', '&quot;')
                               .replace("'", '&#39;'))

                    if i < len(lines) - 1:
                        formatted_lines.append(f'{line}<br />')
                    else:
                        formatted_lines.append(line)

                code_content = '\n'.join(formatted_lines)
                return self.config["code_box"].format(code=code_content)

            code_block_pattern = re.compile(r'```(?:\w+)?\n(.*?)```', re.DOTALL)
            return code_block_pattern.sub(extract_and_format_code, markdown_content)

    input_file = input_entry.get()
    output_file = output_entry.get()

    with open(input_file, 'r', encoding='utf-8') as md_file:
        markdown_content = md_file.read()

    converter = MarkdownConverter({"code_box": code_box_entry.get()})

    if var_remove_code_tags.get():
        markdown_content = re.sub(r'```[a-zA-Z0-9]+\n', '```\n', markdown_content)

    markdown_content = converter.process_code_blocks(markdown_content)
    markdown_content = re.sub(r'`([^`]+)`', r'<b>\1</b>', markdown_content)

    html_content = markdown.markdown(markdown_content, extensions=['fenced_code', 'tables'])
    soup = BeautifulSoup(html_content, 'html.parser')

    if var_headers.get():
        for i in range(1, 7):
            for tag in soup.find_all(f'h{i}'):
                tag['style'] = "text-align: left;"

    if var_lists.get():
        for tag in soup.find_all(['ol', 'ul']):
            tag['style'] = "text-align: left;"

    modified_html = str(soup)

    if var_whitespace.get():
        modified_html = re.sub(r'>\s+<', '><', modified_html)

    with open(output_file, 'w', encoding='utf-8') as html_out:
        html_out.write(modified_html)

    status_label.config(text="Conversión completada")

# Configuración inicial de la GUI
root = tk.Tk()
root.title("Conversor de Markdown a HTML para Blogger")

input_label = tk.Label(root, text="Archivo de entrada (.md):")
input_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
input_entry = tk.Entry(root, width=50)
input_entry.grid(row=0, column=1, padx=5, pady=5)

output_label = tk.Label(root, text="Archivo de salida (.html):")
output_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
output_entry = tk.Entry(root, width=50)
output_entry.grid(row=1, column=1, padx=5, pady=5)

var_remove_code_tags = tk.BooleanVar(value=True)
var_headers = tk.BooleanVar(value=True)
var_lists = tk.BooleanVar(value=True)
var_whitespace = tk.BooleanVar(value=True)

convert_button = tk.Button(root, text="Convertir", command=convert_markdown_to_blogger)
convert_button.grid(row=2, column=1, pady=10)

status_label = tk.Label(root, text="")
status_label.grid(row=3, column=0, columnspan=2, pady=5)

root.mainloop()
