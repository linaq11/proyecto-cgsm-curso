# Guía de notebooks — Proyecto CGSM

El árbol de notebooks se organiza en dos series —vigente y legacy— pues a lo largo del proyecto el área de estudio se redefinió a partir de los polígonos oficiales del Sistema Nacional de Áreas Protegidas (RUNAP), de modo que las cifras del cuerpo del informe v6 dejaron de ser comparables con las de la primera iteración. La **serie vigente** opera sobre el AOI acotado al Santuario de Fauna y Flora CGSM y al Vía Parque Isla de Salamanca (835,3 km²) y es la que sostiene los resultados del informe; la **serie legacy/baseline**, en cambio, se ejecutó sobre un AOI envolvente de 5.073 km² (marzo 2026) y sus cifras se conservan en el Anexo C del informe únicamente como rastro metodológico, de manera que cualquier lector puede reconstruir el paso entre una versión y otra sin perder trazabilidad.

## Serie vigente — orden de ejecución

| # | Notebook / script | Lenguaje | Salida principal |
|---|-------------------|----------|------------------|
| 1 | `01_gee_acquisition.ipynb` | Python (GEE) | Composites trimestrales y anuales en Drive/CGSM_data_acotado |
| 2 | `02_time_series.ipynb` | Python | `serie_temporal_ndvi_definitiva.csv` (929 obs mensuales 2013–2025) |
| 3 | `02b_bfast_ndvi.R.ipynb` | R | 8 PNG bfast sobre las 8 estaciones (h = 0,10 y 0,15) |
| 4 | `02c_bfast_manglar_unificado.ipynb` | R | bfast unificado sobre las 4 estaciones de manglar denso |
| 5 | `03_segmentation_acotado.ipynb` | Python | `samgeo_acotado/manglar_*.geojson` + reproyección `*_9377.geojson` |
| 6 | `04_fragmentation_acotado.ipynb` | Julia | `metricas_fragmentacion_acotado.csv` (79→38→15 parches; MSI, NND) |
| 7 | `04b_topologia_acotado.ipynb` | Python | `parches_topologia_acotado.csv`, `estaciones_clasificadas.csv` |
| 8 | `04c_topologia_julia.ipynb` | Julia | Validación cruzada DE-9IM Python ↔ Julia (LibGEOS.jl) |
| 9 | `05_flooding_nasa_acotado.ipynb` | Python | Inundación SAR + GFD + JRC sobre AOI acotado (43,08 km² bajo dosel sep-2020) |
| 10 | `07_era5_clima.ipynb` | Python | `correlacion_clima_ndvi.csv` desagregada por naturaleza espectral |
| 11 | `08_validacion_multilingual.ipynb` | Python | `validacion_multilingual.csv` (Python+GEE ↔ R+stars) |
| 12 | `09b_datacube_extendido.ipynb` | Python | Tres datacubes NetCDF CF-1.8 (periodos, trimestral, Landsat anual) |
| 13 | `10_validacion_extendida.ipynb` | Python | Validación contra INVEMAR 1:25.000 y ESA WorldCover v200 (F1 = 0,583 y 0,548 umbrales) |
| 14 | `11_random_forest_benchmark.ipynb` | Python (GEE) | Benchmark Random Forest (F1 = 0,826 vs INVEMAR; 0,889 vs WorldCover); importancia de variables |
| 15 | `11_indices_enso_noaa.ipynb` | Python | Índices ENSO ONI y SOI de NOAA CPC, correlaciones por rezago |
| 16 | `11b_indices_enso_noaa_R.ipynb` | R | Réplica R del análisis ENSO con `tidyverse` |
| 17 | `12_chirps_cuenca_magdalena.ipynb` | Python | Precipitación CHIRPS sobre cuencas aportantes (Magdalena alta-media + Sierra Nevada) |
| 18 | `12_sentinel1_sar_serie.ipynb` | Python | Serie continua Sentinel-1 SAR-VH 2018–2025 + correlación SAR-VH ↔ NDVI |
| 19 | `12b_caudal_ideam_elbanco.ipynb` | Python | Caudal IDEAM El Banco (Magdalena) + Ganadería Caribe (Aracataca); correlaciones con NDVI |
| 20 | `12c_caudal_ideam_R.ipynb` | R | Réplica R del análisis de caudal (Python ↔ R hasta 3 decimales) |
| 21 | `13_validacion_invemar.ipynb` | Python | Validación específica contra cartografía INVEMAR 1:25.000 rasterizada |
| 22 | `14_validacion_trilingual.ipynb` | Python + R + Julia | Convergencia caudal-NDVI Python = R = Julia hasta 3 decimales |
| — | `src/python/make_dashboard_html.py` | Python (script) | `dashboard_CGSM_final.html` autocontenido con folium + 17 capas |
| — | `src/python/alertas_manglar.py` | Python (script) | Módulo de alertas tempranas Nivel 2 Digital Twin (`alertas_estaciones.csv`, `alertas_semaforo.png`) |

## Serie legacy / baseline (no ejecutar para los resultados vigentes)

Los notebooks listados a continuación corresponden a la primera iteración del proyecto sobre el AOI envolvente y se conservan en el repositorio por trazabilidad —pues sus cifras alimentan el Anexo C del informe—, de manera que **no se ejecutan para sostener las conclusiones del cuerpo del informe** sino que funcionan, en este sentido, como bitácora del recorrido metodológico.

| Notebook | Estado |
|----------|--------|
| `03_segmentation.ipynb` | Legacy — flujo original sobre AOI envolvente + algunas celdas finales sobre AOI acotado |
| `04_fragmentation.ipynb` (Julia) | Legacy — bloque inicial con aproximación esférica (EPSG:4326) + bloque final EPSG:9377 |
| `04b_topologia.ipynb` | Legacy — análisis sobre AOI envolvente |
| `05_flooding_nasa.ipynb` | Legacy — inundación NASA sobre AOI envolvente; sustituido por `05_flooding_nasa_acotado.ipynb` |
| `06_dashboard.ipynb` | Legacy — dashboard ipyleaflet sobre AOI envolvente; el HTML autocontenido lo produce ahora `src/python/make_dashboard_html.py` con AOI acotado |
| `09_datacube_netcdf.ipynb` | Legacy — versión preliminar del datacube sin reproyección a EPSG:9377 |
| `99_diagnose_ndvi_year.ipynb` | Diagnóstico — auxiliar para inspección puntual de capas NDVI por año |

Quien quiera reproducir el baseline del Anexo C debe ejecutar `03_segmentation.ipynb` y `04_fragmentation.ipynb` desde la primera celda, así como están, sin reemplazar el AOI; en cambio, para reproducir la v6 vigente —que es lo recomendado— se ejecutan los notebooks con sufijo `_acotado` y el `09b`, los cuales sustituyen por completo a sus homónimos legacy.

## Productos derivados (entregables del proyecto)

Para regenerar el dashboard sin pasar por Jupyter:

```bash
cd /home/rstudio/work/proyecto-cgsm
python src/python/make_dashboard_html.py
```

El script construye el HTML autocontenido con folium y AOI acotado leído de `data/raw/cgsm_aoi_acotado_4326.geojson`; los tiles de Earth Engine se sirven mediante `mapId` con vigencia de algunas horas, de modo que conviene regenerarlo poco antes de presentar.

Para regenerar el módulo de alertas tempranas:

```bash
python src/python/alertas_manglar.py
```

Para renderizar el informe técnico y el artículo journal:

```bash
quarto render docs/informe_final.qmd          # 28 páginas · PDF + HTML + DOCX
quarto render docs/articulo_cgsm_journal.qmd  # ~5.300 palabras · PDF + HTML
```

## Carpetas y convenciones de salida

| Carpeta | Contiene | Usado en |
|---------|----------|----------|
| `data/raw/` | AOI acotado GeoJSON, shapefiles RUNAP, INVEMAR-GBIF, IDEAM-DHIME | Todos |
| `data/processed/rgb_acotado/` | 3 RGB Sentinel-2 sobre AOI acotado | 03_acotado, 09b |
| `data/processed/rgb/` | 3 RGB sobre AOI envolvente (legacy) | 03 legacy |
| `data/processed/s2/` | Composites trimestrales NDVI/NDWI/CMRI (descargar de Drive) | 02, 09b |
| `data/processed/landsat/` | Composites anuales Landsat (descargar de Drive) | 02, 09b |
| `data/processed/samgeo_acotado/` | Máscaras + GeoJSON SamGeo sobre AOI acotado | 04_acotado, 04b_acotado, 10 |
| `data/processed/cubo/` | NetCDF CF-1.8 generados por 09b (periodos 40 MB, trimestral 275 MB, Landsat 119 MB) | 09b, todos los análisis posteriores |
| `data/validation/` | Cartografía de referencia INVEMAR 1:25.000 y ESA WorldCover v200 | 10, 11, 13 |
| `outputs/tables/` | 47 CSV con resultados numéricos | Todos |
| `outputs/figures/` | 35 PNG estáticos (mapas, series, correlaciones, validación, alertas) | bfast, ERA5, ENSO, caudal, CHIRPS, validación, alertas |
| `outputs/maps/` | HTML interactivos (`dashboard_CGSM_final.html`) | `make_dashboard_html.py`, 06 legacy |
| `docs/` | Informe Quarto, artículo journal, dashboard ejecutivo `dashboard.html` | Quarto + GitHub Pages |

## Insumos externos que requieren descarga manual

| Insumo | Cómo obtener | Destino local |
|--------|--------------|---------------|
| Composites trimestrales S2 | Drive/CGSM_data_acotado → manual o Drive Desktop | `data/processed/s2/` |
| Composites anuales Landsat | Drive/CGSM_data_acotado → manual o Drive Desktop | `data/processed/landsat/` |
| INVEMAR manglares 1:25.000 | Servicio ArcGIS REST `SIGMA/MANGLARES_COLOMBIA` (notebook 13) | `data/validation/invemar_manglares_25k.geojson` |
| ESA WorldCover v200 | GEE `ESA/WorldCover/v200`, clase 95 (notebook 10) | Acceso vía GEE, sin descarga local |
| Polígonos RUNAP | <https://runap.parquesnacionales.gov.co/> | `data/raw/Ciénaga Grande de Santa Marta_1126/` |
| Caudal IDEAM | Portal DHIME → estaciones El Banco (25027020) y Ganadería Caribe (29067150) | `data/raw/Datos_de_Estaciones_de_IDEAM_*.csv` |
| INVEMAR-GBIF estaciones | DOI [10.15472/0fqdp4](https://doi.org/10.15472/0fqdp4) | `data/raw/invemar_gbif_estaciones.csv` |

## Credenciales requeridas

- **GEE**: autenticación vía `gcloud auth application-default login` con quota project configurado en `~/.config/gcloud/application_default_credentials.json`
- **CDS API**: archivo `~/.cdsapirc` con URL y key de <https://cds.climate.copernicus.eu/> (para ERA5-Land)
- **GitHub**: Personal Access Token para `git push` si se trabaja sobre el repositorio remoto

## Validaciones cruzadas multilingües (Anexo)

Las cuatro validaciones cruzadas formales que verifican la convergencia entre lenguajes:

1. **Serie NDVI Python ↔ R**: `08_validacion_multilingual.ipynb` (ρ > 0,95; RMSE < 0,05)
2. **Correlación caudal-NDVI Python = R = Julia**: `14_validacion_trilingual.ipynb` (convergencia hasta 3 decimales)
3. **Topología DE-9IM Python ↔ Julia**: `04c_topologia_julia.ipynb` (conteos idénticos de parches en borde)
4. **Réplicas ENSO + caudal en R**: `11b_indices_enso_noaa_R.ipynb` + `12c_caudal_ideam_R.ipynb` (16 + 8 filas idénticas)
