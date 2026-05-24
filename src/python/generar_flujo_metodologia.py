"""
Genera la figura del flujo metodológico (6 fases + 5 salidas + Docker)
usando matplotlib puro, sin dependencia de cairo / librsvg / Inkscape.

Reemplaza el pipeline SVG -> PNG vía svg_a_png.py para esta figura
específica, evitando problemas de portabilidad cuando cairo nativo no
está instalado.

Uso:
    cd /home/rstudio/work/proyecto-cgsm
    python src/python/generar_flujo_metodologia.py

Salida:
    outputs/figures/flujo_metodologia.png  (resolución 200 dpi)
"""
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle

ROOT = Path(__file__).resolve().parents[2]
OUT  = ROOT / 'outputs' / 'figures' / 'flujo_metodologia.png'

# ---- Layout config ----
FIG_W, FIG_H = 15.5, 4.8   # pulgadas
BOX_W, BOX_H = 2.20, 1.20  # caja de fase (datos del proyecto)
OUT_BOX_W, OUT_BOX_H = 2.55, 0.85  # cajas de salida

PHASES = [
    {'n': '1', 'color': '#0d47a1', 'title': 'Datacube',
     'lines': ['Sentinel-2 + Landsat', 'geemap · xarray · CF-1.8',
               'Notebooks 01 · 09']},
    {'n': '2', 'color': '#4527a0', 'title': 'Series + bfast',
     'lines': ['NDVI mensual · z-score', 'Python + R · bfast',
               'Notebooks 02 · 02b · 02c']},
    {'n': '3', 'color': '#ad1457', 'title': 'Segmentación',
     'lines': ['SamGeo · 3 RGB S2', 'Topología DE-9IM',
               'Notebooks 03 · 04b · 04c']},
    {'n': '4', 'color': '#311b92', 'title': 'Fragmentación',
     'lines': ['Julia · LibGEOS', 'NP · MSI · NND · área',
               'Notebook 04']},
    {'n': '5', 'color': '#1b5e20', 'title': 'Clima · SAR',
     'lines': ['ERA5 · ENSO · CHIRPS', 'Caudal · S1 SAR-VH',
               'Notebooks 07 · 08 · 12']},
    {'n': '6', 'color': '#bf360c', 'title': 'Validación + RF',
     'lines': ['INVEMAR · WorldCover', 'Random Forest · alertas',
               'Notebooks 05 · 10 · 11']},
]

OUTPUTS = [
    ('32 notebooks',     '.ipynb numerados · reproducibles'),
    ('54 tablas CSV',    'Resultados numéricos'),
    ('43 figuras PNG',   'Mapas · series · correlaciones'),
    ('Dashboard 17 capas','HTML interactivo Leaflet'),
    ('Informe Quarto 50+ pp','PDF + HTML reproducible'),
]

# ---- Render ----
plt.rcParams['font.family'] = ['DejaVu Sans', 'Arial', 'sans-serif']
fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=200)
ax.set_xlim(0, FIG_W)
ax.set_ylim(0, FIG_H)
ax.set_aspect('equal')
ax.axis('off')
fig.patch.set_facecolor('white')

# Título
ax.text(FIG_W/2, FIG_H - 0.20, 'FLUJO DE TRABAJO · 6 FASES SECUENCIALES CON VALIDACIÓN CRUZADA',
        ha='center', va='center', fontsize=13, fontweight=700,
        color='#bf360c')

# ---- Fases (fila superior) ----
gap = 0.15
phase_y = 2.55
phase_w_total = len(PHASES) * BOX_W + (len(PHASES) - 1) * gap
phase_x0 = (FIG_W - phase_w_total) / 2

for i, p in enumerate(PHASES):
    x = phase_x0 + i * (BOX_W + gap)
    # Caja
    box = FancyBboxPatch((x, phase_y), BOX_W, BOX_H,
                         boxstyle='round,pad=0.02,rounding_size=0.10',
                         linewidth=1.8, edgecolor=p['color'], facecolor='#f5f8fa',
                         zorder=2)
    ax.add_patch(box)
    # Círculo numerado en esquina superior izquierda (FUERA del flujo del texto)
    cx = x + 0.20
    cy = phase_y + BOX_H - 0.22
    circ = Circle((cx, cy), 0.16, facecolor=p['color'],
                  edgecolor='white', linewidth=1.5, zorder=3)
    ax.add_patch(circ)
    ax.text(cx, cy, p['n'], ha='center', va='center',
            fontsize=11, fontweight=700, color='white', zorder=4)
    # Título de fase (a la derecha del círculo)
    ax.text(cx + 0.25, cy + 0.01, p['title'], ha='left', va='center',
            fontsize=10.5, fontweight=700, color=p['color'], zorder=4)
    # Subtítulos (3 líneas debajo)
    base_y = phase_y + BOX_H - 0.50
    for j, line in enumerate(p['lines']):
        gray = ['#1a1a1a', '#4a4a4a', '#6a6a6a'][j]
        size = [9.0, 9.0, 8.0][j]
        ax.text(x + BOX_W/2, base_y - j*0.18, line, ha='center', va='center',
                fontsize=size, color=gray, zorder=4)
    # Flecha entre fases
    if i < len(PHASES) - 1:
        ax_x = x + BOX_W + 0.02
        bx = x + BOX_W + gap - 0.02
        arrow = FancyArrowPatch((ax_x, phase_y + BOX_H/2),
                                 (bx, phase_y + BOX_H/2),
                                 arrowstyle='-|>', mutation_scale=12,
                                 color='#bf360c', linewidth=1.8, zorder=1)
        ax.add_patch(arrow)

# ---- Salidas (fila inferior) ----
ax.text(FIG_W/2, 2.15, 'SALIDAS UNIFICADAS', ha='center', va='center',
        fontsize=9.5, color='#6a6a6a')

out_gap = 0.15
out_w_total = len(OUTPUTS) * OUT_BOX_W + (len(OUTPUTS) - 1) * out_gap
out_x0 = (FIG_W - out_w_total) / 2
out_y = 1.15

for i, (title, sub) in enumerate(OUTPUTS):
    x = out_x0 + i * (OUT_BOX_W + out_gap)
    box = FancyBboxPatch((x, out_y), OUT_BOX_W, OUT_BOX_H,
                         boxstyle='round,pad=0.02,rounding_size=0.08',
                         linewidth=1.2, edgecolor='#1b5e20', facecolor='#f5f8fa',
                         zorder=2)
    ax.add_patch(box)
    ax.text(x + OUT_BOX_W/2, out_y + OUT_BOX_H - 0.28, title,
            ha='center', va='center', fontsize=10.5, fontweight=600,
            color='#1b5e20', zorder=3)
    ax.text(x + OUT_BOX_W/2, out_y + 0.20, sub,
            ha='center', va='center', fontsize=8.5, color='#4a4a4a', zorder=3)

# Flechas verticales de cada fase hacia las salidas (suaves)
for i in range(min(len(PHASES), len(OUTPUTS))):
    px = phase_x0 + i * (BOX_W + gap) + BOX_W/2
    ox = out_x0 + i * (OUT_BOX_W + out_gap) + OUT_BOX_W/2
    arrow = FancyArrowPatch((px, phase_y - 0.02),
                             (ox, out_y + OUT_BOX_H + 0.02),
                             arrowstyle='-|>', mutation_scale=8,
                             color='#bf360c', linewidth=0.9,
                             alpha=0.35, zorder=1)
    ax.add_patch(arrow)

# ---- Docker base ----
docker_w = 5.5
docker = FancyBboxPatch(((FIG_W - docker_w)/2, 0.20), docker_w, 0.60,
                       boxstyle='round,pad=0.02,rounding_size=0.08',
                       linewidth=1.2, edgecolor='#006064', facecolor='#f5f8fa',
                       linestyle=(0, (5, 3)), zorder=2)
ax.add_patch(docker)
ax.text(FIG_W/2, 0.50, 'Contenedor Docker sig_unal v1.11 · base reproducible',
        ha='center', va='center', fontsize=10, fontweight=700, color='#006064')

# ---- Guardar ----
plt.savefig(OUT, dpi=200, bbox_inches='tight', facecolor='white')
plt.close()
print(f'OK: {OUT.relative_to(ROOT)} ({OUT.stat().st_size/1024:.0f} KB)')
