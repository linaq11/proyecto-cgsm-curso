"""
Construccion del AOI acotado CGSM.

Une los poligonos oficiales del Santuario de Fauna y Flora Cienaga Grande
de Santa Marta y del Via Parque Isla de Salamanca (descargados del
Registro Unico Nacional de Areas Protegidas, RUNAP) en un unico poligono
de area de estudio acotado a la zona con figura de proteccion.

Sustituye al poligono envolvente de 5.073 km2 que se utilizo en el
baseline por uno cercano a los 560 km2 que corresponde al humedal real
con figura legal de proteccion.

Entradas (Shapefiles del RUNAP):
    data/raw/Cienaga Grande de Santa Marta_1126/runap_id_pnn_02030001.shp
    data/raw/Isla de Salamanca_1525/runap_id_pnn_02050001.shp

Salidas:
    data/raw/cgsm_aoi_acotado_4326.geojson  -- para uso en GEE (lat/lon)
    data/raw/cgsm_aoi_acotado_9377.geojson  -- para analisis local en metros

Lina Maria Quintero Fonseca -- Maestria en Geomatica, UNAL (2026-1)
"""

from __future__ import annotations

import sys
from pathlib import Path

import geopandas as gpd
from shapely.ops import unary_union

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"

EPSG_NACIONAL = "EPSG:9377"
EPSG_GEOGRAFICO = "EPSG:4326"

# Las rutas usan el caracter "e con acento" tal como el RUNAP nombra la carpeta.
ENTRADAS = {
    "sff": RAW / "Ciénaga Grande de Santa Marta_1126" / "runap_id_pnn_02030001.shp",
    "vpi": RAW / "Isla de Salamanca_1525"                  / "runap_id_pnn_02050001.shp",
}

SALIDAS = {
    "geo":  RAW / "cgsm_aoi_acotado_4326.geojson",
    "proj": RAW / "cgsm_aoi_acotado_9377.geojson",
}


def cargar_polygon(path: Path) -> gpd.GeoDataFrame:
    if not path.exists():
        raise FileNotFoundError(
            "No encontrado: " + str(path) + "\n"
            "Descargalo de https://runap.parquesnacionales.gov.co/ y "
            "dejalo en data/raw/."
        )
    gdf = gpd.read_file(path)
    if gdf.crs is None:
        print("  Aviso: " + path.name + " sin CRS declarado, asumiendo 4326")
        gdf = gdf.set_crs(EPSG_GEOGRAFICO)
    if str(gdf.crs).upper() != EPSG_GEOGRAFICO:
        gdf = gdf.to_crs(EPSG_GEOGRAFICO)
    return gdf


def construir_aoi_acotado():
    sff = cargar_polygon(ENTRADAS["sff"])
    vpi = cargar_polygon(ENTRADAS["vpi"])
    print("SFF CGSM: " + str(len(sff)) + " poligono(s)")
    print("VPI Salamanca: " + str(len(vpi)) + " poligono(s)")

    union_geom = unary_union(list(sff.geometry) + list(vpi.geometry))

    gdf_4326 = gpd.GeoDataFrame(
        {
            "name": ["CGSM_AOI_acotado"],
            "components": ["SFF CGSM + Via Parque Isla de Salamanca"],
            "source": ["RUNAP / Parques Nacionales Naturales"],
        },
        geometry=[union_geom],
        crs=EPSG_GEOGRAFICO,
    )
    gdf_9377 = gdf_4326.to_crs(EPSG_NACIONAL)

    area_km2 = float(gdf_9377.geometry.area.iloc[0]) / 1_000_000.0
    print("\nArea del AOI acotado: {:,.1f} km2".format(area_km2))
    if not (300 < area_km2 < 900):
        print("  Aviso: el area esperada estaba ~560 km2. "
              "Verifica que descargaste los poligonos correctos.")
    return gdf_4326, gdf_9377


def escribir_salidas(gdf_4326, gdf_9377):
    SALIDAS["geo"].parent.mkdir(parents=True, exist_ok=True)
    gdf_4326.to_file(SALIDAS["geo"],  driver="GeoJSON")
    gdf_9377.to_file(SALIDAS["proj"], driver="GeoJSON")
    print("\nGuardado:\n  " + str(SALIDAS["geo"]) + "\n  " + str(SALIDAS["proj"]))


def main():
    try:
        gdf_4326, gdf_9377 = construir_aoi_acotado()
    except FileNotFoundError as exc:
        print("ERROR: " + str(exc), file=sys.stderr)
        return 1
    escribir_salidas(gdf_4326, gdf_9377)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
