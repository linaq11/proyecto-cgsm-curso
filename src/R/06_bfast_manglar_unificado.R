# =============================================================
# 06_bfast_manglar_unificado.R
# bfast solo sobre las 4 estaciones de manglar (excluye limnológicas)
# =============================================================
# Re-ejecuta el análisis bfast del notebook 02b_bfast_ndvi.R restringiéndolo
# a las 4 estaciones que efectivamente miden cobertura de manglar denso
# ---Caño Palos, Caño Clarín, CP Aguas Negras y CP Luna--- y excluye las
# 4 estaciones limnológicas ---Isla Boquerón, Punta Cerro, Punta Chino y
# Río Sevilla--- que están sobre la lámina de agua del complejo lagunar.
# El propósito es eliminar el ruido espectral de las estaciones que
# monitorean agua y refinar la detección de quiebres asociados a eventos
# ENSO sobre el dosel del manglar.
# =============================================================

library(bfast)
library(dplyr)
library(tidyr)
library(readr)
library(ggplot2)

setwd("/home/rstudio/work/proyecto-cgsm")
csv_in   <- "outputs/tables/serie_temporal_ndvi_definitiva.csv"
out_csv  <- "outputs/tables/bfast_manglar_unificado.csv"
out_fig  <- "outputs/figures"
dir.create(out_fig, showWarnings = FALSE, recursive = TRUE)

# ---- Las 4 estaciones de manglar (excluye limnológicas) ----
manglar_4 <- c("Cano_Palos", "Cano_Clarin", "CP_Aguas_Negras", "CP_Luna")

df <- read_csv(csv_in, show_col_types = FALSE)
cat("Estaciones disponibles:\n")
print(table(df$subzona))

df_man <- df %>%
  filter(subzona %in% manglar_4) %>%
  mutate(date = as.Date(date)) %>%
  arrange(subzona, date)

cat("\nEstaciones de manglar seleccionadas:\n")
print(table(df_man$subzona))

# ---- Aplicar bfast con h=0.15 y h=0.10 a cada estación ----
resultados <- list()

for (est in manglar_4) {
  cat("\n=== ", est, " ===\n", sep = "")
  serie <- df_man %>% filter(subzona == est)

  if (nrow(serie) < 36) {
    cat("  Insuficientes observaciones (", nrow(serie), "), salto.\n", sep = "")
    next
  }

  # Convertir a ts mensual; rellenar con NA donde falte mes
  fechas_mes <- seq(min(serie$date), max(serie$date), by = "month")
  serie_mes  <- data.frame(date = fechas_mes) %>%
    left_join(serie %>% select(date, ndvi), by = "date")

  ts_obj <- ts(serie_mes$ndvi,
               start = c(as.integer(format(min(fechas_mes), "%Y")),
                         as.integer(format(min(fechas_mes), "%m"))),
               frequency = 12)

  # Interpolar NA si los hay
  if (any(is.na(ts_obj))) ts_obj <- zoo::na.approx(ts_obj, rule = 2)

  for (h_val in c(0.15, 0.10)) {
    tryCatch({
      fit <- bfast(ts_obj, h = h_val, season = "harmonic", max.iter = 5)
      n_brks <- length(fit$output[[1]]$Vt.bp)
      if (n_brks > 0 && !is.na(fit$output[[1]]$Vt.bp[1])) {
        fechas_brks <- time(ts_obj)[fit$output[[1]]$Vt.bp]
        fechas_brks_str <- paste(round(fechas_brks, 2), collapse = "; ")
      } else {
        n_brks <- 0
        fechas_brks_str <- ""
      }
      resultados[[length(resultados) + 1]] <- data.frame(
        estacion = est,
        h = h_val,
        n_quiebres = n_brks,
        fechas_quiebres = fechas_brks_str,
        n_obs = length(ts_obj),
        rango = paste(min(fechas_mes), max(fechas_mes), sep = " a ")
      )
      cat("  h = ", h_val, ": ", n_brks, " quiebres ", fechas_brks_str, "\n", sep = "")

      # Guardar gráfico
      png(file.path(out_fig, sprintf("bfast_manglar_unif_%s_h%02d.png", est, h_val * 100)),
          width = 1000, height = 700)
      plot(fit, main = sprintf("%s — bfast h=%.2f", est, h_val))
      dev.off()
    }, error = function(e) {
      cat("  h = ", h_val, ": ERROR — ", e$message, "\n", sep = "")
      resultados[[length(resultados) + 1]] <- data.frame(
        estacion = est, h = h_val, n_quiebres = NA,
        fechas_quiebres = paste("error:", e$message),
        n_obs = length(ts_obj),
        rango = paste(min(fechas_mes), max(fechas_mes), sep = " a ")
      )
    })
  }
}

# ---- Consolidar y exportar ----
df_res <- bind_rows(resultados)
write_csv(df_res, out_csv)

cat("\n=== RESUMEN bfast 4 estaciones manglar (unificadas) ===\n")
print(df_res)
cat("\nGuardado: ", out_csv, "\n", sep = "")
cat("Gráficos PNG: ", out_fig, "/bfast_manglar_unif_*.png\n", sep = "")
