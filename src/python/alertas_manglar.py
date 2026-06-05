"""
Módulo de detección de alertas tempranas para el manglar de la CGSM.

Materializa el nivel 2 del paradigma Digital Twin: sobre las series temporales
NDVI y SAR-VH ya construidas, se integran dos señales complementarias y se
aplica una lógica de semáforo que clasifica cada estación en tres estados
(estable, alerta o crítica):

  1. z-score reciente del NDVI (anomalías últimos 12 meses).
  2. Breakpoints de bfastmonitor near-real-time leídos de
     `outputs/tables/bfastmonitor_estaciones.csv` (notebook 06b_bfast_monitor_R).
     bfastmonitor opera sobre series zonales (CP Pajarales, VIPIS) que cuentan
     con la ventana histórica 2013-2019 requerida por el método. La señal zonal
     se propaga a las estaciones de manglar del polígono via BFM_ZONA_ESTACIONES;
     las limnológicas no se propagan porque muestrean espejo de agua, no dosel.

La combinación de ambas señales permite escalar a crítica cuando hay
breakpoint con magnitud negativa y z-score deteriorado en paralelo, marcar
alerta cuando el monitor detecta breakpoint aún si las anomalías z son
moderadas, y conservar estable solo si no hay ninguna de las dos señales.

Entradas:
    outputs/tables/serie_temporal_ndvi_definitiva.csv
    outputs/tables/sar_vh_serie_mensual.csv          (opcional)
    outputs/tables/bfast_resumen.csv                  (opcional · bfast clásico)
    outputs/tables/bfastmonitor_estaciones.csv        (opcional · near-real-time)

Salidas:
    outputs/tables/alertas_estaciones.csv
    outputs/figures/alertas_semaforo.png

Uso:
    cd /home/rstudio/work/proyecto-cgsm
    python src/python/alertas_manglar.py
"""
from pathlib import Path
from datetime import datetime

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

ROOT = Path(__file__).resolve().parents[2]
TABLES = ROOT / 'outputs' / 'tables'
FIGURES = ROOT / 'outputs' / 'figures'

# ------------------------------------------------------------------
# 1. Cargar series temporales NDVI y SAR
# ------------------------------------------------------------------
ndvi_path = TABLES / 'serie_temporal_ndvi_definitiva.csv'
sar_path = TABLES / 'sar_vh_serie_mensual.csv'

print(f'Cargando series temporales...')
ndvi = pd.read_csv(ndvi_path, parse_dates=['date']) if ndvi_path.exists() else None
sar = pd.read_csv(sar_path, parse_dates=['date']) if sar_path.exists() else None

if ndvi is None:
    raise FileNotFoundError(f'Serie NDVI no encontrada: {ndvi_path}')

# Normalizar columna 'subzona' o 'estacion'
if 'subzona' in ndvi.columns:
    ndvi = ndvi.rename(columns={'subzona': 'estacion'})

print(f'  NDVI: {len(ndvi)} registros · {ndvi["estacion"].nunique()} estaciones')
if sar is not None:
    print(f'  SAR:  {len(sar)} registros · {sar["estacion"].nunique()} estaciones')

# ------------------------------------------------------------------
# 2. Calcular z-scores recientes (últimos 12 meses)
# ------------------------------------------------------------------
fecha_corte = ndvi['date'].max() - pd.DateOffset(months=12)
ndvi['z_ndvi'] = ndvi.groupby('estacion')['ndvi'].transform(
    lambda x: (x - x.mean()) / x.std()
)

recientes = ndvi[ndvi['date'] >= fecha_corte].copy()

# ------------------------------------------------------------------
# 3. Cargar quiebres bfast clásico (si existen)
# ------------------------------------------------------------------
bfast_path = TABLES / 'bfast_resumen.csv'
bfast = pd.read_csv(bfast_path) if bfast_path.exists() else pd.DataFrame()
if not bfast.empty:
    print(f'  bfast: {len(bfast)} estaciones')

# ------------------------------------------------------------------
# 3b. Cargar resultados bfastmonitor near-real-time (si existen)
#     Producido por notebooks/06b_bfast_monitor_R.ipynb
#     Columnas: estacion, breakpoint, magnitud, estado
# ------------------------------------------------------------------
bfm_path = TABLES / 'bfastmonitor_estaciones.csv'
bfm = pd.read_csv(bfm_path) if bfm_path.exists() else pd.DataFrame()
if not bfm.empty:
    print(f'  bfastmonitor: {len(bfm)} estaciones')


# Mapping zona bfastmonitor -> estaciones individuales.
# El notebook 06b corre bfastmonitor sobre series zonales agregadas
# (CP Pajarales, VIPIS) que requieren la ventana histórica 2013-2019
# disponible en ndvi_combinado_2013_2025.csv. Las estaciones individuales
# solo tienen serie desde 2018 (S2), insuficiente para la ventana
# histórica del monitor. Por eso el breakpoint zonal se propaga a las
# estaciones de manglar dentro del polígono. Las limnológicas no se
# propagan porque muestrean espejo de agua, no manglar.
BFM_ZONA_ESTACIONES = {
    'CP Pajarales': ['CP_Aguas_Negras', 'CP_Luna', 'Cano_Palos', 'Cano_Clarin'],
    # 'VIPIS': []  # ninguna estación de monitoreo cae dentro del manglar VIPIS
}


def _bfm_row(estacion):
    """Devuelve la fila bfastmonitor de la zona que contiene la estación, o None.

    Búsqueda por zona y propagación a las estaciones del polígono. El supuesto
    de propagación está documentado en BFM_ZONA_ESTACIONES.
    """
    if bfm.empty or 'estacion' not in bfm.columns:
        return None
    # Match directo (por si bfastmonitor se aplicó a la estación misma)
    sub = bfm[bfm['estacion'] == estacion]
    if not sub.empty:
        return sub.iloc[0]
    # Match por zona (propagación)
    for zona, estaciones in BFM_ZONA_ESTACIONES.items():
        if estacion in estaciones:
            sub = bfm[bfm['estacion'] == zona]
            if not sub.empty:
                return sub.iloc[0]
    return None


# ------------------------------------------------------------------
# 4. Lógica de alertas (z-score NDVI + bfastmonitor near-real-time)
# ------------------------------------------------------------------
def clasificar_estacion(estacion, ndvi_rec, sar_rec=None, bfast_est=None, bfm_est=None):
    """Asigna estado de alerta a una estación.

    Reglas integradas (z-score + bfastmonitor):
        crítica: anomalía NDVI z<-2 en el último mes O
                 2+ anomalías z<-2 en 12 meses O
                 bfastmonitor breakpoint con magnitud NEGATIVA Y z mínimo 3 meses <-1
        alerta:  anomalía NDVI -2<=z<-1 en últimos 3 meses O
                 2+ anomalías z<-1 en 12 meses O
                 bfastmonitor breakpoint con magnitud NEGATIVA (deterioro)
        estable: sin anomalías z significativas y sin breakpoint negativo.
                 Si bfastmonitor reporta breakpoint POSITIVO (recuperación), se
                 anota en la razón como contexto pero no cambia el estado.
    """
    if len(ndvi_rec) == 0:
        return {'estado': 'sin_datos', 'razon': 'No hay registros recientes'}

    ndvi_rec = ndvi_rec.sort_values('date')
    ultimo_mes = ndvi_rec.iloc[-1] if len(ndvi_rec) else None
    ultimos_3 = ndvi_rec.tail(3)
    z_min_3 = ultimos_3['z_ndvi'].min()
    n_anomalias = (ndvi_rec['z_ndvi'] < -1).sum()
    n_criticas = (ndvi_rec['z_ndvi'] < -2).sum()

    # Señal bfastmonitor
    bfm_breakpoint = False
    bfm_magnitud_neg = False
    bfm_etiqueta = ''
    if bfm_est is not None:
        estado_bfm = str(bfm_est.get('estado', ''))
        magn = bfm_est.get('magnitud', None)
        if estado_bfm == 'breakpoint_detectado':
            bfm_breakpoint = True
            if pd.notna(magn) and magn < 0:
                bfm_magnitud_neg = True
            bfm_etiqueta = f' · bfastmonitor bp magnitud={magn:.3f}' if pd.notna(magn) else ' · bfastmonitor bp'

    # Estado CRÍTICO
    if ultimo_mes is not None and ultimo_mes['z_ndvi'] < -2:
        return {
            'estado': 'critica',
            'razon': f'NDVI z={ultimo_mes["z_ndvi"]:.2f} en {ultimo_mes["date"].strftime("%Y-%m")}{bfm_etiqueta}',
            'z_actual': ultimo_mes['z_ndvi'],
            'ndvi_actual': ultimo_mes['ndvi'],
        }

    if n_criticas >= 2:
        return {
            'estado': 'critica',
            'razon': f'{n_criticas} anomalías z<-2 en últimos 12 meses{bfm_etiqueta}',
            'z_actual': ultimo_mes['z_ndvi'] if ultimo_mes is not None else np.nan,
            'ndvi_actual': ultimo_mes['ndvi'] if ultimo_mes is not None else np.nan,
        }

    if bfm_magnitud_neg and z_min_3 < -1:
        return {
            'estado': 'critica',
            'razon': f'bfastmonitor breakpoint magnitud<0 + z min 3m={z_min_3:.2f}',
            'z_actual': ultimo_mes['z_ndvi'] if ultimo_mes is not None else np.nan,
            'ndvi_actual': ultimo_mes['ndvi'] if ultimo_mes is not None else np.nan,
        }

    # Estado ALERTA · solo el breakpoint con magnitud negativa escala estado.
    # Breakpoints positivos (recuperaciones) se mencionan en la razón pero no
    # disparan alerta, porque indican mejora del dosel, no deterioro.
    if (bfm_breakpoint and bfm_magnitud_neg) or z_min_3 < -1 or n_anomalias >= 2:
        razon_alerta = (f'z mínimo últimos 3 meses = {z_min_3:.2f} · '
                        f'{n_anomalias} anomalías 12 meses{bfm_etiqueta}')
        return {
            'estado': 'alerta',
            'razon': razon_alerta,
            'z_actual': ultimo_mes['z_ndvi'] if ultimo_mes is not None else np.nan,
            'ndvi_actual': ultimo_mes['ndvi'] if ultimo_mes is not None else np.nan,
        }

    # Estado ESTABLE · si bfastmonitor reporta breakpoint positivo (recuperación)
    # se anota como contexto, pero no afecta el estado.
    razon_estable = ('Sin anomalías significativas en 12 meses' +
                     (f'; bfastmonitor reporta recuperación regional magnitud={bfm_est.get("magnitud", float("nan")):+.3f}'
                      if bfm_breakpoint and not bfm_magnitud_neg else
                      ' y sin breakpoint near-real-time'))
    return {
        'estado': 'estable',
        'razon': razon_estable,
        'z_actual': ultimo_mes['z_ndvi'] if ultimo_mes is not None else np.nan,
        'ndvi_actual': ultimo_mes['ndvi'] if ultimo_mes is not None else np.nan,
    }


# ------------------------------------------------------------------
# 5. Generar tabla de alertas
# ------------------------------------------------------------------
alertas = []
for estacion in sorted(ndvi['estacion'].unique()):
    sub_ndvi = recientes[recientes['estacion'] == estacion]
    sub_bfast = bfast[bfast.get('estacion', pd.Series()).eq(estacion)] if not bfast.empty else None
    sub_bfm = _bfm_row(estacion)
    resultado = clasificar_estacion(estacion, sub_ndvi, None, sub_bfast, sub_bfm)
    resultado['estacion'] = estacion
    alertas.append(resultado)

df_alertas = pd.DataFrame(alertas)
df_alertas = df_alertas[['estacion', 'estado', 'z_actual', 'ndvi_actual', 'razon']]
df_alertas = df_alertas.round(3)
df_alertas['icono'] = df_alertas['estado'].map(
    {'critica': '🔴', 'alerta': '🟡', 'estable': '🟢', 'sin_datos': '⚪'}
)

print('\n' + '=' * 70)
print('TABLA DE ALERTAS · Estado actual del manglar CGSM')
print('=' * 70)
print(df_alertas.to_string(index=False))

df_alertas.to_csv(TABLES / 'alertas_estaciones.csv', index=False)
print(f'\n✓ {TABLES / "alertas_estaciones.csv"}')


# ------------------------------------------------------------------
# 6. Figura: semáforo sobre mapa
# ------------------------------------------------------------------
stations_coords = {
    'Isla_Boqueron': (-74.298, 10.962),
    'Punta_Cerro':   (-74.283, 10.973),
    'Punta_Chino':   (-74.305, 10.912),
    'Rio_Sevilla':   (-74.325, 10.880),
    'Cano_Palos':    (-74.471, 10.758),
    'CP_Luna':       (-74.560, 10.870),
    'CP_Aguas_Negras': (-74.570, 10.800),
    'Cano_Clarin':   (-74.500, 10.600),
}
# Soporta nombres con/sin underscore
def buscar_coords(nombre):
    n1 = nombre.replace(' ', '_')
    for k, v in stations_coords.items():
        if k.lower() == n1.lower():
            return v
    return None

colores = {'critica': '#d32f2f', 'alerta': '#fbc02d',
           'estable': '#43a047', 'sin_datos': '#9e9e9e'}

# ---- Estilo y figura ----
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.edgecolor'] = '#b0b8c0'
plt.rcParams['axes.linewidth'] = 0.8

fig, ax = plt.subplots(figsize=(11, 7.5))
fig.patch.set_facecolor('white')
ax.set_facecolor('#f6f8fa')

# ---- Referencias geográficas mínimas (costa Caribe colombiana) ----
# Costa aproximada como sombreado azul muy suave al norte
ax.axhspan(11.00, 11.10, alpha=0.4, color='#dcecf5', zorder=0)
ax.text(-74.20, 11.05, 'Mar Caribe', fontsize=8.5, color='#5b7a8c',
        style='italic', ha='right', va='center', zorder=1)

# Ciudades de referencia
cities = {
    'Barranquilla': (-74.78, 10.96),
    'Santa Marta':  (-74.21, 11.24),  # fuera de plot pero la dejamos para flecha
    'Ciénaga':      (-74.25, 11.01),
}
for name, (lon, lat) in cities.items():
    if -74.70 < lon < -74.15 and 10.50 < lat < 11.10:
        ax.plot(lon, lat, marker='s', color='#9aa4b2', markersize=5,
                markeredgecolor='white', markeredgewidth=0.8, zorder=2)
        ax.annotate(name, xy=(lon, lat), xytext=(7, -2),
                    textcoords='offset points', fontsize=8.5,
                    color='#5b6472', style='italic')

# ---- Bbox del AOI: línea punteada sutil, sin label ----
ax.add_patch(Rectangle((-74.65, 10.55), 0.45, 0.55,
                       fill=False, edgecolor='#1f7a52', lw=1.2,
                       linestyle=(0, (6, 4)), alpha=0.65, zorder=2))
ax.text(-74.65, 10.55 - 0.018, 'AOI acotado CGSM',
        fontsize=8.5, color='#1f7a52', style='italic', alpha=0.85)

# ---- Offsets de label por estación para evitar solapamientos ----
# Punta_Cerro (norte) ↔ Isla_Boqueron (justo al lado, sur-oeste) → separar
# Punta_Chino ↔ Rio_Sevilla → separar verticalmente
LABEL_OFFSET = {
    'Punta_Cerro':     (12,  10),   # NE del marker
    'Isla_Boqueron':   (-12, -2),   # W del marker (a la izquierda, alineado verticalmente)
    'Punta_Chino':     (12,  -8),   # SE del marker (abajo-derecha)
    'Rio_Sevilla':     (-12, -2),   # W del marker
    'Cano_Palos':      (12,   6),
    'CP_Luna':         (-12,  10),  # NW del marker
    'CP_Aguas_Negras': (-12, -14),  # SW del marker
    'Cano_Clarin':     (12,   6),
}

# Mapeo de IDs (sin tilde, joinable con CSVs) a labels visibles (con tilde).
# Los IDs internos como Cano_Palos deben coincidir con la columna 'estacion'
# de outputs/tables/alertas_estaciones.csv; los labels son lo que el lector ve.
PRETTY = {
    'Cano Palos':      'Caño Palos',
    'Cano Clarin':     'Caño Clarín',
    'Isla Boqueron':   'Isla Boquerón',
    'Rio Sevilla':     'Río Sevilla',
}

# ---- Plotear estaciones ----
for _, row in df_alertas.iterrows():
    coords = buscar_coords(row['estacion'])
    if coords is None:
        continue
    lon, lat = coords
    color = colores.get(row['estado'], '#9e9e9e')
    ax.scatter(lon, lat, s=320, c=color, edgecolor='white', lw=2.2,
               zorder=4, alpha=0.95)
    # Punto interior pequeño para "anclar" el círculo grande
    ax.scatter(lon, lat, s=18, c='white', zorder=5)

    raw_label = row['estacion'].replace('_', ' ')
    label = PRETTY.get(raw_label, raw_label)
    dx, dy = LABEL_OFFSET.get(row['estacion'], (10, 8))
    ha = 'right' if dx < 0 else 'left'
    ax.annotate(label, xy=(lon, lat), xytext=(dx, dy),
                textcoords='offset points', fontsize=9.5, fontweight=600,
                ha=ha, color='#0f172a', zorder=6,
                bbox=dict(facecolor='white', alpha=0.92,
                          edgecolor='#d4dae0', boxstyle='round,pad=0.32',
                          linewidth=0.8))

# ---- Leyenda con círculos reales (sin emojis) ----
estado_orden = [('estable',  'Estable'),
                ('alerta',   'En alerta'),
                ('critica',  'Crítica')]
legend_handles = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor=colores[k],
           markeredgecolor='white', markeredgewidth=1.5,
           markersize=12, label=lbl)
    for k, lbl in estado_orden
]
leg = ax.legend(handles=legend_handles, loc='lower right',
                fontsize=10, framealpha=0.97,
                title='Estado al cierre 2025',
                title_fontsize=10.5, borderpad=0.8,
                edgecolor='#d4dae0', facecolor='white')
leg.get_title().set_fontweight('600')

# ---- Ejes y título ----
ax.set_xlim(-74.70, -74.15)
ax.set_ylim(10.50, 11.10)
ax.set_xlabel('Longitud (°)', fontsize=10, color='#5b6472')
ax.set_ylabel('Latitud (°)', fontsize=10, color='#5b6472')
ax.tick_params(colors='#5b6472', labelsize=9)
for spine in ax.spines.values():
    spine.set_color('#d4dae0')

# Título + subtítulo posicionados con fig.text para evitar superposición
# con el área del plot (ax.text con ax.transAxes podía caer dentro del axes).
fig.text(0.02, 0.965, 'Alerta temprana por estación · CGSM',
         fontsize=15, fontweight=700, color='#0f172a',
         ha='left', va='top')
fig.text(0.02, 0.935,
         f'Sistema de alertas tempranas · actualizado {datetime.now().strftime("%d %b %Y")}',
         fontsize=10, color='#5b6472', ha='left', va='top', style='italic')
# Reservar espacio arriba para el título
plt.subplots_adjust(top=0.88)

ax.grid(True, alpha=0.35, linestyle='-', linewidth=0.5, color='#c8d0d8')
ax.set_axisbelow(True)

# NOTA: no usar tight_layout aquí porque pisa el subplots_adjust del título.
plt.savefig(FIGURES / 'alertas_semaforo.png', dpi=180,
            bbox_inches='tight', facecolor='white')
plt.close()
print(f'✓ {FIGURES / "alertas_semaforo.png"}')


# ------------------------------------------------------------------
# 7. Resumen final
# ------------------------------------------------------------------
conteo = df_alertas['estado'].value_counts()
print(f'\n{"=" * 70}')
print('RESUMEN · Distribución de estados sobre 8 estaciones')
print('=' * 70)
for estado in ['critica', 'alerta', 'estable', 'sin_datos']:
    n = conteo.get(estado, 0)
    icono = {'critica': '🔴', 'alerta': '🟡', 'estable': '🟢', 'sin_datos': '⚪'}[estado]
    print(f'  {icono} {estado:>10}: {n} estaciones')

print(f'\nFecha generación: {datetime.now().strftime("%Y-%m-%d %H:%M")}')
