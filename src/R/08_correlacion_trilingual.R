# =============================================================
# 08_correlacion_trilingual.R
# Componente R del notebook 14 — validación cruzada trilingüe
# =============================================================
# Calcula la correlación de Pearson entre la anomalía z-score del caudal
# medio mensual del río Magdalena en El Banco y la anomalía NDVI z-score
# promediada sobre las cuatro estaciones de manglar, con rezagos de 0 a 3
# meses. Resultado a stdout en formato CSV simple parseable desde Python.
# =============================================================

suppressPackageStartupMessages({
  library(dplyr)
  library(lubridate)
  library(readr)
})

setwd('/home/rstudio/work/proyecto-cgsm')

caudal <- read_csv('data/raw/ideam/descargaDhime_elbanco_medio.csv',
                   show_col_types = FALSE) %>%
  mutate(date = as.Date(Fecha) + days(14),
         caudal = as.numeric(Valor)) %>%
  filter(!is.na(caudal)) %>%
  group_by(mes = month(date)) %>%
  mutate(caudal_z = (caudal - mean(caudal)) / sd(caudal)) %>%
  ungroup() %>%
  select(date, caudal_z)

manglar <- c('Cano_Palos', 'Cano_Clarin', 'CP_Aguas_Negras', 'CP_Luna')

ndvi <- read_csv('outputs/tables/serie_temporal_ndvi_definitiva.csv',
                 show_col_types = FALSE) %>%
  filter(subzona %in% manglar) %>%
  group_by(subzona) %>%
  mutate(z = (ndvi - mean(ndvi, na.rm = TRUE)) / sd(ndvi, na.rm = TRUE)) %>%
  ungroup() %>%
  mutate(date = floor_date(as.Date(date), 'month') + days(14)) %>%
  group_by(date) %>%
  summarise(z = mean(z, na.rm = TRUE), .groups = 'drop')

merged <- inner_join(ndvi, caudal, by = 'date') %>% arrange(date)

cat('lenguaje,rezago_meses,rho_caudal,n\n')
for (lag in 0:3) {
  caudal_lag <- dplyr::lag(merged$caudal_z, lag)
  validos <- !is.na(caudal_lag) & !is.na(merged$z)
  rho <- cor(merged$z[validos], caudal_lag[validos])
  cat(sprintf('R,%d,%.4f,%d\n', lag, rho, sum(validos)))
}
