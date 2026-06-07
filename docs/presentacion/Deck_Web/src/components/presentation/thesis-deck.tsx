"use client";

import Image from "next/image";
import {
  Boxes,
  CalendarRange,
  ChevronRight,
  Cloud,
  CloudRain,
  Coins,
  Cpu,
  Database,
  Globe,
  Layers,
  LineChart,
  MapPin,
  Ruler,
  Satellite,
  ScanSearch,
  Target,
  Trees,
  TrendingDown,
  Waves,
  type LucideIcon,
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
   Cover credits — edit these lines.
   ---------------------------------------------------------------- */
const PRESENTER = "Lina Quintero Fonseca";
const ADVISOR = "Advisor: Iván Lizarazo";
const DEFENSE_DATE = "June 16, 2026";
const PROGRAM = "Master's in Geomatics";
const FACULTY = "Facultad de Ciencias Agrarias · Sede Bogotá";

/* ----------------------------------------------------------------
   Speaker script (Spanish) — what to say on each slide (~1 min each).
   Toggle in the app with the "N" key or the notebook button.
   ---------------------------------------------------------------- */
const SCRIPT = {
  cover:
    "Buenos días. Agradezco al jurado y a mi director por su tiempo. Presento mi propuesta de tesis de la Maestría en Geomática, titulada Gemelo Digital basado en GeoAI para el modelamiento dinámico de ecosistemas costeros. En esta propuesta, el marco conceptual del Gemelo Digital se desarrolla y evalúa tomando como caso de estudio la Ciénaga Grande de Santa Marta, con énfasis en el monitoreo dinámico del manglar, su condición y la inundación asociada. El título plantea un marco transferible; la aplicación empírica está delimitada a la CGSM.",
  context:
    "La CGSM es un sistema estratégico del Caribe colombiano. Su importancia no está solo en la extensión del manglar, sino en los servicios ecosistémicos que sostiene y en su historia de degradación y recuperación. El problema de fondo es que hay datos satelitales frecuentes, pero esa información no siempre se convierte en monitoreo espacialmente explícito y útil para la gestión. Las estaciones son fundamentales, pero no capturan toda la heterogeneidad espacial del sistema.",
  study:
    "Para evitar una propuesta abstracta, el área de estudio se delimitó desde el inicio. El AOI es el núcleo lagunar-manglar de la Ciénaga Grande de Santa Marta, aproximadamente 1.286 kilómetros cuadrados. Uso el término sensu stricto para aclarar que la tesis no analiza todo el sitio Ramsar ni todo el delta del Magdalena, sino ese núcleo definido como área de estudio. Además, se revisó la disponibilidad de imágenes y capas de referencia en Google Earth Engine para asegurar que la metodología sea viable desde la fase inicial. Las áreas métricas se trabajarán en EPSG:9377, que corresponde al sistema oficial colombiano.",
  gap:
    "La brecha no está en la ausencia de datos. La brecha está en la integración. Hay datos ópticos, radar y referencias institucionales, pero falta una arquitectura que los organice como datacube, evalúe modelos GeoAI y entregue productos reproducibles para monitoreo. La oportunidad de esta investigación está en conectar esos componentes en un solo flujo evaluable.",
  objectives:
    "La pregunta se concentra en cómo integrar datos ópticos y radar dentro de un Gemelo Digital basado en GeoAI para monitorear tres variables: extensión, condición e inundación. La nubosidad persistente y la variabilidad hidroclimática justifican el uso de fusión óptico-radar. Los tres objetivos responden directamente a esa pregunta: primero organizo los datos, luego evalúo los modelos y finalmente integro los productos en un prototipo reproducible.",
  coherence:
    "Esta diapositiva responde a una preocupación típica del jurado: la coherencia interna. La propuesta no presenta técnicas sueltas. Cada objetivo tiene una pregunta, un método, un resultado y una forma de evaluación. El objetivo 1 produce la infraestructura de datos; el objetivo 2 produce los mapas y la comparación de modelos; y el objetivo 3 integra esos productos en un prototipo reproducible.",
  framework:
    "La metodología se organiza en tres capas. La primera es la capa de observación: sensores ópticos, radar y datos de referencia. La segunda es la capa analítica: datacube, Random Forest, modelos SAM-based y detección de inundación. La tercera es la capa operativa: flujo automatizado, tablero y repositorio. La validación conecta las tres capas con el Global Mangrove Watch, el INVEMAR y CARICOMP.",
  data:
    "Sobre los métodos, priorizo una ruta concreta. Primero construyo un datacube listo para análisis, con composiciones ópticas y SAR, índices espectrales y co-registro espacial. La ruta principal de clasificación es Random Forest porque es interpretable, corre en Earth Engine y funciona bien con datos heterogéneos. SamGeo y MW-SAM se evalúan como comparación, para valorar el aporte del radar y de la segmentación, no como promesa de superioridad.",
  metrics:
    "Cada producto tiene una métrica. Para clasificación no me quedo solo con exactitud global, porque puede ocultar errores en clases difíciles. Por eso uso precisión, recall y F1 por clase. Para segmentación uso IoU, y para variables continuas usaría RMSE y R cuadrado. Kappa puede reportarse como métrica secundaria, pero no será la base de interpretación.",
  example:
    "Este ejemplo evita que la metodología suene abstracta. Muestra el flujo completo: primero se ingieren los datos, luego se clasifica la cobertura, después se detecta inundación según el tipo de dosel y finalmente el prototipo muestra frecuencia de inundación por sector. El producto no reemplaza una decisión institucional, pero sí genera una capa de apoyo para priorizar monitoreo.",
  results:
    "Los resultados esperados se organizan por objetivo. El primero entrega el datacube; el segundo, los mapas validados y el benchmark; el tercero, el prototipo interactivo y el repositorio. El cronograma se distribuye en cuatro semestres: construcción del datacube, experimentos de modelos, análisis de inundación y cambio, integración del prototipo y escritura. La latencia objetivo y la capacidad computacional quedan documentadas como referencia: el procesamiento se apoya en Earth Engine, con requerimientos limitados de infraestructura local.",
  closing:
    "Cierro con tres ideas. Primero, el problema no es la ausencia de datos, sino su integración operativa. Segundo, la metodología es evaluable porque cada producto tiene datos, referencia y métrica. Tercero, la contribución es transferible como arquitectura, no como un modelo que se copia sin recalibrar. Muchas gracias, quedo atenta a sus preguntas y comentarios.",
  feasibility:
    "Esta diapositiva es de respaldo. El proyecto es viable porque se basa en datos abiertos, Google Earth Engine, software abierto e infraestructura institucional. El presupuesto operativo se concentra en apoyo técnico puntual, almacenamiento, validación o socialización institucional y divulgación. No requiere compra de imágenes comerciales.",
};

export function ThesisDeck() {
  return (
    <Deck.Root brand="verde">
      {/* ====================================================== 01 · COVER */}
      <Deck.Slide title="Cover" variant="cover" notes={SCRIPT.cover}>
        <p className="deck-sans text-[0.86cqw] font-semibold uppercase tracking-[0.28em] text-[var(--brand-gold)]">
          Universidad Nacional de Colombia
        </p>
        <p className="deck-sans mt-[0.5cqw] text-[0.85cqw] uppercase tracking-[0.22em] text-[var(--brand-on-color-soft)]">
          Master&apos;s Thesis Proposal &middot; Defense
        </p>
        <h1 className="deck-serif mt-[1.6cqw] max-w-[78%] text-[3.5cqw] font-semibold leading-[1.05] text-white">
          GeoAI-based Digital Twin for Dynamic Modeling of Coastal Ecosystems
        </h1>
        <span className="mt-[1.4cqw] block h-[3px] w-[5cqw] rounded-full bg-[var(--brand-gold)]" />
        <p className="deck-sans mt-[1.4cqw] max-w-[64%] text-[1.25cqw] leading-snug text-[var(--brand-on-color-soft)]">
          Dynamic monitoring of the Ci&eacute;naga Grande de Santa Marta under
          persistent tropical cloud cover and hydroclimatic variability.
        </p>
        <div className="mt-[2.2cqw] flex flex-col gap-[0.35cqw]">
          <p className="deck-serif text-[1.5cqw] font-semibold text-white">
            {PRESENTER}
          </p>
          <p className="deck-sans text-[0.98cqw] text-[var(--brand-on-color-soft)]">
            {PROGRAM} &middot; {FACULTY}
          </p>
          <p className="deck-sans text-[0.98cqw] text-[var(--brand-on-color-soft)]">
            {ADVISOR} &nbsp;&middot;&nbsp; {DEFENSE_DATE}
          </p>
        </div>
      </Deck.Slide>

      {/* ============================================ 02 · CONTEXT / PROBLEM */}
      <Deck.Slide title="Context & the problem" notes={SCRIPT.context}>
        <SlideHeader
          eyebrow="Context · Why it matters"
          title="The Ciénaga Grande de Santa Marta"
        />
        <div className="mt-[1.4cqw] grid flex-1 grid-cols-[1.15fr_1fr] gap-[2cqw]">
          <div className="flex flex-col justify-between">
            <Lead>
              A strategic coastal lagoon-delta system in the Colombian Caribbean,
              with documented mangrove dieback, restoration efforts and persistent
              monitoring challenges.
            </Lead>
            <div className="grid grid-cols-2 gap-[0.9cqw]">
              <StatCard value="1,286" unit="km²" label="Core lagoon-mangrove system" />
              <StatCard value=">24,000" unit="ha" label="Historical mangrove dieback" />
              <StatCard value="~300,000" label="People linked to ecosystem services" />
              <StatCard value="5–12" unit="d" label="Satellite revisit potential" />
            </div>
          </div>
          <Panel title="The monitoring gap" icon={TrendingDown} className="justify-center">
            <ul className="flex flex-col gap-[0.8cqw]">
              {[
                "Fixed stations provide valuable but spatially limited information.",
                "Persistent cloud cover limits optical monitoring.",
                "SAR improves continuity, but vegetation interpretation remains complex.",
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
                Recent canopy loss in the{" "}
                <span className="font-semibold text-[var(--brand-primary)]">
                  Aguas Negras
                </span>{" "}
                sector shows the need for spatially explicit monitoring.
              </p>
            </div>
          </Panel>
        </div>
      </Deck.Slide>

      {/* ====================================== 03 · STUDY AREA + DATA READINESS */}
      <Deck.Slide title="Study area & data" notes={SCRIPT.study}>
        <SlideHeader
          eyebrow="Study area · Data readiness"
          title="A bounded AOI with available multi-sensor data"
        />
        <div className="mt-[1.2cqw] grid flex-1 grid-cols-[0.92fr_1.08fr] gap-[1.6cqw]">
          <div className="flex flex-col gap-[0.9cqw]">
            <FeatureItem icon={MapPin} title="AOI — Core CGSM study area">
              1,286 km² lagoon-mangrove polygon within the broader Ramsar
              system (Magdalena, 10.7°–11.05° N).
            </FeatureItem>
            <FeatureItem icon={Satellite} title="Imagery availability checked in GEE">
              Sentinel-2, Sentinel-1 C-band, ALOS-2 L-band, Landsat 8/9 and
              ancillary layers for 2015–2025.
            </FeatureItem>
            <FeatureItem icon={MapPin} title="Reference layers and metric georeferencing">
              GMW v3.0, INVEMAR stations, CARICOMP and SRTM; metric areas in
              EPSG:9377 (MAGNA-SIRGAS).
            </FeatureItem>
          </div>
          <FigureFrame
            src="/figures/study-area.png"
            alt="Study area: Colombia, Magdalena, and the Ciénaga Grande de Santa Marta with the 1,286 km² AOI, GMW mangrove cover and six INVEMAR stations."
            className="h-full"
          />
        </div>
      </Deck.Slide>

      {/* ============================================ 04 · THE GAP */}
      <Deck.Slide title="The knowledge gap" notes={SCRIPT.gap}>
        <SlideHeader
          eyebrow="Why this research"
          title="Three gaps constrain operational monitoring"
        />
        <div className="mt-[1.6cqw] grid flex-1 grid-cols-3 gap-[1.2cqw] content-center">
          <NumberedItem n={1} title="Data infrastructure">
            No analysis-ready optical-SAR datacube has been implemented for CGSM
            monitoring.
          </NumberedItem>
          <NumberedItem n={2} title="GeoAI benchmarking">
            SAM-based segmentation has not been systematically evaluated for CGSM
            mangrove and flood mapping.
          </NumberedItem>
          <NumberedItem n={3} title="Operational integration">
            Monitoring products remain weakly connected to automated, reproducible
            Digital Twin workflows.
          </NumberedItem>
        </div>
        <div className="rounded-xl bg-[var(--brand-tint)] px-[1.2cqw] py-[0.9cqw]">
          <p className="deck-sans text-[0.98cqw] leading-snug text-[var(--brand-ink)]">
            <span className="font-semibold text-[var(--brand-primary)]">
              Opportunity:
            </span>{" "}
            connect satellite archives, GeoAI models and monitoring outputs in
            one evaluable framework.
          </p>
        </div>
      </Deck.Slide>

      {/* ==================================== 05 · QUESTION & OBJECTIVES */}
      <Deck.Slide title="Question & objectives" notes={SCRIPT.objectives}>
        <SlideHeader eyebrow="Research question · Objectives" title="One question, three objectives" />
        <div className="mt-[1.3cqw] flex flex-1 flex-col justify-center gap-[1.5cqw]">
          <Panel accent icon={Target} className="py-[1.1cqw]">
            <p className="deck-serif text-[1.25cqw] font-medium leading-snug text-white">
              How can optical and radar Earth observation be integrated into a
              GeoAI-based Digital Twin to monitor mangrove extent, condition and
              flooding dynamics in the CGSM?
            </p>
          </Panel>
          <div className="grid grid-cols-3 gap-[1.2cqw]">
            <NumberedItem n={1} title="Design the datacube" tag="Objective 1">
              Integrate multi-sensor optical and radar data into analysis-ready
              composites.
            </NumberedItem>
            <NumberedItem n={2} title="Benchmark GeoAI" tag="Objective 2">
              Compare SAM-based segmentation against a Random Forest baseline.
            </NumberedItem>
            <NumberedItem n={3} title="Build the Digital Twin" tag="Objective 3">
              Integrate outputs into reusable, automated and reproducible
              workflows.
            </NumberedItem>
          </div>
        </div>
      </Deck.Slide>

      {/* ============================================ 06 · COHERENCE CHECKLIST */}
      <Deck.Slide title="Internal coherence" notes={SCRIPT.coherence}>
        <SlideHeader
          eyebrow="Verification checklist"
          title="One coherent thread"
        />
        <div className="mt-[1.4cqw] flex flex-1 flex-col">
          <div className="overflow-hidden rounded-2xl border border-[var(--brand-line)]">
            <div className="grid grid-cols-[0.7fr_1.3fr] bg-[var(--brand-primary)] px-[1.2cqw] py-[0.6cqw] deck-sans text-[0.74cqw] font-semibold uppercase tracking-wider text-white">
              <span>Element</span>
              <span>What it answers</span>
            </div>
            {(
              [
                ["Title", "GeoAI Digital Twin for dynamic coastal ecosystem modeling"],
                ["Case study", "CGSM mangrove and flooding dynamics"],
                ["Problem", "Fragmented optical-radar monitoring"],
                ["Question", "Integration of EO data, GeoAI and Digital Twin"],
                ["Objective 1", "Datacube"],
                ["Objective 2", "Model benchmark"],
                ["Objective 3", "Reproducible prototype"],
              ] as [string, string][]
            ).map(([el, ans], i) => (
              <div
                key={i}
                className="grid grid-cols-[0.7fr_1.3fr] items-center border-t border-[var(--brand-line)] px-[1.2cqw] py-[0.5cqw] odd:bg-[var(--brand-paper)] even:bg-[var(--brand-paper-2)]"
              >
                <span className="deck-sans text-[0.98cqw] font-semibold text-[var(--brand-primary)]">
                  {el}
                </span>
                <span className="deck-sans text-[0.98cqw] text-[var(--brand-ink)]">
                  {ans}
                </span>
              </div>
            ))}
          </div>
          <p className="mt-[0.9cqw] deck-sans text-[0.92cqw] text-[var(--brand-ink-soft)]">
            Each objective has a method, an output and an evaluation criterion.
          </p>
        </div>
      </Deck.Slide>

      {/* ============================================ 07 · FRAMEWORK FIGURE */}
      <Deck.Slide title="Conceptual framework" notes={SCRIPT.framework}>
        <div className="flex items-center justify-between">
          <SlideHeader
            eyebrow="Methodology · Operational framework"
            title="From satellite observations to monitoring outputs"
          />
          <div className="hidden items-center gap-[0.5cqw] sm:flex">
            <Tag>Observation</Tag>
            <ChevronRight className="h-[1cqw] w-[1cqw] text-[var(--brand-primary)]/50" />
            <Tag>GeoAI modeling</Tag>
            <ChevronRight className="h-[1cqw] w-[1cqw] text-[var(--brand-primary)]/50" />
            <Tag>Digital Twin</Tag>
          </div>
        </div>
        <FigureFrame
          src="/figures/framework.png"
          alt="Conceptual and operational framework: Observation (Sentinel-2, Sentinel-1, ALOS-2, Landsat, ancillary) to GeoAI modeling (datacube, indices, Random Forest, SamGeo/MW-SAM, flood and change detection) to Digital Twin (automated pipeline, dashboard, reproducible workflow), validated against GMW, INVEMAR and CARICOMP."
          className="mt-[1cqw] flex-1"
          contain
        />
      </Deck.Slide>

      {/* ============================================ 08 · DATA & ROUTE */}
      <Deck.Slide title="Data & method" notes={SCRIPT.data}>
        <SlideHeader
          eyebrow="Methods · Objectives 1 &amp; 2"
          title="Datacube + prioritized modeling route"
        />
        <div className="mt-[1.4cqw] grid flex-1 grid-cols-2 gap-[1.4cqw]">
          <Panel title="Analysis-ready datacube" icon={Layers}>
            <ul className="flex flex-col gap-[0.65cqw]">
              {[
                "10 m working grid",
                "Dry-season optical composites",
                "Seasonal SAR composites",
                "NDVI · NDWI · CMRI · NDBaI",
              ].map((t, i) => (
                <li key={i} className="flex gap-[0.6cqw]">
                  <span className="mt-[0.5cqw] h-[0.45cqw] w-[0.45cqw] shrink-0 rounded-full bg-[var(--brand-primary)]" />
                  <span className="deck-sans text-[0.92cqw] leading-snug text-[var(--brand-ink-soft)]">
                    {t}
                  </span>
                </li>
              ))}
            </ul>
            <div className="mt-[1.1cqw]">
              <p className="deck-sans text-[0.66cqw] font-semibold uppercase tracking-wider text-[var(--brand-ink-soft)]">
                The datacube · layers co-registered at 10 m · 2015–2025
              </p>
              <div className="mt-[0.6cqw] flex flex-col gap-[0.42cqw]">
                {(
                  [
                    ["Sentinel-2 · optical", "#0b7a4b"],
                    ["Sentinel-1 · C-band SAR", "#3b82c4"],
                    ["ALOS-2 · L-band SAR", "#ffb93e"],
                    ["Indices: NDVI · NDWI · CMRI", "#14b086"],
                  ] as [string, string][]
                ).map(([n, c]) => (
                  <div
                    key={n}
                    className="flex items-center gap-[0.7cqw] rounded-lg border border-[var(--brand-line)] bg-[var(--brand-paper)] px-[0.8cqw] py-[0.42cqw]"
                  >
                    <span
                      className="h-[0.7cqw] w-[0.7cqw] shrink-0 rounded-full"
                      style={{ background: c }}
                    />
                    <span className="deck-sans text-[0.92cqw] text-[var(--brand-ink)]">
                      {n}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </Panel>

          <Panel title="Chosen route: Random Forest" icon={Cpu} accent>
            <p className="deck-sans text-[0.92cqw] leading-snug text-white/90">
              Primary classifier on the fused datacube — 200 trees,
              <span className="font-semibold"> smileRandomForest</span> in GEE.
            </p>
            <ul className="mt-[0.7cqw] flex flex-col gap-[0.6cqw]">
              {[
                "Widely used in tropical mangrove mapping",
                "Interpretable; transparent variable importance (Gini)",
                "Robust with limited, heterogeneous samples",
                "GEE-native — runs at cloud scale, no local setup",
              ].map((t, i) => (
                <li key={i} className="flex gap-[0.6cqw]">
                  <span className="mt-[0.5cqw] h-[0.45cqw] w-[0.45cqw] shrink-0 rounded-full bg-[var(--brand-gold)]" />
                  <span className="deck-sans text-[0.88cqw] leading-snug text-white/85">
                    {t}
                  </span>
                </li>
              ))}
            </ul>
            <p className="deck-sans mt-[0.8cqw] text-[0.84cqw] text-white/70">
              Benchmarked against{" "}
              <span className="font-semibold text-[var(--brand-gold)]">
                SamGeo / MW-SAM
              </span>{" "}
              to assess the added value of radar and segmentation.
            </p>
          </Panel>
        </div>
      </Deck.Slide>

      {/* ============================== 09 · CLASSIFICATION, FLOODS & METRICS */}
      <Deck.Slide title="Mapping & evaluation" notes={SCRIPT.metrics}>
        <SlideHeader
          eyebrow="Methods · Mapping &amp; evaluation criteria"
          title="Classification, floods & metrics"
        />
        <div className="mt-[1.4cqw] grid flex-1 grid-cols-2 gap-[1.4cqw]">
          <div className="flex flex-col gap-[1cqw]">
            <Panel title="Classes & flood mapping" icon={CloudRain}>
              <div className="mb-[0.7cqw] flex gap-[0.5cqw]">
                {["Intact", "Degraded", "Non-mangrove"].map((t) => (
                  <Tag key={t}>{t}</Tag>
                ))}
              </div>
              <ul className="flex flex-col gap-[0.5cqw]">
                {[
                  "C-band for open / degraded areas",
                  "L-band support for closed canopy",
                  "Layers merged by canopy-closure stratification",
                ].map((t, i) => (
                  <li key={i} className="flex gap-[0.6cqw]">
                    <span className="mt-[0.5cqw] h-[0.45cqw] w-[0.45cqw] shrink-0 rounded-full bg-[var(--brand-primary)]" />
                    <span className="deck-sans text-[0.88cqw] leading-snug text-[var(--brand-ink-soft)]">
                      {t}
                    </span>
                  </li>
                ))}
              </ul>
            </Panel>
          </div>

          <Panel title="Evaluation criteria" icon={Ruler}>
            <div className="flex flex-col gap-[0.7cqw]">
              <MetricRow
                icon={ScanSearch}
                task="Classification (RF)"
                metrics="Overall Accuracy · per-class Precision / Recall / F1"
              />
              <MetricRow
                icon={Layers}
                task="Segmentation (SAM)"
                metrics="Intersection-over-Union (IoU)"
              />
              <MetricRow
                icon={LineChart}
                task="Continuous (canopy height)"
                metrics="RMSE · R²"
              />
              <div className="rounded-xl bg-[var(--brand-tint)] p-[0.8cqw]">
                <p className="deck-sans text-[0.86cqw] leading-snug text-[var(--brand-ink)]">
                  Kappa only as a secondary metric — interpretation relies on
                  class-specific metrics. Validated against{" "}
                  <span className="font-semibold text-[var(--brand-primary)]">
                    GMW v3.0
                  </span>
                  , INVEMAR and CARICOMP.
                </p>
              </div>
            </div>
          </Panel>
        </div>
      </Deck.Slide>

      {/* ============================================ 10 · WORKED EXAMPLE */}
      <Deck.Slide title="End-to-end example" notes={SCRIPT.example}>
        <SlideHeader
          eyebrow="Worked example · Rinconada sector"
          title="From satellite pixels to a monitoring layer"
        />
        <div className="flex flex-1 items-center">
          <div className="grid w-full grid-cols-4 gap-[1cqw]">
            <StepCard
              n={1}
              icon={Database}
              title="Ingest"
              text="S2 dry-season, S1 wet-season and ALOS-2 L-band composites for the Rinconada sector."
            />
            <StepCard
              n={2}
              icon={Cpu}
              title="Classify"
              text="RF labels each pixel intact / degraded / non-mangrove; SAM benchmarked."
            />
            <StepCard
              n={3}
              icon={Waves}
              title="Detect floods"
              text="L-band support under closed canopy; C-band in open / degraded areas."
            />
            <StepCard
              n={4}
              icon={Globe}
              title="Support monitoring"
              text="Flood frequency by sector; comparison against the 2015–2025 baseline."
            />
          </div>
        </div>
      </Deck.Slide>

      {/* ====================================== 11 · RESULTS · DT · TIMELINE */}
      <Deck.Slide title="Results, twin & timeline" notes={SCRIPT.results}>
        <SlideHeader
          eyebrow="Expected results · 24 months"
          title="Outputs, prototype and plan"
        />
        <div className="mt-[1.1cqw] grid grid-cols-3 gap-[1cqw]">
          <FeatureItem icon={Boxes} title="Obj. 1 — Datacube">
            Multi-sensor analysis-ready datacube, 2015–2025, 10 m, on GEE.
          </FeatureItem>
          <FeatureItem icon={Trees} title="Obj. 2 — GeoAI maps">
            Validated mangrove + flood maps; RF-vs-SAM comparison.
          </FeatureItem>
          <FeatureItem icon={Globe} title="Obj. 3 — Digital Twin">
            Interactive prototype + open pipeline, article & technical report.
          </FeatureItem>
        </div>

        <div className="mt-[1.1cqw] flex flex-1 flex-col">
          <div className="rounded-2xl border border-[var(--brand-line)] bg-[var(--brand-paper-2)] p-[1.2cqw]">
            <div className="mb-[0.6cqw] grid grid-cols-[1.7fr_repeat(4,1fr)] deck-sans text-[0.7cqw] font-semibold uppercase tracking-wider text-[var(--brand-ink-soft)]">
              <span>Activity</span>
              <span className="text-center">S1</span>
              <span className="text-center">S2</span>
              <span className="text-center">S3</span>
              <span className="text-center">S4</span>
            </div>
            {(
              [
                ["Datacube design & construction", [1, 1, 0, 0]],
                ["RF + SAM/MW-SAM experiments", [0, 1, 1, 0]],
                ["Flood dynamics & change detection", [0, 1, 1, 0]],
                ["Digital Twin & dashboard", [0, 0, 1, 1]],
                ["Writing · article · defense", [0, 0, 1, 1]],
              ] as [string, number[]][]
            ).map(([label, cells], i) => (
              <div key={i} className="grid grid-cols-[1.7fr_repeat(4,1fr)] items-center py-[0.32cqw]">
                <span className="deck-sans text-[0.86cqw] text-[var(--brand-ink)]">
                  {label}
                </span>
                {cells.map((on, j) => (
                  <div key={j} className="px-[0.4cqw]">
                    <div
                      className={cn(
                        "h-[0.62cqw] rounded-full",
                        on ? "bg-[var(--brand-primary)]" : "bg-[var(--brand-line)]",
                      )}
                    />
                  </div>
                ))}
              </div>
            ))}
          </div>
        </div>
      </Deck.Slide>

      {/* ============================================ 12 · CLOSING */}
      <Deck.Slide title="Take-home & thanks" variant="cover" notes={SCRIPT.closing}>
        <p className="deck-sans text-[0.86cqw] font-semibold uppercase tracking-[0.28em] text-[var(--brand-gold)]">
          Take-home messages
        </p>
        <div className="mt-[1.3cqw] flex flex-col gap-[1cqw]">
          {(
            [
              ["1", "The problem is operational", "Data exist, but monitoring remains fragmented."],
              ["2", "The method is evaluable", "Each output has a target variable, reference data and a metric."],
              ["3", "The contribution is transferable", "The workflow can be adapted to other tropical coastal wetlands."],
            ] as [string, string, string][]
          ).map(([n, t, d]) => (
            <div key={n} className="flex items-baseline gap-[1cqw]">
              <span className="deck-serif text-[1.7cqw] font-semibold leading-none text-[var(--brand-gold)]">
                {n}
              </span>
              <div>
                <p className="deck-serif text-[1.2cqw] font-semibold leading-tight text-white">
                  {t}
                </p>
                <p className="deck-sans text-[0.98cqw] text-[var(--brand-on-color-soft)]">
                  {d}
                </p>
              </div>
            </div>
          ))}
        </div>
        <div className="mt-[1.8cqw]">
          <p className="deck-serif text-[1.7cqw] font-semibold text-white">
            Thank you
          </p>
          <p className="deck-sans mt-[0.2cqw] text-[0.96cqw] text-[var(--brand-on-color-soft)]">
            Questions and comments
          </p>
        </div>
      </Deck.Slide>

      {/* ===================================== 13 · BACKUP · FEASIBILITY */}
      <Deck.Slide title="Backup · Feasibility" notes={SCRIPT.feasibility}>
        <SlideHeader
          eyebrow="Backup · Feasibility"
          title="Timeline & budget"
        />
        <div className="mt-[1.3cqw] grid flex-1 grid-cols-2 gap-[1.4cqw]">
          {/* Timeline */}
          <Panel title="Timeline" icon={CalendarRange}>
            <div className="mb-[0.9cqw] flex items-baseline gap-[0.5cqw]">
              <span className="deck-serif text-[2cqw] font-semibold leading-none text-[var(--brand-primary)]">
                24
              </span>
              <span className="deck-sans text-[0.96cqw] text-[var(--brand-ink-soft)]">
                months &middot; 4 semesters
              </span>
            </div>
            <div className="flex flex-col gap-[0.6cqw]">
              {[
                ["Phase 1", "Datacube construction", "S1–S2"],
                ["Phase 2", "GeoAI benchmark & flood mapping", "S2–S3"],
                ["Phase 3", "Digital Twin · writing · defense", "S3–S4"],
              ].map(([p, t, s]) => (
                <div
                  key={p}
                  className="flex items-center justify-between border-b border-[var(--brand-line)] pb-[0.5cqw]"
                >
                  <div className="flex items-center gap-[0.7cqw]">
                    <span className="deck-sans text-[0.68cqw] font-semibold uppercase tracking-wider text-[var(--brand-primary)]">
                      {p}
                    </span>
                    <span className="deck-sans text-[0.92cqw] text-[var(--brand-ink)]">
                      {t}
                    </span>
                  </div>
                  <Tag>{s}</Tag>
                </div>
              ))}
            </div>
          </Panel>

          {/* Budget */}
          <Panel title="Budget estimate" icon={Coins}>
            <div className="mb-[0.9cqw] flex items-baseline gap-[0.6cqw]">
              <span className="deck-serif text-[2cqw] font-semibold leading-none text-[var(--brand-primary)]">
                ~15–18 M
              </span>
              <span className="deck-sans text-[0.88cqw] text-[var(--brand-ink-soft)]">
                COP · estimated operating budget
              </span>
            </div>
            <p className="deck-sans text-[0.72cqw] font-semibold uppercase tracking-wider text-[var(--brand-ink-soft)]">
              Main cost drivers
            </p>
            <ul className="mt-[0.6cqw] flex flex-col gap-[0.55cqw]">
              {[
                "Technical support",
                "Storage & backup",
                "Validation & institutional meetings",
                "Publication / dissemination support",
              ].map((t, i) => (
                <li key={i} className="flex gap-[0.6cqw]">
                  <span className="mt-[0.5cqw] h-[0.45cqw] w-[0.45cqw] shrink-0 rounded-full bg-[var(--brand-primary)]" />
                  <span className="deck-sans text-[0.94cqw] text-[var(--brand-ink-soft)]">
                    {t}
                  </span>
                </li>
              ))}
            </ul>
            <p className="mt-[0.9cqw] deck-sans text-[0.74cqw] leading-snug text-[var(--brand-ink-soft)]">
              Academic supervision and institutional infrastructure are treated
              as{" "}
              <span className="font-semibold text-[var(--brand-ink)]">
                in-kind support
              </span>
              .
            </p>
          </Panel>
        </div>

        <div className="mt-[1cqw] flex items-center gap-[0.8cqw] rounded-2xl bg-[var(--brand-tint)] px-[1.2cqw] py-[0.9cqw]">
          <Cloud className="h-[1.4cqw] w-[1.4cqw] shrink-0 text-[var(--brand-primary)]" strokeWidth={2} />
          <p className="deck-sans text-[0.96cqw] leading-snug text-[var(--brand-ink)]">
            Mostly based on{" "}
            <span className="font-semibold text-[var(--brand-primary)]">
              open data and institutional infrastructure
            </span>{" "}
            — open satellite archives (Sentinel, Landsat, ALOS-2, GMW), Google
            Earth Engine, and UNAL computing. No commercial imagery is required.
          </p>
        </div>
      </Deck.Slide>
    </Deck.Root>
  );
}

/* ----------------------------------------------------- local helpers ---- */

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

function MetricRow({
  icon: Icon,
  task,
  metrics,
}: {
  icon: LucideIcon;
  task: string;
  metrics: string;
}) {
  return (
    <div className="flex items-start gap-[0.7cqw] rounded-xl border border-[var(--brand-line)] bg-[var(--brand-paper)] p-[0.8cqw]">
      <span className="inline-flex h-[1.8cqw] w-[1.8cqw] shrink-0 items-center justify-center rounded-lg bg-[var(--brand-tint-strong)] text-[var(--brand-primary)]">
        <Icon className="h-[0.95cqw] w-[0.95cqw]" strokeWidth={2} />
      </span>
      <div>
        <p className="deck-sans text-[0.88cqw] font-semibold text-[var(--brand-ink)]">
          {task}
        </p>
        <p className="deck-sans text-[0.76cqw] leading-snug text-[var(--brand-ink-soft)]">
          {metrics}
        </p>
      </div>
    </div>
  );
}

function StepCard({
  n,
  icon: Icon,
  title,
  text,
}: {
  n: number;
  icon: LucideIcon;
  title: string;
  text: string;
}) {
  return (
    <div className="flex h-full flex-col rounded-2xl border border-[var(--brand-line)] bg-[var(--brand-paper-2)] p-[1cqw]">
      <div className="flex items-center gap-[0.6cqw]">
        <span className="inline-flex h-[1.8cqw] w-[1.8cqw] items-center justify-center rounded-full bg-[var(--brand-primary)] deck-serif text-[0.95cqw] font-semibold text-white">
          {n}
        </span>
        <Icon className="h-[1.2cqw] w-[1.2cqw] text-[var(--brand-primary)]" strokeWidth={2} />
      </div>
      <p className="deck-serif mt-[0.7cqw] text-[1.05cqw] font-semibold text-[var(--brand-ink)]">
        {title}
      </p>
      <p className="deck-sans mt-[0.45cqw] text-[0.84cqw] leading-snug text-[var(--brand-ink-soft)]">
        {text}
      </p>
    </div>
  );
}
