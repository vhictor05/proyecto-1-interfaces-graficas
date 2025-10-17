# ej6_histograma_rgb_y_gris.py
# Uso:
#   python ej6_histograma_rgb_y_gris.py ruta/imagen.png [--smooth 5] [--show]
#
# Qué hace:
#   - Calcula y grafica los histogramas de R, G, B y Gris (curvas superpuestas).
#   - Indica la tonalidad (modo 0..255) más repetida en R, G, B y Gris.
#   - Guarda:
#       1) figura combinada RGB+Gris:  *_hist_rgb_gris.png
#       2) imagen en escala de grises: *_GRAY.png     <-- NUEVO
#       3) histograma solo del gris:   *_hist_gray.png <-- EXTRA útil

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import argparse, sys

# -------- utilidades ----------
def pedir_archivo_si_falta():
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk(); root.withdraw()
        path = filedialog.askopenfilename(
            title="Selecciona la imagen (para histogramas RGB y gris)",
            filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg;*.bmp;*.tif;*.tiff"), ("Todos", "*.*")]
        )
        return path or None
    except Exception:
        return None

def hist256(arr_uint8: np.ndarray) -> np.ndarray:
    return np.bincount(arr_uint8.ravel(), minlength=256)

def suavizar(y: np.ndarray, k: int = 0) -> np.ndarray:
    """Suaviza el histograma con media móvil (solo visual)."""
    if k <= 1:
        return y
    k = int(k)
    if k % 2 == 0: k += 1
    pad = k // 2
    ypad = np.pad(y, (pad, pad), mode="edge")
    kernel = np.ones(k) / k
    return np.convolve(ypad, kernel, mode="valid")

# -------- principal ----------
def main():
    ap = argparse.ArgumentParser(description="Histograma R/G/B y Gris (modos + guardado de imagen gris).")
    ap.add_argument("imagen", nargs="?", help="Ruta de la imagen")
    ap.add_argument("--smooth", type=int, default=3, help="Suavizado visual de curvas (p.ej. 5)")
    ap.add_argument("--show", action="store_true", help="Muestra la figura")
    args = ap.parse_args()

    in_path = args.imagen or pedir_archivo_si_falta()
    if not in_path:
        print("Uso: python ej6_histograma_rgb_y_gris.py <ruta> [--smooth 5] [--show]")
        sys.exit(1)
    p = Path(in_path)
    if not p.exists():
        print(f"Archivo no encontrado: {p}")
        sys.exit(1)

    # ---- Cargar y separar ----
    img = Image.open(p).convert("RGB")
    r, g, b = img.split()
    gray = img.convert("L")  # (0.299R + 0.587G + 0.114B) — gris normal

    R = np.array(r, dtype=np.uint8)
    G = np.array(g, dtype=np.uint8)
    B = np.array(b, dtype=np.uint8)
    GR = np.array(gray, dtype=np.uint8)

    # ---- Histogramas ----
    hR, hG, hB, hGR = hist256(R), hist256(G), hist256(B), hist256(GR)
    hsR, hsG, hsB, hsGR = [suavizar(h, args.smooth) for h in (hR, hG, hB, hGR)]

    # ---- Modos (tonalidad más frecuente) ----
    mR, fR = int(np.argmax(hR)), int(hR.max())
    mG, fG = int(np.argmax(hG)), int(hG.max())
    mB, fB = int(np.argmax(hB)), int(hB.max())
    mGR, fGR = int(np.argmax(hGR)), int(hGR.max())

    # ---- (1) Figura combinada RGB + Gris ----
    xs = np.arange(256)
    plt.figure(figsize=(8, 4))
    plt.plot(xs, hsR, color="red",   label=f"Rojo (modo {mR})")
    plt.plot(xs, hsG, color="green", label=f"Verde (modo {mG})")
    plt.plot(xs, hsB, color="blue",  label=f"Azul (modo {mB})")
    plt.plot(xs, hsGR, color="black", linestyle="--", label=f"Gris (modo {mGR})")
    plt.title(p.name)
    plt.xlabel("Valores de píxel (0–255)")
    plt.ylabel("Frecuencia")
    plt.grid(alpha=0.25)
    plt.legend()
    plt.xlim(0, 255)
    plt.tight_layout()
    out_overlay = p.with_name(p.stem + "_hist_rgb_gris.png")
    plt.savefig(out_overlay, dpi=150)
    if args.show:
        plt.show()
    plt.close()

    # ---- (2) Guardar IMAGEN en GRIS ----
    out_gray_img = p.with_name(p.stem + "_GRAY.png")
    gray.save(out_gray_img)

    # ---- (3) (Extra) Histograma solo del GRIS (barras) ----
    plt.figure(figsize=(6, 3))
    plt.bar(np.arange(256), hGR, width=1.0, edgecolor="none", color="black")
    plt.title(f"Histograma (Gris) – modo {mGR}")
    plt.xlabel("Intensidad (0–255)")
    plt.ylabel("Frecuencia")
    plt.xlim(0, 255)
    plt.tight_layout()
    out_gray_hist = p.with_name(p.stem + "_hist_gray.png")
    plt.savefig(out_gray_hist, dpi=150)
    if args.show:
        plt.show()
    plt.close()

    # ---- Consola ----
    print("=== Tonalidad más repetida (modo) ===")
    print(f"Rojo (R):  {mR} (freq={fR})")
    print(f"Verde (G): {mG} (freq={fG})")
    print(f"Azul (B):  {mB} (freq={fB})")
    print(f"Gris:      {mGR} (freq={fGR})")
    print("\nGuardados:")
    print(f"  Figura RGB+Gris: {out_overlay}")
    print(f"  Imagen en Gris:  {out_gray_img}")     # <-- NUEVO
    print(f"  Hist. solo Gris: {out_gray_hist}")    # <-- EXTRA
    print("OK ✔️")

if __name__ == "__main__":
    main()
