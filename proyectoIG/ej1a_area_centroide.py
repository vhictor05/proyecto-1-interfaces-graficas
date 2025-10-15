# ej1a_area_centroide.py
# Uso (CLI): python ej1a_area_centroide.py ruta/figura1a.png [--thresh 128] [--invert] [--save-bin]
from PIL import Image, ImageDraw
import numpy as np
from pathlib import Path
import argparse
import sys

# ---------------- Funciones pedidas (reciben la imagen por parámetro) ----------------

def binarizar(img: Image.Image, thresh: int = 128, invertir: bool = False) -> np.ndarray:
    """Devuelve B binaria 0/1 con 1=figura."""
    a = np.array(img.convert("L"))
    B = (a >= thresh).astype(np.uint8)
    if invertir:
        B = 1 - B
    return B

def momentos_geometricos(B: np.ndarray):
    """m00, m10, m01 para B binaria (1=figura)."""
    yy, xx = np.indices(B.shape, dtype=np.float64)
    f = B.astype(np.float64)
    m00 = f.sum()
    m10 = (xx * f).sum()
    m01 = (yy * f).sum()
    return m00, m10, m01

def centroide_por_momentos(B: np.ndarray):
    """(xc, yc) a partir de m_{pq}. Equivale al centroide geométrico."""
    m00, m10, m01 = momentos_geometricos(B)
    if m00 == 0:
        return None
    return (m10 / m00, m01 / m00)

def area_pixeles(B: np.ndarray) -> int:
    """Área como cantidad de píxeles figura = m00."""
    return int(B.sum())

def marcar_centroide(img: Image.Image, xc: float, yc: float,
                     color=(255, 0, 0), size=7) -> Image.Image:
    """Devuelve una copia RGB con una cruz en (xc, yc)."""
    out = img.convert("RGB").copy()
    d = ImageDraw.Draw(out)
    x0, y0 = int(round(xc)), int(round(yc))
    d.line([(x0 - size, y0), (x0 + size, y0)], fill=color, width=2)
    d.line([(x0, y0 - size), (x0, y0 + size)], fill=color, width=2)
    return out

# ---------------- Wrapper de conveniencia + CLI ----------------

def calcular_area_y_centroide_desde_path(path_img: str, thresh=128, invertir=False,
                                         guardar_bin=False):
    p = Path(path_img)
    img = Image.open(p)
    B = binarizar(img, thresh=thresh, invertir=invertir)
    area = area_pixeles(B)
    c = centroide_por_momentos(B)
    if c is None:
        raise ValueError("Figura vacía (m00=0). Ajusta --thresh o usa --invert.")
    xc, yc = c

    # Guardados deterministas
    marcado = marcar_centroide(img, xc, yc)
    out_cent = p.with_name(p.stem + "_centroide.png")
    marcado.save(out_cent)

    out_bin = None
    if guardar_bin:
        from PIL import Image as PILImage
        out_bin = p.with_name(p.stem + "_bin.png")
        PILImage.fromarray((B * 255).astype(np.uint8)).save(out_bin)

    return {
        "area_px": area,
        "centroide": (xc, yc),
        "salida_centroide": str(out_cent),
        "salida_binaria": str(out_bin) if out_bin else None
    }
def centroide_por_definicion(B: np.ndarray):
    """Centroide (2.14): promedio de coordenadas de los píxeles figura."""
    ys, xs = np.where(B.astype(bool))
    if xs.size == 0:
        return None
    return (xs.mean(), ys.mean())

def calcular_area_y_centroide_desde_path(path_img: str, thresh=128, invertir=False,
                                         guardar_bin=False):
    p = Path(path_img)
    img = Image.open(p)
    B = binarizar(img, thresh=thresh, invertir=invertir)
    area = area_pixeles(B)

    c_mom = centroide_por_momentos(B)
    if c_mom is None:
        raise ValueError("Figura vacía (m00=0). Ajusta --thresh o usa --invert.")
    xc_m, yc_m = c_mom

    c_def = centroide_por_definicion(B)
    if c_def is None:
        raise ValueError("Figura vacía tras definición. Revisa binarización.")
    xc_d, yc_d = c_def

    # Chequeo numérico (deberían coincidir)
    diff = float(np.hypot(xc_m - xc_d, yc_m - yc_d))

    marcado = marcar_centroide(img, xc_m, yc_m)  # marcamos el de momentos
    out_cent = p.with_name(p.stem + "_centroide.png")
    marcado.save(out_cent)

    out_bin = None
    if guardar_bin:
        from PIL import Image as PILImage
        out_bin = p.with_name(p.stem + "_bin.png")
        PILImage.fromarray((B * 255).astype(np.uint8)).save(out_bin)

    return {
        "area_px": area,
        "centroide_momentos": (xc_m, yc_m),
        "centroide_definicion": (xc_d, yc_d),
        "distancia_entre_metodos": diff,
        "salida_centroide": str(out_cent),
        "salida_binaria": str(out_bin) if out_bin else None
    }

def main():
    parser = argparse.ArgumentParser(
        description="Ej1(a): área y centroide (por momentos) sobre una figura binaria."
    )
    parser.add_argument("imagen", help="Ruta de la imagen (Figura 1.a)")
    parser.add_argument("--thresh", type=int, default=128, help="Umbral 0..255 (def:128)")
    parser.add_argument("--invert", action="store_true", help="Invierte la máscara (1=figura)")
    parser.add_argument("--save-bin", action="store_true", help="Guarda la binaria *_bin.png")
    args = parser.parse_args()

    try:
        res = calcular_area_y_centroide_desde_path(
            args.imagen, thresh=args.thresh, invertir=args.invert, guardar_bin=args.save_bin
        )
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    print(f"Umbral: {args.thresh} | Invertido: {bool(args.invert)}")
    print(f"Área (px): {res['area_px']}")

    xm, ym = res["centroide_momentos"]
    xd, yd = res["centroide_definicion"]

    print(f"Centroide por momentos (x,y): ({xm:.6f}, {ym:.6f})")
    print(f"Centroide por definición (x,y): ({xd:.6f}, {yd:.6f})")
    print(f"Diferencia entre métodos (px): {res['distancia_entre_metodos']:.6e}")

    print(f"Marcado guardado en: {res['salida_centroide']}")
    if res["salida_binaria"]:
        print(f"Binaria guardada en: {res['salida_binaria']}")


if __name__ == "__main__":
    main()
