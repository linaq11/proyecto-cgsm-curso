#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────────
# refresh_mapids.sh
# Regenera dashboard_CGSM_final.html con mapId frescos de Google Earth Engine,
# lo copia a docs/ para GitHub Pages y hace commit + push en un solo paso.
#
# Los mapId del raster NDVI expiran en horas. Este script se corre justo
# antes de presentar/entregar para que el slider del dashboard funcione.
#
# Uso (desde la raíz del proyecto):
#   bash scripts/refresh_mapids.sh                  # commit + push
#   bash scripts/refresh_mapids.sh --no-push        # solo commit
#   bash scripts/refresh_mapids.sh --no-commit      # solo regenera y copia
#
# Requisitos:
#   - gcloud Application Default Credentials con scope GEE
#     (gcloud auth application-default login)
#   - python con earthengine-api, folium, geopandas, pandas, jinja2, branca
# ──────────────────────────────────────────────────────────────────────
set -eu

PROJECT_ROOT="${PROJECT_ROOT:-$(pwd)}"
SCRIPT="$PROJECT_ROOT/src/python/make_dashboard_html.py"
OUT_SRC="$PROJECT_ROOT/outputs/maps/dashboard_CGSM_final.html"
OUT_DOCS="$PROJECT_ROOT/docs/outputs/maps/dashboard_CGSM_final.html"

DO_COMMIT=1
DO_PUSH=1
for arg in "$@"; do
  case "$arg" in
    --no-push) DO_PUSH=0 ;;
    --no-commit) DO_COMMIT=0; DO_PUSH=0 ;;
    *) echo "Flag desconocido: $arg" ; exit 1 ;;
  esac
done

if [ ! -f "$SCRIPT" ]; then
  echo "ERROR: no existe $SCRIPT"
  exit 1
fi

# 1. Regenerar HTML con mapId frescos
echo "→ Regenerando dashboard_CGSM_final.html con mapIds frescos de GEE..."
python "$SCRIPT"
if [ ! -f "$OUT_SRC" ]; then
  echo "ERROR: el script no produjo $OUT_SRC"
  exit 1
fi
sz_kb=$(awk "BEGIN{printf \"%.0f\", $(stat -c%s "$OUT_SRC" 2>/dev/null || stat -f%z "$OUT_SRC")/1024}")
echo "  ✓ $OUT_SRC ($sz_kb KB)"

# 2. Copiar al directorio que GitHub Pages sirve
mkdir -p "$(dirname "$OUT_DOCS")"
cp "$OUT_SRC" "$OUT_DOCS"
echo "  ✓ espejo en $OUT_DOCS"

# 3. Commit
if [ "$DO_COMMIT" = "0" ]; then
  echo ""
  echo "Listo. Sin commit (--no-commit). Para subir:"
  echo "  git add docs/outputs/maps/dashboard_CGSM_final.html"
  echo "  git commit -m \"Refresh GEE mapIds NDVI\""
  echo "  git push origin main"
  exit 0
fi

cd "$PROJECT_ROOT"
git add docs/outputs/maps/dashboard_CGSM_final.html
if git diff --staged --quiet; then
  echo "  · sin cambios para commitear (HTML idéntico)"
  exit 0
fi
git commit -m "Refresh GEE mapIds NDVI"
echo "  ✓ commit creado"

# 4. Push
if [ "$DO_PUSH" = "0" ]; then
  echo ""
  echo "Listo. Sin push (--no-push). Para subir:"
  echo "  git push origin main"
  exit 0
fi

git push origin main
echo "  ✓ push a origin/main"
echo ""
echo "GitHub Pages re-deploya en 1-2 min. Ctrl+F5 para ver las capas NDVI."
