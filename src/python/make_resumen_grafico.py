"""
Genera la figura compuesta del resumen gráfico (graphical abstract) para el
artículo CGSM. Combina cuatro paneles en un único PNG 1600x1200 px:

  (a) Mapa esquemático del AOI con las 8 estaciones coloreadas por estado
      semáforo del módulo Digital Twin Nivel 2.
  (b) Serie temporal NDVI sobre las cuatro estaciones de manglar denso,
      con franjas que marcan los tres eventos ENSO documentados.
  (c) Barras del benchmark Random Forest vs umbrales (F1 por referencia).
  (d) Barras de correlación SAR-NDVI rezago cero por estación, con código
      de color manglar denso vs limnológica.

Uso:
    cd /home/rstudio/work/proyecto-cgsm
    python src/python/make_resumen_grafico.py
"""
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
TABLES = ROOT / 'outputs' / 'tables'
OUT = ROOT / 'outputs' / 'figures' / 'resumen_grafico_cgsm.png'

# Paletas y constantes
COLOR_M = '#1B5E20'       # manglar denso (verde oscuro)
COLOR_L = '#0288D1'       # limnológica (azul)
COLOR_EST = {'estable': '#43A047', 'alerta': '#FBC02D', 'critica': '#D32F2F'}

manglar_denso = {'CP Aguas Negras', 'CP Luna', 'Cano Palos', 'Cano Clarin'}
limnologica   = {'Isla Boqueron', 'Punta Cerro', 'Punta Chino', 'Rio Sevilla'}

stations_xy = {
    'Isla Boqueron':   (-74.298, 10.962),
    'Punta Cerro':     (-74.283, 10.973),
    'Punta Chino':     (-74.305, 10.912),
    'Rio Sevilla':     (-74.325, 10.880),
    'Cano Palos':      (-74.471, 10.758),
    'CP Luna':         (-74.560, 10.870),
    'CP Aguas Negras': (-74.570, 10.800),
    'Cano Clarin':     (-74.500, 10.600),
}


def _norm(s):
    return s.replace('_', ' ').strip()


# ------------------------------------------------------------------
# Cargar datos
# ------------------------------------------------------------------
df_alertas = pd.read_csv(TABLES / 'alertas_estaciones.csv')
df_alertas['estacion'] = df_alertas['estacion'].map(_norm)

df_ndvi = pd.read_csv(TABLES / 'ndvi_combinado_2013_2025.csv')
df_ndvi['estacion'] = df_ndvi['estacion'].map(_norm)
df_ndvi['fecha'] = pd.to_datetime(df_ndvi['fecha'], errors='coerce')

df_bench = pd.read_csv(TABLES / 'benchmark_rf_vs_umbrales.csv')

df_sar = pd.read_csv(TABLES / 'sar_vs_ndvi_correlacion.csv')
df_sar['estacion'] = df_sar['estacion'].map(_norm)
df_sar_lag0 = df_sar[df_sar['lag_meses'] == 0].copy()


# ------------------------------------------------------------------
# Figura compuesta 2x2
# ------------------------------------------------------------------
fig = plt.figure(figsize=(16, 11.5), dpi=110)
gs = fig.add_gridspec(2, 2, hspace=0.35, wspace=0.22,
                      left=0.06, right=0.98, top=0.92, bottom=0.07)

fig.suptitle('Monitor multilenguaje del manglar de la CGSM (2013-2025) — '
             'Digital Twin Nivel 2',
             fontsize=15, fontweight='bold', color='#1f5a4b', y=0.97)

# ============================================================
# Panel (a): mapa esquemático con estaciones por estado
# ============================================================
ax = fig.add_subplot(gs[0, 0])
ax.set_facecolor('#e8f4f8')

# Bbox AOI aproximado
ax.add_patch(mpatches.Rectangle(
    (-74.65, 10.55), 0.55, 0.55,
    fill=False, edgecolor='#1f5a4b', lw=2.5, label='AOI SFF + VPI'))

# Estaciones por estado
for _, row in df_alertas.iterrows():
    est = row['estacion']
    if est not in stations_xy:
        continue
    lon, lat = stations_xy[est]
    color = COLOR_EST.get(row['estado'], '#9E9E9E')
    ax.scatter(lon, lat, s=320, c=color, edgecolor='black', lw=1.5,
               zorder=3, alpha=0.92)
    ax.annotate(est, xy=(lon, lat), xytext=(7, 7),
                textcoords='offset points', fontsize=9, fontweight='bold',
                bbox=dict(facecolor='white', alpha=0.88,
                          edgecolor='gray', boxstyle='round,pad=0.25'))

# Leyenda semáforo
n_est = (df_alertas['estado'] == 'estable').sum()
n_alt = (df_alertas['estado'] == 'alerta').sum()
n_crt = (df_alertas['estado'] == 'critica').sum()
legend_p = [
    mpatches.Patch(color=COLOR_EST['estable'], label=f'Estable: {n_est}'),
    mpatches.Patch(color=COLOR_EST['alerta'],  label=f'Alerta: {n_alt}'),
    mpatches.Patch(color=COLOR_EST['critica'], label=f'Crítica: {n_crt}'),
]
ax.legend(handles=legend_p, loc='upper right', fontsize=9,
          framealpha=0.95, title='Estado actual', title_fontsize=10)

ax.set_xlim(-74.70, -74.15)
ax.set_ylim(10.50, 11.10)
ax.set_xlabel('Longitud', fontsize=10)
ax.set_ylabel('Latitud', fontsize=10)
ax.set_title('(a) Estado del semáforo por estación (2025-12)',
             fontsize=11.5, fontweight='bold', loc='left', color='#1f5a4b')
ax.grid(True, alpha=0.3)

# ============================================================
# Panel (b): serie NDVI manglar denso con franjas ENSO
# ============================================================
ax = fig.add_subplot(gs[0, 1])
ax.set_facecolor('#fafafa')

# Franjas ENSO documentadas
ax.axvspan(pd.Timestamp('2015-04-01'), pd.Timestamp('2016-05-01'),
           alpha=0.18, color='#D32F2F', label='El Niño 2015-2016')
ax.axvspan(pd.Timestamp('2020-08-01'), pd.Timestamp('2022-02-01'),
           alpha=0.18, color='#1565C0', label='La Niña 2020-2022')
ax.axvspan(pd.Timestamp('2023-06-01'), pd.Timestamp('2024-05-01'),
           alpha=0.18, color='#D32F2F', label='El Niño 2023-2024')

# Líneas NDVI por estación de manglar
colors_m = {'CP Aguas Negras': '#1B5E20', 'CP Luna': '#2E7D32',
            'Cano Palos': '#43A047', 'Cano Clarin': '#66BB6A'}
for est, col in colors_m.items():
    sub = df_ndvi[df_ndvi['estacion'] == est].sort_values('fecha')
    if len(sub):
        ax.plot(sub['fecha'], sub['ndvi'], color=col, lw=1.4,
                alpha=0.85, label=est)

# Línea de referencia 0,7
ax.axhline(0.7, color='#1B5E20', ls='--', lw=1, alpha=0.5)
ax.text(pd.Timestamp('2013-03-01'), 0.715, 'NDVI > 0,7 = manglar denso',
        fontsize=8, color='#1B5E20')

ax.set_ylim(0, 1.0)
ax.set_ylabel('NDVI', fontsize=10)
ax.set_xlabel('Año', fontsize=10)
ax.set_title('(b) Serie NDVI manglar denso 2013-2025 + eventos ENSO',
             fontsize=11.5, fontweight='bold', loc='left', color='#1f5a4b')
ax.legend(loc='lower right', fontsize=8, framealpha=0.92, ncol=2)
ax.grid(True, alpha=0.3)

# ============================================================
# Panel (c): benchmark RF vs umbrales (F1)
# ============================================================
ax = fig.add_subplot(gs[1, 0])
ax.set_facecolor('#fafafa')

referencias = df_bench['Referencia'].unique()
x = np.arange(len(referencias))
w = 0.36

f1_umb = df_bench[df_bench['Método'] == 'Umbrales NDVI/CMRI'].set_index('Referencia')['F1'].reindex(referencias)
f1_rf  = df_bench[df_bench['Método'] == 'Random Forest'].set_index('Referencia')['F1'].reindex(referencias)

b1 = ax.bar(x - w/2, f1_umb, w, label='Umbrales NDVI/CMRI',
            color='#FFB74D', edgecolor='black', lw=0.8)
b2 = ax.bar(x + w/2, f1_rf,  w, label='Random Forest',
            color='#1B5E20', edgecolor='black', lw=0.8)

# Etiquetas de valor
for bars in (b1, b2):
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.015,
                f'{h:.3f}', ha='center', va='bottom',
                fontsize=9.5, fontweight='bold')

# Flechas de mejora
for i, (umb, rf) in enumerate(zip(f1_umb, f1_rf)):
    delta = (rf - umb) / umb * 100
    ax.annotate(f'+{delta:.0f}%', xy=(i, max(rf, umb) + 0.07),
                ha='center', fontsize=10, fontweight='bold', color='#1B5E20')

ax.set_xticks(x)
ax.set_xticklabels(referencias, fontsize=10)
ax.set_ylabel('F1-score', fontsize=10)
ax.set_ylim(0, 1.1)
ax.set_title('(c) Random Forest vs umbrales — F1-score',
             fontsize=11.5, fontweight='bold', loc='left', color='#1f5a4b')
ax.legend(loc='upper left', fontsize=9.5, framealpha=0.92)
ax.grid(True, axis='y', alpha=0.3)

# ============================================================
# Panel (d): correlación SAR-NDVI rezago 0 por estación
# ============================================================
ax = fig.add_subplot(gs[1, 1])
ax.set_facecolor('#fafafa')

df_sar_lag0 = df_sar_lag0.copy()
df_sar_lag0['naturaleza'] = df_sar_lag0['estacion'].apply(
    lambda x: 'manglar' if x in manglar_denso else 'limnológica')
df_sar_lag0 = df_sar_lag0.sort_values('rho', ascending=False)

colors = [COLOR_M if n == 'manglar' else COLOR_L
          for n in df_sar_lag0['naturaleza']]
bars = ax.barh(df_sar_lag0['estacion'], df_sar_lag0['rho'],
               color=colors, edgecolor='black', lw=0.8)

# Etiquetas con valor y p-value
for bar, rho, p, est in zip(bars, df_sar_lag0['rho'], df_sar_lag0['p_value'],
                             df_sar_lag0['estacion']):
    sig = '***' if p < 0.001 else ('**' if p < 0.01 else ('*' if p < 0.05 else 'ns'))
    x_text = rho + 0.02 if rho > 0 else rho - 0.02
    ha = 'left' if rho > 0 else 'right'
    ax.text(x_text, bar.get_y() + bar.get_height()/2,
            f'{rho:+.3f} {sig}', ha=ha, va='center',
            fontsize=9.5, fontweight='bold')

ax.axvline(0, color='black', lw=1)
ax.set_xlim(-0.30, 1.05)
ax.set_xlabel('Correlación de Pearson (rezago 0)', fontsize=10)
ax.set_title('(d) Correlación SAR-VH vs NDVI por estación',
             fontsize=11.5, fontweight='bold', loc='left', color='#1f5a4b')
legend_p = [
    mpatches.Patch(color=COLOR_M, label='Manglar denso'),
    mpatches.Patch(color=COLOR_L, label='Limnológica'),
]
ax.legend(handles=legend_p, loc='lower right', fontsize=9.5,
          framealpha=0.92)
ax.grid(True, axis='x', alpha=0.3)

# Pie con resumen numérico
fig.text(0.5, 0.015,
         'Cadena Python+R+Julia · 929 obs. NDVI (2013-2025) · '
         '760 obs. SAR-VH (2018-2025) · 8 estaciones · AOI 835,3 km² '
         '(SFF CGSM + VPI Salamanca)',
         ha='center', fontsize=9.5, style='italic', color='#555')

plt.savefig(OUT, dpi=160, bbox_inches='tight', facecolor='white')
plt.close()
print(f'Resumen gráfico exportado: {OUT}')
print(f'Tamaño: {OUT.stat().st_size / 1024:.0f} KB')
