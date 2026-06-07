# Guion del orador (ES) — Sustentación de propuesta

**GeoAI-based Digital Twin for Dynamic Modeling of Coastal Ecosystems · CGSM**
Lina Quintero Fonseca · Maestría en Geomática · Universidad Nacional de Colombia
Director: Iván Lizarazo · Sustentación: 16 de junio de 2026

Duración objetivo: ~11 minutos · ~1 minuto por diapositiva.
Las diapositivas están en inglés; el guion es para hablar en español.
En la app, abre/cierra estas notas con la tecla **N**. En PowerPoint, vista de moderador.

Línea argumental que se mantiene en todas las diapositivas:
- **Problema claro:** los datos existen, pero el monitoreo sigue fragmentado.
- **Método evaluable:** cada producto tiene variable, referencia y métrica.
- **Aporte defendible:** no se promete un gemelo digital total, sino un prototipo
  reproducible de monitoreo dinámico.

---

## 1 · Portada

Buenos días. Agradezco al jurado y a mi director por su tiempo. Presento mi propuesta de
tesis de la Maestría en Geomática, titulada *Gemelo Digital basado en GeoAI para el
modelamiento dinámico de ecosistemas costeros*. En esta propuesta, el marco conceptual del Gemelo Digital se
desarrolla y evalúa tomando como caso de estudio la Ciénaga Grande de Santa Marta, con
énfasis en el monitoreo dinámico del manglar, su condición y la inundación asociada. El
título plantea un marco transferible; la aplicación empírica está delimitada a la CGSM.

## 2 · Context · Why it matters

La CGSM es un sistema estratégico del Caribe colombiano. Su importancia no está solo en la
extensión del manglar, sino en los servicios ecosistémicos que sostiene y en su historia
de degradación y recuperación. El problema de fondo es que hay datos satelitales
frecuentes, pero esa información no siempre se convierte en monitoreo espacialmente
explícito y útil para la gestión. Las estaciones son fundamentales, pero no capturan toda
la heterogeneidad espacial del sistema.

## 3 · Study area · Data readiness

Para evitar una propuesta abstracta, el área de estudio se delimitó desde el inicio. El
AOI corresponde a la CGSM sensu stricto, aproximadamente 1.286 kilómetros cuadrados.
Además, se revisó la disponibilidad de imágenes y capas de referencia en Google Earth
Engine para asegurar que la metodología sea viable desde la fase inicial. Las áreas
métricas se trabajarán en EPSG:9377, que corresponde al sistema oficial colombiano.

## 4 · Why this research (brechas)

La brecha no está en la ausencia de datos. La brecha está en la integración. Hay datos
ópticos, radar y referencias institucionales, pero falta una arquitectura que los organice
como datacube, evalúe modelos GeoAI y entregue productos reproducibles para monitoreo. La
oportunidad de esta investigación está en conectar esos componentes en un solo flujo
evaluable.

## 5 · Research question · Objectives

La pregunta se concentra en cómo integrar datos ópticos y radar dentro de un Gemelo Digital
basado en GeoAI para monitorear tres variables: extensión, condición e inundación. La
nubosidad persistente y la variabilidad hidroclimática justifican el uso de fusión
óptico-radar. Los tres objetivos responden directamente a esa pregunta: primero organizo
los datos, luego evalúo los modelos y finalmente integro los productos en un prototipo
reproducible.

## 6 · Verification checklist (coherencia)

Esta diapositiva responde a una preocupación típica del jurado: la coherencia interna. La
propuesta no presenta técnicas sueltas. Cada objetivo tiene una pregunta, un método, un
resultado y una forma de evaluación. El objetivo 1 produce la infraestructura de datos; el
objetivo 2 produce los mapas y la comparación de modelos; y el objetivo 3 integra esos
productos en un prototipo reproducible.

## 7 · Methodology · Operational framework

La metodología se organiza en tres capas. La primera es la capa de observación: sensores
ópticos, radar y datos de referencia. La segunda es la capa analítica: datacube, Random
Forest, modelos SAM-based y detección de inundación. La tercera es la capa operativa: flujo
automatizado, tablero y repositorio. La validación conecta las tres capas con el Global
Mangrove Watch, el INVEMAR y CARICOMP.

## 8 · Methods · Datacube + ruta priorizada

Sobre los métodos, priorizo una ruta concreta. Primero construyo un datacube listo para
análisis, con composiciones ópticas y SAR, índices espectrales y co-registro espacial. La
ruta principal de clasificación es Random Forest porque es interpretable, corre en Earth
Engine y funciona bien con datos heterogéneos. SamGeo y MW-SAM se evalúan como comparación,
para valorar el aporte del radar y de la segmentación, no como promesa de superioridad.

## 9 · Mapping & evaluation criteria

Cada producto tiene una métrica. Para clasificación no me quedo solo con exactitud global,
porque puede ocultar errores en clases difíciles. Por eso uso precisión, recall y F1 por
clase. Para segmentación uso IoU, y para variables continuas usaría RMSE y R cuadrado.
Kappa puede reportarse como métrica secundaria, pero no será la base de interpretación.

## 10 · Worked example · Rinconada

Este ejemplo evita que la metodología suene abstracta. Muestra el flujo completo: primero
se ingieren los datos, luego se clasifica la cobertura, después se detecta inundación según
el tipo de dosel y finalmente el prototipo muestra frecuencia de inundación por sector. El
producto no reemplaza una decisión institucional, pero sí genera una capa de apoyo para
priorizar monitoreo.

## 11 · Expected results · cronograma

Los resultados esperados se organizan por objetivo. El primero entrega el datacube; el
segundo, los mapas validados y el benchmark; el tercero, el prototipo interactivo y el
repositorio. El cronograma se distribuye en cuatro semestres: construcción del datacube,
experimentos de modelos, análisis de inundación y cambio, integración del prototipo y
escritura. La latencia objetivo y la capacidad computacional quedan documentadas como
referencia: el procesamiento se apoya en Earth Engine, con requerimientos limitados de
infraestructura local.

## 12 · Take-home messages / cierre

Cierro con tres ideas. Primero, el problema no es la ausencia de datos, sino su integración
operativa. Segundo, la metodología es evaluable porque cada producto tiene datos,
referencia y métrica. Tercero, la contribución es transferible como arquitectura, no como
un modelo que se copia sin recalibrar. Muchas gracias, quedo atenta a sus preguntas y
comentarios.

## 13 · Backup · Feasibility (solo si preguntan)

Esta diapositiva es de respaldo. El proyecto es viable porque se basa en datos abiertos,
Google Earth Engine, software abierto e infraestructura institucional. El presupuesto
operativo se concentra en apoyo técnico puntual, almacenamiento, validación o socialización
institucional y divulgación. No requiere compra de imágenes comerciales.

---

## Respuesta preparada si cuestionan el título

El título corresponde al marco metodológico general de la tesis: un Gemelo Digital basado
en GeoAI para el modelamiento dinámico de ecosistemas costeros. La aplicación empírica está
claramente delimitada en el subtítulo, la pregunta, los objetivos y la metodología: la
Ciénaga Grande de Santa Marta, con énfasis en manglar, condición del dosel e inundación.
Por eso no cambio el título oficial; lo acoto mediante el caso de estudio.
