# ej1b_momentos_23.py
# Uso: python ej1b_momentos_23.py ruta/figura1b.png
from PIL import Image
import numpy as np
import sys
from pathlib import Path

def binarizar(img, thresh=128):
    g = img.convert("L")
    a = np.array(g)
    return (a >= thresh).astype(np.uint8)  # 1=figura, 0=fondo

def momentos_raw(B, p, q):
    # m_{p,q} = sum_x sum_y x^p y^q f(x,y)
    yy, xx = np.indices(B.shape, dtype=np.float64)
    f = B.astype(np.float64)
    return float(((xx**p) * (yy**q) * f).sum())

def centroide(B):
    m00 = momentos_raw(B, 0, 0)
    if m00 == 0:
        return None, 0.0
    m10 = momentos_raw(B, 1, 0)
    m01 = momentos_raw(B, 0, 1)
    return (m10/m00, m01/m00), m00

def momento_central(B, p, q, xc, yc):
    yy, xx = np.indices(B.shape, dtype=np.float64)
    x = xx - xc
    y = yy - yc
    f = B.astype(np.float64)
    return float(((x**p) * (y**q) * f).sum())

def momento_central_normalizado(mu_pq, m00, p, q):
    # η_{p,q} = μ_{p,q} / m00^{1 + (p+q)/2}
    if m00 == 0:
        return 0.0
    gamma = 1.0 + (p + q) / 2.0
    return float(mu_pq / (m00**gamma))

def pedir_archivo_si_falta():
    # Intenta abrir un diálogo si no hay argumento
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk(); root.withdraw()
        path = filedialog.askopenfilename(
            title="Selecciona la Figura 1.b",
            filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg;*.bmp;*.tif;*.tiff"), ("Todos", "*.*")]
        )
        return path or None
    except Exception:
        return None

def main():
    # Obtener ruta
    if len(sys.argv) >= 2:
        in_path = sys.argv[1]
    else:
        in_path = pedir_archivo_si_falta()
        if not in_path:
            print("Uso: python ej1b_momentos_23.py <ruta_de_imagen>")
            sys.exit(1)

    p = Path(in_path)
    if not p.exists():
        print(f"Archivo no encontrado: {p}")
        sys.exit(1)

    # Cargar imagen y binarizar
    img = Image.open(p)
    B = binarizar(img)

    # Calcular momentos
    m23 = momentos_raw(B, 2, 3)
    c, m00 = centroide(B)
    if c is None:
        print("Figura vacía (m00=0). Revisa el umbral o la imagen.")
        sys.exit(1)
    xc, yc = c

    mu23 = momento_central(B, 2, 3, xc, yc)
    eta23 = momento_central_normalizado(mu23, m00, 2, 3)

    # Salida
    print("=== Resultados (Figura 1.b) ===")
    print(f"m00 (área): {m00:.0f}")
    print(f"Centroide:  (xc, yc) = ({xc:.6f}, {yc:.6f})")
    print(f"m_23:       {m23:.6e}")
    print(f"mu_23:      {mu23:.6e}")
    print(f"eta_23:     {eta23:.6e}")

if __name__ == "__main__":
    main()
