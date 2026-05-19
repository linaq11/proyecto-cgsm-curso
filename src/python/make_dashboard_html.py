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
    """Agrega una capa EE como TileLayer de folium y la devuelve para agruparla después."""
    try:
        img = ee.Image(ee_object)
    except Exception:
        img = ee_object  # FeatureCollection.style() ya devuelve un Image
    map_id_dict = img.getMapId(vis_params)
    tl = folium.raster_layers.TileLayer(
        tiles=map_id_dict['tile_fetcher'].url_format,
        attr='Google Earth Engine',
        name=name,
        overlay=True,
        control=True,
        show=shown,
        opacity=opacity,
    )
    tl.add_to(self)
    return tl


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

# --- Capas NDVI por periodo ---
ly_ndvi_act = m.add_ee_layer(ndvi_act,    vis_ndvi,   'NDVI Actual (2024-2025)',  shown=False)
ly_ndvi_deg = m.add_ee_layer(ndvi_deg,    vis_ndvi,   'NDVI Degradación (2020)',  shown=False)
ly_ndvi_rec = m.add_ee_layer(ndvi_rec,    vis_ndvi,   'NDVI Recuperación (2022)', shown=False)
ly_ndvi_chg = m.add_ee_layer(ndvi_change, vis_change, 'Cambio NDVI (Actual − Degradación)', shown=False)

# --- Manglar por periodo (clasificación) ---
ly_md = m.add_ee_layer(md, {'palette': ['#E57373']}, 'Manglar Degradación (2020)',  shown=False, opacity=0.75)
ly_mr = m.add_ee_layer(mr, {'palette': ['#FFB74D']}, 'Manglar Recuperación (2022)', shown=False, opacity=0.75)
ly_ma = m.add_ee_layer(ma, {'palette': ['#81C784']}, 'Manglar Actual (2024-2025)',  shown=False, opacity=0.75)

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

manglar_set     = {'Cano Palos', 'Cano Clarin', 'CP Pajarales', 'VIPIS'}
limnologica_set = {'Isla Boqueron', 'Punta Cerro', 'Punta Chino', 'Rio Sevilla'}

# Centroides de estaciones — añadidos directamente al mapa (no como capa controlable)
# para evitar duplicar leyendas con "Estaciones INVEMAR" y "Estaciones complementarias".
# Se colorean por fuente para que coincidan con las capas de buffer correspondientes.
for nombre, (lon, lat, tipo) in stations.items():
    fuente     = 'INVEMAR-GBIF' if tipo == 'I' else 'Complementaria'
    naturaleza = 'manglar' if nombre in manglar_set else 'limnológica'
    color = '#E91E63' if tipo == 'I' else '#FF9800'

    CircleMarker(
        location=[lat, lon],
        radius=5,
        color='white',
        weight=1.5,
        fill=True,
        fill_color=color,
        fill_opacity=0.95,
        tooltip=folium.Tooltip(
            f'<b>{nombre}</b><br><span style="font-size:10px">{naturaleza} · {fuente}</span>',
            sticky=False,
        ),
        popup=folium.Popup(
            f'<b>{nombre}</b><br>'
            f'Fuente: {fuente}<br>'
            f'Naturaleza espectral: {naturaleza}<br>'
            f'Coordenadas: {lat:.4f}, {lon:.4f}',
            max_width=260,
        ),
    ).add_to(m)

# Capa 2: etiquetas con nombres (sin fondo, opcional/prendible-apagable)
grupo_etiquetas = FeatureGroup(name='Etiquetas de estaciones', show=False)

for nombre, (lon, lat, tipo) in stations.items():
    naturaleza = 'manglar' if nombre in manglar_set else 'limnológica'
    color_texto = '#1B5E20' if naturaleza == 'manglar' else '#01579B'

    # Texto sin fondo, con borde blanco para legibilidad sobre cualquier basemap
    Marker(
        location=[lat, lon],
        icon=DivIcon(
            icon_size=(140, 18),
            icon_anchor=(70, -10),
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
        '🌿 Estado del manglar (NDVI)': [ly_ndvi_act, ly_ndvi_deg, ly_ndvi_rec, ly_ndvi_chg],
        '🗺️ Clasificación por periodo': [ly_md, ly_mr, ly_ma],
        '🔄 Dinámica de cambio 2020→2024': [ly_perdida, ly_estable, ly_ganancia],
        '💧 Inundación SAR sept-2020': [ly_sar_open, ly_sar_dose],
        '📍 Estaciones y AOI': [ly_aoi, grupo_etiquetas, ly_inv_buf, ly_com_buf],
        '📚 Referencias cartográficas': [
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
    'Manglar Actual': {tipo:'fill', color:'#81C784'},
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

  // Ensanchar el panel para que los símbolos no truncen el texto
  var ctrls = document.querySelectorAll('.leaflet-control-layers');
  ctrls.forEach(function(c) {
    c.style.maxWidth = '320px';
    c.style.fontSize = '12px';
    c.style.lineHeight = '1.5';
  });
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
<div id="cgsm-timeslider" style="position:absolute; bottom:24px; left:12px;
     z-index:1000;
     background:rgba(255,255,255,0.97); padding:10px 14px; border-radius:8px;
     box-shadow:0 2px 6px rgba(0,0,0,0.2);
     font-family:'Inter',-apple-system,sans-serif; font-size:12px;
     border:1px solid #d4e4dd; width:300px;">
  <div style="display:flex; align-items:center; justify-content:space-between;
       margin-bottom:6px;">
    <span><b style="color:#1f5a4b;">NDVI año:</b>
      <span id="cgsm-year-label" style="color:#1f5a4b; font-weight:700;
            font-size:14px; margin-left:4px;">{{this.year_max}}</span>
    </span>
    <button id="cgsm-ts-toggle" style="padding:3px 10px; font-size:11px;
            border:1px solid #1f5a4b; background:#1f5a4b; color:white;
            border-radius:4px; cursor:pointer; font-weight:600;">▶ Activar</button>
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

  function cgsmShowYear(year) {
    if (cgsmActiveLayer) { cgsmMap.removeLayer(cgsmActiveLayer); }
    cgsmActiveLayer = L.tileLayer(cgsmYears[year], {
      opacity: 0.85,
      attribution: 'Google Earth Engine · Sentinel-2 NDVI'
    });
    cgsmActiveLayer.addTo(cgsmMap);
  }

  var slider = document.getElementById('cgsm-year-slider');
  var label  = document.getElementById('cgsm-year-label');
  var toggle = document.getElementById('cgsm-ts-toggle');

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
}, 400);
{% endmacro %}
        """)


# Obtener mapId de cada composite anual (registro de visualización GEE, rápido)
print('Registrando tiles NDVI anuales en GEE...')
ndvi_urls = {y: img.getMapId(vis_ndvi)['tile_fetcher'].url_format
             for y, img in ndvi_anual.items()}
print(f'  {len(ndvi_urls)} URLs registradas.')

m.add_child(TimeSlider(ndvi_urls, vis_ndvi['palette']))

m.save(str(OUT_HTML))

print(f'\nDashboard exportado: {OUT_HTML}')
print(f'Tamano: {OUT_HTML.stat().st_size / 1024:.0f} KB')
print('Capas totales: 17 + slider NDVI anual 2018-2025')
