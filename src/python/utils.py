"""
Utilidades reutilizables del pipeline CGSM.

Concentra los patrones validados en los talleres del curso de Programacion SIG:

* reproject_to_9377    -- Tarea 19: reproyeccion a MAGNA-SIRGAS Origen Nacional
* lazy_open_window     -- Tarea 18: lectura perezosa de rasters por bloques
* raster_metadata      -- Tarea 18: metadatos sin materializar la grilla
* vector_to_9377       -- reproyeccion de capas vectoriales
* area_ha_9377         -- area en hectareas sobre proyeccion equivalente
* parches_borde        -- Cap. 16: predicado intersects con frontera del AOI
* parches_con_punto    -- Cap. 16: predicado contains con puntos de muestreo
* estaciones_geodataframe -- 8 estaciones CGSM clasificadas por naturaleza
* etiquetar_estaciones_aoi -- distancia y asociacion al AOI con buffer

Lina Maria Quintero Fonseca -- Maestria en Geomatica, UNAL (2026-1)
"""

from __future__ import annotations

import os
from pathlib import Path

import geopandas as gpd
import rasterio
from rasterio.warp import Resampling, calculate_default_transform, reproject
from rasterio.windows import Window

EPSG_NACIONAL = "EPSG:9377"
EPSG_GEOGRAFICO = "EPSG:4326"


# ---------------------------------------------------------------------------
# Reproyeccion raster (Tarea 19)
# ---------------------------------------------------------------------------

def reproject_to_9377(src_path, dst_path, resampling=Resampling.bilinear):
    """Reproyecta un GeoTIFF al EPSG:9377 conservando metadatos."""
    src_path = Path(src_path)
    dst_path = Path(dst_path)
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    with rasterio.open(src_path) as src:
        transform, width, height = calculate_default_transform(
            src.crs, EPSG_NACIONAL, src.width, src.height, *src.bounds
        )
        kwargs = src.meta.copy()
        kwargs.update(crs=EPSG_NACIONAL, transform=transform,
                      width=width, height=height)
        with rasterio.open(dst_path, "w", **kwargs) as dst:
            for i in range(1, src.count + 1):
                reproject(
                    source=rasterio.band(src, i),
                    destination=rasterio.band(dst, i),
                    src_transform=src.transform, src_crs=src.crs,
                    dst_transform=transform, dst_crs=EPSG_NACIONAL,
                    resampling=resampling,
                )
    return dst_path


# ---------------------------------------------------------------------------
# Lectura perezosa por ventanas (Tarea 18)
# ---------------------------------------------------------------------------

def lazy_open_window(src_path, block_size=1024):
    """Itera ventanas de lectura sobre un raster sin cargar la grilla a RAM."""
    with rasterio.open(src_path) as src:
        for top in range(0, src.height, block_size):
            for left in range(0, src.width, block_size):
                width = min(block_size, src.width - left)
                height = min(block_size, src.height - top)
                yield Window(left, top, width, height), src


def raster_metadata(src_path):
    """Devuelve metadatos sin materializar la grilla."""
    with rasterio.open(src_path) as src:
        return {
            "shape": (src.height, src.width),
            "count": src.count,
            "dtype": src.dtypes[0],
            "crs": str(src.crs),
            "res": src.res,
            "bounds": tuple(src.bounds),
            "nodata": src.nodata,
        }


# ---------------------------------------------------------------------------
# Reproyeccion vectorial y areas en hectareas
# ---------------------------------------------------------------------------

def vector_to_9377(src_path, dst_path):
    """Reproyecta un GeoJSON/Shapefile al EPSG:9377 y lo escribe a disco."""
    src_path = Path(src_path)
    dst_path = Path(dst_path)
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    gdf = gpd.read_file(src_path)
    if gdf.crs is None:
        gdf = gdf.set_crs(EPSG_GEOGRAFICO)
    gdf = gdf.to_crs(EPSG_NACIONAL)
    gdf.to_file(dst_path, driver="GeoJSON")
    return dst_path


def area_ha_9377(gdf):
    """Agrega columna area_ha calculada sobre EPSG:9377."""
    if str(gdf.crs).upper() != EPSG_NACIONAL:
        gdf = gdf.to_crs(EPSG_NACIONAL)
    gdf = gdf.copy()
    gdf["area_ha"] = gdf.geometry.area / 10_000.0
    gdf["perim_m"] = gdf.geometry.length
    return gdf


# ---------------------------------------------------------------------------
# Predicados topologicos DE-9IM (Cap. 16, Practica 2)
# ---------------------------------------------------------------------------

def parches_borde(parches, aoi, tolerancia_m=30.0):
    """Identifica parches que intersecan la frontera del AOI."""
    if str(parches.crs).upper() != EPSG_NACIONAL:
        parches = parches.to_crs(EPSG_NACIONAL)
    if str(aoi.crs).upper() != EPSG_NACIONAL:
        aoi = aoi.to_crs(EPSG_NACIONAL)
    frontera = aoi.geometry.boundary.iloc[0]
    if tolerancia_m > 0:
        frontera = frontera.buffer(tolerancia_m)
    out = parches.copy()
    out["borde"] = out.geometry.intersects(frontera)
    return out


def parches_con_punto(parches, estaciones, nombre_col="estacion"):
    """Asocia a cada parche la estacion que contiene."""
    if str(parches.crs).upper() != EPSG_NACIONAL:
        parches = parches.to_crs(EPSG_NACIONAL)
    if str(estaciones.crs).upper() != EPSG_NACIONAL:
        estaciones = estaciones.to_crs(EPSG_NACIONAL)
    join = gpd.sjoin(
        parches, estaciones[[nombre_col, "geometry"]],
        predicate="contains", how="left",
    )
    join = (
        join.groupby(join.index)
        .agg({nombre_col: lambda s: ", ".join(sorted(set(s.dropna())))})
        .replace("", None)
    )
    out = parches.copy()
    out["estacion_dentro"] = join[nombre_col]
    out["con_estacion"] = out["estacion_dentro"].notna()
    return out


# ---------------------------------------------------------------------------
# Clasificacion de estaciones de muestreo (Opcion 4)
# ---------------------------------------------------------------------------

ESTACIONES_CGSM = [
    # (nombre, lon, lat, fuente, naturaleza)
    ("Isla_Boqueron",   -74.298457, 10.962255, "INVEMAR",        "limnologica"),
    ("Punta_Cerro",     -74.283206, 10.973076, "INVEMAR",        "limnologica"),
    ("Punta_Chino",     -74.304827, 10.912032, "INVEMAR",        "limnologica"),
    ("Rio_Sevilla",     -74.325228, 10.880496, "INVEMAR",        "limnologica"),
    ("Cano_Palos",      -74.471258, 10.757558, "INVEMAR",        "manglar"),
    ("CP_Luna",         -74.56,     10.87,     "Complementaria", "manglar"),
    ("CP_Aguas_Negras", -74.57,     10.80,     "Complementaria", "manglar"),
    ("Cano_Clarin",     -74.50,     10.60,     "Complementaria", "manglar"),
]


def estaciones_geodataframe():
    """Devuelve las 8 estaciones como GeoDataFrame en EPSG:4326."""
    from shapely.geometry import Point as _P
    rows, geoms = [], []
    for nombre, lon, lat, fuente, naturaleza in ESTACIONES_CGSM:
        rows.append({"estacion": nombre, "fuente": fuente,
                     "naturaleza": naturaleza})
        geoms.append(_P(lon, lat))
    return gpd.GeoDataFrame(rows, geometry=geoms, crs=EPSG_GEOGRAFICO)


def etiquetar_estaciones_aoi(estaciones, aoi, buffer_m=2000.0):
    """Etiqueta estaciones con distancia al AOI y asociacion por buffer."""
    if str(estaciones.crs).upper() != EPSG_NACIONAL:
        estaciones = estaciones.to_crs(EPSG_NACIONAL)
    if str(aoi.crs).upper() != EPSG_NACIONAL:
        aoi = aoi.to_crs(EPSG_NACIONAL)
    aoi_geom = aoi.geometry.union_all()
    out = estaciones.copy()
    out["dist_a_aoi_m"] = out.geometry.apply(
        lambda g: float(g.distance(aoi_geom)))
    out["dentro_aoi"] = out.geometry.apply(lambda g: aoi_geom.contains(g))
    out["asociada_aoi"] = out.geometry.apply(
        lambda g: g.buffer(buffer_m).intersects(aoi_geom))
    return out


__all__ = [
    "EPSG_NACIONAL", "EPSG_GEOGRAFICO", "ESTACIONES_CGSM",
    "reproject_to_9377", "lazy_open_window", "raster_metadata",
    "vector_to_9377", "area_ha_9377",
    "parches_borde", "parches_con_punto",
    "estaciones_geodataframe", "etiquetar_estaciones_aoi",
]
