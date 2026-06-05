"""Regenera docs/informe_anexos.qmd desde docs/informe_anexos.md.

Convierte bloques de código indentados con 4 espacios (estilo verbatim de pandoc)
a fenced code blocks con detección de lenguaje, para que Typst aplique
syntax highlighting en el PDF.
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
MD = ROOT / 'docs' / 'informe_anexos.md'
QMD = ROOT / 'docs' / 'informe_anexos.qmd'

YAML = '''---
title: "Pipeline multilenguaje GeoAI para el monitoreo del manglar en la Ciénaga Grande de Santa Marta · Anexos"
author: "Lina María Quintero Fonseca"
lang: es
format:
  typst:
    toc: false
    number-sections: false
    fontsize: 11pt
    margin:
      x: 2.5cm
      y: 2.5cm
    highlight-style: github
---
'''


def detect_lang(code: str) -> str:
    if re.search(r'\blibrary\(|\binstall\.packages\(|<-\s|read\.csv\(|data\.frame\(|bfastmonitor\(', code):
        return 'r'
    if re.search(r'\busing Pkg\b|Pkg\.add\(|\busing GeoJSON\b|\busing DataFrames\b', code):
        return 'julia'
    if re.search(r'\bimport \w+|\bfrom \w+ import|\bdef \w+\(|\bxr\.open_dataset|\bgeopandas|\brasterio\.', code):
        return 'python'
    if re.search(r'^pip install|^earthengine |^docker |^cd /|^bash |\.sh\b|^Rscript |^python3? ', code, re.M):
        return 'bash'
    if '├──' in code or '└──' in code:
        return ''  # ASCII tree, sin highlighting
    return ''


def convert_indented(md: str) -> str:
    lines = md.split('\n')
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        # Detecta inicio de bloque indentado (línea con 4 espacios + previa vacía o inicio)
        prev_blank = (i == 0) or (lines[i - 1].strip() == '')
        if line.startswith('    ') and prev_blank and line.strip() != '':
            block: list[str] = []
            while i < len(lines) and (lines[i].startswith('    ') or lines[i].strip() == ''):
                if lines[i].startswith('    '):
                    block.append(lines[i][4:])
                else:
                    block.append('')
                i += 1
            while block and block[-1] == '':
                block.pop()
            body = '\n'.join(block)
            lang = detect_lang(body)
            out.append('```' + lang)
            out.append(body)
            out.append('```')
            continue
        out.append(line)
        i += 1
    return '\n'.join(out)


def main() -> int:
    if not MD.exists():
        print(f'ERROR: {MD} no existe', file=sys.stderr)
        return 1
    md = MD.read_text(encoding='utf-8')
    md_converted = convert_indented(md)
    QMD.write_text(YAML + '\n' + md_converted, encoding='utf-8')
    n_blocks = md_converted.count('```') // 2
    print(f'  qmd anexos regenerado: {len(md_converted)} chars, {n_blocks} fenced blocks')
    return 0


if __name__ == '__main__':
    sys.exit(main())
