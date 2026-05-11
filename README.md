# Pipeline multilenguaje (Python, R, Julia) para el monitoreo de manglar en la CGSM (2013-2025)

Proyecto final - Programacion en SIG: Python, R y Julia
Maestria en Geomatica, Universidad Nacional de Colombia
Docente: Alexys H. Rodriguez-Avellaneda PhD.
Estudiante: Lina Maria Quintero Fonseca - 2026-1

## Descripcion

Cadena de procesamiento GeoAI multilenguaje para el monitoreo de la dinamica espaciotemporal
de la cobertura de manglar en la Cienaga Grande de Santa Marta (CGSM), Colombia, sobre el
area protegida acotada (SFF CGSM + Via Parque Isla de Salamanca, ~835 km2) reproyectada al
sistema oficial colombiano EPSG:9377 MAGNA-SIRGAS Origen Nacional.

## Resultados principales (AOI acotado, EPSG:9377)

- Serie temporal 2013-2025: 929 registros NDVI combinando Landsat 8 (345) y Sentinel-2 (584)
- 18 anomalias significativas (z < -2), septiembre 2020 como evento mas severo (La Nina)
- Quiebre estructural en 2016 detectado por bfast en 7/8 estaciones (El Nino 2015-2016)
- Cobertura de manglar (Julia, envolvente): 12.426 -> 8.651 -> 4.037 ha (degradacion, recuperacion, actual)
- Cobertura de manglar (Python, area efectiva): 17 -> 17 -> 15 parches >= 1 ha
- Fragmentacion: NND 1,1 -> 2,4 km, MSI 0,51 -> 1,46 entre 2020 y 2024-2025
- Acoplamiento ERA5-Land: correlacion clima-NDVI desagregada por naturaleza espectral de las 4 estaciones de manglar (rho = -0,12 con lag 2 meses) y 4 limnologicas (rho = +0,29 con lag 2 meses)
- Validacion preliminar contra GMW v4.0: F1=0.442, OA=0.899, Kappa~0.38
- Datacube NetCDF CF-1.8 sobre EPSG:9377 con 3 periodos de referencia
- Dashboard interactivo con 15 capas tematicas

## Notebooks

| Notebook | Estado | Vigencia |
|----------|--------|----------|
| 01_gee_acquisition.ipynb | Fase 1: datacube S2 + Landsat | **Vigente** (AOI acotado, exportacion a Drive/CGSM_data_acotado) |
| 02_time_series.ipynb | Fase 2: z-scores y series temporales (Python) | Vigente |
| 02b_bfast_ndvi.R.ipynb | Fase 2: deteccion de quiebres con bfast (R) | Vigente |
| 03_segmentation.ipynb | Fase 3: SamGeo + reproyeccion EPSG:9377 | **Vigente** ejecutar las celdas que apuntan a `samgeo_acotado/`; las celdas que escriben sobre `samgeo/` corresponden al baseline preliminar y se conservan por trazabilidad |
| 04_fragmentation.ipynb | Fase 4: metricas de fragmentacion (Julia) | **Vigente** ejecutar el bloque que apunta a `samgeo_acotado/manglar_*_9377.geojson`; el bloque legado sobre `samgeo/` (con aproximacion esferica) se conserva para comparacion historica |
| 04b_topologia.ipynb | Predicados topologicos DE-9IM (Python) | Vigente (AOI acotado) |
| 05_flooding_nasa.ipynb | Validacion NASA SAR + GFD + JRC | Vigente (baseline grande, no se reejecuto sobre AOI acotado) |
| 06_dashboard.ipynb | Fase 5: dashboard interactivo (15 capas) | Vigente |
| 07_era5_clima.ipynb | Forzamiento climatico ERA5-Land (Cap. 20) | Vigente |
| 08_validacion_multilingual.ipynb | Comparacion series Python+GEE vs R+stars | Vigente |
| 09_datacube_netcdf.ipynb | Datacube NetCDF CF-1.8 sobre EPSG:9377 | Vigente (detecta TIFs automaticamente; produce hasta 3 NetCDF complementarios) |

## Estructura de directorios

```
data/raw/             AOI acotado RUNAP, shapefiles SFF y VPI, NetCDF ERA5
data/processed/
  rgb_acotado/        3 RGB Sentinel-2 sobre AOI acotado (insumo SamGeo)
  rgb/                3 RGB del baseline (AOI envolvente, conservados por trazabilidad)
  samgeo_acotado/     Mascaras SamGeo + GeoJSON 4326 + GeoJSON 9377 + GeoJSON topologia
  samgeo/             Salidas SamGeo del baseline preliminar
  cubo/               NetCDF CF-1.8 del datacube
src/python/utils.py   Reproyeccion 9377, lectura perezosa, DE-9IM, clasificacion estaciones
src/python/aoi_acotado.py  Construccion del AOI acotado desde shapefiles RUNAP
src/python/clasificar_estaciones.py  Clasifica 8 estaciones por naturaleza espectral
src/julia/04_fragmentacion.jl  Fragmentacion en Julia con bloques legado y 9377
src/R/05_stars_cubo.R  Cubo stars desde TIFs trimestrales (Cap. 21)
docs/informe_final.qmd Informe Quarto reproducible
docs/INSTRUCCIONES_EJECUCION.md  Orden paso a paso para reproducir en Docker
outputs/tables/       17+ archivos CSV con resultados numericos
outputs/figures/      Graficos y mapas estaticos
outputs/maps/         Dashboard HTML interactivo
```

## Requisitos

- Docker: alexyshr/sig_unal:v1.11
- Python: earthengine-api, geemap, segment-geospatial, leafmap, rasterio, geopandas, xarray, rioxarray, cdsapi, netCDF4
- R: bfast, terra, sf, ggplot2, stars, dplyr
- Julia: GeoJSON, DataFrames, CSV, Statistics
- Google Earth Engine: autenticacion via Application Default Credentials con `gcloud auth application-default login` + proyecto Cloud personal
- Climate Data Store: cuenta gratuita en https://cds.climate.copernicus.eu/ y archivo `~/.cdsapirc`

## Como reproducir

1. `git clone https://github.com/linaq11/proyecto-cgsm-curso.git`
2. Iniciar contenedor Docker sig_unal v1.11
3. Autenticar GEE con ADC (ver `docs/INSTRUCCIONES_EJECUCION.md`)
4. Descargar shapefiles RUNAP a `data/raw/` (SFF Cienaga Grande de Santa Marta + Isla de Salamanca)
5. Ejecutar `python3 src/python/aoi_acotado.py` para generar el AOI acotado
6. Ejecutar notebooks en orden: 01 -> 02 -> 02b -> 03 -> 04 -> 04b -> 05 -> 06 -> 07 -> 08 -> 09
7. Renderizar el informe: `cd docs && quarto render informe_final.qmd`
8. Resultados en `outputs/`

## Decisiones metodologicas clave

1. **AOI acotado a figura legal de proteccion**: el area de estudio se redujo de los 5.073 km2 del baseline envolvente a los 835 km2 del SFF CGSM + VPI Salamanca, de acuerdo con los poligonos oficiales del RUNAP. Las cifras del baseline se conservan en el Anexo C del informe para trazabilidad.
2. **EPSG:9377 MAGNA-SIRGAS Origen Nacional**: todos los productos geometricos se reproyectan al sistema oficial colombiano, conforme a la Resolucion IGAC 471 de 2020.
3. **Clasificacion de estaciones por naturaleza espectral**: las 8 estaciones de muestreo se separan en 4 limnologicas (sobre cuerpo de agua) y 4 de manglar, lo que evita que el promedio simple enmascare senales reales en los analisis de correlacion clima-NDVI.
4. **Fragmentacion Julia vs Python**: la diferencia entre los conteos de parches obedece a que Julia procesa solo el anillo exterior de cada poligono mientras Python descuenta huecos interiores; ambas mediciones son validas pero responden preguntas diferentes (ver Anexo D del informe).
5. **Datacube NetCDF CF-1.8**: el OE1 se materializa en `cgsm_datacube_periodos.nc` y, cuando los composites trimestrales se descargan a `data/processed/s2/`, tambien en `cgsm_datacube_trimestral.nc` y `cgsm_datacube_landsat.nc`.

## Trabajo futuro

- Validar la cadena causal La Nina -> caudal -> mortandad con series IDEAM (Calamar, Plato, Aracataca, Fundacion, Rio Frio)
- Complementar ERA5-Land con Oceanic Nino Index y Southern Oscillation Index de NOAA
- Validacion cruzada de SamGeo contra cartografia INVEMAR 2020 a escala 1:25.000
- Unificar el conjunto de 8 estaciones entre el analisis bfast historico y la clasificacion espectral actual
- Empaquetar el datacube como STAC catalog con pystac

## Fuentes de datos

- Sentinel-2 L2A: COPERNICUS/S2_SR_HARMONIZED (789 imagenes, 2018-2025)
- Landsat 8/9 C2 L2: LANDSAT/LC08/C02/T1_L2 (328 imagenes, 2013-2025)
- Sentinel-1 SAR: COPERNICUS/S1_GRD (banda VH, modo IW)
- Global Flood Database: GLOBAL_FLOOD_DB (16 eventos 2001-2017)
- JRC Surface Water: JRC/GSW1_4
- GMW v4.0: sat-io/GMW/annual-extent (referencia 2020)
- SRTM v3: USGS/SRTMGL1_003
- INVEMAR: GBIF DOI 10.15472/0fqdp4 (5 estaciones de monitoreo)
- ERA5-Land monthly: reanalysis-era5-land-monthly-means (CDS ECMWF)
- RUNAP: poligonos oficiales SFF CGSM (cod. 1126) y VPI Isla de Salamanca (cod. 1525)

## Licencia

MIT
