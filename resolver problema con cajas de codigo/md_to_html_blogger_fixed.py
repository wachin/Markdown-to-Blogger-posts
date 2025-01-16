import tkinter as tk
from tkinter import filedialog, ttk
import markdown
import re
from bs4 import BeautifulSoup
import os
import json
from typing import List, Tuple


# Función para cargar la configuración
# Esta función verifica si existe un archivo de configuración llamado 'save.json'.
# Si no existe o está vacío, crea uno con valores predeterminados.
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

# Función para guardar la configuración
# Toma el valor de una entrada de texto en la interfaz y lo guarda en 'save.json'.
def save_config():
    config = {"code_box": code_box_entry.get()}
    with open('save.json', 'w') as f:
        json.dump(config, f)
    status_label.config(text="Configuración guardada")

# Cargar la configuración inicial
config = load_config()

def select_input_file():
    # Permite al usuario seleccionar un archivo Markdown de entrada.
    initial_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Conversiones")
    file_path = filedialog.askopenfilename(
        initialdir=initial_dir,
        filetypes=[("Markdown files", "*.md")]
    )
    if file_path:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, file_path)

        # Autogenera el nombre del archivo de salida con extensión .html
        output_path = os.path.splitext(file_path)[0] + ".html"
        output_entry.delete(0, tk.END)
        output_entry.insert(0, output_path)

def select_output_file():
    # Permite al usuario seleccionar la ubicación y el nombre del archivo HTML de salida.
    initial_file = output_entry.get()
    file_path = filedialog.asksaveasfilename(
        initialfile=os.path.basename(initial_file),
        defaultextension=".html",
        filetypes=[("HTML files", "*.html")]
    )
    if file_path:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, file_path)

def convert_markdown_to_blogger():
    # Convierte el contenido de un archivo Markdown a HTML estilizado para Blogger.
    input_file = input_entry.get()
    output_file = output_entry.get()

    with open(input_file, 'r', encoding='utf-8') as md_file:
        markdown_content = md_file.read()

    # Opción para eliminar etiquetas de lenguajes en bloques de código
    def remove_code_language_tags(md_content):
        if var_remove_code_tags.get():
            # Busca bloques de código con etiquetas y las elimina.
            return re.sub(r'```[a-zA-Z0-9]+\n', '```\n', md_content)
        return md_content

    markdown_content = remove_code_language_tags(markdown_content)

    # Detectar y convertir listas en el Markdown manualmente
    def convert_lists_to_html(md_content):
        # Convierte listas no ordenadas y ordenadas en HTML usando etiquetas <ul>, <ol>, <li>.
        lines = md_content.splitlines()
        html_lines = []
        in_ul = False
        in_ol = False

        for line in lines:
            line = line.rstrip()

            if re.match(r'^\s*[-*]\s+', line):  # Detectar listas no ordenadas
                if not in_ul:
                    if in_ol:
                        html_lines.append('</ol>')
                        in_ol = False
                    html_lines.append('<ul style="text-align: left;">')
                    in_ul = True
                html_lines.append(f'<li>{line.lstrip("- *")}</li>')
            elif re.match(r'^\s*\d+\.\s+', line):  # Detectar listas ordenadas
                if not in_ol:
                    if in_ul:
                        html_lines.append('</ul>')
                        in_ul = False
                    html_lines.append('<ol style="text-align: left;">')
                    in_ol = True
                html_lines.append(f'<li>{line.lstrip("0123456789.")}</li>')
            else:
                # Cierra las listas si se encuentra con una línea que no es parte de ellas.
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

    markdown_content = convert_lists_to_html(markdown_content)
    
    
    def extract_code_blocks(self, text: str) -> List[Tuple[str, str]]:
        """
        Extrae los bloques de código y los reemplaza con marcadores únicos.
        Retorna una lista de tuplas (marcador, contenido del código).
        """
        code_blocks = []
        pattern = r'```(?:\w+)?\n(.*?)```'
        
        def replacement(match):
            marker = f'__CODE_BLOCK_{len(code_blocks)}__'
            # Eliminar la última línea vacía si existe
            code_content = match.group(1).rstrip()
            code_blocks.append((marker, code_content))
            return marker
        
        processed_text = re.sub(pattern, replacement, text, flags=re.DOTALL)
        return processed_text, code_blocks

    def convert_paragraphs(self, text: str) -> str:
        """Convierte párrafos de texto normal."""
        paragraphs = text.split('\n\n')
        converted = []
        
        for p in paragraphs:
            if p.strip() and not p.startswith('__CODE_BLOCK_'):
                converted.append(f'<p>{p.strip()}</p>')
            else:
                converted.append(p)
                
        return '\n'.join(converted)

    def format_code_block(self, code_content: str) -> str:
        """Formatea un bloque de código en HTML con el estilo apropiado."""
        # Dividir las líneas y mantener la continuación de línea
        lines = code_content.split('\n')
        formatted_lines = []
        
        for i, line in enumerate(lines):
            line = line.rstrip()
            if line.endswith('\\'):
                formatted_lines.append(f'<code>{line}<br /></code>')
            else:
                if i < len(lines) - 1:  # No es la última línea
                    formatted_lines.append(f'<code>{line}<br /></code>')
                else:  # Última línea
                    formatted_lines.append(f'<code>{line}</code>')
        
        return f'<pre class="linux-code" style="{self.code_block_style}">' + \
               ''.join(formatted_lines) + '</pre>'    

        html_content = markdown.markdown(markdown_content, extensions=['fenced_code', 'tables'])

        soup = BeautifulSoup(html_content, 'html.parser')

    # Procesar tablas
    for table in soup.find_all('table'):
        # Aplica estilos a las tablas generadas en HTML.
        table['style'] = "border-collapse: collapse; width: 100%;"
        for i, row in enumerate(table.find_all('tr')):
            row['style'] = "background-color: #f2f2f2;" if i % 2 == 0 else "background-color: #ffffff;"
        for cell in table.find_all(['th', 'td']):
            cell['style'] = "border: 1px solid #ddd; padding: 8px; text-align: left;"

        # Envolver la tabla en un bloque desplazable para facilitar la visualización.
        wrapper = soup.new_tag('pre', **{
            "class": "table-code-box",
            "style": "background-color: #f9f9f9; padding: 10px; border: 1px solid #ddd; overflow-x: auto;"
        })
        table.insert_before(wrapper)
        wrapper.append(table.extract())

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

class AboutWindow(tk.Toplevel):
    # Ventana "Acerca de"
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Acerca de md to html Blogger")
        self.geometry("420x450")
        self.resizable(False, False)

        text = tk.Text(self, wrap=tk.WORD, padx=10, pady=10, relief=tk.FLAT)
        text.pack(expand=True, fill=tk.BOTH)

        text.tag_configure("bold", font=("TkDefaultFont", 10, "bold"))
        text.tag_configure("italic", font=("TkDefaultFont", 10, "italic"))

        text.insert(tk.END, "md to html Blogger\n\n", "bold")
        text.insert(tk.END, "Una ")
        text.insert(tk.END, "GUI ", "italic")
        text.insert(tk.END, "para convertir archivos markdown (.md) a .html para publicar en Blogger.\n\n")
        text.insert(tk.END, "Copyright 2025 \u24e9 Washington Indacochea Delgado.\n")
        text.insert(tk.END, "wachin.id@gmail.com\n")
        text.insert(tk.END, "Licencia: GNU GPL3. \n\n")
        text.insert(tk.END, "Este programa convierte archivos Markdown (.md) a HTML optimizado para Blogger, incluyendo una caja de código personalizada y elimina etiquetas de código en cajas de código markdown.\n\n")

        text.insert(tk.END, "Para más información, visite: \n\n", "italic")
        text.insert(tk.END, "md to html Blogger\n")
        text.insert(tk.END, "https://github.com/wachin/Markdown-to-Blogger-posts\n\n")

        text.config(state=tk.DISABLED)

        close_button = ttk.Button(self, text="Cerrar", command=self.destroy)
        close_button.pack(pady=10)

def show_about():
    AboutWindow(root)

# Crear la ventana principal
root = tk.Tk()
root.title("Conversor de Markdown a HTML para Blogger")

# Crear y colocar widgets
input_label = tk.Label(root, text="Archivo de entrada (.md):")
input_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
input_entry = tk.Entry(root, width=50)
input_entry.grid(row=0, column=1, padx=5, pady=5)
input_button = tk.Button(root, text="Seleccionar", command=select_input_file)
input_button.grid(row=0, column=2, padx=5, pady=5)

output_label = tk.Label(root, text="Archivo de salida (.html):")
output_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
output_entry = tk.Entry(root, width=50)
output_entry.grid(row=1, column=1, padx=5, pady=5)
output_button = tk.Button(root, text="Seleccionar", command=select_output_file)
output_button.grid(row=1, column=2, padx=5, pady=5)

# Variables para las casillas de verificación
var_headers = tk.BooleanVar(value=True)
var_lists = tk.BooleanVar(value=True)
var_blockquotes = tk.BooleanVar(value=True)
var_whitespace = tk.BooleanVar(value=True)
var_paragraph_space = tk.BooleanVar(value=True)
var_line_breaks = tk.BooleanVar(value=True)
var_remove_code_tags = tk.BooleanVar(value=True)  # Nueva variable para eliminar etiquetas de lenguajes

# Crear y colocar casillas de verificación
tk.Checkbutton(root, text="Modificar los encabezados añadiendo el estilo text-align: left", variable=var_headers).grid(row=2, column=0, columnspan=3, sticky="w", padx=5, pady=2)
tk.Checkbutton(root, text="Modificar las listas ordenadas y no ordenadas añadiendo el estilo text-align: left", variable=var_lists).grid(row=3, column=0, columnspan=3, sticky="w", padx=5, pady=2)
tk.Checkbutton(root, text="Agregar párrafos vacíos solo antes y después de los blockquotes", variable=var_blockquotes).grid(row=4, column=0, columnspan=3, sticky="w", padx=5, pady=2)
tk.Checkbutton(root, text="Eliminar espacios en blanco entre etiquetas para que sea un código continuo", variable=var_whitespace).grid(row=5, column=0, columnspan=3, sticky="w", padx=5, pady=2)
tk.Checkbutton(root, text="Agregar un espacio no separable al principio de cada párrafo", variable=var_paragraph_space).grid(row=6, column=0, columnspan=3, sticky="w", padx=5, pady=2)
tk.Checkbutton(root, text="Agregar dos saltos de línea al final del contenido", variable=var_line_breaks).grid(row=7, column=0, columnspan=3, sticky="w", padx=5, pady=2)
tk.Checkbutton(root, text="Borrar las etiquetas de las cajas de código", variable=var_remove_code_tags).grid(row=8, column=0, columnspan=3, sticky="w", padx=5, pady=2)  # Nueva casilla

# Añadir caja de texto para el formato de la caja de código
code_box_label = tk.Label(root, text="Formato de caja de código:")
code_box_label.grid(row=10, column=0, sticky="w", padx=5, pady=5)
code_box_entry = tk.Entry(root, width=50)
code_box_entry.grid(row=10, column=1, padx=5, pady=5)
code_box_entry.insert(0, config["code_box"])

# Botón para guardar la configuración
save_button = tk.Button(root, text="Guardar configuración", command=save_config)
save_button.grid(row=10, column=2, padx=5, pady=5)

convert_button = tk.Button(root, text="Convertir", command=convert_markdown_to_blogger)
convert_button.grid(row=11, column=1, pady=10)

status_label = tk.Label(root, text="")
status_label.grid(row=12, column=0, columnspan=3, pady=5)

# Botón "Acerca de"
about_button = ttk.Button(root, text="Acerca de...", command=show_about)
about_button.grid(row=13, column=1, pady=10)

root.mainloop()
