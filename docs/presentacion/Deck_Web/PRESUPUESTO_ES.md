# Presupuesto de la propuesta — Tabla 1 (formato FCA)

> Cifras con **costos reales de Colombia** (junio 2026). Validar con cotizaciones
> y con la oficina financiera de la FCA. El detalle de la investigación de costos
> y las fuentes está en `PRESUPUESTO_COSTOS_REALES_ES.md`. Narrativa: el proyecto
> es **viable con datos abiertos e infraestructura institucional**; el personal y
> la plataforma GEE se aportan **en especie** (no se monetizan) y el efectivo lo
> domina el cargo de publicación (APC).

**Código:** B.FCA.FT.05.007.005 · **Unidad:** miles de pesos (COP '000)
*(un valor de `12.900` = COP 12.900.000) · USD/COP ≈ 4.200*

## Tabla 1. Presupuesto global de la propuesta por fuentes de financiación (en miles de $)

| Rubros | Contrapartida UN | Cofinanciación | Total |
|---|---:|---:|---:|
| Personal | 0 \* | — | 0 \* |
| Servicios Técnicos (cómputo · Colab Pro+ ~6 m) | 0 | 1.300 | 1.300 |
| Equipos (componentes / en especie) | 1.000 | 0 | 1.000 |
| Materiales y Suministros (SSD 2 TB) | 0 | 500 | 500 |
| Viáticos y Gastos de Viaje (1 campaña) | 800 | 1.200 | 2.000 |
| Impresos y Publicaciones (APC + empaste) | 0 | 12.900 | 12.900 |
| Patentes | 0 | 0 | 0 |
| **TOTAL** | **1.800** | **15.900** | **17.700** |

- **Total = COP 17.700.000 (~USD 4.200).**
- **Publicación (APC):** *Remote Sensing* (MDPI) CHF 2.700 ≈ **USD 3.000 ≈ COP 12,6–13 M** + impresión/empaste ≈ COP 0,3 M. Posible **descuento IOAP** si UNAL participa.
- **\* En especie (no monetizado):** dedicación del equipo académico (Personal) y la **plataforma Google Earth Engine**.
- La celda de Cofinanciación en **Personal** va sombreada / "no aplica" (formato UN).

## Justificación por rubro (costos reales)

- **Personal (en especie):** dedicación de director, codirector e investigadora en formación, 24 meses, valorada a hora-docente UNAL.
- **Servicios Técnicos — cómputo (1.300):** GEE académico gratis; GPU para SAM vía **Google Colab Pro+ USD 49,99/mes** (~COP 200k/mes), ~6 meses.
- **Equipos (1.000):** componentes (RAM/SSD) o uso de equipo institucional. *(Un portátil RTX 4060/4070 en Colombia cuesta ≈ COP 4,5–8 M; ver escenario B en el doc de costos.)*
- **Materiales y Suministros (500):** SSD externo 2 TB (≈ COP 0,4–0,7 M) e insumos.
- **Viáticos y Gastos de Viaje (2.000):** escala Decreto 613/2025 (interior, tramo bajo ≈ COP 162k–222k/día) × ~5 días + vuelo Bogotá–Santa Marta ida/vuelta (≈ COP 0,35–0,45 M).
- **Impresos y Publicaciones (12.900):** APC en revista indexada de acceso abierto + empaste/impresión de la tesis.
- **Patentes (0):** no se contemplan.

## Supuestos clave (sustento de viabilidad)

1. **Datos** (Sentinel-1/2, Landsat, ALOS-2, GMW, INVEMAR/CARICOMP) **abiertos** → costo = 0.
2. **Cómputo principal:** Google Earth Engine (académico, gratuito).
3. **Software base** (SNAP, QGIS, Python/R/Julia, Docker) de **código abierto**.
4. El efectivo lo domina el **APC**; palancas de ahorro: descuento IOAP de MDPI o
   revista de acceso abierto diamante (APC = 0), y usar Colab/GEE gratis.
