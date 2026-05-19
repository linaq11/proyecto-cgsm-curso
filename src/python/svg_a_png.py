"""
Convierte SVG a PNG (necesario para PDF Quarto).
Intenta cairosvg → rsvg-convert → resvg (en ese orden).

Uso:
    python src/python/svg_a_png.py outputs/figures/flujo_metodologia.svg
"""
import shutil
import subprocess
import sys
from pathlib import Path


def convert(svg_path: Path, png_path: Path, scale: float = 2.0) -> None:
    """Convierte SVG → PNG con la primera herramienta disponible."""
    # 1) cairosvg (Python puro, fácil de instalar)
    try:
        import cairosvg
        cairosvg.svg2png(url=str(svg_path), write_to=str(png_path),
                         scale=scale, output_width=int(1100 * scale))
        print(f'[cairosvg] {png_path} ({png_path.stat().st_size/1024:.0f} KB)')
        return
    except ImportError:
        print('cairosvg no instalado, probando rsvg-convert...')

    # 2) rsvg-convert (librsvg, suele venir con GTK)
    if shutil.which('rsvg-convert'):
        subprocess.run(['rsvg-convert', '-z', str(scale), '-o', str(png_path),
                        str(svg_path)], check=True)
        print(f'[rsvg-convert] {png_path}')
        return

    # 3) resvg (binario rust, súper rápido)
    if shutil.which('resvg'):
        subprocess.run(['resvg', '--zoom', str(scale), str(svg_path),
                        str(png_path)], check=True)
        print(f'[resvg] {png_path}')
        return

    # 4) Fallback: instalar cairosvg
    print('Instalando cairosvg...')
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'cairosvg',
                    '--break-system-packages', '--quiet'], check=True)
    import cairosvg
    cairosvg.svg2png(url=str(svg_path), write_to=str(png_path),
                     scale=scale, output_width=int(1100 * scale))
    print(f'[cairosvg-recien-instalado] {png_path}')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Uso: python svg_a_png.py <ruta_svg> [escala]')
        sys.exit(1)
    svg = Path(sys.argv[1]).resolve()
    scale = float(sys.argv[2]) if len(sys.argv) > 2 else 2.0
    png = svg.with_suffix('.png')
    convert(svg, png, scale=scale)
