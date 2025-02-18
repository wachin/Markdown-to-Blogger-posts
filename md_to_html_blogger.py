import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os
import json
import re
from bs4 import BeautifulSoup
import html

def load_config():
    default_config = {
        "code_box": '<pre class="linux-code" style="background: rgb(231, 232, 233); border-color: rgb(214, 73, 55); border-style: solid; border-width: 1px 1px 1px 20px; font-family: &quot;UbuntuBeta Mono&quot;, &quot;Ubuntu Mono&quot;, &quot;Courier New&quot;, Courier, monospace; font-size: medium; line-height: 22.4px; margin: 10px; max-height: 500px; min-height: 16px; overflow: auto; padding: 28px 10px 10px 20px; z-index: 10000;"><code>{code}</code></pre>'
    }
    try:
        with open('save.json', 'r') as f:
            content = f.read().strip()
            return json.loads(content) if content else default_config
    except (FileNotFoundError, json.JSONDecodeError):
        with open('save.json', 'w') as f:
            json.dump(default_config, f)
        return default_config

def save_config():
    config = {"code_box": code_box_entry.get()}
    with open('save.json', 'w') as f:
        json.dump(config, f)
    messagebox.showinfo("Configuración", "Configuración guardada correctamente.")

def select_input_file():
    file_path = filedialog.askopenfilename(filetypes=[("Markdown files", "*.md")])
    if file_path:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, file_path)
        output_entry.delete(0, tk.END)
        output_entry.insert(0, os.path.splitext(file_path)[0] + ".html")

def select_output_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML files", "*.html")])
    if file_path:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, file_path)

def remove_code_language_tags(md_content):
    if var_remove_code_tags.get():
        return re.sub(r'```[a-zA-Z0-9]+\n', '```\n', md_content)
    return md_content

def cleanup_html(html_content):
    html_content = re.sub(r'<p>(\s*<pre.*?</pre>\s*)</p>', r'\1', html_content)
    html_content = re.sub(r'(</pre>)(?!\s*<p>)', r'\1<p></p>', html_content)
    html_content = re.sub(r'<p>\s*</p>', '', html_content)
    if var_whitespace.get():
        html_content = re.sub(r'>\s+<', '><', html_content)
    return html_content

def replace_code_block(match, code_box_template):
    code_content = html.escape(match.group(1).strip())
    code_content = code_content.replace('\n', '<br />')
    return code_box_template.replace("{code}", code_content)

def convert_bold_and_italic(text):
    text = re.sub(r'\*\*(\S.*?\S)\*\*', r'<b>\1</b>', text, flags=re.DOTALL)
    text = re.sub(r'\*(\S.*?\S)\*', r'<em>\1</em>', text)
    text = re.sub(r'`(.*?)`', r'<b>\1</b>', text)
    return text

def convert_headers_to_html(md_content):
    def header_replacement(match):
        level = len(match.group(1))
        text = html.escape(match.group(2).strip())
        text = convert_bold_and_italic(text)
        return f'<h{level} style="text-align: left;">{text}<br /></h{level}>'
    return re.sub(r'^(#{1,6})\s+(.+)$', header_replacement, md_content, flags=re.MULTILINE)

def convert_md_lists_and_paragraphs(content):
    blocks = re.split(r'\n\s*\n', content)
    html_output = []
    
    for block in blocks:
        if re.match(r'^(\s*[\*\-+] .*?(\n\s*[\*\-+] .*?)*)$', block, re.MULTILINE):
            html_output.append('<ul style="text-align: left;">')
            for line in block.split('\n'):
                if line.strip():
                    cleaned_line = line.lstrip("*\-+ ").strip()
                    html_output.append(f'<li>{convert_bold_and_italic(cleaned_line)}</li>')
            html_output.append('</ul>')
        elif re.match(r'^(\s*\d+\. .*?(\n\s*\d+\. .*?)*)$', block, re.MULTILINE):
            html_output.append('<ol style="text-align: left;">')
            for line in block.split('\n'):
                if line.strip():
                    cleaned_line = re.sub(r'^\d+\.\s*', "", line).strip()
                    html_output.append(f'<li>{convert_bold_and_italic(cleaned_line)}</li>')
            html_output.append('</ol>')
        else:
            paragraph_lines = []
            for raw_line in block.split('\n'):
                line = raw_line.rstrip('\n')
                if line.endswith('  '):
                    processed_line = line.rstrip(' ') + '<br />'
                else:
                    processed_line = line
                processed_line = convert_bold_and_italic(processed_line.strip())
                if processed_line:
                    paragraph_lines.append(processed_line)
            if paragraph_lines:
                para_content = ' '.join(paragraph_lines)
                html_output.append(f'<p>&nbsp;{para_content}</p>')
    
    return '\n'.join(html_output)

def convert_markdown_table_to_html(md_content):
    table_pattern = re.compile(
        r'(\n|^)([^\n]*\|[^\n]*\n)([^\n]*\|[^\n]*\n)((?:\s*\|.*\|?\s*\n)*)',
        re.MULTILINE
    )
    
    def format_table(match):
        full_table = match.group(0).strip()
        rows = [row.strip() for row in full_table.split('\n') if row.strip()]
        if len(rows) < 2:
            return match.group(0)
            
        table_html = [
            '<table style="border-collapse: collapse; width: 100%;">',
            '<thead><tr style="background-color: #f2f2f2;">'
        ]
        
        headers = [cell.strip() for cell in rows[0].split('|') if cell.strip()]
        table_html.extend(
            f'<th style="border: 1px solid #ddd; padding: 8px; text-align: left;">{html.escape(cell)}</th>'
            for cell in headers
        )
        table_html.append('</tr></thead><tbody>')

        for i, row in enumerate(rows[2:]):
            cells = [cell.strip() for cell in row.split('|') if cell.strip()]
            if not cells:
                continue
                
            bg_color = "#ffffff" if i % 2 == 0 else "#f2f2f2"
            table_html.append(f'<tr style="background-color: {bg_color};">')
            for cell in cells:
                content = convert_bold_and_italic(html.escape(cell))
                table_html.append(f'<td style="border: 1px solid #ddd; padding: 8px; text-align: left;">{content}</td>')
            table_html.append('</tr>')

        table_html.append('</tbody></table>')
        return ''.join(table_html)

    return table_pattern.sub(format_table, md_content)

def convert_markdown_to_blogger():
    input_file = input_entry.get()
    output_file = output_entry.get()

    if not input_file or not output_file:
        messagebox.showerror("Error", "Por favor, selecciona los archivos de entrada y salida.")
        return

    try:
        with open(input_file, 'r', encoding='utf-8') as md_file:
            markdown_content = md_file.read()

        config = load_config()
        code_box_template = config["code_box"]

        # Process code blocks first
        code_blocks = []
        def save_code_block(match):
            code_blocks.append(match.group(0))
            return f"CODE_BLOCK_{len(code_blocks)-1}"
        markdown_content = re.sub(r'```(.*?)```', save_code_block, markdown_content, flags=re.DOTALL)
        markdown_content = remove_code_language_tags(markdown_content)

        # Processing order: Tables -> Headers -> Lists/Paragraphs
        content_with_tables = convert_markdown_table_to_html(markdown_content)
        content_with_headers = convert_headers_to_html(content_with_tables)
        content_with_lists = convert_md_lists_and_paragraphs(content_with_headers)

        # Restore code blocks
        html_content = content_with_lists
        for i, block in enumerate(code_blocks):
            code_content = block.strip('`').strip()
            if var_remove_code_tags.get():
                code_content = re.sub(r'^[a-zA-Z0-9]+\n', '', code_content)
            formatted_block = replace_code_block(re.match(r'(.*)', code_content, re.DOTALL), code_box_template)
            html_content = html_content.replace(f"CODE_BLOCK_{i}", formatted_block)

        # Process tables with proper wrapper
        soup = BeautifulSoup(html_content, 'html.parser')
        for table in soup.find_all('table'):
            wrapper = soup.new_tag('pre', **{
                "class": "table-code-box",
                "style": "background-color: #f9f9f9; padding: 10px; border: 1px solid #ddd; overflow-x: auto;"
            })
            table.insert_before(wrapper)
            wrapper.append(table.extract())

        html_content = str(soup)
        html_content = cleanup_html(html_content)

        if var_line_breaks.get():
            html_content += '<p><br /></p><p><br /></p>'

        with open(output_file, 'w', encoding='utf-8') as html_out:
            html_out.write(html_content)

        messagebox.showinfo("Éxito", "La conversión se completó correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

# GUI Setup
root = tk.Tk()
root.title("Conversor de Markdown a HTML")

# Input file selection
input_label = tk.Label(root, text="Archivo de entrada (.md):")
input_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
input_entry = tk.Entry(root, width=50)
input_entry.grid(row=0, column=1, padx=5, pady=5)
input_button = tk.Button(root, text="Seleccionar", command=select_input_file)
input_button.grid(row=0, column=2, padx=5, pady=5)

# Output file selection
output_label = tk.Label(root, text="Archivo de salida (.html):")
output_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
output_entry = tk.Entry(root, width=50)
output_entry.grid(row=1, column=1, padx=5, pady=5)
output_button = tk.Button(root, text="Seleccionar", command=select_output_file)
output_button.grid(row=1, column=2, padx=5, pady=5)

# Options checkboxes
options_frame = tk.LabelFrame(root, text="Opciones", padx=10, pady=10)
options_frame.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="we")

var_headers = tk.BooleanVar(value=True)
var_whitespace = tk.BooleanVar(value=True)
var_paragraph_space = tk.BooleanVar(value=True)
var_line_breaks = tk.BooleanVar(value=True)
var_remove_code_tags = tk.BooleanVar(value=True)

check_headers = tk.Checkbutton(options_frame, text="Modificar encabezados con text-align: left", variable=var_headers)
check_headers.pack(anchor="w")
check_whitespace = tk.Checkbutton(options_frame, text="Eliminar espacios entre etiquetas", variable=var_whitespace)
check_whitespace.pack(anchor="w")
check_paragraph_space = tk.Checkbutton(options_frame, text="Espacio no separable en párrafos", variable=var_paragraph_space)
check_paragraph_space.pack(anchor="w")
check_line_breaks = tk.Checkbutton(options_frame, text="Añadir saltos de línea finales", variable=var_line_breaks)
check_line_breaks.pack(anchor="w")
check_remove_code_tags = tk.Checkbutton(options_frame, text="Borrar etiquetas de código", variable=var_remove_code_tags)
check_remove_code_tags.pack(anchor="w")

# Code box configuration
code_box_label = tk.Label(root, text="Formato de caja de código:")
code_box_label.grid(row=3, column=0, sticky="w", padx=5, pady=5)
code_box_entry = tk.Entry(root, width=50)
code_box_entry.grid(row=3, column=1, padx=5, pady=5)
config = load_config()
code_box_entry.insert(0, config["code_box"])

# Save and convert buttons
save_button = tk.Button(root, text="Guardar configuración", command=save_config)
save_button.grid(row=3, column=2, padx=5, pady=5)
convert_button = tk.Button(root, text="Convertir", command=convert_markdown_to_blogger)
convert_button.grid(row=4, column=0, columnspan=3, pady=10)

root.mainloop()
