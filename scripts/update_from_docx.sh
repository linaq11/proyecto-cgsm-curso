#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────────
# update_from_docx.sh
# Workflow: docx como fuente de verdad → html + md + pdf vía Typst
#
# Uso (desde la raíz del proyecto):
#   bash scripts/update_from_docx.sh [final|anexos|all]
#
# Pre-requisitos:
#   - Quarto >= 1.4 con Typst
#   - Pandoc (bundle con Quarto)
#
# Después de editar informe_final.docx (o informe_anexos.docx) en Word,
# correr este script para regenerar HTML, MD y PDF.
# ──────────────────────────────────────────────────────────────────────
set -u

PROJECT_ROOT="${PROJECT_ROOT:-$(pwd)}"
DOCS="$PROJECT_ROOT/docs"
PANDOC="${PANDOC:-quarto pandoc}"

if ! command -v quarto >/dev/null 2>&1; then
  echo "ERROR: quarto no está en PATH"
  exit 1
fi

# Resolver pandoc del bundle Quarto si no está suelto
if ! command -v pandoc >/dev/null 2>&1; then
  PANDOC_BIN="$(quarto --paths 2>/dev/null | grep -i pandoc | head -1)/pandoc"
  if [ ! -x "$PANDOC_BIN" ]; then
    PANDOC_BIN="$(dirname $(command -v quarto))/tools/pandoc"
  fi
  PANDOC="$PANDOC_BIN"
else
  PANDOC="pandoc"
fi

echo "Quarto: $(quarto --version)"
echo "Pandoc: $($PANDOC --version 2>&1 | head -1)"
echo

# ──────────────────────────────────────────────────────────────────────
# Función: regenerar html + md desde docx
# ──────────────────────────────────────────────────────────────────────
regenerate_from_docx() {
  local NAME="$1"
  local DOCX="$DOCS/${NAME}.docx"
  local HTML="$DOCS/${NAME}.html"
  local MD="$DOCS/${NAME}.md"
  local MEDIA="$DOCS/${NAME}_media"

  if [ ! -f "$DOCX" ]; then
    echo "  ✗ $DOCX no existe · saltando"
    return 1
  fi

  echo "  → $NAME · regenerando html + md desde docx"
  rm -rf "$MEDIA"

  "$PANDOC" "$DOCX" -o "$HTML" \
    --standalone --wrap=none \
    --extract-media="$MEDIA" 2>&1 | tail -2

  "$PANDOC" "$DOCX" -o "$MD" \
    --wrap=none \
    --extract-media="$MEDIA" 2>&1 | tail -2

  echo "  ✓ $HTML"
  echo "  ✓ $MD"
}

# ──────────────────────────────────────────────────────────────────────
# Función: regenerar qmd para anexos (no se mantiene a mano)
# Combina YAML base + cuerpo regenerado del md.
# ──────────────────────────────────────────────────────────────────────
regenerate_anexos_qmd() {
  local MD="$DOCS/informe_anexos.md"
  local QMD="$DOCS/informe_anexos.qmd"

  if [ ! -f "$MD" ]; then return 0; fi

  python3 "$PROJECT_ROOT/scripts/_regenerate_anexos_qmd.py"
}

# ──────────────────────────────────────────────────────────────────────
# Función: renderizar PDF vía Typst (si hay qmd)
# ──────────────────────────────────────────────────────────────────────
render_pdf_typst() {
  local NAME="$1"
  local QMD="$DOCS/${NAME}.qmd"

  # Para anexos, regenerar siempre el qmd desde el md
  if [ "$NAME" = "informe_anexos" ]; then
    regenerate_anexos_qmd
  fi

  if [ ! -f "$QMD" ]; then
    echo "  · $NAME · sin qmd · saltando PDF Typst"
    return 0
  fi

  echo "  → $NAME · renderizando PDF vía Typst"
  quarto render "$QMD" --to typst 2>&1 | tail -3
}

# ──────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────
TARGET="${1:-all}"

case "$TARGET" in
  final)
    regenerate_from_docx "informe_final"
    # NOTA: PDF de informe_final NO se regenera aquí por defecto. Lina lo
    # exporta desde Word para preservar el layout aprobado.
    # Para forzar el render Typst: bash scripts/update_from_docx.sh final-pdf
    echo "  · informe_final.pdf · no se regenera (export manual desde Word)"
    ;;
  final-pdf)
    regenerate_from_docx "informe_final"
    render_pdf_typst "informe_final"
    ;;
  anexos)
    regenerate_from_docx "informe_anexos"
    # NOTA: PDF de anexos NO se regenera aquí por defecto. Lina lo exporta
    # manualmente desde Word para preservar el layout con highlighting nativo.
    # Para forzar el render Typst: bash scripts/update_from_docx.sh anexos-pdf
    echo "  · informe_anexos.pdf · no se regenera (export manual desde Word)"
    ;;
  anexos-pdf)
    regenerate_from_docx "informe_anexos"
    render_pdf_typst "informe_anexos"
    ;;
  all)
    regenerate_from_docx "informe_final"
    echo "  · informe_final.pdf · no se regenera (export manual desde Word)"
    echo
    regenerate_from_docx "informe_anexos"
    echo "  · informe_anexos.pdf · no se regenera (export manual desde Word)"
    ;;
  all-pdf)
    regenerate_from_docx "informe_final"
    render_pdf_typst "informe_final"
    echo
    regenerate_from_docx "informe_anexos"
    render_pdf_typst "informe_anexos"
    ;;
  *)
    echo "Uso: $0 [final|final-pdf|anexos|anexos-pdf|all|all-pdf]"
    echo "       final       · informe_final.docx -> html/md (PDF manual desde Word)"
    echo "       final-pdf   · igual a 'final' pero también regenera PDF vía Typst"
    echo "       anexos      · informe_anexos.docx -> html/md/qmd (PDF manual desde Word)"
    echo "       anexos-pdf  · igual a 'anexos' pero también regenera PDF vía Typst"
    echo "       all         · final + anexos, ambos sin PDF (export manual)"
    echo "       all-pdf     · all + ambos PDFs regenerados vía Typst"
    exit 1
    ;;
esac

echo
echo "════════════════════════════════════════════════════════════════════"
echo " Resumen de salidas"
echo "════════════════════════════════════════════════════════════════════"
for f in "$DOCS"/informe_final.{docx,html,md,pdf} \
         "$DOCS"/informe_anexos.{docx,html,md,pdf}; do
  if [ -f "$f" ]; then
    sz=$(stat -c%s "$f" 2>/dev/null || stat -f%z "$f" 2>/dev/null)
    kb=$(awk "BEGIN{printf \"%.0f\", $sz/1024}")
    echo "  ✓ $(basename $f)  (${kb} KB)"
  fi
done

echo
echo "Listo. Si todo está OK:"
echo "  git add docs/informe_final.{docx,html,md,pdf} docs/informe_anexos.*"
echo "  git commit -m \"Update desde docx revisado\""
echo "  git push"
