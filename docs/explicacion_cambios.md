# Explicación de Cambios: Informe Original → Informe Mejorado

**Documento:** Pipeline Multilenguaje para el Monitoreo de Manglar en la CGSM (2013-2025)  
**Autora:** Lina María Quintero Fonseca  
**Fecha de revisión:** 23 de mayo de 2026

---

## Criterios generales de mejora aplicados

Antes de explicar cada sección, estos son los cuatro criterios que guiaron **todos** los cambios:

| Criterio | Descripción |
|---|---|
| **Redacción académica** | Eliminar frases ambiguas, redundancias y lenguaje coloquial |
| **Un verbo por objetivo** | Norma básica de escritura de objetivos en trabajos académicos |
| **Citas APA 7ma edición** | Formato autor-año en texto y lista de referencias completa y consistente |
| **Alcance explícito** | Todo informe académico debe declarar qué cubre y qué no cubre |

---

## Sección por sección

---

### 🔹 Título

| | Texto |
|---|---|
| **Original** | *(título no aparecía claramente estructurado como tal)* |
| **Mejorado** | *Pipeline Multilenguaje (Python, R, Julia) para el Monitoreo de Manglar en la Ciénaga Grande de Santa Marta (2013-2025)* |

**¿Por qué?**  
El título es lo primero que lee un evaluador. Debe contener: (1) el objeto de estudio, (2) el método principal, y (3) el período/área de análisis. Se hizo explícito el período temporal (2013-2025) y los lenguajes de programación, que son el aporte técnico central del trabajo.

---

### 🔹 Resumen Ejecutivo *(sección nueva)*

**¿Por qué se añadió?**  
El documento original no tenía resumen. En cualquier informe académico o técnico, el resumen es obligatorio porque:
- Permite al lector decidir si el documento es relevante antes de leerlo completo.
- Sintetiza objetivos, métodos, resultados y conclusiones en máximo 250 palabras.
- Es el estándar en maestrías, congresos y publicaciones científicas.

**Qué contiene el resumen añadido:**  
Área de estudio (835,3 km²), período (2013-2025), métodos principales (Random Forest, SamGeo, bfast, ERA5-Land), y resultados cuantitativos clave (F1-score 0,826; r = +0,807; quiebres en 2016, 2020, 2023-2024).

---

### 🔹 Sección 1 — Introducción y Justificación

| | Situación |
|---|---|
| **Original** | Texto con buena información pero con frases largas, sin conectores lógicos claros y algunas citas incompletas |
| **Mejorado** | Párrafos reorganizados con progresión lógica: contexto → problema → estado del arte → vacío → propuesta |

**Cambios específicos:**

1. **Estructura de párrafos:** Se reorganizó siguiendo el esquema clásico de introducción académica: *contexto general → problema específico → antecedentes → justificación del trabajo*.

2. **Conectores:** Se añadieron frases de transición ("En este marco...", "Sin embargo...", "No obstante...") para mejorar la cohesión entre ideas.

3. **Citas:** Se completaron las referencias incompletas. Por ejemplo, la cita a INVEMAR se formalizó como `(Instituto de Investigaciones Marinas y Costeras [INVEMAR], 2024)` según APA 7ma para instituciones con sigla.

4. **Precisión técnica:** Se especificó la resolución espacial de Sentinel-2 (10 m) y la cadencia temporal (5 días), datos que estaban implícitos en el original pero no declarados explícitamente.

---

### 🔹 Sección 2 — Objetivos

#### Objetivo General

| | Texto |
|---|---|
| **Original** | *"Desarrollar u pipeline GeoAI multilenguaje para el monitoreo de la dinámica espaciotemporal de la cobertura de manglar en la CGSM (2013-2025)."* |
| **Mejorado** | *"Desarrollar un pipeline de procesamiento multilenguaje (Python, R, Julia) para el monitoreo espaciotemporal de la cobertura de manglar en la Ciénaga Grande de Santa Marta durante el período 2013-2025."* |

**¿Por qué?**
- Se corrigió el error tipográfico (*"u pipeline"* → *"un pipeline"*).
- Se eliminó *"GeoAI"* del objetivo general porque es un término que requiere definición previa y puede confundir; queda mejor en el cuerpo del texto.
- Se explicitaron los lenguajes *(Python, R, Julia)* porque son el aporte diferencial del trabajo.
- **Se mantuvo un solo verbo:** *Desarrollar*.

#### Objetivos Específicos

| # | Original | Mejorado | Cambio realizado |
|---|---|---|---|
| OE1 | *Construir un datacube multitemporal de índices espectrales para la caracterización de la cobertura de manglar en la CGSM* | *Construir un datacube multitemporal de índices espectrales (NDVI, CMRI, EVI) a partir de imágenes Landsat 8/9, Sentinel-2 y Sentinel-1 SAR para la caracterización de la cobertura de manglar en la CGSM.* | Se especificaron los índices y las fuentes de datos, que ya estaban en el cuerpo del trabajo. Verbo: **Construir** ✅ |
| OE2 | *Identificar los períodos de degradación/recuperación del manglar mediante análisis de anomalías temporales* | *Identificar los períodos de degradación y recuperación del manglar mediante el análisis de anomalías y quiebres estructurales en las series temporales (2013-2025).* | Se añadió "quiebres estructurales" (método bfast que ya se usa) y el período explícito. Verbo: **Identificar** ✅ |
| OE3 | *Validar la segmentación automática de cobertura de manglar contra cartografía de referencia* | *Validar la segmentación automática de cobertura de manglar (SamGeo) contra la cartografía de referencia INVEMAR 1:25.000.* | Se especificó la herramienta (SamGeo) y la escala de la cartografía (1:25.000), que ya aparecían en el cuerpo. Verbo: **Validar** ✅ |

**Regla aplicada en todos los objetivos:** Un solo verbo en infinitivo por objetivo. Los verbos *diseñar, implementar, validar* juntos en un mismo objetivo (como estaban en la versión anterior del mejorado) son incorrectos porque mezclan tres acciones distintas que el lector no puede evaluar por separado.

---

### 🔹 Sección 3 — Alcance, Delimitaciones y Limitaciones *(sección nueva)*

**¿Por qué se añadió?**  
El documento original no tenía una sección de alcance. Esto es un problema académico porque:

- Sin alcance, el lector no sabe qué queda **dentro** y qué queda **fuera** del trabajo.
- Los evaluadores esperan encontrar delimitaciones explícitas (espaciales, temporales, temáticas).
- Las limitaciones permiten contextualizar los resultados y protegen al autor de críticas por lo que no se hizo.

**Contenido añadido:**

| Subsección | Qué declara |
|---|---|
| **3.1 Alcance** | Qué hace el trabajo: área (835,3 km²), período (2013-2025), técnicas incluidas |
| **3.2 Delimitaciones** | Qué NO hace el trabajo: no incluye validación de campo, no cubre toda Colombia, no modela proyecciones futuras |
| **3.3 Limitaciones** | Restricciones externas: nubosidad persistente, resolución temporal de datos, acceso a datos IDEAM |

---

### 🔹 Sección 4 — Marco Teórico y Estado del Arte

| | Situación |
|---|---|
| **Original** | Sección llamada *"Estado del Arte"* con subsecciones temáticas bien definidas pero citas en formato inconsistente |
| **Mejorado** | Renombrada a *"Marco Teórico y Estado del Arte"* con citas estandarizadas APA 7ma |

**Cambios específicos:**

1. **Nombre de la sección:** Se añadió *"Marco Teórico"* porque el documento incluye definiciones conceptuales (teledetección, aprendizaje automático, modelos de fundación) que van más allá del estado del arte puro.

2. **Subsección 2.1 del original** (*"Teledetección óptica y radar en ecosistemas de manglar"*) no tenía número en el original. Se numeró correctamente como 4.1.

3. **Citas corregidas:** Ejemplos de correcciones aplicadas:
   - `Giri et al., 2011` → `(Giri et al., 2011)` con año y DOI en referencias.
   - `Hamilton & Casey, 2016` → formato APA con `&` en paréntesis y `and` en texto corrido.
   - Referencias a SamGeo: `Wu & Osco, 2023` añadida con DOI completo.

---

### 🔹 Sección 6 — Metodología

| | Situación |
|---|---|
| **Original** | Llamada *"Metodología y código"*, organizada por fases (Fase 1, Fase 2...) con mezcla de texto explicativo y bloques de código extensos |
| **Mejorado** | Reorganizada por componentes lógicos del pipeline, con subsecciones de cuarto nivel para mayor granularidad |

**Cambios específicos:**

1. **Nombre:** Se eliminó *"y código"* del título porque el código pertenece a los Anexos, no a la metodología. La metodología describe *qué se hizo y por qué*, no *cómo se programó*.

2. **Reorganización:** Las "Fases" del original eran útiles para mostrar secuencia, pero mezclaban procesos de naturaleza distinta. La versión mejorada separa claramente:
   - Adquisición de datos (6.2)
   - Clasificación (6.3)
   - Segmentación (6.4)
   - Series temporales (6.5)
   - Forzamiento climático (6.6)
   - Alertas tempranas (6.7)

3. **Subsecciones de cuarto nivel:** Se añadieron para que el lector pueda ubicar exactamente dónde se describe cada paso (ej. 6.3.2 Entrenamiento del clasificador, 6.5.3 Detección de quiebres con bfast).

4. **Bloques de código:** Se movieron a los Anexos C y D. En la metodología se describen los algoritmos en prosa académica, no en código.

---

### 🔹 Sección 7 — Resultados

| | Situación |
|---|---|
| **Original** | Llamada *"Resultados y discusión"* mezclando ambas partes en una sola sección con 18 subsecciones |
| **Mejorado** | Separada en Sección 7 (Resultados) y Sección 8 (Discusión) |

**¿Por qué se separaron?**  
En escritura académica formal, resultados y discusión son secciones distintas:
- **Resultados:** Describe *qué se encontró* (datos, métricas, tablas, figuras) sin interpretación.
- **Discusión:** Interpreta *qué significan* los resultados, los compara con la literatura y explica las implicaciones.

Mezclarlos dificulta la evaluación y no sigue el estándar IMRaD (Introducción, Métodos, Resultados, Discusión) requerido en maestrías.

**Consolidación de subsecciones:** Las 18 subsecciones originales se consolidaron en 5 temáticas claras:
- 7.1 Clasificación de cobertura y validación
- 7.2 Segmentación y análisis espacial
- 7.3 Series temporales y detección de cambios
- 7.4 Correlación SAR-Óptico
- 7.5 Alertas tempranas

---

### 🔹 Sección 8 — Discusión *(sección nueva/separada)*

**¿Por qué?**  
Ver explicación en Sección 7. Se creó como sección independiente para interpretar los resultados, compararlos con la literatura citada en el marco teórico, y discutir las implicaciones para la gestión del ecosistema.

---

### 🔹 Sección 9 — Conclusiones

| | Situación |
|---|---|
| **Original** | Conclusiones presentes pero redactadas como lista de hallazgos técnicos sin conexión explícita con los objetivos |
| **Mejorado** | Cada conclusión responde directamente a uno de los tres objetivos específicos |

**¿Por qué?**  
Las conclusiones de un trabajo académico deben cerrar el ciclo con los objetivos. La regla es: *si tienes 3 objetivos específicos, debes tener al menos 3 conclusiones, una por objetivo*. Esto permite al evaluador verificar que el trabajo cumplió lo que prometió.

---

### 🔹 Sección 10 — Recomendaciones y Trabajo Futuro *(sección nueva)*

**¿Por qué se añadió?**  
El documento original terminaba en conclusiones. En trabajos de maestría es estándar incluir recomendaciones porque:
- Demuestra visión crítica del propio trabajo.
- Abre líneas de investigación futura.
- Muestra madurez académica al reconocer lo que queda pendiente.

---

### 🔹 Sección 11 — Referencias

| | Situación |
|---|---|
| **Original** | Lista de referencias presente pero con formato inconsistente (algunas en APA, otras sin año, otras sin DOI) |
| **Mejorado** | Todas estandarizadas a APA 7ma edición con DOI cuando disponible |

**Correcciones específicas aplicadas:**

| Problema encontrado | Corrección aplicada |
|---|---|
| Citas sin año de publicación | Se añadió el año entre paréntesis |
| Autores institucionales sin sigla | Se añadió la sigla entre corchetes en la primera mención: `[INVEMAR]` |
| DOIs faltantes | Se añadieron los DOIs disponibles (ej. GBIF: `10.15472/0fqdp4`) |
| Inconsistencia `&` vs `y` | APA 7ma: `&` dentro de paréntesis, `and`/`y` en texto corrido |
| Referencias de software sin versión | Se añadió versión y URL del repositorio (ej. SamGeo, GEE) |

---

### 🔹 Anexos

| | Situación |
|---|---|
| **Original** | 5 anexos (A-E) con código extenso mezclado con explicaciones metodológicas |
| **Mejorado** | 4 anexos reorganizados: A (especificaciones técnicas), B (estructura del repositorio), C (código RF), D (código R bfast) |

**¿Por qué se reorganizaron?**  
El código que estaba en la metodología (Secciones 6.x del original) se movió a los Anexos. Los Anexos son el lugar correcto para el código fuente; la metodología debe describir el proceso en lenguaje académico, no mostrar implementaciones.

---

## Resumen de cambios por tipo

| Tipo de cambio | Secciones afectadas | Razón principal |
|---|---|---|
| **Corrección de redacción** | 1, 2, 4, 6, 9 | Fluidez, precisión y tono académico |
| **Un verbo por objetivo** | 2 (OG y OE1-OE3) | Norma de escritura académica de objetivos |
| **Estandarización de citas APA 7ma** | 1, 4, 11 | Consistencia y trazabilidad de fuentes |
| **Sección nueva añadida** | 3 (Alcance), 8 (Discusión), 10 (Recomendaciones), Resumen | Estructura académica completa (IMRaD) |
| **Reorganización estructural** | 6 (Metodología), 7 (Resultados), Anexos | Separar descripción de implementación |

---

*Documento generado el 23 de mayo de 2026 como parte del proceso de mejora del informe final.*
