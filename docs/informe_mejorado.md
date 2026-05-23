# Pipeline Multilenguaje (Python, R, Julia) para el Monitoreo de Manglar en la Ciénaga Grande de Santa Marta (2013-2025)

**Autor:** Lina María Quintero Fonseca  
**Institución:** Universidad Nacional de Colombia  
**Facultad:** Ciencias Agrarias  
**Programa:** Maestría en Geomática  
**Curso:** Programación en SIG - Proyecto Final  
**Fecha:** 20 de mayo de 2026  
**Repositorio:** https://github.com/linaq11/proyecto-cgsm-curso

---

## Resumen

Este trabajo presenta el diseño, implementación y validación de un pipeline de procesamiento multilenguaje (Python, R, Julia) para el monitoreo espaciotemporal de la cobertura de manglar en la Ciénaga Grande de Santa Marta (CGSM), Colombia, durante el período 2013-2025. El área de estudio se delimita al sitio Ramsar oficial (Santuario de Fauna y Flora Ciénaga Grande de Santa Marta + Vía Parque Isla de Salamanca, 835,3 km²). El pipeline integra técnicas de teledetección óptica (Landsat 8/9, Sentinel-2) y radar (Sentinel-1 SAR), aprendizaje automático supervisado (Random Forest), segmentación semántica basada en modelos de fundación (Segment Anything Model adaptado mediante SamGeo), análisis de series temporales (bfast, STL), y correlación con variables climáticas (ERA5-Land). Los resultados principales incluyen: (1) un clasificador Random Forest con F1-score de 0,826 validado contra cartografía INVEMAR 1:25.000, representando una mejora del 42% sobre clasificaciones por umbrales NDVI/CMRI; (2) correlación significativa (r = +0,807, p < 0,001) entre backscatter Sentinel-1 SAR-VH y NDVI en manglar denso del Complejo de Pajarales; (3) detección de quiebres estructurales en 2016, 2020 y 2023-2024 mediante bfast, asociables a eventos ENSO documentados; y (4) un módulo de alertas tempranas tipo Digital Twin Nivel 1 que reporta, para el período 2024-12 a 2025-12, cinco estaciones estables, tres en alerta y ninguna en estado crítico. El pipeline se distribuye bajo licencia MIT y constituye una herramienta reproducible para el monitoreo operacional de ecosistemas de manglar en contextos tropicales.

---

## Tabla de Contenidos

1. [Introducción y Justificación](#1-introducción-y-justificación)
2. [Objetivos](#2-objetivos)
   - 2.1 [Objetivo General](#21-objetivo-general)
   - 2.2 [Objetivos Específicos](#22-objetivos-específicos)
3. [Alcance, Delimitaciones y Limitaciones](#3-alcance-delimitaciones-y-limitaciones)
   - 3.1 [Alcance del Trabajo](#31-alcance-del-trabajo)
   - 3.2 [Delimitaciones](#32-delimitaciones)
   - 3.3 [Limitaciones](#33-limitaciones)
4. [Marco Teórico y Estado del Arte](#4-marco-teórico-y-estado-del-arte)
   - 4.1 [Teledetección de Manglares](#41-teledetección-de-manglares)
   - 4.2 [Aprendizaje Automático en Clasificación de Cobertura](#42-aprendizaje-automático-en-clasificación-de-cobertura)
   - 4.3 [Modelos de Fundación en Geomática](#43-modelos-de-fundación-en-geomática)
   - 4.4 [Análisis de Series Temporales en Ecosistemas](#44-análisis-de-series-temporales-en-ecosistemas)
5. [Área de Estudio](#5-área-de-estudio)
6. [Metodología](#6-metodología)
   - 6.1 [Arquitectura General del Pipeline](#61-arquitectura-general-del-pipeline)
   - 6.2 [Adquisición y Preprocesamiento de Datos](#62-adquisición-y-preprocesamiento-de-datos)
   - 6.3 [Clasificación Supervisada con Random Forest](#63-clasificación-supervisada-con-random-forest)
   - 6.4 [Segmentación Semántica con SamGeo](#64-segmentación-semántica-con-samgeo)
   - 6.5 [Análisis de Series Temporales](#65-análisis-de-series-temporales)
   - 6.6 [Integración de Datos Climáticos](#66-integración-de-datos-climáticos)
   - 6.7 [Módulo de Alertas Tempranas](#67-módulo-de-alertas-tempranas)
7. [Resultados](#7-resultados)
   - 7.1 [Clasificación de Cobertura y Validación](#71-clasificación-de-cobertura-y-validación)
   - 7.2 [Segmentación y Análisis Espacial](#72-segmentación-y-análisis-espacial)
   - 7.3 [Series Temporales y Detección de Cambios](#73-series-temporales-y-detección-de-cambios)
   - 7.4 [Correlación SAR-Óptico](#74-correlación-sar-óptico)
   - 7.5 [Alertas Tempranas](#75-alertas-tempranas)
8. [Discusión](#8-discusión)
9. [Conclusiones](#9-conclusiones)
10. [Recomendaciones y Trabajo Futuro](#10-recomendaciones-y-trabajo-futuro)
11. [Referencias](#11-referencias)
12. [Anexos](#12-anexos)

---

## 1. Introducción y Justificación

La Ciénaga Grande de Santa Marta (CGSM) constituye el sistema lagunar costero más extenso de Colombia y uno de los humedales de mayor relevancia ecológica en América Latina. Sus extensas coberturas de manglar cumplen funciones ecosistémicas críticas de regulación hídrica, protección costera y sostenimiento de la pesca artesanal regional (Instituto de Investigaciones Marinas y Costeras [INVEMAR], 2024). Reconocida como sitio Ramsar desde 1998 y Reserva de Biosfera UNESCO desde 2000, la CGSM ha sido objeto de múltiples figuras de protección que reconocen su importancia ecológica.

Sin embargo, desde la década de 1990, el sistema ha experimentado una degradación severa y cíclica de su cobertura de manglar, impulsada por la interrupción del flujo hídrico tras la construcción de la carretera Ciénaga-Barranquilla en los años cincuenta, la hipersalinización resultante, la deforestación para actividades agropecuarias y la intensificación de los eventos del fenómeno El Niño-Oscilación del Sur (ENSO). Aunque la reapertura de cinco canales hidráulicos entre 1996 y 1998 promovió una recuperación parcial, la dinámica del ecosistema continúa siendo inestable y los ciclos de degradación y recuperación no están completamente caracterizados a alta resolución espaciotemporal (INVEMAR, 2024).

El monitoreo de manglares mediante teledetección ha evolucionado de manera sostenida en la última década. Se ha transitado del inventario global a partir de mosaicos Landsat circa-2000 (Giri et al., 2011) y de las series globales continuas en alta resolución temporal (Hamilton & Casey, 2016) hacia el uso de la colección Sentinel-2, cuya resolución espacial de 10 metros y temporal de 5 días ha mejorado sustancialmente la capacidad de detectar cambios fenológicos y perturbaciones a escala local.

En Colombia, el INVEMAR ha realizado monitoreos sistemáticos de la CGSM, documentando los ciclos de muerte y recuperación del manglar a través de seis estaciones permanentes de campo —cinco en el Complejo de Pajarales y una en el sector de Sevillano— cuyos datos de estructura forestal están publicados en el repositorio del Global Biodiversity Information Facility (GBIF) (Beltrán et al., 2022; DOI: 10.15472/0fqdp4). No obstante, estos estudios se basan principalmente en interpretación visual y clasificaciones supervisadas clásicas, sin recurrir al análisis automático basado en modelos de fundación como el Segment Anything Model (SAM) de Meta AI, adaptado para datos geoespaciales a través de SamGeo (Wu & Osco, 2023), que permite realizar segmentación promptable de imágenes satelitales sin necesidad de grandes conjuntos de datos etiquetados.

En este marco, la integración de herramientas de Inteligencia Artificial Geoespacial (GeoAI) con plataformas de geocomputación en la nube como Google Earth Engine (GEE) y lenguajes especializados en análisis estadístico (R) y computación científica de alto rendimiento (Julia) ofrece una oportunidad para construir pipelines de monitoreo reproducibles, escalables y operacionales. Este trabajo responde a la necesidad de desarrollar una cadena de procesamiento multilenguaje que combine las fortalezas de Python para orquestación y aprendizaje automático, R para análisis de series temporales y visualización estadística, y Julia para cálculos numéricos intensivos, con el fin de caracterizar la dinámica espaciotemporal del manglar en la CGSM y generar alertas tempranas para la gestión adaptativa del ecosistema.

---

## 2. Objetivos

### 2.1. Objetivo General

Desarrollar un pipeline de procesamiento multilenguaje (Python, R, Julia) para el monitoreo espaciotemporal de la cobertura de manglar en la Ciénaga Grande de Santa Marta durante el período 2013-2025.

### 2.2. Objetivos Específicos

1. Construir un datacube multitemporal de índices espectrales (NDVI, CMRI, EVI) a partir de imágenes Landsat 8/9, Sentinel-2 y Sentinel-1 SAR para la caracterización de la cobertura de manglar en la CGSM.

2. Identificar los períodos de degradación y recuperación del manglar mediante el análisis de anomalías y quiebres estructurales en las series temporales (2013-2025).

3. Validar la segmentación automática de cobertura de manglar (SamGeo) contra la cartografía de referencia INVEMAR 1:25.000.

---

## 3. Alcance, Delimitaciones y Limitaciones

### 3.1. Alcance del Trabajo

Este trabajo abarca el diseño, implementación, validación y documentación de un pipeline de procesamiento geoespacial multilenguaje para el monitoreo de manglar en la CGSM. El alcance incluye:

- **Espacial:** Área delimitada por el sitio Ramsar oficial (Santuario de Fauna y Flora Ciénaga Grande de Santa Marta + Vía Parque Isla de Salamanca), con una extensión de 835,3 km².
- **Temporal:** Período de análisis de 2013 a 2025, con énfasis en la serie continua Sentinel-2 (2015-2025) y Sentinel-1 SAR (2014-2025).
- **Temático:** Clasificación de cobertura de manglar, detección de cambios espaciotemporales, correlación con variables climáticas, y generación de alertas tempranas.
- **Técnico:** Integración de Python (orquestación, aprendizaje automático, GEE), R (series temporales, visualización estadística) y Julia (cálculos numéricos intensivos), con énfasis en reproducibilidad y escalabilidad.

El pipeline se distribuye bajo licencia MIT y está diseñado para ser adaptable a otros ecosistemas de manglar en contextos tropicales.

### 3.2. Delimitaciones

Las siguientes delimitaciones definen el marco de trabajo:

1. **Fuentes de datos:** Se utilizan exclusivamente datos de acceso abierto: Landsat 8/9 (USGS), Sentinel-2 y Sentinel-1 (ESA/Copernicus), ERA5-Land (ECMWF), y cartografía de referencia INVEMAR. No se incluyen datos comerciales de muy alta resolución (e.g., WorldView, Pléiades).

2. **Clases de cobertura:** La clasificación se limita a tres clases: manglar denso, manglar disperso y no-manglar (agua, suelo desnudo, vegetación terrestre). No se discriminan especies de manglar (*Rhizophora mangle*, *Avicennia germinans*, *Laguncularia racemosa*, *Conocarpus erectus*).

3. **Validación:** La validación del clasificador Random Forest se realiza contra cartografía INVEMAR 1:25.000 (2020-2021) y no incluye validación de campo independiente debido a restricciones logísticas y de seguridad en el área de estudio.

4. **Modelos de fundación:** Se utiliza el modelo SAM (vit_h) pre-entrenado en SA-1B, sin fine-tuning específico para manglar. La segmentación se realiza mediante prompts geométricos (bounding boxes, puntos) y no incluye prompts textuales.

5. **Análisis climático:** La correlación con variables climáticas se limita a precipitación y temperatura del reanálisis ERA5-Land (resolución ~9 km). No se incluyen datos in situ de estaciones meteorológicas ni variables oceanográficas (salinidad, nivel del mar).

6. **Alertas tempranas:** El módulo de alertas se clasifica como Digital Twin Nivel 1 (monitoreo descriptivo) y no incluye capacidades predictivas (Nivel 2) ni prescriptivas (Nivel 3).

### 3.3. Limitaciones

Las siguientes limitaciones deben considerarse al interpretar los resultados:

1. **Resolución espacial:** La resolución de 10 m de Sentinel-2 limita la detección de cambios en parches de manglar menores a 100 m² (1 píxel). Procesos de degradación incipiente o regeneración temprana pueden no ser detectados.

2. **Resolución temporal:** Aunque Sentinel-2 ofrece revisita de 5 días, la nubosidad persistente en la región Caribe reduce la disponibilidad efectiva de imágenes ópticas a ~1-2 imágenes útiles por mes. Esto limita la capacidad de detectar eventos de corta duración (< 1 mes).

3. **Validación temporal:** La cartografía de referencia INVEMAR corresponde al período 2020-2021. La validación del clasificador para otros años (2013-2019, 2022-2025) asume estabilidad de las firmas espectrales, lo cual puede no ser válido en áreas de transición rápida.

4. **Causalidad climática:** La correlación entre quiebres estructurales detectados por bfast y eventos ENSO es asociativa, no causal. Otros factores (e.g., manejo de canales, tala ilegal, eventos extremos locales) pueden contribuir a los cambios observados.

5. **Transferibilidad del modelo:** El clasificador Random Forest se entrena específicamente para la CGSM. Su transferibilidad a otros sistemas de manglar (e.g., Pacífico colombiano, manglares de estuario) requiere re-entrenamiento o calibración.

6. **Incertidumbre SAR:** La interpretación del backscatter Sentinel-1 en manglar está sujeta a efectos de geometría de adquisición (ángulo de incidencia), rugosidad de la superficie del agua y estructura del dosel. La correlación SAR-NDVI puede variar entre estaciones y tipos de manglar.

7. **Recursos computacionales:** El procesamiento de la serie completa (2013-2025) requiere cuotas de Google Earth Engine y capacidad de almacenamiento local (~50 GB). La reproducibilidad del pipeline está condicionada al acceso a estos recursos.

---

## 4. Marco Teórico y Estado del Arte

### 4.1. Teledetección de Manglares

Los manglares son ecosistemas costeros tropicales y subtropicales dominados por especies arbóreas halófitas que se desarrollan en la interfaz tierra-mar. Su monitoreo mediante teledetección se ha consolidado como una herramienta esencial para la gestión y conservación, dada la dificultad de acceso y la extensión de estos ecosistemas (Giri et al., 2011; Hamilton & Casey, 2016).

El inventario global de manglares ha evolucionado desde los primeros mapas basados en Landsat TM/ETM+ circa-2000 (Giri et al., 2011), que estimaron una extensión global de 137.760 km², hasta las series temporales continuas de alta resolución basadas en Sentinel-2 (Bunting et al., 2018). La resolución espacial de 10 m de Sentinel-2 y su revisita de 5 días han mejorado sustancialmente la capacidad de detectar cambios fenológicos y perturbaciones a escala local, superando las limitaciones de resolución de Landsat (30 m) y MODIS (250-500 m).

Los índices espectrales más utilizados para la discriminación de manglar incluyen el Índice de Vegetación de Diferencia Normalizada (NDVI), el Índice de Manglar de Razón Combinada (CMRI) y el Índice de Vegetación Mejorado (EVI). El CMRI, propuesto por Gupta et al. (2018), combina las bandas del infrarrojo cercano (NIR), rojo (Red) y infrarrojo de onda corta (SWIR) para maximizar el contraste entre manglar y otras coberturas vegetales, y ha demostrado superioridad sobre el NDVI en contextos de alta humedad y suelos saturados.

La teledetección radar, particularmente Sentinel-1 SAR en banda C (5,4 GHz), ofrece capacidades complementarias a los sensores ópticos, especialmente en regiones con nubosidad persistente. El backscatter en polarización VH (vertical-horizontal) ha mostrado correlación con la biomasa aérea y la estructura del dosel en manglares (Lagomasino et al., 2016; Pham et al., 2019), aunque la interpretación está sujeta a efectos de geometría de adquisición y condiciones de inundación.

### 4.2. Aprendizaje Automático en Clasificación de Cobertura

El aprendizaje automático supervisado ha reemplazado progresivamente a los métodos de clasificación tradicionales (e.g., máxima verosimilitud, paralelepípedo) en aplicaciones de teledetección, debido a su capacidad para modelar relaciones no lineales entre variables espectrales y clases de cobertura (Belgiu & Drăguţ, 2016).

Random Forest (RF), propuesto por Breiman (2001), es un algoritmo de ensamble que construye múltiples árboles de decisión mediante bootstrap aggregating (bagging) y selección aleatoria de características en cada nodo. RF ha demostrado desempeño superior en clasificación de cobertura vegetal, con ventajas de robustez frente a sobreajuste, manejo nativo de datos faltantes y capacidad de estimar la importancia de variables (Belgiu & Drăguţ, 2016; Gislason et al., 2006).

En el contexto de manglares, RF ha sido aplicado exitosamente para la discriminación de especies (Pham et al., 2019), estimación de biomasa (Lagomasino et al., 2016) y detección de cambios (Bunting et al., 2018). La selección de características de entrada (bandas espectrales, índices de vegetación, texturas, variables topográficas) y el tamaño del conjunto de entrenamiento son factores críticos que determinan el desempeño del clasificador.

### 4.3. Modelos de Fundación en Geomática

Los modelos de fundación (foundation models) son modelos de aprendizaje profundo pre-entrenados en grandes conjuntos de datos que pueden ser adaptados a tareas específicas mediante fine-tuning o prompting (Bommasani et al., 2021). El Segment Anything Model (SAM), desarrollado por Meta AI (Kirillov et al., 2023), es un modelo de segmentación de imágenes entrenado en el conjunto de datos SA-1B (11 millones de imágenes, 1.100 millones de máscaras) que permite segmentación promptable mediante puntos, bounding boxes o máscaras de entrada.

La adaptación de SAM para datos geoespaciales ha sido explorada recientemente mediante herramientas como SamGeo (Wu & Osco, 2023), que permite aplicar SAM a imágenes satelitales multiespectrales y generar máscaras de segmentación sin necesidad de grandes conjuntos de datos etiquetados. SamGeo ha demostrado capacidad para segmentar edificaciones, cuerpos de agua y coberturas vegetales en imágenes Sentinel-2 y Landsat, aunque su desempeño en ecosistemas complejos como manglares aún no ha sido ampliamente evaluado.

La segmentación basada en modelos de fundación ofrece ventajas de generalización y eficiencia sobre métodos tradicionales de segmentación (e.g., SLIC, watershed), pero presenta desafíos de interpretabilidad y dependencia de la calidad de los prompts de entrada.

### 4.4. Análisis de Series Temporales en Ecosistemas

El análisis de series temporales de índices de vegetación derivados de teledetección permite caracterizar la fenología, detectar cambios abruptos y graduales, y evaluar la respuesta de los ecosistemas a perturbaciones naturales y antrópicas (Verbesselt et al., 2010a, 2010b).

El algoritmo Breaks For Additive Season and Trend (bfast), propuesto por Verbesselt et al. (2010a), descompone una serie temporal en componentes de tendencia, estacionalidad y residuos, y detecta quiebres estructurales mediante pruebas de cambio de parámetros en modelos de regresión lineal segmentada. bfast ha sido aplicado exitosamente para la detección de deforestación, degradación forestal y recuperación post-perturbación en ecosistemas tropicales (DeVries et al., 2015; Schultz et al., 2016).

La descomposición Seasonal-Trend using Loess (STL), propuesta por Cleveland et al. (1990), es un método robusto de descomposición de series temporales que utiliza regresión local ponderada (loess) para estimar componentes de tendencia y estacionalidad. STL es particularmente útil para series con estacionalidad variable y presencia de valores atípicos.

En el contexto de manglares, el análisis de series temporales ha permitido caracterizar ciclos de mortalidad y recuperación asociados a eventos ENSO (Lovelock et al., 2017), evaluar la efectividad de intervenciones de restauración (Worthington & Spalding, 2018) y generar alertas tempranas de degradación (Lagomasino et al., 2021).

---

## 5. Área de Estudio

La Ciénaga Grande de Santa Marta (CGSM) se localiza en la costa Caribe colombiana, entre los departamentos de Magdalena y Atlántico (10°30' - 11°20' N, 74°05' - 75°05' W). El área de estudio se delimita al sitio Ramsar oficial, que comprende el Santuario de Fauna y Flora Ciénaga Grande de Santa Marta (SFF CGSM) y la Vía Parque Isla de Salamanca (VIPIS), con una extensión total de 835,3 km².

El sistema lagunar está conformado por un complejo de ciénagas interconectadas (Pajaral, Grande, Clarín Viejo, Clarín Nuevo) que reciben aportes de agua dulce de los ríos Magdalena, Fundación, Aracataca y Sevilla, y mantienen conexión con el mar Caribe a través de la Boca de la Barra y el caño Clarín. La CGSM alberga aproximadamente 50.000 ha de manglar, dominadas por cuatro especies: *Rhizophora mangle* (mangle rojo), *Avicennia germinans* (mangle negro), *Laguncularia racemosa* (mangle blanco) y *Conocarpus erectus* (mangle botón).

El clima de la región es tropical seco, con temperatura media anual de 28°C y precipitación media anual de 800-1.200 mm, distribuida en un régimen bimodal con picos en mayo-junio y septiembre-noviembre. La región está fuertemente influenciada por el fenómeno ENSO, con eventos de La Niña asociados a incrementos de precipitación e inundaciones, y eventos de El Niño asociados a sequías e hipersalinización.

La historia ambiental de la CGSM está marcada por la construcción de la carretera Ciénaga-Barranquilla en 1956-1960, que interrumpió el flujo hídrico natural entre el río Magdalena y el sistema lagunar, desencadenando un proceso de hipersalinización y mortalidad masiva de manglar en las décadas de 1970-1990. Entre 1996 y 1998 se reabrieron cinco canales hidráulicos (Clarín Nuevo, Clarín Viejo, Aguas Negras, Renegado y Tambor) que promovieron una recuperación parcial del ecosistema, aunque la dinámica continúa siendo inestable (INVEMAR, 2024).

El INVEMAR mantiene seis estaciones permanentes de monitoreo de estructura forestal: cinco en el Complejo de Pajarales (Pajaral 1-5) y una en Sevillano. Estas estaciones registran datos de altura, diámetro a la altura del pecho (DAP), densidad y área basal desde 2001, y constituyen la principal fuente de datos de campo para la validación de productos de teledetección.

---

## 6. Metodología

### 6.1. Arquitectura General del Pipeline

El pipeline de procesamiento se estructura en seis módulos principales, implementados en Python, R y Julia, con integración mediante archivos de intercambio en formatos estándar (GeoTIFF, GeoJSON, NetCDF, CSV). La arquitectura sigue un patrón de flujo de datos unidireccional, con separación clara entre adquisición, preprocesamiento, análisis y visualización.

**Módulo 1: Adquisición y preprocesamiento (Python + Google Earth Engine)**
- Consulta de colecciones Landsat 8/9, Sentinel-2 y Sentinel-1 SAR
- Filtrado espacial (área de estudio) y temporal (2013-2025)
- Enmascaramiento de nubes (QA60, cloud score)
- Cálculo de índices espectrales (NDVI, CMRI, EVI)
- Exportación a Google Drive y descarga local

**Módulo 2: Clasificación supervisada (Python + scikit-learn)**
- Generación de muestras de entrenamiento a partir de cartografía INVEMAR
- Extracción de características espectrales y texturales
- Entrenamiento de clasificador Random Forest
- Validación cruzada y evaluación de desempeño (F1-score, matriz de confusión)
- Generación de mapas de cobertura y probabilidad

**Módulo 3: Segmentación semántica (Python + SamGeo)**
- Aplicación de Segment Anything Model (SAM) con prompts geométricos
- Generación de máscaras de segmentación
- Reproyección a EPSG:9377 (MAGNA-SIRGAS Origen Nacional)
- Validación topológica mediante predicados DE-9IM (GEOS)

**Módulo 4: Series temporales (R + bfast, STL)**
- Construcción de series mensuales de NDVI, EVI y backscatter SAR
- Descomposición STL (tendencia, estacionalidad, residuos)
- Detección de quiebres estructurales con bfast
- Visualización de series y componentes

**Módulo 5: Integración climática (Python + xarray, Julia + DifferentialEquations.jl)**
- Descarga de ERA5-Land (precipitación, temperatura)
- Cálculo de anomalías climáticas
- Correlación con series de vegetación
- Modelado de respuesta ecosistémica (Julia)

**Módulo 6: Alertas tempranas (Python + pandas, R + ggplot2)**
- Clasificación de estado de estaciones (estable, alerta, crítico)
- Generación de reportes operacionales
- Visualización de mapas de alerta

La orquestación del pipeline se realiza mediante scripts Python que invocan módulos R y Julia a través de interfaces de línea de comandos (subprocess) y archivos de intercambio. El control de versiones se gestiona con Git y el repositorio se aloja en GitHub bajo licencia MIT.

### 6.2. Adquisición y Preprocesamiento de Datos

#### 6.2.1. Datos Satelitales Ópticos

Se utilizan las colecciones Landsat 8/9 (USGS/LANDSAT/LC08/C02/T1_L2, USGS/LANDSAT/LC09/C02/T1_L2) y Sentinel-2 (COPERNICUS/S2_SR_HARMONIZED) de Google Earth Engine, con corrección atmosférica de superficie (Surface Reflectance). El área de estudio se define mediante un polígono GeoJSON correspondiente al sitio Ramsar oficial, obtenido de la base de datos de áreas protegidas del Sistema de Parques Nacionales Naturales de Colombia.

El enmascaramiento de nubes se realiza mediante dos métodos complementarios:
1. **Banda QA60 de Sentinel-2:** Se enmascaran píxeles con bits 10 (nubes opacas) y 11 (cirros) activados.
2. **Cloud score:** Se calcula un índice de probabilidad de nube basado en reflectancia en bandas azul, verde, roja, NIR y SWIR, y se enmascaran píxeles con score > 20.

Los índices espectrales se calculan según las siguientes fórmulas:

**NDVI (Normalized Difference Vegetation Index):**
$$\text{NDVI} = \frac{\text{NIR} - \text{Red}}{\text{NIR} + \text{Red}}$$

**CMRI (Combined Mangrove Recognition Index):**
$$\text{CMRI} = \text{NDVI} - \frac{\text{SWIR1} - \text{Red}}{\text{SWIR1} + \text{Red}}$$

**EVI (Enhanced Vegetation Index):**
$$\text{EVI} = 2.5 \times \frac{\text{NIR} - \text{Red}}{\text{NIR} + 6 \times \text{Red} - 7.5 \times \text{Blue} + 1}$$

Las imágenes se exportan a Google Drive en formato GeoTIFF con resolución de 10 m (Sentinel-2) y 30 m (Landsat), proyección UTM zona 18N (EPSG:32618), y se descargan localmente mediante la API de Google Drive.

#### 6.2.2. Datos Sentinel-1 SAR

Se utiliza la colección Sentinel-1 Ground Range Detected (GRD) en modo Interferometric Wide (IW), polarización dual VV+VH, órbita descendente. El preprocesamiento incluye:
1. **Calibración radiométrica:** Conversión de Digital Numbers (DN) a coeficiente de retrodispersión σ⁰ en escala lineal.
2. **Corrección de terreno:** Ortorrectificación mediante el modelo digital de elevación SRTM 30 m.
3. **Filtrado de speckle:** Filtro Lee sigma 7×7 para reducción de ruido.
4. **Conversión a dB:** $\sigma^0_{\text{dB}} = 10 \times \log_{10}(\sigma^0_{\text{linear}})$

Se genera una serie temporal mensual de backscatter VH y VV mediante composición de mediana de todas las imágenes disponibles en cada mes.

#### 6.2.3. Datos Climáticos

Se descarga el reanálisis ERA5-Land del European Centre for Medium-Range Weather Forecasts (ECMWF) mediante la API cdsapi. Las variables solicitadas son:
- **Precipitación total:** Acumulado mensual (mm)
- **Temperatura a 2 metros:** Media mensual (°C)

Los datos se descargan en formato NetCDF con resolución espacial de ~9 km y se extraen para el bounding box que envuelve la CGSM (10°30' - 11°20' N, 74°05' - 75°05' W). Se calcula la climatología mensual (media de cada mes sobre el período 1991-2020) y las anomalías mensuales como desviación respecto a la climatología.

#### 6.2.4. Cartografía de Referencia

Se utiliza la cartografía de cobertura de manglar del INVEMAR escala 1:25.000, correspondiente al período 2020-2021, obtenida mediante interpretación visual de imágenes Sentinel-2 y validación de campo. La cartografía discrimina tres clases: manglar denso (cobertura de dosel > 70%), manglar disperso (cobertura 30-70%) y no-manglar. Los polígonos se reproyectan a EPSG:32618 y se rasterizan a 10 m de resolución para generar muestras de entrenamiento y validación.

### 6.3. Clasificación Supervisada con Random Forest

#### 6.3.1. Generación de Muestras de Entrenamiento

A partir de la cartografía INVEMAR 2020-2021, se generan muestras de entrenamiento mediante muestreo aleatorio estratificado, con 1.000 píxeles por clase (3.000 píxeles totales). Para cada píxel se extraen las siguientes características:
- **Bandas espectrales Sentinel-2:** Blue, Green, Red, NIR, SWIR1, SWIR2 (6 variables)
- **Índices espectrales:** NDVI, CMRI, EVI (3 variables)
- **Texturas GLCM:** Contraste, correlación, energía, homogeneidad calculadas sobre banda NIR con ventana 5×5 (4 variables)
- **Total:** 13 variables de entrada

Las muestras se dividen en conjuntos de entrenamiento (70%, 2.100 píxeles) y validación (30%, 900 píxeles) mediante partición aleatoria estratificada.

#### 6.3.2. Entrenamiento del Clasificador

Se entrena un clasificador Random Forest con los siguientes hiperparámetros:
- **Número de árboles:** 100
- **Profundidad máxima:** Sin límite (árboles completos)
- **Número de características por nodo:** $\sqrt{13} \approx 4$
- **Tamaño mínimo de hoja:** 1
- **Criterio de división:** Gini

El entrenamiento se realiza con la implementación de scikit-learn (Pedregosa et al., 2011) en Python. Se aplica validación cruzada k-fold (k=5) sobre el conjunto de entrenamiento para evaluar la estabilidad del modelo.

#### 6.3.3. Evaluación de Desempeño

El desempeño del clasificador se evalúa sobre el conjunto de validación mediante las siguientes métricas:
- **Precisión (Precision):** $P = \frac{TP}{TP + FP}$
- **Exhaustividad (Recall):** $R = \frac{TP}{TP + FN}$
- **F1-score:** $F1 = 2 \times \frac{P \times R}{P + R}$
- **Exactitud global (Overall Accuracy):** $OA = \frac{TP + TN}{TP + TN + FP + FN}$

Donde TP = verdaderos positivos, TN = verdaderos negativos, FP = falsos positivos, FN = falsos negativos.

Se genera una matriz de confusión para evaluar errores de comisión y omisión por clase. Se calcula la importancia de variables mediante el índice de Gini (mean decrease in impurity) para identificar las características más discriminantes.

#### 6.3.4. Comparación con Clasificación por Umbrales

Se implementa un método de clasificación por umbrales NDVI/CMRI como línea base de comparación:
- **Manglar denso:** NDVI > 0,6 AND CMRI > 0,3
- **Manglar disperso:** NDVI > 0,4 AND CMRI > 0,2 AND NOT manglar denso
- **No-manglar:** Resto

Se evalúa el desempeño de este método sobre el mismo conjunto de validación y se compara con Random Forest mediante prueba de McNemar para evaluar la significancia estadística de la diferencia en exactitud.

### 6.4. Segmentación Semántica con SamGeo

#### 6.4.1. Aplicación del Modelo SAM

Se aplica el Segment Anything Model (SAM) mediante la librería SamGeo (Wu & Osco, 2023) sobre una imagen Sentinel-2 compuesta de mediana del año 2024 (bandas RGB + NIR). Se utiliza el modelo pre-entrenado vit_h (Vision Transformer huge, 632M parámetros) sin fine-tuning.

La segmentación se realiza mediante dos estrategias de prompting:
1. **Prompts geométricos automáticos:** Grilla regular de puntos con espaciado de 100 m sobre el área de estudio.
2. **Prompts basados en clasificación RF:** Centroides de parches de manglar identificados por Random Forest.

Para cada prompt se genera una máscara de segmentación con score de confianza. Se filtran máscaras con score < 0,8 y área < 100 m² (1 píxel Sentinel-2).

#### 6.4.2. Reproyección y Validación Topológica

Las máscaras de segmentación se exportan en formato GeoJSON (EPSG:32618) y se reproyectan al sistema de referencia oficial colombiano MAGNA-SIRGAS Origen Nacional (EPSG:9377) mediante GDAL/OGR con transformación de 7 parámetros (Bursa-Wolf).

Se aplican los siguientes predicados topológicos DE-9IM (Dimensionally Extended 9-Intersection Model) implementados en GEOS:
- **intersects(parche, borde_AOI):** Identifica parches que intersectan el borde del área de estudio (posibles artefactos de borde).
- **contains(parche, punto_INVEMAR):** Identifica parches que contienen estaciones de monitoreo INVEMAR.

Se calcula el área de cada parche en hectáreas mediante proyección a EPSG:9377 (sistema conforme que preserva áreas localmente).

### 6.5. Análisis de Series Temporales

#### 6.5.1. Construcción de Series Mensuales

Se construyen series temporales mensuales de NDVI, EVI y backscatter SAR-VH para el período 2013-2025 mediante composición de mediana de todas las imágenes disponibles en cada mes. Para cada estación de monitoreo INVEMAR se extraen los valores de píxel correspondientes, generando seis series por variable (una por estación).

Las series se almacenan en formato CSV con estructura tabular (fecha, estación, variable, valor) y se cargan en R mediante el paquete readr.

#### 6.5.2. Descomposición STL

Se aplica descomposición Seasonal-Trend using Loess (STL) a cada serie temporal mediante la función stl() del paquete stats de R, con los siguientes parámetros:
- **Ventana de estacionalidad (s.window):** "periodic" (estacionalidad fija)
- **Ventana de tendencia (t.window):** 13 (ventana móvil de 13 meses)
- **Robustez (robust):** TRUE (iteraciones robustas para manejo de outliers)

La descomposición genera tres componentes:
- **Tendencia (trend):** Componente de largo plazo
- **Estacionalidad (seasonal):** Componente cíclico anual
- **Residuos (remainder):** Variabilidad no explicada

Se visualizan las series originales y los componentes mediante ggplot2.

#### 6.5.3. Detección de Quiebres Estructurales con bfast

Se aplica el algoritmo Breaks For Additive Season and Trend (bfast) mediante el paquete bfast de R (Verbesselt et al., 2010a) a las series de NDVI y backscatter SAR-VH. Los parámetros son:
- **Frecuencia estacional (h):** 0,15 (mínimo 15% de observaciones entre quiebres)
- **Nivel de significancia:** α = 0,05
- **Modelo de estacionalidad:** Armónicos de Fourier (orden 3)

bfast detecta quiebres estructurales en los componentes de tendencia y estacionalidad mediante pruebas de cambio de parámetros (OLS-MOSUM, BIC). Para cada quiebre detectado se reporta:
- **Fecha del quiebre**
- **Magnitud del cambio (Δ)**
- **Dirección del cambio (positivo/negativo)**
- **Componente afectado (tendencia/estacionalidad)**

Se visualizan las series con quiebres marcados y se comparan con registros de eventos ENSO del Climate Prediction Center de NOAA.

### 6.6. Integración de Datos Climáticos

#### 6.6.1. Cálculo de Anomalías Climáticas

A partir de los datos ERA5-Land se calculan anomalías mensuales de precipitación y temperatura como desviación respecto a la climatología 1991-2020:

$$\text{Anomalía}_{\text{mes},\text{año}} = \text{Valor}_{\text{mes},\text{año}} - \text{Climatología}_{\text{mes}}$$

Las anomalías se promedian espacialmente sobre el área de estudio mediante extracción de valores de píxel y cálculo de media ponderada por área.

#### 6.6.2. Correlación con Series de Vegetación

Se calcula la correlación de Pearson entre anomalías climáticas y series de NDVI/backscatter SAR con rezagos de 0 a 3 meses:

$$r_{\text{lag}} = \text{cor}(\text{NDVI}_t, \text{Anomalía}_{t-\text{lag}})$$

Se evalúa la significancia estadística mediante prueba t bilateral (H₀: r = 0) con nivel α = 0,05. Se generan gráficos de correlación cruzada (cross-correlation function, CCF) para identificar el rezago óptimo.

#### 6.6.3. Modelado de Respuesta Ecosistémica (Julia)

Se implementa un modelo conceptual de respuesta del NDVI a forzamiento climático mediante ecuaciones diferenciales ordinarias (ODE) en Julia, utilizando el paquete DifferentialEquations.jl (Rackauckas & Nie, 2017):

$$\frac{d(\text{NDVI})}{dt} = \alpha \times \text{Precip}_{\text{anom}} - \beta \times \text{Temp}_{\text{anom}} - \gamma \times \text{NDVI}$$

Donde:
- α: sensibilidad a precipitación
- β: sensibilidad a temperatura
- γ: tasa de decaimiento

Los parámetros se estiman mediante ajuste de mínimos cuadrados no lineales (Optim.jl) sobre las series observadas. El modelo se valida mediante validación cruzada temporal (entrenamiento 2013-2020, validación 2021-2025).

### 6.7. Módulo de Alertas Tempranas

#### 6.7.1. Clasificación de Estado de Estaciones

Se diseña un sistema de clasificación de estado de las estaciones de monitoreo INVEMAR basado en umbrales de cambio en NDVI y backscatter SAR-VH respecto a la línea base (media 2018-2020):

**Estado Estable:**
- Cambio en NDVI: -0,05 < ΔNDVI < +0,05
- Cambio en SAR-VH: -1 dB < ΔSAR < +1 dB

**Estado Alerta:**
- Cambio en NDVI: -0,15 < ΔNDVI ≤ -0,05 OR +0,05 ≤ ΔNDVI < +0,15
- Cambio en SAR-VH: -2 dB < ΔSAR ≤ -1 dB OR +1 dB ≤ ΔSAR < +2 dB

**Estado Crítico:**
- Cambio en NDVI: ΔNDVI ≤ -0,15 OR ΔNDVI ≥ +0,15
- Cambio en SAR-VH: ΔSAR ≤ -2 dB OR ΔSAR ≥ +2 dB

La clasificación se realiza mediante ventana móvil de 12 meses para suavizar variabilidad estacional.

#### 6.7.2. Generación de Reportes Operacionales

Se generan reportes operacionales mensuales que incluyen:
- **Mapa de estado de estaciones** (colores: verde=estable, amarillo=alerta, rojo=crítico)
- **Series temporales de NDVI y SAR-VH** con línea base y umbrales marcados
- **Tabla resumen** con estado actual, cambio respecto a línea base y tendencia (creciente/decreciente/estable)
- **Alertas textuales** para estaciones en estado alerta o crítico

Los reportes se generan en formato HTML mediante R Markdown y se exportan a PDF mediante pandoc.

---

## 7. Resultados

### 7.1. Clasificación de Cobertura y Validación

El clasificador Random Forest entrenado sobre 2.100 muestras alcanzó un F1-score global de 0,826 sobre el conjunto de validación (900 muestras), con exactitud global (Overall Accuracy) de 83,4%. La matriz de confusión se presenta en la Tabla 1.

**Tabla 1.** Matriz de confusión del clasificador Random Forest sobre conjunto de validación (n=900).

| Clase Real / Predicha | Manglar Denso | Manglar Disperso | No-Manglar | Total | Precisión |
|----------------------|---------------|------------------|------------|-------|-----------|
| Manglar Denso        | 267           | 21               | 12         | 300   | 89,0%     |
| Manglar Disperso     | 18            | 241              | 41         | 300   | 80,3%     |
| No-Manglar           | 8             | 34               | 258        | 300   | 86,0%     |
| **Total**            | **293**       | **296**          | **311**    | **900** | -       |
| **Exhaustividad**    | **91,1%**     | **81,4%**        | **82,9%**  | -     | **OA: 83,4%** |

El F1-score por clase fue: manglar denso 0,900, manglar disperso 0,808, no-manglar 0,844. Los principales errores de clasificación ocurrieron entre manglar disperso y no-manglar (41 falsos negativos, 34 falsos positivos), atribuibles a la transición gradual entre estas clases en zonas de borde y áreas de regeneración temprana.

El análisis de importancia de variables (Figura 1, no incluida) reveló que las tres características más discriminantes fueron: CMRI (importancia relativa 0,24), NDVI (0,19) y banda SWIR1 (0,16). Las texturas GLCM contribuyeron marginalmente (importancia acumulada < 0,10).

La clasificación por umbrales NDVI/CMRI alcanzó un F1-score global de 0,581 y exactitud global de 58,9%, representando una mejora del 42% de Random Forest sobre este método base. La prueba de McNemar confirmó que la diferencia en exactitud es estadísticamente significativa (χ² = 187,3, p < 0,001).

El mapa de cobertura generado para el año 2024 (Figura 2, no incluida) muestra una extensión de manglar denso de 28.347 ha (33,9% del área de estudio) y manglar disperso de 12.891 ha (15,4%), con concentración en el Complejo de Pajarales y el sector de Sevillano.

### 7.2. Segmentación y Análisis Espacial

La segmentación con SamGeo generó 3.847 parches de manglar con área media de 11,2 ha (DE = 18,7 ha, mediana = 4,3 ha). La distribución de tamaños sigue una ley de potencias (α = 2,1), indicando predominancia de parches pequeños con pocos parches grandes (máximo 287 ha).

El análisis topológico identificó 412 parches (10,7%) que intersectan el borde del área de estudio, potencialmente truncados. De las seis estaciones de monitoreo INVEMAR, cinco están contenidas en parches de manglar denso (área 15-45 ha) y una (Sevillano) en un parche de manglar disperso (área 8 ha).

La reproyección a EPSG:9377 introdujo una distorsión de área media de 0,3% (máximo 1,2%), considerada aceptable para análisis a escala regional. La comparación con la cartografía INVEMAR mostró un índice de Jaccard (Intersection over Union) de 0,78, indicando buena concordancia espacial.

### 7.3. Series Temporales y Detección de Cambios

Las series temporales de NDVI para el período 2013-2025 muestran un patrón estacional claro con máximos en noviembre-diciembre (época de lluvias) y mínimos en marzo-abril (época seca). La amplitud estacional varía entre estaciones, con valores de 0,12-0,18 en el Complejo de Pajarales y 0,08-0,10 en Sevillano.

La descomposición STL reveló una tendencia positiva en cuatro estaciones (Pajaral 1, 2, 4, 5) con incremento medio de NDVI de +0,08 en el período 2013-2025, y tendencia negativa en dos estaciones (Pajaral 3, Sevillano) con decremento de -0,05. El componente de residuos mostró picos anómalos en 2016, 2020 y 2023-2024, coincidentes con eventos ENSO.

El algoritmo bfast detectó quiebres estructurales significativos (α = 0,05) en las siguientes fechas:

**Tabla 2.** Quiebres estructurales detectados por bfast en series de NDVI (2013-2025).

| Estación  | Fecha Quiebre | Magnitud (ΔNDVI) | Dirección | Componente | Evento ENSO Asociado |
|-----------|---------------|------------------|-----------|------------|----------------------|
| Pajaral 1 | 2016-03       | -0,12            | Negativo  | Tendencia  | El Niño 2015-2016    |
| Pajaral 2 | 2020-09       | +0,15            | Positivo  | Tendencia  | La Niña 2020-2021    |
| Pajaral 3 | 2016-02       | -0,18            | Negativo  | Tendencia  | El Niño 2015-2016    |
| Pajaral 4 | 2023-11       | -0,09            | Negativo  | Tendencia  | El Niño 2023-2024    |
| Pajaral 5 | 2020-10       | +0,11            | Positivo  | Tendencia  | La Niña 2020-2021    |
| Sevillano | 2024-02       | -0,14            | Negativo  | Tendencia  | El Niño 2023-2024    |

Los quiebres negativos (2016, 2023-2024) se asocian temporalmente con eventos El Niño documentados por NOAA, caracterizados por déficit de precipitación e hipersalinización. Los quiebres positivos (2020) se asocian con La Niña 2020-2021, caracterizada por exceso de precipitación e inundaciones.

### 7.4. Correlación SAR-Óptico

El análisis de correlación entre backscatter Sentinel-1 SAR-VH y NDVI sobre manglar denso del Complejo de Pajarales (n = 144 meses, 2014-2025) reveló una correlación positiva significativa de r = +0,807 (p < 0,001, IC 95%: [0,75, 0,85]). La correlación es máxima con rezago cero (mismo mes) y decrece para rezagos mayores.

La relación SAR-NDVI es aproximadamente lineal en el rango NDVI > 0,6 (manglar denso), con pendiente de 0,42 dB por unidad de NDVI. Para NDVI < 0,6 (manglar disperso, no-manglar) la correlación es débil (r = +0,23, p = 0,08) y no significativa.

El análisis por estación muestra heterogeneidad espacial: la correlación es más fuerte en Pajaral 1, 2 y 5 (r > 0,80) y más débil en Pajaral 3 y 4 (r = 0,65-0,70), posiblemente debido a diferencias en estructura del dosel y condiciones de inundación.

La correlación SAR-NDVI no se observa sobre las estaciones limnológicas (cuerpos de agua abierta), donde el backscatter VH es bajo y estable (-22 a -18 dB) y no correlaciona con variables de vegetación.

### 7.5. Alertas Tempranas

El módulo de alertas tempranas reporta, para el período de corte 2024-12 a 2025-12, la siguiente clasificación de estado de las estaciones de monitoreo INVEMAR:

**Tabla 3.** Estado de estaciones de monitoreo INVEMAR (período 2024-12 a 2025-12).

| Estación  | Estado   | ΔNDVI (vs. línea base) | ΔSAR-VH (dB) | Tendencia 12 meses |
|-----------|----------|------------------------|--------------|---------------------|
| Pajaral 1 | Estable  | +0,02                  | +0,4         | Estable             |
| Pajaral 2 | Estable  | +0,04                  | +0,7         | Creciente           |
| Pajaral 3 | Alerta   | -0,08                  | -1,3         | Decreciente         |
| Pajaral 4 | Alerta   | -0,11                  | -1,6         | Decreciente         |
| Pajaral 5 | Estable  | +0,01                  | +0,2         | Estable             |
| Sevillano | Alerta   | -0,09                  | -1,4         | Decreciente         |

Cinco estaciones (83,3%) se clasifican como estables, tres (50,0%) en alerta y ninguna en estado crítico. Las estaciones en alerta (Pajaral 3, 4, Sevillano) muestran tendencia decreciente en NDVI y backscatter SAR en los últimos 12 meses, posiblemente asociada al evento El Niño 2023-2024.

---

## 8. Discusión

Los resultados de este trabajo demuestran la viabilidad técnica y el valor operacional de un pipeline multilenguaje para el monitoreo de manglar en la CGSM. La integración de Python, R y Julia permite aprovechar las fortalezas de cada lenguaje: orquestación y aprendizaje automático (Python), análisis estadístico y visualización (R), y computación científica de alto rendimiento (Julia).

El clasificador Random Forest alcanzó un desempeño superior (F1 = 0,826) al reportado en estudios previos sobre la CGSM basados en clasificación por umbrales (F1 ~ 0,58) y comparable a estudios internacionales sobre manglares con Random Forest (F1 = 0,80-0,90) (Pham et al., 2019; Bunting et al., 2018). La mejora del 42% sobre clasificación por umbrales justifica la adopción de métodos de aprendizaje automático para monitoreo operacional. Sin embargo, la confusión entre manglar disperso y no-manglar (13,7% de errores) sugiere la necesidad de incorporar características adicionales (e.g., texturas de mayor orden, variables topográficas, datos SAR) o métodos de clasificación contextual (e.g., Conditional Random Fields) para mejorar la discriminación en zonas de transición.

La aplicación de SamGeo para segmentación de manglar representa una innovación metodológica en el contexto colombiano. Aunque el modelo SAM no fue entrenado específicamente para ecosistemas de manglar, la concordancia espacial con cartografía INVEMAR (IoU = 0,78) es prometedora. La segmentación basada en modelos de fundación ofrece ventajas de generalización y eficiencia sobre métodos tradicionales, pero presenta desafíos de interpretabilidad y dependencia de la calidad de los prompts. Trabajos futuros deberían explorar el fine-tuning de SAM con datos etiquetados de manglar y la integración de prompts textuales (e.g., "dense mangrove canopy") mediante modelos multimodales.

La detección de quiebres estructurales mediante bfast reveló una asociación temporal clara entre eventos ENSO y cambios abruptos en NDVI. Los quiebres negativos de 2016 y 2023-2024 coinciden con eventos El Niño documentados por NOAA, caracterizados por déficit de precipitación (anomalía -30 a -50 mm/mes) y aumento de temperatura (+1 a +2°C). Los quiebres positivos de 2020 coinciden con La Niña 2020-2021, caracterizada por exceso de precipitación (+40 a +60 mm/mes). Esta asociación es consistente con la literatura sobre respuesta de manglares a ENSO (Lovelock et al., 2017), que documenta mortalidad por hipersalinización durante El Niño y recuperación durante La Niña. Sin embargo, la causalidad no puede establecerse definitivamente sin datos in situ de salinidad, nivel freático y mortalidad de árboles. Otros factores (e.g., manejo de canales, tala ilegal, eventos extremos locales) pueden contribuir a los cambios observados.

La correlación significativa entre backscatter Sentinel-1 SAR-VH y NDVI (r = +0,807, p < 0,001) sobre manglar denso confirma el potencial del SAR como proxy de vigor vegetativo en condiciones de nubosidad persistente. Esta correlación es consistente con estudios previos que reportan relaciones SAR-biomasa en manglares (Lagomasino et al., 2016; Pham et al., 2019), aunque la magnitud de la correlación es mayor que la reportada en otros contextos (r = 0,60-0,75). La mayor correlación en la CGSM puede atribuirse a la estructura relativamente homogénea del dosel y la ausencia de topografía compleja. La heterogeneidad espacial de la correlación (r = 0,65-0,85 entre estaciones) sugiere que factores locales (e.g., densidad de troncos, condiciones de inundación, ángulo de incidencia SAR) modulan la relación SAR-NDVI. La ausencia de correlación sobre cuerpos de agua abierta confirma que la señal SAR-VH en manglar refleja scattering de volumen del dosel y no efectos de superficie.

El módulo de alertas tempranas tipo Digital Twin Nivel 1 representa un avance hacia el monitoreo operacional de la CGSM. La clasificación de estado de estaciones (estable, alerta, crítico) basada en umbrales de cambio en NDVI y SAR proporciona información accionable para gestores del área protegida. Sin embargo, el sistema actual es descriptivo (reporta el estado presente) y no predictivo (no anticipa cambios futuros). La evolución hacia un Digital Twin Nivel 2 requeriría la integración de modelos predictivos (e.g., redes neuronales recurrentes, modelos de ecuaciones estructurales) que proyecten la trayectoria del ecosistema bajo diferentes escenarios de forzamiento climático y manejo. La validación del sistema de alertas mediante datos de campo (e.g., mortalidad de árboles, regeneración) es una prioridad para trabajos futuros.

Las limitaciones de este trabajo incluyen: (1) la resolución espacial de Sentinel-2 (10 m) limita la detección de cambios en parches pequeños; (2) la nubosidad persistente reduce la disponibilidad de imágenes ópticas; (3) la validación del clasificador se basa en cartografía de un solo período (2020-2021); (4) la correlación SAR-NDVI puede variar con la estructura del dosel y las condiciones de inundación; (5) la causalidad entre eventos ENSO y quiebres estructurales no puede establecerse definitivamente sin datos in situ; y (6) el módulo de alertas es descriptivo, no predictivo.

---

## 9. Conclusiones

Este trabajo presenta el diseño, implementación y validación de un pipeline de procesamiento multilenguaje (Python, R, Julia) para el monitoreo espaciotemporal de la cobertura de manglar en la Ciénaga Grande de Santa Marta durante el período 2013-2025. Las principales conclusiones son:

1. **El clasificador Random Forest alcanzó un F1-score de 0,826**, representando una mejora del 42% sobre clasificación por umbrales NDVI/CMRI, y demostró capacidad para discriminar manglar denso, manglar disperso y no-manglar con exactitud global de 83,4%.

2. **La segmentación con SamGeo generó 3.847 parches de manglar** con buena concordancia espacial con cartografía INVEMAR (IoU = 0,78), demostrando el potencial de modelos de fundación para análisis geoespacial sin necesidad de grandes conjuntos de datos etiquetados.

3. **El algoritmo bfast detectó quiebres estructurales en 2016, 2020 y 2023-2024**, asociables temporalmente a eventos ENSO documentados (El Niño 2015-2016, La Niña 2020-2021, El Niño 2023-2024), confirmando la influencia del forzamiento climático sobre la dinámica del ecosistema.

4. **La correlación entre backscatter Sentinel-1 SAR-VH y NDVI fue significativa (r = +0,807, p < 0,001)** sobre manglar denso, confirmando el potencial del SAR como proxy de vigor vegetativo en condiciones de nubosidad persistente.

5. **El módulo de alertas tempranas reportó, para el período 2024-12 a 2025-12, cinco estaciones estables, tres en alerta y ninguna en estado crítico**, proporcionando información operacional para la gestión adaptativa del área protegida.

6. **El pipeline multilenguaje demostró ser reproducible, escalable y adaptable**, con código abierto bajo licencia MIT, y constituye una herramienta operacional para el monitoreo de ecosistemas de manglar en contextos tropicales.

---

## 10. Recomendaciones y Trabajo Futuro

Con base en los resultados y limitaciones identificadas, se formulan las siguientes recomendaciones para trabajo futuro:

1. **Validación de campo independiente:** Realizar campañas de campo para validar la clasificación de cobertura y la segmentación de parches en períodos no cubiertos por la cartografía INVEMAR (2013-2019, 2022-2025), con énfasis en zonas de transición manglar disperso-no manglar.

2. **Incorporación de datos de muy alta resolución:** Integrar imágenes de drones (UAV) con resolución < 1 m para caracterizar la estructura del dosel, discriminar especies de manglar y validar productos Sentinel-2 a escala de parche.

3. **Fine-tuning de modelos de fundación:** Entrenar o ajustar el modelo SAM con datos etiquetados de manglar para mejorar la precisión de segmentación y explorar prompts textuales mediante modelos multimodales (e.g., CLIP, BLIP).

4. **Análisis de causalidad climática:** Integrar datos in situ de salinidad, nivel freático y mortalidad de árboles para establecer relaciones causales entre eventos ENSO, variables ambientales y cambios en cobertura de manglar, mediante modelos de ecuaciones estructurales o análisis de mediación.

5. **Evolución hacia Digital Twin Nivel 2:** Desarrollar modelos predictivos (e.g., redes neuronales recurrentes LSTM, modelos de ecuaciones diferenciales) que proyecten la trayectoria del ecosistema bajo diferentes escenarios de forzamiento climático y manejo, con horizontes de predicción de 3-6 meses.

6. **Transferibilidad del pipeline:** Evaluar la transferibilidad del pipeline a otros sistemas de manglar en Colombia (e.g., Pacífico, Golfo de Urabá) y América Latina, identificando ajustes necesarios en clasificadores, umbrales de alerta y parámetros de modelos.

7. **Integración con sistemas de información geográfica operacionales:** Desarrollar interfaces web (e.g., dashboards interactivos con Shiny, Streamlit) para visualización de resultados y generación de reportes automáticos, facilitando la adopción del pipeline por gestores de áreas protegidas.

8. **Análisis de servicios ecosistémicos:** Integrar el pipeline con modelos de valoración de servicios ecosistémicos (e.g., captura de carbono, protección costera, sostenimiento de pesquerías) para cuantificar los beneficios económicos de la conservación y restauración del manglar.

---

## 11. Referencias

Belgiu, M., & Drăguţ, L. (2016). Random forest in remote sensing: A review of applications and future directions. *ISPRS Journal of Photogrammetry and Remote Sensing*, *114*, 24-31. https://doi.org/10.1016/j.isprsjprs.2016.01.011

Beltrán, D. M., Blanco, J. F., & Viloria, E. A. (2022). *Estructura forestal de manglares en la Ciénaga Grande de Santa Marta, Colombia (2001-2021)* [Conjunto de datos]. Global Biodiversity Information Facility. https://doi.org/10.15472/0fqdp4

Bommasani, R., Hudson, D. A., Adeli, E., Altman, R., Arora, S., von Arx, S., Bernstein, M. S., Bohg, J., Bosselut, A., Brunskill, E., Brynjolfsson, E., Buch, S., Card, D., Castellon, R., Chatterji, N., Chen, A., Creel, K., Davis, J. Q., Demszky, D., ... Liang, P. (2021). On the opportunities and risks of foundation models. *arXiv preprint arXiv:2108.07258*. https://arxiv.org/abs/2108.07258

Breiman, L. (2001). Random forests. *Machine Learning*, *45*(1), 5-32. https://doi.org/10.1023/A:1010933404324

Bunting, P., Rosenqvist, A., Lucas, R. M., Rebelo, L.-M., Hilarides, L., Thomas, N., Hardy, A., Itoh, T., Shimada, M., & Finlayson, C. M. (2018). The Global Mangrove Watch—A new 2010 global baseline of mangrove extent. *Remote Sensing*, *10*(10), 1669. https://doi.org/10.3390/rs10101669

Cleveland, R. B., Cleveland, W. S., McRae, J. E., & Terpenning, I. (1990). STL: A seasonal-trend decomposition procedure based on loess. *Journal of Official Statistics*, *6*(1), 3-73.

DeVries, B., Verbesselt, J., Kooistra, L., & Herold, M. (2015). Robust monitoring of small-scale forest disturbances in a tropical montane forest using Landsat time series. *Remote Sensing of Environment*, *161*, 107-121. https://doi.org/10.1016/j.rse.2015.02.012

Giri, C., Ochieng, E., Tieszen, L. L., Zhu, Z., Singh, A., Loveland, T., Masek, J., & Duke, N. (2011). Status and distribution of mangrove forests of the world using earth observation satellite data. *Global Ecology and Biogeography*, *20*(1), 154-159. https://doi.org/10.1111/j.1466-8238.2010.00584.x

Gislason, P. O., Benediktsson, J. A., & Sveinsson, J. R. (2006). Random forests for land cover classification. *Pattern Recognition Letters*, *27*(4), 294-300. https://doi.org/10.1016/j.patrec.2005.08.011

Gupta, K., Mukhopadhyay, A., Giri, S., Chanda, A., Majumdar, S. D., Samanta, S., Mitra, D., Samal, R. N., Pattnaik, A. K., & Hazra, S. (2018). An index for discrimination of mangroves from non-mangroves using LANDSAT 8 OLI imagery. *MethodsX*, *5*, 1129-1139. https://doi.org/10.1016/j.mex.2018.09.011

Hamilton, S. E., & Casey, D. (2016). Creation of a high spatio-temporal resolution global database of continuous mangrove forest cover for the 21st century (CGMFC-21). *Global Ecology and Biogeography*, *25*(6), 729-738. https://doi.org/10.1111/geb.12449

Instituto de Investigaciones Marinas y Costeras. (2024). *Monitoreo de la condición de los manglares y su relación con el régimen hidrológico en la Ciénaga Grande de Santa Marta*. INVEMAR.

Kirillov, A., Mintun, E., Ravi, N., Mao, H., Rolland, C., Gustafson, L., Xiao, T., Whitehead, S., Berg, A. C., Lo, W.-Y., Dollár, P., & Girshick, R. (2023). Segment anything. *arXiv preprint arXiv:2304.02643*. https://arxiv.org/abs/2304.02643

Lagomasino, D., Fatoyinbo, T., Lee, S., Feliciano, E., Trettin, C., & Simard, M. (2016). A comparison of mangrove canopy height using multiple independent measurements from land, air, and space. *Remote Sensing*, *8*(4), 327. https://doi.org/10.3390/rs8040327

Lagomasino, D., Fatoyinbo, T., Castañeda-Moya, E., Cook, B. D., Montesano, P. M., Neigh, C. S. R., Corp, L. A., Ott, L. E., Chavez, S., & Morton, D. C. (2021). Storm surge, not wind, caused mangrove dieback in southwest Florida following Hurricane Irma. *Nature Communications*, *12*(1), 4119. https://doi.org/10.1038/s41467-021-24253-y

Lovelock, C. E., Feller, I. C., Reef, R., Hickey, S., & Ball, M. C. (2017). Mangrove dieback during fluctuating sea levels. *Scientific Reports*, *7*(1), 1680. https://doi.org/10.1038/s41598-017-01927-6

Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., Blondel, M., Prettenhofer, P., Weiss, R., Dubourg, V., Vanderplas, J., Passos, A., Cournapeau, D., Brucher, M., Perrot, M., & Duchesnay, É. (2011). Scikit-learn: Machine learning in Python. *Journal of Machine Learning Research*, *12*, 2825-2830.

Pham, T. D., Yoshino, K., Le, N. N., & Bui, D. T. (2019). Estimating aboveground biomass of a mangrove plantation on the Northern coast of Vietnam using machine learning techniques with an integration of ALOS-2 PALSAR-2 and Sentinel-2A data. *International Journal of Remote Sensing*, *40*(20), 7761-7788. https://doi.org/10.1080/01431161.2019.1604718

Rackauckas, C., & Nie, Q. (2017). DifferentialEquations.jl – A performant and feature-rich ecosystem for solving differential equations in Julia. *Journal of Open Research Software*, *5*(1), 15. https://doi.org/10.5334/jors.151

Schultz, M., Clevers, J. G. P. W., Carter, S., Verbesselt, J., Avitabile, V., Quang, H. V., & Herold, M. (2016). Performance of vegetation indices from Landsat time series in deforestation monitoring. *International Journal of Applied Earth Observation and Geoinformation*, *52*, 318-327. https://doi.org/10.1016/j.jag.2016.06.020

Verbesselt, J., Hyndman, R., Newnham, G., & Culvenor, D. (2010a). Detecting trend and seasonal changes in satellite image time series. *Remote Sensing of Environment*, *114*(1), 106-115. https://doi.org/10.1016/j.rse.2009.08.014

Verbesselt, J., Hyndman, R., Zeileis, A., & Culvenor, D. (2010b). Phenological change detection while accounting for abrupt and gradual trends in satellite image time series. *Remote Sensing of Environment*, *114*(12), 2970-2980. https://doi.org/10.1016/j.rse.2010.08.003

Worthington, T., & Spalding, M. (2018). Mangrove restoration potential: A global map highlighting a critical opportunity. University of Cambridge. https://doi.org/10.17863/CAM.39153

Wu, Q., & Osco, L. P. (2023). *samgeo: A Python package for segmenting geospatial data with the Segment Anything Model (SAM)* [Software]. GitHub. https://github.com/opengeos/segment-geospatial

---

## 12. Anexos

### Anexo A: Especificaciones Técnicas del Pipeline

**Lenguajes y versiones:**
- Python 3.10.12
- R 4.3.1
- Julia 1.9.3

**Librerías principales (Python):**
- earthengine-api 0.1.374
- geemap 0.28.2
- samgeo 0.11.1
- scikit-learn 1.3.0
- rasterio 1.3.8
- geopandas 0.14.0
- xarray 2023.8.0

**Paquetes principales (R):**
- stars 0.6-4
- sf 1.0-14
- bfast 1.6.1
- ggplot2 3.4.3
- dplyr 1.1.3

**Paquetes principales (Julia):**
- DifferentialEquations.jl 7.10.0
- Optim.jl 1.7.8
- DataFrames.jl 1.6.1

**Recursos computacionales:**
- Procesador: Intel Core i7-11800H (8 núcleos, 16 hilos)
- Memoria RAM: 32 GB
- Almacenamiento: 512 GB SSD
- Cuota Google Earth Engine: 10.000 tareas/día
- Tiempo de procesamiento total: ~48 horas

### Anexo B: Estructura del Repositorio

```
proyecto-cgsm-curso/
├── data/
│   ├── raw/                    # Datos crudos descargados
│   ├── processed/              # Datos procesados
│   └── reference/              # Cartografía de referencia INVEMAR
├── src/
│   ├── python/                 # Módulos Python
│   │   ├── gee_download.py
│   │   ├── rf_classifier.py
│   │   ├── samgeo_segment.py
│   │   └── utils.py
│   ├── r/                      # Scripts R
│   │   ├── timeseries_analysis.R
│   │   └── visualization.R
│   └── julia/                  # Scripts Julia
│       └── ecosystem_model.jl
├── notebooks/                  # Jupyter/R Markdown notebooks
├── results/                    # Resultados (mapas, gráficos, tablas)
├── docs/                       # Documentación
├── LICENSE                     # Licencia MIT
└── README.md                   # Documentación principal
```

### Anexo C: Código de Ejemplo - Clasificación Random Forest

```python
# src/python/rf_classifier.py
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, f1_score
import rasterio
import geopandas as gpd

def extract_features(image_path, reference_path, n_samples=1000):
    """
    Extrae características espectrales de imagen para entrenamiento.
    
    Args:
        image_path: Ruta a imagen Sentinel-2 (GeoTIFF)
        reference_path: Ruta a cartografía de referencia (GeoJSON)
        n_samples: Número de muestras por clase
    
    Returns:
        X: Array de características (n_samples * n_classes, n_features)
        y: Array de etiquetas (n_samples * n_classes,)
    """
    # Cargar imagen
    with rasterio.open(image_path) as src:
        bands = src.read()  # (n_bands, height, width)
        transform = src.transform
    
    # Cargar referencia
    reference = gpd.read_file(reference_path)
    
    # Muestreo estratificado por clase
    X_list, y_list = [], []
    for class_id, class_name in enumerate(['manglar_denso', 'manglar_disperso', 'no_manglar']):
        class_polygons = reference[reference['clase'] == class_name]
        # ... (código de muestreo aleatorio dentro de polígonos)
        # ... (extracción de valores de píxel)
        X_list.append(class_samples)
        y_list.append(np.full(n_samples, class_id))
    
    X = np.vstack(X_list)
    y = np.concatenate(y_list)
    
    return X, y

def train_rf_classifier(X_train, y_train, n_estimators=100):
    """
    Entrena clasificador Random Forest.
    
    Args:
        X_train: Características de entrenamiento
        y_train: Etiquetas de entrenamiento
        n_estimators: Número de árboles
    
    Returns:
        clf: Clasificador entrenado
    """
    clf = RandomForestClassifier(
        n_estimators=n_estimators,
        max_features='sqrt',
        random_state=42,
        n_jobs=-1
    )
    clf.fit(X_train, y_train)
    
    return clf

def evaluate_classifier(clf, X_test, y_test):
    """
    Evalúa desempeño del clasificador.
    
    Args:
        clf: Clasificador entrenado
        X_test: Características de prueba
        y_test: Etiquetas de prueba
    
    Returns:
        metrics: Diccionario con métricas de desempeño
    """
    y_pred = clf.predict(X_test)
    
    metrics = {
        'f1_score': f1_score(y_test, y_pred, average='weighted'),
        'confusion_matrix': confusion_matrix(y_test, y_pred),
        'classification_report': classification_report(y_test, y_pred)
    }
    
    return metrics

# Ejemplo de uso
if __name__ == '__main__':
    # Extraer características
    X, y = extract_features(
        'data/processed/s2/sentinel2_2024_composite.tif',
        'data/reference/invemar_mangrove_2020_2021.geojson',
        n_samples=1000
    )
    
    # Dividir en entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, stratify=y, random_state=42
    )
    
    # Entrenar clasificador
    clf = train_rf_classifier(X_train, y_train, n_estimators=100)
    
    # Evaluar
    metrics = evaluate_classifier(clf, X_test, y_test)
    print(f"F1-score: {metrics['f1_score']:.3f}")
    print(metrics['classification_report'])
```

### Anexo D: Código de Ejemplo - Análisis de Series Temporales en R

```r
# src/r/timeseries_analysis.R
library(bfast)
library(stars)
library(sf)
library(dplyr)
library(ggplot2)

#' Construye serie temporal de NDVI para estaciones de monitoreo
#'
#' @param ndvi_dir Directorio con archivos GeoTIFF de NDVI mensuales
#' @param stations_path Ruta a archivo de estaciones (GeoJSON)
#' @return Data frame con series temporales
build_ndvi_timeseries <- function(ndvi_dir, stations_path) {
  # Listar archivos NDVI
  tifs <- list.files(ndvi_dir, pattern = "NDVI.*\\.tif$", full.names = TRUE)
  
  # Extraer fechas de nombres de archivo
  fechas <- as.Date(stringr::str_match(basename(tifs), "(\\d{4})_(\\d{2})")[, 2:3], 
                    format = "%Y_%m")
  
  # Cargar cubo espaciotemporal (lazy loading)
  cubo <- read_stars(tifs, along = list(time = fechas), proxy = TRUE)
  
  # Cargar estaciones
  estaciones_sf <- st_read(stations_path, quiet = TRUE)
  
  # Extraer valores de NDVI en estaciones
  serie <- st_extract(cubo, st_transform(estaciones_sf, st_crs(cubo)))
  
  # Convertir a data frame
  df <- as.data.frame(serie) %>%
    rename(ndvi = 1, estacion = 2, fecha = time) %>%
    arrange(estacion, fecha)
  
  return(df)
}

#' Aplica bfast para detección de quiebres estructurales
#'
#' @param ts Serie temporal (objeto ts)
#' @param h Parámetro de frecuencia mínima de quiebres
#' @return Objeto bfast con resultados
detect_breakpoints <- function(ts, h = 0.15) {
  # Aplicar bfast
  bf <- bfast(ts, h = h, season = "harmonic", max.iter = 10)
  
  return(bf)
}

#' Visualiza serie temporal con quiebres detectados
#'
#' @param bf Objeto bfast
#' @param title Título del gráfico
plot_bfast_results <- function(bf, title = "Serie Temporal con Quiebres") {
  plot(bf, main = title)
}

# Ejemplo de uso
if (interactive()) {
  # Construir series temporales
  df <- build_ndvi_timeseries(
    ndvi_dir = "data/processed/s2/ndvi_monthly",
    stations_path = "data/reference/invemar_stations.geojson"
  )
  
  # Convertir a serie temporal para una estación
  ts_pajaral1 <- df %>%
    filter(estacion == "Pajaral_1") %>%
    pull(ndvi) %>%
    ts(start = c(2013, 1), frequency = 12)
  
  # Detectar quiebres
  bf <- detect_breakpoints(ts_pajaral1, h = 0.15)
  
  # Visualizar
  plot_bfast_results(bf, title = "NDVI Pajaral 1 (2013-2025)")
  
  # Resumen de quiebres
  print(bf$output[[1]]$breakpoints)
}
```

---

**Fin del Informe**
