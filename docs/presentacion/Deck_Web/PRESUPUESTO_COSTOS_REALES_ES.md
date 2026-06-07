# Costos reales en Colombia — Presupuesto Tabla 1 (formato FCA)

> Investigación de costos reales (junio 2026) por rubro, con fuentes. Las cifras
> son estimaciones de mercado; valídalas con cotizaciones y con la oficina
> financiera de la FCA. **Supuestos de cambio:** USD/COP ≈ 4.000–4.200 ·
> CHF/COP ≈ 4.800–4.900. **Unidad de la tabla:** miles de pesos (COP '000).

## Costos investigados por rubro

| Rubro | Costo real investigado | Fuente |
|---|---|---|
| **Impresos y Publicaciones** (APC) | Revista *Remote Sensing* (MDPI): **CHF 2.700 ≈ USD 3.000 ≈ COP 12,6–13,2 M**. Posible descuento si UNAL participa en el IOAP de MDPI. + impresión/empaste de tesis (tapa dura, Bogotá) ≈ COP 0,2–0,3 M. | MDPI APC |
| **Viáticos y Gastos de Viaje** | Escala nacional Decreto 613/2025 (interior, por asignación básica): **COP 162.510 a 360.077 / día**. Para estudiante/auxiliar aplica el tramo bajo ≈ **COP 162k–222k/día** (cubre alojamiento + comida + transporte local). Campaña de campo de ~5 días ≈ COP 0,9–1,1 M. Vuelos Bogotá–Santa Marta ida y vuelta ≈ **COP 0,35–0,45 M**. Total ~1 salida ≈ **COP 1,4–2,0 M**. | Decreto 613/2025 · vuelos BOG–SMR |
| **Servicios Técnicos** (software/cómputo) | GEE académico = gratis. Cómputo GPU para SAM: **Google Colab Pro+ USD 49,99/mes** (~COP 200k/mes) o Paperspace **A100 USD 3,18/h**. 6 meses de Colab Pro+ ≈ **COP 1,2–1,5 M**. | Colab pricing · Paperspace |
| **Equipos** | Portátil con GPU NVIDIA RTX 4060/4070 en Colombia (Ktronix / Alkosto / MercadoLibre): **≈ COP 4,5–8 M**. Si se usa equipo existente o solo componentes (RAM/SSD): **≈ COP 1 M**. Workstations de referencia global: USD 3.090–3.490. | Ktronix · Teknopolis · NVIDIA |
| **Materiales y Suministros** | SSD externo 2 TB ≈ **COP 0,4–0,7 M**; insumos de oficina menores. | MercadoLibre CO |
| **Personal** | Aporte **en especie** (no efectivo): dedicación de director/codirector valorada a hora-docente UNAL; indicativo ≈ COP 12–15 M en 24 meses. No se suma al total en efectivo. | — |
| **Patentes** | No aplica (COP 0). | — |

## Tabla 1 — escenario recomendado (open-infra · equipos en especie)

Coherente con "datos abiertos + infraestructura institucional". El gasto real lo
domina el APC.

| Rubros | Contrapartida UN | Cofinanciación | Total |
|---|---:|---:|---:|
| Personal | 0 \* | — | 0 \* |
| Servicios Técnicos (Colab Pro+ ~6 m) | 0 | 1.300 | 1.300 |
| Equipos (componentes / en especie) | 1.000 | 0 | 1.000 |
| Materiales y Suministros (SSD 2 TB) | 0 | 500 | 500 |
| Viáticos y Gastos de Viaje (1 campaña) | 800 | 1.200 | 2.000 |
| Impresos y Publicaciones (APC + empaste) | 0 | 12.900 | 12.900 |
| Patentes | 0 | 0 | 0 |
| **TOTAL** | **1.800** | **15.900** | **≈ 17.700** |

**≈ COP 17,7 M (~USD 4,2k).** \* Personal, plataforma GEE y equipo base = aporte
institucional en especie, no costeado.

## Tabla 1 — escenario B (compra de portátil GPU)

Si se adquiere un portátil RTX para inferencia local de SAM:

| Rubro | Total (miles) |
|---|---:|
| Equipos (portátil RTX 4060/4070) | 5.500 |
| Servicios Técnicos (cómputo) | 1.300 |
| Materiales (SSD 2 TB) | 500 |
| Viáticos (1 campaña) | 2.000 |
| Impresos y Publicaciones (APC + empaste) | 12.900 |
| **TOTAL** | **≈ 22.200** |

**≈ COP 22,2 M (~USD 5,3k).**

## Conclusión / reconciliación con el total de 15 M

- El **APC (~COP 12,6–13 M)** es el rubro dominante; por sí solo casi consume el
  presupuesto de 15 M.
- El presupuesto actual de **COP 15 M** es alcanzable **solo si** el cómputo usa
  niveles gratuitos (GEE + Colab free) y el equipo es en especie. Con costos
  reales (Colab Pro+ + SSD + 1 campaña completa) el total realista es
  **≈ COP 17–18 M**; con portátil GPU, **≈ COP 22 M**.
- Palancas para bajarlo: verificar **descuento IOAP de MDPI** para UNAL, o elegir
  una revista de APC menor / diamante (sin cargo); usar **Colab free / GEE** en
  vez de Pro+; y reportar equipo y cómputo como **contrapartida**.

## Fuentes

- Remote Sensing (MDPI) — APC: https://www.mdpi.com/journal/remotesensing/apc · https://www.mdpi.com/about/apc-2025
- Decreto 613 de 2025 (escala de viáticos, interior): https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=260138
- UNAL — Circular No. 16 GNFA, escala de viáticos 2025: https://gerencia.unal.edu.co/ (Normativa Interna)
- Vuelos Bogotá–Santa Marta: https://www.google.com/travel/flights · https://www.kayak.com.co/vuelos/Colombia-CO0/Santa-Marta-Simon-Bolivar-SMR
- Google Colab — precios: https://colab.research.google.com/signup · Paperspace: https://www.thundercompute.com/blog/colab-alternatives-for-cheap-deep-learning-in-2025
- Portátiles RTX en Colombia: https://www.ktronix.com/computadores-tablet/computadores-portatiles/portatiles-gaming/c/BI_0080_KTRON · https://www.teknopolis.co/blog/rtx-4060-colombia-vale-la-pena-2026/
- SSD 2 TB (MercadoLibre CO): https://listado.mercadolibre.com.co/ssd-externo-2tb
