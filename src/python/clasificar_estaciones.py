"""
Clasifica las 8 estaciones de muestreo CGSM por naturaleza espectral
(manglar vs limnologica) y por asociacion con el AOI acotado, y exporta
la tabla outputs/tables/estaciones_clasificadas.csv.

Uso:
    cd /home/rstudio/work/proyecto-cgsm
    python3 src/python/clasificar_estaciones.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

import geopandas as gpd
import pandas as pd

from python.utils import estaciones_geodataframe, etiquetar_estaciones_aoi

AOI_9377 = ROOT / "data" / "raw" / "cgsm_aoi_acotado_9377.geojson"
NDVI_CSV = ROOT / "outputs" / "tables" / "serie_temporal_ndvi_definitiva.csv"
OUT_CSV  = ROOT / "outputs" / "tables" / "estaciones_clasificadas.csv"

aoi = gpd.read_file(AOI_9377)
est = etiquetar_estaciones_aoi(estaciones_geodataframe(), aoi, buffer_m=2000.0)

df = pd.DataFrame(est.drop(columns="geometry"))
df["dist_a_aoi_m"] = df["dist_a_aoi_m"].round(0).astype(int)

ndvi = pd.read_csv(NDVI_CSV)
df["ndvi_mediano"] = df["estacion"].map(
    ndvi.groupby("subzona")["ndvi"].median().round(3).to_dict()
)
df = df.sort_values(["naturaleza", "fuente", "estacion"]).reset_index(drop=True)
df.to_csv(OUT_CSV, index=False)

print(df.to_string(index=False))
print("\nGuardado:", OUT_CSV)
print("\nResumen por naturaleza:")
print(df.groupby("naturaleza").agg(
    n=("estacion", "count"),
    ndvi_medio=("ndvi_mediano", "mean"),
    dist_media_km=("dist_a_aoi_m", lambda s: round(s.mean() / 1000, 2)),
    n_asociadas=("asociada_aoi", "sum"),
).round(3))
