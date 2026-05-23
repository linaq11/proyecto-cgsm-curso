"""
diagnose_ndvi_year.py — diagnóstico del bug del slider NDVI año.

Replica EXACTAMENTE la construcción de imágenes que hace make_dashboard_html.py
y reporta, año por año:
  - cuántas imágenes Sentinel-2 sobreviven al filtro
  - si la composite mediana tiene datos válidos sobre la CGSM
  - si el mapId generado devuelve tiles con contenido o transparentes

Uso:
    cd /home/rstudio/work/proyecto-cgsm
    python src/python/diagnose_ndvi_year.py
"""
from pathlib import Path
import json
import urllib.request
import urllib.error
import ee
import geopandas as gpd

# === Setup idéntico a make_dashboard_html.py ===
PROJECT = 'basic-buttress-338101'
ee.Initialize(project=PROJECT)
print(f'[OK] Earth Engine inicializado: project={PROJECT}\n')

ROOT = Path(__file__).resolve().parents[2]
AOI_PATH = ROOT / 'data' / 'raw' / 'cgsm_aoi_acotado_4326.geojson'
gdf_aoi = gpd.read_file(AOI_PATH)
if gdf_aoi.crs is None or gdf_aoi.crs.to_epsg() != 4326:
    gdf_aoi = gdf_aoi.to_crs(4326)
geom_union = gdf_aoi.geometry.union_all()
aoi = ee.Geometry(geom_union.__geo_interface__)
area_km2 = aoi.area().divide(1e6).getInfo()
bounds = geom_union.bounds  # (minx, miny, maxx, maxy)
print(f'[OK] AOI cargado: {len(gdf_aoi)} polígono(s), área = {area_km2:.1f} km²')
print(f'     bbox: lon [{bounds[0]:.3f}, {bounds[2]:.3f}], '
      f'lat [{bounds[1]:.3f}, {bounds[3]:.3f}]\n')


def mask_s2(image):
    qa = image.select('QA60')
    return image.updateMask(
        qa.bitwiseAnd(1 << 10).eq(0).And(qa.bitwiseAnd(1 << 11).eq(0)))


def add_idx(image):
    ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')
    ndwi = image.normalizedDifference(['B3', 'B8']).rename('NDWI')
    return image.addBands([ndvi, ndwi, ndvi.subtract(ndwi).rename('CMRI')])


s2 = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
      .filterBounds(aoi)
      .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
      .map(mask_s2).map(add_idx))

vis_ndvi = {'min': -0.2, 'max': 0.8,
            'palette': ['#8B0000', '#D32F2F', '#FF6F00', '#FDD835',
                        '#7CB342', '#2E7D32', '#1B5E20']}

# === Test 1: conteo de imágenes por año (pre y post filtros) ===
print('=' * 70)
print('TEST 1 — Cuántas imágenes Sentinel-2 quedan por año')
print('=' * 70)
print(f'{"Año":<6}{"Sin filtro":>14}{"CLOUDY<20":>14}{"Veredicto":>20}')
s2_raw = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
          .filterBounds(aoi))
for y in range(2018, 2026):
    n_raw = s2_raw.filterDate(f'{y}-01-01', f'{y+1}-01-01').size().getInfo()
    n_filtered = s2.filterDate(f'{y}-01-01', f'{y+1}-01-01').size().getInfo()
    verdict = 'OK' if n_filtered >= 3 else ('VACÍO ❌' if n_filtered == 0 else 'POCAS ⚠')
    print(f'{y:<6}{n_raw:>14}{n_filtered:>14}{verdict:>20}')
print()

# === Test 2: la mediana tiene valores válidos NDVI sobre CGSM? ===
print('=' * 70)
print('TEST 2 — Reducer.mean del NDVI mediano sobre el centroide del AOI')
print('         (None = imagen vacía / sin píxeles válidos)')
print('=' * 70)
print(f'{"Año":<6}{"NDVI_min":>12}{"NDVI_mean":>12}{"NDVI_max":>12}{"Veredicto":>20}')
for y in range(2018, 2026):
    img = (s2.filterDate(f'{y}-01-01', f'{y+1}-01-01')
           .select('NDVI').median().clip(aoi))
    try:
        stats = img.reduceRegion(
            reducer=ee.Reducer.minMax().combine(ee.Reducer.mean(), '', True),
            geometry=aoi, scale=100, maxPixels=1e8, bestEffort=True
        ).getInfo()
        nmin = stats.get('NDVI_min')
        nmean = stats.get('NDVI_mean')
        nmax = stats.get('NDVI_max')
        if nmean is None:
            verdict = 'VACÍO ❌'
            nmin_s, nmean_s, nmax_s = 'None', 'None', 'None'
        else:
            verdict = 'OK' if -0.2 < nmean < 0.8 else 'fuera de rango'
            nmin_s = f'{nmin:.3f}' if nmin is not None else 'None'
            nmean_s = f'{nmean:.3f}'
            nmax_s = f'{nmax:.3f}' if nmax is not None else 'None'
        print(f'{y:<6}{nmin_s:>12}{nmean_s:>12}{nmax_s:>12}{verdict:>20}')
    except Exception as e:
        print(f'{y:<6}   ERROR: {type(e).__name__}: {str(e)[:50]}')
print()

# === Test 3: getMapId y fetch directo de un tile ===
print('=' * 70)
print('TEST 3 — Generar mapId y descargar un tile real sobre CGSM')
print('         (esperado: >1 KB con bytes de PNG con data)')
print('=' * 70)
print(f'{"Año":<6}{"Tile bytes":>14}{"Veredicto":>30}')
for y in [2020, 2022, 2024]:
    img = (s2.filterDate(f'{y}-01-01', f'{y+1}-01-01')
           .select('NDVI').median().clip(aoi))
    try:
        mid = img.getMapId(vis_ndvi)
        url_template = mid['tile_fetcher'].url_format
        # tile sobre el centro de la CGSM en zoom 11
        url = (url_template.replace('{z}', '11')
               .replace('{x}', '610').replace('{y}', '927'))
        with urllib.request.urlopen(url, timeout=20) as r:
            data = r.read()
        verdict = ('OK con data' if len(data) > 1000
                   else f'TRANSPARENTE ({len(data)}B) ❌')
        print(f'{y:<6}{len(data):>14}{verdict:>30}')
    except urllib.error.HTTPError as e:
        print(f'{y:<6}   HTTP {e.code}: {e.reason}')
    except Exception as e:
        print(f'{y:<6}   ERROR: {type(e).__name__}: {str(e)[:50]}')
print()

print('=' * 70)
print('Si TEST 1 muestra muchos años con 0-2 imágenes → filtro CLOUDY_PIXEL')
print('  muy estricto. Subir el umbral a 60 en make_dashboard_html.py.')
print('Si TEST 1 muestra imágenes pero TEST 2 da None → problema con la')
print('  máscara QA60 o el AOI. Revisar mask_s2 o el geometry del AOI.')
print('Si TEST 2 da valores pero TEST 3 da tiles transparentes → bug del')
print('  visParams o de getMapId. Probar sin clip(aoi).')
print('=' * 70)
