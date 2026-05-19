"""
Genera un reference-doc.docx para Quarto que aplica Times 11 negro al cuerpo,
encabezados Times bold y header institucional UNAL, de modo que el DOCX
generado replique la estética del PDF.

Uso:
    cd /home/rstudio/work/proyecto-cgsm
    python docs/crear_reference_doc.py
"""
import subprocess
import sys
from pathlib import Path

# Auto-instalar python-docx si no está
try:
    import docx
except ImportError:
    print('Instalando python-docx...')
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'python-docx',
                    '--break-system-packages', '--quiet'], check=True)
    import docx

from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, RGBColor

DOCS = Path(__file__).parent
OUT  = DOCS / 'reference_unal.docx'

# 1) Generar la plantilla por defecto de Pandoc como punto de partida
subprocess.run(['pandoc', '-o', str(OUT), '--print-default-data-file',
                'reference.docx'], check=True)

# 2) Aplicar overrides: Times 11 negro en todos los estilos
doc = docx.Document(str(OUT))

styles_to_fix = ['Normal', 'Heading 1', 'Heading 2', 'Heading 3',
                 'Heading 4', 'Title', 'Subtitle', 'Caption',
                 'Body Text', 'Block Text', 'List Paragraph']

for style_name in styles_to_fix:
    try:
        s = doc.styles[style_name]
        if s.font:
            s.font.name = 'Times New Roman'
            s.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
            if style_name == 'Normal':
                s.font.size = Pt(11)
                # Justificado para el cuerpo
                s.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            elif style_name == 'Title':
                s.font.size = Pt(16)
                s.font.bold = True
            elif style_name == 'Heading 1':
                s.font.size = Pt(14)
                s.font.bold = True
            elif style_name == 'Heading 2':
                s.font.size = Pt(12)
                s.font.bold = True
            elif style_name in ['Heading 3', 'Heading 4']:
                s.font.size = Pt(11)
                s.font.bold = True
            elif style_name == 'Caption':
                s.font.size = Pt(10)
                s.font.italic = True
            elif style_name == 'Body Text':
                s.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    except KeyError:
        continue

doc.save(str(OUT))
print(f'Reference doc generada: {OUT}')
print(f'Tamano: {OUT.stat().st_size/1024:.0f} KB')
print('Reference doc creada con Times New Roman, negro, 11pt por defecto.')
