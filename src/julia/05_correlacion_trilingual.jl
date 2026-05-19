#!/usr/bin/env julia
# =============================================================
# 05_correlacion_trilingual.jl
# Componente Julia del notebook 14 — validación cruzada trilingüe
# =============================================================
# Calcula la correlación de Pearson entre la anomalía z-score del caudal
# medio mensual del río Magdalena en El Banco y la anomalía NDVI z-score
# promediada sobre las cuatro estaciones de manglar, con rezagos de 0 a 3
# meses. Resultado a stdout en formato CSV simple parseable desde Python.
# =============================================================

using CSV, DataFrames, Statistics, Dates

cd("/home/rstudio/work/proyecto-cgsm")

# --- Caudal El Banco con z-score por mes ---
caudal_raw = CSV.read("data/raw/ideam/descargaDhime_elbanco_medio.csv", DataFrame)
caudal_raw.date = Date.(string.(SubString.(string.(caudal_raw.Fecha), 1, 10))) .+ Day(14)
caudal_raw.caudal = parse.(Float64, string.(caudal_raw.Valor))
caudal_raw.mes = month.(caudal_raw.date)

caudal = combine(groupby(caudal_raw, :mes)) do sub
    transform(sub, :caudal => (x -> (x .- mean(x)) ./ std(x)) => :caudal_z)
end
caudal = sort(select(caudal, :date, :caudal_z), :date)

# --- NDVI promedio sobre manglar, z-score por estación, mensual ---
manglar = Set(["Cano_Palos", "Cano_Clarin", "CP_Aguas_Negras", "CP_Luna"])
ndvi_raw = CSV.read("outputs/tables/serie_temporal_ndvi_definitiva.csv", DataFrame)
ndvi_raw = filter(:subzona => in(manglar), ndvi_raw)
ndvi_raw.date = Date.(string.(SubString.(string.(ndvi_raw.date), 1, 10)))

ndvi_z = combine(groupby(ndvi_raw, :subzona)) do sub
    transform(sub, :ndvi => (x -> (x .- mean(skipmissing(x))) ./ std(skipmissing(x))) => :z)
end

# Promediar sobre el mes
ndvi_z.date_m = Date.(year.(ndvi_z.date), month.(ndvi_z.date), 15)
ndvi_mensual = combine(groupby(ndvi_z, :date_m), :z => (x -> mean(skipmissing(x))) => :z)
rename!(ndvi_mensual, :date_m => :date)
sort!(ndvi_mensual, :date)

# --- Merge y correlación con rezago ---
merged = innerjoin(ndvi_mensual, caudal, on = :date)
sort!(merged, :date)

println("lenguaje,rezago_meses,rho_caudal,n")
for lag in 0:3
    n = nrow(merged)
    if lag == 0
        x = merged.z
        y = merged.caudal_z
    else
        x = merged.z[(lag+1):end]
        y = merged.caudal_z[1:(end-lag)]
    end
    validos = .!ismissing.(x) .& .!ismissing.(y) .& .!isnan.(x) .& .!isnan.(y)
    rho = cor(collect(skipmissing(x[validos])), collect(skipmissing(y[validos])))
    println("Julia,$lag,$(round(rho, digits=4)),$(sum(validos))")
end
