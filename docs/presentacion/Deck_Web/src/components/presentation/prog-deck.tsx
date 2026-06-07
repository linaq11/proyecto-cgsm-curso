"use client";

import Image from "next/image";
import {
  Activity,
  AlertTriangle,
  Boxes,
  CheckCircle2,
  CloudRain,
  Container,
  GitBranch,
  ExternalLink,
  Globe,
  LayoutDashboard,
  Layers,
  LineChart,
  MapPin,
  Radar,
  Ruler,
  Satellite,
  ScanSearch,
  Target,
  Trees,
  Waves,
} from "lucide-react";
import { cn } from "@/lib/utils";
import {
  Deck,
  FeatureItem,
  Lead,
  NumberedItem,
  Panel,
  SlideHeader,
  StatCard,
  Tag,
} from "@/components/deck";

/* ----------------------------------------------------------------
   Créditos de portada — edita estas líneas.
   ---------------------------------------------------------------- */
const PRESENTER = "Lina María Quintero Fonseca";
const COURSE = "Programación en SIG · Proyecto final";
const PROGRAM = "Maestría en Geomática";
const FACULTY = "Facultad de Ciencias Agrarias · Sede Bogotá";
const PROFESSOR = "Prof. Alexys H. Rodríguez-Avellaneda";
const REPO = "github.com/linaq11/proyecto-cgsm-curso";
const MONITOR = "linaq11.github.io/proyecto-cgsm-curso/dashboard.html";

/* ----------------------------------------------------------------
   Guion del orador (ES) — qué decir en cada diapositiva (~1 min).
   Se abre en la app con la tecla "N" o el botón de notas.
   ---------------------------------------------------------------- */
const SCRIPT = {
  cover:
    "Buenas. El énfasis del proyecto está en la programación geoespacial y la reproducibilidad: cómo articular Python, R, Julia, Google Earth Engine, un contenedor Docker y un dashboard web dentro de un mismo flujo de trabajo. La Ciénaga Grande de Santa Marta funciona como caso de aplicación y, al mismo tiempo, como una línea de avance para mi investigación de maestría.",
  context:
    "La Ciénaga Grande de Santa Marta es un sistema lagunar-costero estratégico de Colombia, reconocido como sitio Ramsar y Reserva de Biosfera. Su manglar ha presentado ciclos de degradación y recuperación relacionados con cambios hidrológicos, hipersalinización y variabilidad climática, especialmente asociada al ENSO. Para este proyecto trabajé con un AOI acotado de 835,3 km², correspondiente al Santuario de Fauna y Flora CGSM y la Vía Parque Isla de Salamanca. El reto no es la falta de datos: existen imágenes satelitales frecuentes. El problema es convertir esos datos en un flujo reproducible que integre información óptica, radar y climática para monitorear cambios del manglar.",
  gap:
    "La oportunidad del proyecto está en la integración. La información existe, pero suele estar dispersa: imágenes ópticas por un lado, radar por otro, métricas de fragmentación en otro flujo, y variables climáticas en análisis separados. Por eso, la pregunta no se centra solo en mapear manglar, sino en entender cómo cambiaron la cobertura, la fragmentación y el vigor del manglar entre 2013 y 2025, y cómo esas perturbaciones se relacionan con forzamientos climáticos e hidrológicos, especialmente ENSO, caudal y precipitación.",
  objectives:
    "El objetivo general fue desarrollar un pipeline multilenguaje, reproducible e interoperable para monitorear la dinámica del manglar de la CGSM entre 2013 y 2025. Ese objetivo se concreta en cinco pasos. Primero, construir un datacube multitemporal con índices espectrales. Segundo, detectar anomalías y quiebres temporales en las series de NDVI. Tercero, segmentar el manglar y calcular métricas de fragmentación. Cuarto, relacionar esas señales con variables climático-hidrológicas. Y quinto, validar la clasificación comparando una regla por umbrales con un Random Forest frente a cartografías de referencia.",
  area:
    "El área de estudio se acotó para evitar un análisis espacial sobredimensionado. Inicialmente se tenía un AOI de más de cinco mil kilómetros cuadrados, pero ese polígono incluía vegetación riberana, salitrales y zonas que no correspondían directamente al objetivo del proyecto. Por eso se trabajó con un AOI de 835,3 km², obtenido de la unión del Santuario de Fauna y Flora CGSM y la Vía Parque Isla de Salamanca. Además, se definieron ocho estaciones de análisis: cinco provenientes de INVEMAR-GBIF y tres complementarias sobre áreas de manglar verificadas. Todas las áreas se calcularon en EPSG:9377 para mantener coherencia métrica con el sistema oficial colombiano.",
  data:
    "El pipeline integra trece conjuntos de datos agrupados en seis categorías. La base óptica proviene de Sentinel-2 y Landsat 8/9; el componente radar usa Sentinel-1; la validación cartográfica se apoya en INVEMAR y ESA WorldCover; y el contexto climático e hidrológico integra ERA5-Land, ENSO, caudal IDEAM y precipitación CHIRPS. Además, se incorporan capas de agua e inundación, como JRC Global Surface Water y Global Flood Database, junto con SRTM y estaciones INVEMAR-GBIF. La mayoría de fuentes se gestionó desde Google Earth Engine, lo que reduce la necesidad de descargar imágenes pesadas y favorece la reproducibilidad del flujo.",
  pipeline:
    "Esta es la diapositiva central del proyecto. El aporte de programación está en orquestar tres lenguajes dentro de una sola arquitectura reproducible. Python centraliza la adquisición en Google Earth Engine, la segmentación con SamGeo, el Random Forest, los datacubes y el dashboard. R se usa para el análisis temporal, especialmente BFAST y las relaciones con variables climáticas e hidrológicas. Julia se encarga del cómputo geométrico, las métricas de fragmentación y la topología DE-9IM. El punto de encuentro es un datacube en NetCDF CF-1.8, reproyectado a EPSG:9377. El contenedor Docker congela el entorno y permite que el flujo sea reproducible de extremo a extremo.",
  methods:
    "El flujo metodológico se organiza en cinco fases y un módulo SAR. Primero, se construye el datacube con composiciones Sentinel-2 y Landsat. Segundo, se extraen series temporales de NDVI y se aplican anomalías z-score y BFAST para detectar quiebres. Tercero, se usa SamGeo para segmentar el manglar en tres periodos. Cuarto, Julia calcula métricas de fragmentación y relaciones topológicas. El módulo SAR analiza inundación con Sentinel-1 VH mediante la diferencia entre condiciones secas e inundadas. Finalmente, se entrena un Random Forest como referencia robusta frente a la clasificación por umbrales.",
  ndvi:
    "En la dinámica temporal se integraron 929 observaciones mensuales de NDVI. La serie muestra dieciocho anomalías significativas, concentradas especialmente en 2016, 2018 y septiembre de 2020. El NDVI mediano del manglar se mantuvo cerca de 0,80, cayó alrededor de 0,60 entre 2019 y 2020, y volvió a estabilizarse cerca de 0,80 desde 2022. BFAST detectó un quiebre generalizado en 2016, consistente con el evento El Niño. Cuando el análisis se restringe a estaciones de manglar denso, la señal de 2020 y las respuestas posteriores se vuelven más claras.",
  fragmentation:
    "En la dinámica espacial, la segmentación con SamGeo muestra una reorganización del manglar. La cobertura clasificada disminuye de 12.426 a 4.037 hectáreas y el número de parches baja de 79 a 15. Sin embargo, el área media por parche aumenta de 157 a 269 hectáreas. Por eso, la lectura no debe ser una pérdida directa de cobertura. La señal indica una contracción aparente acompañada de consolidación estructural: menos parches, pero más grandes y compactos. Esta interpretación se refuerza al cruzar la segmentación con el comportamiento del NDVI y las métricas de fragmentación. La topología DE-9IM permitió verificar de forma consistente las relaciones espaciales entre Python y Julia.",
  climate:
    "El módulo climático e hidrológico muestra que no conviene promediar todas las estaciones, porque manglar y cuerpos de agua pueden responder con signos opuestos. Al desagregar por naturaleza espectral, la señal se vuelve más interpretable. El caudal del río Magdalena presenta una asociación positiva con el NDVI del manglar, con un rezago de tres meses. En el componente radar, Sentinel-1 permitió identificar 59,02 km² de inundación en septiembre de 2020, de los cuales 43,08 km² corresponden a inundación bajo dosel asociada al doble rebote agua-tronco. En Pajarales, la relación SAR-VH y NDVI alcanza un rho de 0,81, lo que sugiere que el radar captura cambios estructurales complementarios al vigor óptico.",
  validation:
    "La validación cartográfica compara dos enfoques: una regla por umbrales y un Random Forest. La regla por umbrales es conservadora y obtiene F1 de 0,583 frente a INVEMAR y 0,548 frente a WorldCover. El Random Forest mejora de forma clara el desempeño, con F1 de 0,826 frente a INVEMAR y 0,889 frente a WorldCover. Además, el acuerdo entre INVEMAR y WorldCover es de 0,833, lo que funciona como un techo metodológico realista: no se debe esperar un acuerdo perfecto cuando las propias referencias difieren. La importancia de variables muestra que las bandas SWIR y la distancia al agua pesan más que el NDVI, lo cual es coherente con un ecosistema de manglar influenciado por humedad, salinidad y proximidad al agua.",
  alerts:
    "El pipeline cierra con un módulo de alertas tempranas que funciona como componente operacional inicial hacia un futuro Gemelo Digital. El módulo usa series incrementales y clasifica cada estación con una lógica tipo semáforo. Al cierre del periodo analizado se identifican cinco estaciones estables, tres en alerta y ninguna crítica. Más importante que el semáforo en sí es que el resultado viene de un flujo reproducible: Python, R y Julia producen valores equivalentes hasta tres decimales, el contenedor Docker congela el entorno y el dashboard HTML permite consultar los productos sin depender de Jupyter.",
  monitor:
    "El producto final del pipeline es el CGSM Monitor, un dashboard HTML publicado en GitHub Pages. Tiene cinco pestañas: Resumen, Cobertura, Clima e hidrología, Validación multilenguaje y Acerca de. El valor del monitor no está solo en mostrar mapas bonitos. Su aporte es que convierte el flujo de programación en un producto consultable, con diecisiete capas temáticas, indicadores clave y documentación de datos y métodos. Además, al ser un HTML autocontenido, puede consultarse desde el navegador sin abrir notebooks ni instalar software especializado.",
  conclusions:
    "Para cerrar, este proyecto demuestra que es posible orquestar Python, R y Julia en un flujo reproducible para monitorear la dinámica del manglar en la Ciénaga Grande de Santa Marta. Los hallazgos principales son tres: la respuesta temporal del manglar frente a eventos ENSO, una dinámica espacial de contracción aparente con consolidación estructural, y la mejora clara del Random Forest frente a la regla por umbrales. También hay límites importantes: no se contó con validación de campo independiente, la red hidrométrica es limitada y las relaciones encontradas son asociaciones temporales, no causalidad. Como trabajo futuro, el flujo puede fortalecerse con validación in situ, más estaciones y una transición hacia un Gemelo Digital costero con alertas operativas. Muchas gracias.",
};

export function ProgDeck() {
  return (
    <Deck.Root brand="monitor">
      {/* ====================================================== 01 · PORTADA */}
      <Deck.Slide title="Portada" variant="cover" notes={SCRIPT.cover}>
        <p className="deck-sans text-[0.86cqw] font-semibold uppercase tracking-[0.28em] text-[var(--brand-gold)]">
          Universidad Nacional de Colombia
        </p>
        <p className="deck-sans mt-[0.5cqw] text-[0.85cqw] uppercase tracking-[0.22em] text-[var(--brand-on-color-soft)]">
          {COURSE}
        </p>
        <h1 className="deck-serif mt-[1.5cqw] max-w-[82%] text-[3.1cqw] font-semibold leading-[1.06] text-white">
          Pipeline multilenguaje para el monitoreo del manglar en la Ciénaga
          Grande de Santa Marta
        </h1>
        <span className="mt-[1.3cqw] block h-[3px] w-[5cqw] rounded-full bg-[var(--brand-gold)]" />
        <p className="deck-sans mt-[1.3cqw] max-w-[66%] text-[1.2cqw] leading-snug text-[var(--brand-on-color-soft)]">
          Pipeline en Python, R y Julia, conectado a Google Earth Engine y
          ejecutado en Docker para caracterizar la dinámica espaciotemporal del
          manglar, 2013&ndash;2025.
        </p>
        <div className="mt-[2cqw] flex flex-col gap-[0.35cqw]">
          <p className="deck-serif text-[1.5cqw] font-semibold text-white">
            {PRESENTER}
          </p>
          <p className="deck-sans text-[0.98cqw] text-[var(--brand-on-color-soft)]">
            {PROGRAM} &middot; {FACULTY}
          </p>
          <p className="deck-sans text-[0.98cqw] text-[var(--brand-on-color-soft)]">
            {PROFESSOR} &nbsp;&middot;&nbsp; {REPO}
          </p>
        </div>
      </Deck.Slide>

      {/* ================================================= 02 · CONTEXTO */}
      <Deck.Slide title="Contexto y problema" notes={SCRIPT.context}>
        <SlideHeader
          eyebrow="Contexto · Por qué importa"
          title="La Ciénaga Grande de Santa Marta"
        />
        <div className="mt-[1.4cqw] grid flex-1 grid-cols-[1.15fr_1fr] gap-[2cqw]">
          <div className="flex flex-col justify-between">
            <Lead>
              Un sistema lagunar-costero estratégico de Colombia, sitio Ramsar y
              Reserva de Biosfera, con ciclos documentados de degradación y
              recuperación del manglar asociados a hipersalinización, variabilidad
              climática y cambios hidrológicos.
            </Lead>
            <div className="grid grid-cols-2 gap-[0.9cqw]">
              <StatCard value="835,3" unit="km²" label="AOI acotado: SFF CGSM + VPI Salamanca" />
              <StatCard value="2013–2025" label="Serie multisensor analizada" />
              <StatCard value="Ramsar" unit="1998" label="Reserva de Biosfera UNESCO" />
              <StatCard value="ENSO" label="El Niño 2015–16 · La Niña 2020–22" />
            </div>
          </div>
          <Panel title="El reto de monitoreo" icon={Waves} className="justify-center">
            <ul className="flex flex-col gap-[0.8cqw]">
              {[
                "Existen datos satelitales frecuentes, pero no siempre se integran en productos reproducibles.",
                "La nubosidad tropical limita la continuidad de la observación óptica.",
                "El radar aporta continuidad, pero requiere integración con datos ópticos y climáticos.",
              ].map((t, i) => (
                <li key={i} className="flex gap-[0.6cqw]">
                  <span className="mt-[0.55cqw] h-[0.45cqw] w-[0.45cqw] shrink-0 rounded-full bg-[var(--brand-gold)]" />
                  <span className="deck-sans text-[0.96cqw] leading-snug text-[var(--brand-ink-soft)]">
                    {t}
                  </span>
                </li>
              ))}
            </ul>
            <div className="mt-[1cqw] rounded-xl bg-[var(--brand-tint)] p-[0.9cqw]">
              <p className="deck-sans text-[0.92cqw] leading-snug text-[var(--brand-ink)]">
                La mortandad de manglar registrada en{" "}
                <span className="font-semibold text-[var(--brand-primary)]">
                  2020
                </span>{" "}
                evidencia la necesidad de seguimiento espacial y temporal continuo.
              </p>
            </div>
          </Panel>
        </div>
      </Deck.Slide>

      {/* ================================================= 03 · VACÍO / PREGUNTA */}
      <Deck.Slide title="Vacío y pregunta" notes={SCRIPT.gap}>
        <SlideHeader
          eyebrow="Justificación · La oportunidad"
          title="El vacío no es de datos, es de integración"
        />
        <div className="mt-[1.3cqw] flex flex-1 flex-col gap-[1.3cqw]">
          <div className="grid grid-cols-3 gap-[1.1cqw]">
            <NumberedItem n={1} title="Óptico + radar">
              La observación óptica y SAR suele analizarse por separado; falta
              integrarlas en una serie consistente.
            </NumberedItem>
            <NumberedItem n={2} title="Pipeline reproducible">
              Segmentación, fragmentación, validación y quiebres temporales
              requieren una arquitectura ejecutable común.
            </NumberedItem>
            <NumberedItem n={3} title="Clima e hidrología">
              ENSO, caudal y precipitación deben cruzarse con la respuesta
              espacial del manglar.
            </NumberedItem>
          </div>
          <Panel
            title="Pregunta de investigación"
            icon={Target}
            accent
            className="justify-center"
          >
            <p className="deck-serif text-[1.5cqw] leading-[1.3] text-white">
              ¿Cómo variaron la cobertura, la fragmentación y el vigor del manglar
              de la CGSM entre 2013 y 2025, y cómo se relacionan esas
              perturbaciones con forzamientos climáticos e hidrológicos asociados
              al ENSO?
            </p>
          </Panel>
        </div>
      </Deck.Slide>

      {/* ================================================= 04 · OBJETIVOS */}
      <Deck.Slide title="Objetivos" notes={SCRIPT.objectives}>
        <SlideHeader
          eyebrow="Objetivos · Una meta, cinco pasos"
          title="Qué construye el pipeline"
        />
        <div className="mt-[1.3cqw] grid flex-1 grid-cols-[1fr_1.25fr] gap-[1.6cqw]">
          <Panel title="Objetivo general" icon={Boxes} accent className="justify-center">
            <p className="deck-serif text-[1.5cqw] leading-[1.32] text-white">
              Desarrollar un pipeline multilenguaje, reproducible e interoperable
              para monitorear la dinámica del manglar de la CGSM entre 2013 y 2025.
            </p>
            <p className="deck-sans mt-[1cqw] text-[0.9cqw] text-[var(--brand-on-color-soft)]">
              Transferible a otros humedales costeros tropicales.
            </p>
          </Panel>
          <div className="grid grid-cols-1 gap-[0.7cqw]">
            <FeatureItem icon={Layers} title="1 · Datacube multitemporal">
              Construir índices NDVI, NDWI y CMRI a partir de Landsat 8/9 y
              Sentinel-2.
            </FeatureItem>
            <FeatureItem icon={LineChart} title="2 · Degradación y recuperación">
              Detectar anomalías z-score y quiebres estructurales con BFAST.
            </FeatureItem>
            <FeatureItem icon={ScanSearch} title="3 · Segmentación y fragmentación">
              Aplicar SamGeo y calcular métricas del paisaje en EPSG:9377.
            </FeatureItem>
            <FeatureItem icon={CloudRain} title="4 · Forzamientos climático-hidrológicos">
              Relacionar la dinámica del manglar con ERA5-Land, ENSO, caudal IDEAM
              y CHIRPS.
            </FeatureItem>
            <FeatureItem icon={CheckCircle2} title="5 · Validación cartográfica">
              Comparar reglas por umbrales y Random Forest frente a INVEMAR y ESA
              WorldCover.
            </FeatureItem>
          </div>
        </div>
      </Deck.Slide>

      {/* ================================================= 05 · ÁREA DE ESTUDIO */}
      <Deck.Slide title="Área de estudio" notes={SCRIPT.area}>
        <SlideHeader
          eyebrow="Área de estudio · AOI acotado"
          title="835,3 km² de área protegida oficial"
        />
        <div className="mt-[1.2cqw] grid flex-1 grid-cols-[1.05fr_0.95fr] gap-[1.6cqw]">
          <div className="flex flex-col gap-[0.85cqw]">
            <FeatureItem icon={MapPin} title="AOI RUNAP">
              Unión del SFF CGSM y la Vía Parque Isla de Salamanca. Reemplaza un
              AOI preliminar de 5.073 km².
            </FeatureItem>
            <FeatureItem icon={Trees} title="8 estaciones de análisis">
              Cinco estaciones INVEMAR-GBIF y tres estaciones complementarias
              sobre manglar verificado.
            </FeatureItem>
            <FeatureItem icon={Ruler} title="Áreas en EPSG:9377">
              Sistema oficial MAGNA-SIRGAS para cálculos métricos. Cerca del 51 %
              del AOI corresponde a agua permanente o estacional según JRC.
            </FeatureItem>
          </div>
          <FigureFrame
            src="/figures/prog/area.png"
            alt="Localización del área de estudio: Colombia, Magdalena, AOI acotado de la CGSM con estaciones INVEMAR y composición Sentinel-2."
            className="h-full"
          />
        </div>
      </Deck.Slide>

      {/* ================================================= 06 · FUENTES DE DATOS */}
      <Deck.Slide title="Fuentes de datos" notes={SCRIPT.data}>
        <SlideHeader
          eyebrow="Datos · 13 conjuntos, 6 categorías"
          title="Una base multisensor y multifuente"
        />
        <div className="mt-[1.2cqw] grid flex-1 grid-cols-3 gap-[1.1cqw]">
          {[
            {
              icon: Satellite,
              t: "Óptico satelital",
              d: "Sentinel-2 MSI y Landsat 8/9 para índices espectrales y serie NDVI.",
            },
            {
              icon: Radar,
              t: "Radar Sentinel-1",
              d: "SAR banda VH para análisis de inundación y respuesta estructural del dosel.",
            },
            {
              icon: Globe,
              t: "Cartografía de referencia",
              d: "ESA WorldCover e INVEMAR 1:25.000 para validación.",
            },
            {
              icon: CloudRain,
              t: "Clima e hidrología",
              d: "ERA5-Land, ENSO ONI/SOI, caudal IDEAM y CHIRPS.",
            },
            {
              icon: Waves,
              t: "Agua e inundación",
              d: "JRC Global Surface Water y Global Flood Database.",
            },
            {
              icon: Ruler,
              t: "Elevación y campo",
              d: "SRTM e INVEMAR-GBIF para contexto físico y estaciones.",
            },
          ].map((s, i) => (
            <FeatureItem key={i} icon={s.icon} title={s.t}>
              {s.d}
            </FeatureItem>
          ))}
        </div>
        <div className="mt-[1.1cqw] flex items-center justify-between rounded-2xl border border-[var(--brand-line)] bg-[var(--brand-paper-2)] px-[1.4cqw] py-[0.9cqw]">
          <span className="deck-sans text-[0.92cqw] text-[var(--brand-ink-soft)]">
            La mayoría de fuentes se gestionó desde{" "}
            <span className="font-semibold text-[var(--brand-primary)]">
              Google Earth Engine
            </span>
            , reduciendo descargas locales y mejorando reproducibilidad.
          </span>
          <div className="flex gap-[0.5cqw]">
            <Tag>EPSG:9377</Tag>
            <Tag>NetCDF CF-1.8</Tag>
            <Tag>10–30 m</Tag>
          </div>
        </div>
      </Deck.Slide>

      {/* ================================================= 07 · PIPELINE MULTILENGUAJE */}
      <Deck.Slide title="Pipeline multilenguaje" notes={SCRIPT.pipeline}>
        <SlideHeader
          eyebrow="Arquitectura · El corazón del proyecto"
          title="Python, R y Julia conectados por un datacube común"
        />
        <div className="mt-[0.8cqw] flex-1">
          <FigureFrame
            src="/figures/prog/flujo_final.png"
            alt="Flujo metodológico del pipeline CGSM, coloreado por lenguaje (Python, R, Julia): entradas (Sentinel-2/1, Landsat, ERA5, ENSO, IDEAM, CHIRPS, INVEMAR, WorldCover), preparación del datacube, análisis (series BFAST, inundación SAR, segmentación SamGeo, fragmentación en Julia, forzamiento climático), validación y benchmark, y salidas incluido el dashboard, todo dentro de Docker sig_unal v1.11."
            className="h-full"
          />
        </div>
      </Deck.Slide>

      {/* ================================================= 08 · MÉTODOS A FONDO */}
      <Deck.Slide title="Métodos" notes={SCRIPT.methods}>
        <SlideHeader
          eyebrow="Métodos · 5 fases + módulo SAR/climático"
          title="Decisiones técnicas del flujo"
        />
        <div className="mt-[1.2cqw] grid flex-1 grid-cols-3 gap-[1.1cqw]">
          {(
            [
              ["1", "Datacube", "Composiciones Sentinel-2 y Landsat 8/9; NetCDF CF-1.8 en EPSG:9377.", "Fase 1"],
              ["2", "Series temporales", "929 observaciones NDVI; z-score y BFAST.", "Fase 2"],
              ["3", "Segmentación", "SamGeo con backbone vit_b sobre composiciones RGB.", "Fase 3"],
              ["4", "Fragmentación", "Julia: parches, índice de forma, distancia al vecino y DE-9IM.", "Fase 4"],
              ["S1", "Inundación SAR", "Sentinel-1 VH: diferencia seco–inundado y doble rebote bajo dosel.", "Módulo"],
              ["5", "Random Forest", "100 árboles, 15 variables, 1.000 puntos y validación cruzada.", "Fase 5"],
            ] as [string, string, string, string][]
          ).map(([n, t, d, tag], i) => (
            <NumberedItem key={i} n={n} title={t} tag={tag}>
              {d}
            </NumberedItem>
          ))}
        </div>
      </Deck.Slide>

      {/* ================================================= 09 · RESULTADOS 1 · NDVI/BFAST */}
      <Deck.Slide title="Resultados · series y quiebres" notes={SCRIPT.ndvi}>
        <SlideHeader
          eyebrow="Resultados 1 · Dinámica temporal"
          title="NDVI, anomalías y quiebres BFAST"
        />
        <div className="mt-[1.1cqw] grid flex-1 grid-cols-[1.35fr_1fr] gap-[1.4cqw]">
          <FigureFrame
            src="/figures/prog/ndvi_serie.png"
            alt="Serie temporal del NDVI mediano del manglar sobre el AOI acotado 2018–2025, con caída 2019–2020 y recuperación desde 2022."
            className="h-full"
          />
          <div className="flex flex-col gap-[0.85cqw]">
            <div className="grid grid-cols-2 gap-[0.8cqw]">
              <StatCard value="929" label="Observaciones mensuales de NDVI" />
              <StatCard value="18" label="Anomalías significativas" />
              <StatCard value="0,80→0,60→0,80" label="Caída y recuperación del NDVI mediano" />
              <StatCard value="2016" label="Quiebre BFAST asociado a El Niño" />
            </div>
            <Panel title="Lectura clave" icon={Activity}>
              <p className="deck-sans text-[0.92cqw] leading-snug text-[var(--brand-ink-soft)]">
                La señal temporal muestra caída entre 2019–2020, recuperación
                posterior y respuestas diferenciadas al analizar estaciones de
                manglar denso.
              </p>
            </Panel>
          </div>
        </div>
      </Deck.Slide>

      {/* ============================================ 10 · RESULTADOS 2 · FRAGMENTACIÓN */}
      <Deck.Slide title="Resultados · fragmentación" notes={SCRIPT.fragmentation}>
        <SlideHeader
          eyebrow="Resultados 2 · Dinámica espacial"
          title="Contracción aparente y consolidación estructural"
        />
        <div className="mt-[1.1cqw] grid flex-1 grid-cols-[1fr_1.2fr] gap-[1.4cqw]">
          <FigureFrame
            src="/figures/prog/ndvi_cambio.png"
            alt="Mapa de cambio del NDVI mediano entre el estado actual y la degradación: azul indica ganancia de vigor, rojo indica pérdida."
            className="h-full"
          />
          <div className="flex flex-col gap-[0.85cqw]">
            <div className="grid grid-cols-2 gap-[0.8cqw]">
              <StatCard value="12.426→4.037" unit="ha" label="Cobertura clasificada por segmentación" />
              <StatCard value="79→15" label="Número de parches" />
              <StatCard value="157→269" unit="ha" label="Área media por parche" />
              <StatCard value="+76" unit="km²" label="Cambio neto entre degradación y estado actual" />
            </div>
            <Panel title="Lectura clave" icon={Trees}>
              <p className="deck-sans text-[0.92cqw] leading-snug text-[var(--brand-ink-soft)]">
                La reducción del área segmentada no se interpreta como pérdida
                directa. Debe leerse junto con NDVI, densidad de parches y métricas
                de forma.
              </p>
            </Panel>
          </div>
        </div>
      </Deck.Slide>

      {/* ============================================ 11 · RESULTADOS 3 · CLIMA + SAR */}
      <Deck.Slide title="Resultados · clima y SAR" notes={SCRIPT.climate}>
        <SlideHeader
          eyebrow="Resultados 3 · Forzamiento e inundación"
          title="Acoplamiento climático, hidrológico y radar"
        />
        <div className="mt-[1.1cqw] grid flex-1 grid-cols-[1.3fr_1fr] gap-[1.4cqw]">
          <FigureFrame
            src="/figures/prog/sar.png"
            alt="Serie temporal Sentinel-1 SAR-VH 2018–2025 sobre estaciones del manglar, con anomalías codificadas por color."
            className="h-full"
          />
          <div className="flex flex-col gap-[0.85cqw]">
            <div className="grid grid-cols-2 gap-[0.8cqw]">
              <StatCard value="ρ +0,256" label="Caudal Magdalena ↔ NDVI, rezago 3 meses" />
              <StatCard value="59,02" unit="km²" label="Inundación SAR en septiembre de 2020" />
              <StatCard value="43,08" unit="km²" label="Inundación bajo dosel" />
              <StatCard value="ρ +0,81" label="SAR-VH ↔ NDVI en Pajarales" />
            </div>
            <Panel title="Lectura clave" icon={CloudRain}>
              <p className="deck-sans text-[0.92cqw] leading-snug text-[var(--brand-ink-soft)]">
                Manglar y cuerpos de agua responden con signos distintos; por eso
                el análisis debe desagregarse por naturaleza espectral.
              </p>
            </Panel>
          </div>
        </div>
      </Deck.Slide>

      {/* ============================================ 12 · RESULTADOS 4 · VALIDACIÓN/RF */}
      <Deck.Slide title="Resultados · validación" notes={SCRIPT.validation}>
        <SlideHeader
          eyebrow="Resultados 4 · Validación cartográfica"
          title="Umbrales vs. Random Forest"
        />
        <div className="mt-[1.1cqw] grid flex-1 grid-cols-[1fr_1.15fr] gap-[1.4cqw]">
          <FigureFrame
            src="/figures/prog/rf.png"
            alt="Importancia de las 15 variables del Random Forest: las bandas SWIR B11 y B12 y la distancia al agua dominan."
            className="h-full"
          />
          <div className="flex flex-col gap-[0.85cqw]">
            <Panel title="F1-score por método y referencia" icon={CheckCircle2}>
              <div className="flex flex-col gap-[0.55cqw]">
                {[
                  ["F1 umbrales vs. INVEMAR", "0,583"],
                  ["F1 umbrales vs. WorldCover", "0,548"],
                  ["F1 RF vs. INVEMAR", "0,826"],
                  ["F1 RF vs. WorldCover", "0,889"],
                ].map(([k, v], i) => (
                  <div key={i} className="flex items-center justify-between gap-[0.6cqw]">
                    <span className="deck-sans text-[0.9cqw] text-[var(--brand-ink-soft)]">
                      {k}
                    </span>
                    <span className="deck-serif text-[1.15cqw] font-semibold text-[var(--brand-primary)]">
                      {v}
                    </span>
                  </div>
                ))}
              </div>
            </Panel>
            <div className="grid grid-cols-2 gap-[0.8cqw]">
              <StatCard value="0,833" label="Acuerdo INVEMAR ↔ WorldCover" />
              <StatCard value="SWIR + dist. agua" label="Variables más influyentes que NDVI" />
            </div>
          </div>
        </div>
      </Deck.Slide>

      {/* ============================================ 13 · ALERTAS + REPRODUCIBILIDAD */}
      <Deck.Slide title="Alertas y reproducibilidad" notes={SCRIPT.alerts}>
        <SlideHeader
          eyebrow="Operación · Hacia un Gemelo Digital"
          title="Alertas tempranas y reproducibilidad"
        />
        <div className="mt-[1.1cqw] grid flex-1 grid-cols-[1.25fr_1fr] gap-[1.4cqw]">
          <FigureFrame
            src="/figures/prog/semaforo.png"
            alt="Mapa semáforo del estado del manglar por estación: verde estable, amarillo en alerta, rojo crítico."
            className="h-full"
          />
          <div className="flex flex-col gap-[0.85cqw]">
            <div className="grid grid-cols-3 gap-[0.7cqw]">
              <StatCard value="5" label="Estaciones estables" />
              <StatCard value="3" label="Estaciones en alerta" />
              <StatCard value="0" label="Estaciones críticas" />
            </div>
            <FeatureItem icon={GitBranch} title="Validación trilingüe">
              Python, R y Julia producen valores equivalentes hasta tres decimales.
            </FeatureItem>
            <FeatureItem icon={Container} title="Reproducibilidad">
              Dashboard HTML, contenedor Docker y repositorio público en GitHub.
            </FeatureItem>
          </div>
        </div>
      </Deck.Slide>

      {/* ============================================ 14 · MONITOR EN VIVO */}
      <Deck.Slide title="Monitor en vivo" notes={SCRIPT.monitor}>
        <SlideHeader
          eyebrow="Producto · Monitor en vivo"
          title="El pipeline termina en un producto consultable"
        />
        <div className="mt-[1.1cqw] grid flex-1 grid-cols-[1.55fr_1fr] gap-[1.4cqw]">
          <FigureFrame
            src="/figures/prog/monitor.png"
            alt="CGSM Monitor: mapa interactivo del manglar con capas NDVI, estaciones y semáforo de alertas."
            className="h-full"
          />
          <div className="flex flex-col gap-[0.85cqw]">
            <Panel title="Cinco pestañas" icon={LayoutDashboard}>
              <ul className="flex flex-col gap-[0.5cqw]">
                {[
                  "Resumen: estado general y métricas clave",
                  "Cobertura: NDVI, cambio y mapa interactivo",
                  "Clima e hidrología: ENSO, caudal y CHIRPS",
                  "Validación multilenguaje: Python, R y Julia",
                  "Acerca de: datos, métodos y repositorio",
                ].map((t, i) => (
                  <li key={i} className="flex gap-[0.6cqw]">
                    <span className="mt-[0.5cqw] h-[0.45cqw] w-[0.45cqw] shrink-0 rounded-full bg-[var(--brand-primary)]" />
                    <span className="deck-sans text-[0.9cqw] leading-snug text-[var(--brand-ink-soft)]">
                      {t}
                    </span>
                  </li>
                ))}
              </ul>
            </Panel>
            <div className="grid grid-cols-3 gap-[0.7cqw]">
              <StatCard value="17" label="Capas temáticas" />
              <StatCard value="HTML" label="Autocontenido, sin Jupyter" />
              <StatCard value="GitHub" unit="Pages" label="Publicación web abierta" />
            </div>
            <a
              href="https://linaq11.github.io/proyecto-cgsm-curso/dashboard.html"
              target="_blank"
              rel="noreferrer"
              className="flex items-center gap-[0.7cqw] rounded-2xl bg-[var(--brand-primary)] px-[1.1cqw] py-[0.7cqw] no-underline transition-transform hover:scale-[1.01]"
            >
              <ExternalLink className="h-[1.3cqw] w-[1.3cqw] shrink-0 text-[var(--brand-gold)]" strokeWidth={2} />
              <span className="deck-sans text-[0.86cqw] leading-snug text-white">
                <span className="font-semibold">linaq11.github.io</span>
                /proyecto-cgsm-curso/dashboard.html
              </span>
            </a>
          </div>
        </div>
      </Deck.Slide>

      {/* ================================================= 15 · CONCLUSIONES */}
      <Deck.Slide title="Conclusiones" variant="cover" notes={SCRIPT.conclusions}>
        <p className="deck-sans text-[0.86cqw] font-semibold uppercase tracking-[0.26em] text-[var(--brand-gold)]">
          Conclusiones
        </p>
        <h2 className="deck-serif mt-[1cqw] max-w-[86%] text-[2.5cqw] font-semibold leading-[1.12] text-white">
          Un flujo reproducible para monitorear el manglar con tres lenguajes
        </h2>
        <span className="mt-[1.2cqw] block h-[3px] w-[4.4cqw] rounded-full bg-[var(--brand-gold)]" />
        <div className="mt-[1.6cqw] grid w-full grid-cols-3 gap-[1.2cqw]">
          {[
            {
              icon: Activity,
              t: "Hallazgos",
              d: "Respuesta temporal a El Niño 2016 y La Niña 2020; consolidación estructural; Random Forest mejora la regla por umbrales.",
            },
            {
              icon: AlertTriangle,
              t: "Límites",
              d: "Sin validación de campo independiente; red hidrométrica limitada; relaciones de asociación temporal, no causalidad.",
            },
            {
              icon: Target,
              t: "Trabajo futuro",
              d: "Validación in situ, más estaciones y transición hacia un Gemelo Digital costero con alertas.",
            },
          ].map((c, i) => (
            <div
              key={i}
              className="rounded-2xl border border-white/15 bg-white/10 p-[1.1cqw]"
            >
              <c.icon className="h-[1.6cqw] w-[1.6cqw] text-[var(--brand-gold)]" strokeWidth={2} />
              <p className="deck-sans mt-[0.7cqw] text-[1.05cqw] font-semibold text-white">
                {c.t}
              </p>
              <p className="deck-sans mt-[0.35cqw] text-[0.86cqw] leading-snug text-[var(--brand-on-color-soft)]">
                {c.d}
              </p>
            </div>
          ))}
        </div>
        <p className="deck-sans mt-[1.8cqw] text-[1cqw] text-[var(--brand-on-color-soft)]">
          {PRESENTER} &nbsp;&middot;&nbsp; Monitor: {MONITOR} &nbsp;&middot;&nbsp; Gracias.
        </p>
      </Deck.Slide>
    </Deck.Root>
  );
}

/* ----------------------------------------------------- helper local ---- */

function FigureFrame({
  src,
  alt,
  className,
  contain = true,
}: {
  src: string;
  alt: string;
  className?: string;
  contain?: boolean;
}) {
  return (
    <div
      className={cn(
        "relative overflow-hidden rounded-2xl border border-[var(--brand-line)] bg-white",
        className,
      )}
    >
      <Image
        src={src}
        alt={alt}
        fill
        sizes="70vw"
        className={cn(contain ? "object-contain p-[0.8cqw]" : "object-cover")}
        priority
      />
    </div>
  );
}
