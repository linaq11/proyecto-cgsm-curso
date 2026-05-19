"""
Descarga un composite RGB Sentinel-2 que cubre el AOI + las 5 estaciones
INVEMAR (incluyendo Isla Boquerón, Punta Cerro y Punta Chino que quedan
al este del recorte original).

Periodo: 2024-07 a 2025-06 (mismo periodo 'actual' del informe).
Resolución: 30 m (suficiente para figura de área de estudio).
Salida: data/processed/rgb_acotado_wide/CGSM_RGB_actual_wide.tif

Uso (requiere autenticación GEE previa):
    cd /home/rstudio/work/proyecto-cgsm
    python src/python/descargar_rgb_extendido.py
"""
from pathlib import Path

import ee
import geemap
import geopandas as gpd

ROOT    = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / 'data' / 'processed' / 'rgb_acotado_wide'
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_TIF = OUT_DIR / 'CGSM_RGB_actual_wide.tif'

# ---- Auth GEE ----
try:
    ee.Initialize(project='basic-buttress-338101')
except Exception:
    import google.auth
    creds, _ = google.auth.default()
    ee.Initialize(credentials=creds, project='basic-buttress-338101')

# ---- Bounding box: AOI + estaciones + padding ----
AOI_PATH = ROOT / 'data' / 'raw' / 'cgsm_aoi_acotado_4326.geojson'
gdf_aoi = gpd.read_file(AOI_PATH).to_crs(4326)
aoi_b = gdf_aoi.total_bounds  # xmin, ymin, xmax, ymax

stations = {
    'Isla Boquerón': (-74.298, 10.962),
    'Punta Cerro':   (-74.283, 10.973),
    'Punta Chino':   (-74.305, 10.912),
    'Río Sevilla':   (-74.325, 10.880),
    'Caño Palos':    (-74.471, 10.758),
}
stx = [lon for lon, _ in stations.values()]
sty = [lat for _, lat in stations.values()]

pad = 0.02
xmin = min(aoi_b[0], min(stx)) - pad
ymin = min(aoi_b[1], min(sty)) - pad
xmax = max(aoi_b[2], max(stx)) + pad
ymax = max(aoi_b[3], max(sty)) + pad

bbox = ee.Geometry.BBox(xmin, ymin, xmax, ymax)
print(f'BBox extendido: [{xmin:.4f}, {ymin:.4f}, {xmax:.4f}, {ymax:.4f}]')
print(f'  Ancho: {(xmax-xmin)*111:.1f} km, Alto: {(ymax-ymin)*111:.1f} km')


def mask_s2(img):
    qa = img.select('QA60')
    return img.updateMask(
        qa.bitwiseAnd(1 << 10).eq(0).And(qa.bitwiseAnd(1 << 11).eq(0)))


s2 = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
      .filterBounds(bbox)
      .filterDate('2024-07-01', '2025-06-30')
      .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
      .map(mask_s2))

n_imgs = s2.size().getInfo()
print(f'Composite de {n_imgs} imágenes S2 (2024-07 a 2025-06, <20% nubes)')

# RGB real-color con B4 (rojo), B3 (verde), B2 (azul)
rgb = s2.median().select(['B4', 'B3', 'B2']).clip(bbox)

print(f'\nDescargando a {OUT_TIF.name} (puede tardar 1-3 min)...')

# Estrategia 1: download_ee_image (auto-tilea, mantiene 30 m)
try:
    geemap.download_ee_image(rgb, str(OUT_TIF), scale=30, region=bbox,
                             crs='EPSG:4326')
    print('  Descarga 30 m con tiling exitosa.')
except Exception as e:
    print(f'  Tiling 30 m falló ({e}); reintentando a 60 m sin tiling...')
    # Estrategia 2: ee_export_image a 60 m (1/4 del tamaño, cabe en el limite)
    geemap.ee_export_image(rgb, str(OUT_TIF), scale=60, region=bbox,
                           file_per_band=False)
    print('  Descarga 60 m exitosa.')

if OUT_TIF.exists():
    mb = OUT_TIF.stat().st_size / (1024 * 1024)
    print(f'\nListo: {OUT_TIF} ({mb:.1f} MB)')
else:
    print('\nERROR: archivo no se creó. Revisa autenticación GEE.')
