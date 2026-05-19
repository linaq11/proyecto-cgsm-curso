"""
Genera mapa multipanel (a)(b)(c) del área de estudio para el informe final.

  (a) Colombia con Magdalena resaltado
  (b) Departamento Magdalena con cabeceras y bbox del AOI
  (c) Zoom CGSM: composite RGB Sentinel-2 + manglar + AOI + estaciones INVEMAR

Salida: outputs/figures/mapa_area_estudio.png

Uso:
    cd /home/rstudio/work/proyecto-cgsm
    python src/python/generar_mapa_area_estudio.py
"""
from pathlib import Path

import geopandas as gpd
import matplotlib.patches as mpatches
import matplotlib.patheffects as path_effects
import matplotlib.pyplot as plt
import numpy as np
import rasterio
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

ROOT  = Path(__file__).resolve().parents[2]
OUT   = ROOT / 'outputs' / 'figures' / 'mapa_area_estudio.png'
CACHE = ROOT / 'data' / 'raw' / 'admin'  # cache local para no descargar cada vez
CACHE.mkdir(parents=True, exist_ok=True)

# ------------------------------------------------------------------
# 1. Datos vectoriales: Colombia y departamentos (GADM v4.1 desde URL)
# ------------------------------------------------------------------
GADM_URL = 'https://geodata.ucdavis.edu/gadm/gadm4.1/json/gadm41_COL_1.json.zip'
GADM_LOCAL = CACHE / 'gadm41_COL_1.json'

if GADM_LOCAL.exists():
    print(f'Usando admin cacheado: {GADM_LOCAL.name}')
    co_dpts = gpd.read_file(GADM_LOCAL)
else:
    print(f'Descargando departamentos Colombia desde GADM...')
    co_dpts = gpd.read_file(GADM_URL)
    # Guardar como GeoJSON para cache
    co_dpts.to_file(GADM_LOCAL, driver='GeoJSON')
    print(f'  Cacheado en {GADM_LOCAL}')

# Asegurar CRS WGS84
if co_dpts.crs is None or co_dpts.crs.to_epsg() != 4326:
    co_dpts = co_dpts.to_crs(4326)

# Colombia = unión de todos los departamentos
colombia = gpd.GeoDataFrame(geometry=[co_dpts.geometry.union_all()], crs=4326)
magdalena = co_dpts[co_dpts['NAME_1'].str.contains('Magdalena', case=False, na=False)]
print(f'  Departamentos Colombia: {len(co_dpts)}')
print(f'  Magdalena encontrado: {magdalena.iloc[0]["NAME_1"] if len(magdalena) else "NO"}')

# AOI y manglar
aoi = gpd.read_file(ROOT / 'data' / 'raw' / 'cgsm_aoi_acotado_4326.geojson')
manglar = gpd.read_file(ROOT / 'data' / 'processed' / 'samgeo_acotado'
                        / 'manglar_actual.geojson')
if manglar.crs is None:
    manglar.set_crs(4326, inplace=True)
manglar = manglar.to_crs(4326)
aoi_bounds = aoi.total_bounds  # xmin, ymin, xmax, ymax

# ------------------------------------------------------------------
# 2. Estaciones INVEMAR
# ------------------------------------------------------------------
stations = {
    'Isla Boquerón': (-74.298, 10.962),
    'Punta Cerro':   (-74.283, 10.973),
    'Punta Chino':   (-74.305, 10.912),
    'Río Sevilla':   (-74.325, 10.880),
    'Caño Palos':    (-74.471, 10.758),
}

# ------------------------------------------------------------------
# 3. Helpers
# ------------------------------------------------------------------
def add_scalebar(ax, length_km, label, y_frac=0.05, color='black', lat_ref=10.5):
    """Barra de escala simple en grados (aprox 1° lon ≈ 111 km * cos(lat))."""
    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()
    km_per_deg = 111.0 * np.cos(np.deg2rad(lat_ref))
    length_deg = length_km / km_per_deg
    x0 = xmin + (xmax - xmin) * 0.06
    y0 = ymin + (ymax - ymin) * y_frac
    ax.plot([x0, x0 + length_deg], [y0, y0], color=color, lw=3.5,
            solid_capstyle='butt', zorder=10)
    ax.text(x0 + length_deg / 2, y0 + (ymax - ymin) * 0.018, label,
            color=color, ha='center', va='bottom',
            fontsize=10, fontweight='bold', zorder=10,
            path_effects=[path_effects.Stroke(linewidth=2.5, foreground='white'),
                          path_effects.Normal()] if color == 'black' else
                         [path_effects.Stroke(linewidth=2.5, foreground='black'),
                          path_effects.Normal()])

def add_north(ax, color='black'):
    txt = ax.text(0.94, 0.94, 'N', transform=ax.transAxes,
                  fontsize=15, fontweight='bold', ha='center', va='top',
                  color=color)
    if color == 'white':
        txt.set_path_effects([path_effects.Stroke(linewidth=2.5, foreground='black'),
                              path_effects.Normal()])

# ------------------------------------------------------------------
# 4. Figura — 3 paneles
# ------------------------------------------------------------------
fig = plt.figure(figsize=(16, 11), facecolor='white')
gs = fig.add_gridspec(2, 2, width_ratios=[1, 2.4], height_ratios=[1, 1],
                      hspace=0.16, wspace=0.08,
                      left=0.04, right=0.98, top=0.95, bottom=0.05)

# --- (a) Colombia ----------------------------------------------------
ax_a = fig.add_subplot(gs[0, 0])
ax_a.set_facecolor('#CFE7F2')
co_dpts.boundary.plot(ax=ax_a, color='#999', lw=0.3)
colombia.plot(ax=ax_a, color='#FFFBEB', edgecolor='#444', lw=0.9)
magdalena.plot(ax=ax_a, color='#FF8C00', edgecolor='#A65000', lw=0.6, alpha=0.95)
ax_a.set_xlim(-82, -66); ax_a.set_ylim(-5, 13)
mc = magdalena.geometry.iloc[0].centroid
ax_a.annotate('Magdalena', xy=(mc.x, mc.y), xytext=(-74.5, 12.3),
              fontsize=12, ha='center', fontweight='bold',
              arrowprops=dict(arrowstyle='-', color='#444', lw=0.7))
ax_a.text(0.05, 0.95, '(a)', transform=ax_a.transAxes,
          fontsize=20, fontweight='bold', va='top')
add_north(ax_a)
ax_a.tick_params(labelsize=9)
add_scalebar(ax_a, 500, '500 km', y_frac=0.07, lat_ref=4)

# --- (b) Magdalena ---------------------------------------------------
ax_b = fig.add_subplot(gs[1, 0])
ax_b.set_facecolor('#CFE7F2')
co_dpts.boundary.plot(ax=ax_b, color='#888', lw=0.4)
magdalena.plot(ax=ax_b, color='#FF8C00', edgecolor='#A65000', lw=0.8, alpha=0.95)
# Bbox del AOI
rect = Rectangle((aoi_bounds[0], aoi_bounds[1]),
                 aoi_bounds[2] - aoi_bounds[0],
                 aoi_bounds[3] - aoi_bounds[1],
                 fill=False, edgecolor='#C0392B', lw=1.8, zorder=5)
ax_b.add_patch(rect)
ciudades = {
    'Santa Marta':  (-74.21, 11.24),
    'Ciénaga':      (-74.25, 11.00),
    'Barranquilla': (-74.80, 10.95),
}
for nombre, (lon, lat) in ciudades.items():
    ax_b.scatter(lon, lat, s=24, color='black', zorder=6)
    ax_b.annotate(nombre, xy=(lon, lat), xytext=(6, 6),
                  textcoords='offset points', fontsize=10,
                  bbox=dict(facecolor='white', alpha=0.85, edgecolor='none',
                            boxstyle='round,pad=0.25'), zorder=6)
ax_b.set_xlim(-75.6, -73.4); ax_b.set_ylim(9.3, 11.8)
ax_b.text(0.05, 0.95, '(b)', transform=ax_b.transAxes,
          fontsize=20, fontweight='bold', va='top')
ax_b.text(-74.4, 11.6, 'Caribbean Sea', fontsize=11, style='italic',
          color='#1A5490', ha='center', fontweight='bold')
ax_b.text(-74.5, 10.3, 'Magdalena', fontsize=13, fontweight='bold',
          ha='center', color='#7A3D0D')
add_north(ax_b)
ax_b.tick_params(labelsize=9)
add_scalebar(ax_b, 50, '50 km', y_frac=0.05, lat_ref=10.5)

# --- (c) Zoom CGSM con RGB ------------------------------------------
ax_c = fig.add_subplot(gs[:, 1])
# Prioridad: RGB extendido (cubre las 5 estaciones); fallback al original
rgb_wide = ROOT / 'data' / 'processed' / 'rgb_acotado_wide' / 'CGSM_RGB_actual_wide.tif'
rgb_orig = ROOT / 'data' / 'processed' / 'rgb_acotado' / 'CGSM_RGB_actual.tif'
rgb_path = rgb_wide if rgb_wide.exists() else rgb_orig
print(f'Leyendo {rgb_path.name}...')
with rasterio.open(rgb_path) as src:
    rgb = src.read([1, 2, 3]).astype(float)
    for i in range(3):
        valid = rgb[i][rgb[i] > 0]
        p2, p98 = np.percentile(valid, [2, 98])
        rgb[i] = np.clip((rgb[i] - p2) / (p98 - p2 + 1e-9), 0, 1)
    rgb_show = np.transpose(rgb, (1, 2, 0))
    extent_c = (src.bounds.left, src.bounds.right,
                src.bounds.bottom, src.bounds.top)
    src_crs = src.crs

print(f'  RGB CRS: {src_crs}, extent: {extent_c}')
ax_c.imshow(rgb_show, extent=extent_c, origin='upper', interpolation='nearest')

# Manglar (overlay) — opacidad menor para no tapar la imagen
manglar.plot(ax=ax_c, facecolor='#2ECC71', edgecolor='none', alpha=0.22, zorder=2)
# AOI
aoi.boundary.plot(ax=ax_c, edgecolor='#C0392B', lw=2.0, zorder=3)

# Halo grueso negro sobre texto blanco para legibilidad sobre cualquier fondo
halo_black = [path_effects.Stroke(linewidth=3.5, foreground='black'),
              path_effects.Normal()]

# Estaciones INVEMAR — con marcador más visible y etiquetas con offsets
# diferenciados para evitar solape entre Punta Cerro e Isla Boquerón
label_offset = {
    'Punta Cerro':   (-12, 8),   # arriba-izquierda
    'Isla Boquerón': (12, -10),  # abajo-derecha
    'Punta Chino':   (12, 6),    # derecha
    'Río Sevilla':   (12, 6),
    'Caño Palos':    (12, 6),
}
label_ha = {
    'Punta Cerro':   'right',
    'Isla Boquerón': 'left',
    'Punta Chino':   'left',
    'Río Sevilla':   'left',
    'Caño Palos':    'left',
}
for nombre, (lon, lat) in stations.items():
    ax_c.scatter(lon, lat, marker='^', s=170, color='#E74C3C',
                 edgecolor='white', lw=1.5, zorder=6)
    ax_c.annotate(nombre, xy=(lon, lat),
                  xytext=label_offset.get(nombre, (11, 7)),
                  textcoords='offset points', fontsize=10.5,
                  ha=label_ha.get(nombre, 'left'),
                  style='italic', fontweight='bold', color='#222',
                  bbox=dict(facecolor='white', alpha=0.92, edgecolor='#888',
                            lw=0.4, boxstyle='round,pad=0.3'), zorder=7)

# Etiquetas geográficas con halo negro para contraste sobre verde/azul
ax_c.text(-74.50, 10.90, 'Ciénaga\nGrande de\nSanta Marta',
          fontsize=14, style='italic', color='white', ha='center',
          fontweight='bold', path_effects=halo_black, zorder=4)
ax_c.text(-74.50, 11.05, 'Vía Parque Isla de Salamanca',
          fontsize=11, style='italic', color='white', ha='center',
          fontweight='bold', path_effects=halo_black, zorder=4)
# Mar Caribe — en el agua real visible al norte (lat ~11.08), no encima del título
ax_c.text(-74.55, 11.085, 'Mar Caribe', fontsize=13, style='italic',
          color='white', ha='center', fontweight='bold',
          path_effects=halo_black, zorder=4)

# Leyenda
legend_handles = [
    mpatches.Patch(facecolor='none', edgecolor='#C0392B', lw=2.0,
                   label='Área de estudio (1.286 km²)'),
    mpatches.Patch(facecolor='#00FF7F', alpha=0.4, edgecolor='none',
                   label='Manglar (SamGeo, 2024-2025)'),
    Line2D([0], [0], marker='^', color='w', markerfacecolor='#C0392B',
           markeredgecolor='black', markersize=12, lw=0,
           label=f'Estación INVEMAR ({len(stations)})'),
]
leg = ax_c.legend(handles=legend_handles, loc='upper left', fontsize=10.5,
                  framealpha=0.92, fancybox=True, edgecolor='#888')
leg.get_frame().set_linewidth(0.6)

ax_c.set_title('(c) Área de estudio — 1.286 km²', fontsize=15,
               fontweight='bold', pad=10)
# N un poco más adentro (0.92, 0.92) para que no roce el borde derecho
n_txt = ax_c.text(0.92, 0.92, 'N', transform=ax_c.transAxes,
                  fontsize=16, fontweight='bold', ha='center', va='top',
                  color='white')
n_txt.set_path_effects([path_effects.Stroke(linewidth=2.8, foreground='black'),
                        path_effects.Normal()])
ax_c.tick_params(labelsize=10)

# Si el RGB extendido existe, su propio extent cubre todas las estaciones
# (no hace falta extender X). Si es el fallback, extiendo igual que antes.
if rgb_path.name.endswith('_wide.tif'):
    ax_c.set_xlim(extent_c[0], extent_c[1])
else:
    station_xmax = max(lon for lon, _ in stations.values())
    ax_c.set_xlim(extent_c[0], max(extent_c[1], station_xmax + 0.02))
ax_c.set_ylim(extent_c[2], extent_c[3])
add_scalebar(ax_c, 10, '10 km', y_frac=0.04, color='white', lat_ref=10.8)

plt.savefig(OUT, dpi=180, bbox_inches='tight', facecolor='white')
plt.close(fig)

mb = OUT.stat().st_size / (1024 * 1024)
print(f'\nGuardado: {OUT}')
print(f'Tamaño: {mb:.1f} MB')
