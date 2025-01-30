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
            if not content:
                raise ValueError("El archivo está vacío.")
            return json.loads(content)
    except (FileNotFoundError, ValueError):
        with open('save.json', 'w') as f:
            json.dump(default_config, f)
        return default_config

# Función para guardar la configuración
def save_config():
    config = {"code_box": code_box_entry.get()}
    with open('save.json', 'w') as f:
        json.dump(config, f)
    messagebox.showinfo("Configuración", "Configuración guardada correctamente.")

# Función para seleccionar un archivo de entrada
def select_input_file():
    file_path = filedialog.askopenfilename(filetypes=[("Markdown files", "*.md")])
    if file_path:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, file_path)
        output_entry.delete(0, tk.END)
        output_entry.insert(0, os.path.splitext(file_path)[0] + ".html")

# Función para seleccionar un archivo de salida
def select_output_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML files", "*.html")])
    if file_path:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, file_path)

# Esta función borra los tags de las cajas de código
def remove_code_language_tags(md_content):
    if var_remove_code_tags.get():
        return re.sub(r'```[a-zA-Z0-9]+\n', '```\n', md_content)
    return md_content

# Agregada la función cleanup_html() para arreglar código alrededor de los bloques de cajas código <pre>
def cleanup_html(html_content):
    # Eliminar <p> alrededor de los bloques <pre>
    html_content = re.sub(r'<p>(\s*<pre.*?</pre>\s*)</p>', r'\1', html_content)
    # Asegurar que hay un <p></p> vacío después de cada <pre>
    html_content = re.sub(r'(</pre>)(?!\s*<p>)', r'\1<p></p>', html_content)
    # Eliminar espacios extra entre etiquetas
    if var_whitespace.get():
        html_content = re.sub(r'>\s+<', '><', html_content)
    return html_content

# Función para convertir listas en el contenido Markdown
def convert_lists_to_html(md_content):
    lines = md_content.splitlines()
    html_lines = []
    in_ul = False
    in_ol = False

    for line in lines:
        line = line.rstrip()

        if re.match(r'^\s*[-*]\s+', line):
            if not in_ul:
                if in_ol:
                    html_lines.append('</ol>')
                    in_ol = False
                html_lines.append('<ul style="text-align: left;">')
                in_ul = True
            html_lines.append(f'<li>{line.lstrip("-* ")}</li>')
        elif re.match(r'^\s*\d+\.\s+', line):
            if not in_ol:
                if in_ul:
                    html_lines.append('</ul>')
                    in_ul = False
                html_lines.append('<ol style="text-align: left;">')
                in_ol = True
            html_lines.append(f'<li>{line.lstrip("0123456789. ")}</li>')
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

# Función para reemplazar bloques de cajas de código
def replace_code_block(match, code_box_template):
    code_content = html.escape(match.group(1).strip())
    # Reemplazar los saltos de línea con <br />
    code_content = code_content.replace('\n', '<br />')
    # Asegurar que las líneas que terminan con \ también tengan <br />
    code_content = code_content.replace('\\<br />', '\\<br />')
    formatted_code = code_box_template.replace("{code}", code_content)
    return formatted_code

def convert_bold_and_italic(text):
    # Convertir texto en negrita (doble asterisco) a <b> en lugar de <strong>
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    # Convertir texto en cursiva (un asterisco)
    text = re.sub(r'\*([^\*]+)\*', r'<em>\1</em>', text)
    return text

# Función para convertir encabezados markdown a html
def convert_headers_to_html(md_content):
    def header_replacement(match):
        level = len(match.group(1))
        text = html.escape(match.group(2).strip())
        # Aplicar negrita y cursiva al texto del encabezado
        text = convert_bold_and_italic(text)
        return f'<h{level} style="text-align: left;">{text}<br /></h{level}>'

    return re.sub(r'^(#{1,6})\s+(.+)$', header_replacement, md_content, flags=re.MULTILINE)

def convert_text_to_paragraphs(content):
    # Dividir el contenido en líneas
    lines = content.split('\n')
    processed_lines = []
    current_paragraph = []
    
    for line in lines:
        # Si la línea está vacía y tenemos contenido en el párrafo actual
        if not line.strip() and current_paragraph:
            # Unir las líneas del párrafo actual con <br />
            paragraph_content = '<br />'.join(map(convert_bold_and_italic, current_paragraph))
            processed_lines.append(f'<p>{paragraph_content}</p>')
            current_paragraph = []
        # Si la línea no está vacía y no es un encabezado
        elif line.strip() and not line.strip().startswith('#'):
            current_paragraph.append(line.strip())
    
    # Procesar el último párrafo si existe
    if current_paragraph:
        paragraph_content = '<br />'.join(map(convert_bold_and_italic, current_paragraph))
        processed_lines.append(f'<p>{paragraph_content}</p>')
    
    return '\n'.join(processed_lines)

# Función para aplicar modificaciones finales al HTML
def apply_final_modifications(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    if var_headers.get():
        for i in range(1, 7):
            for tag in soup.find_all(f'h{i}'):
                tag['style'] = "text-align: left;"

    if var_lists.get():
        for tag in soup.find_all(['ol', 'ul']):
            tag['style'] = "text-align: left;"

    if var_whitespace.get():
        html_content = re.sub(r'>\s+<', '><', str(soup))

    if var_paragraph_space.get():
        html_content = re.sub(r'<p>', '<p>&nbsp;', html_content)

    if var_line_breaks.get():
        html_content += '<p><br /></p><p><br /></p>'

    return html_content

# Función para realizar la conversión
def convert_markdown_to_blogger():
    input_file = input_entry.get()
    output_file = output_entry.get()

    if not input_file or not output_file:
        messagebox.showerror("Error", "Por favor, selecciona los archivos de entrada y salida.")
        return

    try:
        with open(input_file, 'r', encoding='utf-8') as md_file:
            markdown_content = md_file.read()

        # Cargar la configuración para las cajas de código
        config = load_config()
        code_box_template = config["code_box"]

        # Almacenar los bloques de código temporalmente
        code_blocks = []
        def save_code_block(match):
            code_blocks.append(match.group(0))
            return f"CODE_BLOCK_{len(code_blocks)-1}"

        # Guardar los bloques de código y reemplazarlos con marcadores
        markdown_content = re.sub(r'```(.*?)```', save_code_block, markdown_content, flags=re.DOTALL)

        # Remover etiquetas de lenguaje si está activada la opción
        markdown_content = remove_code_language_tags(markdown_content)

        # Convertir encabezados
        content_with_headers = convert_headers_to_html(markdown_content)

        # Función para convertir tablas Markdown a HTML
        def convert_markdown_table_to_html(md_content):
            table_pattern = re.compile(
                r'(?:^|\n)\|(.+?)\|\n\|([ \-:|]+)\|\n((?:\|.*?\|\n)+)',  # Tabla con encabezados, separadores y filas
                re.MULTILINE
            )

            def format_table(match):
                header = match.group(1).split('|')
                separator = match.group(2)
                rows = [row.split('|') for row in match.group(3).strip().split('\n')]

                thead = '<thead><tr style="background-color: #f2f2f2;">' + ''.join(
                    f'<th style="border: 1px solid #ddd; padding: 8px; text-align: left;">{html.escape(cell.strip())}</th>'
                    for cell in header
                ) + '</tr></thead>'

                tbody = '<tbody>' + ''.join(
                    f'<tr style="background-color: {"#f2f2f2" if i % 2 == 0 else "#ffffff"};">' +
                    ''.join(
                        f'<td style="border: 1px solid #ddd; padding: 8px; text-align: left;">{html.escape(cell.strip())}</td>'
                        for cell in row
                    ) + '</tr>'
                    for i, row in enumerate(rows)
                ) + '</tbody>'

                return f'<table style="border-collapse: collapse; width: 100%;">{thead}{tbody}</table>'

            return table_pattern.sub(format_table, md_content)

        # Convertir tablas Markdown a HTML
        content_with_tables = convert_markdown_table_to_html(content_with_headers)

        # Separar el contenido en secciones (entre encabezados)
        sections = re.split(r'(<h[1-6].*?</h[1-6]>)', content_with_tables)

        # Procesar cada sección
        processed_sections = []
        for section in sections:
            if section.strip():
                if section.startswith('<h'):
                    processed_sections.append(section)
                else:
                    processed_sections.append(convert_text_to_paragraphs(section))

        # Unir todo el contenido
        html_content = ''.join(processed_sections)

        # Restaurar los bloques de código
        for i, block in enumerate(code_blocks):
            # Eliminar los marcadores de código y procesar el contenido
            code_content = block.strip('`').strip()
            if var_remove_code_tags.get():
                code_content = re.sub(r'^[a-zA-Z0-9]+\n', '', code_content)
            formatted_block = replace_code_block(re.match(r'(.*)', code_content, re.DOTALL), code_box_template)
            html_content = html_content.replace(f"CODE_BLOCK_{i}", formatted_block)

        # Procesar tablas en el HTML con estilos adicionales
        soup = BeautifulSoup(html_content, 'html.parser')
        for table in soup.find_all('table'):
            # Envolver la tabla en un bloque desplazable para facilitar la visualización.
            wrapper = soup.new_tag('pre', **{
                "class": "table-code-box",
                "style": "background-color: #f9f9f9; padding: 10px; border: 1px solid #ddd; overflow-x: auto;"
            })
            table.insert_before(wrapper)
            wrapper.append(table.extract())

        html_content = str(soup)

        # Limpiar el HTML
        html_content = cleanup_html(html_content)

        # Agregar saltos de línea finales si está activada la opción
        if var_line_breaks.get():
            html_content += '<p><br /></p><p><br /></p>'

        with open(output_file, 'w', encoding='utf-8') as html_out:
            html_out.write(html_content)

        messagebox.showinfo("Éxito", "La conversión se completó correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

# Crear la ventana principal
root = tk.Tk()
root.title("Conversor de Markdown a HTML")

# Widgets para seleccionar archivo de entrada
input_label = tk.Label(root, text="Archivo de entrada (.md):")
input_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
input_entry = tk.Entry(root, width=50)
input_entry.grid(row=0, column=1, padx=5, pady=5)
input_button = tk.Button(root, text="Seleccionar", command=select_input_file)
input_button.grid(row=0, column=2, padx=5, pady=5)

# Widgets para seleccionar archivo de salida
output_label = tk.Label(root, text="Archivo de salida (.html):")
output_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
output_entry = tk.Entry(root, width=50)
output_entry.grid(row=1, column=1, padx=5, pady=5)
output_button = tk.Button(root, text="Seleccionar", command=select_output_file)
output_button.grid(row=1, column=2, padx=5, pady=5)

# Casillas de verificación
options_frame = tk.LabelFrame(root, text="Opciones", padx=10, pady=10)
options_frame.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="we")

var_headers = tk.BooleanVar(value=True)
var_lists = tk.BooleanVar(value=True)
var_whitespace = tk.BooleanVar(value=True)
var_paragraph_space = tk.BooleanVar(value=True)
var_line_breaks = tk.BooleanVar(value=True)
var_remove_code_tags = tk.BooleanVar(value=True)

check_headers = tk.Checkbutton(options_frame, text="Modificar los encabezados añadiendo el estilo text-align: left", variable=var_headers)
check_headers.pack(anchor="w")
check_lists = tk.Checkbutton(options_frame, text="Modificar las listas ordenadas y no ordenadas añadiendo el estilo text-align: left", variable=var_lists)
check_lists.pack(anchor="w")
check_whitespace = tk.Checkbutton(options_frame, text="Eliminar espacios en blanco entre etiquetas para que sea un código continuo", variable=var_whitespace)
check_whitespace.pack(anchor="w")
check_paragraph_space = tk.Checkbutton(options_frame, text="Agregar un espacio no separable al principio de cada párrafo", variable=var_paragraph_space)
check_paragraph_space.pack(anchor="w")
check_line_breaks = tk.Checkbutton(options_frame, text="Agregar dos saltos de línea al final del contenido", variable=var_line_breaks)
check_line_breaks.pack(anchor="w")
check_remove_code_tags = tk.Checkbutton(options_frame, text="Borrar las etiquetas de las cajas de código", variable=var_remove_code_tags)
check_remove_code_tags.pack(anchor="w")

# Entrada para configurar el formato de la caja de código
code_box_label = tk.Label(root, text="Formato de caja de código:")
code_box_label.grid(row=3, column=0, sticky="w", padx=5, pady=5)
code_box_entry = tk.Entry(root, width=50)
code_box_entry.grid(row=3, column=1, padx=5, pady=5)
config = load_config()
code_box_entry.insert(0, config["code_box"])

# Botón para guardar la configuración
save_button = tk.Button(root, text="Guardar configuración", command=save_config)
save_button.grid(row=3, column=2, padx=5, pady=5)

# Botón para realizar la conversión
convert_button = tk.Button(root, text="Convertir", command=convert_markdown_to_blogger)
convert_button.grid(row=4, column=0, columnspan=3, pady=10)

root.mainloop()
