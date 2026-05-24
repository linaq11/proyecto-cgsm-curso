# Pipeline multilenguaje (Python, R, Julia) para el monitoreo de manglar en la CGSM (2013–2025)

![License](https://img.shields.io/badge/License-MIT-black)
![Stack](https://img.shields.io/badge/Stack-Python%20%C2%B7%20R%20%C2%B7%20Julia-blue)
[![Dashboard en vivo](https://img.shields.io/badge/Dashboard-en%20vivo-success?logo=github)](https://linaq11.github.io/proyecto-cgsm-curso/dashboard.html)
[![Informe PDF](https://img.shields.io/badge/Descargar-Informe%20PDF-red)](https://github.com/linaq11/proyecto-cgsm-curso/raw/main/docs/informe_final.pdf)
[![Artículo journal](https://img.shields.io/badge/Art%C3%ADculo-PDF-orange)](https://github.com/linaq11/proyecto-cgsm-curso/raw/main/docs/articulo_cgsm_journal.pdf)

> 🌿 **Dashboard interactivo**: <https://linaq11.github.io/proyecto-cgsm-curso/dashboard.html>
>
> 🛰 **Datos NASA y observación terrestre**: Landsat 8/9 (NASA-USGS), SRTM v3 (NASA), índices ENSO ONI/SOI (NOAA CPC), inventario histórico Global Flood Database (Dartmouth, deriva de MODIS NASA), segmentación con [SamGeo](https://github.com/opengeos/segment-geospatial) (Prof. Qiusheng Wu). Tematicamente alineado con la línea [Flood Early Warning](https://nasalifelines.org/hfs-data-series/flood-early-warning-2/) de **NASA Lifelines**.

Monitoreo espaciotemporal de la cobertura, fragmentación y vigor del manglar de la Ciénaga Grande de Santa Marta entre 2013 y 2025, mediante un pipeline multilenguaje (Python, R, Julia) que integra series ópticas Landsat 8 + Sentinel-2, radar Sentinel-1 SAR y forzantes climáticos (ENSO, IDEAM, ERA5-Land, CHIRPS); detección de quiebres bfast; segmentación con SamGeo y clasificación Random Forest (F1 = 0,83); y validación contra cartografía colombiana INVEMAR 1:25.000 y global ESA WorldCover v200.

**Curso:** Programación en SIG, Maestría en Geomática, Universidad Nacional de Colombia &nbsp;&nbsp; **Autora:** Lina María Quintero Fonseca &nbsp;&nbsp; **Docente:** Alexys H. Rodríguez-Avellaneda Ph.D. &nbsp;&nbsp; **Fecha de entrega:** 20 de mayo de 2026

---

## Resumen del trabajo

La Ciénaga Grande de Santa Marta —CGSM— es el sistema lagunar costero más extenso de Colombia y un humedal Ramsar reconocido por su valor ecológico. Desde la década de los noventa el manglar ha experimentado ciclos de degradación y recuperación asociados al colapso hidrológico por la carretera Ciénaga–Barranquilla, a la hipersalinización y a la intensificación de los eventos ENSO. El presente proyecto desarrolla una pipeline multilenguaje que integra Python, R y Julia para caracterizar la dinámica espaciotemporal del manglar sobre el AOI acotado oficial (835 km² del SFF CGSM + Vía Parque Isla de Salamanca) entre 2013 y 2025, articulando los siguientes componentes:

**Fase 1 — Datacube multitemporal (Python + geemap).** Construcción de un datacube NetCDF CF-1.8 sobre EPSG:9377 a partir de 789 imágenes Sentinel-2 SR Harmonized (2018–2025) y 345 registros Landsat 8/9 (2013–2017), con composites trimestrales de NDVI, NDWI y CMRI.

**Fase 2 — Series temporales y detección de cambios (Python + R).** Cálculo de z-scores y anomalías sobre las 8 estaciones de muestreo INVEMAR, complementado con detección de quiebres estructurales mediante bfast en R (`h=0.10`).

**Fase 3 — Segmentación automática (Python + SamGeo).** Segmentación promptable de los composites RGB de tres periodos de referencia (degradación 2020, recuperación 2022, actual 2024–2025) mediante el modelo Segment Anything Model con backbone vit_b.

**Fase 4 — Métricas de fragmentación (Julia).** Cómputo de NP, PD, MPA, MSI y NND sobre los parches segmentados en EPSG:9377, con descomposición de MultiPolygons y filtrado por rango 1–5.000 ha.

**Fase 5 — Forzamiento climático y validación cruzada.** Acoplamiento con ERA5-Land, CHIRPS, índices ENSO (ONI, SOI) y caudal IDEAM-DHIME del río Magdalena en El Banco y Aracataca; validación doble contra INVEMAR 1:25.000 y ESA WorldCover v200.

## Productos

- **Dashboard ejecutivo** (`docs/dashboard.html`) con 5 pestañas (Resumen, Cobertura, Clima e hidrología, Validación multilenguaje, Acerca de), 18 KPI, 14 figuras, 6 tablas, glosario técnico y mapa folium con 17 capas temáticas y slider temporal NDVI 2018–2025
- **Informe final** en PDF y HTML (~46 páginas, 19 referencias APA)
- **Artículo journal** en PDF y HTML (versión condensada para publicación)
- **3 datacubes NetCDF CF-1.8** (períodos 40 MB, trimestral 275 MB, anual Landsat 119 MB)
- **35 figuras PNG** (mapas, series temporales, correlaciones, validación)
- **47 tablas CSV** con resultados numéricos completos
- **29 notebooks numerados y reproducibles** dentro de contenedor Docker `sig_unal v1.11`

### Nota sobre el mapa interactivo

El mapa folium embebido en el dashboard sirve las capas NDVI raster como tiles de Google Earth Engine (`mapId`). **Estos tokens tienen vigencia limitada (algunas horas)**; cuando expiran, el slider funciona pero las capas raster no se renderizan. Para regenerarlos:

```bash
python src/python/make_dashboard_html.py
cp outputs/maps/dashboard_CGSM_final.html docs/outputs/maps/
git add docs/outputs/maps/dashboard_CGSM_final.html && git commit -m "Refresh GEE mapIds" && git push
```

Requiere autenticación activa con Google Earth Engine.

## Reproducibilidad

El proyecto se ejecuta dentro del contenedor Docker `sig_unal v1.11` que integra Python 3.12, R 4.3.3, Julia 1.11.3 y Quarto 1.4. Las instrucciones detalladas de instalación, autenticación con Google Earth Engine y dependencias adicionales están en el **Anexo A** del informe final. Los archivos de configuración del entorno se encuentran en `environment.yml`.

```bash
# Clonar el repositorio
git clone https://github.com/linaq11/proyecto-cgsm-curso
cd proyecto-cgsm-curso

# Levantar el contenedor (requiere Docker Desktop)
docker run -p 8889:8888 -p 8788:8787 \
  -v $(pwd):/home/rstudio/work/proyecto-cgsm \
  image_sig_unal:v1.11_produccion_final

# Acceder a Jupyter en http://localhost:8889
# Acceder a RStudio en http://localhost:8788
```

## Estructura del repositorio

```
proyecto-cgsm-curso/
├── data/                Datos crudos (AOI, admin, INVEMAR) y procesados (cubos, RGB)
├── docs/                Informe Quarto + dashboard ejecutivo servido por GitHub Pages
│   ├── dashboard.html               Dashboard principal (open-design, self-contained)
│   ├── informe_final.{pdf,html,qmd} Informe técnico completo
│   ├── articulo_cgsm_journal.*      Artículo journal condensado
│   └── outputs/                     Figuras y mapa copiados para Pages
├── notebooks/           29 notebooks numerados (Python + R) en orden de ejecución
├── outputs/             Figuras PNG, tablas CSV, mapas HTML, métricas
└── src/
    ├── python/          Módulos auxiliares + scripts de generación
    ├── R/               Scripts bfast y cubo stars
    └── julia/           Métricas de fragmentación
```

## Citas y datos abiertos

Los datos satelitales provienen de Google Earth Engine (Sentinel-2, Landsat 8/9, Sentinel-1 SAR, JRC GSW, SRTM, GFD). Los datos de campo provienen del INVEMAR vía GBIF ([DOI: 10.15472/0fqdp4](https://doi.org/10.15472/0fqdp4)). Los forzantes climáticos provienen de NOAA-CPC (ENSO), IDEAM-DHIME (caudal) y ECMWF ERA5-Land/CHIRPS (clima local). La cartografía de referencia es INVEMAR 1:25.000 y ESA WorldCover v200.

## Licencia

MIT — uso libre con atribución. Ver archivo `LICENSE`.
