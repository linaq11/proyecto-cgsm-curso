"""
Mapa de comparacion: AOI grande (5.073 km2) vs AOI acotado (~835 km2).

Genera un mapa HTML interactivo con folium que superpone los dos AOI
sobre un mapa base, para verificar visualmente el acotamiento antes de
reejecutar la cadena de procesamiento.

Salida:
    outputs/maps/comparacion_aoi.html

Uso:
    python3 src/python/visualizar_aoi.py
    # luego abrir outputs/maps/comparacion_aoi.html en el navegador
"""

from pathlib import Path
import folium
import geopandas as gpd

ROOT   = Path(__file__).resolve().parents[2]
RAW    = ROOT / "data" / "raw"
OUTMAP = ROOT / "outputs" / "maps"
OUTMAP.mkdir(parents=True, exist_ok=True)

aoi_grande   = gpd.read_file(RAW / "cgsm_aoi.geojson").to_crs(4326)
aoi_acotado  = gpd.read_file(RAW / "cgsm_aoi_acotado_4326.geojson").to_crs(4326)

# Calculo de areas en EPSG:9377 para reportar
area_grande_km2  = float(aoi_grande.to_crs(9377).geometry.area.iloc[0])  / 1e6
area_acotado_km2 = float(aoi_acotado.to_crs(9377).geometry.area.iloc[0]) / 1e6
print(f"AOI grande:   {area_grande_km2:,.1f} km2")
print(f"AOI acotado:  {area_acotado_km2:,.1f} km2")
print(f"Reduccion:    {area_grande_km2 / area_acotado_km2:.1f}x")

# Centroide del acotado para centrar el mapa
centroide = aoi_acotado.to_crs(9377).geometry.centroid.to_crs(4326).iloc[0]
m = folium.Map(location=[centroide.y, centroide.x], zoom_start=10,
               tiles="OpenStreetMap")
folium.TileLayer("Esri.WorldImagery", name="Satelite Esri").add_to(m)

folium.GeoJson(
    aoi_grande,
    name=f"AOI grande ({area_grande_km2:,.0f} km2)",
    style_function=lambda x: {"color": "#d62728", "weight": 2,
                              "fillColor": "#d62728", "fillOpacity": 0.05},
    tooltip="AOI grande baseline (5.073 km2)",
).add_to(m)

folium.GeoJson(
    aoi_acotado,
    name=f"AOI acotado ({area_acotado_km2:,.0f} km2)",
    style_function=lambda x: {"color": "#2ca02c", "weight": 2,
                              "fillColor": "#2ca02c", "fillOpacity": 0.20},
    tooltip="AOI acotado SFF + VPI (~835 km2)",
).add_to(m)

# Estaciones de muestreo INVEMAR
estaciones = [
    ("Isla_Boqueron",    -74.298457, 10.962255, "INVEMAR"),
    ("Punta_Cerro",      -74.283206, 10.973076, "INVEMAR"),
    ("Punta_Chino",      -74.304827, 10.912032, "INVEMAR"),
    ("Rio_Sevilla",      -74.325228, 10.880496, "INVEMAR"),
    ("Cano_Palos",       -74.471258, 10.757558, "INVEMAR"),
    ("CP_Luna",          -74.56,     10.87,     "Complementaria"),
    ("CP_Aguas_Negras",  -74.57,     10.80,     "Complementaria"),
    ("Cano_Clarin",      -74.50,     10.60,     "Complementaria"),
]
fg_est = folium.FeatureGroup(name="Estaciones de muestreo")
for nombre, lon, lat, fuente in estaciones:
    color = "#1f77b4" if fuente == "INVEMAR" else "#ff7f0e"
    folium.CircleMarker([lat, lon], radius=5, color=color, fill=True,
                        fill_color=color, fill_opacity=0.9,
                        popup=f"{nombre} ({fuente})").add_to(fg_est)
fg_est.add_to(m)

folium.LayerControl(collapsed=False).add_to(m)

out = OUTMAP / "comparacion_aoi.html"
m.save(str(out))
print(f"\nGuardado: {out}")
