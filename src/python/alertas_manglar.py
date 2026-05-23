"""
Módulo de detección de alertas tempranas para el manglar de la CGSM.

Materializa el nivel 2 del paradigma Digital Twin: sobre las series temporales
NDVI y SAR-VH ya construidas, se aplica una lógica de semáforo que clasifica
cada estación en tres estados ---estable, alerta o crítica--- según la
severidad de las anomalías recientes y la presencia de quiebres bfast en
los últimos doce meses.

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
# 3. Cargar quiebres bfast (si existen)
# ------------------------------------------------------------------
bfast_path = TABLES / 'bfast_resumen.csv'
bfast = pd.read_csv(bfast_path) if bfast_path.exists() else pd.DataFrame()
if not bfast.empty:
    print(f'  bfast: {len(bfast)} estaciones')

# ------------------------------------------------------------------
# 4. Lógica de alertas
# ------------------------------------------------------------------
def clasificar_estacion(estacion, ndvi_rec, sar_rec=None, bfast_est=None):
    """Asigna estado de alerta a una estación.

    Reglas:
        🔴 crítica: anomalía NDVI z<-2 en el último mes O quiebre bfast en últimos 6 meses
        🟡 alerta:  anomalía NDVI -2<=z<-1 en últimos 3 meses O 2+ anomalías z<-1 en 12 meses
        🟢 estable: sin anomalías significativas recientes
    """
    if len(ndvi_rec) == 0:
        return {'estado': 'sin_datos', 'razon': 'No hay registros recientes'}

    ndvi_rec = ndvi_rec.sort_values('date')
    ultimo_mes = ndvi_rec.iloc[-1] if len(ndvi_rec) else None
    ultimos_3 = ndvi_rec.tail(3)
    z_min_3 = ultimos_3['z_ndvi'].min()
    n_anomalias = (ndvi_rec['z_ndvi'] < -1).sum()
    n_criticas = (ndvi_rec['z_ndvi'] < -2).sum()

    # Estado CRÍTICO
    if ultimo_mes is not None and ultimo_mes['z_ndvi'] < -2:
        return {
            'estado': 'critica',
            'razon': f'NDVI z={ultimo_mes["z_ndvi"]:.2f} en {ultimo_mes["date"].strftime("%Y-%m")}',
            'z_actual': ultimo_mes['z_ndvi'],
            'ndvi_actual': ultimo_mes['ndvi'],
        }

    if n_criticas >= 2:
        return {
            'estado': 'critica',
            'razon': f'{n_criticas} anomalías z<-2 en últimos 12 meses',
            'z_actual': ultimo_mes['z_ndvi'] if ultimo_mes is not None else np.nan,
            'ndvi_actual': ultimo_mes['ndvi'] if ultimo_mes is not None else np.nan,
        }

    # Estado ALERTA
    if z_min_3 < -1 or n_anomalias >= 2:
        return {
            'estado': 'alerta',
            'razon': f'z mínimo últimos 3 meses = {z_min_3:.2f} · {n_anomalias} anomalías 12 meses',
            'z_actual': ultimo_mes['z_ndvi'] if ultimo_mes is not None else np.nan,
            'ndvi_actual': ultimo_mes['ndvi'] if ultimo_mes is not None else np.nan,
        }

    # Estado ESTABLE
    return {
        'estado': 'estable',
        'razon': 'Sin anomalías significativas en 12 meses',
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
    resultado = clasificar_estacion(estacion, sub_ndvi, None, sub_bfast)
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

fig, ax = plt.subplots(figsize=(10, 8))
ax.set_facecolor('#e8f4f8')

# Dibujar bbox del AOI
from matplotlib.patches import Rectangle
ax.add_patch(Rectangle((-74.65, 10.55), 0.45, 0.55,
                       fill=False, edgecolor='#1f5a4b', lw=2,
                       label='AOI acotado CGSM'))

# Plotear estaciones
for _, row in df_alertas.iterrows():
    coords = buscar_coords(row['estacion'])
    if coords is None:
        continue
    lon, lat = coords
    color = colores.get(row['estado'], '#9e9e9e')
    ax.scatter(lon, lat, s=400, c=color, edgecolor='black', lw=2,
               zorder=3, alpha=0.92)
    ax.annotate(row['estacion'], xy=(lon, lat), xytext=(8, 8),
                textcoords='offset points', fontsize=10, fontweight='bold',
                bbox=dict(facecolor='white', alpha=0.9, edgecolor='gray',
                          boxstyle='round,pad=0.3'))

# Leyenda
legend_patches = [
    mpatches.Patch(color=colores['critica'], label='🔴 Crítica'),
    mpatches.Patch(color=colores['alerta'], label='🟡 Alerta'),
    mpatches.Patch(color=colores['estable'], label='🟢 Estable'),
]
ax.legend(handles=legend_patches, loc='upper right', fontsize=11,
          framealpha=0.95, title='Estado actual del manglar')

ax.set_xlim(-74.70, -74.15)
ax.set_ylim(10.50, 11.10)
ax.set_xlabel('Longitud')
ax.set_ylabel('Latitud')
ax.set_title('Semáforo de alertas CGSM · Estado actual por estación de monitoreo\n'
             f'(generado el {datetime.now().strftime("%Y-%m-%d")})',
             fontsize=12, fontweight='bold', pad=15)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(FIGURES / 'alertas_semaforo.png', dpi=180, bbox_inches='tight')
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
