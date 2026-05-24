# ===========================================================================
# Script 05 — Cubo stars desde TIFs Sentinel-2 + extracción por estación
# ===========================================================================
#
# Aplica el patrón del Cap. 21 del curso (Cubos Multidimensionales Vector y
# Raster) para construir un cubo (x, y, time) a partir de los composites
# trimestrales Sentinel-2 ya descargados de GEE, y extraer la serie temporal
# de NDVI sobre las 8 estaciones de muestreo INVEMAR.
#
# Funciona como validación cruzada multilingüe del flujo Python+GEE de la
# Fase 2: si los valores extraídos por stars coinciden con los obtenidos vía
# reduceRegions en GEE, la robustez de la serie temporal queda confirmada.
#
# Insumo:    data/processed/s2/*.tif (composites trimestrales NDVI)
# Salida:    outputs/tables/series_temporales_stars.csv
#
# Lina María Quintero Fonseca — Maestría en Geomática, UNAL (2026-1)
# ===========================================================================

suppressPackageStartupMessages({
  library(stars)
  library(sf)
  library(dplyr)
  library(tidyr)
  library(readr)
  library(stringr)
})

# ---------------------------------------------------------------------------
# 1. Rutas y constantes
# ---------------------------------------------------------------------------

# Ejecutar desde la raíz del proyecto (../ desde src/R/)
ROOT       <- normalizePath(file.path(dirname(rstudioapi::getActiveDocumentContext()$path), "..", ".."))
if (is.na(ROOT) || ROOT == "") ROOT <- normalizePath("../..")
S2_DIR     <- file.path(ROOT, "data", "processed", "s2")
OUT_TABLES <- file.path(ROOT, "outputs", "tables")
dir.create(OUT_TABLES, recursive = TRUE, showWarnings = FALSE)

EPSG_GEO  <- 4326
EPSG_NAC  <- 9377

# ---------------------------------------------------------------------------
# 2. Estaciones de muestreo (5 INVEMAR + 3 complementarias)
# ---------------------------------------------------------------------------

estaciones <- data.frame(
  estacion = c("Isla_Boqueron", "Punta_Cerro", "Punta_Chino", "Rio_Sevilla",
               "Cano_Palos",    "CP_Luna",     "CP_Aguas_Negras", "Cano_Clarin"),
  fuente   = c(rep("INVEMAR", 5), rep("Complementaria", 3)),
  lon      = c(-74.298457, -74.283206, -74.304827, -74.325228,
               -74.471258, -74.56,     -74.57,     -74.50),
  lat      = c( 10.962255,  10.973076,  10.912032,  10.880496,
                10.757558,  10.87,      10.80,      10.60)
)

estaciones_sf <- st_as_sf(estaciones, coords = c("lon", "lat"), crs = EPSG_GEO)
cat("Estaciones cargadas:", nrow(estaciones_sf), "\n")

# ---------------------------------------------------------------------------
# 3. Listar y ordenar los composites trimestrales (Cap. 21)
# ---------------------------------------------------------------------------

# Convención de nombre esperada: cgsm_s2_NDVI_2018_Q1.tif, ..._2025_Q4.tif
tifs <- list.files(S2_DIR, pattern = "NDVI.*\\.tif$", full.names = TRUE)
if (length(tifs) == 0) {
  stop(sprintf(paste0(
    "No se encontraron TIFs de NDVI en %s\n",
    "Asegúrate de haber descargado los composites desde Drive ",
    "(carpeta CGSM_data) a esa ruta."), S2_DIR))
}

# Extraer fecha aproximada del nombre del archivo (año + trimestre)
fechas <- sapply(basename(tifs), function(n) {
  m <- str_match(n, "(\\d{4})[_-]?Q(\\d)")
  if (any(is.na(m))) return(NA_character_)
  anio <- as.integer(m[, 2]); trim <- as.integer(m[, 3])
  mes  <- (trim - 1) * 3 + 2  # mes central del trimestre
  sprintf("%04d-%02d-15", anio, mes)
})
ord <- order(as.Date(fechas))
tifs   <- tifs[ord]
fechas <- as.Date(fechas[ord])
cat("Composites encontrados:", length(tifs), "\n")
cat("Rango temporal:", as.character(min(fechas)), "→", as.character(max(fechas)), "\n")

# ---------------------------------------------------------------------------
# 4. Construir el cubo stars (x, y, time)
# ---------------------------------------------------------------------------

cat("\n--- Construyendo cubo stars (puede tardar varios minutos) ---\n")
cubo <- read_stars(tifs, along = list(time = fechas), proxy = TRUE)
cat("Cubo:\n"); print(cubo)

# ---------------------------------------------------------------------------
# 5. Extracción sobre las estaciones (st_extract — Cap. 21 sección 21.4)
# ---------------------------------------------------------------------------

# Garantizar coherencia de CRS antes del extract
estaciones_match <- st_transform(estaciones_sf, st_crs(cubo))

cat("\n--- Extrayendo series temporales sobre estaciones ---\n")
serie <- st_extract(cubo, estaciones_match)
serie_df <- as.data.frame(serie)

# Pivot a formato largo: una fila por (estacion, fecha)
serie_long <- serie_df %>%
  mutate(estacion = estaciones$estacion,
         fuente   = estaciones$fuente) %>%
  pivot_longer(cols = -c(estacion, fuente, geometry),
               names_to = "fecha", values_to = "ndvi") %>%
  mutate(fecha = as.Date(fecha))

# Limpiar geometría para CSV
serie_long$geometry <- NULL

# ---------------------------------------------------------------------------
# 6. Exportar
# ---------------------------------------------------------------------------

out_csv <- file.path(OUT_TABLES, "series_temporales_stars.csv")
write_csv(serie_long, out_csv)
cat(sprintf("\nGuardado: %s (%d filas)\n", out_csv, nrow(serie_long)))

# Diagnóstico breve
cat("\nResumen por estación (NDVI medio, n observaciones):\n")
print(serie_long %>% group_by(estacion) %>%
        summarise(n = n(),
                  ndvi_medio = round(mean(ndvi, na.rm = TRUE), 3),
                  ndvi_min   = round(min(ndvi, na.rm = TRUE), 3),
                  ndvi_max   = round(max(ndvi, na.rm = TRUE), 3)))

cat("\n*** FASE STARS COMPLETA ***\n")
