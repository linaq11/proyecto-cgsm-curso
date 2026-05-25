"""
Post-procesa los DOCX rendereados por Quarto para que las tablas se vean
bonitas (Word):
    - bordes negros visibles en todas las celdas (full grid)
    - cabecera con fondo azul suave + texto blanco bold
    - alternancia de filas (banded rows)
    - texto compacto (9 pt) y padding pequeño
    - ancho de tabla = 100% de la página

Uso:
    cd /home/rstudio/work/proyecto-cgsm
    python scripts/embellish_docx_tables.py docs/informe_final.docx
    python scripts/embellish_docx_tables.py docs/informe_anexos.docx
    python scripts/embellish_docx_tables.py docs/cgsm_version_acotada.docx

Requiere:  pip install python-docx
"""
import sys
from pathlib import Path
from docx import Document
from docx.shared import Pt, RGBColor
from docx.oxml.ns import qn, nsmap
from docx.oxml import OxmlElement


def _set_cell_borders(cell, color='000000', size='8'):
    """Elimina todos los bordes de la celda (val=nil)."""
    tc_pr = cell._tc.get_or_add_tcPr()
    # Limpiar tcBorders previo
    for old in tc_pr.findall(qn('w:tcBorders')):
        tc_pr.remove(old)
    tc_borders = OxmlElement('w:tcBorders')
    for edge in ('top', 'left', 'bottom', 'right'):
        b = OxmlElement(f'w:{edge}')
        b.set(qn('w:val'), 'nil')         # nil = sin borde
        tc_borders.append(b)
    tc_pr.append(tc_borders)


def _strip_table_style(tbl):
    """Quita el estilo heredado del reference doc y los bordes a nivel
    de tabla; reemplaza por bordes sólidos negros uniformes. También
    quita cualquier posicionamiento flotante / wrapping (marco externo)."""
    tbl_pr = tbl._tbl.tblPr
    # 1. quitar referencia al estilo (no más 'TableGrid' etc del reference)
    for s in tbl_pr.findall(qn('w:tblStyle')):
        tbl_pr.remove(s)
    # 2. limpiar bordes a nivel tabla
    for old in tbl_pr.findall(qn('w:tblBorders')):
        tbl_pr.remove(old)
    # 3. quitar posicionamiento flotante (causa el "marco externo")
    for pos in tbl_pr.findall(qn('w:tblpPr')):
        tbl_pr.remove(pos)
    # 4. quitar wrapping
    for wrap in tbl_pr.findall(qn('w:tblOverlap')):
        tbl_pr.remove(wrap)
    # 5. declarar todos los bordes a nivel tabla como "nil" (sin línea)
    tbl_borders = OxmlElement('w:tblBorders')
    for edge in ('top', 'left', 'bottom', 'right',
                 'insideH', 'insideV'):
        b = OxmlElement(f'w:{edge}')
        b.set(qn('w:val'), 'nil')
        tbl_borders.append(b)
    tbl_pr.append(tbl_borders)


def _strip_paragraph_borders(doc):
    """Recorre TODOS los párrafos del documento (body + celdas) y quita
    cualquier `w:pBdr` (border-around-paragraph). Esto elimina el
    'recuadro' que el reference doc añade a captions de figuras/tablas."""
    def _strip(p):
        p_pr = p._p.find(qn('w:pPr'))
        if p_pr is None:
            return
        for pbdr in p_pr.findall(qn('w:pBdr')):
            p_pr.remove(pbdr)
    # Body
    for p in doc.paragraphs:
        _strip(p)
    # Tablas
    for tbl in doc.tables:
        for row in tbl.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    _strip(p)


def _strip_figure_borders(doc):
    """Quita el contorno (línea de borde) de TODAS las imágenes inline
    o ancladas del documento. Busca elementos `<a:ln>` (line) dentro
    de drawings y los reemplaza por `<a:ln><a:noFill/></a:ln>` para
    asegurar que ni siquiera un estilo heredado pueda pintar borde."""
    A_NS  = 'http://schemas.openxmlformats.org/drawingml/2006/main'
    A_LN  = f'{{{A_NS}}}ln'
    A_NOFILL = f'{{{A_NS}}}noFill'
    # Eliminar todos los <a:ln> existentes
    for ln in list(doc.element.iter(A_LN)):
        parent = ln.getparent()
        if parent is not None:
            parent.remove(ln)
    # (Opcional) inyectar un <a:ln><a:noFill/></a:ln> dentro de cada
    # <pic:spPr> para sellar el borde a None definitivamente.
    PIC_NS = 'http://schemas.openxmlformats.org/drawingml/2006/picture'
    SP_PR  = f'{{{PIC_NS}}}spPr'
    from lxml import etree
    for sp_pr in doc.element.iter(SP_PR):
        ln_off = etree.SubElement(sp_pr, A_LN)
        etree.SubElement(ln_off, A_NOFILL)


def _force_all_text_black(doc):
    """Recorre todo el documento (body + tablas) y fuerza color = negro
    en cada run de texto. También quita cursiva y bold heredados de los
    estilos Caption del reference doc para los párrafos con estilo
    'Image Caption', 'Caption' o similar (texto de leyendas de figuras
    y tablas)."""
    def _process_paragraph(p):
        # Solo forzar color a negro; preservar cursivas de cualquier estilo
        for run in p.runs:
            run.font.color.rgb = RGBColor(0, 0, 0)
    # Body
    for p in doc.paragraphs:
        _process_paragraph(p)
    # Tablas
    for tbl in doc.tables:
        for row in tbl.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    _process_paragraph(p)


def _set_cell_shading(cell, color_hex):
    """Aplica color de relleno a una celda."""
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), color_hex)
    tc_pr.append(shd)


def _set_cell_margins(cell, top=60, right=80, bottom=60, left=80):
    """Padding interno de celda en twentieths of a point (1 pt = 20)."""
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_mar = OxmlElement('w:tcMar')
    for edge, val in (('top', top), ('left', left),
                       ('bottom', bottom), ('right', right)):
        m = OxmlElement(f'w:{edge}')
        m.set(qn('w:w'), str(val))
        m.set(qn('w:type'), 'dxa')
        tc_mar.append(m)
    tc_pr.append(tc_mar)


def _set_table_width(table, pct=100):
    """Fuerza el ancho de la tabla al 100% de la página."""
    tbl_pr = table._tbl.tblPr
    tbl_w = tbl_pr.find(qn('w:tblW'))
    if tbl_w is None:
        tbl_w = OxmlElement('w:tblW')
        tbl_pr.append(tbl_w)
    tbl_w.set(qn('w:w'), f'{pct * 50}')   # pct units = pct * 50
    tbl_w.set(qn('w:type'), 'pct')


def _set_table_layout_autofit(table):
    """Permite que las celdas autoajusten el ancho del contenido."""
    tbl_pr = table._tbl.tblPr
    layout = tbl_pr.find(qn('w:tblLayout'))
    if layout is None:
        layout = OxmlElement('w:tblLayout')
        tbl_pr.append(layout)
    layout.set(qn('w:type'), 'autofit')


# ── estilo: limpio, sin fondos, bordes negros sólidos ────────────────
BORDER_COLOR   = '000000'  # negro
BORDER_SIZE    = '16'      # eighths of pt → 16 = 2pt sólida inequívoca
TABLE_FONT_SZ  = Pt(10)   # 10 pt para texto de tablas (cuerpo = 11 pt)
HEADER_FONT_SZ = Pt(10)


def _clear_cell_shading(cell):
    """Quita cualquier shading existente (vuelve a blanco)."""
    tc_pr = cell._tc.get_or_add_tcPr()
    for shd in tc_pr.findall(qn('w:shd')):
        tc_pr.remove(shd)


def embellish(path: Path):
    print(f'──── {path.name}')
    if not path.exists():
        print(f'  SKIP (no existe)')
        return
    doc = Document(str(path))
    n = 0
    for tbl in doc.tables:
        n += 1
        # 1. Quitar estilo heredado del reference doc (bordes punteados/azules)
        _strip_table_style(tbl)
        _set_table_width(tbl, pct=100)
        _set_table_layout_autofit(tbl)
        for r_idx, row in enumerate(tbl.rows):
            for c_idx, cell in enumerate(row.cells):
                # Bordes sólidos negros en todas las celdas
                _set_cell_borders(cell, color=BORDER_COLOR, size=BORDER_SIZE)
                # Sin shading (blanco)
                _clear_cell_shading(cell)
                # Padding interno reducido
                _set_cell_margins(cell, top=40, right=60, bottom=40, left=60)
                # Tipografía
                for p in cell.paragraphs:
                    p.paragraph_format.space_before = Pt(0)
                    p.paragraph_format.space_after  = Pt(0)
                    for run in p.runs:
                        run.font.size = TABLE_FONT_SZ
                        if r_idx == 0:
                            run.font.bold = True
                            # Header: texto negro bold, sin color de relleno
                            run.font.color.rgb = RGBColor(0, 0, 0)
                            run.font.size = HEADER_FONT_SZ
    # Forzar todo el texto a negro
    _force_all_text_black(doc)
    # Quitar bordes de párrafo (recuadros alrededor de captions)
    _strip_paragraph_borders(doc)
    # Quitar bordes de las figuras (contorno de imágenes inline / ancladas)
    _strip_figure_borders(doc)
    doc.save(str(path))
    print(f'  ✓ {n} tablas embellecidas · texto en negro · sin recuadros en captions ni figuras')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        # Procesar los 3 documentos por default
        ROOT = Path(__file__).resolve().parents[1]
        targets = [
            ROOT / 'docs' / 'informe_final.docx',
            ROOT / 'docs' / 'informe_anexos.docx',
            ROOT / 'docs' / 'cgsm_version_acotada.docx',
        ]
    else:
        targets = [Path(a) for a in sys.argv[1:]]
    for t in targets:
        embellish(t)
    print('\nListo. Abrir los DOCX para ver el resultado.')
