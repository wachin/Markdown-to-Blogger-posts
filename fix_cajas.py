import tkinter as tk
from tkinter import filedialog, ttk
import markdown
import re
from bs4 import BeautifulSoup
import os
import json

# [Previous imports and configuration loading remain the same...]

class MarkdownConverter:
    def __init__(self, config):
        self.config = config
        
    def process_code_blocks(self, markdown_content):
        """Procesa los bloques de código con un manejo más robusto"""
        def extract_and_format_code(match):
            code = match.group(1).strip()
            # Preservar los saltos de línea y espacios exactos
            lines = code.split('\n')
            formatted_lines = []
            
            for i, line in enumerate(lines):
                line = line.rstrip()
                # Escapar caracteres especiales HTML
                line = (line.replace('&', '&amp;')
                           .replace('<', '&lt;')
                           .replace('>', '&gt;')
                           .replace('"', '&quot;')
                           .replace("'", '&#39;'))
                
                if line.endswith('\\'):
                    formatted_lines.append(f'{line}<br />')
                else:
                    if i < len(lines) - 1:  # No es la última línea
                        formatted_lines.append(f'{line}<br />')
                    else:  # Última línea
                        formatted_lines.append(line)
            
            code_content = '\n'.join(formatted_lines)
            return self.config["code_box"].format(code=code_content)

        # Procesar bloques de código
        code_block_pattern = re.compile(r'```(?:\w+)?\n(.*?)```', re.DOTALL)
        return code_block_pattern.sub(extract_and_format_code, markdown_content)

def convert_markdown_to_blogger():
    input_file = input_entry.get()
    output_file = output_entry.get()

    with open(input_file, 'r', encoding='utf-8') as md_file:
        markdown_content = md_file.read()

    # Inicializar el convertidor con la configuración actual
    converter = MarkdownConverter({"code_box": code_box_entry.get()})

    # Eliminar etiquetas de lenguaje si está activada la opción
    if var_remove_code_tags.get():
        markdown_content = re.sub(r'```[a-zA-Z0-9]+\n', '```\n', markdown_content)

    # Convertir listas manualmente
    def convert_lists_to_html(md_content):
        lines = md_content.splitlines()
        html_lines = []
        in_ul = False
        in_ol = False

        for line in lines:
            line = line.rstrip()
            
            # Ignorar líneas dentro de bloques de código
            if '```' in line:
                html_lines.append(line)
                continue

            if re.match(r'^\s*[-*]\s+', line):
                if not in_ul:
                    if in_ol:
                        html_lines.append('</ol>')
                        in_ol = False
                    html_lines.append('<ul style="text-align: left;">')
                    in_ul = True
                html_lines.append(f'<li>{line.lstrip("- *").strip()}</li>')
            elif re.match(r'^\s*\d+\.\s+', line):
                if not in_ol:
                    if in_ul:
                        html_lines.append('</ul>')
                        in_ul = False
                    html_lines.append('<ol style="text-align: left;">')
                    in_ol = True
                html_lines.append(f'<li>{re.sub(r"^\s*\d+\.\s+", "", line).strip()}</li>')
            else:
                if in_ul:
                    html_lines.append('</ul>')
                    in_ul = False
                if in_ol:
                    html_lines.append('</ol>')
                    in_ol = False
                html_lines.append(line)

        if in_ul:
            html_lines.append('</ul>')
        if in_ol:
            html_lines.append('</ol>')

        return '\n'.join(html_lines)

    # Procesar el contenido en el orden correcto
    markdown_content = convert_lists_to_html(markdown_content)
    
    # Procesar bloques de código
    markdown_content = converter.process_code_blocks(markdown_content)
    
    # Convertir inline code
    markdown_content = re.sub(r'`([^`]+)`', r'<b>\1</b>', markdown_content)
    
    # Convertir el resto del markdown
    html_content = markdown.markdown(markdown_content, extensions=['fenced_code', 'tables'])

    # Procesar con BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # [Rest of the table processing and styling code remains the same...]

    # Aplicar estilos adicionales según las configuraciones seleccionadas
    if var_headers.get():
        for i in range(1, 7):
            for tag in soup.find_all(f'h{i}'):
                tag['style'] = "text-align: left;"

    if var_lists.get():
        for tag in soup.find_all(['ol', 'ul']):
            tag['style'] = "text-align: left;"

    if var_blockquotes.get():
        for tag in soup.find_all('blockquote'):
            tag.insert_before(soup.new_tag('p'))
            tag.insert_after(soup.new_tag('p'))

    modified_html = str(soup)

    if var_whitespace.get():
        modified_html = re.sub(r'>\s+<', '><', modified_html)

    if var_paragraph_space.get():
        modified_html = re.sub(r'<p>', '<p>&nbsp;', modified_html)

    if var_line_breaks.get():
        modified_html += '<p><br /></p><p><br /></p>'

    with open(output_file, 'w', encoding='utf-8') as html_out:
        html_out.write(modified_html)

    status_label.config(text="Conversión completada")

# [Rest of the GUI code remains the same...]
