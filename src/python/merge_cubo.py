"""
Concatena los NetCDFs temporales reproyectados a EPSG:9377 que generó
build_cubos.py en un único cubo final. Sustituye a la llamada a
xr.open_mfdataset que produce Segmentation fault en HDF5 cuando hay muchos
archivos abiertos simultáneamente.

Estrategia: abrir cada NetCDF temporal con chunks dask, encadenar con
xr.concat en bucle y escribir el resultado comprimido. Los archivos
permanecen perezosos durante la concatenación, de modo que la memoria del
contenedor no se satura.

Uso:
    cd /home/rstudio/work/proyecto-cgsm
    python src/python/merge_cubo.py trimestral
    python src/python/merge_cubo.py landsat
"""
import gc
import shutil
import sys
from pathlib import Path

import pandas as pd
import xarray as xr

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / 'data' / 'processed' / 'cubo'

CONFIGS = {
    'trimestral': {
        'tmp_dir': OUT_DIR / 'tmp_trimestral',
        'out_nc':  OUT_DIR / 'cgsm_datacube_trimestral.nc',
        'bands':   ['NDVI', 'NDWI', 'CMRI'],
        'title':   'Datacube trimestral CGSM 2018-2025',
        'comment': 'Composites trimestrales NDVI/NDWI/CMRI Sentinel-2 sobre AOI acotado.',
    },
    'landsat': {
        'tmp_dir': OUT_DIR / 'tmp_landsat',
        'out_nc':  OUT_DIR / 'cgsm_datacube_landsat.nc',
        'bands':   ['NDVI', 'NDWI', 'CMRI'],
        'title':   'Datacube anual Landsat CGSM 2013-2025',
        'comment': 'Composites anuales NDVI/NDWI/CMRI Landsat 8/9 sobre AOI acotado.',
    },
}

ATTRS_BASE = {
    'Conventions': 'CF-1.8',
    'institution': 'Universidad Nacional de Colombia, Maestria en Geomatica',
    'creator_name': 'Lina Maria Quintero Fonseca',
    'creator_email': 'linaq112008@gmail.com',
    'project': 'Proyecto final Programacion en SIG, UNAL 2026-1',
    'crs_origen': 'EPSG:9377 MAGNA-SIRGAS Origen Nacional',
    'references': 'Hersbach et al. 2020; Bunting et al. 2022; Wu y Osco 2023',
    'geospatial_lat_min':  10.30, 'geospatial_lat_max':  11.20,
    'geospatial_lon_min': -75.05, 'geospatial_lon_max': -74.05,
}


def merge(tipo):
    cfg = CONFIGS[tipo]
    tmp_dir = cfg['tmp_dir']
    out_nc  = cfg['out_nc']

    ncs = sorted(tmp_dir.glob('*.nc'))
    if not ncs:
        print(f'No hay NetCDFs en {tmp_dir}'); return
    print(f'Concatenando {len(ncs)} archivos de {tmp_dir}')

    # Concatenar uno a uno, manteniendo dask perezoso
    acc = None
    for i, p in enumerate(ncs, 1):
        ds = xr.open_dataset(p, chunks={'x': 512, 'y': 512}, engine='netcdf4')
        acc = ds if acc is None else xr.concat([acc, ds], dim='time')
        if i % 5 == 0 or i == len(ncs):
            print(f'  encadenados {i}/{len(ncs)}')
        gc.collect()

    # Renombrar 'band' a 'band_idx' si existe
    if 'band' in acc.dims:
        acc = acc.rename({'band': 'band_idx'})
        acc = acc.assign_coords(band_idx=cfg['bands'])
    acc = acc.rio.write_crs('EPSG:9377')

    # Atributos CF
    acc.attrs.update(ATTRS_BASE)
    acc.attrs['title']   = cfg['title']
    acc.attrs['comment'] = cfg['comment']
    acc.attrs['history'] = pd.Timestamp.now().strftime('%Y-%m-%d') + f' merge_cubo.py {tipo}'

    if out_nc.exists():
        out_nc.unlink()
    enc = {v: {'zlib': True, 'complevel': 4} for v in acc.data_vars}
    print('Escribiendo NetCDF final...')
    acc.to_netcdf(out_nc, encoding=enc, format='NETCDF4', engine='netcdf4')
    tam_mb = out_nc.stat().st_size / (1024 * 1024)
    print(f'Guardado: {out_nc.name}  ({tam_mb:.1f} MB)')

    # Limpiar temporales
    shutil.rmtree(tmp_dir)
    print(f'tmp limpiado: {tmp_dir.name}')


if __name__ == '__main__':
    if len(sys.argv) != 2 or sys.argv[1] not in CONFIGS:
        print('Uso: python merge_cubo.py {trimestral|landsat}')
        sys.exit(1)
    merge(sys.argv[1])
