"""
Regenera el dashboard CGSM como HTML autocontenido usando folium + Earth Engine.

A diferencia del notebook 06_dashboard.ipynb —que usa geemap.Map (ipyleaflet)
y produce un HTML solo abrible dentro de un kernel de Jupyter—, este script
construye el mapa con folium, de manera que el archivo se abre directamente en
cualquier navegador sin necesidad del entorno de widgets.

Los tiles de Earth Engine se sirven mediante mapId, con vigencia limitada de
algunas horas, por lo que conviene regenerar el HTML poco antes de presentar.

Uso:
    cd /home/rstudio/work/proyecto-cgsm
    python src/python/make_dashboard_html.py
"""
from pathlib import Path

import ee
import folium
import geopandas as gpd

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / 'outputs' / 'maps'
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_HTML = OUT_DIR / 'dashboard_CGSM_final.html'

try:
    ee.Initialize(project='basic-buttress-338101')
except Exception:
    # Fallback: usar Application Default Credentials de gcloud
    import google.auth
    creds, _ = google.auth.default()
    ee.Initialize(credentials=creds, project='basic-buttress-338101')


def add_ee_layer(self, ee_object, vis_params, name, shown=True, opacity=1.0):
    """Agrega una capa EE como TileLayer de folium."""
    try:
        img = ee.Image(ee_object)
    except Exception:
        img = ee_object  # FeatureCollection.style() ya devuelve un Image
    map_id_dict = img.getMapId(vis_params)
    folium.raster_layers.TileLayer(
        tiles=map_id_dict['tile_fetcher'].url_format,
        attr='Google Earth Engine',
        name=name,
        overlay=True,
        control=True,
        show=shown,
        opacity=opacity,
    ).add_to(self)


folium.Map.add_ee_layer = add_ee_layer

# --- AOI acotado oficial: SFF CGSM + Vía Parque Isla de Salamanca (RUNAP) ---
AOI_PATH = ROOT / 'data' / 'raw' / 'cgsm_aoi_acotado_4326.geojson'
gdf_aoi = gpd.read_file(AOI_PATH)
if gdf_aoi.crs is None or gdf_aoi.crs.to_epsg() != 4326:
    gdf_aoi = gdf_aoi.to_crs(4326)
geom_union = gdf_aoi.geometry.union_all()
aoi = ee.Geometry(geom_union.__geo_interface__)
centroid = geom_union.centroid
MAP_CENTER = [float(centroid.y), float(centroid.x)]
print(f'AOI acotado cargado: {len(gdf_aoi)} polígono(s), '
      f'centroide [{MAP_CENTER[0]:.3f}, {MAP_CENTER[1]:.3f}]')


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

srtm = ee.Image('USGS/SRTMGL1_003').clip(aoi)
elev_mask = srtm.lt(10)
jrc = ee.Image('JRC/GSW1_4/GlobalSurfaceWater').select('occurrence').clip(aoi)
near_water = jrc.gt(30).fastDistanceTransform().sqrt().multiply(30).lt(3000)

vis_ndvi   = {'min': -0.2, 'max': 0.8,
              'palette': ['#8B0000', '#D32F2F', '#FF6F00', '#FDD835',
                          '#7CB342', '#2E7D32', '#1B5E20']}
vis_change = {'min': -0.4, 'max': 0.4,
              'palette': ['#d73027', '#f46d43', '#fdae61', '#ffffbf',
                          '#a6d96a', '#66bd63', '#1a9850']}

ndvi_deg = s2.filterDate('2020-07-01', '2020-12-31').select('NDVI').median().clip(aoi)
ndvi_rec = s2.filterDate('2022-01-01', '2022-06-30').select('NDVI').median().clip(aoi)
ndvi_act = s2.filterDate('2024-07-01', '2025-06-30').select('NDVI').median().clip(aoi)
ndvi_change = ndvi_act.subtract(ndvi_deg)


def manglar(start, end):
    return (s2.filterDate(start, end).median().clip(aoi)
            .normalizedDifference(['B8', 'B4'])
            .gt(0.70).And(elev_mask).And(near_water).selfMask())


md = manglar('2020-07-01', '2020-12-31')
mr = manglar('2022-01-01', '2022-06-30')
ma = manglar('2024-07-01', '2025-06-30')

db = md.unmask(0).gt(0)
ab = ma.unmask(0).gt(0)
perdida  = db.And(ab.Not()).selfMask()
estable  = db.And(ab).selfMask()
ganancia = db.Not().And(ab).selfMask()

s1d = (ee.ImageCollection('COPERNICUS/S1_GRD')
       .filterBounds(aoi).filterDate('2020-01-01', '2020-03-31')
       .filter(ee.Filter.eq('instrumentMode', 'IW'))
       .select('VH').median().clip(aoi))
s1f = (ee.ImageCollection('COPERNICUS/S1_GRD')
       .filterBounds(aoi).filterDate('2020-09-01', '2020-10-31')
       .filter(ee.Filter.eq('instrumentMode', 'IW'))
       .select('VH').median().clip(aoi))
sar_diff = s1d.subtract(s1f)

stations = {
    'Isla Boqueron':  (-74.298, 10.962, 'I'),
    'Punta Cerro':    (-74.283, 10.973, 'I'),
    'Punta Chino':    (-74.305, 10.912, 'I'),
    'Rio Sevilla':    (-74.325, 10.880, 'I'),
    'Cano Palos':     (-74.471, 10.758, 'I'),
    'CP Pajarales':   (-74.75,  10.85,  'C'),
    'Cano Clarin':    (-74.55,  10.55,  'C'),
    'VIPIS':          (-74.65,  11.02,  'C'),
}
inv = [ee.Feature(ee.Geometry.Point([lon, lat]).buffer(500))
       for n, (lon, lat, t) in stations.items() if t == 'I']
com = [ee.Feature(ee.Geometry.Point([lon, lat]).buffer(500))
       for n, (lon, lat, t) in stations.items() if t == 'C']
ist = ee.FeatureCollection(inv).style(color='E91E63', fillColor='E91E6399', width=2)
cst = ee.FeatureCollection(com).style(color='FF9800', fillColor='FF980099', width=2)
styled_aoi = ee.FeatureCollection([ee.Feature(aoi)]).style(
    color='FF3333', fillColor='00000000', width=2)

# --- Construir mapa folium ---
m = folium.Map(location=MAP_CENTER, zoom_start=10, tiles=None,
               control_scale=True)

# Basemap Esri Topo
folium.TileLayer(
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}',
    attr='Tiles &copy; Esri',
    name='Esri WorldTopoMap', control=True).add_to(m)
folium.TileLayer('OpenStreetMap', name='OpenStreetMap').add_to(m)

# NDVI
m.add_ee_layer(ndvi_act,    vis_ndvi,   'NDVI Actual (2024-2025)',  shown=False)
m.add_ee_layer(ndvi_deg,    vis_ndvi,   'NDVI Degradacion (2020)',  shown=False)
m.add_ee_layer(ndvi_rec,    vis_ndvi,   'NDVI Recuperacion (2022)', shown=False)
m.add_ee_layer(ndvi_change, vis_change, 'Cambio NDVI',              shown=False)

# Manglar por período
m.add_ee_layer(md, {'palette': ['#E57373']}, 'Manglar Degradacion (2020)',  shown=False, opacity=0.75)
m.add_ee_layer(mr, {'palette': ['#FFB74D']}, 'Manglar Recuperacion (2022)', shown=False, opacity=0.75)
m.add_ee_layer(ma, {'palette': ['#81C784']}, 'Manglar Actual (2024-2025)',  shown=False, opacity=0.75)

# Cambios
m.add_ee_layer(perdida,  {'palette': ['#EF5350']}, 'Perdida manglar',  shown=True, opacity=0.8)
m.add_ee_layer(estable,  {'palette': ['#66BB6A']}, 'Manglar estable',  shown=True, opacity=0.8)
m.add_ee_layer(ganancia, {'palette': ['#42A5F5']}, 'Ganancia manglar', shown=True, opacity=0.8)

# SAR
m.add_ee_layer(sar_diff.gt(3).selfMask(),  {'palette': ['#4DD0E1']}, 'Inundacion agua abierta', shown=False, opacity=0.7)
m.add_ee_layer(sar_diff.lt(-2).selfMask(), {'palette': ['#CE93D8']}, 'Inundacion bajo dosel',   shown=False, opacity=0.7)

# AOI y estaciones
m.add_ee_layer(styled_aoi, {}, 'Area de estudio')
m.add_ee_layer(ist,        {}, 'Estaciones INVEMAR')
m.add_ee_layer(cst,        {}, 'Estaciones complementarias')

folium.LayerControl(collapsed=False).add_to(m)
m.save(str(OUT_HTML))

print(f'Dashboard exportado: {OUT_HTML}')
print(f'Tamano: {OUT_HTML.stat().st_size / 1024:.0f} KB')
