Pipeline multilenguaje (Python; R, Julia) para el monitoreo de
manglar en la CGSM (2013-2025)

# Lina Maria Quintero Fonseca

2026-05-20

Universidad Nacional de Colombia
Facultad de Ciencias Agrarias Maestria en Geomatica
Programacion en SIG Proyecto Final
Repositorio: https: 'github . con/linaq11/proyecto-cgsm-curso

# Puntos destacados

Cadena de procesamiento multilenguaje (Python + R + Julia) sobre la CGSM acotada
al sitio Ramsar oficial (SFF + VPI Salamanca, 835,3 km?, en el periodo 2013-2025_

El clasificador supervisado Random Forest   alcanza Fl 0,826 frente INVEMAR
1.25.000 , una mejora del 42 % sobre la clasificacion por umbrales NDVI/CMRI:

La serie continua Sentinel-1 SAR-VH correlaciona con NDVI +0,807 sobre el
manglar denso del Complejo de Pajarales (p < 0,001) , comportamiento ausente sobre las
estaciones limnologicas_

El algoritmo bfast detecta quiebres estructurales en 2016, 2020 y 2023-2024 sobre las
series mensuales combinadas Landsat + Sentinel-2 , asociables los eventos ENSO
documentados.

El modulo de alertas tempranas Digital Twin Nivel reporta sobre el corte 2024-12
2025-12: cinco estaciones estables; tres en alerta y ninguna en estado critico.

# 1 Introduccion Y Justificacion

La Cienaga Grande de Santa Marta CGSM constituye el sistema lagunar costero mas extenso
de Colombia uno de los humedales de mayor relevancia ecologica en America Latina, gracias
que SUs extensas coberturas de manglar cumplen funciones de regulacion hidrica, proteccion costera
sostenimiento de la pesca artesanal regional (Instituto de Investigaciones Marinas Costeras
[INVEMAR] , 2024) . Reconocida como sitio Ramsar desde 1998 y Reserva de Biosfera UNESCO
desde 2000,; 1a CGSM ha sido objeto de multiples figuras de proteccion que reconocen SI importancia
ecologica; sin embargo; desde la decada de los noventa el sistema ha experimentado una degradacion
severa y ciclica de Su cobertura de manglar; impulsada por la interrupcion del flujo hidrico tras
la construccion de la carretera Cienaga-Barranquilla en los aiios   cincuenta, la hipersalinizacion
resultante; la deforestacion para actividades agropecuarias y la intensificacion de los eventos ENSO
especialmente La Niiia de modo que aunque la reapertura de cinco canales hidraulicos entre
1996 y 1998 promovio una recuperacion parcial, la dinamica del ecosistema continua siendo inestable

y los ciclos de degradacion y recuperacion no estan completamente caracterizados a alta resolucion
espaciotemporal (INVEMAR, 2024)_

El monitoreo de manglares mediante teledeteccion ha evolucionado de manera sostenida en la ultima
decada, de modo que se ha transitado del inventario global partir de mosaicos Landsat circa-
2000 (Giri et al., 2011) y de las series globales continuas en alta resolucion temporal Hamilton
Casey, 2016) hacia el US0 de la coleccion Sentinel-2, cuya resolucion espacial de 10 metros
temporal de 5 dias ha mejorado sustancialmente la capacidad de detectar cambios fenologicos
perturbaciones escala local: En Colombia, el INVEMAR ha realizado monitoreos sistematicos de
la CGSM documentando los ciclos de muerte y recuperacion del manglar a traves de seis estaciones
permanentes de campo ~cinco en el Complejo de Pajarales y una en el sector de Sevillano cuyos
datos de estructura forestal estan publicados en el repositorio del Global Biodiversity Information
Facility GBIF Beltran et al.. 2022; DOI: 10.15472 /Ofqdp4). No obstante;, estos estudios se
basan principalmente en interpretacion visual clasificaciones supervisadas clasicas, sin recurrir al
analisis automatico basado en modelos de fundacion como el Segment Anything Model SAM de
Meta AI, adaptado para datos geoespaciales traves de SamGeo (Wu y Osco, 2023) , que permite
realizar segmentacion promptable de imagenes satelitales sin necesidad de grandes conjuntos de
datos etiquetados_

En este marco; la integracion de herramientas de Inteligencia Artificial Geoespacial GeoAI con
plataformas  de geocomputacion en la   nube como Google Earth Engine GEE abre uha via
metodologica para el monitoreo costero a alta resolucion espaciotemporal. El presente proyecto se
propone desarrollar UII pipeline multilenguaje Python; R Julia que articule el analisis de
series de tiempo de indices espectrales con la segmentacion automatica de cobertura de manglar de
manera que el resultado pueda servir como componente de observacion de un futuro Digital Twin
costero para la CGSM, sin pretender constituirse en si mismo como tal en Su version actual. La
caracterizacion espaciotemporal del manglar en la CGSM constituye un insumo para la gestion de
riesgos de inundacion y la formulacion de politica publica ambiental; en febrero de 2026 se firmo el
Plan de Manejo Ambiental del sitio Ramsar Sistema Delta Estuarino del Rio Magdalena-CGSM con
ua vigencia de diez aiios, Y que orienta el seguimiento ambiental permanente del humedal Comision
Conjunta CGSM, 2026) , de modo que un pipeline automatizado como el que aqui se propone resulta
pertinente para alimentar dicho seguimiento COn productos cartograficos reproducibles.

A partir de lo anterior, el presente estudio se articula en torno a la siguiente pregunta de investigacion:
icomo ha variado la cobertura; la fragmentacion y el vigor del manglar de la Cienaga
Grande de Santa Marta entre 2013 y 2025,Y que evidencia cuantitativa permite atribuir
las perturbaciones detectadas forzantes climaticos asociados al evento La Nina 2020
2021?

# 2 Estado del Arte

2.1 Teledeteccion de manglares: de Landsat al monitoreo multitemporal con
Sentinel-2

EL monitoreo satelital de manglares ha avanzado en las ultimas tres decadas: el primer inventario
global  moderno lo produjo Giri et al (2011) sobre U mosaico Landsat circa-2000 30 de
resolucion; mientras que Hamilton y Casey (2016) extendieron la observacion a ua serie temporal
anual continua   mediante el conjunto CGMFC-21 para el periodo 2000-2012, ambos basados en
archivos Landsat. Con el lanzamiento de la coleccion Sentinel-2, la resolucion espacial de 10 metros

y la revisita de 5 dias mejoraron sustancialmente la capacidad de detectar cambios fenologicos
escala local, de modo que hoy es posible construir series  temporales densas que capturen la
variabilidad estacional e interanual de la cobertura vegetal costera. Raza et al. (2024) demostraron
que el analisis de series de tiempo del NDVI derivadas de Sentinel-2 en GEE permite detectar
tendencias de deterioro en la salud del manglar incluso cuando la extension del bosque se mantiene
estable, razon por la cual las estimaciones de cobertura pOr si solas resultan insuficientes deben
acompanarse de indicadores de condicion de la vegetacion.

En cuanto los  indices   espectrales , Gupta et al. (2018)   propusieron el Combined   Mangrove
Recognition Index CMRI definido como la   diferencia   entre NDVI el NDWI, que ha
demostrado ser efectivo para   discriminar  manglar de otras coberturas   vegetales en ambientes
estuarinos, alcanzando uha precision del 73,43%  frente indices   convencionales como el NDVI
(56,29%) 0 el Simple Ratio (48,79%) . escala global, el Global Mangrove Watch GMW de
JAXA provee la referencia mas completa de distribucion de manglares para el periodo 1996-2020
en su   version 3.0 (Bunting et al., 2022) , mientras que a escala  nacional, el INVEMAR genero
en 2020 la cartografia oficial de manglares de Colombia escala 1.25.000 mediante clasificacion
supervisada en GEE con imagenes opticas y de radar, con una   unidad minima cartografiada de
1.600 m2 (INVEMAR, 2020) .

Los inventarios   globales basados en Landsat han   consolidado ua narrativa   segun la cual la
perdida de  manglar   obedece, en SU mayor parte; la   presion   antropica directa:  Goldberg et
al. (2020) , mediante clasificacion por Random Forest sobre mas de ul millon de escenas Landsat
30 1, atribuyen el 62 % de la perdida mundial entre 2000 y 2016 al cambio de us0 del suelo
~principalmente acuicultura agricultura de exportacion con casi 80 %   concentrado en
seis   paises del  sudeste asiatico. Sin   embargo, este marco centrado en transiciones abruptas
detectables como conversiones estanques cultivos tiende a invisibilizar las perdidas graduales
que dominan en   otras geografias, de manera que SU aplicacion contexto colombiano resulta
limitada. Asimismo, Murillo-Sandoval et al. (2022) , al reconstruir 36 aiios de cobertura mediante el
algoritmo LandTrendr sobre el archivo Landsat, documentan una disminucion de aproximadamente
48 000 ha -14 % del area nacional muestran que la transicion dominante no es la conversion
abrupta sino la degradacion de manglar denso a otra vegetacion, con 38 469 + 2 829 ha afectadas;
asimismo, identifican UIl retroceso sostenido en el Pacifico desde 2004 descensos en el Caribe
enbre 1984-1988 posteriores 2012 asociados expansion  agricola; construccion de  vias
alteraciones hidrosedimentarias_ La tension que emerge entre ambas   fuentes global   frente
nacional sustenta la necesidad de aproximaciones pOr trayectorias temporales densas capaces de
capturar transiciones intermedias entre cobertura plena y suelo desnudo.

# 2.2 Google Earth Engine como plataforma de monitoreo

La adopcion de GEE para estudio de manglares se ha acelerado en los ultimos   aios,
pues   la   plataforma   permite procesar  miles   de imagenes   satelitales sin   requerir infraestructura
computacional local. Selvaraj Gallego-Perez (2023) aplicaron GEE al mapeo de manglares en
el Pacifico colombiano combinando datos opticos de Landsat y datos de radar SAR de ALOS-
2 /PALSAR-2 con un clasificador Random Forest, obteniendo precisiones moderadas a altas en la
deteccion de cambios de cobertura entre 2009 y 2019. Bunting et al. (2022) generaron la version 3.0
del GMW mediante deteccion de cambios sobre series anuales de SAR L-band JERS-1, ALOS
ALOS-2 PALSAR de JAXA produciendo mapas de extension de manglar para once epocas
discretas entre 1996 y 2020, complementadas con imagenes Landsat accedidas via Google Earth
Engine para la validacion de exactitud.

En esta misma linea, Yancho et al. (2020) presentan la Google Earth Engine Mangrove Mapping
Methodology GEEMMM una herramienta abierta replicable concebida para que gestores
costeros sin formacion especializada puedan cartografiar y monitorear manglares dentro del entorno
de computo en la nube de GEE, integrando una calibracion mareal basada en reflectancia de linea
de costa y validada sobre la totalidad del litoral de Myanmar: Su precedente resulta directamente
aplicable, de manera que la presente investigacion adopta una arquitectura analoga ~procesamiento
integro en GEE; mascaras de nube y composiciones temporales aunque sustituye la clasificacion
supervisada pOr umbrales espectrales NDVI y CMRI calibrados localmente para la Cienaga Grande
de Santa Marta. Asimismo, dado que toda cartografia de cambio exige cuantificar SU incertidumbre;
las recomendaciones canonicas de Olofsson et al (2014) sobre diseno de muestreo probabilistico,
matriz de error expresada en proporciones de area intervalos de confianza para superficies de
cambio constituyen la   referencia   metodologica que se   desarrollara en  la   seccion de Validacion;
garantizando trazabilidad estadistica los productos derivados_

# 2.3 Monitoreo de la Cienaga Grande de Santa Marta

En la CGSM, el INVEMAR realiza monitoreo continuo desde la reapertura de los canales hidraulicos
entre 1996 y 1998, evaluando la calidad de aguas, la estructura del bosque de manglar y los recursos
pesqueros en marco del Convenio de Cooperacion No. 16/2006 con la Corporacion Autonoma
Regional del Magdalena CORPAMAG (INVEMAR 2024)_ El monitoreo de manglar opera
en seis estaciones permanentes: cinco en el Complejo de Pajarales Luna, Aguas Negras Caiio
Grande; Km22 y Rinconada una en el sector de Sevillano, y los datos de estructura forestal
correspondientes al periodo 2013-2019 estan publicados en GBIF bajo licencia CC-BY Beltran et
al,, 2022) . El informe tecnico mas reciente documenta que cinco estaciones mantienen una integridad
biologica Regular Aguas Negras Caiio Grande, Km 22 y Luna Rinconada se sostiene en
"Buen estado" y Sevillano se encuentra en Alerta las perdidas masivas historicas de individuos
se concentraron en Km 22 Luna tras el evento El Nino 2015-2016 (INVEMAR , 2024) .

Entre los  antecedentes   especificos para   el complejo lagunar resulta especialmente pertinente el
trabajo de Vinasco et al. (2020) , quienes  cuantificaron los cambios de cobertura en  la Cienaga
Grande de Santa Marta entre 2013 y 2018 partir de 119 escenas Landsat-8 procesadas de manera
local, con  correccion DOS y clasificacion supervisada mediante Random Forest u perceptron
multicapa  entrenados sobre 300 muestras distribuidas en seis   clases CORINE Land Cover_ Los
autores articularon su   analisis partir de los  indices NDVI, EVI NDWI empleados cOmo
descriptores temporales del estado de la vegetacion y de las superficies inundadas reportaron UI
incremento de la frontera agricola y urbana acompaiado de una contraccion del 27 % al 12 % de las
areas hiimedas_ Esta aproximacion, si bien metodologicamente afin al presente estudio en cuanto
al uSo de indices espectrales sobre Landsat, opera como ejercicio de clasificacion de coberturas
generales no aisla la cobertura de manglar, de manera que el aporte de este trabajo consiste
en sustituir los clasificadores supervisados por   umbrales NDVI CMRI sobre series  temporales
armonizadas Landsat 8/9 y Sentinel-2 asi como en migrar el procesamiento integramente a Google
Earth Engine.

# 2.4 GeoAI y segmentacion geoespacial

La aparicion de modelos de fundacion como el Segment Anything Model de Meta AI (Kirillov
et al,, 2023) , adaptado para datos geoespaciales a traves de SamGeo (Wu y Osco; 2023) , permite
realizar segmentacion promptable de imagenes satelitales sin grandes conjuntos de datos etiquetados,
mediante prompts geometricos ~puntos, cajas 0 mascaras nativos del modelo 0, alternativamente,

mediante text  prompts  aportados por detector   Grounding  DINO acoplado en SamGeo. La
plataforma  OpenGeoAI, liderada por el profesor Qiusheng Wu de la Universidad de Tennessee.
ha desarrollado un  conjunto de herramientas de codigo abierto geemap; leal fmap y SamGeo
integradas cOnl GEE, de manera que posible construir cadenas de procesamiento geoespacial
completas en la nube. El concepto de Digital Twin aplicado humedales, explorado recientemente
como marco para soportar el monitoreo y la gestion de ecosistemas (Lu et al , 2026) , combina datos
de observacion de la Tierra, modelos fisicos y aprendizaje automatico para reflejar dinamicamente
el estado del sistema. En este marco, el componente de monitoreo basado en teledeteccion que este
proyecto desarrolla podria servir como capa de actualizacion para U futuro gemelo digital, sin
pretender agotar la complejidad de un sistema acoplado de observacion-modelacion-simulacion_

# 3 Objetivos

# 3.1 Objetivo general

Desarrollar u pipeline GeoAl multilenguaje para el monitoreo de la dinamica espaciotemporal de
la cobertura de manglar en la Cienaga Grande de Santa Marta (2013-2025).

# 3.2 Objetivos especificos

1,. Construir un   datacube multitemporal de indices espectrales para la caracterizacion de la
cobertura de manglar en la CGSM:

Identificar los   periodos de  degradacion recuperacion del   manglar   mediante analisis de
anomalias temporales_

Validar la segmentacion automatica de cobertura de manglar contra cartografia de referencia_

# Area de estudio

A map of Colombia showing its departments. The map is labeled with a title "Magdalena" at the top center and "(a)" in the top left corner. A compass rose with "N" is in the top right corner.

The map is set against a light blue background. The outline of Colombia is light orange, and its internal departmental borders are thin black lines. The department of Magdalena, located in the northern part of Colombia, is highlighted in a darker orange color.

A horizontal scale bar is located in the bottom left corner, labeled "500 km".

The map has a coordinate system with latitude and longitude lines.
- Latitude lines are marked on the left side at intervals of 2, from -4 to 12.
- Longitude lines are marked at the bottom at intervals of 2, from -82 to -66.


A map of a coastal region, likely in South America, with a focus on the Magdalena department of Colombia.

**Map Details:**
*   **Title:** (b)
*   **Body of Water:** Caribbean Sea, labeled in blue text at the top.
*   **Landmass:** A large landmass is depicted, with a significant portion highlighted in orange, labeled "Magdalena" in large orange text.
*   **Cities/Locations:**
    *   Santa Marta: Labeled in black text, located on the coast within the orange Magdalena region. A black dot marks its location.
    *   Ciénaga: Labeled in black text, located on the coast within the orange Magdalena region, south of Santa Marta. A black dot marks its location.
    *   Barranquilla: Labeled in black text, located on the coast just outside the orange Magdalena region, to the west. A black dot marks its location.
*   **Area of Interest:** A red rectangular box highlights a coastal area encompassing Barranquilla and the northwestern part of the Magdalena region.
*   **Scale Bar:** A black and white scale bar is present in the bottom left corner, labeled "50 km".
*   **Compass Rose:** A black "N" indicates North in the top right corner.
*   **Coordinates:**
    *   **Latitude (Y-axis):** Labeled from 9.5 to 11.5 in increments of 0.5.
    *   **Longitude (X-axis):** Labeled from -75.50 to -73.50 in increments of 0.25.
*   **Background:** The ocean is light blue, and the unhighlighted land is light gray.


(c) Area de estudio 1.286 km'

A satellite image of a coastal region, with a legend in the top left corner and a scale bar in the bottom left.

**Legend:**
*   **Red outline:** Área de estudio (1.286 km²)
*   **Light green shaded area:** Manglar (SamGeo, 2024-2025)
*   **Red triangle:** Estación INVEMAR (5)

**Geographic Features:**
*   **Top center:** Mar Caribe
*   **Below Mar Caribe, along the coast:** Vía Parque Isla de Salamanca
*   **Center-right:** Ciénaga Grande de Santa Marta (a large body of water)

**INVEMAR Stations (Red Triangles with Labels):**
*   **Top right, on the coast:** Punta Cerro
*   **Below Punta Cerro, slightly inland:** Isla Boquerón
*   **Below Isla Boquerón, slightly inland:** Punta Chino
*   **Below Punta Chino, slightly inland:** Río Sevilla
*   **Center-bottom, within the Ciénaga Grande de Santa Marta:** Caño Palos

**Coordinates:**
*   **Y-axis (Latitude):** 10.6, 10.7, 10.8, 10.9, 11.0, 11.1
*   **X-axis (Longitude):** -74.8, -74.7, -74.6, -74.5, -74.4, -74.3

**Scale Bar:**
*   **Bottom left:** 10 km

**Compass Rose:**
*   **Top right:** N (North)


Figura 1: Localizacion del area   de estudio. (a Colombia con el  departamento del Magdalena
resaltado en naranja, escala 500 km: (b) Departamento del Magdalena con las ciudades de referencia
Santa Marta, Cienaga, Barranquilla bbox  del AOI acotado en rojo; escala 50 km (c
Composite Sentinel-2 RGB de color real (B4-B3-B2) del periodo actual 2024-2025 sobre un bounding
box extendido que cubre el AOI acotado (835 km? del SFF CGSMy la Via Parque Isla de Salamanca;
poligono rojo) junto con las cinco estaciones INVEMAR-GBIF (triangulos rojos: Isla Boqueron;
Punta Cerro, Punta Chino, Rio Sevilla y Caio Palos) , con la cobertura de manglar segmentada por
SamGeo superpuesta en verde trasliicido.

El area de estudio comprende la CGSM y SU zona de influencia costera, ubicada en el departamento
del Magdalena; Colombia , enbre aproximadamente 10820' N-11905 N 74810' W_74855' W. El
proyecto opera con dos delimitaciones de area anidadas que cumplen funciones distintas La primera,
denominada AOI envolvente y delimitada con 34 vertices sobre 5.073 km? se utilizo unicamente
en la iteracion preliminar del proyecto (marzo de 2026) y se utilizo como baseline preliminar para la
iteracion inicial del proyecto antes del acotamiento metodologico; comprende la Via Parque Isla de
Salamanca, el Complejo de Pajarales , el Santuario de Fauna y Flora CGSM, los canales hidraulicos
rehabilitados Cazio Clarin, Aguas Negras y Renegado y las desembocaduras de los rios Sevilla,
Aracataca y Fundacion: La segunda, denominada AOI acotado y delimitada con 835,3 km? sobre
la union de los poligonos oficiales del Santuario de Fauna y Flora CGSM (26.810 ha) y la Via Parque
Isla de Salamanca extraidos del Registro Unico Nacional de Areas Protegidas (RUNAP), constituye
el area  sobre la cual se sostienen todos los resultados reportados en cuerpo del informe v6;
este acotamiento obedece que la inclusion de vegetacion riberana, salitral y zonas agropecuarias
en el AOI envolvente inflaba   sistematicamente las cifras de manglar potencial comprometia la
comparabilidad con la cartografia oficial de manglares de Colombia (INVEMAR, 2020) con el

Tabla 1: Fuentes de datos utilizadas en pipeline para el monitoreo de manglar_

Tabla 2:

Dataset Fuente Tipo Uso en el proyecto Acces
Sentinel-2 MSI L2A ESA) 789 imagenes (2018-2025) Indices espectrales y RGB para SamGeo GEE:
Landsat 8 OLI USGS) 345 registros (2013-2017) Serie historica NDVI complementaria GEE:
Sentinel-1 SAR ESA) 85 imagenes (2020) Deteccion de inundacion bajo dosel GEE:
Global Flood Database 16 eventos (2001-2017) Registro historico de inundaciones GEE:
JRC Global Surface Water Raster global Transiciones y estacionalidad hidrica GEE:
SRTM v3 (NASA) DEM 30 m Restriccion de elevacion < 10 m) GEE:
Monitoreo manglar INVEMAR 376 registros (2013-2019) Coordenadas estaciones de muestreo GBIF
Global Mangrove Watch v4.0 Raster (2020) Validacion de clasificacion GEE:

Global  Mangrove Watch (Bunting et al,, 2022) , referencias que tambien se acotan al humedal
propiamente dicho.

Para analisis de series de   tiempo se definieron estaciones de muestreo, de las cuales
5   corresponden estaciones con coordenadas exactas obtenidas del dataset de monitoreo
de estructura de   manglares del INVEMAR publicado en GBIF (Beltran et al. 2022; DOI:
10.15472 /Ofqdp4) Isla Boqueron (10,962 N, 74,298 W) , Punta Cerro (10,973 N, 74,283 W), Punta
Chino (10,912 N, 74,305 W) , Rio Sevilla (10,880 N 74,325 W) y Caio Palos (10,758 N 74,471
W) mientras que las 3 restantes son estaciones complementarias seleccionadas sobre cobertura
de manglar verificada mediante NDVI > 0,4 en composites Sentinel-2 de 2024, con proposito de
representar el Complejo de Pajarales y la zona de rehabilitacion hidrologica del Canio Clarin:

# 5 Fuentes de Datos

Los datos   utilizados en este proyecto provienen tanto de plataformas de geocomputacion en  la
nube como de repositorios institucionales abiertos. Siguiendo la declaracion cuadruple de resolucion
recomendada por Gomarasca 2010) para datos de teledeteccion; las dos colecciones opticas centrales
del proyecto se caracterizan pOr: Sentinel-2 MSI LZA con resolucion espacial de 10 m B2 azul,
B3 verde, B4 rojo, B8 NIR), 20 m (B5-B7, BSA, BlI, B12 SWIR) y 60 m Bl, B9, BlO) , resolucion
espectral de 13 bandas entre 443 y 2190 nm; resolucion temporal de 5 dias (constelacion S2A+S2B_
y resolucion radiometrica de 12 bits; y Landsat 8/9 OLI con resolucion espacial de 30 m en bandas
multispectrales (15 m en pancromatica) , resolucion espectral de 11 bandas entre 433 y 12500 nm
resolucion temporal de 16 dias por satelite 8 dias combinados LS+L9) y resolucion radiometrica
de 12 bits cuantizada 16 bits para distribucion:

# 6 Metodologia y codigo

El proyecto se desarrolla siguiendo un pipeline modular reproducible organizado en cuatro fases
uil modulo de validacion que se ejecutan dentro de U contenedor Docker ~sig unal vl.ll; que

Tabla 3: Distribucion de responsabilidades tecnicas entre los tres lenguajes del proyecto, con las
librerias centrales y los notebooks que materializan cada funcion. La eleccion obedece a las fortalezas
disciplinares de cada ecosistema se   valida   cruzadamente en la seccion de Validacion   cruzada
multilingiie.

Lenguaje Funcion tecnica Librerias clave
Python Adquisicion GEE, segmentacion SAM, Random Forest, datacubes, dashboard geemap, samgeo,
Deteccion de quiebres bfast; cubo stars , replicas estadisticas bfast, stars sf
Julia Metricas de fragmentacion, topologia DE-9IM, computo geometrico GeoJSON . j1, Data

integra Python 3.12 R 4.3.3, Julia 1.11.3 y Quarto 1.4 de modo que se garantiza la replicabilidad
completa del entorno de analisis. Cada fase se implementa aprovechando las fortalezas del lenguaje
mas   adecuado para la tarea, y la interoperabilidad entre fases se   mantiene mediante formatos
estandar GeoTIFF GeoJSON y CSV

# 6.1 Distribucion multilingiie de responsabilidades

La arquitectura del proyecto distribuye las tareas entre los tres lenguajes del curso Python;
Julia segun la conveniencia  disciplinar de cada fase; n0 como mera   coexistencia obligatoria_
Python sustenta la mayor parte del flujo: adquisicion y procesamiento en Google Earth Engine;
segmentacion   promptable con SamGeo, manipulacion de datacubes con xarray, clasificacion
supervisada con Random Forest, generacion  del dashboard interactivo con folium descarga
del  forzamiento  climatico ERA5-Land con cdsapi_ R se reserva   para tareas estadisticas de
series ecohidrologicas donde Su ecosistema es mas maduro: deteccion de quiebres bfast sobre las
series NDVI mediante el paquete bfast construccion de un  datacube stars como contraparte
local del flujo GEE, y replicacion independiente de los analisis ENSO y caudal IDEAM mediante
tidyverse para   validacion cruzada Python Julia se incorpora para el computo geometrico
de alta velocidad sobre miles de poligonos vectoriales: metricas de fragmentacion del paisaje (NP;
PD. MPA_ MSL, NND) , calculo exacto del area en EPSG:9377 mediante el algoritmo del cordon
(shoelace predicados topologicos DE-9IM (intersects; contains) ejecutados con LibGEOS . jl,
la misma biblioteca GEOS que   sustenta PostGIS geopandas, lo cual garantiza consistencia
geometrica entre los tres entornos. La equivalencia operativa entre lenguajes se demuestra mediante
cuatro validaciones cruzadas formales documentadas en la seccion de Validacion_

# 6.2 Fase l: Construccion del datacube multitemporal (Python + geemap)

La primera fase del pipeline consiste en la construccion de un datacube listo para analisis ua
estructura tridimensional (X, Y, tiempo) que organiza las observaciones satelitales de la CGSM
resoluciones de 10 a 30 metros segun el sensor donde cada capa temporal contiene los valores de
reflectancia superficial e indices espectrales derivados para Un periodo de composicion determinado
Se construye ua coleccion de 789 imagenes Sentinel-2 SR Harmonized para el periodo 2018-2025,

Tabla 5: Datacubes NetCDF CF-1.8 materializados sobre el AOI acotado en EPSG:9377 (MAGNA-
SIRGAS Origen Nacional) , comprimidos con zlib nivel 4

# Tabla 6:

Archivo Sensor Frecuencia Periodo
cgsm_datacube peri odos nc Sentinel-2 Tres composites discretos Degradacion (2020 H2) , recuperac
cgsm_datacube trimestral.nc Sentinel-2 Trimestral 2018-Q1 2025-Q4 (31 trimestres _
cgsm_datacube landsat nc Landsat 8/9 Anual 2013-2025 (13 aios

filtrada pOr cobertura de nubes inferior al 20% y recortada al poligono del area de estudio. Se
aplica uha mascara de nubes   utilizando la banda QA60 se calculan los indices NDVI B8-
B4)/(BS+B4) ; NDWI (B3-B8) / (B3+B8) y CMRI NDVI NDWI pOr imagen, cuya efectividad
para discriminar manglar de otras coberturas en ambientes estuarinos ha sido documentada por
Gupta et al. (2018)_

Construir coleccion S2 SR Harnonized y agregar tres indices espectrales
def add_indices (image)
ndvi image.normalizedDifference ( [ 'B8 B4 ' ] ) rename NDVI
ndwi image.normalizedDifference ( [ 'B3 B8 ' ] ) rename NDWI '
cmri ndvi. subtract (ndwi) rename ( CMRI
return image.addBands ( [ndvi_ ndwi . cmri])

s2 (ee.ImageCollection ( COPERNICUS/S2_SR_HARMONIZED
filterBounds (a0i)
filterDate ( 2018-01-01 ' 2025-12-31 ' )
filter(ee.Filter.lt ( ' CLOUDY PIXEL_PERCENTAGE 20) )
map (mask_s2_clouds)
map (add_indices) )

EL datacube se materializa adicionalmente como tres archivos NetCDF COn convenciones CF-1.8
generados pOr el script build_cubos. Py mediante xarray y rioxarray de modo que el cubo
queda disponible en disco para analisis fuera de la nube y reutilizable desde Python, R Julia sin
necesidad de re-consultar la API de GEE Cada raster se reproyecta al sistema oficial colombiano
EPSG:9377 y se resamplea a 30 metros antes de concatenarse a lo largo del eje temporal, de esta
manera los tres cubos comparten ua sola rejilla espacial y se diferencian unicamente pOr la fuente
sensorial y la frecuencia temporal, asi el flujo de la Fase 4 puede leer cualquiera de los tres con el
mismo bloque de codigo

El bloque de lectura perezosa del datacube NetCDF con catray se documenta en el Anexo E, item
E.1.a.

La diferencia espacial entre la mediana de NDVI del estado actual (julio 2024-junio 2025) y la
del periodo de degradacion   (julio-diciembre 2020) ~calculada   directamente  sobre el datacube
trimestral CF-1.8 permite leer en un solo mapa las zonas que recuperaron vigor frente a aquellas
que   perdieron   cobertura, de modo que la  figura  figura 2  sostiene cualitativamente lo que las

metricas de fragmentacion describen cuantitativamente Las areas en azul corresponden pixeles
que ganaron al menos 0,1 unidades NDVI entre ambos periodos consistentes con la regeneracion
del manglar mientras que las areas en rojo, concentradas principalmente en el borde norte del
Via Parque y en sectores hipersalinos del Santuario, marcan reducciones que pueden asociarse tanto
estresores   climaticos persistentes como heterogeneidad fenologica del manglar entre ambas
ventanas temporales.

# Cambio NDVI: Actual (2024-2025) Degradacion (2020 H2)

A map displaying areas of vigor change, with a legend in the top-left corner.

**Legend:**
*   **Rojo** (Red) = pérdida de vigor (loss of vigor)
*   **Azul** (Blue) = ganancia de vigor (gain of vigor)

**X-axis:** X EPSG:9377 (m)
*   Values range from 4.80e6 to 4.85e6.
*   Tick marks are at 4.80, 4.81, 4.82, 4.83, 4.84, and 4.85.

**Y-axis:** Y EPSG:9377 (m)
*   Values range from 2.74e6 to 2.78e6.
*   Tick marks are at 2.74, 2.75, 2.76, 2.77, and 2.78.

**Map Content:**
The map shows several distinct landmasses or regions, outlined in a light gray. Within these regions, areas are colored in a gradient from red to blue, indicating changes in vigor.

*   **Northern Region:** Located roughly between Y 2.77e6 and 2.78e6, and X 4.80e6 and 4.85e6. This region shows a mix of light blue and light red areas, with some more intense blue patches, particularly towards the center-right. A prominent band of red is visible along the northern edge of this region.
*   **Central Region:** Located roughly between Y 2.76e6 and 2.77e6, and X 4.82e6 and 4.84e6. This region is characterized by a high concentration of dark blue areas, indicating significant gain in vigor. There are also several distinct patches of dark red, indicating significant loss of vigor, interspersed within the blue.
*   **Southern Region:** Located roughly between Y 2.74e6 and 2.76e6, and X 4.82e6 and 4.85e6. This is the largest and most complex region. It features extensive areas of dark blue, particularly in the western and southern parts. Numerous large and small patches of dark red are also present, especially in the central and eastern parts of this region. A thin, elongated landmass extends eastward from this region, showing a mix of light blue and light red.

The background of the map is white, representing areas outside the analyzed regions.


| Visual Element | Meaning |
|---|---|
| Color gradient from dark blue to dark red | ΔNDVI (Change in Normalized Difference Vegetation Index) |
| Dark blue | ΔNDVI = 0.50 |
| Light blue | ΔNDVI = 0.25 |
| White/light beige | ΔNDVI = 0.00 |
| Light red | ΔNDVI = -0.25 |
| Dark red | ΔNDVI = -0.50 |


Figura 2: Cambio en   la mediana de NDVI entre el estado actual (2024-2025) el periodo de
degradacion (2020 H2) , calculado desde el datacube trimestral CF-1.8 sobre el AOL acotado. El
azul indica ganancia de vigor (regeneracion), el rojo indica perdida; coordenadas en metros sobre
EPSG:9377 MAGNA-SIRGAS Origen Nacional.

# 6.3 Fase 2: Analisis de series de tiempo (Python pandas R + bfast)

Se extraen series   temporales   mensuales   de NDVI para   las estaciones de muestreo definidas.
utilizando U buffer de 500 metros alrededor de cada punto y la funcion reduceRegion de GEE
para obtener el valor medio del indice pOr estacion y pOr mes_ La serie se construye combinando dos
sensores: Landsat 8 Collection 2 Level 2 para el periodo 2013-2017 (345 registros, con correccion del
factor de escala x0.0000275 0,2 segun especificacion USGS) y Sentinel-2 SR Harmonized para el
periodo 2018-2025 (584 registros), generando una serie combinada de 929 observaciones mensuales
que cubre 12 aiios. Posteriormente se calcula el z-score temporal por estacion (NDVI del
mes media historica) desviacion estandar lo que permite identificar anomalias pronunciadas

10

definidas como aquellas con z < -2. De manera complementaria; se aplica el algoritmo bfast (Breaks
For Additive Season and Trend) en R sobre las series mensuales combinadas con parametros h
0,15 y h 0,10 para evaluar la presencia de quiebres estructurales en la tendencia de largo plazo.

library(bfast)

serie read. csv ( "outputs/tables serie_temporal ndvi_ combinada _ csV" )
ts_est < - ts(subset (serie _ estacion = "Cano_Palos Sndvi _
start (2013 1) frequency 12)

fit bfast (ts_est , 0.10 season "harmonic" max.iter 2)
plot (fit) quiebres 2016 (El Nino) _ 2020 (La Nina) 2023-24 (El Nino)

El calculo de z-scores y la deteccion de anomalias en Python se documentan en el Anexo E, item
E.1.b.

# 6.4 Fase 3: Segmentacion automatica con SamGeo (Python + samgeo)

Se aplica el modelo SamGeo con el backbone vit b sobre los composites RGB de los tres periodos de
referencia degradacion (juliodiciembre 2020) , recuperacion (enero junio 2022) estado actual
(julio 2024 junio 2025 previamente remuestreados de 10 30 metros para ajustarse las
limitaciones de memoria del contenedor Docker. Las mascaras resultantes se vectorizan y se clasifican
por   estado manglar nO manglar segun valor medio de CMRI dentro de cada   parche;
calculado mediante reduceRegions en GEE con procesamiento en lotes de 200 parches. Se filtran los
parches por area minima de hectarea y maxima de 5.000 hectareas para eliminar fragmentos de
ruido y fondos de imagen:

from samgeo import SamGeo

la RAM del contenedor

# Modelo base vit b para ajustarse SamGeo (model_type= 'vit_b' automatic-True) sam

for periodo in ['degradacion recuperacion 'actual'] :
rgb f '{res_dir}/CGSM_RGB_{periodo} 30m.tif
mask {out_dir}/mask_{periodo} tif
poly f ' {out_dir}/manglar_{periodo}. geojson
sam generate(rgb , output-mask) raster binario
sam.tiff to_vector(mask_ poly) # parches vectoriales

# 6.5 Fase 4: Metricas de fragmentacion del paisaje (Julia)

Se computan metricas de ecologia del paisaje sobre los parches de manglar vectorizados para cada
uno de los tres periodos,  aprovechando la   velocidad de Julia en operaciones   geometricas sobre
grandes volumenes de datos vectoriales  Las metricas incluyen: nimero de parches, densidad de
parches por 1.000 hectareas, area media de parche con desviacion estandar indice de forma medio
MSI perimetro sqrt (pi X area) distribucion de parches por clases de tamano (1-10, 10-50,
50-100 , 100-500, 500-1.000 y 1.000 5.000 ha) , y distancia media al vecino mas cercano NND
como indicador de conectividad.

using GeoJSON DataFrames Statistics

function compute_metrics (periodo , base_dir)

11

path joinpath (base_dir "manglar 8 (periodo)_9377.geojson
parches GeoJSON .read (read (path, String)

# Area por formula del cordon (shoelace) perinetro en metros
areas [shoelace_ area (p) for in parches]
perim [polygon_perimeter (p) for P in parches]
msi perim sqrt . (pi areas) indice de forma medio
nnd nearest ~neighbor_distances (parches) km al vecino mas cercano

return DataFrame (
periodo periodo ,
parches length (parches)
area_total sum (areas) 1e4
area_media mean (areas) 1e4 _
msi mean mean (msi) _
nnd_mean mean (nnd) 1e3 _

# hectareas

end

# 6.6 Patrones de implementacion: lectura perezosa, reproyeccion y topologia

Como cierre de la Metodologia se incorporan tres patrones que refuerzan la robustez tecnica del flujo:
lectura perezosa de rasters, reproyeccion al sistema oficial colombiano y evaluacion de predicados
topologicos DE-9IM:

En primer lugar, los rasters de mascara producidos por SamGeo se inspeccionan mediante lectura
perezosa, abriendo el archivo con rasterio . open () para extraer dimensiones; CRS, resolucion y
valor de NoData sin materializar la grilla en memoria. Este patron resulta especialmente pertinente
en este  proyecto, toda vez que   la carga   completa de los TIF de RGB de  la CGSM provoco
previamente el colapso del kernel de Jupyter al intentar usar SamGeo con el backbone vit
razon pOr la cual se opto por el modelo vit y pOr' la lectura pOr ventanas en las verificaciones
posteriores_

En segundo lugar, los GeoJSON resultantes de la segmentacion se reproyectan al sistema oficial
colombiano MAGNA-SIRGAS Origen Nacional (EPSG:9377 mediante rasterio.warp. calculate_defaul
geopandas .to_ crs Esta reproyeccion  permite que el calculo del area en hectareas se  realice
sobre uha proyeccion equivalente para el territorio colombiano, sustituyendo las aproximaciones
esfericas tipo area dey 111.000 cos( 111.000 que se empleaban inicialmente en el script  Julia
que solo son exactas en el centro del paisaje. La eleccion del EPSG:9377 obedece, ademas, al
estandar oficial del IGAC desde la Resolucion 471 de 2020, lo que facilita la integracion futura del
producto con la cartografia base nacional_

En tercer lugar; sobre los parches reproyectados se aplican dos predicados topologicos DE-9IM,
calculados con geopandas y shapely que delegan en GEOS los mismos predicados que reconocen
PostGIS JTS. El  primer   predicado, intersects (parche frontera AOI) con tolerancia de
30  metros, identifica  los   parches truncados por el   limite del area de estudio, cuya geometria
responde  mas ua decision cartografica externa  que la dinamica del   manglar; el segundo;
contains (parche , estacion_INVEMAR) evalua si los parches segmentados envuelven los puntos
de muestreo utilizados en el analisis bfast, lo que ofrece ua validacion cualitativa adicional al

12

F-score contra GMW.

El   bloque que articula   lectura perezosa del raster,  reproyeccion EPSG:9377 y  aplicacion de
predicados DE-9IM se documenta en el Anexo E, item E.e.a.

# 6.7 Forzamiento climatico ERA5-Land

Para   validar cuantitativamente la hipotesis de que la mortandad de manglar de septiembre 2020
estuvo asociada a la fase La Nina 2020-2021_ se acopla el reanalisis ERAs-Land del Centro Europeo
de Previsiones   Meteorologicas a Plazo Medio ECMWF , Hersbach et al. 2020 como forzante
climatico sobre las series temporales NDVI calculadas en la Fase 2_ La descarga se realiza cOn
cdsapi directamente desde el Climate Data Store, solicitando precipitacion total y temperatura
dos metros sobre Um bounding box que envuelve la CGSM con buffer (11,20 N-10,30 N, 75,05
W-74,05 W) en escala mensual entre 2018 y 20025.

Los datos se reciben en formato NetCDF con convenciones CF y se cargan cOnl xarray open_dataset (chunks=
aplicando u patron de evaluacion perezosa: las dimensiones (time; latitude; longitude) y las
unidades originales metros por dia para precipitacion; kelvin para temperatura se decodifican
automaticamente, y solo se materializa el resultado final con compute () Se calcula la climatologia
mensual sobre el   periodo   disponible la anomalia  respecto esa climatologia, se promedia
espacialmente sobre el AOI acotado se cruza con la anomalia NDVI promediada sobre las ocho
estaciones para diferentes rezagos temporales 0; 1, 2 y 3 meses de modo que se identifique el lag
optimo entre forzante y respuesta del manglar. La descarga del reanalisis ERAS-Land con cdsapi
y el calculo de anomalias mensuales se documentan en el Anero E, item E.3.a:

# 6.8 Validacion cruzada multilingiie con cubo stars en R

Como contraparte local del flujo Python+GEE de la Fase 2, se construye U cubo stars cOn
los   composites   trimestrales Sentinel-2 ya   descargados_ Los TIFs se ordenan   cronologicamente
se ensamblan cOnl read_stars (tifs_ along list(time fechas) proxy TRUE) lo
que   produce UI cubo de tres dimensiones ~X J; time evaluado de manera perezosa hasta
que la   operacion st extract materializa los valores sobre las ocho estaciones de muestreo
INVEMAR. La extraccion devuelve uha serie temporal pOr"   estacion,  que exporta como
series_temporales_stars csv para comparacion contra serie_temporal_ndvi_definitiva _ CSV
~la version producida por reduceRegions en GEE

El proposito de este ejercicio n0 es sustituir el flujo de la nube sino validarlo: si las dos series
coinciden con p > 0,95 y RMSE 0{,}05 unidades NDVI, queda demostrado que la serie temporal
del proyecto no depende del entorno computacional ni de la implementacion. Discrepancias mayores
indicarian sesgos sistematicos diferencias en el enmascaramiento de nubes, en elremuestreo al armar
composite trimestral, en el manejo de pixeles mixtos en la frontera del buffer de extraccion
que conviene reportar como limitacion metodologica. El bloque de construccion del cubo stars en
R y la extraccion sobre las ocho estaciones se documenta en el Anero E, item E.l.c.

# 6.9 Fase 5: Validacion con datos NASA y dashboard

Como componente de validacion cruzada, se integran datos de la Global Flood Database que
registra 16 eventos de inundacion historicos en la CGSM entre 2001 y 2017 y del JRC Global
Surface Water que identifica 977,4 km2 de agua superficial permanente (ocurrencia 50%) en
area de estudio Para el evento de septiembre 2020, se realiza ua deteccion de inundacion

13

mediante Sentinel-1 SAR (banda VH, modo IW), comparando el backscatter medio del periodo
seco de referencia (enero marzo 2020, 49 imagenes) contra el periodo de inundacion (septiembre
octubre 2020, 36 imagenes)_ Se aplica un  umbral de diferencia de 3 dB para inundacion en agua
abierta y se identifica inundacion bajo dosel de manglar mediante valores negativos de diferencia
SAR donde el aumento del backscatter refleja el scattering de doble rebote caracteristico de la
interaccion agua-tronco La deteccion de inundacion Sentinel-1 SAR para el evento de septiembre
2020 se documenta en el Anexo E, item E.3.b

# 6.10 Flujo de datos

# FLUJO DE TRABAJO FASES SECUENCIALES CoN VALIDAcION CRUZADA

This image is a flowchart depicting a data processing and analysis workflow.

**Top Row (Workflow Steps):**

*   **Step 1: Datacube** (Blue rounded rectangle with a '1' icon)
    *   Sentinel-2 + Landsat
    *   geemap · xarray · CF-1.8
    *   Notebooks 01 · 09
    *   An orange arrow points from this step to Step 2.

*   **Step 2: Series + BFAST** (Purple rounded rectangle with a '2' icon)
    *   NDVI mensual · z-score
    *   Python + R · bfast
    *   Notebooks 02 · 02b · 02c
    *   An orange arrow points from this step to Step 3.

*   **Step 3: Segmentación** (Red rounded rectangle with a '3' icon)
    *   SamGeo · 3 RGB S2
    *   Topología DE-9IM
    *   Notebooks 03 · 04b · 04c
    *   An orange arrow points from this step to Step 4.

*   **Step 4: Fragmentación** (Blue rounded rectangle with a '4' icon)
    *   Julia · shoelace
    *   NND · MSI · área
    *   Notebook 04
    *   An orange arrow points from this step to Step 5.

*   **Step 5: Clima · ENSO · SAR** (Green rounded rectangle with a '5' icon)
    *   ERA5 · ONI · CHIRPS
    *   Caudal · S1 SAR serie
    *   07 · 08 · 12
    *   An orange arrow points from this step to Step 6.

*   **Step 6: Validación + RF + DT** (Red rounded rectangle with a '6' icon)
    *   WorldCover · INVEMAR
    *   RF · alertas semáforo
    *   05 · 10 · 11 · alertas

**Middle Section (Unified Outputs):**

*   Below the workflow steps, the text "SALIDAS UNIFICADAS" is centered.
*   Five green rounded rectangles are arranged horizontally below this text, each connected by a light orange diagonal arrow from one of the workflow steps above.

    *   **Output 1:** (Connected from Step 1)
        *   **31 notebooks**
        *   .ipynb numerados · reproducibles

    *   **Output 2:** (Connected from Step 2)
        *   **47 tablas CSV**
        *   Resultados numéricos

    *   **Output 3:** (Connected from Step 3)
        *   **38 figuras PNG**
        *   Mapas · series · correlaciones

    *   **Output 4:** (Connected from Step 4)
        *   **Dashboard 15 capas**
        *   HTML interactivo Leaflet

    *   **Output 5:** (Connected from Step 5)
        *   **Informe Quarto 50+ pp**
        *   PDF reproducible

**Bottom Section (Reproducibility):**

*   Below the unified outputs, a dashed green rounded rectangle contains the text:
    *   **Contenedor Docker sig_unal v1.11 · base reproducible**


Figura 3: Flujo   metodologico del proyecto: seis fases secuenciales con validacion cruzada
entre Python, R Julia, todas   ejecutadas   dentro de U contenedor Docker que   garantiza la
reproducibilidad bit a bit de cada analisis_

A nivel operativo, el siguiente cuadro detalla cada paso del flujo con la herramienta concreta,
lenguaje en que se ejecuta, la entrada que consume y la salida que produce:

# 6.11 Entorno de ejecucion

# Resultados y discusion

# 7.1 Series temporales de NDVI y deteccion de anomalias

El analisis de series temporales de NDVI para las 8 estaciones de monitoreo revelo 18 anomalias
significativas -2) durante el periodo 2013-2025. El evento de septiembre de 2020 se identifico
como la perturbacion de mayor magnitud, COH valores negativos de NDVI en Punta Cerro (-0,078;2 =
-2,46) e Isla Boqueron (-0,018; 2 = -3,36) , coincidente con el inicio de La Nina 2020-2021 que provoco
inundaciones prolongadas en el sistema lagunar_ Un segundo cluster de anomalias se concentro en
marzo de 2018, afectando las estaciones occidentales Caiio Clarin (0,166; z = -3, 15) y CP Aguas
Negras (0,203; -2,50) probablemente asociado a condiciones de hipersalinizacion en epoca
seca . La extension de la serie con Landsat 8 revelo 4 anomalias adicionales en VIPIS durante 2016
=-2,93 en abril) , que no eran visibles con la serie Sentinel-2 sola, demostrando la importancia de
contar con series temporales largas. Las estaciones con mayo1 variabilidad fueron Canio Palos (std
0,143) y Caiio Clarin (std 0,147) , mientras que Punta Chino mostro la menor (std 0,078) ,
lo cual es consistente con SU ubicacion   protegida en el borde suroriental del sistema Con base
en estos hallazgos se seleccionaron tres periodos de referencia para la segmentacion: degradacion

14

Tabla 7: Flujo de datos del pipeline multilenguaje_

# Tabla &:

Paso Herramienta Lenguaje Entrada
1. Adquisicion GEE + geemap Python Sentinel-2 Landsat
2. Series de tiempo pandas + bfast Python R Indices + estaciones
3. Segmentacion SamGeo + umbrales Python Composites RGB
Metricas DataFrames:jl Julia Parches vectoriales
4b. Topologia DE-9IM geopandas + shapely Python Parches en EPSG:9377
Inundacion SAR GEE Sentinel-1 Python SAR VH seco vs humedo
Dashboard geemap Python Todas las capas
Forzamiento ERA5 cdsapi Xarray Python NetCDF ERA5-Land
Cubo stars stars + sf TIFs trimestrales S2
Validacion multilingue pandas Python Series Python + R
10_ RF benchmark GEE smileRandonForest Python Sentinel-2 + INVEMAR WorldCover

Tabla &: (Continued)

Paso Herramienta Lenguaje Entrada
11. SAR continuo VH GEE Sentinel-1 pandas Python Sentinel-1 GRD 2018 2025
12. Alertas tempranas pandas + matplotlib Python Series NDVI + SAR + bfast

Tabla 9: Entorno de ejecucion del proyecto.

# Tabla 10:

Componente Especificacion
Contenedor Docker sig unal vl.IL (Ubuntu + RStudio Server)
Python 3.12.3 + geemap, samgeo, leafinap, rasterio, geopandas
43.3 terra, sf, tidyverse, bfast, tmap
Julia 1.11.3 + DataFrames, CSV GeoJSON, Statistics
Quarto 1.4.550 (informe reproducible)
Control de versiones Git + GitHub
Geocomputacion en la nube Google Earth Engine (API Python)

15

Tabla Il: Anomalias significativas de NDVI (z < -2) en la serie combinada 2013-2025_

Tabla 12:

Estacion Fecha NDVI Z-score Sensor
Isla Boqueron 2020-09 -0,018 -3,36 Sentinel-2
Caiio Clarin 2018-03 0,166 -3,15 Sentinel-2
VIPIS 2016-04 -0,291 2,93 Landsat 8
Caiio Clarin 2025-03 0,223 2,77 Sentinel-2
Caio Palos 2024-09 0,272 2,66 Sentinel-2
CP Pajarales 2018-03 0,203 2,50 Sentinel-2
Punta Cerro 2020-09 -0,078 -2,46 Sentinel-2
CP Pajarales 2022-09 0,217 2,40 Sentinel-2

(julio-diciembre 2020) , recuperacion (enero-junio 2022) y estado actual (julio 2024 junio 2025)_
La definicion de estos tres bloques temporales obedece a una logica de muestreo de estados estables
del sistema antes que a ua serie continua: cada periodo cubre una  ventana de seis a doce meses
elegida para representar una fase fenologica caracteristica posterior a la disipacion de la perturbacion
previa, de modo que el composite resultante refleja un estado estructural n0 un transitorio. El
periodo actual" cubre UI unico ano hidrologico (julio 2024 junio 2025 , en lugar de U horizonte
mas amplio porque la ventana se selecciono para capturar el estado vigente del sistema al cierre del
proyecto sin contaminar el composite cOn eventos La Nina 2023-2024 que afectaron parcialmente
al Caribe colombiano; en consecuencia; los resultados sobre este periodo deben interpretarse cOmo
U snapshot del estado actual nO como una  tendencia  anualizada, coherente con la logica de
Bunting et al. (2022) , quienes trabajan con epocas discretas y no con series temporales continuas
para reportar extension de manglar_

La construccion del datacube trimestral CF-1.8 sobre el AOI acotado ver tabla tabla 5 permite;
ademas, calcular una serie temporal del NDVI mediano restringida a los pixeles que superan
umbral de manglar (NDVI > 0,4) , de modo que la dinamica observada deja de estar diluida por
agua, las salinas y los arenales que tambien ocupan el poligono. El resultado; presentado en la figura
figura 4, confirma el patron ya identificado en las estaciones individuales pues el NDVI mediaio
del manglar oscila alrededor de 0,80 en condiciones normales, cae a valores cercaiios a 0,60 entre
segundo semestre de 2019 y el primer semestre de 2020 coincidiendo con la sequia precursora
y el inicio del episodio La Nitia 2020-2021 y vuelve a estabilizarse en torno a 0,80 desde 2022
en adelante; de esta manera la serie temporal espacializada sostiene el mismo argumento que las
series puntuales de las ocho estaciones pero sobre la totalidad de la cobertura de manglar del AOI
acotado.

# 7.2 Analisis bfast (serie combinada 2013-2025)

La aplicacion de bfast sobre las series  mensuales de NDVI combinadas Landsat Sentinel-2
(2013-2025, 12 aiios) detecto quiebres estructurales en de las 8 estaciones con h 0,15 y en las
estaciones cOnl 0,10. Este resultado contrasta COn el analisis previo basado unicamente en

16

Serie temporal NDVI del manglar sobre AOl acotado (SFF VPI), 2018-2025

This is a line chart titled "NDVI mediano del manglar" (Median NDVI of the mangrove).
The x-axis is labeled "Trimestre" (Quarter) and ranges from 2018 to 2026.
The y-axis is labeled "NDVI mediano del manglar" and ranges from 0.50 to 0.90.

The chart displays a single line in dark green with circular markers, representing the "Actual (2024-2025)" data.
The line shows the following approximate values:
- 2018: ~0.75
- 2019: ~0.81, ~0.75, ~0.64
- 2020: ~0.80, ~0.76, ~0.75, ~0.60
- 2021: ~0.76, ~0.82, ~0.75
- 2022: ~0.80, ~0.85, ~0.77, ~0.74
- 2023: ~0.80, ~0.76, ~0.75, ~0.83
- 2024: ~0.83, ~0.78, ~0.73
- 2025: ~0.84, ~0.86, ~0.83, ~0.79
- 2026: ~0.82, ~0.84

There are three shaded vertical regions:
- A light red shaded region labeled "Degradación (2020 H2)" covers the second half of 2020 and the first half of 2021.
- A light orange shaded region labeled "Recuperación (2022 H1)" covers the first half of 2022.
- A light green shaded region labeled "Actual (2024-2025)" covers the years 2024 and 2025.

A dashed red line labeled "Umbral manglar (0.4)" is present at y=0.40, but it is outside the visible range of the y-axis (0.50-0.90).


Figura 4: Serie temporal del NDVI mediano del manglar sobre AOI acotado (SFF CGSM + VPI
Salamanca, 835 km? entre 2018 y 2025, calculada a partir del datacube trimestral CF-1.8 restringida
pixeles con NDVI 0,45 Las franjas sombreadas marcan los tres periodos de referencia de la
segmentacion; la caida de 2019-2020 coincide con la sequia y el episodio La Niia que sostienen la
narrativa del informe.

Sentinel-2 (2018-2025, aiios) , que no detecto quiebres en ninguna estacion; lo cual demuestra
la importancia de contar COn series temporales suficientemente largas para la deteccion de cambios
estructurales con bfast. El patron dominante es Un quiebre generalizado en 2016 ~detectado en 7 de
8 estaciones entre abril y diciembre de ese ano coincidente con el evento El Nino 2015-2016, uno de
los mas intensos registrados, que provoco sequias prolongadas y estres hidrico en el sistema lagunar_
La estacion Punta Cerro fue la mas inestable, con quiebres detectados (h 0,10): noviembre de
2016 (El Nino) , abril de 2020 (inicio de La Niiia) agosto de 2021 (recuperacion post-La Niiia)
capturando los dos eventos climaticos mas importantes del periodo de estudio. VIPIS presento U
segundo quiebre en 2022, posiblemente asociado la recuperacion post-La Nina 2020-2021_

# 7.3 Analisis bfast unificado sobre las cuatro estaciones de manglar real (2018
2025)

El analisis bfast presentado en la tabla tabla 13 se calcula sobre las ocho estaciones de muestreo
originales del proyecto, las cuales incluyen tanto estaciones que monitorean cobertura de manglar
denso como estaciones limnologicas ubicadas sobre la lamina de agua del complejo lagunar central.
La clasificacion introducida en la tabla tabla 21 demuestra que esas dos naturalezas espectrales
responden forzantes climaticos con signos opuestos ver tabla tabla 23 J; por consiguiente; la
aplicacion de bfast sobre el promedio de las ocho estaciones puede diluir la firma del evento climatico
sobre el dosel forestal. Para refinar la atribucion del episodio La Niiia 2020-2021 sobre el manglar;
se re-ejecuta bfast  restringiendolo a las cuatro estaciones que efectivamente miden cobertura de
manglar denso Caio Palos, Cazio Clarin; CP Aguas Negras y CP Luna en este sentido la tabla
tabla 15 reporta el resultado de esta evaluacion_

El analisis unificado confirma cuantitativamente la hipotesis central del informe sobre la atribucion
del evento humanitario de septiembre 2020 al forzamiento La Niiia, pues bfast detecta quiebres
estructurales en febrero y diciembre de 2020 sobre Caiio Clarin en junio de 2020 sobre Cano
Palos las dos estaciones del Complejo de Pajarales con mayor exposicion a la entrada del flujo del
rio Magdalena en tanto que CP Aguas Negras y CP Luna presentan quiebres en enero y abril

17

Tabla 13: Quiebres estructurales detectados por bfast en la serie NDVI combinada (2013-2025) .

Tabla 14:

Estacion Quiebres (h=0,15) Fecha principal Quiebres (h=0,10) Evento asociado
CP Pajarales 2016-10 El Nitio 2015-2016
Caiio Clarin 2016-09 El Nitio 2015-2016
Caiio Palos 2015-06 error El Nirio (inicio)
Isla Boqueron 2016-04, 2018-05 El Niiio + transicion
Punta Cerro 2016-11 El Niiio + La Niiia + recup
Punta Chino 2016-05 El Niiio 2015-2016
Rio Sevilla 2016-12 El Nirio 2015-2016
VIPIS 2016-04, 2022-03 El Niiio + recuperacion

Tabla 15: Quiebres estructurales detectados por bfast sobre las cuatro estaciones de manglar real,
periodo 2018-2025 Sentinel-2 unicamente). Los quiebres se agrupan en tres bloques temporales
coincidentes COn eventos ENSO documentados en la seccion de forzamiento climatico_

# Tabla 16:

Estacion Quiebre 2020 La Nina) Quiebre 2022 Recuperacion) Quiebre 2023 2025
Caiio Palos 2020-06 2024-06

# Tabla 16: Continued)

Estacion Quiebre 2020 'La Nina) Quiebre 2022 Recuperacion) Quiebre 2023 2025
Caiio Clarin 2020-02, 2020-12 2021-04 2023-08, 2024-05, 2025-0

Tabla 16: Continued)

Estacion Quiebre 2020 La Nina) Quiebre 2022 Recuperacion) Quiebre 2023 2025
CP Aguas Negras 2022-04 2023-10

Tabla 16: Continued)

Estacion Quiebre 2020 (La Nina) Quiebre 2022 Recuperacion) Quiebre 2023 2025
CP Luna 2022-01 2024-06

18

de 2022 que corresponden exactamente al periodo de recuperacion definido en la fase 2, lo cual es
coherente con que INVEMAR (2024) documenta que la regeneracion natural en Aguas Negras se
ve afectada por la entrada excesiva de agua dulce y sedimentos. Adicionalmente, el analisis revela
U tercer bloque de quiebres entre agosto de 2023 y junio de 2024 que coincide con el episodio El
Niio 2023 2024 visible en la serie ONI ver figura figura 5 y que el analisis previo sobre las ocho
estaciones no habia evidenciado, asi la unificacion subconjunto de manglar denso no solo refina
la deteccion del evento 2020 sino que extiende la trazabilidad de la respuesta del manglar la fase
ENSO opuesta. La diferencia metodologica entre los dos analisis ocho estaciones heterogeneas VS
cuatro estaciones de manglar denso ilustra la pertinencia de clasificar las estaciones pOr naturaleza
espectral antes de cualquier analisis de quiebres estructurales sobre series multitemporales_

# 7.4 Segmentacion y dinamica de cobertura sobre el AOI acotado

La segmentacion con SamGeo (vit b, 30 m) sobre los composites RGB recortados al AOI acotado
constituye la fuente principal de los resultados de cobertura y fragmentacion reportados en este
estudio. Una iteracion anterior del proyecto opero sobre el AOI envolvente (5.073 km? antes del
acotamiento al area protegida oficial; Sus cifras mantienen lnicamente en el repositorio Git de
trazabilidad y no se utilizan para sostener las conclusiones del estudio. La decision metodologica de
reportar resultados sobre el AOI acotado obedece que la inclusion de vegetacion riberana, salitral
Y zonas agropecuarias en el AOI envolvente inflaba sistematicamente las cifras de manglar potencial
comprometia la comparabilidad con la cartografia oficial de manglares de Colombia (INVEMAR,
2020) y con el Global Mangrove Watch Bunting et al,, 2022) , referencias que tambien se acotan al
humedal propiamente dicho.

# 7.5 Recalculo en EPSG:9377 y analisis topologico de parches

La reproyeccion de los GeoJSON al sistema oficial colombiano y la consecuente sustitucion de la
aproximacion esferica pOr el calculo directo del area en  metros  redefine las cifras de cobertura
por periodo, de modo que las hectareas reportadas continuacion corresponden ua proyeccion
equivalente y son comparables con la cartografia base del IGAC Sobre el AOI acotado, las metricas
de fragmentacion reportadas en la tabla tabla 17 describen una secuencia de contraccion de area
clasificada con simultanea consolidacion estructural: el numero de parches en el rango filtrado
5.000 ha disminuye de 79 en el periodo de degradacion a 38 en el de recuperacion y a 15 en el actual,
en tanto que el area total clasificada como manglar pasa de 12.425,6 a 8.650,8 y 4.037,0 hectareas
en los mismos cortes El area media de parche, en contraste, crece de 157,3 269,1 hectareas, de
esta manera los parches sobrevivientes son mas grandes pero menos numerosos; asi el paisaje se
reorganiza alrededor de unidades de manglar maduro mientras los parches pequenos degradados
quedan por fuera del umbral espectral aplicado por la clasificacion. Esta lectura se complementa cOn
el indice de forma medio (MSI) que pasa de 0,51 a 1,46 bordes progresivamente mas irregulares
consistentes con regeneracion natural no uniforme con la distancia media al vecino mas cercano
que aumenta de 1,10 a 2,39 km; evidenciando un aislamiento creciente de los parches sobrevivientes_

Antes de interpretar las cifras conviene aclarar el alcance temporal de cada periodo de referencia
la degradacion corresponde al semestre julio-diciembre de 2020 y captura la respuesta espectral
del manglar durante el evento humanitario de mortandad asociado La Ninia; la recuperacion
corresponde al semestre enero-junio de 2022 captura la fase de   regeneracion temprana
documentada por INVEMAR (2024); el periodo actual corresponde al ciclo anual julio 2024
junio 2025 y constituye UI snapshot del estado mas reciente disponible al momento de la entrega;
no una tendencia post-recuperacion estabilizada. La comparacion entre los tres periodos debe leerse,

19

Tabla 17: Metricas de fragmentacion sobre AOI acotado (SFF CGSM + VPI Salamanca, 835 km2) ,
calculadas en EPSG:9377 . Los parches estan filtrados al rango 1-5.000 ha y procesados en Julia
descomponiendo MultiPolygons

Tabla 18:

Periodo Parches Julia) Area total (ha) Area media (ha) MSI medio NND
Degradacion (2020-82) 79 12.425,6 157,3 0,51 1,10
Recuperacion (2022-S1) 38 8.650,8 227,7 1,01 1,99
Actual (2024-2025) 15 4.037,0 269,1 1,46 2,39

por lo tanto, como uhla secuencia de tres estados puntuales y n0 como Um analisis de tendencia, en
la medida en que se requieren al menos dos ciclos anuales adicionales 2025-2026 y 2026-2027
para evaluar si el patron observado en 2024-2025 corresponde uhla contraccion estable ua
fluctuacion intermedia _ Esta consideracion metodologica matiza las inferencias sobre cambio neto
que se discuten continuacion.

Conviene precisar que la contraccion del area clasificada por  umbrales nO equivale, pOr si sola,
perdida de cobertura del manglar; en efecto, la figura figura ~calculada directamente sobre
el datacube trimestral CF-1.8 como diferencia de NDVI mediano entre el periodo actual y el de
degradacion muestra que la mayor parte del AOI acotado presenta tonos   azules consistentes
con ganancia de vigor vegetativo sobre los parches sobrevivientes, mientras los tonos rojos se
concentran en los bordes hipersalinos del Via Parque y en sectores puntuales del Santuario asociados
a las lagunas internas_ Ambos hallazgos son compatibles: el manglar se consolida en menos parches
pero mas densos espectralmente; asi la metrica de area filtrada subestima la dinamica del ecosistema
cuando se interpreta de forma aislada, en este sentido se justifica reportar de manera conjunta las
metricas de fragmentacion; las series temporales y el mapa de cambio NDVI, pues los tres se sostienen
mutuamente.

El analisis topologico complementa estas cifras con dos lecturas adicionales sobre los mismos parches_
La aplicacion del predicado intersects entre cada parche y la frontera del AOI con una tolerancia
de 30 metros  identifico ua proporcion variable de parches truncados por' el borde del area de
estudio: 24,0 % en el periodo de degradacion equivalentes 2.238,1 ha 7,5 % en el periodo de
recuperacion -1.640,0 ha y 18,3 % en el periodo actual 2.076,2 ha Esta diferencia sugiere
que los parches del periodo de recuperacion estan mas agrupados al interior del sistema lagunar;
mientras que los de degradacion y los actuales se extienden hasta el limite cartografico del AOI, de
modo que SUs metricas de fragmentacion globales reflejan tambien el efecto del recorte. La aplicacion
del predicado contains con los ocho puntos de monitoreo no devolvio parches que envolvieran las
estaciones bajo el filtro de tamano 1-5.000 ha , lo cual se explica porque las estaciones INVEMAR
estan ubicadas sobre cuerpos de agua 0 en bordes inmediatos al manglar , donde la segmentacion
devuelve parches menores a 1 ha 0 el agua misma; la representatividad espacial de las estaciones;
en consecuencia, debe discutirse en escalas de buffer y no de contenencia estricta.

El analisis topologico sobre el AOI acotado muestra ua proporcion creciente de parches truncados
por'  el limite del area protegida, que pasa del 35,3 en 2020 al 53,3 % en 2024-2025 Esta
tendencia es coherente COH patron de contraccion documentado en la fragmentacion: medida

20

Tabla 19: Parches  de  manglar  truncados pOr"  la  frontera   del AOI acotado  (predicado DE-9IM
intersects con tolerancia de 30 m). Los parches se cuentan agregados como features completos en
geopandas_

# Tabla 20:

Periodo Parches Parches en borde % en borde Area en borde (ha)
Degradacion 2020-52) 17 35,3 5.104,3

Tabla 20: (Continued)

Continued on next page

Periodo Parches Parches en borde % en borde Area en borde (ha)
Recuperacion (2022-S1) 17 47,1 8.325,

Tabla 20: (Continued)

Continued on next page

Periodo Parches Parches en borde % en borde Area en borde (ha
Actual (2024-2025) 15 53,3 5.237,9

que los parches centrales del sistema lagunar desaparecen pierden cobertura espectral suficiente,
los parches sobrevivientes se concentran en posiciones perifericas del Santuario de Fauna y Flora y
del Via Parque, donde el limite legal de proteccion se acerca la franja costera la frontera cOn
zonas agropecuarias_ La ausencia total de estaciones de muestreo INVEMAR dentro de parches
segmentados mayores ua hectarea ~predicado DE-9IM contains confirma  la observacion
metodologica de la seccion anterior: las cuatro estaciones limnologicas originales estan ubicadas
sobre   cuerpos de agua, n0 sobre   manglar   denso, las   cuatro estaciones de   manglar real se
encuentran en pixeles de borde donde la segmentacion automatica produce parches inferiores al
umbral de filtrado

# 7.6 Comparacion dinamica dentro y fuera del area protegida

Una   observacion  metodologica importante surge al CrUar las ocho estaciones de muestreo cOn
el AOI acotado (SFF CGSM VPI Salamanca, 835,3 km2): solo Cano_ Palos cae estrictamente
dentro del area protegida, mientras que Cano Clarin y Rio Sevilla   quedan asociadas mediante
buffer de dos kilometros, y las cinco restantes quedan fuera. Esta distribucion espacial n0 UII
error de seleccion sino una caracteristica de las estaciones INVEMAR-GBIF originales, las cuales
fueron disenadas como puntos de monitoreo limnologico calidad de agua, estructura del cuerpo
lagunar y pOr tanto se ubican sobre la lamina de agua del sistema, no sobre el manglar_ Esto
se confirma al observar el NDVI mediano historico (2013-2025): las cuatro estaciones del costado
oriental Isla Boqueron, Punta Cerro, Punta Chino y Rio Sevilla presentan NDVI mediaiios
entre 0,14 y 0,28, valores compatibles con superficies de agua 0 transicion agua-borde; mientras que
las cuatro estaciones sobre manglar Caiio Palos , Caiio Clarin, CP Aguas Negras y CP Luna
presentan NDVI medianos entre 0,38 y 0,75, consistentes cOn cobertura vegetal densa.

Esta   diferenciacion   permite reorganizar la lectura de los resultados de la Fase 2 en  dos grupos
comparables. Las anomalias   negativas detectadas en septiembre 2020 sobre las estaciones

21

Tabla 21: Clasificacion de las ocho estaciones de muestreo por naturaleza espectral y distancia al
AOI

# Tabla 22:

Naturaleza Estaciones NDVI mediano Distancia me
Manglar Cano Palos , Cano_ Clarin, CP Aguas_Negras, CP Luna 0,59 1,9 km
Limnologica Isla Boqueron; Punta Cerro, Punta Chino, Rio Sevilla 0,21 4,2 km

limnologicas NDVI -0,078 en Punta   Cerro, NDVI -0,018 en Isla   Boqueron reflejan
principalmente la respuesta del cuerpo de agua al exceso hidrico y al arrastre de sedimentos, n0
necesariamente mortalidad de manglar En contraste, las anomalias detectadas en las estaciones
de manglar CP Aguas Negras con 2 = 22,50, Caiio Clarin con 2 -3,15 representan estres real
del dosel vegetal y son las que efectivamente miden el efecto de La Niiia sobre la cobertura. Este
reordenamiento conceptual refuerza el argumento de que la mortandad de septiembre 2020 fue mas
severa de lo que sugiere la lectura uniforme de las ocho estaciones pues el evento se concentro en
las que realmente capturan dinamica de manglar y no en las que dominan el agua superficial.

# 7.7 Acoplamiento ERAs-Land y discusion del forzante La Nina

El cruce entre las anomalias mensuales de precipitacion y temperatura ERA5-Land y las anomalias
NDVI promediadas sobre las ocho estaciones arrojo correlaciones debiles e indistinguibles de cero
con valores absolutos |pl 0,12 para todos los rezagos entre cero y tres meses lo que sugiere
primera vista que el forzante climatico local n0 explica directamente la dinamica del manglar de
la CGSM. Sin embargo, este resultado agregado oculta una asimetria importante que solo aparece
al desagregar las ocho estaciones segun la clasificacion por naturaleza espectral introducida en la
seccion anterior: las cuatro estaciones de manglar y las cuatro limnologicas responden al mismo
forzante climatico con signos opuestos, de modo que el promedio de las ocho cancela mutuamente
las dos seiiales.

En las cuatro estaciones que efectivamente miden cobertura de manglar Caiio Palos, Caio Clarin,
CP Aguas Negras y CP Luna la correlacion entre la anomalia de precipitacion ERA5-Land
Z-score NDVI CcOn rezago de dos meses es   de ~0,123, valor  debil pero consistente cOn
la hipotesis   original de La Niiia como forzante de mortandad: precipitacion anomalamente alta
induce inundacion prolongada hipoxia en el sistema radicular. COH caida posterior del NDVI: La
temperatura presenta una correlacion analoga en rezago de tres meses pT2m 0,087 que refuerza
el patron sin alcanzar significancia estadistica individual En las cuatro estaciones limnologicas Isla
Boqueron, Punta Cerro, Punta Chino; Rio Sevilla en cambio, la precipitacion anomala se asocia
positivamente con el z-score NDVI con rezago de dos meses (p +0,292) y la temperatura se asocia
negativamente con rezago de tres meses (prem. ~0,201). Este patron; fisicamente coherente; refleja
la respuesta del cuerpo de agua al exceso hidrico: la Iluvia anomala arrastra sedimentos y nutrientes
desde las cuencas altas que estimulan floraciones de fitoplancton y vegetacion acuatica efimera en
bordes; lo que aumenta temporalmente la senal NDVI sobre los pixeles dominados pOr agua.

Tres consideraciones permiten interpretal esta evidencia de manera prudente En primer lugar; la
resolucion espacial de ERAs-Land nueve kilometros nominales _ promedia el campo de precipitacion

22

Tabla 23: Correlacion entre anomalias climaticas ERAS-Land NDVI z-score, desagregada por
naturaleza espectral de las estaciones de muestreo

Tabla 24:

Naturaleza Rezago (meses) precip vs NDVI z T2m vs NDVI
Manglar 0,081 +0,022 86

Tabla 24: (Continued)

Continued 0n next page

Naturaleza Rezago (meses) precip vs NDVI T2m vs NDVI
Manglar 0,081 +0,040 85

Continued on next page

Tabla 24: (Continued)

Naturaleza Rezago (meses) precip vs NDVI z T2m vs NDVI z
Manglar -0,123 -0,018

Continued 0n next page

Tabla 24: (Continued)

Naturaleza Rezago (meses) precip vs NDVI z T2m vs NDVI z
Manglar 0,020 0,087 83

Tabla 24: (Continued)

Continued on next page

Naturaleza Rezago (meses) 0 precip vs NDVI T2m vs NDVI
Limnologica +0,082 -0,173 72

Tabla 24: Continued)

Continued 0n next page

Naturaleza Rezago (meses) precip vs NDVI z T2m vs NDVI
Limnologica +0,108 0,149

Continued 0n next page

Tabla 24: (Continued)

Naturaleza Rezago (meses) precip vs NDVI z T2m vs NDVI z
Limnologica +0,292 0,144 70

Tabla 24: (Continued)

Continued on next page

Naturaleza Rezago (meses) precip vs NDVI z T2m vs NDVI z
Limnologica +0,271 0,201 69

23

sobre una zona que excede la escala caracteristica del sistema lagunar y, pOr tanto, no captura
microclimas locales que   probablemente median la respuesta del manglar: En segundo lugar,
mecanismo causal real de la mortandad de septiembre 2020 n0 es necesariamente la lluvia caida
sobre la CGSM, sino el incremento de caudal aportado pOr el rio Magdalena ~Y secundariamente
por los rios Sevilla, Aracataca y Fundacion que  viene de cuencas altas en la Sierra Nevada de
Santa Marta, donde la lluvia La Niia si fue copiosa; el insumo apropiado para validar esa cadena
causal serian las series mensuales de caudal del IDEAM no las anomalias ERA5-Land sobre
el pixel del humedal: En tercer lugar; el contraste de signos opuestos entre manglar y estaciones
limnologicas constituye en si mismo Uil hallazgo metodologico relevante: confirma que el promedio
de las ocho estaciones aplicado en la version preliminar del proyecto enmascara una   senal real
en el subconjunto de estaciones que monitorea cobertura vegetal, justifica retrospectivamente la
decision metodologica de clasificar las estaciones pOr naturaleza espectral antes de cualquier analisis
de correlacion:

# 7.8 Forzamiento climatico global ENSO (ONI y SOI de NOAA)

La descarga directa de los indices ENSO mensuales del Climate Prediction Center de la NOAA
Oceanic Niiio Index ONI) basado en la anomalia de temperatura superficial del Pacifico ecuatorial
3.4 y el Southern Oscillation Index (SOI) basado en el gradiente de presion Tahiti-Darwin permite
complementar el forzamiento ERA5-Land local con uhla medida directa del estado de la oscilacion
del Pacifico, asimismo se evita el promediado espacial sobre el AOI que limitaba el analisis previo_
La figura figura 5 presenta la evolucion conjunta de ambos indices sobre el periodo del proyecto y
deja ver con claridad el evento El Nitio 2015 2016 ONI maximo de +2,75 y SOI minimo de 3,6,
valores extremos del registro y el episodio La Niza 2020-2022 que sostuvo ONI entre 0,5 y -1,2
durante casi dos aios, en el cual se ubica el evento de mortandad del manglar de septiembre 2020
que sostiene la narrativa del informe:

indices ENSO (ONI SOi, NOAA) sobre periodo del proyecto 2013-2025

**Título:** Índices ENSO (ONI y SOI, NOAA) sobre el periodo del proyecto, 2013-2023

**Tipo de gráfico:** Gráfico de líneas con áreas sombreadas.

**Eje X:** Años, de 2014 a 2026, con marcas cada dos años.

**Eje Y:** Índice ENSO (estandarizado), de -4 a 4, con marcas cada unidad.

**Líneas:**
*   **ONI (NOAA CPC):** Línea roja, más suave, representando el Índice Oceánico de El Niño.
*   **SOI estandarizado:** Línea azul, más irregular, representando el Índice de Oscilación del Sur estandarizado.

**Áreas sombreadas:**
*   **El Niño 2015-2016:** Área sombreada en rojo claro, aproximadamente desde finales de 2014 hasta principios de 2016.
*   **La Niña 2020-2022:** Área sombreada en azul claro, aproximadamente desde finales de 2020 hasta principios de 2023.

**Descripción de las líneas y áreas:**

La línea roja (ONI) muestra una tendencia general de fluctuación alrededor de 0. Se observa un pico significativo de El Niño en 2015-2016, donde el índice supera 2.5. Posteriormente, hay un período de valores negativos, indicando La Niña, especialmente pronunciado en 2020-2022, con valores por debajo de -1.5. Hacia el final del período, la línea roja muestra un aumento, sugiriendo un posible retorno a condiciones de El Niño.

La línea azul (SOI estandarizado) es mucho más volátil, con picos y valles frecuentes. Durante el evento de El Niño 2015-2016 (área roja), el SOI muestra valores predominantemente negativos, con un valle profundo por debajo de -3. Durante el evento de La Niña 2020-2022 (área azul), el SOI muestra valores predominantemente positivos, con varios picos por encima de 2.

Las áreas sombreadas resaltan los períodos de El Niño y La Niña, que corresponden a los valores extremos de ONI y SOI.


Fecha

Figura 5: Indices ENSO mensuales (ONI SOI, Climate Prediction Center de la NOAA)
sobre el periodo del proyecto 2013-2025. Las franjas sombreadas marcan los dos eventos ENSO
documentados: El Nino 2015-2016 que sostiene los quiebres bfast del periodo medio del analisis y
La Niiia 2020-2022 que sostiene la mortandad del manglar de septiembre 2020_

La correlacion de Pearson entre ambos indices y las anomalias NDVI promediadas pO naturaleza
espectral segin la clasificacion introducida en la seccion anterior arroja UIl patron debil pero

24

Tabla 25: Correlacion de Pearson entre indices ENSO globales  (ONI SOI de NOAA) y NDVI
Z-score desagregada por naturaleza espectral de las estaciones de muestreo.

Tabla 26:

Naturaleza Rezago (meses) PONI PsOI
Manglar +0,027 +0,143 86
Manglar ~0,007 +0,198 85
Manglar 0,039 +0,146 84
Manglar ~0,070 +0,058 83
Limnologica 0,121 +0,201 72
Limnologica 0,089 +0,120
Limnologica 0,054 +0,135 70
Limnologica 0,014 +0,153 69

consistente en signo, presentado en la tabla tabla 25. El SOI emerge como mejor predictor que
ONI para ambos grupos de estaciones, con PsO1 entre +0,12 y +0,20 a traves de los cuatro rezagos
evaluados; sobre las estaciones de manglar la correlacion con ONI evoluciona de +0,027 en el rezago
cero hacia 0,070 en el rezago de tres meses; en tanto que sobre las estaciones limnologicas pONI es
negativa en todos los rezagos con U maximo absoluto de -0,121 sin rezago.

Correlacion entre indices ENSO globales anomalias NDVI por naturaleza espectral, 2013-2025

### Naturaleza: manglar

This is a grouped bar chart showing the Pearson correlation coefficient (ρ) between ENSO indices (ONI and SOI) and NDVI z-score, across different lag times (Rezago).

**Y-axis:** ρ (Pearson) — ENSO vs NDVI z-score, ranging from -0.10 to 0.20.
**X-axis:** Rezago (meses), with values 0, 1, 2, and 3.
**Legend:**
*   Red bars: ONI
*   Blue bars: SOI

**Data:**

| Rezago (meses) | ONI (ρ) | SOI (ρ) |
| :------------- | :------ | :------ |
| 0              | 0.025   | 0.145   |
| 1              | -0.005  | 0.200   |
| 2              | -0.040  | 0.145   |
| 3              | -0.070  | 0.060   |


### Naturaleza: limnologica

| Rezago (meses) | ONI | SOI |
|---|---|---|
| 0 | -1.5 | 1.5 |
| 1 | -1.0 | 1.0 |
| 2 | -0.5 | 1.2 |
| 3 | -0.2 | 1.3 |


Figura 6: Correlacion entre los indices ENSO globales (ONI en rojo, SOI en azul) y las anomalias
NDVI z-score, desagregada pOr naturaleza espectral de las estaciones, para rezagos de cero tres
meses

Conviene contrastar estos   resultados con las correlaciones ERA5-Land reportadas en la seccion
anterior, pues los signos  parecen oponerse: sobre manglar la  precipitacion ERA5-Land   local
correlaciona negativamente COH el NDVI Pprecip ~0.123 en rezago de dos meses) mientras que el
SOI cuya fase positiva indica condiciones La Nina con mayor precipitacion regional correlaciona

25

positivamente Con el NDVI del mismo grupo de estaciones (Pso1 +0,146 en rezago de dos meses)
Esta aparente contradiccion no debe leerse como inconsistencia metodologica sino como evidencia
del caracter no lineal de la respuesta del manglar al forzamiento climatico, en la medida en que
el ENSO global captura el estado de fondo de la oscilacion del Pacifico que organiza el regimen
hidrico regional y favorece el vigor inicial de la vegetacion cuando la fase es positiva mientras
la precipitacion ERA5-Land sobre el pixel del humedal captura la intensidad puntual del aporte
hidrico, asi eventos de Iluvia copiosa y prolongada se asocian con inundacion bajo dosel hipoxia
que si afectan negativamente el dosel. Ambos forzantes, en este sentido, son complementarios y n0
excluyentes; y la magnitud debil de las correlaciones individuales ~lel < 0,25 en todos los casos
confirma que la cadena causal La Nitia caudal fluvial inundacion prolongada mortandad
opera traves de variables intermedias no capturadas directamente por ninguno de los dos forzantes
climaticos; lo que ratifica la pertinencia de complementar el analisis con series de caudal del IDEAM
con indices de oleaje del Caribe colombiano en trabajo futuro.

# 7.9 Acoplamiento con el caudal de las cuencas aportantes (IDEAM-DHIME)

Para cerrar la  cadena causal La Nina caudal  fluvial inundacion   lagunar mortandad
del   manglar con datos   oficiales   colombiaiios, se   descargan del  portal DHIME del IDEAM las
series de caudal medio mensual del rio Magdalena en la estacion El Banco (codigo 25027020 ,
144 observaciones continuas 2013 2025 , del rio Aracataca en   la estacion Ganaderia Caribe
(codigo 29067150, 130 observaciones 2013-2025) , asimismo las dos estaciones cubren las dos vias
hidrologicas independientes que alimentan el sistema CGSM: la entrada central a traves de los
canales rehabilitados Caiio Clarin, Aguas Negras y Renegado, y la entrada oriental desde la Sierra
Nevada de Santa Marta. La seleccion de la variable caudal medio mensual en lugar del caudal
maximo mensual tambien disponible obedece a la coherencia metodologica entre las dos cuencas
y al hecho de que el regimen hidrologico sostenido representa mejor la dinamica de fondo que los
pulsos extremos puntuales_ Las dos series se  estandarizan por Z-score  mensual se cruzan con
las anomalias NDVI desagregadas segin la naturaleza  espectral de las estaciones, replicando la
metodologia de las secciones ERAs-Land y ENSO.

El resultado obliga matizar la version simple de la cadena causal planteada inicialmente
en la medida en que todas las correlaciones entre caudal y NDVI tanto para las estaciones de
manglar como para las limnologicas resultan positivas con magnitud absoluta entre 0,04 y 0,27
La correlacion positiva mas alta corresponde a El Banco con manglar a tres meses de rezago
+0,256, n 71) Ganaderia Caribe COn manglar U mes de rezago +0,224, 67) ,
valores que indican un acoplamiento debil pero consistente entre el caudal de las cuencas aportantes
y el vigor del dosel del manglar de la CGSM en sentido directo, esto es, mayor caudal sostenido
se asocia con NDVI mas alto n0 con   estres del manglar como sugiere la lectura ingenua
del evento de septiembre 2020. Este resultado es coherente con la ecologia hidrologica del manglar
de la CGSM, en la cual el aporte sostenido de agua dulce desde la cuenca alta del Magdalena
rehabilitado por la reapertura de canales entre 1996 1998 contrarresta la hipersalinizacion
cronica que constituye el principal estresor historico del sistema (INVEMAR, 2024). Adicionalmente;
los meses con anomalias de caudal extremas >+2) se concentran en 2022 ~agosto y septiembre
en EL Banco, abril, septiembre y diciembre en Ganaderia Caribe HO en septiembre de 2020,
de esta manera el pico fluvial del periodo La Niia 2020-2022 ocurrio de manera tardia sobre las
cuencas aportantes; despues del evento de mortandad documentado en el sistema lagunar_

La reformulacion operativa de la cadena causal que estos datos obligan adoptar es la siguiente:
Primero, el episodio La Niiia   2020-2021 induce Uil regimen prolongado de mayor  precipitacion

26

Tabla 27: Correlacion de Pearson entre anomalia de caudal IDEAM y NDVI z-score, desagregada
pOr estacion hidrologica, naturaleza espectral del sitio de monitoreo y rezago temporal:

# Tabla 28:

Estacion Naturaleza Rezago meses) Pcaudal
El Banco (Magdalena) Manglar +0,064 74
El Banco (Magdalena) Manglar +0,039 73
El Banco (Magdalena) Manglar +0,108 72
El Banco (Magdalena) Manglar +0,256 71
El Banco (Magdalena) Limnologica +0,181 61
El Banco (Magdalena) Limnologica +0,233 60
El Banco (Magdalena) Limnologica +0,043 59
El Banco (Magdalena) Limnologica +0,050 58
Ganaderia Caribe (Aracataca) Manglar +0,196 68
Ganaderia Caribe (Aracataca) Manglar +0,224 67
Ganaderia Caribe (Aracataca) Manglar +0,184 66
Ganaderia Caribe (Aracataca) Manglar +0,180 65

Continued 0 next page

Tabla 28: (Continued)

Estacion Naturaleza Rezago meses) Pcaudal
Ganaderia Caribe (Aracataca) Limnologica +0,107 58
Ganaderia Caribe (Aracataca) Limnologica +0,263 57
Ganaderia Caribe (Aracataca) Limnologica +0,267 56
Ganaderia Caribe (Aracataca) Limnologica +0,150 55

27

regional sobre la cuenca del Magdalena la Sierra Nevada que se acumula progresivamente en los
caudales fluviales hasta alcanzar valores extremos en 2022_ Segundo, el aporte sostenido de caudal
en la mayor parte del periodo es beneficioso para el manglar en terminos agregados pues reduce la
hipersalinizacion del sustrato y favorece la productividad del dosel, lo cual explica las correlaciones
positivas con NDVI Tercero, el evento puntual de mortandad detectado en septiembre 2020 n0 se
explica por un pico de caudal fluvial simultaneo que no existe en las series IDEAM sino pOr
U mecanismo distinto y compatible con los demas hallazgos del proyecto: la lluvia local intensa
sobre el pixel del humedal PERA5 ~0,123 a rezago de dos meses, tabla tabla 23) acompanada de
inundacion bajo dosel detectable por SAR (43,08 km? en septiembre-octubre 2020, tabla tabla 33)_
Cuarto; los efectos de mediano plazo del regimen La Nina sobre el sistema se manifiestan en los
quiebres blast de 2022 sobre CP Aguas Negras y CP Luna ~tabla tabla 15 periodo en el cual
los caudales del Magdalena y Aracataca alcanzan Su maximo historico de la serie 2013-2025 . Esta
reformulacion honra los datos sin renunciar la atribucion climatica del evento de 2020 La Niiia;
en el entendido de que la mediacion operativa entre el forzante atmosferico global y la respuesta
espectral local del manglar opera a traves de procesos hidrologicos multiescalares que ningtin forzante
tnico captura por si solo_

| Visual Element | Meaning |
|---|---|
| Text: "Caudal mensual IDEAM/DHIME - dos cuencas aportantes al sistema CGSM, 2013-2025" | Monthly flow IDEAM/DHIME - two contributing basins to the CGSM system, 2013-2025 |


A bar chart titled "Río Magdalena en El Banco (cuenca central, máximo mensual)" displays "Anomalía z-score caudal" on the y-axis, ranging from -2 to 2 with major grid lines at -2, -1, 0, 1, and 2. A horizontal red line is present at y=2. The x-axis represents time, with major grid lines at approximately 10-month intervals.

The chart consists of numerous vertical bars, colored either red or blue, indicating positive or negative anomalies respectively. A horizontal black line at y=0 serves as the baseline.

Two vertical shaded regions highlight specific periods:
- A light red shaded region spans from approximately the 10th to the 25th bar from the left.
- A light blue shaded region spans from approximately the 50th to the 60th bar from the left.

The bars show a fluctuating pattern of positive and negative anomalies over time.
- The first few bars are a mix of red and blue, mostly below 0.
- A period of predominantly blue bars (negative anomalies) occurs, including the light red shaded region, with some bars reaching close to -2.
- Following this, there is a sustained period of predominantly red bars (positive anomalies), with many bars exceeding 0.5 and some reaching above 1.
- Another period of predominantly blue bars follows, including the light blue shaded region, with some bars reaching close to -2.
- This is succeeded by a very prominent period of red bars, with many exceeding 1 and some reaching close to 2.
- The chart concludes with a period of predominantly blue bars, followed by a mix of red and blue bars, mostly above 0.


Rlo Aracataca Ganaderia Caribe (Sierra Nevada medio mensual)

A bar chart titled "Río Aracataca en Ganadería Caribe (Sierra Nevada, medio mensual)" displays the "Anomalía z-score caudal" on the y-axis, ranging from -2 to 2, and "Fecha" on the x-axis, spanning from 2013 to 2026.

The chart features vertical bars, colored red for positive anomalies and green for negative anomalies, representing monthly data points. A horizontal line at y=0 indicates the mean. A light red horizontal line at y=2 serves as a threshold.

Two shaded vertical regions highlight specific periods:
- A light red shaded area from late 2015 to early 2016.
- A light blue shaded area from late 2020 to early 2022.

**Data points (approximate z-score values):**

**2013:**
- Late 2013: Several red bars, peaking around 1.5.
- Late 2013: Several green bars, bottoming around -1.5.

**2014:**
- Early 2014: Several red bars, peaking around 1.5.
- Mid 2014: Several green bars, bottoming around -1.
- Late 2014: Several red bars, peaking around 1.5.

**2015:**
- Early 2015: Several red bars, peaking around 1.5.
- Mid 2015: Several green bars, bottoming around -1.5.
- Late 2015 (within red shaded area): Several green bars, bottoming around -1.5.

**2016:**
- Early 2016 (within red shaded area): Several green bars, bottoming around -1.5.
- Mid 2016: Several green bars, bottoming around -1.
- Late 2016: Several red bars, peaking around 0.5.

**2017:**
- Early 2017: Several red bars, peaking around 0.5.
- Mid 2017: Several green bars, bottoming around -1.
- Late 2017: Several red bars, peaking around 1.5.

**2018:**
- Early 2018: Several green bars, bottoming around -1.
- Mid 2018: Several red bars, peaking around 0.5.
- Late 2018: Several green bars, bottoming around -1.

**2019:**
- Early 2019: Several green bars, bottoming around -1.5.
- Mid 2019: Several green bars, bottoming around -1.5.
- Late 2019: Several green bars, bottoming around -1.5.

**2020:**
- Early 2020: Several green bars, bottoming around -1.5.
- Mid 2020: Several green bars, bottoming around -1.5.
- Late 2020 (within blue shaded area): Several green bars, bottoming around -1.5.

**2021:**
- Early 2021 (within blue shaded area): Several green bars, bottoming around -1.5.
- Mid 2021 (within blue shaded area): Several red bars, peaking around 1.5.
- Late 2021 (within blue shaded area): Several red bars, peaking around 1.5.

**2022:**
- Early 2022 (within blue shaded area): Several red bars, peaking around 1.5.
- Mid 2022: Several red bars, peaking around 2.5.
- Late 2022: Several red bars, peaking around 1.5.

**2023:**
- Early 2023: Several red bars, peaking around 1.5.
- Mid 2023: Several green bars, bottoming around -0.5.
- Late 2023: Several red bars, peaking around 0.5.

**2024:**
- Early 2024: Several green bars, bottoming around -1.5.
- Mid 2024: Several green bars, bottoming around -1.5.
- Late 2024: Several green bars, bottoming around -1.5.

**2025:**
- Early 2025: Several green bars, bottoming around -1.5.
- Mid 2025: Several red bars, peaking around 1.5.
- Late 2025: Several red bars, peaking around 1.5.

**2026:**
- Early 2026: Several green bars, bottoming around -1.


Figura 7: Series temporales de anomalia z-score del caudal mensual IDEAM para el rio Magdalena en
El Banco (panel superior maximo mensual) y el rio Aracataca en Ganaderia Caribe (panel inferior,
medio mensual) , 2013-2025. Las franjas sombreadas marcan los dos eventos ENSO documentados;
notese que los picos de caudal extremo >+2) ocurren en 2022, no en 2020.

# 7.9.1 Triangulacion con precipitacion satelital CHIRPS sobre las cuencas aportantes

Para verificar la robustez del hallazgo de correlacion positiva entre caudal y NDVI mediante una
fuente independiente del IDEAM, se descarga del Climate Hazards Group de la Universidad de
California en Santa Barbara la serie diaria de precipitacion CHIRPS v2.0 Funk et al. , 2015 sobre
dos bounding boxes que cubren las dos cuencas aportantes al sistema CGSM la cuenca alta-media

28

# Correlacion caudal IDEAM vs NDVI manglar CGSM, 2013-2025

Banco

Centra

**Title:** El Banco - Río Magdalena central

**Chart Type:** Grouped Bar Chart

**X-axis:** Rezago (meses)
**Y-axis:** ρ Pearson (caudal vs NDVI z-score)

**Legend (Naturaleza):**
*   manglar (green)
*   limnologica (blue)

**Data Points:**

*   **Rezago: 0 m**
    *   manglar: ~0.065
    *   limnologica: ~0.18
*   **Rezago: 1 m**
    *   manglar: ~0.04
    *   limnologica: ~0.23
*   **Rezago: 2 m**
    *   manglar: ~0.105
    *   limnologica: ~0.045
*   **Rezago: 3 m**
    *   manglar: ~0.26
    *   limnologica: ~0.05


### Ganadería Caribe — Sierra Nevada (Aracataca)

This is a grouped bar chart showing the distribution of two categories, "manglar" and "limnologica", across four "Rezago (meses)" values.

**Legend:**
*   **manglar**: Green bars
*   **limnologica**: Blue bars

**X-axis:** Rezago (meses)
*   0 m
*   1 m
*   2 m
*   3 m

**Y-axis:** (Implicitly, a count or frequency, ranging from 0 to approximately 1.0)

**Data:**

| Rezago (meses) | manglar | limnologica |
| :------------- | :------ | :---------- |
| 0 m            | ~0.9    | ~0.4        |
| 1 m            | ~0.8    | ~1.0        |
| 2 m            | ~0.7    | ~1.0        |
| 3 m            | ~0.6    | ~0.5        |


Figura &: Correlacion   de Pearson entre anomalia  de caudal IDEAM y anomalia   NDVI z-score,
desagregada por estacion hidrologica (paneles) . naturaleza espectral del sitio de monitoreo (barras
verdes  manglar , azules   limnologicas) rezago temporal de cero tres meses Las  correlaciones
positivas universales reflejan el efecto beneficioso del aporte fluvial sostenido sobre la productividad
del manglar_

del rio Magdalena entre 2' y 9 de latitud norte sobre la cordillera central colombiana; y la vertiente
noroccidental de la Sierra Nevada de Santa Marta entre 10,4 y 11,38 N asimismo CHIRPS aporta
una medida satelital de precipitacion regional que es la fuente meteorologica de los caudales medidos
en El Banco y Ganaderia Caribe

Los resultados CHIRPS convergen casi exactamente con los del caudal IDEAM ver tabla tabla 27
en este sentido la correlacion mas alta para el manglar se observa en ambas [uentes con la cuenca
alta-media del Magdalena a tres meses de rezago (PCHIRPS +0,252 vSs PIDEAM +0,277) y con
la Sierra Nevada con el mismo rezago de tres meses PCHIRPS +0,281 VS PIDEAM +0,224 UI
mes ) , asi dos fuentes cientificas independientes caudal hidrometrico medido en estaciones IDEAM
precipitacion satelital CHIRPS validada cOnl estaciones  meteorologicas  colombianas arrojan
correlaciones positivas de magnitud comparable y con el mismo orden de rezago temporal Esta
convergencia constituye uha doble validacion del hallazgo principal: el aporte hidrico sostenido
sobre las cuencas aportantes sea medido como precipitacion como caudal esta asociado de
manera positiva con el vigor del manglar de la CGSM en escalas de uno a tres meses, asi la dinamica
climatica del periodo La Niiia 2020-2022 favorece en terminos agregados al manglar y no constituye
en si misma el mecanismo de la mortandad puntual de septiembre 2020, la cual debe atribuirse
procesos  hidrologicos locales de pulsos extremos HO capturados por'  las   anomalias   mensuales
agregadas ERAs-Land p ~0,123 a dos meses + SAR de 43,08 km? bajo dosel) .

# 7.10 Validacion cruzada multilingiie Python + R + Julia

El proyecto materializa   la naturaleza multilingiie  del curso Python; Julia mediante
dos vias de validacion cruzada que verifican que las conclusiones del informe n0 dependen de la
implementacion ni del entorno computacional La primera via replica el flujo de series temporales
NDVI en R con stars st extract sobre el cubo construido partir de los TIFs trimestrales
lo compara contra la serie producida pOr reduceRegions en GEE para las mismas ocho estaciones,

29

# Anomalias mensuales CHIRPS sobre cuencas aportantes la CGSM, 2013-2025

CHIRPS magdalena alta media

A bar chart titled "z-score precipitación" displays a series of vertical bars, each representing a z-score value for precipitation. The x-axis is not explicitly labeled with values but shows a progression over time, indicated by vertical grid lines. The y-axis is labeled "z-score precipitación" and ranges from -2 to 3, with major grid lines at -2, -1, 0, 1, 2, and 3. A horizontal black line marks the 0 z-score level.

The bars are colored either red or blue. Red bars extend upwards from the 0 line, indicating positive z-scores, while blue bars extend downwards, indicating negative z-scores.

There are two shaded vertical regions on the chart. The first is a light red shaded area, spanning approximately 15 bars, where most bars are blue and extend significantly downwards. The second is a light blue shaded area, spanning approximately 15 bars, where most bars are red and extend significantly upwards.

The chart shows a fluctuating pattern of precipitation z-scores over time.


CHIRPS sierra nevada oeste

This is a bar chart showing the z-score of precipitation over time.

**Chart Title:** (None explicitly stated, but the y-axis label "z-score precipitación" implies the subject.)

**Axes:**
*   **X-axis:** Labeled "Fecha" (Date), ranging from late 2013 to early 2026. Major tick marks are at 2014, 2016, 2018, 2020, 2022, 2024, and 2026.
*   **Y-axis:** Labeled "z-score precipitación", ranging from -2.5 to 3.0. Major tick marks are at -2, -1, 0, 1, 2, and 3.

**Data Representation:**
The chart uses vertical bars to represent the z-score of precipitation for discrete time intervals (likely months).
*   Bars above the 0-line are colored red, indicating positive z-scores (above average precipitation).
*   Bars below the 0-line are colored blue, indicating negative z-scores (below average precipitation).

**Key Features and Observations:**
1.  **Overall Trend:** The chart displays significant variability in precipitation z-scores over the period. There are extended periods of both above-average and below-average precipitation.
2.  **Period of Prolonged Drought (Late 2014 - Early 2016):**
    *   A prominent period of consecutive blue bars (negative z-scores) is observed from late 2014 through early 2016.
    *   This period is highlighted by a light red shaded vertical band from approximately mid-2015 to mid-2016.
    *   During this time, many bars reach z-scores of -1.5 to -2.5, indicating severe drought conditions.
3.  **Period of Above-Average Precipitation (Mid-2016 - Mid-2018):**
    *   Following the drought, there is a period dominated by red bars (positive z-scores) from mid-2016 to mid-2018.
    *   Several bars during this time exceed z-scores of 1.5, with a peak around 2.5 in late 2017.
4.  **Mixed Period (Mid-2018 - Mid-2020):**
    *   This period shows a mix of red and blue bars, with a slight tendency towards negative z-scores in late 2019 and early 2020.
5.  **Another Period of Drought (Late 2020 - Mid-2022):**
    *   A second significant period of consecutive blue bars (negative z-scores) occurs from late 2020 to mid-2022.
    *   This period is highlighted by a light blue shaded vertical band from approximately late 2020 to mid-2022.
    *   Many bars during this time reach z-scores of -1.0 to -2.0.
6.  **Recent Period of Above-Average Precipitation (Mid-2022 - Early 2025):**
    *   From mid-2022 to early 2025, the chart is again dominated by red bars (positive z-scores).
    *   Several bars exceed z-scores of 1.5, with peaks around 2.0 to 2.5 in late 2022 and late 2023.
7.  **End of Chart (Early 2025 - Early 2026):**
    *   The chart ends with a mix of red and blue bars, with a few negative z-scores appearing in late 2025 and early 2026.

**Shaded Areas:**
*   A light red vertical shaded band extends from approximately mid-2015 to mid-2016, coinciding with a period of severe drought.
*   A light blue vertical shaded band extends from approximately late 2020 to mid-2022, coinciding with another period of severe drought.

**Gridlines:**
Light gray horizontal and vertical gridlines are present to aid in reading values.


Figura 9: Anomalias   mensuales de precipitacion CHIRPS sobre las dos cuencas aportantes a  la
CGSM cuenca alta-media   del Magdalena (panel superior) vertiente occidental de la Sierra
Nevada   (panel inferior) 2013-2025 Las franjas   sombreadas marcan El Nizo 2015-2016 (con
anomalias negativas sostenidas que confirman la sequia documentada) y La Ninia 2020-2022 (con
dominancia de anomalias positivas que confirman el regimen himedo)_ Los picos extremos >+2
se concentran en 2022 , en linea CcOn la observacion equivalente sobre los caudales IDEAM (figura
figura 7) .

30

# Correlacion entre precipitacion CHIRPS sobre cuencas aportantes NDVI z-score de la CGSM; 2013-2025

magdalena alta media mangiar

A bar chart titled "Pearson Correlation Coefficients".

The y-axis is labeled "ρ Pearson" and ranges from 0.00 to 0.35 in increments of 0.05.
The x-axis has four unlabeled categories.

The bars are blue.
- Bar 1: Height is approximately 0.075.
- Bar 2: Height is approximately 0.17.
- Bar 3: Height is approximately 0.098.
- Bar 4: Height is approximately 0.25.


magdalena aita media limnologica

A bar chart with a light gray background and a grid of horizontal lines. The y-axis is on the left, with tick marks and labels at intervals of 10, from 0 at the bottom to 100 at the top. The x-axis is at the bottom, with four unlabeled bars.

The bars are light blue.
- Bar 1 extends to a value of 70.
- Bar 2 extends to a value of 30.
- Bar 3 extends to a value of 65.
- Bar 4 extends to a value of 50.


sierra nevada oeste mangiar

This is a bar chart titled "Rezago (meses)" on the x-axis and "ρ Pearson" on the y-axis.

The x-axis represents "Rezago (meses)" with values 0, 1, 2, and 3.
The y-axis represents "ρ Pearson" with values ranging from 0.00 to 0.35, in increments of 0.05.

The chart displays four blue bars:
- At Rezago (meses) = 0, the bar reaches approximately 0.14.
- At Rezago (meses) = 1, the bar reaches approximately 0.13.
- At Rezago (meses) = 2, the bar reaches approximately 0.06.
- At Rezago (meses) = 3, the bar reaches approximately 0.28.


siena nevada oeste limnologica

A bar chart titled "Rezago (meses)" on the x-axis. The y-axis is not labeled but shows numerical values. The chart has a light gray grid background.

The chart displays four blue bars:
- Bar 1, labeled "0" on the x-axis, reaches a height of approximately 4.
- Bar 2, labeled "1" on the x-axis, reaches a height of approximately 7.
- Bar 3, labeled "2" on the x-axis, reaches a height of approximately 9.
- Bar 4, labeled "3" on the x-axis, reaches a height of approximately 6.


Figura 10: Correlacion de Pearson entre anomalia mensual de precipitacion CHIRPS y anomalia
NDVI z-score de la CGSM, organizada pOr cuenca aportante (filas) y naturaleza espectral del sitio
de monitoreo (columnas con rezagos temporales de cero a tres meses. La convergencia con la figura
equivalente del caudal IDEAM (figura figura 8) ofrece doble validacion de la direccion y magnitud
del acoplamiento hidroclimatico sobre el manglar:

31

Tabla 29: Correlacion de Pearson entre anomalia mensual de precipitacion CHIRPS sobre cuencas
aportantes y NDVI z-score de las estaciones de la CGSM, principales valores pOr cuenca, naturaleza
rezago temporal.

Tabla 30:

Cuenca CHIRPS Naturaleza Rezago meses Pprecip
Magdalena alta-media Manglar +0,075 86
Magdalena alta-media Manglar +0,170 85
Magdalena alta-media Manglar +0,097 84
Magdalena alta-media Manglar +0,252 83
Magdalena alta-media Limnologica +0,276 72
Magdalena alta-media Limnologica +0,268 70
Sierra Nevada oeste Manglar +0,281 83
Sierra Nevada oeste Limnologica +0,359 70

de esta manera la coincidencia de p > 0,95 y RMSE 0{,}05 unidades NDVI confirma que la serie
temporal del proyecto se reproduce de manera equivalente en los dos lenguajes_

La segunda via amplia el ejercicio a un analisis estadistico identico ejecutado en los tres lenguajes
~notebook 14_validacion_trilingual.ipynb en el cual se calcula la correlacion de Pearson
entre el caudal medio  mensual del rio Magdalena en El Banco y la anomalia NDVI Z-score de
las cuatro estaciones de manglar para rezagos de cero tres meses; mediante implementaciones
independientes en Python (pandas) , R (tidyverse invocado pOr' Rscript desde el notebook)
Julia (DataFrames . jl invocado pOr julia como subproceso) . Los tres   flujos   producen valores
identicos hasta al menos tres  decimales 0,064 rezago cero, 0,039 rezago uno, 0,108
a rezago  dos 0,256 a   rezago tres en   los tres   lenguajes con diferencia maxima del orden
de 10 atribuible la  precision  numerica interna de cada entorno. La convergencia   operativa
entre Python, R Julia, ilustrada en la figura figura 11, demuestra que el pipeline del proyecto
constituye ua arquitectura interoperable y que la eleccion del lenguaje obedece la conveniencia
disciplinar de cada fase Python para GEE SamGeo, para bfast y series  ecohidrologicas;
Julia para fragmentacion predicados DE-9IM con LibGEOS . jl antes que ua restriccion
metodologica. esta via estadistica trilingiie se suma uhla validacion   geometrica adicional
~notebook 04c_topologia_julia. ipynb en la cual los   predicados   topologicos intersects
contains se ejecutan en Julia   mediante LibGEOS . jl  sobre los   mismos   parches la misma
frontera del AOI que utilizo el flujo Python con geopandas y shapely, asimismo los dos lenguajes
producen conteos identicos de parches en borde sobre los tres periodos de referencia (17/6, 17/8
15/8 parches   totales/en borde para degradacion, recuperacion actual respectivamente, con
proporciones de borde 35,3 %, 47,1 % y 53,3 %), asi la  equivalencia   trilingiie del analisis   del
proyecto se sostiene tambien para las operaciones topologicas no solo para las estadisticas_

El balance   multilingiie  del  proyecto se cierra con dos   replicas adicionales en que verifican
operativamente la equivalencia Python R sobre los dos analisis hidroclimaticos mas relevantes del
informe. La primera, notebook 11b_indices_enso noaa_R. ipynb, replica en COn tidyverse la

32

descarga directa de los indices ENSO globales y el calculo de correlaciones por rezago desagregadas
por   naturaleza espectral, asi las ocho filas  de la tabla tabla 25 coinciden hasta tres decimales
entre las dos implementaciones (en particular pSOnglar; lag +0,198 y p ologica; lag 0 0,121 en
ambos lenguajes) . La segunda, notebook 12c_caudal ideam_R. ipynb, replica de la misma manera
el analisis de correlacion entre caudal IDEAM NDVI de las dos estaciones hidrologicas, asi las
dieciseis filas de la tabla tabla 27 coinciden hasta tres decimales entre Python y R -incluido el
valor pico pEL Banco; manglar , lag +0,256 que sostiene la interpretacion del informe sobre el efecto
beneficioso del aporte fluvial sostenido La consistencia entre las cuatro validaciones cruzadas

ENSO Python R, caudal Python R, caudal Python Julia, y predicados DE-9IM Python
Julia confirma de manera operativa que la arquitectura   multilingiie   del  proyecto produce
resultados reproducibles independientes del entorno computacional

Validacion cruzada trilingue caudal IDEAM EE Banco vs NDVI manglar CGSM, 2013-2025

This is a grouped bar chart titled "Lenguaje" (Language) showing the Pearson correlation coefficient (ρ Pearson) between the Magdalena River flow (caudal Magdalena) and the Mangrove NDVI (NDVI manglar) across different temporal ranges.

The y-axis represents the Pearson correlation coefficient (ρ Pearson (caudal Magdalena vs NDVI manglar)) and ranges from 0.00 to 0.25.
The x-axis represents the temporal range (Rango temporal) with categories: 0 m, 1 m, 2 m, and 3 m.

There are three groups of bars for each temporal range, representing different languages:
- Python (light blue)
- R (medium blue)
- Julia (purple)

Here are the values for each bar:

**Temporal Range: 0 m**
- Python: ~0.06
- R: ~0.06
- Julia: ~0.06

**Temporal Range: 1 m**
- Python: ~0.035
- R: ~0.035
- Julia: ~0.035

**Temporal Range: 2 m**
- Python: ~0.11
- R: ~0.11
- Julia: ~0.11

**Temporal Range: 3 m**
- Python: ~0.26
- R: ~0.26
- Julia: ~0.26

All three languages show identical Pearson correlation coefficients for each temporal range. The correlation increases with the temporal range, from approximately 0.06 at 0 m to 0.26 at 3 m.


Figura Il: Validacion cruzada trilingiie Python + R + Julia sobre la correlacion de Pearson entre
el caudal medio mensual del rio Magdalena en El Banco y la anomalia NDVI z-score de las cuatro
estaciones de manglar de la CGSM, con rezagos de cero a tres meses, 2013-2025. Las tres barras
de cada rezago son visualmente identicas, de esta manera la convergencia numerica entre los tres
lenguajes hasta tres decimales valida la independencia del analisis respecto al entorno computacional.

# 7.11 Validacion con datos NASA: deteccion de inundacion SAR

La consulta a la Global Flood Database identifico 16 eventos de inundacion historicos que intersecan
el AOI acotado entre 2001 y 2017, de los cuales 14 registraron areas de inundacion superiores a cero_
El evento de mayor magnitud ocurrio en febrero de 2005 con 299,2 km? inundados el 35,8 % del
AOI acotado seguido por los eventos de noviembre de 2004 (274,8 km? y septiembre-diciembre
de 2005 (239,4 km? , 92 dias de duracion, el mas prolongado del registro)_ Estos eventos coinciden
con episodios ENSO documentados pOr el IDEAM, lo que confirma la vulnerabilidad del sistema
lagunar la variabilidad climatica interanual. Las estaciones del borde oriental del complejo lagunar
~Isla Boqueron; Punta Cerro, Punta Chino y Rio Sevilla registraron inundacion en 9 0 10 de los
16 eventos, en tanto que Caio Clarin solo fue afectado en evento, lo cual es consistente COn Su
ubicacion mas alejada del cuerpo de agua principal:

Para el evento de septiembre-octubre de 2020 IO registrado en la Global Flood Database cuya

33

Tabla 31: Eventos de inundacion COn mayo1 area afectada dentro del AOI acotado (Global Flood
Database , 2001-2017)_

Tabla 32:

Evento Inicio Fin Area km? Dias
DFO 2625 2005-02-11 2005-02-26 299,2 15

Tabla 32: (Continued)

Continued on next page

Evento Inicio Fin Area km? Dias
DFO 2588 2004-11-20 2004-11-27 274,8

Tabla 32:

Continued on next page (Continued

Evento Inicio Fin Area km? Dias
DFO 2761 2005-09-15 2005-12-16 239,4 92

Continued on next page
Tabla 32: (Continued)

Evento Inicio Fin Area km? Dias
DFO 1996 2002-07-20 2002-07-31 233,9 11

Continued on next page

Tabla 32: (Continued)

Evento Inicio Fin Area km? Dias
DFO 4495 2017-08-04 2017-08-21 221,3 17

Continued on next page
Tabla 32: Continued)

Evento Inicio Fin Area km? Dias
DFO 3212 2007-10-01 2007-12-10 211,5 70

Continued on next page

Tabla 32: (Continued)

Evento Inicio Fin Area 'km? Dias
DFO 3750 2010-11-15 2010-12-20 190,1 35

Continued on next page Tabla 32: (Continued)

Evento Inicio Fin Area km? Dias
DFO 3754 2010-11-25 2010-12-20 175,0 25

Continued on next page
Tabla 32: (Continued)

Evento Inicio Fin Area km? Dias
DFO 3421 2008-12-13 2008-12-14 151,9

Tabla 32: 3Continued) Continued on next page

Evento Inicio Fin Area (km? Dias
Cl

Tabla 33: Extension de la inundacion detectada con Sentinel-1 SAR (septiembre-octubre 2020) sobre
el AOI acotado SFF + VPI Salamanca.

# Tabla 34:

Tipo de inundacion Area (km?) AOI acotado
Agua abierta (SAR diff > +3 dB) 15,93 1,9 %
Bajo dosel manglar (SAR diff < -2 dB) 43,08 5,2 %
Total afectado 59,02 7,1 %

cobertura termina en 2017 la deteccion con Sentinel-1 SAR (banda VH, modo IW) restringida
al AOI acotado identifico 15,93 km? de inundacion en agua abierta (diferencia de backscatter
dB) y 43,08 km? de inundacion bajo dosel de manglar (diferencia negativa, indicativa de scattering
de doble rebote agua-tronco), para un total de 59,02 km? afectados 7,1 % del AOI acotado
Este orden de magnitud sustancialmente menor al reportado en la iteracion preliminar sobre el
AOI envolvente (1.507,4 km? y resulta mas defendible, pues la  version envolvente contabilizaba
cambios espectrales en zonas no-manglar de la Sierra Nevada y areas inland que tambien producen
diferencia SAR negativa pOr dinamica de vegetacion natural sin relacion con la inundacion La Nina
El cruce con las anomalias NDVI revela patrones diferenciados por estacion que se discuten en la
tabla tabla 35 .

# 7.12 Dinamica hidrica: transiciones JRC en zonas de manglar

El analisis de las transiciones del JRC Global Surface Water restringido al AOI acotado revela una
dinamica hidrica donde la perdida y la ganancia de cuerpos de agua son aproximadamente del mismo
orden, de esta manera el sistema lagunar se redistribuye mas que se contrae_ Se identifican 18,55 km?
de agua permanente perdida cuerpos que se secaron entre 1984 y 2021 y 29,38 km? de agua
estacional perdida; en tanto que 23,55 km? aparecen como nuevo permanente y 31,31 km? como
nuevo estacional; sumando, el sistema gana 54,86 km? y pierde 47,93 km? para U balance neto
positivo de aproximadamente km?. De manera complementaria, 49,30 km? se  clasifican como
efimero   estacional zonas  donde la inundacion esporadica nO sigue ull patron estacional
definido y 18,54 km? muestran transicion de regimen permanente estacional, lo que sugiere UII
retroceso parcial de la lamina de agua permanente Estos hallazgos son coherentes con el contexto
hidrologico de UI humedal en proceso de rehabilitacion tras la reapertura de canales (1996-1998)
que reintrodujo la conexion con el rio Magdalena, asi la dinamica observada en la ventana JRC
captura los efectos combinados de la intervencion y de los episodios ENSO posteriores_

# 7.13 Ganancia y perdida de manglar (2020 vs 2024-2025)

Entre el periodo de degradacion y el estado actual se cuantifican 183,2 km? de perdida y 259,2 km?
de ganancia de manglar, sobre una base estable de 690,9 km? lo que resulta en un cambio neto
positivo de +76,0 km?.

35

Tabla 35: Cruce de sezial SAR, NDVI y frecuencia de inundacion historica pOr estacion; restringido al
AOI acotado SFF + VPI Salamanca. Solo dos de las ocho estaciones quedan estrictamente dentro del
poligono protegido oficial Caiio Palos al sur del Santuario y VIPIS sobre el Via Parque ambas
presentan un SAR diff positivo cercano a cero durante septiembre-octubre de 2020, lo que descarta
inundacion bajo dosel detectable por SAR en ese par de puntos_ Las seis estaciones restantes caen
fuera del poligono acotado y por tanto el clip(aoi) aplicado a la imagen de diferencia SAR retorna
None en SuS buffers, asimismo este resultado Uil hallazgo metodologico relevante: las estaciones
INVEMAR-GBIF fueron diseriadas como puntos de monitoreo limnologico sobre la lamina de agua
del sistema lagunar central, fuera de los poligonos oficiales de proteccion; asi Su USO para monitorear
manglar requiere mediar la lectura mediante buffers amplios 0 ampliar el AOI mas alla de RUNAP.

Tabla 36:

Estacion Naturaleza Dentro AOI acotado SAR diff (dB) NDVI sept-2020 Eventos GF
Isla Boqueron Limnologica No N/A -0,018 10 de 16
Punta Cerro Limnologica No N/A -0,078 10 de 16
Punta Chino Limnologica No N/A 0,200 9 de 16
Rio Sevilla Limnologica No N/A 0,050 10 de 16
Caiio Palos Manglar Si +0,15 0,400 2 de 16
CP Pajarales Manglar No N/A 0,300 9 de 16
Caiio Clarin Manglar No N/A 0,500 1 de 16
VIPIS Manglar Si +0,12 0,350 9 de 16

36

Tabla 37: Transiciones JRC Global Surface Water (1984-20021) dentro del AOI acotado SFF + VPI
Salamanca. El AOI acotado contiene 385,3 km? de agua permanente (>75 del tiempo) y 44,1 km?
de agua estacional (25-75 %), de modo que casi la mitad del poligono protegido es lamina de agua

# Tabla 38:

Transicion JRC dentro del AOI acotado Area km?) Interpretacion
Permanente 377,75 Lamina de agua estable
Nuevo permanente 23,55 Cuerpos nuevos consolidados
Permanente perdido 18,55 Cuerpos de agua secados
Estacional 17,98 Zonas con regimen estacional estable

# Tabla 38: (Continued)

Continued On next page

Transicion JRC dentro del AOI acotado Area (km?) Interpretacion
Nuevo estacional 31,31 Nuevas areas de inundacion estacional
Estacional perdido 29,38 Zonas que dejaron de inundarse
Permanente a estacional 18,54 Retroceso parcial de lamina permanente
Efimero estacional 49,30 Inundacion intermitente sin patron estacional

# Tabla 38: (Continued)

Continued on next page

Transicion JRC dentro del AOI acotado Area (km?) Interpretacion
Efimero permanente 1,74 Agua intermitente persistente

37

# 7.14 Validacion doble contra cartografia oficial (INVEMAR 1:25.000) y global
(ESA WorldCover v200)

La clasificacion pOr umbrales espectrales se valida sobre el AOI acotado contra ESA WorldCover
v200 (Zanaga et al,, 2022) ~producto cartografico  global de 10 de resolucion que reporta
cobertura de tierra para el ano 2021 y que se acota a la clase 95 (manglar) como referencia binaria

La sustitucion del Global Mangrove Watch por ESA WorldCover como cartografia de referencia
obedece a que el catalogo publico de sat-io en Google Earth Engine reorganizo el dataset GMW
al momento de la entrega y los paths conocidos del GMW v3.0 (Bunting et al., 2022) dejaron de
ser accesibles directamente desde el contenedor, asi WorldCover ofrece una alternativa con mayor
resolucion  espacial nativa (10 m frente los 25 m del GMW) validacion   independiente pOr la
Agencia Espacial Europea y consistencia metodologica con la cartografia global de cobertura de
tierra_ El calculo de la matriz de confusion se realiza directamente sobre los servidores de Earth
Engine mediante reduceRegion con histograma de frecuencias, comparando pixel a pixel a 25
de resolucion la clasificacion por umbrales NDVI 0,70, elevacion SRTM 10 m, distancia al
agua JRC 3 km contra la clase 95 de WorldCover, sin necesidad de descargar los rasters al
contenedor local.

Los resultados sobre el AOI acotado mejoran sustancialmente respecto al baseline envolvente de
la iteracion preliminar: el Fl-score pasa de 0,442 a 0,548 (+24 %), la Precision acuerdo positivo
predictivo) sube de 0,428 a 0,768 (+79 %) y la Specificity alcanza 0,944,asimismo el acotamiento al
area protegida oficial reduce dramaticamente los falsos positivos por vegetacion riberana; salitrales
y zonas agropecuarias del AOI envolvente que comparten firma espectral con el manglar pero HO
constituyen habitat potencial dentro del poligono RUNAP. La Recall sensibilidad) baja ligeramente
de 0,457 0,426 atribuible que el umbral NDVI 0,70 es conservador y deja fuera manglar
joven degradado que WorldCover si reconoce con Su clasificador supervisado en tanto que la
Overall Accuracy desciende de 0,899 0,788 unicamente porque la prevalencia de la clase positiva
pasa de cerca del 8 % en el AOI envolvente a aproximadamente el 30 % en el AOI acotado; lo cual
hace de OA ula metrica menos engaiiosa Y mas informativa pues deja de estar dominada pOr el
acuerdo trivial sobre la clase mayoritaria.

Conviene precisar tres aspectos del alcance de la validacion. En primer lugar, la metrica reportada se
calcula sobre la clasificacion pOr umbrales espectrales con restricciones geofisicas, no sobre la salida
directa de SamGeo: la segmentacion automatica produce poligonos que cubren cualquier objeto
coherente del raster RGB ~incluidos cuerpos de agua y suelo desnudo y pOL tanto requiere U
filtrado posterior por CMRI 0 NDVI medio antes de SU comparacion con la cartografia de referencia,
filtrado que en esta entrega se realiza  implicitamente al usar la clasificacion pOr umbrales cOmo
producto evaluado. En segundo lugar. la cartografia WorldCover identifica aproximadamente 412
km? de manglar dentro del AOI acotado mientras que el clasificador pOr  umbrales identifica 229
km? , es decir , una subestimacion sistematica que se explica pOr el umbral conservador NDVI > 0,70
y que sugiere como linea de trabajo bajar el umbral a 0,60-0,65 complementarlo con CMRI para
mejorar la Recall sin comprometer la Precision alcanzada. En tercer lugar; la diferencia residual entre
ambas cartografias corresponde a heterogeneidad espectral del manglar de la CGSM vegetacion
riberana, pastizales inundables, salitrales con cobertura intermitente a la diferencia entre
clasificador supervisado de WorldCover (entrenado globalmente sobre etiquetas de referencia) y la
regla deterministica pOr umbrales usada en este proyecto, distincion que conviene tener presente
al comparar este Fl con los rangos 0,80-0,90 reportados por Selvaraj Gallego-Perez (2023 para
flujos optico-SAR supervisados con Random Forest _

Adicionalmente al calculo de   la matriz conbra WorldCover; se descarga la   cartografia oficial

38

Tabla 39: Metricas de validacion de la clasificacion de manglar contra dos cartografias de referencia
INVEMAR 1:25.000   (Instituto de Investigaciones  Marinas Costeras, 2020) como referencia
nacional oficial y ESA WorldCover v200 (Zanaga et al 2022) como referencia global 10 La
columna de baseline  envolvente  corresponde a la iteracion  preliminar sobre 5.073 km?; las dos
columnas vigentes corresponden al AOI acotado SFF + VPI '835 km?) constituyen la validacion
doble del informe v6_

# Tabla 40:

Metrica Baseline envolvente INVEMAR 1:25.000 vigente)
Overall Accuracy (OA) 0,899 0,803
Precision Producer s) 0,428 0,811
Recall User's) 0,457 0,454
Fl-score 0,442 0,583
Specificity 0,954
TP FP FN TN 188.097 43.777 225.733 913.309
Area referencia 2020-2021 376,5 km? (GMW v3) 297 km? (INVEMAR AOI)
Area clasificacion 556,0 km? 147 km?
Resolucion de evaluacion 25 m 25 m
Umbrales NDVI > 0,70, elev 10 1, agua < 3 km idem

colombiana de manglares escala 1:25.000 publicada por el Instituto de Investigaciones Marinas
y Costeras   (INVEMAR , 2020) mediante el servicio ArcGIS REST SIGMA /MANGLARES_COLOMBIA;
asimismo clasificador se evalia simultaneamente contra dos referencias independientes
ua global con criterio supervisado a 10 m una nacional con criterio fotointerpretado a escala
1.25.000 lo cual ofrece uhla validacion robusta y permite establecer un techo metodologico realista
para el FL esperable_ La car tografia INVEMAR se rasteriza sobre la misma grilla de WoldCover a
25 m de resolucion usando rasterio.features.rasterize COn el parametro all_touched-True
limpieza   previa de geometrias invalidas con shapely.validation.make_valid, asi los nueve
MultiPolygon presentes que concentran el 86 % del area total y serian descartados silenciosamente
pOr ula rasterizacion ingenua quedan correctamente incorporados la comparacion:

Como medida de techo metodologico, conviene reportar tambien el acuerdo directo entre las dos
cartografias de referencia: la matriz de confusion INVEMAR 1:25.000 vs ESA WorldCover v200
sobre el AOI acotado arroja un Fl-score de 0,833 Precision 0,833, Recall 0,832 , Specificity
0,928) , lo que indica que las dos cartografias oficiales convergen en aproximadamente el 83 % de Su
acuerdo dentro del poligono protegido; de esta manera cualquier clasificador evaluado conbra ua
otra referencia tiene como cota superior realista uIl F1 cercano ese valor y no la unidad. La
proximidad de los FL del clasificador del proyecto contra ambas referencias 0,583 vs INVEMAR y
0,548 vs WorldCover demuestra que el rendimiento consistente e independiente de la cartografia
elegida.

39

Tabla 41: Benchmark del clasificador supervisado Random Forest frente al clasificador deterministico
pOr umbrales espectrales, sobre el AOI acotado y la mediana Sentinel-2 del periodo actual 2024-2025_
El RF se entrena con 1.000 puntos estratificados sobre ESA WorldCover v200 y validacion cruzada
K-fold 5 (Fl medio 0,931 = 0,017)_ Las metricas pixel-a-pixel se calculan sobre 10.000
puntos de muestreo aleatorio dentro del AOI.

Tabla 42:

Metodo Referencia F1 Precision Recall Specificity OA
Umbrales NDVI/CMRI INVEMAR 1:25.000 0,583 0,811 0,454 0,954 0,803
Umbrales NDVI/CMRI ESA WorldCover v200 0,548 0,768 0,426 0,944 0,788
Random Forest INVEMAR 1:25.000 0,826 0,745 0,926 0,884 0,895
Random Forest ESA WorldCover v200 0,889 0,846 0,937 0,926 0,930

# 7.15 Benchmark del clasificador supervisado Random Forest

Con el proposito de cuantificar la ganancia esperable al sustituir la regla deterministica por umbrales
NDVI y CMRI por un clasificador supervisado; se implementa un Random Forest dentro de Google
Earth Engine sobre la misma imagen mediana Sentinel-2 del periodo actual (2024-2025 y el mismo
AOI acotado, siguiendo el notebook reproducible 11_random_forest_ benchmark. ipynb. El modelo
opera con 100 arboles, minLeafPopulation 5 y un conjunto de 15 variables predictoras ~las diez
bandas reflectivas de Sentinel-2 (B2 B12) , los tres indices espectrales (NDVI, NDWI, CMRI)
dos variables auxiliares (elevacion SRTM y distancia al agua JRC) El entrenamiento utiliza 1.000
puntos estratificados sobre la cartografia oficial INVEMAR 1:25.000 500 manglar, 500 no manglar) ,
con validacion cruzada K-fold (K=5) y metricas reportadas sobre el conjunto retenido en cada
particion. El clasificador resultante se aplica pixel a pixel a la imagen completa se evalua contra
las mismas dos referencias del clasificador por umbrales, en condiciones experimentales identicas
para garantizar comparabilidad.

Random Forest Importancia de variables predictoras

This is a horizontal bar chart titled "Importancia (Gini)". The y-axis lists 15 categories, and the x-axis represents numerical values from 0.0 to 20.0, with major ticks at 2.5 unit intervals. The bars are dark green.

Here are the categories and their corresponding values, ordered from top to bottom as they appear on the y-axis:

*   **B11**: Approximately 19.0
*   **dist_agua**: Approximately 16.0
*   **B12**: Approximately 14.0
*   **CMRI**: Approximately 11.0
*   **NDWI**: Approximately 10.5
*   **B5**: Approximately 8.5
*   **NDVI**: Approximately 8.0
*   **B8A**: Approximately 7.5
*   **B2**: Approximately 7.0
*   **B3**: Approximately 6.5
*   **B8**: Approximately 6.0
*   **B4**: Approximately 5.5
*   **B7**: Approximately 5.0
*   **B6**: Approximately 4.5
*   **elev**: Approximately 3.0


Figura 12: Importancia relativa de las quince variables predictoras del clasificador Random Forest
ordenadas pOr contribucion al modelo (Gini importance). Las variables con mayor peso aportan la
capacidad de discriminacion entre manglar y HO manglar dentro del AOI acotado_

La comparacion entre ambos metodos arroja ua ganancia consistente del clasificador supervisado:
el FI-score asciende de 0,583 0,826 contra INVEMAR (+42 %) y de 0,548 a 0,889 contra ESA
WorldCover (+62 %) , con U patron analogo en la Overall Accuracy que pasa de 0,803 a 0,895 y de
0,788 0,930 respectivamente_ La mejora mas pronunciada se observa en la Recall que duplica Su
valor en ambas referencias (0,454 7 0,926 contra INVEMAR; 0,426 0,937 contra WorldCover) ,
lo cual resuelve la subestimacion cronica detectada en el clasificador por umbrales conservadores
atribuida al corte NDVI > 0,70. La Precision desciende ligeramente bajo el clasificador supervisado
(de 0,811 0,745 contra INVEMAR), comportamiento esperable cuando la Recall aumenta de
forma asimetrica, pero el balance neto medido por FL favorece sin ambigiiedad al Random Forest_
El analisis de importancia de variables (figura figura 12) revela que las bandas SWIR de Sentinel-
Bll y Bl2 concentran la mayor capacidad discriminante (importancia Gini de 19,6 y 14,3
respectivamente), seguidas por la distancia al agua del JRC (16,0) y los indices CMRI (11,4) y
NDWI (11,1) , de manera que la informacion de humedad y proximidad hidrologica resulta tan 0 mas
relevante que el vigor vegetativo (NDVI 8,4) para discriminar el manglar de la CGSM, hallazgo
coherente con la naturaleza inundada y halofita del bosque y que orienta futuras extensiones cOn
datos SAR de Sentinel-1 ALOS-2 PALSAR para profundizar la deteccion de manglar inundado
bajo dosel:

# 7.16 Serie temporal continua Sentinel-1 SAR

Mas   alla de la   deteccion   puntual  del evento de inundacion de septiembre 2020 reportada en
la seccion   anterior; se construye uha serie  temporal mensual continua de backscatter
Sentinel-1 SAR-VH sobre el AOI acotado para el periodo 2018-2025 , mediante el notebook
12_sentinell sar serie. ipynb. Se filtra la coleccion COPERNICUS/S1 GRD pOr polarizacion VH,
modo IW orbita descendente para garantizar consistencia geometrica sobre el Caribe colombiano;

se construyen composites mensuales pOr mediana y se extrae la serie sobre las ocho estaciones de
muestreo COn UI buffer de 500 m; replicando el protocolo aplicado al NDVI en Sentinel-2. Sobre la
serie asi construida se calcula el z-score por estacion y se identifican las anomalias significativas ((z]
> 2) que corresponden episodios de cambio abrupto en el backscatter, asociables inundaciones
bajo dosel ~reduccion de VH aclaramiento de canopia -aumento de VH La correlacion
de Pearson cruzada entre SAR-VH NDVI z-score pOr rezagos de cero a tres meses se reporta
en outputs_ tables sar vs_ndvi correlacion . CSV, permite caracterizar el desfase temporal
entre la senal radarica ~sensible a la humedad y estructura del dosel y la respuesta optica del
vigor vegetativo. La figura figura 13 muestra la serie completa sobre cinco estaciones representativas
con las anomalias codificadas pOr color, de manera que la integracion del SAR como serie continua
complementa el monitoreo optico aporta  sensibilidad ante perturbaciones   sub-canopy que
NDVI pOr' si solo no detecta.

Serie temporal Sentinel-1 SAR-VH (mediana mensual, buffer 500 m) 2018-2025

The image is a line chart with the following characteristics:

*   **Title:** None visible.
*   **X-axis:** No label visible. The x-axis appears to represent time, with tick marks at regular intervals.
*   **Y-axis:** Labeled "Cano Palos VH (dB)". The y-axis ranges from -17 to -15.
*   **Data:** A single line plot is present. The line is initially blue, then transitions to green, and finally to orange. The line has a general upward trend, with significant fluctuations. The blue portion of the line is more volatile than the green and orange portions. The orange portion of the line appears to be more stable than the green portion.
*   **Background:** The background is light gray with faint vertical gridlines. A lighter gray band is present behind the line plot.
*   **Markers:** Small circles are present along the line, changing color to match the line segment.
*   **Legend:** No legend is visible.


This is a line chart showing "CP Aguas Negras VH (dB)" on the y-axis. The x-axis is not labeled but represents a sequence of data points over time.

The y-axis ranges from -20 to -16, with major tick marks at -20, -18, and -16. There is a shaded horizontal band between -18.5 and -17.5.

The chart displays a single line with markers at each data point. The line is composed of three distinct segments, each with a different color and line style:

1.  **Blue solid line with light blue circular markers:** This segment starts at the left edge of the chart, around y = -19.5. It shows a fluctuating pattern, generally decreasing to a low of approximately -20.5, then increasing to around -18.5. This segment covers the first 20 data points.
2.  **Dark green dashed line with light green circular markers:** This segment continues from the blue segment, starting around y = -18.5. It shows a generally increasing trend with fluctuations, reaching a peak of approximately -17.0, then decreasing slightly. This segment covers the next 20 data points.
3.  **Dark green solid line with orange circular markers:** This segment continues from the dark green dashed segment, starting around y = -17.0. It shows a sharp increase to a peak of approximately -16.0, followed by a decrease to around -18.0, then a fluctuating pattern generally staying within the -17.0 to -17.5 range. This segment covers the remaining 20 data points, ending at the right edge of the chart around y = -17.0.

In total, there are approximately 60 data points plotted on the chart.


This is a line chart with a y-axis labeled "CP Luna VH (dB)" ranging from -23 to -19. The x-axis is not labeled but appears to represent time or a sequence of data points.

The chart displays two distinct line segments, each with its own color and marker style:

1.  **Blue Line Segment:** This segment is a solid line with blue circular markers. It starts at approximately -20.5 dB, drops to a minimum of about -23.5 dB, then rises to approximately -21 dB, and finally drops again to about -23 dB before rising to approximately -22 dB. This segment covers the initial portion of the x-axis.

2.  **Orange Line Segment:** This segment is a dashed line with orange circular markers. It starts at approximately -21 dB, rises to a maximum of about -19 dB, then fluctuates between approximately -21 dB and -19 dB, and finally rises to approximately -19 dB. This segment covers the latter portion of the x-axis.

The transition between the blue and orange segments occurs at approximately -21 dB. The chart background is light gray with a darker gray horizontal band between -20 dB and -19 dB. Vertical grid lines are present but not labeled.


A line chart titled "Cano Clarin VH (dB)" on the y-axis, ranging from -20 to -14. The x-axis is not labeled but appears to represent time or a sequence of observations.

The chart displays a single line with markers at each data point. The line is solid dark green when the data points are within a shaded gray band, and dashed dark green when outside. The shaded gray band extends from approximately -16.5 dB to -14.5 dB.

The markers are colored based on their position relative to the shaded band:
- Orange markers indicate data points above the shaded band.
- Light blue markers indicate data points within the shaded band.
- Dark blue markers indicate data points below the shaded band.

The line shows significant fluctuations. Key features include:
- An initial segment with dark blue markers, then light blue, then a peak with orange markers, followed by a dip with dark blue markers.
- A subsequent segment with light blue markers, then a peak with orange markers, followed by a dip with dark blue markers.
- A long segment with light blue markers, then a peak with orange markers, followed by a dip with dark blue markers.
- A final segment with light blue markers, then a peak with orange markers, followed by a dip with dark blue markers.

Vertical grid lines are present, dividing the chart into several sections. Horizontal grid lines correspond to the y-axis ticks.


This is a line chart titled "Punta Cerro VH (dB)".
The y-axis represents "Punta Cerro VH (dB)" and ranges from -23 to -20.
The x-axis represents time, ranging from 2018 to 2026.
The chart displays a single line with markers, which changes color and line style at different points.

The line starts in 2018 with orange markers and a solid dark green line.
- The first point is at approximately 2018.0, -20.7 dB.
- The line then drops to approximately 2018.2, -21.2 dB.
- It continues to drop to approximately 2018.3, -22.8 dB.
- It then rises to approximately 2018.4, -22.5 dB.
- It drops again to approximately 2018.5, -23.2 dB.
- It rises to approximately 2018.6, -22.8 dB.
- It drops to approximately 2018.7, -23.5 dB.
- It rises to approximately 2018.8, -22.8 dB.
- It drops to approximately 2018.9, -23.5 dB.
- It rises to approximately 2019.0, -22.5 dB.

Around 2019.0, the markers change to light blue, but the line remains solid dark green.
- The line drops to approximately 2019.1, -23.5 dB.
- It rises to approximately 2019.2, -22.5 dB.
- It drops to approximately 2019.3, -23.5 dB.
- It rises to approximately 2019.4, -22.8 dB.
- It drops to approximately 2019.5, -23.5 dB.
- It rises to approximately 2019.6, -22.8 dB.
- It drops to approximately 2019.7, -23.5 dB.
- It rises to approximately 2019.8, -22.8 dB.
- It drops to approximately 2019.9, -23.5 dB.
- It rises to approximately 2020.0, -22.8 dB.

Around 2020.0, the markers change back to orange, and the line remains solid dark green.
- The line rises sharply to approximately 2020.1, -21.5 dB.
- It continues to rise to approximately 2020.2, -21.0 dB.
- It drops slightly to approximately 2020.3, -21.2 dB.
- It rises to approximately 2020.4, -20.8 dB.
- It drops to approximately 2020.5, -21.0 dB.
- It rises to approximately 2020.6, -20.8 dB.
- It drops to approximately 2020.7, -21.0 dB.
- It rises to approximately 2020.8, -20.8 dB.
- It drops to approximately 2020.9, -21.0 dB.
- It rises to approximately 2021.0, -20.8 dB.

The line continues with orange markers and a solid dark green line through 2021, 2022, and into 2023.
- The line generally fluctuates between -20.5 dB and -21.5 dB during this period, with a peak around 2022.5 at approximately -20.2 dB.
- The last orange marker and solid line segment is around 2023.2, at approximately -20.5 dB.

Around 2023.2, the markers change to light blue, and the line style changes to a dashed dark green line.
- The line drops sharply to approximately 2023.3, -22.5 dB.
- It rises to approximately 2023.4, -22.0 dB.
- It drops to approximately 2023.5, -22.5 dB.
- It rises to approximately 2023.6, -22.0 dB.
- It drops to approximately 2023.7, -22.5 dB.
- It rises to approximately 2023.8, -22.0 dB.
- It drops to approximately 2023.9, -22.5 dB.
- It rises to approximately 2024.0, -22.0 dB.

The line continues with light blue markers and a dashed dark green line through 2024 and into 2025.
- The line generally fluctuates between -22.0 dB and -23.0 dB during this period.
- The lowest point in this segment is around 2025.2, at approximately -23.5 dB.
- The line then rises to approximately 2025.3, -22.5 dB.
- It drops to approximately 2025.4, -23.0 dB.
- It rises to approximately 2025.5, -22.5 dB.
- It drops to approximately 2025.6, -23.0 dB.
- It rises to approximately 2025.7, -22.5 dB.
- It drops to approximately 2025.8, -23.0 dB.
- It rises to approximately 2025.9, -22.5 dB.
- The last visible point is around 2026.0, at approximately -22.8 dB.


Fecha

Figura 13: Serie  temporal Sentinel-1 SAR-VH (mediana mensual, buffer 500 m) sobre cinco
estaciones de muestreo del manglar de la CGSM entre 2018 y 2025. Los puntos estan coloreados
pOI SU anomalia 2-score (rojo backscatter anomalamente alto; azul backscatter anomalamente
bajo, indicativo de inundacion suelo desnudo) La franja gris representa el rango € 1 de cada
estacion.

La inspeccion visual de la   figura   figura 13 revela unl patron consistente con la narrativa de
recuperacion   post-La Niiia 2020   reportada en cuerpo del informe: las tres estaciones del
Complejo de Pajarales Caiio Palos, CP Aguas Negras y CP Luna experimentan una transicion
ascendente sostenida del backscatter VH entre 2020 y 2024, con incrementos del orden de 3 a 5 dB
respecto su linea base de 2018-2019. Este aumento de VH se interpreta como ua recuperacion
estructural del dosel manglar denso   recupera biomasa leriosa rugosidad   superficial, 1o
cual incrementa la   retrodispersion radarica complementaria al aumento del NDVI mediano
del manglar de 0,60 0,80 ya reportado en la figura figura El SAR aporta asi una evidencia
independiente de la regeneracion del bosque   que la teledeteccion optica por   si   sola nO puede
confirmar dado que el NDVI saturado no discrimina entre dosel ralo y dosel denso. La estacion
limnologica Punta Cerro, en contraste, mantiene UI comportamiento estable en torno los - 21 dB
sin tendencia neta; consistente con Su naturaleza de cuerpo lagunar permanente.

El analisis de correlacion cruzada de Pearson entre las series mensuales SAR-VH y NDVI z-score,
calculado para rezagos de cero tres meses sobre las ocho estaciones (tabla tabla 43), arroja lI
resultado metodologicamente robusto: las cuatro estaciones del Complejo de Pajarales presentan
correlaciones positivas significativas en rezago cero CP Aguas Negras +0,807 CP Luna
+0,731, Canio Clarin +0,640 y Caiio Palos +0,462, todas con p 0,001 lo cual
confirma que en zonas de manglar denso el SAR y el optico capturan la misma senal estructural de
biomasa del dosel y que la recuperacion post-2020 detectada por NDVI coincide temporalmente con
el incremento de backscatter Las cuatro estaciones de naturaleza limnologica de borde lagunar
~Isla Boqueron, Punta Cerro, Punta Chino y Rio Sevilla arrojan correlaciones no significativas
(lel 0,20, 0,17) , comportamiento esperable cuando la firma SAR responde la lamina de
agua y la firma Optica responde vegetacion de transicion sin una relacion causal directa. Este
contraste entre estaciones de manglar denso y estaciones de borde valida de manera independiente
la clasificacion espectral previamente reportada y refuerza el argumento de que el Complejo de
Pajarales constituye el nucleo funcional del manglar de la CGSM:

# 7.17 Hacia el Nivel 2 de Digital Twin: modulo de alertas tempranas

El   proyecto   incorpora U modulo de deteccion de alertas tempranas que articula
las series   temporales NDVI SAR-VH con los   quiebres bfast en uhla logica de semaforo
aplicable de manera operativa cada ua de las ocho estaciones de monitoreo. El script
src/python/alertas_manglar . Py clasifica   el estado actual de cada estacion en  tres categorias
estable (); alerta critica segin la   severidad de las   anomalias   observadas en
los iltimos   doce meses: el estado critico se activa cuando la anomalia NDVI del xltimo mes
registra -2 cuando se acumulan dos mas anomalias   de esta magnitud en el periodo
reciente; estado de alerta se dispara con anomalias moderadas entre y -2) en los
iltimos tres meses con una   frecuencia de dos anomalias en  el aiio; el estado estable
corresponde series  sin  desviaciones significativas_ El producto resultante se materializa en la
tabla outputs 'tables/alertas estaciones CSV en el mapa semaforo de la figura figura 14,
de manera   que   el monitor cartografico  estatico del informe se   transforma en UI componente
operativo de deteccion dinamica, caracteristico del nivel 2 del paradigma Digital Twin. Este modulo
es ejecutable de forma   periodica por ejemplo, mensualmente al ingresar nuevos composites
Sentinel-2 Sentinel-1 y constituye el prototipo funcional sobre el cual la tesis de Maestria en
curso  desarrollara la transicion al nivel 3 mediante la incorporacion de modelos predictivos de
tendencia Y simulacion de escenarios climaticos_

43

Tabla 43: Correlacion de Pearson entre la serie mensual Sentinel-1 SAR-VH y el NDVI Z-score
derivado de Sentinel-2 para rezagos temporales de cero a   tres meses, calculada   sobre las ocho
estaciones de muestreo entre 2018 y 2025. Los valores en negrita corresponden las correlaciones
significativas (p 0,001) sobre las cuatro estaciones de manglar denso del Complejo de Pajarales_

Tabla 44:

Estacion Naturaleza lag lag lag lag 3
CP Aguas Negras manglar +0,807 +0,788 +0,773 +0,758 85
CP Luna manglar +0,731 +0,710 +0,717 +0,722 83
Caiio Clarin manglar +0,640 +0,380 -0,025 -0,127 63
Caio Palos manglar +0,462 +0,406 +0,379 +0,434 64
Isla Boqueron limnologica +0,166 +0,192 +0,205 +0,226 70
Punta Cerro limnologica +0,008 +0,086 +0,043 +0,053 70
Punta Chino limnologica +0,134 +0,168 +0,178 +0,203 70
Rio Sevilla borde -0,159 -0,102 -0,077 -0,058

Semaforo de alertas CGSM Estado actual por estacion de monitoreo
(generado el 2026-05-23)

A scatter plot titled "Estado actual del manglar" (Current state of the mangrove) displays points on a coordinate system with "Latitud" (Latitude) on the y-axis and "Longitud" (Longitude) on the x-axis. The plot area is a light blue rectangle with a dark green border, spanning from Latitude 10.5 to 11.1 and Longitude -74.7 to -74.2. A grid is present in the background.

A legend in the top right corner indicates the status of the mangrove:
*   **Crítica** (Critical): Red square
*   **Alerta** (Alert): Orange square
*   **Estable** (Stable): Green square

There are 9 data points plotted, each represented by a circle with a black outline and a text label:

*   **CP_Luna**: Green circle, located at approximately Latitude 10.87, Longitude -74.55.
*   **CP_Aguas_Negras**: Green circle, located at approximately Latitude 10.8, Longitude -74.58.
*   **Cano_Palos**: Green circle, located at approximately Latitude 10.75, Longitude -74.45.
*   **Cano_Clarin**: Orange circle, located at approximately Latitude 10.6, Longitude -74.5.
*   **Rio_Sevilla**: Orange circle, located at approximately Latitude 10.88, Longitude -74.3.
*   **Punta_Chino**: Orange circle, located at approximately Latitude 10.95, Longitude -74.28.
*   **Punta_Cerro**: Green circle, located at approximately Latitude 10.98, Longitude -74.25.
*   **Boqueron**: Green circle, located at approximately Latitude 10.97, Longitude -74.23.
*   **Punta_Cerro_Boqueron**: Green circle, located at approximately Latitude 11.0, Longitude -74.25. This point is very close to "Punta_Cerro" and "Boqueron".

The y-axis ranges from 10.5 to 11.1 with major ticks at 10.5, 10.6, 10.7, 10.8, 10.9, 11.0, and 11.1.
The x-axis ranges from -74.7 to -74.2 with major ticks at -74.7, -74.6, -74.5, -74.4, -74.3, and -74.2.


Figura 14: Mapa semaforo del estado actual del manglar de la CGSM por estacion de monitoreo,
generado por el modulo de alertas tempranas. El color del circulo indica el estado clasificado ~verde
estable, amarillo en alerta, rojo critica partir de la severidad persistencia de las anomalias
NDVI z-score observadas en los ultimos doce meses_

44

Tabla 45: Estado actual del manglar de la CGSM por" estacion de monitoreo segun el modulo de
alertas tempranas, calculado sobre el corte temporal 2024-12 a 2025-12 utilizando las series NDVI y
SAR-VH ya construidas El campo actual corresponde al z-score NDVI del iltimo mes disponible

Tabla 46:

Estacion Estado 2 actual NDVI actual Razon principal
CP Aguas Negras estable +1,63 0,770 Sin anomalias en 12 meses
CP Luna estable +2,38 0,664 Sin anomalias en 12 meses
Caiio Palos estable +1,25 0,849 Sin anomalias en 12 meses
Isla Boqueron estable +0,81 0,308 Sin anomalias en 12 meses
Punta Cerro estable +0,15 0,145 Sin anomalias en 12 meses
Caiio Clarin alerta +0,31 0,735 2 anomalias en 12 meses
Punta Chino alerta +0,69 0,337 2 minimo 3 meses -1,38
Rio Sevilla alerta +0,61 0,215 minimo 3 meses -1,55; 2 anomalias

La ejecucion del modulo sobre el corte 2024-12 a 2025-12 arroja un panorama operativo coherente con
la narrativa de recuperacion post-La Nita 2020 sostenida por el cuerpo del informe: ninguna de las
ocho estaciones se encuentra en estado critico, cinco se clasifican como estables CP Aguas Negras
+1,63) , CP Luna +2,38) , Caio Palos +1,25) , Isla Boqueron +0,81) y Punta
Cerro +0,15) y tres permanecen bajo alerta Caiio Clarin, Punta Chino y Rio Sevilla
El analisis del subgrupo de alertas muestra que ninguna responde a una caida drastica del NDVI en
el iltimo mes (los actuales se mantienen positivos) sino la persistencia de anomalias historicas
en los doce meses previos (entre una y dos anomalias -1,38) , comportamiento esperable en
estaciones de borde lagunar transicion fluvial donde la variabilidad estacional natural es mas
amplia_ Es destacable que las cuatro estaciones del Complejo de Pajarales ~nicleo funcional del
manglar denso de la CGSM queden todas en estado estable; lo cual confirma de manera operativa
la recuperacion estructural sostenida del bosque en SU porcion central La distribucion de estados
cero criticas, tres alertas y cinco estables constituye la primera fotografia cuantitativa del estado
del ecosistema sustentada en uha logica reproducible; ejecutable mensualmente al ingreso de cada
nuevo composite Sentinel-2

# 7.18 Dashboard interactivo

Se   genero uil dashboard interactivo en formato HTML autocontenido mediante script
src/python/make_dashboard_html.PY, que construye el mapa con folium Earth   Engine
sirviendo las capas como teselas mediante mapId. La version vigente del dashboard opera sobre
el AOI acotado leido del archivo data/raw/cgsm_aoi acotado_4326.geojson integra 17 capas
tematicas organizadas en cuatro bloques. El bloque de estado del manglar comprende el NDVI
pOF periodo de referencia, el mapa de cambio NDVI (Actual Degradacion) y la clasificacion de
manglar pOr periodo (degradacion, recuperacion, actual). El bloque de dinamica de cobertura
comprende las capas de ganancia;,  perdida y estabilidad de manglar entre 2020 y 2024-2025. El
bloque de inundacion comprende la deteccion SAR de septiembre-octubre 2020 en agua abierta y

45

bajo dosel junto con la frecuencia historica de inundacion de la Global Flood Database 2001-2017
UI mapa de calor amarillo a purpura que cuenta el numero de eventos GFD que afecto cada pixel
del AOI El bloque de referencia contexto comprende el poligono del area de estudio, las
estaciones de monitoreo separadas por naturaleza espectral y la cartografia oficial de manglares
de Colombia escala 1:25.000 (INVEMAR, 2020) cargada como vectorial con tooltip interactivo
que muestra el area en hectareas, el tipo de cobertura y el departamento de cada poligono. El
dashboard se abre directamente en cualquier navegador web sin necesidad de Jupyter ni de software
especializado, asi constituye una herramienta de consulta accesible para gestores ambientales del
Plan de Manejo Ambiental del sitio Ramsar; Sus mapId Earth Engine tienen vigencia limitada
de algunas horas, en este  sentido conviene regenerar HTML poco antes de cada   sesion de
presentacion. La version preliminar del dashboard sobre el AOI envolvente, generada con geemap y
dependiente de un kernel Jupyter activo (HTML de 2,7 MB con widgets ipyleaflet embebidos) , se
conserva en el notebook legacy 06_dashboard. ipynb para trazabilidad metodologica.

# 8 Conclusiones

El  pipeline multilenguaje  desarrollado permitio caracterizar la  dinamica  espaciotemporal de la
cobertura de manglar en la CGSM durante el periodo 2013-2025 integrando analisis  de  series
temporales de NDVI en Python (929 registros mensuales que combinan Landsat Sentinel-2) ,
deteccion de quiebres con bfast en R, segmentacion automatica con SamGeo en Python; metricas
de fragmentacion en  Julia validacion cruzada con  datos SAR de inundacion cartografia de
referencia del Global Mangrove Watch: Los resultados principales reportados sobre el AOI acotado
(SFF CGSM VPI Salamanca, 835,3 km?) son los siguientes: primero, la identificacion de UI
quiebre estructural generalizado en 2016 detectado por bfast en de 8 estaciones sobre la serie
combinada 2013-2025 asociado al evento El Ninio 2015-2016, de septiembre de 2020 como el
segundo evento de mayor perturbacion NDVI negativo en 2 de 8 estaciones ~3 asociado
a La Nima 2020-2021, refinado mediante un analisis bfast unificado sobre las cuatro estaciones de
manglar denso que confirma quiebres especificos en 2020 sobre Caio Palos  (junio) y Caiio Clarin
(febrero, diciembre) , en 2022 sobre CP Aguas Negras (abril) y CP Luna (enero) , y un tercer bloque
de quiebres en 2023-2024 coincidente con el episodio El Niiio 2023 2024 visible en la serie ONI,
en U contexto historico de 14 eventos de inundacion documentados por la Global Flood Database
entre 2001 y 2017 con areas inundadas dentro del AOI acotado de hasta 299,2 km? (DFO 2625 .
febrero de 2005); segundo, la deteccion de 18 anomalias significativas 2 < -2) en la serie combinada
de 12 aiios, incluyendo 4 anomalias en VIPIS durante 2016 que solo fueron visibles al extender la
serie con Landsat 8; tercero, Um patron de contraccion del &rea clasificada con consolidacion
estructural sobre el AOI acotado el numero de parches de manglar pasa de 79 a 15 y el area
total clasificada se reduce de 12.425,6 4.037,0 ha entre la degradacion Y el estado actual, en tanto
que el area media de parche aumenta de 157,3 269,1 ha complementado con ua ganancia
generalizada de vigor vegetativo observable en la diferencia de NDVI entre 2020 y 2024-2025
(figura figura 2) y en la recuperacion del NDVI medialio del manglar (figura figura 4) que pasa
de valores cercanos 0,60 en mid-2020 valores estables alrededor de 0,80 desde 2022; cuarto, UI
aumento del indice de forma medio (MSI) de 0,51 a 1,46 y de la distancia media al vecino mas
cercano (NND) de 1,10 a 2,39 kmn; indicativos de bordes mas irregulares y aislamiento progresivo de
los parches sobrevivientes; quinto, la diferenciacion mediante SAR de dos mecanismos de afectacion
durante el evento de septiembre-octubre de 2020 inundacion de agua abierta sobre 15,93 km?
inundacion bajo dosel sobre 43,08 km? para UI total de 59,02 km? afectados (7,1 % del AOI
acotado) complementada con una dinamica hidrica de largo plazo (JRC 1984-20021) que muestra

46

perdida de 18,55 km? de agua permanente y ganancia compensatoria de 23,55 km?, en este sentido
el sistema redistribuye Su lamina de agua mas que la pierde; sexto, ua validacion doble contra
cartografia oficial y global INVEMAR 1:25.000 (Instituto de Investigaciones Marinas y Costeras;
2020) y ESA WoldCover v200 Zanaga et al,, 2022) sobre el AOI acotado que arroja Fl-scores
convergentes de 0,583 0,548 respectivamente, con Precision entre 0,768 y 0,811 Specificity
entre 0,944y 0,954, lo que constituye una mejora del 24 al 32 % sobre el Fl de 0,442 reportado en
el baseline envolvente preliminar y confirma cuantitativamente que el acotamiento los poligonos
oficiales del SFF VPI elimina los falsos positivos pOr  vegetacion riberana agropecuaria Sin
entrenamiento supervisado adicional; el acuerdo directo entre ambas cartografias de referencia es de
Fl 0,833, asi el clasificador del proyecto alcanza aproximadamente el 70 % del techo metodologico
realista que imponen las propias discrepancias enbre cartografias oficiales, en tanto que la Recall
sostenida en 0,43-0,45 indica ua subestimacion atribuible al umbral conservador NDVI 0,70;
septimo, Uil benchmark formal del clasificador supervisado Random Forest sobre la misma imagen
Sentinel-2 y las mismas referencias arroja un Fl-score de 0,826 frente a INVEMAR y 0,889 frente
WorldCover (tabla tabla 41) , lo cual representa mejoras del 42 % y 62 % respectivamente sobre
el clasificador por'   umbrales y resuelve la subestimacion de Recall que limitaba la cota superior
del modelo deterministico; las bandas SWIR (BlI y Bl2) y la distancia al agua emergen cOmo las
variables mas discriminantes para el manglar de la CGSM; octavo, la construccion de ua serie
temporal continua de Sentinel-1 SAR-VH (figura figura 13) sobre las ocho estaciones de muestreo
entre 2018 y 2025 extiende el US0 del radar mas alla del evento puntual de septiembre 2020
aporta sensibilidad ante perturbaciones sub-canopy invisibles al sensor optico, con  correlaciones
positivas altamente significativas entre SAR-VH y NDVI sobre el Complejo de Pajarales (CP Aguas
Negras +0,807 y CP Luna p +0,731 en rezago cero, ambas con 0,001, tabla tabla 43)
que validan independientemente la firma estructural del manglar denso; y noveno, la integracion
de las series NDVL, SAR-VH y los quiebres bfast en liI modulo operativo de alertas tempranas
(figura figura 14, tabla tabla 45) materializa el nivel 2 del paradigma Digital Twin transforma
el monitoreo cartografico estatico en UII sistema de deteccion dinamica; la ejecucion del modulo
sobre el corte 2024-12 a 2025-12 arroja cinco estaciones en estado estable ~incluidas las cuatro
de manglar denso del Complejo de Pajarales tres estaciones de borde en estado de alerta Rio
Sevilla; Punta Chino y Caiio Clarin, pOr persistencia de anomalias historicas ninguna en estado
critico, lo cual constituye la primera fotografia cuantitativa del estado del ecosistema sustentada en
ua logica reproducible y ejecutable de forma periodica al ingreso de nuevos composites Sentinel-2
y Sentinel-l_

Contrastando estos resultados con la literatura, conviene senalar que la cobertura total reportada
para la CGSM bajo el AOI acotado del orden de 4.000 12.000 hectareas seg U el periodo es
coherente con el rango estimado por el Global Mangrove Watch v3.0 para esta misma area en
ciclo 2018-2020 (Bunting et al, , 2022) , si bien el Fl-score de 0,548 alcanzado en la validacion contra
ESA WorldCover v200 sobre el AOI acotado es inferior al rango 0,80-0,90 reportado por Selvaraj y
Gallego-Perez (2023, para manglares del Pacifico colombiano utilizando una combinacion de Landsat
optico y SAR ALOS-2 con clasificador Random Forest _ La discrepancia se atribuye; en primer lugar
a que el enfoque metodologico aqui presentado descansa en umbrales espectrales sobre indices NDVI
y CMRI sin entrenamiento supervisado, en tanto que el flujo de Selvaraj y Gallego-Perez explota la
complementariedad optico-SAR y aprovecha la capacidad discriminativa del Random Forest sobre
vectores de caracteristicas multidimensionales; en segundo lugar, que el habitat del Pacifico
colombiano presenta ua menor heterogeneidad espectral cOnl vegetacion no-manglar comparada
con complejo lagunar de la CGSM; donde la vegetacion riberana, los pastizales inundables y los
salitrales comparten firmas espectrales con el manglar maduro. El analisis de tendencias mediante

z-scores sobre series Sentinel-2 reproduce metodologicamente la aproximacion de Raza et al. (2024)
sobre el manglar de Pakistan; con la diferencia de que aqui se extiende la serie con Landsat 8 para
alcanzar doce aiios de cobertura frente a los ocho del estudio original (2016-2023) que en
lugar de la prueba de Mann-Kendall con pendiente de Sen empleada pOr Raza et al,, se aplican
z-scores y bfast, lo que permite detectar quiebres estructurales asociados a eventos ENSO previos
al periodo Sentinel-2_

Entre las limitaciones tecnicas se identifican: la necesidad de remuestrear los composites RGB de
10 a 30 metros pOr restricciones de memoria para SamGeo (vit_ b) , lo que reduce la resolucion de
la segmentacion; la diferencia en la respuesta espectral entre Landsat 8 y Sentinel-2, que introduce
una discontinuidad en la serie combinada alrededor de 2018 ~visible en estaciones como VIPIS
(NDVI medio L8 0.090 vs S2 0,353) que podria influir en la deteccion de quiebres por bfast
el Fl-score de 0,548 sobre el AOI acotado que; si bien mejora en 24 % al baseline envolvente; sigue
indicando una subestimacion de la Recall pOL' el umbral conservador NDVI > 0,70 que deja fuera
manglar joven degradado detectado por WorldCover; y la aproximacion del calculo de areas en
Julia mediante conversion de coordenadas geograficas a metros. Se recomienda para trabajo futuro
acotar el area de estudio a los poligonos oficiales del SFF CGSM y la Via Parque Isla de Salamanca;
aplicar armonizacion espectral entre Landsat y Sentinel-2 para eliminar la discontinuidad en la serie;
implementar un clasificador Random Forest entrenado con puntos GMW para mejorar la precision
de la clasificacion: Como trabajo futuro inmediato se identifican cinco lineas. Primero, ampliar
red de estaciones IDEAM mas alla de las dos ya integradas El Banco (rio Magdalena central)
Ganaderia Caribe (rio Aracataca, Sierra Nevada) , validadas ademas por precipitacion CHIRPS sobre

las mismas cuencas aportantes con conVCr gencia entre ambas fuentes (tablas tabla 27 y tabla 29)
incorporando series de los rios Fundacion; Rio Frio y los tributarios secundarios del bajo Magdalena,
asimismo la validacion del regimen hidrico podria ganar resolucion espacial sobre las distintas vias
de entrada de agua al sistema lagunar y permitiria discriminar el aporte relativo de cada cuenca
al estado del manglar: Segundo, profundizar el analisis ENSO ya iniciado mediante la integracion
de los indices globales ONI y SOI de NOAA ver seccion de Forzamiento climatico global y tabla
tabla 25 COn metricas de eventos discretos como duracion acumulada de fases La Niiia, asi como
con indices regionales complementarios tales como el Atlantic Multidecadal Oscillation (AMO) que
podria modular la dinamica de la cuenca Magdalena. Tercero, refinar el clasificador para mejorar
la Recall en la medida en que el Fl actual de 0,58 frente al techo metodologico de 0,83 entre
las dos cartografias de referencia sugiere que un ajuste del umbral NDVI 0,60 unl clasificador
supervisado tipo Random Forest entrenado con muestras INVEMAR podria aprovechar el margen
disponible sin sacrificar la Precision alcanzada. Cuarto, extender el analisis bfast  unificado ya
realizado sobre las cuatro estaciones de manglar denso, tabla tabla 15 periodo 2013-2025
incorporando Landsat 8 sobre las mismas estaciones en la medida en que el analisis actual queda
limitado al rango Sentinel-2 (2018-2025) y por tanto no captura el evento El Niiio 2015-2016 que si
emerge en el analisis sobre las ocho estaciones; con la serie extendida tambien seria posible detectar
quiebres asociados episodios ENSO previos al periodo Sentinel-2 sobre las estaciones de manglar
especificamente. Quinto, ampliar la ventana temporal del periodo actual" por lo menos dos ciclos
anuales adicionales (julio 20025_junio 2027) , de modo que la contraccion observada en 2024-2025 se
pueda diferenciar entre fluctuacion intermedia y tendencia estable, se pueda validar la seial de
aislamiento progresivo de parches detectada en las metricas de fragmentacion del paisaje.

Pese a estas limitaciones, el pipeline demuestra la viabilidad de Un enfoque GeoAI multilenguaje para
el monitoreo costero y constituye u prototipo reproducible adaptable a otros sistemas lagunares
tropicales_ El dashboard interactivo generado se ofrece Como inSumo cartografico para el seguimiento
permanente que establece el Plan de Manejo Ambiental del sitio Ramsar CGSM Comision Conjunta

48

CGSM, 2026)_

# 9 Referencias

Beltran; J,, Rodriguez, J. C., Carbono, E. y Blanco, J. (2022) . Datos de monitoreo de la estructura
de los manglares de la Cienaga Grande de Santa Marta (Magdalena) [Conjunto de datos]. INVEMAR
https:, 'doi.org/10.15472 /Ofqdp4

Bunting, P Rosenqvist, Hilarides, L;, Lucas, R. M. Thomas; T,, Tadono; T,, Worthington;
T A Spalding, M,, Murray; N. J,, Rebelo, L-M. (2022) _ Global mangrove extent
change 1996 2020: Global Mangrove Watch version 3.05 Remote Sensing; 14(15) , 3657.
https: / /doi.org/10.3390/1s14153657

Comision Conjunta del sitio Ramsar CGSM. (2026, 2 de febrero). Plan de Manejo Ambiental del sitio
Ramsar Sistema Delta Estuarino del Rio Magdalena, Cienaga Grande de Santa Marta (vigencia
diez aiios) . Corporacion Autonoma Regional del Atlantico, Corporacion  Autonoma Regional del
Magdalena, Establecimiento Publico Ambiental Barranquilla Verde y Parques Nacionales Naturales
de Colombia, con acompanamiento tecnico del Ministerio de Ambiente y Desarrollo Sostenible

Lu; B. Francescutto, L;, Howie, S. Lin, H. Wu, Q., Hedley; N. Jamali, McDonald.
(2026). Exploring the concept of digital twins of wetlands for supporting ecosystem monitoring
and management _ Big Earth Data; 10(1) , 37-67 . https: / /doi.org/10.1080/20964471.2025.2480446

Murillo-Sandoval P. J. Fatoyinbo, L: y Simard, M: (2022). Mangroves cover change trajectories
1984-2020: The gradual decrease of mangroves in Colombia. Frontiers in Marine Science, 9, 892946_
https: / /doi.org/10.3389/fmars.2022.892946

Funk,; C. Peterson, P. Landsfeld, M,, Pedreros, D. Verdin, J,, Shukla, S. Husak, G Rowland.
J. Harrison; L", Hoell, A., Michaelsen, (2015). The climate hazards infrared  precipitation
with stations: new environmental record for  monitoring extremes   Scientific   Data; 150066_
https: / /doi.org/10.1038/sdata.2015.66

Giri, C., Ochieng, E Tieszen; L L,, Zhu; Z , Singh , A. Loveland, T,, Masek, J., y Duke; N. (2011)_
Status and distribution of mangrove forests of the world using earth observation satellite data
Global Ecology and Biogeography; 20(1), 154-159. https: / /doi.org/10.1111/j.1466-8238.2010.00584.xX

Goldberg, L , Lagomasino, D Thomas N. y Fatoyinbo, T. (2020) . Global declines in human-driven
mangrove loss_ Global Change Biology; 26(10), 5844-5855. https: / /doi.org/10.1llL/gcb.15275

Gomarasca, M: A. (2010). Basics of geomatics Applied Geomatics, 2(3), 137-146_ https: , '/doi.org/10.1007/s12518
010-0029-6

Gupta, K Mukhopadhyay; Giri, S. Chanda. Datta Majumdar, S.. Samanta,
Mitra, D., Samal, R. N., Pattnaik, A. K. Hazra, S. (2018) . An index for discrimination
of  mangroves from non-mangroves using LANDSAT OLI imagery. MethodsX, 5, 1129-1139.
https: 'doi.org/10.1016/j mex.2018.09.011

Hamilton; S. E,, y Casey; D. (2016). Creation of a high spatio-temporal resolution global database
of continuous mangrove   forest cover   for the 2lst   century (CGMFC-21). Global   Ecology and
Biogeography; 25(6) , 729-738_ https: , /doi.org/10.1111/geb.12449

Hersbach; H. Bell, B., Berrisford, P. Hirahara, S. Horanyi, A. Muioz-Sabater , J., Nicolas, J.
Peubey; C , Radu; R Schepers, D Simmons, A,,, Soci; C Abdalla, S,, Abellan, X , Balsamo,

49

G Bechtold P. Biavati, G. Bidlot, J. Bonavita, M: Thepaut , J.-N. (2020)_ The ERA5
global   reanalysis. Quarterly Journal of   the Royal   Meteorological  Society;   146(730) , 1999-2049.
https: / /doi.org/10.1002 /4j.3803

Instituto de Hidrologia, Meteorologia y Estudios Ambientales. (2026) . Series de caudal mensual del
rio Magdalena en El Banco (estacion 25027020) y del rio Aracataca en Ganaderia Caribe 'estacion
29067150) [Conjuntos de datos]. Portal DHIME. https: /dhime.ideam:gov.co/

Instituto de Investigaciones Marinas y Costeras  (2020)_ Cartografia de manglares de Colombia
escala 1:25.000 para Caribe y Pacifico. Procesamiento digital de imagenes en Google Earth Engine.

Instituto de Investigaciones Marinas y Costeras. (2024)_ Monitoreo de las condiciones ambientales
y los cambios estructurales y funcionales de las comunidades vegetales y de los recursos pesqueros
durante la  rehabilitacion de la Cienaga Grande de Santa Marta. Informe tecnico final (Vol. 23)
https: WWW invemar.Org co/inf-cgsm

Kirillov . A Mintun, E.: Ravi; N. Mao, H. Rolland, C. Gustafson , L. Xiao, T., Whitehead,
S., Berg; A C_ Lo, W_Y. Dollar , P. Girshick, R. (2023).  Segment anything: arXiv:
https: , 'doi.org/10.48550/arXiv.2304.02643

National Oceanic and Atmospheric  Administration; Climate Prediction Center (2026) . Oceanic
Nino Index (ONI) y Southern Oscillation Index (SOI) [Conjuntos de datos]. https:, WWW. cpc ncep.noaa-gov /data

Olofsson, P, Foody, G. M,, Herold, M.; Stehman, S. V. Woodcock; C. E: Wulder , M: A. (2014)_
Good practices for estimating area  and assessing accuracy of land change: Remote  Sensing  of
Environment, 148, 42-57 https: / /doi.org/10.1016/j.rse.2014.02.015

Raza, S. Zhang; J,, Zuo; S. Chen; J. (2024) . Time series   monitoring and analysis of
Pakistan 's   mangrove   using Sentinel-2 data_ Frontiers in Environmental   Science; 12, 1416450.
https: 'doi.org/10.3389/fenvs.2024.1416450

Selvaraj, J. Gallego-Perez, J. (2023). An enhanced approach to mangrove forest analysis in
the Colombian Pacific coast using optical and SAR data in Google Earth Engine: Remote Sensing
Applications: Society and Environment, 30, 100938. https: Idoi.org/10.1016/j rsase.2023.100938

Vinasco, J. S. Rodriguez; D. A , Velasquez, S., Quintero, D F Livni, R, Hernandez, F
(2020). Coverage changes detection at Cienaga Grande; Santa Marta Colombia using automatic
classification: The International Archives of the  Photogrammetry; Remote  Sensing  and  Spatial
Information  Sciences, XLII-3 , W12-2020, 195-200. https: / /doi.org/10.5194/isprs-archives-XLII-3-
W12-2020-195-2020

Wu, Q,, Osco, (2023). samgeo: Python package for segmenting   geospatial data
with the   Segment Anything Model (SAM). Journal of Open Source   Software; 8(89) , 5663_
https: / /doi.org/10.21105/joss.05663

Yancho, J. MS M,, Jones, T. G Gandhi, S. R,, Ferster, C. Lin, A., Glass, L. (2020). The
Google Earth Engine Mangrove Mapping Methodology (GEEMMM). Remote Sensing; 12(22) , 3758.
https: / /doi.org/10.3390/1s12223758

Zanaga, D. Van De Kerchove, R. Daems, D. De Keersmaecker W. Brockmann; C. Kirches_
G Wevers, J,, Cartus, 0 Santoro, M Fritz; S:, Lesiv , M. Herold; M. Tsendbazar , Nz
E Xu; P. Ramoino F Arino, 0. (2022) . ESA WorldCover 10 2021 0200. Zenodo
https: 'doi.org/10.5281 'zenodo.7254221

50

# 10 Anexo A: Configuracion del entorno Docker

El proyecto se ejecuta sobre el contenedor Docker sig unal vL.IL proporcionado para la asignatura,
con las siguientes modificaciones:

# Librerias Python adicionales instaladas
pip install earthengine-api geemap segment-geospatial leafmap
pip install rasterio geopandas xarray shapely folium rasterstats
pip install matplotlib pandas numpy scikit-learn contextily
pip install cdsapi netCDF4 descarga ERAS-Land desde CDS

Autenticacion Google Earth Eng ine
earthengine authenticate auth_mode-notebook

Autenticacion Clinate Data Store (ECMWF para ERAS-Land

1) Crear cuenta en https: / /cds.climate. copernicus eu/

2) Aceptar terminos del dataset reanalysis-era5-land-monthly-neans

3) Crear archivo ~/.cdsapirc con la URL la API key personales

Paquetes adicionales
install.packages (c ( "bfast "terra sf ggplot2" "tseries
stars "dplyr "tidyr readr" stringr" -

Paquetes Julia adicionales

using Pkg
Pkg add ["GeoJSON" "DataFrames CSV" "Statistics"] )

La autenticacion con GEE se realiza mediante el flujo gcloud auth application-default login
con quota project configurado; que genera credenciales almacenadas en ~ / config/gcloud/application_default_
El contenedor requiere U minimo de 8 GB de RAM asignados en Docker Desktop para ejecutar
SamGeo con el backbone vit_ b; con vit_ h se requieren al menos 12 GB Los composites RGB se
remuestrean de 10 a 30 metros antes de la segmentacion para reducir el consumo de memoria_

# 11 Anexo B: Estructura del repositorio GitHub

El  repositorio  publico esta  disponible en https: / (githubcom/linaql1 /proyecto-cgsm-curso   bajo
licencia MIT: La version anterior del proyecto (baseline marzo 2026 sobre AOI envolvente de 5.073
km?) permanece archivada en https: / /github.com/LinaQuinteroF / proyecto-cgsm para fines de
comparacion historica. El arbol de notebooks se organiza en dos series ~vigente y legacy pues a
lo largo del proyecto el area de estudio redefinio partir de los poligonos oficiales del RUNAP;
de modo que las cifras del cuerpo del informe v6 dejaron de ser comparables con las de la primera
iteracion_

# Serie vigente (v6) ejecutar en este orden para reproducir los resultados del informe:

notebooks/01_gee_acquisition. ipynb: Fase adquisicion   Sentinel-2 Landsat 8 sobre
AOL acotado

notebooks/02_time_series . ipynb: Fase 2 series temporales Y Z-scores (Python pandas)

notebooks/02b_bfast ndvi.R. ipynb: Fase 2 deteccion de quiebres con bfast (R)

notebooks/03_segmentation_acotado. ipynb: Fase segmentacion SamGeo   sobre AOI

51

acotado reproyeccion EPSG:9377

notebooks 04_fragmentation_acotado.ipynb: Fase 4 metricas de fragmentacion en Julia
sobre EPSG:9377

notebooks/04b_topologia_acotado. ipynb: Predicados topologicos DE-9IM clasificacion
de estaciones por naturaleza

notebooks/05_flooding_nasa_acotado. ipynb:  Validacion NASA SAR GFD JRC
restringida al AOI acotado

src/python/nake_dashboard_html.Py: Script que construye dashboard HTML
autocontenido con folium

notebooks/07_ era5_clima. ipynb: Forzamiento climatico ERA5-Land via cdsapi

notebooks/08_validacion_multilingual.ipynb: Comparacion series Python+GEE VS
R+stars

notebooks/O9b_datacube_extendido . ipynb: Construccion de los tres datacubes NetCDF
CF-1.8 (periodos, trimestral, Landsat anual)

notebooks/10_validacion_extendida. ipynb: Validacion contra GMW v4.0 restringida al
AOL acotado

notebooks/ 11_random_forest benchmark. ipynb: Benchmark  del  clasificador  supervisado
Random Forest en GEE vs   umbrales   NDVI/CMRI, validacion K-fold contra INVEMAR
1:25.000 y ESA WorldCover v200

notebooks '12_sentinell_sar serie. ipynb: Serie temporal continua Sentinel-l SAR-VH
2018-2025 sobre las ocho estaciones de muestreo + correlacion cruzada con NDVI pOr rezagos
3 meses

Serie legacy (baseline AOI envolvente) se conservan para trazabilidad historica del
repositorio, no para sostener conclusiones:

notebooks/03_segmentation. ipynb, notebooks/04_fragmentation. ipynb, notebooks/04b_topologia

notebooks/05_flooding_nasa. ipynb, notebooks/06_dashboard. ipynb, notebooks/09 datacube_netcd

# Scripts auxiliares y modulos compartidos:

src/python/utils.Py: funciones reutilizables (reproyeccion 9377 lectura perezosa
predicados DE-9IM clasificacion de estaciones)

src/python/aoi_acotado.Py: helper que une SFF CGSM + VPI Salamanca y reproyecta
EPSG:9377

src_ /python/build_cubos.Py: construccion de los   datacubes Net CDF trimestral anual
(resampling 30 m compresion zlib)

src /python/merge_cubo.Py: respaldo de concatenacion secuencial para evitar segfaults de
HDF5 con muchos archivos

src /python/alertas_manglar.Py: modulo Digital Twin Nivel 2, logica semaforo sobre series
NDVI + SAR-VH quiebres bfast por estacion

src/julia/04_fragmentacion. jl: script Julia con bloques legado (4326) y vigente (9377)

src/R/03_bfast_ndvi R: script R para deteccion de quiebres bfast en las 8 estaciones

src/R/O5_stars_ cubo. R: script que construye cubo stars desde TIFs extrae   sobre
estaciones

# Salidas y documentacion:

notebooks / README . md: guia de ejecucion con la separacion vigente legacy

outputs/tables/: archivos CSV COn resultados numericos

outputs/figures/: figuras estaticas (PNG), incluidas las dos   figuras del  datacube; la

52

importancia de variables del Random Forest (rf feature_ importance. png la serie
temporal Sentinel-1 SAR-VH (sar vh_serie_temporal.png= el   semaforo de alertas
(alertas_ semaforo.png

outputs/maps/dashboard_CGSM_final html: dashboard HTML autocontenido (~80 KB
generado pOr make_dashboard_html.Py

data/processed/ cubo/: datacubes NetCDF CF-1.8 (periodos 40 MB trimestral 275 MB
Landsat 119 MB

docs 'inforne_ final.qud, docs_ 'informe_ final html, docs informe_final.pdf: informe
Quarto reproducible y Sus renderizados

Los composites trimestrales y anuales en formato GeoTIFF , asi como los NetCDF de mayor tamaiio,
n0 se incluyen en el repositorio pOr restricciones de tamaio de GitHub; se regeneran ejecutando los
notebooks en orden secuencial con acceso a GEE autenticado.

# 12 Anexo C: Nota metodologica sobre el conteo de parches (Julia
VS Python)

Las cifras de   fragmentacion sobre el AOI acotado se reportan en dos implementaciones
independientes que arrojan conteos distintos del mismo conjunto de GeoJSON En Julia;
mediante algoritmo del shoelace   aplicado al anillo exterior de cada poligono Tabla
tbl-fragmentacion-acotado), se contabilizan 79 , 38 15 parches para los periodos de
degradacion, recuperacion actual   respectivamente, en tanto que en Python conl geopandas
usando el atributo geometry area Tabla tbl-topologia-acotado), se contabilizan 17, 17 y 15_
La discrepancia obedece a una diferencia metodologica especifica en el calculo del area pOr parche
cuando los poligonos contienen anillos interiores_

Cuando SamGeo segmenta Um parche grande de manglar atravesado pOr U canal hidraulico
como el Caiio Clarin el Canio Aguas Negras el GeoJSON resultante exporta ese parche como
u poligono con un anillo exterior que delimita la cobertura un1O mas anillos interiores que
representan el canal. La implementacion en geopandas calcula el area neta restando los huecos
siguiendo la definicion estandar del Simple Features Access para Polygon area mientras que la
implementacion Julia, al iterar sobre ring geom. coordinates [1] solo procesa el anillo exterior
reporta el area bruta del envolvente externo sin descontar los canales_ En consecuencia, parches
con grandes huecos internos quedan clasificados en el rango filtrado 1-5.000 ha por Julia pero por
debajo del umbral inferior pOr geopandas; lo que infla el conteo de parches Julia en periodos donde
la dinamica hidrica produce huecos detectables 2020 (degradacion) y 2022 (recuperacion) , cuando
los canales atraviesan manglar fragmentado por La Nifia y la rehabilitacion hidraulica y coincide
en periodo actual (2024-2025) donde los parches sobrevivientes son mas compactos sin canales
internos visibles.

Ambas mediciones tienen validez metodologica diferenciada. La version geopandas reporta el area
efectiva de cobertura de manglar; descontando agua interior es apropiada para indicadores de
superficie y validacion contra cartografia de referencia como GMW. La version Julia reporta el area
del envolvente del parche es apropiada para indicadores de extension del paisaje fragmentado
para   calculos de conectividad mediante distancia   entre envolventes_ Para  evitar confusion en
el informe; en la Tabla tbl-fragmentacion-acotado se reporta el conteo Julia con la columna
explicita Parches   (Julia) se  utiliza para indicadores de forma ~MSI y aislamiento ~NND
mientras que en la Tabla tbl-topologia-acotado se reporta el conteo geopandas y se utiliza para
indicadores de superficie y para el cruce con la frontera del AOI mediante predicados DE-9IM.

53

Tabla 47: Comparacion de correlaciones Pearson entre caudal mensual del rio Magdalena en El
Banco NDVI 2-score de la CGSM, calculadas sobre las dos variables hidrometricas disponibles:
caudal maximo mensual (variable original explorada) y caudal medio mensual (variable vigente del
cuerpo del informe)_ La columna reporta la diferencia entre ambas correlaciones_

Tabla 48:

Estacion El Banco Naturaleza Rezago meses Pmaximo Pmedio (vigente)
Caudal Manglar +0,185 +0,064 ~0,121
Caudal Manglar +0,123 +0,039 ~0,084
Caudal Manglar +0,164 +0,108 ~0,056
Caudal Manglar +0,277 +0,256 ~0,021
Caudal Limnologica +0,169 +0,181 +0,012
Caudal Limnologica +0,265 +0,233 ~0,032
Caudal Limnologica +0,127 +0,043 ~0,084
Caudal Limnologica +0,039 +0,050 +0,011

# 13 Anexo D: Analisis complementario con caudal maximo mensual
de El Banco

El cuerpo del informe reporta el acoplamiento entre el caudal medio mensual del rio Magdalena
en El Banco y el NDVI z-score de las estaciones de la CGSM (tabla tabla 27) , en este sentido
la eleccion del caudal medio sobre el caudal maximo obedece a la coherencia metodologica con la
estacion Ganaderia Caribe ~disponible unicamente en caudal medio mensual y al hecho de que
regimen sostenido representa mejor la dinamica hidrologica de fondo que los pulsos extremos
puntuales. Para trazabilidad metodologica se reporta continuacion el mismo analisis ejecutado
sobre la serie alternativa de caudal maximo mensual de El Banco variable tambien disponible
en el portal DHIME del IDEAM 144 observaciones continuas 2013-2025 con media 4.398,5 m*/s y
rango 1.654,8-7.322,8 m*/s), de modo que el lector pueda evaluar la sensibilidad de las correlaciones
a la eleccion de la variable hidrometrica

Las dos variables hidrometricas arrojan correlaciones positivas universales con NDVI signo del
acoplamiento es robusto la eleccion de la variable la correlacion mas alta sobre el manglar se
ubica en ambos casos en el rezago de tres meses, en este sentido las conclusiones cientificas del cuerpo
del informe sobre el regimen de fondo se sostienen en cualquiera de las dos representaciones_ La
principal diferencia se observa en los rezagos cortos Omaximo supera Pmedio por 0,08-0,12 unidades
en lag 0-1), lo cual es coherente con que los picos extremos del caudal maximo se asocian mas
rapidamente con cambios espectrales puntuales en el dosel mientras que el caudal medio captura el
efecto agregado del regimen sostenido. Para analisis ecohidrologicos del regimen general se prefiere
el caudal  medio mensual reportado en el cuerpo del informe; para analisis especificos de pulsos
extremos de avenida linea de trabajo futuro sugerida en las conclusiones el caudal maximo
mensual ofrece la representacion apropiada.

54

# 14 Anexo E: Fragmentos de codigo complementarios

El cuerpo del informe mantiene cuatro bloques representativos uno pOr fase y uno por lenguaje del
proyecto de modo que la lectura tecnica se concentre sobre los pasos canonicos de cada etapa. Los
demas fragmentos que sostienen operaciones secundarias del flujo lectura perezosa de datacubes
NetCDF calculo de z-scores en Python, descarga ERAs-Land via cdsapi, construccion del cubo
stars en R, predicados DE-9IM sobre parches reproyectados deteccion  Sentinel-1 SAR para
septiembre 2020 se documentan continuacion, Organizados tematicamente en tres apartados
que reproducen el orden logico de la cadena de procesamiento_

# 14.1 E.l Datacube multitemporal y series de tiempo

# 14.1.1 E.l.a Lectura perezosa del datacube NetCDF con xarray

El datacube trimestral materializado como NetCDF CF-1.8 se abre con evaluacion perezosa
mediante xarray open_dataset con argumento chunks de modo que las operaciones de seleccion
y reduccion se planifican como Uil grafo de computo dask y solo se materializan los pixeles necesarios
al invocar compute () _ Este patron resulta indispensable para los tres archivos del proyecto (40
MB, 275 MB y 119 MB) cuando se trabaja sobre la totalidad de las 31 laminas trimestrales sin
saturar la memoria del contenedor

import xarray as Xr
ds xr . open_dataset ( 'data/processed/cubo/ cgsm_datacube_trimestral.nc
chunks-{ 'time 512 y 512})
Atributos CF-1.8: Conventions institution, creator name crs origen
Acceso perezoso por  chunks; compute ( ) materializa cuando es necesario
ndvi_serie ds [ 'reflectance sel (band_ idx= NDVI median (din-[ 'x y']) . compute()

# 14.1.2 E.l.b Z-scores y deteccion de anomalias NDVI en Python

Sobre la serie combinada Landsat 8 + Sentinel-2 (929 observaciones mensuales) se calcula el z-score
temporal por estacion mediante groupby () transform() , lo que permite identificar las anomalias
pronunciadas como aquellas COn ~2 El  resultado alimenta tanto la tabla de eventos de
mortandad reportados en la Fase 2 como la logica del modulo de alertas tempranas del Nivel 2
del Digital Twin.

Z-scores deteccion de anomalias por estacion
df ['z_score df .groupby ( 'estacion' ) [ 'ndvi transform (
lambda X: (x mean ( ) ) x.std())
anomalias df [df [ '2 score' ] 2] sort_values ( '2 score

# 14.1.3 E.l.c Cubo stars en R y extraccion sobre estaciones INVEMAR

Como contraparte local del flujo Python+GEE de la Fase 2 , los TIFs trimestrales descar "gados
desde GEE se ensamblan en como UI cubo stars proxy cOn evaluacion perezosa hasta
que st extract materializa los valores sobre las ocho estaciones INVEMAR La salida
series_temporales_stars csv se contrasta contra serie_temporal ndvi definitiva csv para
sostener la validacion cruzada multilingiie Python reportada en la seccion homonima.

library(stars) library(sf) library(dplyr)
tifs < - list.files ( "data/processed/s2" pattern "NDVI . *| |.tifs" full names TRUE)

55

fechas as . Date (stringr: str_match (basename (tifs) (IIa{4})_Q(la) ") [, c (2, 3)] )
cubo read_stars (tifs, along list(time fechas) proxy TRUE)
serie < - st extract cubo _ st_transforn(estaciones_sf _ st crs(cubo) ) )

14.2 E.2 Reproyeccion al sistema oficial colombiano y topologia DE-9IM

# 14.2.1 E.2.a Lectura perezosa del raster, reproyeccion EPSG:9377 predicados
topologicos

Los rasters de mascara   producidos por SamGeo se inspeccionan abriendo archivo cOn
rasterio. open () para extraer dimensiones, CRS, resolucion y valor de NoData sin materializar la
grilla en memoria; los GeoJSON resultantes se reproyectan MAGNA-SIRGAS Origen Nacional
'EPSG:9377) estandar oficial del IGAC desde la Resolucion 471 de 2020 y sobre los parches
reproyectados se aplican los predicados topologicos intersects con la frontera del AOI y contains
con los puntos de muestreo INVEMAR, en ambos casos delegando en GEOS los mismos calculos
que sustentan PostGIS y JTS:

from src.python. utils import
raster metadata vector to_9377 , area_ha_9377 _
parches_borde , parches_ con_punto , EPSG_NACIONAL ,
# Inspeccion lazy del raster: metadatos sin cargar la grilla
meta raster metadata ( ' data/processed/ sangeo/mask_actual.tif' )
# Reproyeccion al sistema oficial colonbiano MAGNA-SIRGAS
vector_to_9377 ( 'data/processed/ sangeo /manglar actual.geojson
data/processed/ sangeo /manglar_actual 9377. geojson

# Predicados topologicos DE-9IM sobre los parches reproyectados
gdf area_ha 9377 (gpd.read_file ( ' data/processed/ sangeo/manglar actual 9377 . geojson' ) )
gdf parches_borde (gdf_ aoi) # intersects con la frontera
gdf parches_ con_punto (gdf estaciones) # contains con los puntos INVEMAR

# 14.3 E.3 Forzamiento climatico y deteccion SAR

# 14.3.1 E.3.a Descarga ERAs-Land mediante cdsapi y calculo de anomalias mensuales

La descarga del reanalisis ERAs-Land del ECMWF se realiza con cdsapi directamente desde
Climate Data Store, solicitando precipitacion total y temperatura dos metros sobre U bounding
box que envuelve la CGSM con buffer; los datos se reciben en NetCDF con convenciones CF
se cargan con xarray open dataset (chunks= aplicando ul patron perezoso, calculando la
climatologia mensual y la anomalia respecto ella para los rezagos cero a tres meses_

import cdsapi xarray as Xr
cdsapi.Client ()
retrieve ( ' reanalysis-eras-land-monthly-means
'product_type monthly_averaged_reanalysis
variable' ['total_precipitation 2m emperature' ] ,

56

year [str(y) for in range (2018 2026) ]
month [f {n: 02d} for in range (1 , 13) ]
time 00:00 ' area [11.20 _ -75.05 _ 10.30 , ~74.0 05]
format netcdf '} , data/raw/era5_land_cgsm_monthly.nc ' )
ds xr . open_dataset ( 'data /rawi era5_land_ cgsm_monthly.nc chunks-{ 'time 12})
anon ds. groupby ( 'time.month ds .groupby ( time.month mean ( time

# 14.3.2 E.3.b Deteccion de inundacion Sentinel-1 SAR para el evento de septiembre
2020

Para el evento de septiembre 2020 se realiza una deteccion de inundacion mediante Sentinel-1 SAR
(banda VH, modo IW), comparando el backscatter medio del periodo seco de referencia (enero
marzo 2020, 49 imagenes) contra el periodo de inundacion (septiembre-octubre 2020, 36 imagenes
Se aplica U umbral de 3 dB para inundacion en agua abierta y se identifica inundacion bajo dosel
de manglar mediante valores negativos de diferencia SAR donde el aumento del backscatter refleja
el scattering de doble rebote caracteristico de la interaccion agua tronco

s1_ dry ee ImageCollection ( ' COPERNICUS/S1 GRD ' )
filterDate ( 2020-01-01 2020-03-31 ' ) . select ( 'VH ' ) . median ()
s1_flood ee ImageCollection ( 'COPERNICUS/S1_GRD
filterDate ( '2020-09-01 2020-10-31 ) .select ( 'VH median ()
sar_diff s1 dry subtract (s1_flood)
flood_open sar_diff.gt (3) . selfMask () # agua abierta
flood_canopy sar diff.lt(-2) selfMask() # bajo dosel

ndo es necesario ndvi serie = ds[ reflectance | sel(band idx=='NDVI' ) median(dim= [*x ,y' ]) computed

### E.l.b Z-scores y deteccion de anomalias NDVI en Python

Sobre la serie combinada Landsat Sentinel-2 (929 observaciones mensuales) se calcula el

python
Z-scores deteccion de anomalias por estacion
df [ 'z_score df .groupby ( estacion' ) [ 'ndvi transform (
lambda X: (x mean ( ) ) x.std())
anomalias df [df [ 'z_score' ] -2] sort_values ( 'z_score

# 14.3.3 E.l.c Cubo stars en R y extraccion sobre estaciones INVEMAR

Como contraparte local del flujo Python+GEE de la Fase 2 , los TIFs trimestrales descar "gados
desde GEE se ensamblan en como UI cubo stars proxy cOn evaluacion perezosa hasta
que st extract materializa los valores sobre las ocho estaciones INVEMAR La salida
series_temporales_stars csv se contrasta contra serie_temporal ndvi definitiva csv para
sostener la validacion cruzada multilingiie Python R reportada en la seccion homonima.

library(stars) library(sf) library(dplyr)
tifs < - list.files ( "data/processed/s2" pattern "NDVI . *| |.tifs" full names TRUE)
fechas < - as.Date(stringr: str match (basename(tifs) _ "(|d{4})_ Q(1d) ") [, (2, 3)] )
cubo read_stars (tifs, along list(time fechas) proxy TRUE)

57

serie st extract cubo st_transforn(estaciones_sf st crs (cubo) ) )

# 14.4 E.2 Reproyeccion al sistema oficial colombiano y topologia DE-9IM

# 14.4.1 E.2.a Lectura perezosa del raster, reproyeccion EPSG:9377 predicados
topologicos

Los rasters de mascara   producidos por SamGeo se inspeccionan abriendo archivo cOn
rasterio . open () para extraer dimensiones, CRS resolucion y valor de NoData sin materializar la
grilla en memoria; los GeoJSON resultantes se reproyectan MAGNA-SIRGAS Origen Nacional
(EPSG:9377) estandar oficial del IGAC desde la Resolucion 471 de 2020 y sobre los parches
reproyectados se aplican los predicados topologicos intersects con la frontera del AOI y contains
con los puntos de muestreo INVEMAR, en ambos casos delegando en GEOS los mismos calculos
que sustentan PostGIS y JTS.

from src.python. utils import
raster metadata vector to_9377 , area ha 9377
parches borde _ parches_ con_punto , EPSG_NACIONAL ,
# Inspeccion lazy del raster metadatos Sin cargar la grilla
meta raster_metadata( data/processed/sangeo/mask_actual.tif
# Reproyeccion al sistema oficial colombiano MAGNA-SIRGAS
vector to_ 9377 ( ' data/processed/ sangeo /manglar actual.geojson
data/processed/ sangeo/manglar_actual_9377. geojson

# Predicados topologicos DE-9IM sobre los parches reproyectados
gdf area_ha_9377 (gpd.read_file ( ' data/processed/ sangeo/manglar actual_9377. geojson' ) )
gdf parches_borde (gdf aoi) # intersects con la frontera
gdf parches con_punto (gdf estaciones) # contains con los puntos INVEMAR

# 14.5 E.3 Forzamiento climatico y deteccion SAR

# 14.5.1 E.3.a Descarga ERAs-Land mediante cdsapi y calculo de anomalias mensuales

La descarga del reanalisis ERAs-Land del ECMWF se realiza con cdsapi directamente desde el
Climate Data Store, solicitando precipitacion total y temperatura dos metros sobre U bounding
box que envuelve la CGSM cOnl buffer; los datos se reciben en NetCDF con convenciones CF
se cargan cOn xarray. open dataset (chunks= aplicando U patron perezoso, calculando la
climatologia mensual y la anomalia respecto a ella para los rezagos cero a tres meses_

import cdsapi , xarray as Xr
cdsapi.Client ()
retrieve ( 'reanalysis-era-land-monthly-means
'product_type monthly_averaged_reanalysis
variable ' ['total_precipitation 2m_temperature' ] ,
year [str(y) for in range (2018 , 2026) ]
month [f {n: 02d} for in range (1, 13) ] .

58

'time 00:00 area [11.20 75.05 10.30 -74.05]
format netcdf } , data/raw/era_land_cgsm_monthly.nc
ds xr . open dataset ( 'data/raw/era5_land_ cgsm_monthly nc chunks-{ 'time 12})
anon ds. groupby ( 'time .month ds . groupby ( 'time.month mean ( time

# 14.5.2 E.3.b Deteccion de inundacion Sentinel-1 SAR para el evento de septiembre
2020

Para el evento de septiembre 2020 se realiza una deteccion de inundacion mediante Sentinel-1 SAR
(banda VH,  modo IW) , comparando el backscatter medio del periodo seco de referencia enero
marzo 2020, 49 imagenes) contra el periodo de inundacion (septiembre-octubre 2020, 36 imagenes
Se aplica U umbral de 3 dB para inundacion en agua abierta y se identifica inundacion bajo dosel
de manglar mediante valores negativos de diferencia SAR donde el aumento del backscatter refleja
el scattering de doble rebote caracteristico de la interaccion agua-tronco

s1_ dry ee ImageCollection ( ' COPERNICUS/S1 GRD ' )
filterDate ( 2020-01-01 2020-03-31 ' ) . select ( 'VH ' ) . median ()
s1_flood ee ImageCollection ( ' COPERNICUS /S1_( GRD '
filterDate ( '2020-09-01 2020-10-31' ) . select ( 'VH ' ) . median ()
sar_diff s1_dry.subtract (s1_flood)
flood_open sar_diff.gt (3) . selfMask () # agua abierta
flood_canopy sar_diff.lt(-2) .selfMask() # bajo dosel

59