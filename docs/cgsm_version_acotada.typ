// Some definitions presupposed by pandoc's typst output.
#let blockquote(body) = [
  #set text( size: 0.92em )
  #block(inset: (left: 1.5em, top: 0.2em, bottom: 0.2em))[#body]
]

#let horizontalrule = line(start: (25%,0%), end: (75%,0%))

#let endnote(num, contents) = [
  #stack(dir: ltr, spacing: 3pt, super[#num], contents)
]

#show terms: it => {
  it.children
    .map(child => [
      #strong[#child.term]
      #block(inset: (left: 1.5em, top: -0.4em))[#child.description]
      ])
    .join()
}

// Some quarto-specific definitions.

#show raw.where(block: true): set block(
    fill: luma(230),
    width: 100%,
    inset: 8pt,
    radius: 2pt
  )

#let block_with_new_content(old_block, new_content) = {
  let d = (:)
  let fields = old_block.fields()
  fields.remove("body")
  if fields.at("below", default: none) != none {
    // TODO: this is a hack because below is a "synthesized element"
    // according to the experts in the typst discord...
    fields.below = fields.below.abs
  }
  return block.with(..fields)(new_content)
}

#let empty(v) = {
  if type(v) == str {
    // two dollar signs here because we're technically inside
    // a Pandoc template :grimace:
    v.matches(regex("^\\s*$")).at(0, default: none) != none
  } else if type(v) == content {
    if v.at("text", default: none) != none {
      return empty(v.text)
    }
    for child in v.at("children", default: ()) {
      if not empty(child) {
        return false
      }
    }
    return true
  }

}

// Subfloats
// This is a technique that we adapted from https://github.com/tingerrr/subpar/
#let quartosubfloatcounter = counter("quartosubfloatcounter")

#let quarto_super(
  kind: str,
  caption: none,
  label: none,
  supplement: str,
  position: none,
  subrefnumbering: "1a",
  subcapnumbering: "(a)",
  body,
) = {
  context {
    let figcounter = counter(figure.where(kind: kind))
    let n-super = figcounter.get().first() + 1
    set figure.caption(position: position)
    [#figure(
      kind: kind,
      supplement: supplement,
      caption: caption,
      {
        show figure.where(kind: kind): set figure(numbering: _ => numbering(subrefnumbering, n-super, quartosubfloatcounter.get().first() + 1))
        show figure.where(kind: kind): set figure.caption(position: position)

        show figure: it => {
          let num = numbering(subcapnumbering, n-super, quartosubfloatcounter.get().first() + 1)
          show figure.caption: it => {
            num.slice(2) // I don't understand why the numbering contains output that it really shouldn't, but this fixes it shrug?
            [ ]
            it.body
          }

          quartosubfloatcounter.step()
          it
          counter(figure.where(kind: it.kind)).update(n => n - 1)
        }

        quartosubfloatcounter.update(0)
        body
      }
    )#label]
  }
}

// callout rendering
// this is a figure show rule because callouts are crossreferenceable
#show figure: it => {
  if type(it.kind) != str {
    return it
  }
  let kind_match = it.kind.matches(regex("^quarto-callout-(.*)")).at(0, default: none)
  if kind_match == none {
    return it
  }
  let kind = kind_match.captures.at(0, default: "other")
  kind = upper(kind.first()) + kind.slice(1)
  // now we pull apart the callout and reassemble it with the crossref name and counter

  // when we cleanup pandoc's emitted code to avoid spaces this will have to change
  let old_callout = it.body.children.at(1).body.children.at(1)
  let old_title_block = old_callout.body.children.at(0)
  let old_title = old_title_block.body.body.children.at(2)

  // TODO use custom separator if available
  let new_title = if empty(old_title) {
    [#kind #it.counter.display()]
  } else {
    [#kind #it.counter.display(): #old_title]
  }

  let new_title_block = block_with_new_content(
    old_title_block, 
    block_with_new_content(
      old_title_block.body, 
      old_title_block.body.body.children.at(0) +
      old_title_block.body.body.children.at(1) +
      new_title))

  block_with_new_content(old_callout,
    block(below: 0pt, new_title_block) +
    old_callout.body.children.at(1))
}

// 2023-10-09: #fa-icon("fa-info") is not working, so we'll eval "#fa-info()" instead
#let callout(body: [], title: "Callout", background_color: rgb("#dddddd"), icon: none, icon_color: black, body_background_color: white) = {
  block(
    breakable: false, 
    fill: background_color, 
    stroke: (paint: icon_color, thickness: 0.5pt, cap: "round"), 
    width: 100%, 
    radius: 2pt,
    block(
      inset: 1pt,
      width: 100%, 
      below: 0pt, 
      block(
        fill: background_color, 
        width: 100%, 
        inset: 8pt)[#text(icon_color, weight: 900)[#icon] #title]) +
      if(body != []){
        block(
          inset: 1pt, 
          width: 100%, 
          block(fill: body_background_color, width: 100%, inset: 8pt, body))
      }
    )
}



#let article(
  title: none,
  subtitle: none,
  authors: none,
  date: none,
  abstract: none,
  abstract-title: none,
  cols: 1,
  lang: "en",
  region: "US",
  font: "libertinus serif",
  fontsize: 11pt,
  title-size: 1.5em,
  subtitle-size: 1.25em,
  heading-family: "libertinus serif",
  heading-weight: "bold",
  heading-style: "normal",
  heading-color: black,
  heading-line-height: 0.65em,
  sectionnumbering: none,
  toc: false,
  toc_title: none,
  toc_depth: none,
  toc_indent: 1.5em,
  doc,
) = {
  set par(justify: true)
  set text(lang: lang,
           region: region,
           font: font,
           size: fontsize)
  set heading(numbering: sectionnumbering)
  if title != none {
    align(center)[#block(inset: 2em)[
      #set par(leading: heading-line-height)
      #if (heading-family != none or heading-weight != "bold" or heading-style != "normal"
           or heading-color != black) {
        set text(font: heading-family, weight: heading-weight, style: heading-style, fill: heading-color)
        text(size: title-size)[#title]
        if subtitle != none {
          parbreak()
          text(size: subtitle-size)[#subtitle]
        }
      } else {
        text(weight: "bold", size: title-size)[#title]
        if subtitle != none {
          parbreak()
          text(weight: "bold", size: subtitle-size)[#subtitle]
        }
      }
    ]]
  }

  if authors != none {
    let count = authors.len()
    let ncols = calc.min(count, 3)
    grid(
      columns: (1fr,) * ncols,
      row-gutter: 1.5em,
      ..authors.map(author =>
          align(center)[
            #author.name \
            #author.affiliation \
            #author.email
          ]
      )
    )
  }

  if date != none {
    align(center)[#block(inset: 1em)[
      #date
    ]]
  }

  if abstract != none {
    block(inset: 2em)[
    #text(weight: "semibold")[#abstract-title] #h(1em) #abstract
    ]
  }

  if toc {
    let title = if toc_title == none {
      auto
    } else {
      toc_title
    }
    block(above: 0em, below: 2em)[
    #outline(
      title: toc_title,
      depth: toc_depth,
      indent: toc_indent
    );
    ]
  }

  if cols == 1 {
    doc
  } else {
    columns(cols, doc)
  }
}

#set table(
  inset: 6pt,
  stroke: none
)

#set page(
  paper: "us-letter",
  margin: (x: 1.25in, y: 1.25in),
  numbering: "1",
)

#show: doc => article(
  title: [Pipeline multilenguaje para el monitoreo del manglar de la Ciénaga Grande de Santa Marta (2013-2025)],
  authors: (
    ( name: [Lina María Quintero Fonseca],
      affiliation: [Maestría en Geomática, Universidad Nacional de Colombia],
      email: [lmquinterof\@unal.edu.co] ),
    ),
  date: [2026-05-25],
  lang: "es",
  toc_title: [Tabla de contenidos],
  toc_depth: 3,
  cols: 1,
  doc,
)

#block[
#heading(
level: 
1
, 
numbering: 
none
, 
[
Resumen
]
)
]
La Ciénaga Grande de Santa Marta (CGSM, sitio Ramsar Nº 562, Caribe colombiano) atravesó entre 2013 y 2025 dos eventos del El Niño-Southern Oscillation de signo opuesto que afectaron su cobertura de manglar. El presente trabajo caracterizó la dinámica espaciotemporal de ese manglar sobre los 835,3 km² del área protegida oficial mediante un pipeline multilenguaje (Python, R y Julia) que integró 929 observaciones mensuales del Índice de Vegetación de Diferencia Normalizada (NDVI) combinadas a partir de Landsat 8 y Sentinel-2, segmentación promptable con SamGeo, métricas de fragmentación en EPSG:9377, detección de inundación con Sentinel-1 SAR-VH, y cuatro forzamientos climático-hidrológicos (ERA5-Land, ENSO ONI/SOI, caudal IDEAM y precipitación CHIRPS). El algoritmo bfast identificó quiebres estructurales generalizados en 2016 ---asociados al evento El Niño 2015--2016--- y un evento de mortandad puntual en septiembre 2020 bajo La Niña, con 43,08 km² de inundación bajo dosel detectada por radar. La cobertura se contrajo de 12.426 a 4.037 ha entre 2020 y 2024--2025 con consolidación estructural (área media de parche 157 → 269 ha) y el NDVI mediano del dosel se recuperó de 0,60 a 0,80 desde 2022. La validación doble contra INVEMAR 1:25.000 y ESA WorldCover v200 arrojó F1 = 0,583 y 0,548 para el clasificador por umbrales, y F1 = 0,826 y 0,889 para Random Forest. El pipeline materializa el Nivel 2 del paradigma Digital Twin mediante un módulo operativo de alertas tempranas y constituye un prototipo reproducible transferible a otros sistemas lagunares tropicales.

#strong[Palabras clave:] manglar, NDVI, bfast, Sentinel-2, Sentinel-1 SAR, ENSO, Google Earth Engine, pipeline multilenguaje, Ciénaga Grande de Santa Marta.

= Introducción
<introducción>
La Ciénaga Grande de Santa Marta constituye el sistema lagunar costero más extenso de Colombia y un humedal Ramsar reconocido por su valor ecológico y socioeconómico, en tanto que sus bosques de manglar regulan el flujo hídrico, protegen la costa frente a marejadas y sostienen la pesca artesanal del corredor Tasajera--Pueblo Viejo--Buenavista. Desde la década de los noventa este ecosistema ha experimentado ciclos recurrentes de degradación y recuperación asociados a la hipersalinización crónica que sigue al colapso hidrológico de la carretera Ciénaga--Barranquilla, a la presión agropecuaria sobre los bordes y a la intensificación de los eventos El Niño-Southern Oscillation (ENSO), particularmente La Niña @invemar2024. La reapertura de cinco canales hidráulicos entre 1996 y 1998 promovió una recuperación parcial, pero la dinámica del sistema continúa siendo inestable y los ciclos no se han caracterizado a alta resolución espaciotemporal con métodos reproducibles.

El monitoreo satelital de manglares ha avanzado en las últimas tres décadas: Giri et al. #cite(<giri2011>, form: "year") produjeron el primer inventario global moderno sobre Landsat circa-2000, Hamilton y Casey #cite(<hamilton2016>, form: "year") extendieron la observación a una serie temporal anual continua y, con el lanzamiento de Sentinel-2, la revisita de cinco días y la resolución espacial de diez metros permitieron construir series densas que capturan la variabilidad estacional e interanual de la cobertura vegetal costera. La narrativa dominante en la literatura global atribuye la pérdida de manglar a la presión antrópica directa @goldberg2020, pero este marco invisibiliza las pérdidas graduales que dominan en geografías como la colombiana, donde Murillo-Sandoval et al. #cite(<murillo2022>, form: "year") documentaron 48.000 hectáreas de disminución con LandTrendr, dominadas por degradación de manglar denso a otra vegetación (38.469 ± 2.829 ha) antes que por conversión abrupta.

En la CGSM específicamente, el INVEMAR realiza monitoreo continuo desde 1996 sobre seis estaciones permanentes con datos publicados en GBIF @beltran2022, y Vinasco et al. #cite(<vinasco2020>, form: "year") cuantificaron cambios de cobertura entre 2013 y 2018 sobre 119 escenas Landsat-8 con Random Forest sin aislar la cobertura de manglar. La aparición de modelos de fundación como el Segment Anything Model adaptado a datos geoespaciales a través de SamGeo @wu2023 abre una vía para la segmentación promptable de imágenes satelitales sin grandes conjuntos de datos etiquetados, vía que este proyecto aprovecha para complementar la clasificación supervisada con un enfoque de modelos de fundación. La integración de Google Earth Engine como plataforma de procesamiento @yancho2020 permite ejecutar todo el flujo en la nube sin requerir infraestructura computacional local.

El presente estudio responde a la siguiente pregunta de investigación: #emph[¿cómo ha variado la cobertura, la fragmentación y el vigor del manglar de la CGSM entre 2013 y 2025, y qué evidencia cuantitativa permite atribuir las perturbaciones detectadas a forzamientos climáticos asociados al evento La Niña 2020--2021?] Para responderla se desarrolla un pipeline multilenguaje que integra Python, R y Julia según la fortaleza disciplinar de cada lenguaje y que produce resultados verificables mediante cuatro validaciones cruzadas formales y dos cartografías oficiales de referencia.

= Materiales y métodos
<materiales-y-métodos>
== Área de estudio y delimitación
<área-de-estudio-y-delimitación>
El área de estudio comprende los 835,3 km² del área protegida oficial conformada por la unión del Santuario de Fauna y Flora CGSM y la Vía Parque Isla de Salamanca, extraídos del Registro Único Nacional de Áreas Protegidas (RUNAP) (Fig. #ref(<fig-area-estudio>, supplement: [Fig.])). Esta delimitación reemplaza una iteración preliminar sobre un AOI envolvente de 5.073 km² ---que incluía vegetación riberana, salitral y zonas agropecuarias--- y garantiza la comparabilidad con la cartografía oficial colombiana de manglares 1:25.000 @invemar2020 y con el Global Mangrove Watch v3.0 @bunting2022. Se definieron ocho estaciones de muestreo: cinco con coordenadas exactas del dataset INVEMAR-GBIF @beltran2022 ---Isla Boquerón, Punta Cerro, Punta Chino, Río Sevilla y Caño Palos--- y tres complementarias sobre cobertura de manglar verificada mediante NDVI \> 0,4 en composites Sentinel-2 de 2024 ---Caño Clarín, CP Luna y CP Aguas Negras---.

#figure([
#box(image("../outputs/figures/mapa_area_estudio.png", width: 90.0%))
], caption: figure.caption(
position: bottom, 
[
Localización del área de estudio. (a) Colombia con el departamento del Magdalena resaltado; (b) departamento del Magdalena con el bounding box del AOI acotado; (c) composite Sentinel-2 RGB del periodo actual (2024--2025) con el polígono del AOI (835 km², rojo) y las cinco estaciones INVEMAR-GBIF (triángulos rojos).
]), 
kind: "quarto-float-fig", 
supplement: "Fig.", 
)
<fig-area-estudio>


== Datos y fuentes
<datos-y-fuentes>
El pipeline integró ocho fuentes públicas (Tabla #ref(<tbl-fuentes>, supplement: [Tabla])). La cobertura óptica de alta resolución provino de Sentinel-2 MSI L2A (789 imágenes 2018--2025) complementada con Landsat 8/9 OLI (345 registros 2013--2017), todas accedidas vía Google Earth Engine con filtro de cobertura nubosa inferior al 20 % y máscara QA60. Para el evento de inundación de septiembre 2020 se procesaron 85 imágenes Sentinel-1 SAR (banda VH, modo IW, órbita descendente). La cartografía de referencia para la validación se obtuvo de INVEMAR 1:25.000 @invemar2020 vía servicio ArcGIS REST y de ESA WorldCover v200 @zanaga2022 vía Earth Engine. El forzamiento climático combinó ERA5-Land del ECMWF descargado con `cdsapi`, los índices ENSO ONI y SOI del Climate Prediction Center de la NOAA, el caudal medio mensual del río Magdalena en la estación El Banco (código IDEAM 25027020) y del río Aracataca en Ganadería Caribe (código 29067150), y la precipitación satelital CHIRPS v2.0 @funk2015 sobre las dos cuencas aportantes.

#figure([
#table(
  columns: (28%, 18%, 18%, 36%),
  align: (auto,auto,auto,auto,),
  table.header([Fuente], [Tipo], [Periodo], [Uso],),
  table.hline(),
  [Sentinel-2 MSI L2A], [Óptico 10 m], [2018--2025], [Índices espectrales, segmentación SamGeo],
  [Landsat 8/9 OLI], [Óptico 30 m], [2013--2017], [Serie histórica NDVI],
  [Sentinel-1 SAR-VH], [Radar], [2018--2025], [Inundación bajo dosel + serie continua],
  [Global Flood Database], [Inundación], [2001--2017], [Contexto histórico],
  [ERA5-Land], [Reanálisis], [2018--2025], [Precipitación + temperatura local],
  [ENSO ONI/SOI], [Índices], [2013--2025], [Forzamiento global],
  [Caudal IDEAM-DHIME], [Hidrométrico], [2013--2025], [Magdalena (El Banco) + Aracataca],
  [CHIRPS v2.0], [Precipitación], [2013--2025], [Cuencas aportantes],
  [INVEMAR 1:25.000], [Cartografía], [2020], [Validación nacional],
  [ESA WorldCover v200], [Cartografía], [2021], [Validación global],
)
], caption: figure.caption(
position: top, 
[
Fuentes de datos integradas en el pipeline.
]), 
kind: "quarto-float-tbl", 
supplement: "Tabla", 
)
<tbl-fuentes>


== Arquitectura multilingüe
<arquitectura-multilingüe>
La arquitectura distribuye las tareas entre tres lenguajes según la fortaleza disciplinar de cada uno (Fig. #ref(<fig-flujo>, supplement: [Fig.])). Python ejecutó la adquisición en Google Earth Engine, la segmentación con SamGeo (backbone vit\_b sobre composites RGB remuestreados a 30 m), la construcción del datacube NetCDF CF-1.8 con `xarray` y `rioxarray`, el clasificador Random Forest y la generación del dashboard interactivo con `folium`. R se reservó para los quiebres bfast @verbesselt2010 sobre las series mensuales combinadas Landsat 8 + Sentinel-2 (`h = 0,10`), la construcción del cubo `stars` como contraparte local del flujo Python+GEE y las réplicas estadísticas con `tidyverse`. Julia procesó las métricas de fragmentación del paisaje (NP, MSI, NND) sobre miles de polígonos reproyectados al sistema oficial colombiano MAGNA-SIRGAS Origen Nacional (EPSG:9377) mediante el algoritmo del cordón, y los predicados topológicos DE-9IM con `LibGEOS.jl`, la misma biblioteca GEOS que sustenta PostGIS y GeoPandas. Todo el flujo se ejecutó dentro de un contenedor Docker reproducible (`sig_unal v1.11`).

#figure([
#box(image("../outputs/figures/flujo_metodologia.png", width: 95.0%))
], caption: figure.caption(
position: bottom, 
[
Flujo metodológico del proyecto. Seis fases secuenciales con validación cruzada entre Python, R y Julia, todas ejecutadas dentro del contenedor Docker `sig_unal v1.11` que garantiza la reproducibilidad bit a bit del análisis.
]), 
kind: "quarto-float-fig", 
supplement: "Fig.", 
)
<fig-flujo>


== Análisis de series temporales
<análisis-de-series-temporales>
Las series mensuales de NDVI se extrajeron sobre buffers de 500 m alrededor de cada estación mediante `reduceRegion` en Earth Engine. La combinación de Landsat 8 (factor de escala $times 0 \, 0000275 - 0 \, 2$ según especificación USGS) y Sentinel-2 produjo 929 observaciones mensuales que cubren doce años. Sobre esa serie se calculó el z-score temporal por estación, definiendo como anomalías significativas aquellas con $z < - 2$. El algoritmo bfast se aplicó en R con descomposición armónica en dos iteraciones para detectar quiebres estructurales asociados a eventos ENSO. Las cuatro estaciones de manglar denso del Complejo de Pajarales se analizaron por separado para refinar la atribución del episodio La Niña 2020--2021.

== Segmentación y métricas de fragmentación
<segmentación-y-métricas-de-fragmentación>
Se aplicó SamGeo con backbone vit\_b sobre los composites RGB de tres periodos de referencia: degradación (julio--diciembre 2020), recuperación (enero--junio 2022) y actual (julio 2024--junio 2025). Las máscaras vectorizadas se filtraron por área entre 1 y 5.000 ha y se reproyectaron a EPSG:9377 antes del cálculo de área por el algoritmo del cordón, el índice de forma medio MSI = perímetro / √(π·área) y la distancia al vecino más cercano NND. Sobre los parches reproyectados se aplicaron dos predicados topológicos DE-9IM: `intersects` con la frontera del AOI con tolerancia de 30 m, y `contains` con los puntos de monitoreo INVEMAR.

== Forzamiento climático y validación cruzada
<forzamiento-climático-y-validación-cruzada>
Cada uno de los cuatro forzamientos climático-hidrológicos se cruzó con la anomalía NDVI z-score en rezagos de cero a tres meses, desagregando las ocho estaciones según su naturaleza espectral porque el promedio agregado cancela las dos señales opuestas (las cuatro estaciones limnológicas responden con signo opuesto a las cuatro de manglar denso). Para verificar que las conclusiones no dependen del entorno computacional se ejecutaron cuatro validaciones cruzadas: serie NDVI Python ↔ R sobre las ocho estaciones, correlación caudal-NDVI Python = R = Julia con valores idénticos hasta el tercer decimal, conteo de parches DE-9IM Python ↔ Julia, y réplicas en R de los análisis ENSO y caudal IDEAM.

== Clasificación supervisada y benchmark
<clasificación-supervisada-y-benchmark>
Como benchmark del clasificador determinístico por umbrales se implementó un Random Forest dentro de Google Earth Engine sobre la misma imagen mediana Sentinel-2 del periodo actual con 100 árboles, `minLeafPopulation = 5` y 15 variables predictoras (diez bandas reflectivas de Sentinel-2, tres índices espectrales, elevación SRTM y distancia al agua JRC). El entrenamiento usó 1.000 puntos estratificados sobre INVEMAR 1:25.000 con validación cruzada K-fold (K = 5). Las métricas pixel a pixel se calcularon sobre 10.000 puntos de muestreo aleatorio dentro del AOI.

= Resultados
<resultados>
== Quiebres estructurales y anomalías temporales
<quiebres-estructurales-y-anomalías-temporales>
El algoritmo bfast detectó quiebres estructurales generalizados en 2016 sobre siete de las ocho estaciones (Tabla #ref(<tbl-bfast>, supplement: [Tabla])), coincidentes con el evento El Niño 2015--2016 ---ONI máximo +2,75---, y un segundo evento de perturbación en septiembre de 2020 bajo La Niña con anomalías NDVI negativas en dos estaciones (z \< −3). El análisis bfast unificado sobre las cuatro estaciones de manglar denso del Complejo de Pajarales refinó la atribución de este último episodio con quiebres específicos en Caño Palos (julio 2020) y Caño Clarín (febrero 2020 y abril 2021), un segundo bloque en 2022 sobre CP Aguas Negras (abril) y CP Luna (enero) por excedente hídrico post-Niña, y un tercer bloque en 2023--2024 coincidente con el episodio El Niño visible en la serie ONI. La extensión de la serie con Landsat 8 reveló cuatro anomalías adicionales en VIPIS durante 2016 que no eran visibles con Sentinel-2 únicamente.

#figure([
#table(
  columns: (22%, 18%, 22%, 38%),
  align: (auto,auto,auto,auto,),
  table.header([Estación], [Quiebres (h=0,10)], [Fecha principal], [Evento ENSO asociado],),
  table.hline(),
  [CP Pajarales], [1], [2016-10], [El Niño 2015--2016],
  [Caño Clarín], [1], [2016-09], [El Niño 2015--2016],
  [Isla Boquerón], [2], [2016-04, 2018-05], [El Niño + transición],
  [Punta Cerro], [3], [2016-11, 2020-04, 2021-08], [El Niño + La Niña + recuperación],
  [Punta Chino], [2], [2016-05], [El Niño 2015--2016],
  [Río Sevilla], [1], [2016-12], [El Niño 2015--2016],
  [VIPIS], [2], [2016-04, 2022-03], [El Niño + recuperación],
)
], caption: figure.caption(
position: top, 
[
Quiebres bfast detectados sobre la serie combinada Landsat 8 + Sentinel-2 (2013--2025).
]), 
kind: "quarto-float-tbl", 
supplement: "Tabla", 
)
<tbl-bfast>


== Contracción del área con consolidación estructural
<contracción-del-área-con-consolidación-estructural>
Las métricas de fragmentación describen una secuencia de contracción del área clasificada con simultánea consolidación estructural (Tabla #ref(<tbl-fragmentacion>, supplement: [Tabla])). El número de parches en el rango filtrado 1--5.000 ha disminuyó de 79 en el periodo de degradación a 38 en el de recuperación y a 15 en el actual, mientras el área total clasificada se redujo de 12.425,6 a 4.037,0 hectáreas en los mismos cortes. El área media de parche, en cambio, creció de 157,3 a 269,1 hectáreas, lo que indica que los parches sobrevivientes son más grandes pero menos numerosos. El índice de forma medio MSI pasó de 0,51 a 1,46 ---bordes progresivamente más irregulares consistentes con regeneración no uniforme--- y la distancia media al vecino más cercano aumentó de 1,10 a 2,39 km, evidenciando aislamiento creciente.

#figure([
#table(
  columns: (13.43%, 13.43%, 25.37%, 25.37%, 7.46%, 14.93%),
  align: (auto,auto,auto,auto,auto,auto,),
  table.header([Periodo], [Parches], [Área total (ha)], [Área media (ha)], [MSI], [NND (km)],),
  table.hline(),
  [Degradación (2020-S2)], [79], [12.425,6], [157,3], [0,51], [1,10],
  [Recuperación (2022-S1)], [38], [8.650,8], [227,7], [1,01], [1,99],
  [Actual (2024--2025)], [15], [4.037,0], [269,1], [1,46], [2,39],
)
], caption: figure.caption(
position: top, 
[
Métricas de fragmentación sobre el AOI acotado en EPSG:9377.
]), 
kind: "quarto-float-tbl", 
supplement: "Tabla", 
)
<tbl-fragmentacion>


La contracción del área no equivale a pérdida funcional del manglar: el NDVI mediano del dosel sobre los píxeles con NDVI \> 0,4 cayó a 0,60 entre el segundo semestre de 2019 y el primer semestre de 2020 ---coincidiendo con la sequía precursora y el episodio La Niña 2020--2021--- y recuperó valores estables alrededor de 0,80 desde 2022 (Fig. #ref(<fig-ndvi-mediano>, supplement: [Fig.])). El balance neto de cobertura entre el periodo de degradación y el estado actual arrojó 183,2 km² de pérdida y 259,2 km² de ganancia sobre una base estable de 690,9 km², equivalente a un cambio neto positivo de +76,0 km².

#figure([
#box(image("../outputs/figures/ndvi_mediano_manglar_acotado.png", width: 90.0%))
], caption: figure.caption(
position: bottom, 
[
Serie temporal del NDVI mediano del manglar sobre el AOI acotado (SFF CGSM + VPI Salamanca, 835 km²) entre 2018 y 2025, calculada a partir del datacube trimestral CF-1.8 restringida a píxeles con NDVI \> 0,4. Las franjas sombreadas marcan los tres periodos de referencia; la caída de 2019--2020 coincide con la sequía y el episodio La Niña.
]), 
kind: "quarto-float-fig", 
supplement: "Fig.", 
)
<fig-ndvi-mediano>


== Inundación SAR y dinámica hídrica de largo plazo
<inundación-sar-y-dinámica-hídrica-de-largo-plazo>
La detección con Sentinel-1 SAR para el evento de septiembre--octubre 2020 ---no registrado en la Global Flood Database, cuya cobertura termina en 2017--- identificó dos mecanismos de afectación diferenciados: inundación de agua abierta sobre 15,93 km² (diferencia de backscatter \> +3 dB) e inundación bajo dosel sobre 43,08 km² (diferencia negativa, indicativa de #emph[scattering] de doble rebote agua-tronco), para un total de 59,02 km² afectados ---el 7,1 % del AOI acotado---. La construcción de una serie temporal continua de Sentinel-1 SAR-VH (2018--2025) sobre las ocho estaciones confirmó la independencia del radar frente al óptico: las cuatro estaciones del Complejo de Pajarales presentan correlaciones positivas altamente significativas entre SAR-VH y NDVI (CP Aguas Negras $rho = + 0 \, 807$, CP Luna $rho = + 0 \, 731$, Caño Clarín $rho = + 0 \, 640$, Caño Palos $rho = + 0 \, 462$, todas con $p < 0 \, 001$), mientras las cuatro estaciones limnológicas arrojan correlaciones no significativas ($lr(|rho|) < 0 \, 20$, $p > 0 \, 17$).

== Forzamiento climático multifuente
<forzamiento-climático-multifuente>
Las cuatro fuentes climático-hidrológicas convergen en una reformulación operativa de la cadena causal La Niña → respuesta del manglar (Tabla #ref(<tbl-clima-resumen>, supplement: [Tabla])). Sobre las estaciones de manglar, ERA5-Land local correlaciona con NDVI a $rho = - 0 \, 123$ en rezago de dos meses ---consistente con la hipótesis de hipoxia bajo dosel--- mientras el caudal IDEAM correlaciona positivamente con $rho = + 0 \, 256$ en rezago de tres meses, el SOI con $rho = + 0 \, 146$ y CHIRPS sobre la cuenca Magdalena con $rho = + 0 \, 252$. La aparente contradicción de signos entre la precipitación local (negativa) y los forzamientos regionales (positivos) refleja la naturaleza no lineal de la respuesta: el ENSO global y el caudal de la cuenca alta organizan el régimen hídrico de fondo ---beneficioso para el manglar al contrarrestar la hipersalinización crónica---, mientras la lluvia local intensa sobre el píxel del humedal induce inundación puntual bajo dosel.

#figure([
#table(
  columns: (42%, 22%, 36%),
  align: (auto,auto,auto,),
  table.header([Forzamiento], [Rezago óptimo (meses)], [$rho$ vs NDVI manglar],),
  table.hline(),
  [ERA5-Land precipitación local], [2], [$- 0 \, 123$],
  [ENSO SOI (NOAA)], [1--2], [$+ 0 \, 146$ a $+ 0 \, 198$],
  [Caudal Magdalena (El Banco)], [3], [$+ 0 \, 256$],
  [Caudal Aracataca (Ganadería Caribe)], [1], [$+ 0 \, 224$],
  [CHIRPS Magdalena alta-media], [3], [$+ 0 \, 252$],
  [CHIRPS Sierra Nevada oeste], [3], [$+ 0 \, 281$],
)
], caption: figure.caption(
position: top, 
[
Correlación de Pearson entre cada forzamiento climático-hidrológico y la anomalía NDVI z-score sobre las cuatro estaciones de manglar denso.
]), 
kind: "quarto-float-tbl", 
supplement: "Tabla", 
)
<tbl-clima-resumen>


#figure([
#box(image("../outputs/figures/caudal_ideam_series_2013_2025.png", width: 100.0%))
], caption: figure.caption(
position: bottom, 
[
Anomalía z-score del caudal mensual IDEAM para el río Magdalena en El Banco (panel superior) y el río Aracataca en Ganadería Caribe (panel inferior), 2013--2025. Las franjas sombreadas marcan los dos eventos ENSO documentados; nótese que los picos de caudal extremo ($z > + 2$) ocurren en 2022, no en 2020, lo que matiza la cadena causal La Niña → caudal → mortandad.
]), 
kind: "quarto-float-fig", 
supplement: "Fig.", 
)
<fig-caudal>


La reformulación de la cadena causal opera en cuatro pasos. #emph[Primero];, el episodio La Niña 2020--2021 induce un régimen prolongado de mayor precipitación regional ---visible en ERA5, SOI positivo, caudal y CHIRPS--- que se acumula progresivamente en los caudales fluviales hasta alcanzar valores extremos ($z > + 2$) en 2022, no en 2020. #emph[Segundo];, el aporte sostenido de caudal en la mayor parte del periodo es beneficioso para el manglar pues reduce la hipersalinización del sustrato. #emph[Tercero];, el evento puntual de mortandad de septiembre 2020 no se explica por un pico de caudal simultáneo sino por la lluvia local intensa acompañada de los 43,08 km² de inundación bajo dosel detectada por SAR. #emph[Cuarto];, los efectos de mediano plazo del régimen La Niña se manifiestan en los quiebres bfast de 2022 sobre CP Aguas Negras y CP Luna, periodo en el cual los caudales alcanzan su máximo histórico.

== Validación doble y benchmark Random Forest
<validación-doble-y-benchmark-random-forest>
La clasificación por umbrales NDVI \> 0,70 + elevación SRTM \< 10 m + distancia al agua JRC \< 3 km se evaluó simultáneamente contra dos cartografías de referencia independientes. El F1-score arrojó 0,583 frente a INVEMAR 1:25.000 y 0,548 frente a ESA WorldCover v200 (Tabla #ref(<tbl-validacion>, supplement: [Tabla])), con Precisión entre 0,768 y 0,811 y Specificity entre 0,944 y 0,954. Estas cifras representan una mejora del 24 al 32 % sobre el F1 de 0,442 reportado en el baseline preliminar sobre el AOI envolvente. El acuerdo directo entre ambas cartografías de referencia fue F1 = 0,833, lo que define un techo metodológico realista; el clasificador del proyecto alcanzó aproximadamente el 70 % de ese techo. El benchmark del clasificador supervisado Random Forest sobre la misma imagen y referencias arrojó F1 = 0,826 frente a INVEMAR y F1 = 0,889 frente a WorldCover, mejoras del 42 % y 62 % respectivamente que resuelven la subestimación de Recall del modelo determinístico. Las bandas SWIR de Sentinel-2 (B11 y B12) y la distancia al agua emergieron como las variables más discriminantes.

#figure([
#table(
  columns: (24%, 28%, 12%, 12%, 12%, 12%),
  align: (auto,auto,auto,auto,auto,auto,),
  table.header([Método], [Referencia], [F1], [Precisión], [Recall], [Specificity],),
  table.hline(),
  [Umbrales NDVI/CMRI], [INVEMAR 1:25.000], [0,583], [0,811], [0,454], [0,954],
  [Umbrales NDVI/CMRI], [ESA WorldCover v200], [0,548], [0,768], [0,426], [0,944],
  [#strong[Random Forest];], [INVEMAR 1:25.000], [#strong[0,826];], [0,745], [#strong[0,926];], [0,884],
  [#strong[Random Forest];], [ESA WorldCover v200], [#strong[0,889];], [0,846], [#strong[0,937];], [0,926],
)
], caption: figure.caption(
position: top, 
[
Validación cruzada del clasificador por umbrales y benchmark Random Forest contra dos cartografías de referencia.
]), 
kind: "quarto-float-tbl", 
supplement: "Tabla", 
)
<tbl-validacion>


#figure([
#box(image("../outputs/figures/rf_feature_importance.png", width: 85.0%))
], caption: figure.caption(
position: bottom, 
[
Importancia relativa de las quince variables predictoras del clasificador Random Forest, ordenadas por contribución al modelo (Gini importance). Las bandas SWIR de Sentinel-2 (B11, B12) y la distancia al agua del JRC concentran la mayor capacidad discriminante.
]), 
kind: "quarto-float-fig", 
supplement: "Fig.", 
)
<fig-rf>


== Validación cruzada multilingüe
<validación-cruzada-multilingüe>
La convergencia operativa entre Python, R y Julia se verificó mediante cuatro validaciones cruzadas formales. La serie NDVI extraída con `stars::st_extract` en R sobre el cubo trimestral reprodujo la serie de `reduceRegions` en GEE con $rho > 0 \, 95$ y RMSE \< 0,05 unidades NDVI. La correlación caudal-NDVI por rezago calculada en los tres lenguajes produjo valores idénticos hasta tres decimales ($rho = 0 \, 064$ / $0 \, 039$ / $0 \, 108$ / $0 \, 256$ para los rezagos 0 a 3 meses), con diferencia máxima del orden de $10^(- 4)$. Los predicados topológicos DE-9IM ejecutados con `LibGEOS.jl` en Julia produjeron conteos idénticos a `geopandas` + `shapely` para parches totales y en borde. Las réplicas en R de los análisis ENSO y caudal IDEAM coincidieron hasta tres decimales con las ejecuciones en Python para las dieciséis filas de la tabla de caudal y las ocho de la tabla ENSO.

== Módulo operativo de alertas tempranas
<módulo-operativo-de-alertas-tempranas>
La integración de las series NDVI, SAR-VH y los quiebres bfast en un módulo operativo de semáforo materializa el Nivel 2 del paradigma Digital Twin (Fig. #ref(<fig-alertas>, supplement: [Fig.])). La ejecución del módulo sobre el corte 2024-12 a 2025-12 arrojó cinco estaciones estables ---incluidas las cuatro de manglar denso del Complejo de Pajarales---, tres estaciones de borde en alerta (Río Sevilla, Punta Chino y Caño Clarín por persistencia de anomalías históricas) y ninguna en estado crítico. Esta distribución constituye la primera fotografía cuantitativa del estado del ecosistema sustentada en una lógica reproducible, ejecutable mensualmente al ingreso de cada nuevo composite Sentinel-2 y Sentinel-1.

#figure([
#box(image("../outputs/figures/alertas_semaforo.png", width: 90.0%))
], caption: figure.caption(
position: bottom, 
[
Mapa semáforo del estado del manglar de la CGSM por estación de monitoreo al cierre del corte 2024-12 a 2025-12. Verde = estable; amarillo = alerta; rojo = crítica. La distribución (5 estables, 3 en alerta, 0 críticas) constituye la primera fotografía cuantitativa del estado operativo del ecosistema sustentada en una lógica reproducible.
]), 
kind: "quarto-float-fig", 
supplement: "Fig.", 
)
<fig-alertas>


= Discusión
<discusión>
Los resultados sostienen tres interpretaciones que conectan con la literatura existente. #emph[La convergencia del rango de cobertura] reportado bajo el AOI acotado (del orden de 4.000 a 12.000 hectáreas según el periodo) es coherente con el rango estimado por el Global Mangrove Watch v3.0 para esta misma área en el ciclo 2018--2020 @bunting2022, lo que confirma que el acotamiento a los polígonos oficiales del SFF + VPI elimina los falsos positivos por vegetación riberana y agropecuaria sin entrenamiento supervisado adicional. #emph[El F1 de 0,548 alcanzado contra ESA WorldCover] es inferior al rango 0,80--0,90 reportado por Selvaraj y Gallego-Pérez #cite(<selvaraj2023>, form: "year") para manglares del Pacífico colombiano con clasificador Random Forest sobre Landsat + SAR ALOS-2. La discrepancia se atribuye a que el clasificador determinístico por umbrales aquí presentado no explota la complementariedad óptico--SAR del flujo supervisado, y a que el hábitat del Pacífico presenta menor heterogeneidad espectral con vegetación no-manglar que el complejo lagunar de la CGSM. El benchmark Random Forest implementado en este estudio (F1 = 0,826 vs INVEMAR y 0,889 vs WorldCover) confirma que el margen disponible entre el clasificador determinístico y el techo metodológico de 0,833 se cierra cuando se incorpora aprendizaje supervisado, con las bandas SWIR como variables más discriminantes.

El hallazgo metodológico más significativo del estudio es el contraste de signos opuestos entre la precipitación ERA5-Land local ($rho = - 0 \, 123$) y los forzamientos regionales (caudal $rho = + 0 \, 256$, CHIRPS $rho = + 0 \, 252$, SOI $rho = + 0 \, 146$) sobre las estaciones de manglar. Esta aparente contradicción no es inconsistencia metodológica sino evidencia del carácter no lineal de la respuesta del manglar al forzamiento climático: el ENSO global y el caudal de la cuenca alta organizan el régimen hídrico de fondo ---beneficioso al contrarrestar la hipersalinización crónica que el INVEMAR #cite(<invemar2024>, form: "year") identifica como principal estresor histórico---, mientras la precipitación local sobre el píxel del humedal captura la intensidad puntual del aporte hídrico, así eventos de lluvia copiosa y prolongada se asocian con inundación bajo dosel e hipoxia que sí afectan negativamente al dosel. La cadena causal La Niña → caudal fluvial → inundación prolongada → mortandad opera, en consecuencia, a través de variables intermedias multiescalares que ningún forzamiento único captura por sí solo, lo que justifica la convergencia entre cuatro fuentes independientes como herramienta de triangulación.

El análisis bfast unificado sobre las cuatro estaciones de manglar denso permite refinar la atribución de eventos. El bloque 2022 de quiebres en CP Aguas Negras y CP Luna coincide con el pico de caudal del periodo La Niña 2020--2022 ---rezagado dos años respecto al evento de mortandad de septiembre 2020---, lo que confirma que los efectos de mediano plazo del forzamiento climático sobre el sistema operan en escalas temporales mayores que las del evento puntual. El tercer bloque de quiebres en 2023--2024 anticipa que el evento El Niño 2023--2024 ya empezó a manifestarse sobre el dosel, hallazgo que el módulo de alertas tempranas detecta operativamente y que orienta el monitoreo futuro.

Las limitaciones del estudio incluyen cuatro restricciones explícitas. La nubosidad persistente del Caribe colombiano reduce la disponibilidad efectiva de imágenes ópticas Sentinel-2, limitación parcialmente mitigada con Landsat 8/9 y Sentinel-1 SAR. La resolución espacial de Sentinel-2 (10 m) no caracteriza la heterogeneidad del dosel a escala de individuo. La validación se sustenta en cartografías de un único periodo de referencia (INVEMAR 2020 y WorldCover 2022), lo que introduce incertidumbre temporal al comparar contra los tres periodos del análisis. Finalmente, la red hidrométrica analizada se restringe a las estaciones IDEAM El Banco y Ganadería Caribe, lo cual no abarca la totalidad de los tributarios secundarios del bajo Magdalena.

= Conclusiones y prospectiva
<conclusiones-y-prospectiva>
El pipeline multilenguaje desarrollado caracteriza la dinámica espaciotemporal del manglar de la CGSM entre 2013 y 2025 con resultados verificables: identifica quiebres bfast generalizados en 2016 y un evento de mortandad puntual en septiembre 2020 con 43,08 km² de inundación bajo dosel; documenta una contracción del área clasificada de 12.426 a 4.037 hectáreas con consolidación estructural simultánea (área media de parche 157 → 269 ha) y recuperación del NDVI mediano del dosel de 0,60 a 0,80 desde 2022; reformula la cadena causal La Niña → respuesta del manglar mediante la convergencia de cuatro forzamientos independientes que sostienen un acoplamiento positivo entre el aporte fluvial sostenido y el vigor del dosel; alcanza F1 = 0,826 con Random Forest contra cartografía oficial INVEMAR 1:25.000 frente al techo metodológico de 0,833 que imponen las propias discrepancias entre cartografías de referencia; y materializa el Nivel 2 del paradigma Digital Twin mediante un módulo operativo de alertas tempranas que reporta cinco estaciones estables, tres en alerta y ninguna crítica al cierre de 2025.

La prospectiva inmediata se articula en cinco líneas. #emph[Primero];, ampliar la red de estaciones IDEAM hacia los tributarios secundarios del bajo Magdalena ---Fundación, Río Frío--- para ganar resolución espacial sobre las distintas vías de entrada de agua al sistema. #emph[Segundo];, profundizar el análisis ENSO con métricas de eventos discretos como duración acumulada de fases La Niña, así como con el Atlantic Multidecadal Oscillation que podría modular la dinámica de la cuenca Magdalena. #emph[Tercero];, refinar el clasificador supervisado con armonización espectral Landsat 8 ↔ Sentinel-2 para eliminar la discontinuidad observada alrededor de 2018. #emph[Cuarto];, extender el análisis bfast unificado al periodo 2013--2025 incorporando Landsat 8 sobre las cuatro estaciones de manglar denso. #emph[Quinto];, ampliar la ventana temporal del periodo actual a por lo menos dos ciclos anuales adicionales (julio 2025--junio 2027) para diferenciar entre fluctuación intermedia y tendencia estable.

El pipeline demuestra la viabilidad de un enfoque GeoAI multilenguaje para el monitoreo costero y constituye un prototipo reproducible adaptable a otros sistemas lagunares tropicales. El dashboard interactivo generado se ofrece como insumo cartográfico para el seguimiento permanente que establece el Plan de Manejo Ambiental del sitio Ramsar CGSM @comisionconjunta2026. La materialización del Nivel 2 del paradigma Digital Twin sobre la CGSM abre la vía hacia un Nivel 3 que incorpore modelos predictivos de tendencia y simulación de escenarios climáticos prospectivos, línea de trabajo que la tesis de maestría en curso desarrollará en los próximos ciclos.

#block[
#heading(
level: 
1
, 
numbering: 
none
, 
[
Disponibilidad de datos y código
]
)
]
El código fuente completo, los notebooks reproducibles y los datos derivados están disponibles públicamente bajo licencia MIT en #link("https://github.com/linaq11/proyecto-cgsm-curso");. Todo el procesamiento se ejecuta dentro de un contenedor Docker (`sig_unal v1.11`, Python 3.12 + R 4.3.3 + Julia 1.11.3 + Quarto 1.4) que garantiza la reproducibilidad bit a bit del análisis. Los datos satelitales provienen de Google Earth Engine; los datos de campo provienen de INVEMAR vía GBIF (DOI: #link("https://doi.org/10.15472/0fqdp4")[10.15472/0fqdp4];); las series hidrométricas provienen del portal DHIME del IDEAM; el ERA5-Land del Climate Data Store de ECMWF/Copernicus; los índices ENSO del Climate Prediction Center de la NOAA; y la cartografía de referencia de INVEMAR 1:25.000 y ESA WorldCover v200.

#block[
#heading(
level: 
1
, 
numbering: 
none
, 
[
Referencias
]
)
]
Beltrán, J., Rodríguez, J. C., Carbonó, E., y Blanco, J. (2022). #emph[Datos de monitoreo de la estructura de los manglares de la Ciénaga Grande de Santa Marta (Magdalena)] \[Conjunto de datos\]. INVEMAR. #link("https://doi.org/10.15472/0fqdp4")

Bunting, P., Rosenqvist, A., Hilarides, L., Lucas, R. M., Thomas, T., Tadono, T., Worthington, T. A., Spalding, M., Murray, N. J., y Rebelo, L.-M. (2022). Global mangrove extent change 1996--2020: Global Mangrove Watch versión 3.0. #emph[Remote Sensing];, #emph[14];(15), 3657. #link("https://doi.org/10.3390/rs14153657")

Comisión Conjunta del sitio Ramsar CGSM. (2026, 2 de febrero). #emph[Plan de Manejo Ambiental del sitio Ramsar Sistema Delta Estuarino del Río Magdalena, Ciénaga Grande de Santa Marta] (vigencia diez años). Corporación Autónoma Regional del Atlántico, Corporación Autónoma Regional del Magdalena, Establecimiento Público Ambiental Barranquilla Verde y Parques Nacionales Naturales de Colombia.

Funk, C., Peterson, P., Landsfeld, M., Pedreros, D., Verdin, J., Shukla, S., Husak, G., Rowland, J., Harrison, L., Hoell, A., y Michaelsen, J. (2015). The climate hazards infrared precipitation with stations: a new environmental record for monitoring extremes. #emph[Scientific Data];, #emph[2];, 150066. #link("https://doi.org/10.1038/sdata.2015.66")

Giri, C., Ochieng, E., Tieszen, L. L., Zhu, Z., Singh, A., Loveland, T., Masek, J., y Duke, N. (2011). Status and distribution of mangrove forests of the world using earth observation satellite data. #emph[Global Ecology and Biogeography];, #emph[20];(1), 154--159. #link("https://doi.org/10.1111/j.1466-8238.2010.00584.x")

Goldberg, L., Lagomasino, D., Thomas, N., y Fatoyinbo, T. (2020). Global declines in human-driven mangrove loss. #emph[Global Change Biology];, #emph[26];(10), 5844--5855. #link("https://doi.org/10.1111/gcb.15275")

Hamilton, S. E., y Casey, D. (2016). Creation of a high spatio-temporal resolution global database of continuous mangrove forest cover for the 21st century (CGMFC-21). #emph[Global Ecology and Biogeography];, #emph[25];(6), 729--738. #link("https://doi.org/10.1111/geb.12449")

Instituto de Investigaciones Marinas y Costeras \[INVEMAR\]. (2020). #emph[Mapa de manglares de Colombia escala 1:25.000] \[Capa cartográfica\]. Servicio ArcGIS REST SIGMA/MANGLARES\_COLOMBIA.

Instituto de Investigaciones Marinas y Costeras \[INVEMAR\]. (2024). #emph[Monitoreo de las condiciones ambientales y los cambios estructurales y funcionales de las comunidades vegetales y de los recursos pesqueros durante la rehabilitación de la Ciénaga Grande de Santa Marta. Informe técnico final 2023];. Santa Marta.

Murillo-Sandoval, P. J., Fatoyinbo, L., y Simard, M. (2022). Mangroves cover change trajectories 1984--2020: The gradual decrease of mangroves in Colombia. #emph[Frontiers in Marine Science];, #emph[9];, 892946. #link("https://doi.org/10.3389/fmars.2022.892946")

Selvaraj, J. J., y Gallego-Pérez, B. E. (2023). Assessing mangrove forests in the Colombian Pacific coast using cloud computing and Random Forest classification. #emph[Marine Pollution Bulletin];, #emph[193];, 115176. #link("https://doi.org/10.1016/j.marpolbul.2023.115176")

Verbesselt, J., Hyndman, R., Newnham, G., y Culvenor, D. (2010). Detecting trend and seasonal changes in satellite image time series. #emph[Remote Sensing of Environment];, #emph[114];(1), 106--115. #link("https://doi.org/10.1016/j.rse.2009.08.014")

Vinasco, L., Hamburger, A., y Anaya, J. A. (2020). Análisis multitemporal de la cobertura vegetal en la Ciénaga Grande de Santa Marta entre 2013 y 2018. #emph[Cuadernos del Caribe];, #emph[24];(2), 39--56.

Wu, Q., y Osco, L. P. (2023). samgeo: A Python package for segmenting geospatial data with the Segment Anything Model (SAM). #emph[Journal of Open Source Software];, #emph[8];(89), 5663. #link("https://doi.org/10.21105/joss.05663")

Yancho, J. M. M., Jones, T. G., Gandhi, S. R., Ferster, C., Lin, A., y Glass, L. (2020). The Google Earth Engine Mangrove Mapping Methodology (GEEMMM). #emph[Remote Sensing];, #emph[12];(22), 3758. #link("https://doi.org/10.3390/rs12223758")

Zanaga, D., Van De Kerchove, R., Daems, D., De Keersmaecker, W., Brockmann, C., Kirches, G., Wevers, J., Cartus, O., Santoro, M., Fritz, S., Lesiv, M., Herold, M., Tsendbazar, N.-E., Xu, P., Ramoino, F., y Arino, O. (2022). #emph[ESA WorldCover 10 m 2021 v200] \[Conjunto de datos\]. Zenodo. #link("https://doi.org/10.5281/zenodo.7254221")
