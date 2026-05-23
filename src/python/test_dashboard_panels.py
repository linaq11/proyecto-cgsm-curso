"""
Test sin GEE: genera solo los paneles (header + slider + stats) sobre un mapa
folium con basemap OSM, para validar visualmente que las 6 pestañas funcionen
sin depender del entrenamiento Random Forest ni de la autenticación GEE.

Uso:
    python src/python/test_dashboard_panels.py

Salida:
    outputs/maps/test_dashboard_panels.html
"""
from pathlib import Path
import json
import folium
import pandas as pd
from folium import FeatureGroup, CircleMarker
from branca.element import MacroElement
from jinja2 import Template

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'outputs' / 'maps' / 'test_dashboard_panels.html'
OUT.parent.mkdir(parents=True, exist_ok=True)

# Datos mínimos
stations = {
    'Isla Boqueron':   (-74.298, 10.962),
    'Punta Cerro':     (-74.283, 10.973),
    'Punta Chino':     (-74.305, 10.912),
    'Rio Sevilla':     (-74.325, 10.880),
    'Cano Palos':      (-74.471, 10.758),
    'CP Luna':         (-74.560, 10.870),
    'CP Aguas Negras': (-74.570, 10.800),
    'Cano Clarin':     (-74.500, 10.600),
}

ALERTAS_CSV = ROOT / 'outputs' / 'tables' / 'alertas_estaciones.csv'
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
conteo = df_alertas['estado'].value_counts().to_dict()
n_est, n_alt, n_crt = conteo.get('estable', 0), conteo.get('alerta', 0), conteo.get('critica', 0)
ESTADO_COLORS = {'estable': '#43A047', 'alerta': '#FBC02D', 'critica': '#D32F2F'}
ESTADO_ICON = {'estable': '🟢', 'alerta': '🟡', 'critica': '🔴'}

# Datos NDVI
NDVI_CSV = ROOT / 'outputs' / 'tables' / 'ndvi_combinado_2013_2025.csv'
df_ndvi = pd.read_csv(NDVI_CSV)
df_ndvi['estacion'] = df_ndvi['estacion'].str.replace('_', ' ').str.strip()
# Mapeo CSV (con tildes / nombres legacy) → canonical
csv_to_canon = {
    'Isla Boquerón': 'Isla Boqueron',
    'Río Sevilla':   'Rio Sevilla',
    'Caño Palos':    'Cano Palos',
    'Caño Clarín':   'Cano Clarin',
    'CP Pajarales':  'CP Luna',       # legacy → usar CP Luna como proxy
    'VIPIS':         'CP Aguas Negras',
}
df_ndvi['est_canon'] = df_ndvi['estacion'].map(lambda x: csv_to_canon.get(x, x))
ndvi_series = {}
for est in stations:
    sub = df_ndvi[df_ndvi['est_canon'] == est].sort_values('fecha')
    if len(sub):
        ndvi_series[est] = {
            'fechas': sub['fecha'].astype(str).tolist(),
            'ndvi':   [round(float(v), 4) for v in sub['ndvi'].tolist()],
        }

alertas_data = []
for est, info in estado_por_estacion.items():
    if est not in stations:
        continue
    alertas_data.append({
        'estacion': est,
        'icono': ESTADO_ICON.get(info['estado'], '⚪'),
        'estado': info['estado'],
        'z_actual': f"{info['z_actual']:+.2f}" if info.get('z_actual') is not None else '—',
        'ndvi_actual': f"{info['ndvi_actual']:.3f}" if info.get('ndvi_actual') is not None else '—',
        'razon': info.get('razon', '—'),
    })

print(f'NDVI series: {len(ndvi_series)} estaciones | alertas_data: {len(alertas_data)} entradas')

# Importar las clases macro del script de producción mediante importlib
import importlib.util
spec = importlib.util.spec_from_file_location(
    'mainscript',
    ROOT / 'src' / 'python' / 'make_dashboard_html.py'
)
# Evitar ejecución del cuerpo (que requiere GEE) — extraemos clases del source
src_text = (ROOT / 'src' / 'python' / 'make_dashboard_html.py').read_text()

# Extraer las clases HeaderPanel, TimeSlider y StatsPanel del source
import re

def extract_class(src, name):
    # Extraer hasta el primer renglón a columna 0 que no sea blank
    lines = src.split('\n')
    start = None
    for i, line in enumerate(lines):
        if line.startswith(f'class {name}('):
            start = i
            break
    if start is None:
        return None
    end = len(lines)
    for i in range(start + 1, len(lines)):
        line = lines[i]
        if line and not line.startswith((' ', '\t')) and not line.startswith('#'):
            end = i
            break
    return '\n'.join(lines[start:end])

ns = {'MacroElement': MacroElement, 'Template': Template}
for clase in ['HeaderPanel', 'TimeSlider', 'StatsPanel']:
    code = extract_class(src_text, clase)
    if code:
        exec(code, ns)
        print(f'  extraída: {clase}')

HeaderPanel = ns['HeaderPanel']
TimeSlider = ns['TimeSlider']
StatsPanel = ns['StatsPanel']

# Construir mapa
m = folium.Map(location=[10.85, -74.42], zoom_start=10, tiles='OpenStreetMap',
               control_scale=True)

# FeatureGroups por estado
fg_estable = FeatureGroup(name='__fg_estable', show=True, control=False)
fg_alerta  = FeatureGroup(name='__fg_alerta',  show=True, control=False)
fg_critica = FeatureGroup(name='__fg_critica', show=True, control=False)
fg_por_estado = {'estable': fg_estable, 'alerta': fg_alerta, 'critica': fg_critica}

for nombre, (lon, lat) in stations.items():
    info = estado_por_estacion.get(nombre, {})
    estado = info.get('estado', 'sin_datos')
    color = ESTADO_COLORS.get(estado, '#9E9E9E')
    icono = ESTADO_ICON.get(estado, '⚪')
    CircleMarker(
        location=[lat, lon], radius=7, color='white', weight=2,
        fill=True, fill_color=color, fill_opacity=0.95,
        tooltip=f'{icono} {nombre}: {estado}'
    ).add_to(fg_por_estado.get(estado, fg_estable))

fg_estable.add_to(m); fg_alerta.add_to(m); fg_critica.add_to(m)

# Slider dummy (URLs vacías)
dummy_palette = ['#8B0000', '#D32F2F', '#FF6F00', '#FDD835', '#7CB342', '#2E7D32', '#1B5E20']
dummy_urls = {y: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png' for y in range(2018, 2026)}
m.add_child(TimeSlider(dummy_urls, dummy_palette))

# Header + filtros
m.add_child(HeaderPanel(n_est, n_alt, n_crt,
                         fg_estable.get_name(), fg_alerta.get_name(), fg_critica.get_name()))

# Stats panel con las 6 pestañas
m.add_child(StatsPanel(ndvi_series, alertas_data))

m.save(str(OUT))
print(f'\nGenerado: {OUT}')
print(f'Tamaño: {OUT.stat().st_size / 1024:.0f} KB')
