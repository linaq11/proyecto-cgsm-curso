"""
Construye el cubo NetCDF trimestral o anual reproyectando cada TIF a EPSG:9377
en disco antes de concatenar. Está pensado para correrse fuera de Jupyter, pues
cada llamada es un proceso Python fresco que libera la memoria por completo al
terminar, de modo que el contenedor de 8 GB no se ahoga procesando 31 trimestres
o 13 años seguidos.

Uso:
    cd /home/rstudio/work/proyecto-cgsm
    python src/python/build_cubos.py trimestral
    python src/python/build_cubos.py landsat
"""
import gc
import re
import shutil
import sys
from pathlib import Path

import pandas as pd
import rioxarray
import xarray as xr
from rasterio.enums import Resampling

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / 'data' / 'processed' / 'cubo'
OUT_DIR.mkdir(parents=True, exist_ok=True)

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

CONFIGS = {
    'trimestral': {
        'src_dir':   ROOT / 'data' / 'processed' / 's2',
        'pattern':   'CGSM_indices_*.tif',
        'date_re':   re.compile(r'(\d{4})[_-]?Q(\d)'),
        'date_fn':   lambda m: pd.Timestamp(
            f'{int(m.group(1))}-{(int(m.group(2))-1)*3+2:02d}-15'),
        'out_nc':    OUT_DIR / 'cgsm_datacube_trimestral.nc',
        'tmp_dir':   OUT_DIR / 'tmp_trimestral',
        'bands':     ['NDVI', 'NDWI', 'CMRI'],
        'title':     'Datacube trimestral CGSM 2018-2025',
        'comment':   'Composites trimestrales NDVI/NDWI/CMRI Sentinel-2 sobre AOI acotado.',
    },
    'landsat': {
        'src_dir':   ROOT / 'data' / 'processed' / 'landsat',
        'pattern':   'CGSM_Landsat_indices_*.tif',
        'date_re':   re.compile(r'(\d{4})'),
        'date_fn':   lambda m: pd.Timestamp(f'{int(m.group(1))}-07-01'),
        'out_nc':    OUT_DIR / 'cgsm_datacube_landsat.nc',
        'tmp_dir':   OUT_DIR / 'tmp_landsat',
        'bands':     ['NDVI', 'NDWI', 'CMRI'],
        'title':     'Datacube anual Landsat CGSM 2013-2025',
        'comment':   'Composites anuales NDVI/NDWI/CMRI Landsat 8/9 sobre AOI acotado.',
    },
}


def reproyectar_a_temp(tif, fecha, ref, tmp_dir, target_res=30):
    """Reproyecta un TIF a 'ref' o a EPSG:9377 a 'target_res' metros y guarda comprimido.

    Cada raster temporal se guarda como NetCDF con compresión zlib nivel 4 y
    resampleado a 30 m, pues a 10 m los temporales sumaban 12 GB y saturaban
    el contenedor al concatenar.
    """
    nc_out = tmp_dir / f'{tif.stem}.nc'
    if nc_out.exists():
        return nc_out
    da = rioxarray.open_rasterio(tif, chunks={'x': 512, 'y': 512})
    if ref is None:
        if str(da.rio.crs).upper() != 'EPSG:9377':
            da = da.rio.reproject(
                'EPSG:9377', resolution=target_res, resampling=Resampling.bilinear)
        elif da.rio.resolution()[0] != target_res:
            da = da.rio.reproject(
                'EPSG:9377', resolution=target_res, resampling=Resampling.bilinear)
    else:
        da = da.rio.reproject_match(ref, resampling=Resampling.bilinear)

    ds = da.assign_coords(time=fecha).expand_dims('time').to_dataset(name='reflectance')
    enc = {'reflectance': {'zlib': True, 'complevel': 4}}
    ds.to_netcdf(nc_out, encoding=enc, format='NETCDF4')
    da.close(); ds.close()
    gc.collect()
    return nc_out


def build(tipo):
    cfg = CONFIGS[tipo]
    src_dir  = cfg['src_dir']
    tmp_dir  = cfg['tmp_dir']
    tmp_dir.mkdir(parents=True, exist_ok=True)

    tifs = sorted(src_dir.glob(cfg['pattern']))
    if not tifs:
        print(f'No hay TIFs en {src_dir}')
        return

    print(f'Construyendo cubo {tipo}: {len(tifs)} rasters')

    # Reproyectar el primero a 9377 a 30 m como referencia de grilla
    m0 = cfg['date_re'].search(tifs[0].name)
    fecha0 = cfg['date_fn'](m0)
    print(f'  ref ({tifs[0].name}) -> 9377 @ 30 m')
    ref_path = reproyectar_a_temp(tifs[0], fecha0, None, tmp_dir, target_res=30)
    ref = rioxarray.open_rasterio(tifs[0], chunks={'x': 512, 'y': 512})
    if str(ref.rio.crs).upper() != 'EPSG:9377':
        ref = ref.rio.reproject(
            'EPSG:9377', resolution=30, resampling=Resampling.bilinear)
    elif ref.rio.resolution()[0] != 30:
        ref = ref.rio.reproject(
            'EPSG:9377', resolution=30, resampling=Resampling.bilinear)

    # El resto se alinea contra ref
    for tif in tifs[1:]:
        m = cfg['date_re'].search(tif.name)
        if not m:
            print(f'  sin fecha en nombre: {tif.name}'); continue
        fecha = cfg['date_fn'](m)
        reproyectar_a_temp(tif, fecha, ref, tmp_dir)
        print(f'  {fecha.date()} listo')

    ref.close()
    gc.collect()

    # Concatenar los NC temporales y guardar el cubo final
    print('Concatenando rasters reproyectados...')
    ds = xr.open_mfdataset(
        str(tmp_dir / '*.nc'), combine='nested', concat_dim='time',
        chunks={'time': 1, 'x': 512, 'y': 512})
    ds = ds.rio.write_crs('EPSG:9377')
    if 'band' in ds.dims:
        ds = ds.rename({'band': 'band_idx'})
        ds = ds.assign_coords(band_idx=cfg['bands'])
    ds.attrs.update(ATTRS_BASE)
    ds.attrs['title']   = cfg['title']
    ds.attrs['comment'] = cfg['comment']
    ds.attrs['history'] = pd.Timestamp.now().strftime('%Y-%m-%d') + f' build_cubos.py {tipo}'

    if cfg['out_nc'].exists():
        cfg['out_nc'].unlink()
    enc = {v: {'zlib': True, 'complevel': 4} for v in ds.data_vars}
    ds.to_netcdf(cfg['out_nc'], encoding=enc, format='NETCDF4')
    tam_mb = cfg['out_nc'].stat().st_size / (1024 * 1024)
    print(f'Guardado: {cfg["out_nc"].name}  ({tam_mb:.1f} MB)')

    # Limpieza
    shutil.rmtree(tmp_dir)
    print(f'tmp limpiado: {tmp_dir.name}')


if __name__ == '__main__':
    if len(sys.argv) != 2 or sys.argv[1] not in CONFIGS:
        print('Uso: python build_cubos.py {trimestral|landsat}')
        sys.exit(1)
    build(sys.argv[1])
