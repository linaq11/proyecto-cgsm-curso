#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────────
# render_docs.sh
# Renderiza el informe final y el artículo journal a PDF + HTML + DOCX
# usando Quarto + TinyTeX dentro del contenedor Docker sig_unal v1.11.
#
# Uso (dentro del contenedor):
#   cd /home/rstudio/work/proyecto-cgsm
#   bash scripts/render_docs.sh
#
# Si Quarto falla por TinyTeX, el script intenta repararlo una vez con
# `quarto install tinytex` y vuelve a renderizar.
# ──────────────────────────────────────────────────────────────────────
set -u  # -e desactivado: queremos reportar todos los fallos al final

PROJECT_ROOT="${PROJECT_ROOT:-$(pwd)}"
cd "$PROJECT_ROOT" || { echo "ERROR: no estoy en proyecto-cgsm"; exit 1; }

echo "════════════════════════════════════════════════════════════════════"
echo " Render informe + artículo journal · $(date '+%Y-%m-%d %H:%M:%S')"
echo " Proyecto: $PROJECT_ROOT"
echo "════════════════════════════════════════════════════════════════════"

# Detectar Quarto
if ! command -v quarto >/dev/null 2>&1; then
  echo "ERROR: quarto no está en PATH"
  exit 1
fi
echo "Quarto: $(quarto --version)"
echo

# ──────────────────────────────────────────────────────────────────────
# 1. INFORME FINAL (PDF + HTML + DOCX)
# ──────────────────────────────────────────────────────────────────────
echo "──── 1/2 · informe_final.qmd ────"
INFORME_OK=0
for fmt in pdf html docx; do
  echo "  → $fmt"
  if quarto render docs/informe_final.qmd --to "$fmt" 2>&1 | tail -3; then
    echo "  ✓ $fmt OK"
  else
    echo "  ✗ $fmt FALLÓ"
    INFORME_OK=1
  fi
done

# Si el PDF falló, intentar reparar TinyTeX y reintentar
if [ $INFORME_OK -ne 0 ] && [ ! -f docs/informe_final.pdf ]; then
  echo
  echo "  PDF informe falló · reparando TinyTeX..."
  quarto install tinytex 2>&1 | tail -5
  echo "  Reintentando PDF..."
  quarto render docs/informe_final.qmd --to pdf 2>&1 | tail -3
fi

# ──────────────────────────────────────────────────────────────────────
# 2. ANEXOS TÉCNICOS (PDF + HTML)
# ──────────────────────────────────────────────────────────────────────
echo
echo "──── 2/3 · informe_anexos.qmd ────"
for fmt in pdf html docx; do
  echo "  → $fmt"
  if quarto render docs/informe_anexos.qmd --to "$fmt" 2>&1 | tail -3; then
    echo "  ✓ $fmt OK"
  else
    echo "  ✗ $fmt FALLÓ"
  fi
done

# ──────────────────────────────────────────────────────────────────────
# 3. ARTÍCULO JOURNAL (PDF + HTML + DOCX)
# ──────────────────────────────────────────────────────────────────────
echo
echo "──── 3/3 · cgsm_version_acotada.qmd ────"
for fmt in pdf html docx; do
  echo "  → $fmt"
  if quarto render docs/cgsm_version_acotada.qmd --to "$fmt" 2>&1 | tail -3; then
    echo "  ✓ $fmt OK"
  else
    echo "  ✗ $fmt FALLÓ"
  fi
done

# ──────────────────────────────────────────────────────────────────────
# 3b. Embellecer tablas de los DOCX (header azul, bordes, banded rows)
# ──────────────────────────────────────────────────────────────────────
echo
echo "──── Embellecedor de tablas DOCX ────"
if command -v python >/dev/null 2>&1; then
  python -c "import docx" 2>/dev/null || {
    echo "  Instalando python-docx..."
    pip install --break-system-packages --quiet python-docx 2>&1 | tail -2
  }
  python scripts/embellish_docx_tables.py 2>&1 | tail -8
else
  echo "  ✗ python no disponible · saltando embellecedor"
fi

# ──────────────────────────────────────────────────────────────────────
# 4. RESUMEN DE SALIDAS
# ──────────────────────────────────────────────────────────────────────
echo
echo "════════════════════════════════════════════════════════════════════"
echo " ARCHIVOS GENERADOS"
echo "════════════════════════════════════════════════════════════════════"
for f in docs/informe_final.pdf docs/informe_final.html docs/informe_final.docx \
         docs/informe_anexos.pdf docs/informe_anexos.html docs/informe_anexos.docx \
         docs/cgsm_version_acotada.pdf docs/cgsm_version_acotada.html docs/cgsm_version_acotada.docx; do
  if [ -f "$f" ]; then
    sz=$(stat -c%s "$f" 2>/dev/null || stat -f%z "$f" 2>/dev/null)
    mb=$(awk "BEGIN{printf \"%.2f\", $sz/1024/1024}")
    mtime=$(stat -c%y "$f" 2>/dev/null | cut -d. -f1 || stat -f%Sm "$f" 2>/dev/null)
    echo "  ✓ $f  (${mb} MB · $mtime)"
  else
    echo "  ✗ $f  NO existe"
  fi
done

echo
echo "Si todo está OK, hacer commit + push:"
echo "  git add docs/informe_final.{pdf,html,docx} docs/informe_anexos.{pdf,html} docs/cgsm_version_acotada.{pdf,html}"
echo "  git commit -m \"Re-render informe principal + anexos + articulo journal\""
echo "  git push"
