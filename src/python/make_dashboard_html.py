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
import pandas as pd

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
    """Agrega una capa EE como TileLayer de folium y la devuelve para agruparla después.

    NOTA 1: usa el patrón .visualize(**vis).getMapId() en lugar de .getMapId(vis)
    porque la combinación clip(aoi)+getMapId(visParams) tiene un bug conocido
    en GEE Python API que devuelve tiles PNG completamente transparentes
    (334 B exactos) cuando la imagen está clippeada.

    NOTA 2: las capas raster EE se asignan al pane 'eeRasterPane' (z-index 450)
    para que se rendericen ENCIMA de los polígonos vectoriales (overlayPane
    z=400) y debajo de los markers (markerPane z=600). Sin esto, los polígonos
    de manglar estable/gain/loss tapaban completamente las capas NDVI raster.
    Requiere add_ee_pane(map) al inicio.
    """
    try:
        img = ee.Image(ee_object)
    except Exception:
        img = ee_object  # FeatureCollection.style() ya devuelve un Image
    if vis_params:
        img = img.visualize(**vis_params)
    map_id_dict = img.getMapId()
    tl = folium.raster_layers.TileLayer(
        tiles=map_id_dict['tile_fetcher'].url_format,
        attr='Google Earth Engine',
        name=name,
        overlay=True,
        control=True,
        show=shown,
        opacity=opacity,
        pane='eeRasterPane',
    )
    tl.add_to(self)
    return tl


folium.Map.add_ee_layer = add_ee_layer


# Helper que inyecta el createPane('eeRasterPane') en el HTML del mapa.
# DEBE llamarse DESPUÉS de crear el mapa y ANTES de la primera add_ee_layer.
from jinja2 import Template
import folium as _folium_mod

class _EERasterPane(_folium_mod.MacroElement):
    _template = Template("""
        {% macro script(this, kwargs) %}
            {{this._parent.get_name()}}.createPane('eeRasterPane');
            {{this._parent.get_name()}}.getPane('eeRasterPane').style.zIndex = 450;
            {{this._parent.get_name()}}.getPane('eeRasterPane').style.pointerEvents = 'none';
        {% endmacro %}
    """)

def add_ee_raster_pane(m):
    """Crea el pane eeRasterPane (z=450) en el mapa. Llamar UNA VEZ después de folium.Map()."""
    m.add_child(_EERasterPane())

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

# --- NDVI anual para slider temporal (2018-2025) ---
YEARS_SLIDER = list(range(2018, 2026))
ndvi_anual = {y: s2.filterDate(f'{y}-01-01', f'{y+1}-01-01').select('NDVI')
              .median().clip(aoi) for y in YEARS_SLIDER}
print(f'Composites NDVI anuales para slider: {YEARS_SLIDER}')


def manglar(start, end):
    return (s2.filterDate(start, end).median().clip(aoi)
            .normalizedDifference(['B8', 'B4'])
            .gt(0.70).And(elev_mask).And(near_water).selfMask())


md = manglar('2020-07-01', '2020-12-31')
mr = manglar('2022-01-01', '2022-06-30')
ma = manglar('2024-07-01', '2025-06-30')

# === Clasificador Random Forest (notebook 11) ===
# Replica del clasificador supervisado entrenado con 1.000 puntos estratificados
# sobre ESA WorldCover v200 (F1=0,889 contra WorldCover; F1=0,826 contra INVEMAR).
# Usa la misma mediana Sentinel-2 del periodo actual y las 15 variables predictoras.
print('Entrenando Random Forest sobre WorldCover (esto tarda 1-2 min)...')
img_rf = (s2.filterDate('2024-07-01', '2025-06-30')
          .median()
          .select(['B2','B3','B4','B5','B6','B7','B8','B8A','B11','B12',
                   'NDVI','NDWI','CMRI'])
          .addBands(srtm.rename('ELEV'))
          .addBands(jrc.unmask(0).rename('JRC_OCC'))
          .clip(aoi))
BANDAS_RF = img_rf.bandNames()

wc = ee.Image('ESA/WorldCover/v200/2021').select('Map').clip(aoi)
wc_mangrove = wc.eq(95).rename('mangrove')   # clase 95 = manglar

muestras = wc_mangrove.addBands(img_rf).stratifiedSample(
    numPoints=500, classBand='mangrove', region=aoi, scale=10, seed=42,
    geometries=False)

rf = (ee.Classifier.smileRandomForest(numberOfTrees=100, minLeafPopulation=5,
                                       seed=42)
      .train(features=muestras, classProperty='mangrove',
             inputProperties=BANDAS_RF))

ma_rf = img_rf.classify(rf).rename('manglar_rf').eq(1).selfMask().clip(aoi)
print('  Random Forest listo, generando tile...')

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

# Las 8 estaciones canónicas del proyecto (5 INVEMAR-GBIF + 3 complementarias)
stations = {
    'Isla Boqueron':   (-74.298, 10.962, 'I'),
    'Punta Cerro':     (-74.283, 10.973, 'I'),
    'Punta Chino':     (-74.305, 10.912, 'I'),
    'Rio Sevilla':     (-74.325, 10.880, 'I'),
    'Cano Palos':      (-74.471, 10.758, 'I'),
    'CP Luna':         (-74.560, 10.870, 'C'),
    'CP Aguas Negras': (-74.570, 10.800, 'C'),
    'Cano Clarin':     (-74.500, 10.600, 'C'),
}

# === Cargar estado semáforo (Digital Twin Nivel 2) ===
ALERTAS_CSV = ROOT / 'outputs' / 'tables' / 'alertas_estaciones.csv'
ESTADO_COLORS = {'estable': '#43A047', 'alerta': '#FBC02D',
                 'critica': '#D32F2F', 'sin_datos': '#9E9E9E'}
ESTADO_ICON = {'estable': '🟢', 'alerta': '🟡',
               'critica': '🔴', 'sin_datos': '⚪'}

if ALERTAS_CSV.exists():
    df_alertas = pd.read_csv(ALERTAS_CSV)
    estado_por_estacion = {
        row['estacion'].replace('_', ' '): {
            'estado': row['estado'],
            'razon': row.get('razon', ''),
            'z_actual': row.get('z_actual', None),
            'ndvi_actual': row.get('ndvi_actual', None),
        }
        for _, row in df_alertas.iterrows()
    }
    conteo_estados = df_alertas['estado'].value_counts().to_dict()
    print(f'Estado semáforo cargado: {conteo_estados}')
else:
    estado_por_estacion = {}
    conteo_estados = {}
    print('AVISO: alertas_estaciones.csv no encontrado, se usará coloreo por fuente')
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

# Crear pane dedicado eeRasterPane (z=450) ANTES de cualquier add_ee_layer.
# Esto es lo que hace visibles las capas raster NDVI por encima de los polígonos
# vectoriales (overlayPane z=400). Sin esto, el clasificador / NDVI estáticos
# quedan tapados por los polígonos verdes/azules de manglar y nunca se ven.
add_ee_raster_pane(m)

# Basemap Esri Topo
folium.TileLayer(
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}',
    attr='Tiles &copy; Esri',
    name='Esri WorldTopoMap', control=True).add_to(m)
folium.TileLayer('OpenStreetMap', name='OpenStreetMap').add_to(m)

# --- Capas NDVI por periodo ---
ly_ndvi_act = m.add_ee_layer(ndvi_act,    vis_ndvi,   'NDVI Actual (2024-2025)',  shown=False)
ly_ndvi_deg = m.add_ee_layer(ndvi_deg,    vis_ndvi,   'NDVI Degradación (2020)',  shown=False)
ly_ndvi_rec = m.add_ee_layer(ndvi_rec,    vis_ndvi,   'NDVI Recuperación (2022)', shown=False)
ly_ndvi_chg = m.add_ee_layer(ndvi_change, vis_change, 'Cambio NDVI (Actual − Degradación)', shown=False)

# --- Manglar por periodo (clasificación) ---
ly_md = m.add_ee_layer(md, {'palette': ['#E57373']}, 'Manglar Degradación (2020, umbrales)',  shown=False, opacity=0.75)
ly_mr = m.add_ee_layer(mr, {'palette': ['#FFB74D']}, 'Manglar Recuperación (2022, umbrales)', shown=False, opacity=0.75)
ly_ma = m.add_ee_layer(ma, {'palette': ['#81C784']}, 'Manglar Actual (2024-2025, umbrales · F1=0,55)',  shown=False, opacity=0.75)
ly_rf = m.add_ee_layer(ma_rf, {'palette': ['#2E7D32']}, 'Manglar Actual (Random Forest · F1=0,83)', shown=False, opacity=0.80)

# --- Dinámica de cambio 2020 → 2024-2025 ---
ly_perdida  = m.add_ee_layer(perdida,  {'palette': ['#EF5350']}, 'Pérdida de manglar',  shown=True, opacity=0.8)
ly_estable  = m.add_ee_layer(estable,  {'palette': ['#66BB6A']}, 'Manglar estable',     shown=True, opacity=0.8)
ly_ganancia = m.add_ee_layer(ganancia, {'palette': ['#42A5F5']}, 'Ganancia de manglar', shown=True, opacity=0.8)

# --- Inundación (SAR sept 2020) ---
ly_sar_open = m.add_ee_layer(sar_diff.gt(3).selfMask(),  {'palette': ['#4DD0E1']}, 'SAR · Inundación agua abierta', shown=False, opacity=0.7)
ly_sar_dose = m.add_ee_layer(sar_diff.lt(-2).selfMask(), {'palette': ['#CE93D8']}, 'SAR · Inundación bajo dosel',   shown=False, opacity=0.7)

# --- Referencia / contexto ---
ly_aoi = m.add_ee_layer(styled_aoi, {}, 'Área de estudio (SFF + VPI)')
ly_inv_buf = m.add_ee_layer(ist, {}, 'Estaciones INVEMAR')
ly_com_buf = m.add_ee_layer(cst, {}, 'Estaciones complementarias')

# === Marcadores de estaciones (siempre visibles, capa principal) ===
from folium import FeatureGroup, CircleMarker, Marker
from folium.features import DivIcon

manglar_set     = {'Cano Palos', 'Cano Clarin', 'CP Aguas Negras', 'CP Luna'}
limnologica_set = {'Isla Boqueron', 'Punta Cerro', 'Punta Chino', 'Rio Sevilla'}

# FeatureGroups por estado — sin entrada en LayerControl, controlables desde
# el panel de filtros que se inyecta abajo.
fg_estable = FeatureGroup(name='__fg_estable', show=True, control=False)
fg_alerta  = FeatureGroup(name='__fg_alerta',  show=True, control=False)
fg_critica = FeatureGroup(name='__fg_critica', show=True, control=False)
fg_sindat  = FeatureGroup(name='__fg_sindatos', show=True, control=False)
fg_por_estado = {'estable': fg_estable, 'alerta': fg_alerta,
                 'critica': fg_critica, 'sin_datos': fg_sindat}

# Centroides de estaciones — coloreados por estado semáforo del módulo de alertas
# tempranas (Digital Twin Nivel 2). Si no hay alertas disponibles, se vuelve al
# coloreo por fuente como respaldo visual.
for nombre, (lon, lat, tipo) in stations.items():
    fuente     = 'INVEMAR-GBIF' if tipo == 'I' else 'Complementaria'
    naturaleza = 'manglar' if nombre in manglar_set else 'limnológica'

    info = estado_por_estacion.get(nombre, {})
    estado = info.get('estado', 'sin_datos')
    color  = ESTADO_COLORS.get(estado, '#9E9E9E')
    icono  = ESTADO_ICON.get(estado, '⚪')

    z_str    = f"{info.get('z_actual'):+.2f}" if info.get('z_actual') is not None else '—'
    ndvi_str = f"{info.get('ndvi_actual'):.3f}" if info.get('ndvi_actual') is not None else '—'
    razon    = info.get('razon', 'Sin información de alertas')

    marker = CircleMarker(
        location=[lat, lon],
        radius=7,
        color='white',
        weight=2,
        fill=True,
        fill_color=color,
        fill_opacity=0.95,
        tooltip=folium.Tooltip(
            f'<b>{icono} {nombre}</b><br>'
            f'<span style="font-size:10px">Estado: <b>{estado}</b> · '
            f'{naturaleza} · {fuente}</span>',
            sticky=False,
        ),
        popup=folium.Popup(
            f'<b>{icono} {nombre}</b><br>'
            f'<b>Estado semáforo:</b> {estado}<br>'
            f'<b>Naturaleza espectral:</b> {naturaleza}<br>'
            f'<b>Fuente:</b> {fuente}<br>'
            f'<b>z NDVI actual:</b> {z_str} · <b>NDVI:</b> {ndvi_str}<br>'
            f'<b>Razón:</b> {razon}<br>'
            f'<b>Coords:</b> {lat:.4f}, {lon:.4f}',
            max_width=300,
        ),
    )
    marker.add_to(fg_por_estado.get(estado, fg_sindat))

# Agregar los grupos al mapa
fg_estable.add_to(m)
fg_alerta.add_to(m)
fg_critica.add_to(m)
fg_sindat.add_to(m)

# Capa 2: etiquetas con nombres (sin fondo, opcional/prendible-apagable)
grupo_etiquetas = FeatureGroup(name='Etiquetas de estaciones', show=False)

# Offsets de label personalizados para estaciones muy cercanas entre sí.
# DivIcon icon_anchor=(x, y): el pixel (x,y) del icon queda EN la coord
# geográfica. Por defecto (70, -10) centra y desplaza arriba.
#   Isla Boqueron y Punta Cerro están a ~1.2 km → uno arriba, otro abajo
#   CP Luna y CP Aguas Negras están a ~7.7 km → mismo tratamiento por
#   precaución a zoom medio
LABEL_ANCHOR_DEFAULT = (70, -10)
label_anchors = {
    'Isla Boqueron':   (70, -22),   # label más arriba
    'Punta Cerro':     (70,  22),   # label más abajo
    'CP Luna':         (70, -22),
    'CP Aguas Negras': (70,  22),
}

for nombre, (lon, lat, tipo) in stations.items():
    naturaleza = 'manglar' if nombre in manglar_set else 'limnológica'
    color_texto = '#1B5E20' if naturaleza == 'manglar' else '#01579B'

    # Texto sin fondo, con borde blanco para legibilidad sobre cualquier basemap
    Marker(
        location=[lat, lon],
        icon=DivIcon(
            icon_size=(140, 18),
            icon_anchor=label_anchors.get(nombre, LABEL_ANCHOR_DEFAULT),
            html=(f'<div style="font-size:10px; font-weight:600; '
                  f'color:{color_texto}; text-align:center; white-space:nowrap; '
                  f'text-shadow: -1px -1px 0 white, 1px -1px 0 white, '
                  f'-1px 1px 0 white, 1px 1px 0 white, '
                  f'-1.5px 0 0 white, 1.5px 0 0 white, '
                  f'0 -1.5px 0 white, 0 1.5px 0 white;">{nombre}</div>')
        ),
    ).add_to(grupo_etiquetas)

grupo_etiquetas.add_to(m)

# === Capa nueva: cartografía oficial INVEMAR 1:25.000 (referencia nacional) ===
INVEMAR_GEOJSON = ROOT / 'data' / 'validation' / 'invemar_manglar_25k.geojson'
invemar_layer = None
if INVEMAR_GEOJSON.exists():
    print('Agregando capa INVEMAR 1:25.000...')
    invemar_layer = folium.GeoJson(
        str(INVEMAR_GEOJSON),
        name='INVEMAR 1:25.000 (referencia oficial)',
        style_function=lambda x: {
            'fillColor': '#FFD600',
            'color': '#F57F17',
            'weight': 0.6,
            'fillOpacity': 0.35,
        },
        tooltip=folium.GeoJsonTooltip(
            fields=['AREA_HA', 'COBERTURA', 'DeNombre'],
            aliases=['Área (ha):', 'Cobertura:', 'Departamento:'],
            sticky=True,
        ),
        show=False,
    )
    invemar_layer.add_to(m)

# === Capa nueva: frecuencia histórica de inundación GFD 2001-2017 ===
print('Agregando capa GFD frecuencia de inundación histórica...')
gfd = (ee.ImageCollection('GLOBAL_FLOOD_DB/MODIS_EVENTS/V1')
       .filterBounds(aoi)
       .select('flooded'))
gfd_freq = gfd.sum().clip(aoi).selfMask().rename('eventos_inundacion')
vis_gfd = {'min': 1, 'max': 16, 'palette': ['#FFF59D', '#FB8C00', '#D32F2F', '#6A1B9A']}
ly_gfd = m.add_ee_layer(gfd_freq, vis_gfd,
                        'Frecuencia inundación GFD (2001-2017)',
                        shown=False, opacity=0.7)

# === Control de capas agrupado por temática ===
from folium.plugins import GroupedLayerControl

# LayerControl básico (lo necesita Folium para el manejo interno)
folium.LayerControl(collapsed=False, position='topright').add_to(m)

# GroupedLayerControl encima, con grupos temáticos colapsables
GroupedLayerControl(
    groups={
        'Estado del manglar (NDVI)': [ly_ndvi_act, ly_ndvi_deg, ly_ndvi_rec, ly_ndvi_chg],
        'Clasificación por periodo': [ly_md, ly_mr, ly_ma, ly_rf],
        'Dinámica de cambio 2020→2024': [ly_perdida, ly_estable, ly_ganancia],
        'Inundación SAR sept-2020': [ly_sar_open, ly_sar_dose],
        'Estaciones y AOI': [ly_aoi, grupo_etiquetas, ly_inv_buf, ly_com_buf],
        'Referencias cartográficas': [
            x for x in [invemar_layer, ly_gfd] if x is not None
        ],
    },
    exclusive_groups=False,
    collapsed=False,
).add_to(m)


# === Inyección de simbología en cada label del control de capas ===
from branca.element import MacroElement
from jinja2 import Template

class LegendInjector(MacroElement):
    """Añade un cuadrito de color al lado de cada nombre de capa
    en el control de capas (basado en el texto del label)."""
    def __init__(self):
        super().__init__()
        self._template = Template("""
{% macro script(this, kwargs) %}
setTimeout(function () {
  var simbolos = {
    'NDVI Actual': {tipo:'grad', from:'#D32F2F', to:'#1B5E20'},
    'NDVI Degradación': {tipo:'grad', from:'#D32F2F', to:'#1B5E20'},
    'NDVI Recuperación': {tipo:'grad', from:'#D32F2F', to:'#1B5E20'},
    'Cambio NDVI': {tipo:'grad', from:'#d73027', to:'#1a9850'},
    'Manglar Degradación': {tipo:'fill', color:'#E57373'},
    'Manglar Recuperación': {tipo:'fill', color:'#FFB74D'},
    'Manglar Actual (2024-2025, umbrales': {tipo:'fill', color:'#81C784'},
    'Manglar Actual (Random Forest': {tipo:'fill', color:'#2E7D32'},
    'Pérdida de manglar': {tipo:'fill', color:'#EF5350'},
    'Manglar estable': {tipo:'fill', color:'#66BB6A'},
    'Ganancia de manglar': {tipo:'fill', color:'#42A5F5'},
    'SAR · Inundación agua abierta': {tipo:'fill', color:'#4DD0E1'},
    'SAR · Inundación bajo dosel': {tipo:'fill', color:'#CE93D8'},
    'Área de estudio': {tipo:'border', color:'#FF3333'},
    'Etiquetas de estaciones': {tipo:'text', color:'#1B5E20'},
    'Estaciones INVEMAR': {tipo:'fill', color:'#E91E63', op:0.6},
    'Estaciones complementarias': {tipo:'fill', color:'#FF9800', op:0.6},
    'INVEMAR 1:25.000': {tipo:'fill', color:'#FFD600', op:0.5},
    'Frecuencia inundación GFD': {tipo:'grad', from:'#FFF59D', to:'#6A1B9A'}
  };

  function svg_para(s) {
    if (s.tipo === 'fill') {
      return '<span style="display:inline-block;width:14px;height:12px;background:'+s.color+
             ';opacity:'+(s.op||0.9)+';border:1px solid #555;border-radius:2px;'+
             'margin-right:6px;vertical-align:middle;"></span>';
    } else if (s.tipo === 'grad') {
      return '<span style="display:inline-block;width:24px;height:10px;'+
             'background:linear-gradient(to right,'+s.from+','+s.to+');'+
             'border:1px solid #555;border-radius:2px;margin-right:6px;vertical-align:middle;"></span>';
    } else if (s.tipo === 'circle') {
      return '<span style="display:inline-block;width:12px;height:12px;background:'+s.color+
             ';border:2px solid white;border-radius:50%;box-shadow:0 0 0 1px #555;'+
             'margin-right:6px;vertical-align:middle;"></span>';
    } else if (s.tipo === 'border') {
      return '<span style="display:inline-block;width:14px;height:10px;background:transparent;'+
             'border:2px solid '+s.color+';margin-right:6px;vertical-align:middle;"></span>';
    } else if (s.tipo === 'text') {
      return '<span style="display:inline-block;width:14px;height:12px;color:'+s.color+
             ';font-weight:700;font-size:10px;margin-right:6px;vertical-align:middle;'+
             'text-align:center;line-height:12px;">Aa</span>';
    }
    return '';
  }

  var labels = document.querySelectorAll('.leaflet-control-layers-overlays label, .leaflet-control-layers label');
  labels.forEach(function(label) {
    var span = label.querySelector('span');
    if (!span || span.dataset.legendified === 'true') return;
    var texto = span.textContent.trim();
    for (var key in simbolos) {
      if (texto.indexOf(key) !== -1) {
        span.insertAdjacentHTML('afterbegin', svg_para(simbolos[key]));
        span.dataset.legendified = 'true';
        break;
      }
    }
  });

  // Inyectar CSS de leyenda redesignada (Inter, grupos destacados, espaciado)
  if (!document.getElementById('cgsm-legend-style')) {
    var st = document.createElement('style');
    st.id = 'cgsm-legend-style';
    st.textContent = `
      .leaflet-control-layers {
        font-family: 'Inter', -apple-system, 'Segoe UI', sans-serif !important;
        font-size: 12px !important; line-height: 1.5 !important;
        max-width: 340px !important; padding: 0 !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 16px rgba(0,0,0,0.12) !important;
        border: 1px solid #e6e8ec !important;
        background: rgba(255,255,255,0.97) !important;
      }
      .leaflet-control-layers form { padding: 10px 12px 12px !important; }
      .leaflet-control-layers-overlays { margin: 0 !important; }
      .leaflet-control-layers-overlays label {
        display: flex !important; align-items: center;
        padding: 4px 2px !important; margin: 0 !important;
        cursor: pointer; border-radius: 4px;
        transition: background 120ms ease;
      }
      .leaflet-control-layers-overlays label:hover {
        background: #f6f8fa;
      }
      .leaflet-control-layers-overlays label > input[type=checkbox] {
        margin: 0 8px 0 0 !important; flex: 0 0 auto;
        accent-color: #1f7a52; transform: scale(1.05);
      }
      .leaflet-control-layers-overlays label > span {
        flex: 1; font-size: 12px; color: #0f172a;
        white-space: normal; line-height: 1.45;
      }
      /* Encabezados de grupo del GroupedLayerControl */
      .leaflet-control-layers-group-name {
        font-size: 10px !important; font-weight: 700 !important;
        text-transform: uppercase; letter-spacing: 0.06em;
        color: #1f7a52 !important;
        padding: 10px 4px 6px 4px !important;
        border-top: 1px solid #eef0f3;
        margin: 6px 0 2px !important;
      }
      .leaflet-control-layers-group:first-child .leaflet-control-layers-group-name {
        border-top: none; padding-top: 4px !important;
      }
      .leaflet-control-layers-separator { display: none; }
      /* Toggle button (cuando esta colapsado) */
      .leaflet-control-layers-toggle {
        border-radius: 10px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15) !important;
      }
      /* Subrayado de los abbr.cgsm-term dentro de la leyenda - mas sutil */
      .leaflet-control-layers abbr.cgsm-term {
        text-decoration: underline dotted #1f7a52;
        text-underline-offset: 2px;
        text-decoration-thickness: 1px;
        cursor: help; border: 0;
      }
    `;
    document.head.appendChild(st);
  }
}, 600);

// Re-aplicar si el control se reabre
document.addEventListener('click', function(e) {
  if (e.target.closest('.leaflet-control-layers-toggle')) {
    setTimeout(arguments.callee.caller || function(){}, 300);
  }
});
{% endmacro %}
        """)

m.add_child(LegendInjector())


# === Slider temporal NDVI anual (2018-2025) ===
class TimeSlider(MacroElement):
    """Slider HTML/JS que permite visualizar el NDVI anual mediano.
    Carga 8 tiles de Earth Engine bajo demanda; tile activo cambia con el slider."""
    def __init__(self, urls_by_year, palette):
        super().__init__()
        self.urls = {str(k): v for k, v in urls_by_year.items()}
        self.year_min = min(int(y) for y in urls_by_year.keys())
        self.year_max = max(int(y) for y in urls_by_year.keys())
        # Gradiente para mostrar la paleta como leyenda inline
        self.gradient = ','.join(palette)
        self._template = Template("""
{% macro html(this, kwargs) %}
<div id="cgsm-timeslider" style="position:absolute; top:175px; left:12px;
     z-index:1000;
     background:rgba(255,255,255,0.97); padding:10px 14px; border-radius:8px;
     box-shadow:0 2px 6px rgba(0,0,0,0.2);
     font-family:'Inter',-apple-system,sans-serif; font-size:12px;
     border:1px solid #d4e4dd; width:340px;">
  <div style="display:flex; align-items:center; justify-content:space-between;
       margin-bottom:6px;">
    <span><b style="color:#1f5a4b;">NDVI año:</b>
      <span id="cgsm-year-label" style="color:#1f5a4b; font-weight:700;
            font-size:14px; margin-left:4px;">{{this.year_max}}</span>
    </span>
    <div style="display:flex; gap:4px;">
      <button id="cgsm-ts-toggle" style="padding:3px 8px; font-size:11px;
              border:1px solid #1f5a4b; background:#1f5a4b; color:white;
              border-radius:4px; cursor:pointer; font-weight:600;">▶ Activar</button>
      <button id="cgsm-ts-play" style="padding:3px 8px; font-size:11px;
              border:1px solid #aa4c2a; background:white; color:#aa4c2a;
              border-radius:4px; cursor:pointer; font-weight:600;"
              title="Animar año por año">▶▶ Auto</button>
    </div>
  </div>
  <input type="range" min="{{this.year_min}}" max="{{this.year_max}}" step="1"
         value="{{this.year_max}}" id="cgsm-year-slider"
         style="width:100%; accent-color:#1f5a4b;">
  <div style="display:flex; justify-content:space-between; font-size:10px;
       color:#666; margin-top:2px;">
    <span>{{this.year_min}}</span><span>{{this.year_max}}</span>
  </div>
  <div style="margin-top:6px; display:flex; align-items:center; gap:6px;
       font-size:10px; color:#666;">
    <span>−0.2</span>
    <div style="flex:1; height:8px; border-radius:2px;
         background:linear-gradient(to right,{{this.gradient}});
         border:1px solid #999;"></div>
    <span>0.8</span>
  </div>
</div>
{% endmacro %}

{% macro script(this, kwargs) %}
setTimeout(function() {
  var cgsmYears = {{this.urls|tojson}};
  var cgsmMap = {{this._parent.get_name()}};
  var cgsmActiveLayer = null;

  // Usa el pane 'eeRasterPane' (z=450) creado por add_ee_raster_pane(m) en
  // el setup del mapa, mismo que las capas NDVI/RF/SAR estáticas. Defensivo:
  // crearlo aquí también si por algún motivo no existiera.
  if (!cgsmMap.getPane('eeRasterPane')) {
    cgsmMap.createPane('eeRasterPane');
    cgsmMap.getPane('eeRasterPane').style.zIndex = 450;
    cgsmMap.getPane('eeRasterPane').style.pointerEvents = 'none';
  }

  function cgsmShowYear(year) {
    if (cgsmActiveLayer) { cgsmMap.removeLayer(cgsmActiveLayer); }
    cgsmActiveLayer = L.tileLayer(cgsmYears[year], {
      opacity: 0.75,
      pane: 'eeRasterPane',
      attribution: 'Google Earth Engine · Sentinel-2 NDVI'
    });
    cgsmActiveLayer.addTo(cgsmMap);
  }

  var slider = document.getElementById('cgsm-year-slider');
  var label  = document.getElementById('cgsm-year-label');
  var toggle = document.getElementById('cgsm-ts-toggle');
  var playBtn = document.getElementById('cgsm-ts-play');
  var cgsmPlayInterval = null;

  slider.addEventListener('input', function(e) {
    label.innerText = e.target.value;
    if (cgsmActiveLayer) { cgsmShowYear(e.target.value); }
  });

  toggle.addEventListener('click', function() {
    if (cgsmActiveLayer) {
      cgsmMap.removeLayer(cgsmActiveLayer);
      cgsmActiveLayer = null;
      toggle.innerText = '▶ Activar';
      toggle.style.background = '#1f5a4b';
    } else {
      cgsmShowYear(slider.value);
      toggle.innerText = '■ Ocultar';
      toggle.style.background = '#aa4c2a';
    }
  });

  playBtn.addEventListener('click', function() {
    if (cgsmPlayInterval) {
      clearInterval(cgsmPlayInterval);
      cgsmPlayInterval = null;
      playBtn.innerText = '▶▶ Auto';
      playBtn.style.background = 'white';
      playBtn.style.color = '#aa4c2a';
      return;
    }
    if (!cgsmActiveLayer) { toggle.click(); }
    playBtn.innerText = '■ Pausar';
    playBtn.style.background = '#aa4c2a';
    playBtn.style.color = 'white';
    cgsmPlayInterval = setInterval(function() {
      var y = parseInt(slider.value);
      var max = parseInt(slider.max);
      var min = parseInt(slider.min);
      y = (y >= max) ? min : (y + 1);
      slider.value = y;
      label.innerText = y;
      cgsmShowYear(y);
    }, 1500);
  });
}, 400);
{% endmacro %}
        """)


# Obtener mapId de cada composite anual (registro de visualización GEE, rápido)
# IMPORTANTE: usar .visualize(**vis) ANTES de getMapId() para evitar el bug
# conocido de clip(aoi)+getMapId(visParams) que devuelve tiles transparentes.
# Al "hornear" la visualización como imagen RGB, el render de tiles funciona.
print('Registrando tiles NDVI anuales en GEE...')
ndvi_urls = {y: img.visualize(**vis_ndvi).getMapId()['tile_fetcher'].url_format
             for y, img in ndvi_anual.items()}
print(f'  {len(ndvi_urls)} URLs registradas.')

m.add_child(TimeSlider(ndvi_urls, vis_ndvi['palette']))


# ========================================================================
# DATOS PARA PANELES DINÁMICOS (Plotly + Datatable)
# ========================================================================
NDVI_CSV = ROOT / 'outputs' / 'tables' / 'ndvi_combinado_2013_2025.csv'

def _norm_name(s):
    """Normaliza nombres con underscores → espacios para empatar con stations."""
    return s.replace('_', ' ').strip()

ndvi_series = {}
if NDVI_CSV.exists():
    df_ndvi = pd.read_csv(NDVI_CSV)
    df_ndvi['estacion'] = df_ndvi['estacion'].astype(str).map(_norm_name)
    # Filtrar solo estaciones canónicas del dashboard
    df_ndvi = df_ndvi[df_ndvi['estacion'].isin(stations.keys())]
    for est in stations.keys():
        sub = df_ndvi[df_ndvi['estacion'] == est].sort_values('fecha')
        if len(sub):
            ndvi_series[est] = {
                'fechas': sub['fecha'].astype(str).tolist(),
                'ndvi':   [round(float(v), 4) for v in sub['ndvi'].tolist()],
            }
    print(f'Serie NDVI cargada: {len(ndvi_series)} estaciones')

# Tabla resumen del semáforo
alertas_data = []
for est, info in estado_por_estacion.items():
    if est not in stations:
        continue
    icono = ESTADO_ICON.get(info['estado'], '⚪')
    alertas_data.append({
        'estacion': est,
        'icono': icono,
        'estado': info['estado'],
        'z_actual': f"{info['z_actual']:+.2f}" if info.get('z_actual') is not None else '—',
        'ndvi_actual': f"{info['ndvi_actual']:.3f}" if info.get('ndvi_actual') is not None else '—',
        'razon': info.get('razon', '—'),
    })

n_estable = conteo_estados.get('estable', 0)
n_alerta  = conteo_estados.get('alerta', 0)
n_critica = conteo_estados.get('critica', 0)


# ========================================================================
# PANEL HEADER + FILTROS + AYUDA
# ========================================================================
class HeaderPanel(MacroElement):
    """Cabecera flotante arriba-izquierda con: título, contador semáforo,
    filtros por estado y botón de ayuda."""
    def __init__(self, n_estable, n_alerta, n_critica,
                 fg_estable_name, fg_alerta_name, fg_critica_name):
        super().__init__()
        self.n_estable = n_estable
        self.n_alerta  = n_alerta
        self.n_critica = n_critica
        self.fg_estable = fg_estable_name
        self.fg_alerta  = fg_alerta_name
        self.fg_critica = fg_critica_name
        self._template = Template(r"""
{% macro html(this, kwargs) %}
<div id="cgsm-header" style="position:absolute; top:12px; left:60px;
     z-index:1000;
     background:rgba(255,255,255,0.97); padding:10px 14px; border-radius:8px;
     box-shadow:0 2px 8px rgba(0,0,0,0.18);
     font-family:'Inter',-apple-system,sans-serif; font-size:12px;
     border:1px solid #d4e4dd; width:340px;">
  <div style="display:flex; align-items:center; justify-content:space-between;">
    <div>
      <div style="font-size:14px; font-weight:700; color:#1f5a4b;">
        CGSM · Monitor de manglar 2018-2025
      </div>
      <div style="font-size:10.5px; color:#666; margin-top:1px;">
        Pipeline multilenguaje · Digital Twin Nivel 2
      </div>
    </div>
    <button id="cgsm-help-btn" title="Ayuda"
            style="border:1px solid #1f5a4b; background:white; color:#1f5a4b;
                   width:26px; height:26px; border-radius:50%; cursor:pointer;
                   font-weight:700; font-size:13px;">?</button>
  </div>
  <div style="margin-top:8px; padding:6px 8px; background:#f5f8fa;
       border-radius:4px; font-size:11px;">
    <b>Estado actual:</b>
    <span style="margin-left:6px; cursor:pointer; user-select:none;"
          id="cgsm-flt-estable" data-active="1"
          title="Click para ocultar/mostrar estables">
      🟢 <b>{{this.n_estable}}</b> estables</span>
    <span style="margin-left:10px; cursor:pointer; user-select:none;"
          id="cgsm-flt-alerta" data-active="1"
          title="Click para ocultar/mostrar alertas">
      🟡 <b>{{this.n_alerta}}</b> en alerta</span>
    <span style="margin-left:10px; cursor:pointer; user-select:none;"
          id="cgsm-flt-critica" data-active="1"
          title="Click para ocultar/mostrar críticas">
      🔴 <b>{{this.n_critica}}</b> críticas</span>
  </div>
</div>

<div id="cgsm-help-modal" style="display:none; position:absolute; top:80px;
     left:60px; z-index:1001;
     background:white; padding:16px 18px; border-radius:8px;
     box-shadow:0 4px 16px rgba(0,0,0,0.28);
     font-family:'Inter',-apple-system,sans-serif; font-size:12px;
     border:1px solid #d4e4dd; width:380px; line-height:1.5;">
  <div style="display:flex; justify-content:space-between; align-items:center;
       border-bottom:1px solid #eee; padding-bottom:6px; margin-bottom:10px;">
    <b style="color:#1f5a4b; font-size:13px;">¿Cómo usar este dashboard?</b>
    <span id="cgsm-help-close" style="cursor:pointer; color:#aa4c2a;
          font-weight:700; padding:0 6px;">×</span>
  </div>
  <p style="margin:0 0 8px 0;"><b>1. Panel de capas (arriba-derecha):</b>
     prende/apaga capas por temática: estado del manglar (NDVI), clasificación
     por periodo (umbrales y Random Forest), dinámica de cambio 2020→2024,
     inundación SAR y referencias cartográficas (INVEMAR, GFD).</p>
  <p style="margin:0 0 8px 0;"><b>2. Estaciones de muestreo:</b>
     los círculos del mapa están coloreados por el módulo de alertas tempranas
     (🟢 estable, 🟡 alerta, 🔴 crítica). Haz click sobre cualquiera para ver
     z-score, NDVI actual y la razón del estado.</p>
  <p style="margin:0 0 8px 0;"><b>3. Filtros:</b>
     en el contador superior puedes click en 🟢/🟡/🔴 para ocultar o mostrar
     ese subconjunto de estaciones.</p>
  <p style="margin:0 0 8px 0;"><b>4. Slider temporal (abajo-izquierda):</b>
     desliza el año (2018-2025) para ver la mediana NDVI de cada periodo, o
     pulsa <b>▶▶ Auto</b> para animar año por año.</p>
  <p style="margin:0;"><b>5. Panel de análisis (abajo-derecha):</b>
     alterna entre la <b>gráfica</b> de serie temporal por estación y la
     <b>tabla</b> con el detalle del semáforo.</p>
</div>
{% endmacro %}

{% macro script(this, kwargs) %}
setTimeout(function() {
  var helpBtn   = document.getElementById('cgsm-help-btn');
  var helpModal = document.getElementById('cgsm-help-modal');
  var helpClose = document.getElementById('cgsm-help-close');
  if (helpBtn) helpBtn.addEventListener('click', function() {
    helpModal.style.display = (helpModal.style.display === 'none') ? 'block' : 'none';
  });
  if (helpClose) helpClose.addEventListener('click', function() {
    helpModal.style.display = 'none';
  });

  // Filtros — toggle FeatureGroups por estado
  var fgRef = {
    'estable': {{this.fg_estable}},
    'alerta':  {{this.fg_alerta}},
    'critica': {{this.fg_critica}}
  };
  var mapRef = {{this._parent.get_name()}};

  function applyFilter(estado) {
    var el = document.getElementById('cgsm-flt-' + estado);
    if (!el) return;
    var active = el.dataset.active === '1';
    var fg = fgRef[estado];
    if (!fg) return;
    if (active) {
      mapRef.removeLayer(fg);
      el.dataset.active = '0';
      el.style.opacity = '0.35';
      el.style.textDecoration = 'line-through';
    } else {
      mapRef.addLayer(fg);
      el.dataset.active = '1';
      el.style.opacity = '1';
      el.style.textDecoration = 'none';
    }
  }
  ['estable','alerta','critica'].forEach(function(estado) {
    var el = document.getElementById('cgsm-flt-' + estado);
    if (el) el.addEventListener('click', function() { applyFilter(estado); });
  });
}, 700);
{% endmacro %}
        """)

m.add_child(HeaderPanel(n_estable, n_alerta, n_critica,
                         fg_estable.get_name(), fg_alerta.get_name(),
                         fg_critica.get_name()))


# ========================================================================
# PANEL ESTADÍSTICO (Plotly + Datatable con tabs)
# ========================================================================
class StatsPanel(MacroElement):
    """Panel flotante abajo-derecha con dos pestañas:
    1) Gráfica Plotly de serie temporal NDVI por estación
    2) Tabla interactiva (Datatables) con el estado del semáforo."""
    def __init__(self, ndvi_series, alertas_data):
        super().__init__()
        import json
        self.ndvi_json   = json.dumps(ndvi_series, ensure_ascii=False)
        self.tabla_json  = json.dumps(alertas_data, ensure_ascii=False)
        self._template = Template(r"""
{% macro header(this, kwargs) %}
<script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
<link rel="stylesheet" href="https://cdn.datatables.net/1.13.7/css/jquery.dataTables.min.css">
<script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
<script src="https://cdn.datatables.net/1.13.7/js/jquery.dataTables.min.js"></script>
{% endmacro %}

{% macro html(this, kwargs) %}
<div id="cgsm-stats" style="position:absolute; bottom:24px; left:12px;
     z-index:1000;
     background:rgba(255,255,255,0.97); padding:8px 10px; border-radius:8px;
     box-shadow:0 2px 8px rgba(0,0,0,0.2);
     font-family:'Inter',-apple-system,sans-serif; font-size:11px;
     border:1px solid #d4e4dd; width:580px; box-sizing:border-box;
     overflow:hidden;">
  <div style="display:flex; gap:4px; margin-bottom:6px; flex-wrap:wrap;">
    <button id="cgsm-tab-plot" class="cgsm-tab"
            style="padding:4px 8px; border:1px solid #1f5a4b;
                   background:#1f5a4b; color:white; border-radius:4px;
                   cursor:pointer; font-weight:600; font-size:11px;">📈 Serie</button>
    <button id="cgsm-tab-table" class="cgsm-tab"
            style="padding:4px 8px; border:1px solid #1f5a4b;
                   background:white; color:#1f5a4b; border-radius:4px;
                   cursor:pointer; font-weight:600; font-size:11px;">📋 Tabla</button>
    <button id="cgsm-tab-guide" class="cgsm-tab"
            style="padding:4px 8px; border:1px solid #1f5a4b;
                   background:white; color:#1f5a4b; border-radius:4px;
                   cursor:pointer; font-weight:600; font-size:11px;">📘 Guía</button>
    <button id="cgsm-tab-events" class="cgsm-tab"
            style="padding:4px 8px; border:1px solid #1f5a4b;
                   background:white; color:#1f5a4b; border-radius:4px;
                   cursor:pointer; font-weight:600; font-size:11px;">🎯 Eventos</button>
    <button id="cgsm-tab-rf" class="cgsm-tab"
            style="padding:4px 8px; border:1px solid #1f5a4b;
                   background:white; color:#1f5a4b; border-radius:4px;
                   cursor:pointer; font-weight:600; font-size:11px;">📊 RF vs Umb.</button>
    <button id="cgsm-tab-station" class="cgsm-tab"
            style="padding:4px 8px; border:1px solid #1f5a4b;
                   background:white; color:#1f5a4b; border-radius:4px;
                   cursor:pointer; font-weight:600; font-size:11px;">🔍 Estación</button>
    <span style="flex:1;"></span>
    <button id="cgsm-stats-min" title="Expandir / minimizar panel"
            style="border:1px solid #aaa; background:white; color:#666;
                   width:22px; height:22px; border-radius:4px;
                   cursor:pointer; font-size:13px; padding:0;">+</button>
  </div>
  <div id="cgsm-tab-plot-body" style="display:none;">
    <div style="margin-bottom:4px; font-size:10.5px; color:#666;">
      Estación: <select id="cgsm-plot-station"
                       style="font-size:11px; padding:1px 4px;"></select>
      <label style="margin-left:8px;">
        <input type="checkbox" id="cgsm-plot-allstations"
               style="vertical-align:middle;"> Comparar todas
      </label>
    </div>
    <div id="cgsm-plot" style="width:548px; height:260px; max-width:100%;"></div>
    <div style="font-size:9.5px; color:#555; margin-top:4px; padding:5px 7px;
         background:#f5f8fa; border-radius:4px; line-height:1.45;">
      <b>Cómo leerla:</b> la franja superior (NDVI &gt; 0,70, verde) marca
      manglar denso saludable; la zona media (0,40-0,70) corresponde a
      vegetación intermedia o manglar joven; valores &lt; 0,30 indican
      agua o suelo desnudo. Las estaciones limnológicas
      (Isla Boquerón, Punta Cerro, Punta Chino, Río Sevilla) muestran
      valores bajos porque monitorean la lámina de agua, no el dosel.
    </div>
  </div>
  <div id="cgsm-tab-table-body" style="display:none;">
    <table id="cgsm-table" style="width:100%; font-size:10.5px;" class="display compact cell-border row-border hover">
      <thead><tr>
        <th></th><th>Estación</th><th>Estado</th><th>z</th><th>NDVI</th>
      </tr></thead>
      <tbody></tbody>
    </table>
    <div style="font-size:9.5px; color:#555; margin-top:6px; padding:5px 7px;
         background:#f5f8fa; border-radius:4px; line-height:1.45;">
      <b>Lógica del semáforo:</b> 🟢 <i>estable</i> = sin anomalías
      significativas; 🟡 <i>alerta</i> = z entre -1 y -2 en últimos 3
      meses, o 2+ anomalías z &lt; -1 en el año; 🔴 <i>crítica</i> = z
      &lt; -2 en el último mes, o 2+ anomalías z &lt; -2. El campo
      <i>z</i> reporta el z-score NDVI del mes más reciente disponible.
    </div>
  </div>
  <div id="cgsm-tab-guide-body" style="display:none; max-height:280px; overflow-y:auto;">
    <div style="font-size:10.5px; color:#333; line-height:1.5;">
      <p style="margin:0 0 6px 0;"><b>Cómo navegar el dashboard:</b></p>
      <ol style="margin:0 0 8px 16px; padding:0;">
        <li><b>Mapa central:</b> cobertura del manglar de la CGSM con ocho estaciones de monitoreo coloreadas por estado.</li>
        <li><b>Panel de capas (derecha):</b> activa/desactiva temáticas (NDVI por periodo, Random Forest, dinámica, SAR, INVEMAR).</li>
        <li><b>Filtros del header:</b> click sobre 🟢/🟡/🔴 oculta o muestra estaciones por estado.</li>
        <li><b>Slider NDVI:</b> desliza años 2018-2025 o pulsa ▶▶ Auto para animar.</li>
      </ol>
      <p style="margin:8px 0 4px 0;"><b>Glosario de términos:</b></p>
      <dl style="margin:0; font-size:10px;">
        <dt><b>NDVI</b></dt><dd style="margin:0 0 4px 8px;">Normalized Difference Vegetation Index. Mide vigor vegetal: &gt;0,7 manglar denso, 0,4-0,7 vegetación intermedia, &lt;0,3 agua o suelo.</dd>
        <dt><b>CMRI</b></dt><dd style="margin:0 0 4px 8px;">Combined Mangrove Recognition Index (NDVI − NDWI). Discrimina manglar de otras coberturas en ambientes estuarinos.</dd>
        <dt><b>SAR-VH</b></dt><dd style="margin:0 0 4px 8px;">Backscatter Sentinel-1 polarización vertical-horizontal. Sensible a humedad y estructura del dosel. Útil bajo cubierta de nubes.</dd>
        <dt><b>bfast</b></dt><dd style="margin:0 0 4px 8px;">Breaks For Additive Season and Trend. Detecta quiebres estructurales en series temporales.</dd>
        <dt><b>z-score</b></dt><dd style="margin:0 0 4px 8px;">Anomalía estandarizada respecto a la media histórica: z = (valor − media) / σ. |z|&gt;2 indica anomalía pronunciada.</dd>
        <dt><b>Random Forest</b></dt><dd style="margin:0 0 4px 8px;">Clasificador supervisado por ensamble de árboles de decisión. F1=0,83 en este proyecto.</dd>
        <dt><b>Digital Twin Nivel 2</b></dt><dd style="margin:0 0 4px 8px;">Réplica operativa que detecta anomalías sobre el sistema real, sin componente predictivo (Nivel 3).</dd>
        <dt><b>F1-score</b></dt><dd style="margin:0;">Media armónica de Precision y Recall. 1 = perfecto, 0 = ninguna concordancia.</dd>
      </dl>
    </div>
  </div>
  <div id="cgsm-tab-events-body" style="display:none; max-height:280px; overflow-y:auto;">
    <div style="font-size:10.5px; color:#333; line-height:1.55;">
      <p style="margin:0 0 8px 0;"><b>Eventos climáticos y de mortandad documentados (2013-2025):</b></p>
      <div style="border-left:3px solid #D32F2F; padding:4px 8px; margin-bottom:6px; background:#fff5f5;">
        <b>2015-2016 · El Niño</b><br>
        Sequía sostenida. Quiebres bfast detectados en 7 de 8 estaciones entre abril y diciembre de 2016. NDVI cae por debajo de la media histórica.
      </div>
      <div style="border-left:3px solid #1565C0; padding:4px 8px; margin-bottom:6px; background:#f3f8ff;">
        <b>Septiembre 2020 · Mortandad asociada a La Niña</b><br>
        59 km² afectados: 16 km² agua abierta + 43 km² inundación bajo dosel (detectados por SAR-VH). Quiebres bfast febrero y diciembre 2020 sobre Caño Clarín; junio 2020 sobre Caño Palos.
      </div>
      <div style="border-left:3px solid #43A047; padding:4px 8px; margin-bottom:6px; background:#f3fff5;">
        <b>2022 · Recuperación post-La Niña</b><br>
        NDVI mediano del manglar denso pasa de 0,60 a 0,80. Quiebres bfast enero y abril 2022 sobre CP Aguas Negras y CP Luna. Aporte hídrico sostenido del Magdalena.
      </div>
      <div style="border-left:3px solid #D32F2F; padding:4px 8px; margin-bottom:6px; background:#fff5f5;">
        <b>2023-2024 · El Niño</b><br>
        Quiebres bfast entre agosto 2023 y junio 2024 sobre las cuatro estaciones de manglar denso. Visible en serie ONI y precipitación CHIRPS.
      </div>
      <div style="border-left:3px solid #1B5E20; padding:4px 8px; background:#f0f8f0;">
        <b>2024-2025 · Estado actual</b><br>
        Sistema en consolidación estructural: 5 estaciones estables, 3 en alerta, 0 críticas. Backscatter SAR-VH sube 3-5 dB sobre Complejo de Pajarales respecto a 2018-2019.
      </div>
    </div>
  </div>
  <div id="cgsm-tab-rf-body" style="display:none; max-height:280px; overflow-y:auto;">
    <div style="font-size:10.5px; color:#333; line-height:1.5;">
      <p style="margin:0 0 6px 0;"><b>Benchmark de clasificadores sobre Sentinel-2 2024-2025:</b></p>
      <table style="width:100%; border-collapse:collapse; font-size:10px; margin-bottom:6px;">
        <tr style="background:#f5f8fa;">
          <th style="border:1px solid #ccc; padding:4px;">Método</th>
          <th style="border:1px solid #ccc; padding:4px;">Referencia</th>
          <th style="border:1px solid #ccc; padding:4px;">F1</th>
          <th style="border:1px solid #ccc; padding:4px;">Recall</th>
          <th style="border:1px solid #ccc; padding:4px;">Precision</th>
        </tr>
        <tr><td style="border:1px solid #ccc; padding:4px;">Umbrales NDVI/CMRI</td><td style="border:1px solid #ccc; padding:4px;">INVEMAR</td><td style="border:1px solid #ccc; padding:4px;">0,583</td><td style="border:1px solid #ccc; padding:4px;">0,454</td><td style="border:1px solid #ccc; padding:4px;">0,811</td></tr>
        <tr><td style="border:1px solid #ccc; padding:4px;">Umbrales NDVI/CMRI</td><td style="border:1px solid #ccc; padding:4px;">WorldCover</td><td style="border:1px solid #ccc; padding:4px;">0,548</td><td style="border:1px solid #ccc; padding:4px;">0,426</td><td style="border:1px solid #ccc; padding:4px;">0,768</td></tr>
        <tr style="background:#e8f5e9;"><td style="border:1px solid #ccc; padding:4px;"><b>Random Forest</b></td><td style="border:1px solid #ccc; padding:4px;">INVEMAR</td><td style="border:1px solid #ccc; padding:4px;"><b>0,826</b></td><td style="border:1px solid #ccc; padding:4px;"><b>0,926</b></td><td style="border:1px solid #ccc; padding:4px;">0,745</td></tr>
        <tr style="background:#e8f5e9;"><td style="border:1px solid #ccc; padding:4px;"><b>Random Forest</b></td><td style="border:1px solid #ccc; padding:4px;">WorldCover</td><td style="border:1px solid #ccc; padding:4px;"><b>0,889</b></td><td style="border:1px solid #ccc; padding:4px;"><b>0,937</b></td><td style="border:1px solid #ccc; padding:4px;">0,846</td></tr>
      </table>
      <p style="margin:4px 0; font-size:9.5px;"><b>Variables más discriminantes (Gini):</b> B11/B12 SWIR Sentinel-2 (33,9), distancia al agua JRC (16,0), CMRI (11,4), NDWI (11,1). NDVI solo aporta 8,4.</p>
      <p style="margin:0; font-size:9.5px; color:#555;"><b>Para comparar visualmente:</b> abre el panel de capas (derecha) y prende "Manglar Actual umbrales" y "Manglar Actual Random Forest" simultáneamente.</p>
    </div>
  </div>
  <div id="cgsm-tab-station-body" style="display:none; max-height:280px; overflow-y:auto;">
    <div style="font-size:10.5px; color:#333; line-height:1.5;">
      <div style="margin-bottom:6px;">
        Selecciona estación:
        <select id="cgsm-station-detail" style="font-size:11px; padding:1px 4px;"></select>
      </div>
      <div id="cgsm-station-info" style="background:#f5f8fa; border-radius:4px; padding:8px; min-height:120px;">
        Cargando...
      </div>
    </div>
  </div>
</div>
{% endmacro %}

{% macro script(this, kwargs) %}
setTimeout(function() {
  var ndviSeries = {{this.ndvi_json|safe}};
  var alertasData = {{this.tabla_json|safe}};
  var statsBox = document.getElementById('cgsm-stats');
  var tabPlot  = document.getElementById('cgsm-tab-plot');
  var tabTable = document.getElementById('cgsm-tab-table');
  var bodyPlot  = document.getElementById('cgsm-tab-plot-body');
  var bodyTable = document.getElementById('cgsm-tab-table-body');
  var minBtn = document.getElementById('cgsm-stats-min');

  // Populate station selector
  var sel = document.getElementById('cgsm-plot-station');
  var stations = Object.keys(ndviSeries);
  stations.forEach(function(s) {
    var opt = document.createElement('option');
    opt.value = s; opt.text = s;
    sel.appendChild(opt);
  });

  function renderPlot() {
    var allMode = document.getElementById('cgsm-plot-allstations').checked;
    var traces = [];
    if (allMode) {
      var palette = ['#1f5a4b','#aa4c2a','#D32F2F','#FBC02D','#43A047',
                     '#7B1FA2','#0288D1','#5D4037'];
      stations.forEach(function(s, i) {
        var d = ndviSeries[s];
        if (!d) return;
        traces.push({
          x: d.fechas, y: d.ndvi, mode: 'lines', name: s,
          line: {width: 1.4, color: palette[i % palette.length]}
        });
      });
    } else {
      var s = sel.value;
      var d = ndviSeries[s];
      if (d) {
        traces.push({
          x: d.fechas, y: d.ndvi, mode: 'lines+markers', name: s,
          line: {color: '#1f5a4b', width: 2},
          marker: {size: 3, color: '#1f5a4b'}
        });
      }
    }
    var layout = {
      margin: {t: 16, r: 10, b: 32, l: 36},
      xaxis: {title: '', tickfont: {size: 9}, type: 'date',
              tickformat: '%Y', dtick: 'M12'},
      yaxis: {title: 'NDVI', titlefont: {size: 10},
              tickfont: {size: 9}, range: [-0.2, 0.95]},
      showlegend: allMode, legend: {font: {size: 9}, orientation: 'h',
                                     y: -0.22},
      hovermode: 'closest', height: 240, width: 548, autosize: false,
      plot_bgcolor: '#fafafa',
      shapes: [
        {type:'line', xref:'paper', x0:0, x1:1, y0:0.4, y1:0.4,
         line:{color:'#FB8C00', width:1, dash:'dash'}, opacity:0.55},
        {type:'line', xref:'paper', x0:0, x1:1, y0:0.7, y1:0.7,
         line:{color:'#1B5E20', width:1, dash:'dash'}, opacity:0.55}
      ],
      annotations: [
        {xref:'paper', yref:'y', x:0.99, y:0.42, xanchor:'right',
         showarrow:false, text:'manglar saludable',
         font:{size:8.5, color:'#FB8C00'},
         bgcolor:'rgba(255,255,255,0.85)'},
        {xref:'paper', yref:'y', x:0.99, y:0.72, xanchor:'right',
         showarrow:false, text:'manglar denso',
         font:{size:8.5, color:'#1B5E20'},
         bgcolor:'rgba(255,255,255,0.85)'}
      ]
    };
    Plotly.newPlot('cgsm-plot', traces, layout,
                   {displayModeBar: false, responsive: false, staticPlot: false});
  }
  if (stations.length) {
    renderPlot();
    sel.addEventListener('change', renderPlot);
    document.getElementById('cgsm-plot-allstations')
            .addEventListener('change', renderPlot);
  }

  // Datatable
  var tbody = document.querySelector('#cgsm-table tbody');
  alertasData.forEach(function(r) {
    var tr = document.createElement('tr');
    tr.innerHTML = '<td>' + r.icono + '</td>' +
                   '<td>' + r.estacion + '</td>' +
                   '<td>' + r.estado + '</td>' +
                   '<td>' + r.z_actual + '</td>' +
                   '<td>' + r.ndvi_actual + '</td>';
    tr.title = r.razon;
    tbody.appendChild(tr);
  });
  if (window.jQuery && jQuery.fn.DataTable) {
    jQuery('#cgsm-table').DataTable({
      paging: false, searching: true, info: false,
      order: [[2, 'asc']],
      language: {
        search: 'Buscar:', emptyTable: 'Sin datos',
        zeroRecords: 'Sin coincidencias'
      }
    });
  }

  // Tab switching
  function activate(which) {
    var isPlot = (which === 'plot');
    bodyPlot.style.display  = isPlot ? 'block' : 'none';
    bodyTable.style.display = isPlot ? 'none' : 'block';
    tabPlot.style.background  = isPlot ? '#1f5a4b' : 'white';
    tabPlot.style.color       = isPlot ? 'white' : '#1f5a4b';
    tabTable.style.background = isPlot ? 'white' : '#1f5a4b';
    tabTable.style.color      = isPlot ? '#1f5a4b' : 'white';
  }
  tabPlot.addEventListener('click',  function() { activate('plot'); });
  tabTable.addEventListener('click', function() { activate('table'); });

  // Minimize — el panel INICIA MINIMIZADO para no tapar la leyenda.
  // Solo las pestañas son visibles; al hacer click en + se expande.
  var minimized = true;
  var activeTab = 'plot';
  function expandBody() {
    bodyPlot.style.display  = (activeTab === 'plot')  ? 'block' : 'none';
    bodyTable.style.display = (activeTab === 'table') ? 'block' : 'none';
  }
  // Reescribir tab handlers para que también marquen activeTab y expandan
  tabPlot.addEventListener('click', function() {
    activeTab = 'plot';
    if (minimized) { minimized = false; minBtn.innerText = '−'; }
    expandBody();
  });
  tabTable.addEventListener('click', function() {
    activeTab = 'table';
    if (minimized) { minimized = false; minBtn.innerText = '−'; }
    expandBody();
  });
  minBtn.addEventListener('click', function() {
    if (minimized) {
      minimized = false;
      minBtn.innerText = '−';
      expandBody();
    } else {
      minimized = true;
      minBtn.innerText = '+';
      bodyPlot.style.display = 'none';
      bodyTable.style.display = 'none';
    }
  });

  // === Handlers de las 4 pestañas nuevas ===
  var tabGuide   = document.getElementById('cgsm-tab-guide');
  var tabEvents  = document.getElementById('cgsm-tab-events');
  var tabRf      = document.getElementById('cgsm-tab-rf');
  var tabStation = document.getElementById('cgsm-tab-station');
  var bodyGuide   = document.getElementById('cgsm-tab-guide-body');
  var bodyEvents  = document.getElementById('cgsm-tab-events-body');
  var bodyRf      = document.getElementById('cgsm-tab-rf-body');
  var bodyStation = document.getElementById('cgsm-tab-station-body');

  function showOnlyTab(name) {
    var bodies = {
      'plot': bodyPlot, 'table': bodyTable, 'guide': bodyGuide,
      'events': bodyEvents, 'rf': bodyRf, 'station': bodyStation
    };
    var tabs = {
      'plot': tabPlot, 'table': tabTable, 'guide': tabGuide,
      'events': tabEvents, 'rf': tabRf, 'station': tabStation
    };
    for (var k in bodies) {
      if (bodies[k]) bodies[k].style.display = (k === name) ? 'block' : 'none';
      if (tabs[k]) {
        tabs[k].style.background = (k === name) ? '#1f5a4b' : 'white';
        tabs[k].style.color      = (k === name) ? 'white' : '#1f5a4b';
      }
    }
    activeTab = name;
    if (minimized) { minimized = false; minBtn.innerText = '−'; }
  }
  if (tabGuide)   tabGuide.addEventListener('click',   function() { showOnlyTab('guide'); });
  if (tabEvents)  tabEvents.addEventListener('click',  function() { showOnlyTab('events'); });
  if (tabRf)      tabRf.addEventListener('click',      function() { showOnlyTab('rf'); });
  if (tabStation) tabStation.addEventListener('click', function() { showOnlyTab('station'); });
  // Sobreescribir handlers de plot y table también para que usen showOnlyTab
  tabPlot.addEventListener('click',  function() { showOnlyTab('plot'); });
  tabTable.addEventListener('click', function() { showOnlyTab('table'); });

  // Llenar selector de detalle por estación
  var detSel = document.getElementById('cgsm-station-detail');
  var detInfo = document.getElementById('cgsm-station-info');
  if (detSel && detInfo) {
    alertasData.forEach(function(r) {
      var opt = document.createElement('option');
      opt.value = r.estacion; opt.text = r.icono + ' ' + r.estacion;
      detSel.appendChild(opt);
    });
    function renderStationDetail() {
      var sel = detSel.value;
      var info = alertasData.find(function(r) { return r.estacion === sel; });
      if (!info) { detInfo.innerHTML = 'Sin datos'; return; }
      var serieEst = ndviSeries[sel];
      var nObs = serieEst ? serieEst.fechas.length : 0;
      var rango = serieEst ? (serieEst.fechas[0] + ' a ' + serieEst.fechas[serieEst.fechas.length-1]) : '—';
      detInfo.innerHTML =
        '<div style="font-size:13px;"><b>' + info.icono + ' ' + info.estacion + '</b></div>' +
        '<div style="margin-top:4px;"><b>Estado:</b> ' + info.estado + '</div>' +
        '<div><b>z NDVI actual:</b> ' + info.z_actual + ' · <b>NDVI:</b> ' + info.ndvi_actual + '</div>' +
        '<div style="margin-top:4px; font-size:9.5px; color:#555;"><b>Razón:</b> ' + info.razon + '</div>' +
        '<div style="margin-top:4px; font-size:9.5px; color:#555;"><b>Serie NDVI:</b> ' + nObs + ' observaciones (' + rango + ')</div>' +
        '<div style="margin-top:6px; font-size:9.5px;">Para ver la serie completa, abre la pestaña <b>📈 Serie</b> y selecciona esta estación.</div>';
    }
    detSel.addEventListener('change', renderStationDetail);
    renderStationDetail();
  }


  // === Tooltips inline en términos técnicos (definiciones tipo Wikipedia) ===
  // Inyecta estilo CSS para abbr.cgsm-term (subrayado punteado + cursor help)
  var cgsmStyle = document.createElement('style');
  cgsmStyle.textContent = ''
    + 'abbr.cgsm-term {'
    + '  border-bottom: 1px dotted #1f5a4b !important;'
    + '  cursor: help !important;'
    + '  text-decoration: none !important;'
    + '  color: #1f5a4b !important;'
    + '  font-weight: 500;'
    + '}'
    + 'abbr.cgsm-term:hover { background: rgba(31, 90, 75, 0.08); }';
  document.head.appendChild(cgsmStyle);

  var cgsmTerms = {
    'NDVI':         'Normalized Difference Vegetation Index — índice de vegetación. >0,7 = manglar denso, 0,4-0,7 = vegetación intermedia, <0,3 = agua o suelo desnudo.',
    'CMRI':         'Combined Mangrove Recognition Index = NDVI − NDWI. Discrimina manglar de otras coberturas en ambientes estuarinos (Gupta et al., 2018).',
    'NDWI':         'Normalized Difference Water Index — índice que detecta cuerpos de agua.',
    'SAR-VH':       'Sentinel-1 SAR polarización vertical-horizontal — sensor radar activo que penetra nubes y mide humedad y estructura del dosel.',
    'SAR':          'Synthetic Aperture Radar — sensor radar activo. Funciona en cualquier condición climática y mide rugosidad y humedad.',
    'bfast':        'Breaks For Additive Season and Trend (Verbesselt et al., 2010) — algoritmo R que detecta quiebres estructurales en series temporales de NDVI.',
    'z-score':      'Anomalía estandarizada = (valor − media histórica) / desviación estándar. |z| > 2 indica anomalía pronunciada.',
    'Random Forest':'Clasificador supervisado por ensamble de árboles de decisión. En este proyecto alcanza F1 = 0,83 frente a INVEMAR, una mejora del 42 % sobre umbrales.',
    'Digital Twin': 'Réplica digital operativa del ecosistema real. Nivel 2 = detección de anomalías y alertas; Nivel 3 (futuro) = predicción.',
    'F1-score':     'Media armónica de Precision y Recall: F1 = 2·P·R/(P+R). 1 = clasificador perfecto, 0 = ninguna concordancia.',
    'Recall':       'Sensibilidad o tasa de verdaderos positivos: VP / (VP + falsos negativos). Mide cuánto del manglar real se detectó.',
    'Precision':    'Valor predictivo positivo: VP / (VP + falsos positivos). Mide cuán confiable es una predicción positiva.',
    'INVEMAR':      'Instituto de Investigaciones Marinas y Costeras de Colombia — provee cartografía oficial de manglares a 1:25.000.',
    'WorldCover':   'ESA WorldCover v200 (Zanaga et al., 2022) — clasificación global de coberturas a 10 m de resolución.',
    'Sentinel-2':   'Satélite óptico de la ESA, 10 m de resolución, revisita cada 5 días. Provee 13 bandas espectrales.',
    'Sentinel-1':   'Satélite radar SAR de la ESA, 10 m de resolución, funciona en todo clima (incluso bajo nubes).',
    'Landsat':      'Programa USGS/NASA de observación terrestre, 30 m de resolución, serie histórica desde 1984.',
    'ENSO':         'El Niño-Oscilación del Sur — oscilación climática del Pacífico ecuatorial que modula precipitación en Colombia.',
    'La Niña':      'Fase fría de ENSO — asociada a más lluvia en el Caribe colombiano. La Niña 2020-2022 se ligó a la mortandad de septiembre 2020.',
    'El Niño':      'Fase cálida de ENSO — asociada a sequía en Colombia. El Niño 2015-2016 generó quiebres bfast en 7 de 8 estaciones.',
    'AOI':          'Area Of Interest — zona delimitada del análisis. Aquí: 835,3 km² del SFF CGSM + Vía Parque Isla de Salamanca.',
    'ERA5':         'Reanálisis climático global del ECMWF (Hersbach et al., 2020). Resolución horaria, ~9 km espacial.',
    'JRC':          'Joint Research Centre Global Surface Water — mapa global de ocurrencia de agua superficial 1984-2021.',
    'GFD':          'Global Flood Database — registro histórico de inundaciones detectadas por satélite (2001-2017).'
  };

  // Procesa cada textNode usando DOM API en vez de manipulación de string,
  // así NUNCA toca attributes (title="...") y no se corrompen tooltips
  // anidados. Wrappea TODAS las ocurrencias de cualquier término en cada
  // textNode (no usa wrappedInDoc, que perdía términos repetidos).
  function cgsmAddTooltips(root) {
    if (!root) return;
    var sortedTerms = Object.keys(cgsmTerms).sort(function(a, b) {
      return b.length - a.length;
    });
    // Construir un único regex que matchea cualquier término largo primero
    var escaped = sortedTerms.map(function(t) {
      return t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    });
    var bigPat = new RegExp(
      '(^|[\\s(>])(' + escaped.join('|') + ')(?=$|[\\s.,;:!?)\\u2014\\-/])', 'g'
    );

    var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, null);
    var nodes = [];
    var n;
    while ((n = walker.nextNode())) {
      var p = n.parentNode;
      if (!p) continue;
      var tag = p.tagName;
      if (tag === 'SCRIPT' || tag === 'STYLE' || tag === 'OPTION' ||
          tag === 'ABBR' || tag === 'TEXTAREA') continue;
      if (p.closest && p.closest('abbr.cgsm-term')) continue;
      nodes.push(n);
    }

    nodes.forEach(function(textNode) {
      var text = textNode.nodeValue;
      bigPat.lastIndex = 0;
      if (!bigPat.test(text)) return;
      bigPat.lastIndex = 0;
      // Reconstruir el contenido como secuencia de Text + Abbr nodes
      var frag = document.createDocumentFragment();
      var lastIdx = 0;
      var m;
      while ((m = bigPat.exec(text)) !== null) {
        var prefix = m[1];
        var term = m[2];
        var startTerm = m.index + prefix.length;
        // Texto antes del término (incluido el prefix de separación)
        if (startTerm > lastIdx) {
          frag.appendChild(document.createTextNode(text.slice(lastIdx, startTerm)));
        }
        // El abbr — setAttribute escapa correctamente sin importar lo que tenga
        var abbr = document.createElement('abbr');
        abbr.className = 'cgsm-term';
        abbr.setAttribute('title', cgsmTerms[term]);
        abbr.textContent = term;
        frag.appendChild(abbr);
        lastIdx = startTerm + term.length;
      }
      if (lastIdx < text.length) {
        frag.appendChild(document.createTextNode(text.slice(lastIdx)));
      }
      textNode.parentNode.replaceChild(frag, textNode);
    });
  }

  // Aplicar al panel stats, al header, al modal de ayuda y al control de capas
  setTimeout(function() {
    cgsmAddTooltips(document.getElementById('cgsm-stats'));
    cgsmAddTooltips(document.getElementById('cgsm-header'));
    cgsmAddTooltips(document.getElementById('cgsm-help-modal'));
    document.querySelectorAll('.leaflet-control-layers').forEach(function(el) {
      cgsmAddTooltips(el);
    });
  }, 1400);

}, 900);
{% endmacro %}
        """)

m.add_child(StatsPanel(ndvi_series, alertas_data))

m.save(str(OUT_HTML))

print(f'\nDashboard exportado: {OUT_HTML}')
print(f'Tamano: {OUT_HTML.stat().st_size / 1024:.0f} KB')
print('Capas totales: 18 + slider NDVI anual con animación 2018-2025')
print('Paneles dinámicos: header semaforo + filtros estado + ayuda contextual')
print('                   + tabs Plotly serie NDVI + Datatable interactiva')
print('                   + Guía/glosario, Eventos, RF vs Umb., Detalle estación')
