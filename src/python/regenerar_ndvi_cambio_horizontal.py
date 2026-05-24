"""
Regenera ndvi_cambio_cubo.png con aspecto horizontal (14×6),
para que llene mejor las cards del dashboard.

Lee el mismo netCDF que el notebook 09 y aplica el mismo cálculo:
    cambio = NDVI Actual (2024-07 / 2025-06) − NDVI Degradación (2020 H2)

Uso:
    cd /home/rstudio/work/proyecto-cgsm
    python src/python/regenerar_ndvi_cambio_horizontal.py
"""
from pathlib import Path

import matplotlib.pyplot as plt
import xarray as xr

ROOT = Path(__file__).resolve().parents[2]
NC   = ROOT / 'data' / 'processed' / 'cubo' / 'cgsm_datacube_trimestral.nc'
OUT  = ROOT / 'outputs' / 'figures' / 'ndvi_cambio_cubo.png'

print(f'Leyendo {NC.name}...')
ds = xr.open_dataset(NC)
ndvi = ds['reflectance'].sel(band_idx='NDVI')

ndvi_deg = ndvi.sel(time=slice('2020-07-01', '2020-12-31')).median(dim='time')
ndvi_act = ndvi.sel(time=slice('2024-07-01', '2025-06-30')).median(dim='time')
cambio = (ndvi_act - ndvi_deg).compute()

print(f'  rango cambio: {float(cambio.min()):.3f} a {float(cambio.max()):.3f}')

# Lienzo ancho (14×6) que coincide con el aspecto de la card,
# pero con aspect='equal' para conservar la proporción geográfica real:
# el mapa NO se distorsiona, solo queda con márgenes blancos a los lados
# dentro del PNG. La card del dashboard queda totalmente llena.
fig, ax = plt.subplots(figsize=(14, 6))

im = ax.imshow(cambio.values, cmap='RdBu', vmin=-0.5, vmax=0.5,
               extent=[float(cambio.x.min()), float(cambio.x.max()),
                       float(cambio.y.min()), float(cambio.y.max())],
               origin='upper', aspect='equal')  # mapa sin distorsión

ax.set_title('Cambio NDVI: Actual (2024-2025) − Degradación (2020 H2)',
             fontsize=13, fontweight='bold', color='#1f5a4b')
ax.set_xlabel('X EPSG:9377 (m)', fontsize=10)
ax.set_ylabel('Y EPSG:9377 (m)', fontsize=10)
ax.tick_params(labelsize=9)

cbar = fig.colorbar(im, ax=ax, fraction=0.03, pad=0.02, label='Δ NDVI')
cbar.set_ticks([-0.5, -0.25, 0, 0.25, 0.5])
cbar.ax.tick_params(labelsize=9)

ax.text(0.012, 0.97, 'Rojo = pérdida de vigor\nAzul = ganancia de vigor',
        transform=ax.transAxes, va='top', fontsize=10,
        bbox=dict(facecolor='white', alpha=0.85, edgecolor='#1f5a4b',
                  boxstyle='round,pad=0.4'))

plt.tight_layout()
plt.savefig(OUT, dpi=180, bbox_inches='tight')
plt.close(fig)

mb = OUT.stat().st_size / 1024
print(f'\nGuardado: {OUT}  ({mb:.0f} KB)')
print('Aspect ratio 14:6 — ahora llena las cards horizontales del dashboard.')
