# Instrucciones de ejecución — Proyecto CGSM

Orden exacto en que se deben correr los notebooks y scripts en el contenedor Docker `image_sig_unal:v1.11_produccion_final` para reproducir los resultados nuevos del proyecto, posteriores a la versión v5 del informe.

---

## 0. Preparación previa (una sola vez)

### Credenciales

```bash
# Google Earth Engine
earthengine authenticate --auth_mode=notebook

# Climate Data Store (ECMWF) — para ERA5-Land
# 1. Crear cuenta gratuita en https://cds.climate.copernicus.eu/
# 2. Copiar la URL y la KEY desde el perfil de usuario
# 3. Crear el archivo ~/.cdsapirc con dos líneas:
#    url: https://cds.climate.copernicus.eu/api
#    key: <tu_uid>:<tu_api_key>
# 4. Aceptar los términos del dataset:
#    https://cds.climate.copernicus.eu/datasets/reanalysis-era5-land-monthly-means
```

### Polígonos oficiales del AOI acotado

Descargar de https://runap.parquesnacionales.gov.co/ los polígonos del Santuario de Fauna y Flora Ciénaga Grande de Santa Marta y del Vía Parque Isla de Salamanca, dejarlos en `data/raw/` con los nombres exactos:

```
data/raw/sff_cgsm.geojson
data/raw/via_parque_isla_salamanca.geojson
```

---

## 1. Construir el AOI acotado

```bash
cd /home/rstudio/work/proyecto-cgsm
python3 src/python/aoi_acotado.py
```

Salidas:
- `data/raw/cgsm_aoi_acotado_4326.geojson` (para GEE)
- `data/raw/cgsm_aoi_acotado_9377.geojson` (para análisis local)

Verifica en consola que el área reportada esté entre 300 y 900 km² (esperado ~560).

---

## 2. Clasificar las estaciones por naturaleza (manglar vs limnologica)

Una vez tienes el AOI acotado, corre el clasificador de estaciones:

```bash
python3 src/python/clasificar_estaciones.py
```

Genera `outputs/tables/estaciones_clasificadas.csv` con las 8 estaciones etiquetadas como `manglar` o `limnologica` segun su NDVI mediano historico, y con distancia al AOI + flag de asociacion por buffer de 2 km.

Resultado esperado: 4 estaciones manglar (Cano_Palos, Cano_Clarin, CP_Aguas_Negras, CP_Luna; NDVI medio ~0.59) y 4 limnologicas (Isla_Boqueron, Punta_Cerro, Punta_Chino, Rio_Sevilla; NDVI medio ~0.21). Solo Cano_Palos cae estrictamente dentro del AOI; Cano_Clarin y Rio_Sevilla quedan asociadas con buffer 2 km.

## 3. Reejecutar la cadena con AOI acotado

El notebook `01_gee_acquisition.ipynb` ya quedo modificado para cargar `data/raw/cgsm_aoi_acotado_4326.geojson` (celda 1) y exportar a la carpeta nueva `CGSM_data_acotado` en Drive (celdas 6, 8, 10, 12). Los demas notebooks heredan el AOI a traves del archivo en `data/raw/`, asi que basta con que lo verifiques en la primera celda de cada uno antes de reejecutar.

| Notebook | Tiempo aprox | Salidas que se sobrescriben |
|----------|--------------|------------------------------|
| `01_gee_acquisition.ipynb` | 30–60 min | 32 composites trimestrales S2 + 13 anuales Landsat + 3 RGB en Drive/CGSM_data_acotado |
| `02_time_series.ipynb` | 5 min | `serie_temporal_ndvi_definitiva.csv` |
| `02b_bfast_ndvi.R.ipynb` | 5 min | 8 PNG bfast |
| `03_segmentation.ipynb` | 60–120 min | `manglar_*.geojson`, `manglar_*_9377.geojson` |
| `04_fragmentation.ipynb` (Julia) | 5 min | `metricas_fragmentacion_9377.csv` |
| `04b_topologia.ipynb` | 2 min | `parches_topologia.csv`, `estaciones_clasificadas.csv` |

### Orden de ejecucion de las tareas de GEE

Al lanzar el notebook 01, dispara tres bloques de exportaciones a Drive:

1. **32 composites trimestrales Sentinel-2** (2018Q1 a 2025Q4, bandas NDVI/NDWI/CMRI, 10 m). Carpeta `CGSM_data_acotado`.
2. **13 composites anuales Landsat 8/9** (2013–2025, bandas NDVI/NDWI/CMRI, 30 m). Misma carpeta.
3. **3 RGB de los periodos de referencia** (degradacion 2020-S2, recuperacion 2022-S1, actual 2024-2025, 10 m, byte 0-255 para SamGeo). Misma carpeta.

Monitorea el progreso en https://code.earthengine.google.com bajo la pestana **Tasks**. Las exportaciones se pueden quedar en cola unos minutos; cada tarea individual tarda 1–5 min en correr. Cuando todas digan `COMPLETED`, descargalas con `gdown` o desde la interfaz de Drive a `data/processed/s2/`, `data/processed/landsat/` y `data/processed/rgb/` respectivamente.

### Que esperar de los nuevos numeros

Con AOI acotado a 835 km2 (vs 5.073 km2):
- Las cifras de area de manglar bajaran proporcionalmente (en bloque, del orden de 6x menos)
- El F1 contra GMW v4.0 deberia subir porque ahora la clasificacion ya no incluye vegetacion riberana fuera del humedal
- La fragmentacion del paisaje se reportara solo sobre la zona con figura legal de proteccion

---

## 3. Componente climático (Cap. 20)

```bash
jupyter notebook notebooks/07_era5_clima.ipynb
```

Tiempo: 10–30 min en cola del CDS para la descarga, 5 min de procesamiento. Salidas:

- `data/raw/era5_land_cgsm_monthly.nc`
- `outputs/tables/era5_anomalias_mensuales.csv`
- `outputs/tables/correlacion_clima_ndvi.csv`
- `outputs/figures/clima_vs_ndvi_2018_2025.png`

---

## 4. Componente cubo stars (Cap. 21)

Antes de correr el script R, descargar los TIFs trimestrales NDVI desde Google Drive (carpeta `CGSM_data`) a `data/processed/s2/` con nombres tipo `cgsm_s2_NDVI_2018_Q1.tif` ... `cgsm_s2_NDVI_2025_Q4.tif`.

```bash
Rscript src/R/05_stars_cubo.R
```

Tiempo: 5–15 min según número de TIFs. Salida:

- `outputs/tables/series_temporales_stars.csv`

---

## 5. Validación cruzada multilingüe

```bash
jupyter notebook notebooks/08_validacion_multilingual.ipynb
```

Salidas:
- `outputs/tables/validacion_multilingual.csv`
- `outputs/figures/validacion_multilingual_scatter.png`

---

## 6. Inundación SAR y dashboard (sin cambios)

```bash
jupyter notebook notebooks/05_flooding_nasa.ipynb
jupyter notebook notebooks/06_dashboard.ipynb
```

---

## 7. Renderizar informe v6

```bash
cd docs
quarto render informe_final.qmd
```

Genera `informe_final.html` y `informe_final.pdf` actualizados.

---

## 8. Versionar

```bash
cd /home/rstudio/work/proyecto-cgsm
git add data/raw/cgsm_aoi_acotado_*.geojson \
         src/python/utils.py src/python/aoi_acotado.py \
         src/R/05_stars_cubo.R src/julia/04_fragmentacion.jl \
         notebooks/04b_topologia.ipynb \
         notebooks/07_era5_clima.ipynb \
         notebooks/08_validacion_multilingual.ipynb \
         outputs/tables/areas_9377.csv \
         outputs/tables/parches_topologia.csv \
         outputs/tables/metricas_fragmentacion_9377.csv \
         outputs/tables/era5_anomalias_mensuales.csv \
         outputs/tables/correlacion_clima_ndvi.csv \
         outputs/tables/series_temporales_stars.csv \
         outputs/tables/validacion_multilingual.csv \
         docs/informe_final.qmd docs/informe_final.html docs/informe_final.pdf \
         docs/INSTRUCCIONES_EJECUCION.md
git commit -m "v6: AOI acotado SFF+VPI, EPSG:9377, DE-9IM, ERA5-Land, cubo stars"
git tag v1.0-curso
git push origin main --tags
```

---

## Resumen de dependencias

| Paquete | Lenguaje | Para qué |
|---------|----------|----------|
| `cdsapi`, `netCDF4`, `xarray` | Python | Cap. 20 — ERA5-Land |
| `stars`, `dplyr`, `tidyr`, `stringr` | R | Cap. 21 — cubo desde TIFs |
| `geopandas`, `shapely` | Python | DE-9IM y áreas en EPSG:9377 |
| `rasterio` | Python | Reproyección y lectura perezosa |
| `samgeo` (vit_b) | Python | Segmentación |
| `bfast`, `terra` | R | Detección de quiebres |
| `GeoJSON.jl`, `DataFrames.jl` | Julia | Fragmentación |
