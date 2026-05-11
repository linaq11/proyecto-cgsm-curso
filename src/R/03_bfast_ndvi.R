library(tidyverse)
library(bfast)
library(tseries)

df <- read.csv("../../outputs/tables/serie_temporal_ndvi_definitiva.csv")
cat("Registros cargados:", nrow(df), "\n")

estaciones <- unique(df$estacion)
resultados_bfast <- list()

for (est in estaciones) {
  cat("=== Procesando:", est, "===\n")
  sub <- df %>% filter(estacion == est) %>% arrange(fecha) %>% filter(!is.na(NDVI))
  if (nrow(sub) < 24) { cat("  Insuficientes datos\n\n"); next }
  ts_ndvi <- ts(sub$NDVI, start = c(as.integer(format(as.Date(sub$fecha[1]), "%Y")), as.integer(format(as.Date(sub$fecha[1]), "%m"))), frequency = 12)
  tryCatch({
    bf <- bfast(ts_ndvi, h = 0.15, season = "harmonic", max.iter = 10)
    n_bt <- length(bf$output[[1]]$bp.Vt$breakpoints)
    n_bs <- length(bf$output[[1]]$bp.Wt$breakpoints)
    cat("  Quiebres tendencia:", n_bt, "| estacionalidad:", n_bs, "\n")
    resultados_bfast[[est]] <- data.frame(estacion=est, quiebres_tendencia=n_bt, quiebres_estacionalidad=n_bs)
    png(paste0("../../outputs/figures/bfast_", gsub(" ","_",est), ".png"), width=1200, height=800, res=150)
    plot(bf, main=paste("BFAST -", est)); dev.off()
    cat("  Grafico guardado\n\n")
  }, error=function(e) cat("  Error:", e$message, "\n\n"))
}

if (length(resultados_bfast) > 0) {
  resumen <- do.call(rbind, resultados_bfast)
  write.csv(resumen, "../../outputs/tables/bfast_resumen.csv", row.names=FALSE)
  cat("\n=== RESUMEN ===\n"); print(resumen)
}
cat("\n*** FASE 2 R COMPLETA ***\n")
