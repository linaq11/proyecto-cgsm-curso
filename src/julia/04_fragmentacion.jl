"""
Fase 4 — Metricas de fragmentacion del paisaje de manglar
=========================================================

Calcula numero de parches, area total, area media y maxima, densidad de parches
por 1.000 ha, e indice de forma medio (MSI = perimetro / sqrt(pi x area)) sobre
los polígonos vectorizados por SamGeo.

Se mantiene el bloque legado con aproximación esférica (compatibilidad con
analisis previos) y se agrega un bloque nuevo que opera sobre los GeoJSON
reproyectados al sistema oficial colombiano EPSG:9377 (MAGNA-SIRGAS Origen
Nacional), siguiendo la receta de la **Tarea 19**. En 9377 las coordenadas
estan en metros y el shoelace devuelve area en m² sin aproximaciones.

Lina Maria Quintero Fonseca — Maestria en Geomatica, UNAL (2026-1)
"""

using DataFrames, CSV, GeoJSON, Statistics

println("=== Fase 4: Metricas de fragmentacion ===\n")

periodos = ["degradacion", "recuperacion", "actual"]
samgeo_dir = "../../data/processed/samgeo"

# ----------------------------------------------------------------------------
# Funciones auxiliares
# ----------------------------------------------------------------------------

"""Shoelace genérico. Devuelve (area, perimetro) en las unidades de las coords."""
function shoelace(ring)
    nr = length(ring)
    area = 0.0; perim = 0.0
    for i in 1:(nr-1)
        x1, y1 = ring[i][1], ring[i][2]
        x2, y2 = ring[i+1][1], ring[i+1][2]
        area  += x1 * y2 - x2 * y1
        perim += sqrt((x2 - x1)^2 + (y2 - y1)^2)
    end
    return abs(area) / 2.0, perim
end

"""Procesa un FeatureCollection y devuelve (areas_ha, perim_m) tras aplicar
filtro de tamaño 1 ≤ area_ha < 5000."""
function metricas_geojson(geojson_path::String; en_metros::Bool)
    fc = GeoJSON.read(read(geojson_path, String))
    areas_ha, perim_m = Float64[], Float64[]
    for feat in fc.features
        geom = feat.geometry
        (geom isa GeoJSON.Polygon && length(geom.coordinates) > 0) || continue
        ring = geom.coordinates[1]
        length(ring) >= 4 || continue
        a, per = shoelace(ring)
        if en_metros
            area_ha = a / 10_000.0
            per_metros = per
        else
            # Aproximación esférica para coords en grados (lat ≈ 10.7°)
            factor = 111_000.0 * cos(deg2rad(10.7)) * 111_000.0
            area_ha = a * factor / 10_000.0
            per_metros = per * 111_000.0
        end
        if 1.0 <= area_ha < 5000.0
            push!(areas_ha, area_ha); push!(perim_m, per_metros)
        end
    end
    return areas_ha, perim_m
end

"""Construye una fila de la tabla resumen."""
function fila_resumen(periodo, areas_ha, perim_m)
    n = length(areas_ha)
    n == 0 && return nothing
    msi = mean([perim_m[i] / sqrt(pi * areas_ha[i] * 10_000) for i in 1:n])
    densidad = n / (sum(areas_ha) / 1000)
    return (periodo, n, sum(areas_ha), mean(areas_ha),
            maximum(areas_ha), densidad, msi)
end

# ----------------------------------------------------------------------------
# Bloque 1 (legado): aproximacion esferica sobre EPSG:4326
# ----------------------------------------------------------------------------

println("--- Bloque 1: aproximación esférica (EPSG:4326, legado) ---")
res_legado = DataFrame(
    periodo=String[], num_parches=Int[], area_total_ha=Float64[],
    area_media_ha=Float64[], area_max_ha=Float64[],
    densidad_parches_1000ha=Float64[], indice_forma_medio=Float64[])

for p in periodos
    path = joinpath(samgeo_dir, "manglar_$(p).geojson")
    isfile(path) || (println("  no encontrado: $path"); continue)
    areas_ha, perim_m = metricas_geojson(path; en_metros=false)
    fila = fila_resumen(p, areas_ha, perim_m)
    fila === nothing && (println("  $p: sin parches válidos"); continue)
    push!(res_legado, fila)
    println("  $p → $(fila[2]) parches, $(round(fila[3], digits=1)) ha")
end
CSV.write("../../outputs/tables/metricas_fragmentacion.csv", res_legado)

# ----------------------------------------------------------------------------
# Bloque 2 (nuevo): EPSG:9377 — Tarea 19
# ----------------------------------------------------------------------------

println("\n--- Bloque 2: EPSG:9377 (MAGNA-SIRGAS Origen Nacional, Tarea 19) ---")
res_9377 = DataFrame(
    periodo=String[], num_parches=Int[], area_total_ha=Float64[],
    area_media_ha=Float64[], area_max_ha=Float64[],
    densidad_parches_1000ha=Float64[], indice_forma_medio=Float64[])

for p in periodos
    path = joinpath(samgeo_dir, "manglar_$(p)_9377.geojson")
    isfile(path) || (println("  no encontrado: $path"); continue)
    areas_ha, perim_m = metricas_geojson(path; en_metros=true)
    fila = fila_resumen(p, areas_ha, perim_m)
    fila === nothing && (println("  $p: sin parches válidos"); continue)
    push!(res_9377, fila)
    println("  $p → $(fila[2]) parches, $(round(fila[3], digits=1)) ha")
end

println("\n=== TABLA COMPARATIVA EPSG:9377 ===\n"); println(res_9377)
CSV.write("../../outputs/tables/metricas_fragmentacion_9377.csv", res_9377)

println("\n*** FASE 4 JULIA COMPLETA — bloques legado + 9377 ***")
