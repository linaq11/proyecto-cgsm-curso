# Guía de notebooks — Proyecto CGSM

El árbol de notebooks se organiza en dos series —vigente y legacy— pues a lo largo del proyecto el área de estudio se redefinió a partir de los polígonos oficiales del Sistema Nacional de Áreas Protegidas, de modo que las cifras del cuerpo del informe v6 dejaron de ser comparables con las de la primera iteración. La **serie vigente** opera sobre el AOI acotado al Santuario de Fauna y Flora CGSM y al Vía Parque Isla de Salamanca (835 km²) y es la que sostiene los resultados del informe; la **serie legacy/baseline**, en cambio, se ejecutó sobre un AOI envolvente de 5.073 km² (marzo 2026) y sus cifras se conservan en el Anexo C únicamente como rastro metodológico, de manera que cualquier lector puede reconstruir el paso entre una versión y otra sin perder trazabilidad.

## Serie vigente (v6) — orden de ejecución

| # | Notebook | Lenguaje | Salida principal |
|---|----------|----------|------------------|
| 1 | `01_gee_acquisition.ipynb` | Python (GEE) | Composites trimestrales y anuales en Drive/CGSM_data_acotado |
| 2 | `02_time_series.ipynb` | Python | `serie_temporal_ndvi_definitiva.csv` |
| 3 | `02b_bfast_ndvi.R.ipynb` | R | 8 PNG bfast |
| 4 | `03_segmentation_acotado.ipynb` | Python | `samgeo_acotado/manglar_*.geojson` + `*_9377.geojson` |
| 5 | `04_fragmentation_acotado.ipynb` | Julia | `metricas_fragmentacion_acotado.csv` |
| 6 | `04b_topologia_acotado.ipynb` | Python | `parches_topologia_acotado.csv`, `estaciones_clasificadas.csv` |
| 7 | `05_flooding_nasa_acotado.ipynb` | Python | Inundación SAR + GFD + JRC sobre AOI acotado |
| 8 | `src/python/make_dashboard_html.py` | Python (script) | `dashboard_CGSM_final.html` autocontenido (folium) |
| 9 | `07_era5_clima.ipynb` | Python | `correlacion_clima_ndvi.csv` desagregada |
| 10 | `08_validacion_multilingual.ipynb` | Python | `validacion_multilingual.csv` |
| 11 | `09b_datacube_extendido.ipynb` | Python | `cgsm_datacube_periodos.nc` + trimestral + landsat |
| 12 | `10_validacion_extendida.ipynb` | Python | `validacion_gmw_acotado.csv` (cuando GMW raster exista) |

## Serie legacy/baseline (no ejecutar para v6)

Los notebooks que se listan a continuación corresponden a la primera iteración del proyecto sobre el AOI envolvente y se conservan en el repositorio por trazabilidad —pues sus cifras alimentan el Anexo C—, de manera que **no se ejecutan para sostener las conclusiones del cuerpo del informe** sino que funcionan, en este sentido, como bitácora del recorrido metodológico.

| Notebook | Estado |
|----------|--------|
| `03_segmentation.ipynb` | Legacy — flujo original sobre AOI envolvente + algunas celdas finales sobre AOI acotado |
| `04_fragmentation.ipynb` (Julia) | Legacy — bloque inicial con aproximación esférica (4326) + bloque final 9377 |
| `04b_topologia.ipynb` | Legacy — análisis sobre AOI envolvente |
| `05_flooding_nasa.ipynb` | Legacy — inundación NASA sobre AOI envolvente; sustituido por `05_flooding_nasa_acotado.ipynb` |
| `06_dashboard.ipynb` | Legacy — dashboard ipyleaflet sobre AOI envolvente; el HTML autocontenido lo produce ahora `src/python/make_dashboard_html.py` con AOI acotado |
| `09_datacube_netcdf.ipynb` | Legacy — versión preliminar del datacube sin reproyección a 9377 |

Quien quiera reproducir el baseline del Anexo C debe ejecutar `03_segmentation.ipynb` y `04_fragmentation.ipynb` desde la primera celda, así como están, sin reemplazar el AOI; en cambio, para reproducir la v6 vigente —que es lo recomendado— se ejecutan los notebooks con sufijo `_acotado` y el `09b`, los cuales sustituyen por completo a sus homónimos legacy.

Para regenerar el dashboard sin pasar por Jupyter:

```bash
cd /home/rstudio/work/proyecto-cgsm
python src/python/make_dashboard_html.py
```

El script construye el HTML autocontenido con folium y AOI acotado leído de `data/raw/cgsm_aoi_acotado_4326.geojson`; los tiles de Earth Engine se sirven mediante mapId con vigencia de algunas horas, de modo que conviene regenerarlo poco antes de presentar.

## Carpetas y convenciones de salida

| Carpeta | Contiene | Usado en |
|---------|----------|----------|
| `data/raw/` | AOI acotado GeoJSON, shapefiles RUNAP | Todos |
| `data/processed/rgb_acotado/` | 3 RGB Sentinel-2 sobre AOI acotado | 03_acotado, 09b |
| `data/processed/rgb/` | 3 RGB sobre AOI envolvente (legacy) | 03 legacy |
| `data/processed/s2/` | Composites trimestrales NDVI/NDWI/CMRI (descargar de Drive) | 02, 09b |
| `data/processed/landsat/` | Composites anuales Landsat (descargar de Drive) | 02, 09b |
| `data/processed/samgeo_acotado/` | Máscaras + GeoJSON SamGeo sobre AOI acotado | 04_acotado, 04b_acotado, 10 |
| `data/processed/cubo/` | NetCDF CF-1.8 generados por 09b | 09b |
| `data/validation/gmw/` | Raster GMW v4.0 sobre CGSM (descargar de GEE) | 10 |
| `outputs/tables/` | CSVs con resultados numéricos | Todos |
| `outputs/figures/` | PNG estáticos | bfast, ERA5, validación |
| `outputs/maps/` | HTML interactivos (dashboard, mapas leafmap) | `make_dashboard_html.py`, 06 legacy |

## Insumos externos que requieren descarga manual

| Insumo | Cómo obtener | Destino local |
|--------|--------------|---------------|
| Composites trimestrales S2 | Drive/CGSM_data_acotado → manual o Drive Desktop | `data/processed/s2/` |
| Composites anuales Landsat | Drive/CGSM_data_acotado → manual o Drive Desktop | `data/processed/landsat/` |
| GMW v4.0 raster CGSM | Notebook con `geemap.ee_export_image` | `data/validation/gmw/gmw_v4_2020_cgsm.tif` |
| Polígonos RUNAP | https://runap.parquesnacionales.gov.co/ | `data/raw/Ciénaga Grande de Santa Marta_1126/` |

## Credenciales requeridas

- **GEE**: autenticación via `gcloud auth application-default login` con quota project `basic-buttress-338101`
- **CDS API**: archivo `~/.cdsapirc` con URL y key de https://cds.climate.copernicus.eu/
- **GitHub**: Personal Access Token para push
