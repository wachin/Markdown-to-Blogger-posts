import markdown
import re
from bs4 import BeautifulSoup

def convert_markdown_to_blogger(html_file, markdown_file):
    # Lee el archivo Markdown
    with open(markdown_file, 'r', encoding='utf-8') as md_file:
        markdown_content = md_file.read()

    # Expresión regular para encontrar bloques de código en Markdown
    code_block_pattern = re.compile(r'```(.*?)```', re.DOTALL)

    # Función para reemplazar cada bloque de código con el formato deseado
    def replace_code_block(match):
        code = match.group(1).strip()
        code = re.sub(r'&', '&amp;', code)
        code = re.sub(r'<', '&lt;', code)
        code = re.sub(r'>', '&gt;', code)
        code = re.sub(r'"', '&quot;', code)
        code = re.sub(r"'", '&#39;', code)
        return (f'<pre class="linux-code" style="background: url(https://lh3.googleusercontent.com/-E2WZ-k5ArbU/VnnAeX-_qmI/AAAAAAAABDU/i1aaUUYLZh8/s540-Ic42/lincodewachin.gif) '
                '0px 0px no-repeat scroll rgb(231, 232, 233); border-color: rgb(214, 73, 55); border-style: solid; border-width: 1px 1px 1px 20px; font-family: \'UbuntuBeta Mono\', '
                '\'Ubuntu Mono\', \'Courier New\', Courier, monospace; font-size: medium; line-height: 22.3999996185303px; margin: 10px; max-height: 500px; min-height: 16px; overflow: auto; '
                f'padding: 28px 10px 10px; z-index: 10000;"><code>{code}</code></pre>')

    # Reemplaza los bloques de código en el contenido Markdown
    markdown_content = re.sub(code_block_pattern, replace_code_block, markdown_content)

    # Convierte el contenido Markdown a HTML
    html_content = markdown.markdown(markdown_content, extensions=['fenced_code'])

    # Usar BeautifulSoup para modificar el HTML generado
    soup = BeautifulSoup(html_content, 'html.parser')

    # Modificar los encabezados
    for i in range(1, 7):
        for tag in soup.find_all(f'h{i}'):
            tag['style'] = "text-align: left;"

    # Modificar las listas ordenadas y no ordenadas
    for tag in soup.find_all(['ol', 'ul']):
        tag['style'] = "text-align: left;"

    # Agregar párrafos vacíos solo antes y después de los blockquotes
    for tag in soup.find_all('blockquote'):
        tag.insert_before(soup.new_tag('p'))
        tag.insert_after(soup.new_tag('p'))

    # Convertir el soup modificado de nuevo a string
    modified_html = str(soup)

    # Eliminar espacios en blanco entre etiquetas para que sea un código continuo
    modified_html = re.sub(r'>\s+<', '><', modified_html)

    # Agregar un espacio no separable al principio de cada párrafo
    modified_html = re.sub(r'<p>', '<p>&nbsp;', modified_html)

    # Agregar dos saltos de línea al final del contenido
    modified_html += '<p><br /></p><p><br /></p>'

    # Escribe el contenido HTML resultante en el archivo de salida
    with open(html_file, 'w', encoding='utf-8') as html_out:
        html_out.write(modified_html)

# Ejemplo de uso
convert_markdown_to_blogger('output.html', 'input.md')
