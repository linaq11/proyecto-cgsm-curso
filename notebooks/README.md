# Guía de notebooks — Proyecto CGSM

Los notebooks se dividen en dos series: la **serie vigente** sobre el AOI acotado (SFF CGSM + VPI Salamanca, 835 km²) que produce los resultados reportados en el cuerpo del informe v6, y la **serie legacy/baseline** sobre el AOI envolvente de 5.073 km² (marzo 2026) cuyas cifras se conservan en el Anexo C del informe para trazabilidad metodológica.

## Serie vigente (v6) — orden de ejecución

| # | Notebook | Lenguaje | Salida principal |
|---|----------|----------|------------------|
| 1 | `01_gee_acquisition.ipynb` | Python (GEE) | Composites trimestrales y anuales en Drive/CGSM_data_acotado |
| 2 | `02_time_series.ipynb` | Python | `serie_temporal_ndvi_definitiva.csv` |
| 3 | `02b_bfast_ndvi.R.ipynb` | R | 8 PNG bfast |
| 4 | `03_segmentation_acotado.ipynb` | Python | `samgeo_acotado/manglar_*.geojson` + `*_9377.geojson` |
| 5 | `04_fragmentation_acotado.ipynb` | Julia | `metricas_fragmentacion_acotado.csv` |
| 6 | `04b_topologia_acotado.ipynb` | Python | `parches_topologia_acotado.csv`, `estaciones_clasificadas.csv` |
| 7 | `05_flooding_nasa.ipynb` | Python | Inundación SAR + Global Flood Database + JRC |
| 8 | `06_dashboard.ipynb` | Python | `dashboard_CGSM_final.html` |
| 9 | `07_era5_clima.ipynb` | Python | `correlacion_clima_ndvi.csv` desagregada |
| 10 | `08_validacion_multilingual.ipynb` | Python | `validacion_multilingual.csv` |
| 11 | `09b_datacube_extendido.ipynb` | Python | `cgsm_datacube_periodos.nc` + trimestral + landsat |
| 12 | `10_validacion_extendida.ipynb` | Python | `validacion_gmw_acotado.csv` (cuando GMW raster exista) |

## Serie legacy/baseline (no ejecutar para v6)

Estos notebooks corresponden a la primera iteración del proyecto sobre AOI envolvente. Se conservan para trazabilidad pero **no se usan para sostener las conclusiones del informe**.

| Notebook | Estado |
|----------|--------|
| `03_segmentation.ipynb` | Legacy — flujo original sobre AOI envolvente + algunas celdas finales sobre AOI acotado |
| `04_fragmentation.ipynb` (Julia) | Legacy — bloque inicial con aproximación esférica (4326) + bloque final 9377 |
| `04b_topologia.ipynb` | Legacy — análisis sobre AOI envolvente |
| `09_datacube_netcdf.ipynb` | Legacy — versión preliminar del datacube sin reproyección a 9377 |

Para reproducir el baseline del Anexo C: ejecutar `03_segmentation.ipynb` y `04_fragmentation.ipynb` desde el inicio.

Para reproducir la v6 vigente: ejecutar los notebooks "_acotado" o el 09b en lugar de sus homónimos legacy.

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
