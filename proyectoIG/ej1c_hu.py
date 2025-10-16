# ej1c_hu.py
# Uso: python ej1c_hu.py ruta/figura1c.png
from PIL import Image
import numpy as np
import sys
from pathlib import Path
from math import isfinite
import argparse
from math import log10, copysign

def hu_log(v):
    # phi = -sign(v)*log10(|v|), protegido para v=0
    if v == 0.0:
        return 0.0
    return -copysign(log10(abs(v)), v)

def binarizar(img, thresh=128, invertir=False):
    a = np.array(img.convert("L"))
    B = (a >= thresh).astype(np.uint8)  # 1=figura
    return (1 - B) if invertir else B

def raw_moment(B, p, q):
    yy, xx = np.indices(B.shape, dtype=np.float64)
    f = B.astype(np.float64)
    return float(((xx**p) * (yy**q) * f).sum())

def centroid(B):
    m00 = raw_moment(B, 0, 0)
    if m00 == 0:
        return None, 0.0
    m10 = raw_moment(B, 1, 0)
    m01 = raw_moment(B, 0, 1)
    return (m10/m00, m01/m00), m00

def central_moment(B, p, q, xc, yc):
    yy, xx = np.indices(B.shape, dtype=np.float64)
    x = xx - xc
    y = yy - yc
    f = B.astype(np.float64)
    return float(((x**p) * (y**q) * f).sum())

def eta(mu_pq, m00, p, q):
    if m00 == 0:
        return 0.0
    gamma = 1.0 + (p + q) / 2.0
    return float(mu_pq / (m00**gamma))

def hu_moments(B):
    c, m00 = centroid(B)
    if c is None:
        return (0.0, 0.0, 0.0)
    xc, yc = c

    mu20 = central_moment(B, 2, 0, xc, yc); mu02 = central_moment(B, 0, 2, xc, yc)
    mu11 = central_moment(B, 1, 1, xc, yc)
    mu30 = central_moment(B, 3, 0, xc, yc); mu12 = central_moment(B, 1, 2, xc, yc)
    mu21 = central_moment(B, 2, 1, xc, yc); mu03 = central_moment(B, 0, 3, xc, yc)

    n20 = eta(mu20, m00, 2, 0); n02 = eta(mu02, m00, 0, 2); n11 = eta(mu11, m00, 1, 1)
    n30 = eta(mu30, m00, 3, 0); n12 = eta(mu12, m00, 1, 2)
    n21 = eta(mu21, m00, 2, 1); n03 = eta(mu03, m00, 0, 3)

    H1 = n20 + n02
    H2 = (n20 - n02)**2 + 4.0*(n11**2)
    H3 = (n30 - 3.0*n12)**2 + (3.0*n21 - n03)**2
    return H1, H2, H3

def pedir_archivo_si_falta():
    # Intenta abrir un diálogo si no hay argumento
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk(); root.withdraw()
        path = filedialog.askopenfilename(
            title="Selecciona la Figura 1.c",
            filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg;*.bmp;*.tif;*.tiff"), ("Todos", "*.*")]
        )
        return path or None
    except Exception:
        return None

def main():
    parser = argparse.ArgumentParser(description="Ej1(c): Momentos de Hu H1-H3.")
    parser.add_argument("imagen", nargs="?", help="Ruta de la Figura 1.c")
    parser.add_argument("--thresh", type=int, default=128, help="Umbral 0..255 (def:128)")
    parser.add_argument("--invert", action="store_true", help="Invierte la máscara (1=figura)")
    parser.add_argument("--show-checks", action="store_true",
                        help="Imprime μ00, μ10≈0, μ01≈0 para sanidad")
    parser.add_argument("--show-log", action="store_true",
                        help="Imprime Hu en escala log (phi)")
    args = parser.parse_args()

    in_path = args.imagen or pedir_archivo_si_falta()
    if not in_path:
        print("Uso: python ej1c_hu.py <ruta_de_imagen> [--thresh 128] [--invert]")
        sys.exit(1)

    p = Path(in_path)
    if not p.exists():
        print(f"Archivo no encontrado: {p}")
        sys.exit(1)

    img = Image.open(p)
    B = binarizar(img, thresh=args.thresh, invertir=args.invert)

    c, m00 = centroid(B)
    if c is None:
        print("Figura vacía (m00=0). Revisa el umbral o usa --invert.")
        sys.exit(1)
    xc, yc = c

    H1, H2, H3 = hu_moments(B)
    vals = [H1, H2, H3]
    safe = [v if isfinite(v) else 0.0 for v in vals]

    print("=== Momentos de Hu (Figura 1.c) ===")
    print(f"Umbral: {args.thresh} | Invertido: {bool(args.invert)}")
    print(f"m00 (área): {m00:.0f}")
    print(f"Centroide:   (xc, yc) = ({xc:.6f}, {yc:.6f})")
    print(f"H1 = {safe[0]:.6e}")
    print(f"H2 = {safe[1]:.6e}")
    print(f"H3 = {safe[2]:.6e}")

    if args.show_log:
        print("--- Hu log (phi) ---")
        print(f"phi1 = {hu_log(safe[0]):.6e}")
        print(f"phi2 = {hu_log(safe[1]):.6e}")
        print(f"phi3 = {hu_log(safe[2]):.6e}")

    if args.show_checks:
        # sanidad: mu00=m00, mu10≈0, mu01≈0
        mu00 = central_moment(B, 0, 0, xc, yc)
        mu10 = central_moment(B, 1, 0, xc, yc)
        mu01 = central_moment(B, 0, 1, xc, yc)
        print("--- Checks ---")
        print(f"mu00 (=m00): {mu00:.0f}")
        print(f"mu10 ≈ 0:    {mu10:.6e}")
        print(f"mu01 ≈ 0:    {mu01:.6e}")

if __name__ == "__main__":
    main()
