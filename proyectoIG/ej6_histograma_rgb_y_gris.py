# ej6_histograma_rgb_y_gris.py
# Uso: python ej6_histograma_rgb_y_gris.py ruta/imagen.png
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import sys
from pathlib import Path

def pedir_archivo_si_falta():
    # Intenta abrir un diálogo si no hay argumento
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk(); root.withdraw()
        path = filedialog.askopenfilename(
            title="Selecciona la imagen (para histogramas RGB y Gris)",
            filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg;*.bmp;*.tif;*.tiff"), ("Todos", "*.*")]
        )
        return path or None
    except Exception:
        return None

def modo_mas_repetido(arr: np.ndarray):
    """Devuelve (valor, frecuencia) del bin más frecuente en 0..255."""
    counts = np.bincount(arr.flatten(), minlength=256)
    val = int(counts.argmax())
    return val, int(counts[val])

def guardar_histograma(counts: np.ndarray, titulo: str, out_path: Path):
    if counts.shape[0] != 256:
        print(f"[ERROR] Histograma inesperado ({counts.shape[0]} bins). Se esperaban 256.")
        return
    xs = np.arange(256)
    plt.figure()
    plt.title(titulo)
    plt.xlabel("Intensidad")
    plt.ylabel("Frecuencia")
    plt.bar(xs, counts, width=1.0)
    plt.xlim(0, 255)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()

def main():
    # Obtener ruta
    if len(sys.argv) >= 2:
        in_path = sys.argv[1]
    else:
        in_path = pedir_archivo_si_falta()
        if not in_path:
            print("Uso: python ej6_histograma_rgb_y_gris.py <ruta_de_imagen>")
            sys.exit(1)

    p = Path(in_path)
    if not p.exists():
        print(f"Archivo no encontrado: {p}")
        sys.exit(1)

    # Cargar imagen y separar canales
    img = Image.open(p).convert("RGB")
    r, g, b = img.split()
    R = np.array(r); G = np.array(g); B = np.array(b)
    GR = np.array(img.convert("L"))

    # Histogramas (256 bins)
    hist_R  = np.bincount(R.flatten(),  minlength=256)
    hist_G  = np.bincount(G.flatten(),  minlength=256)
    hist_B  = np.bincount(B.flatten(),  minlength=256)
    hist_GR = np.bincount(GR.flatten(), minlength=256)

    # Tonalidades más repetidas
    tR, fR = modo_mas_repetido(R)
    tG, fG = modo_mas_repetido(G)
    tB, fB = modo_mas_repetido(B)
    tGr, fGr = modo_mas_repetido(GR)
    print(f"Más repetido - R:{tR}({fR})  G:{tG}({fG})  B:{tB}({fB})  Gris:{tGr}({fGr})")

    # Guardar figuras
    out_R  = p.with_name(p.stem + "_hist_R.png")
    out_G  = p.with_name(p.stem + "_hist_G.png")
    out_B  = p.with_name(p.stem + "_hist_B.png")
    out_GR = p.with_name(p.stem + "_hist_gray.png")

    guardar_histograma(hist_R,  "Histograma R",    out_R)
    guardar_histograma(hist_G,  "Histograma G",    out_G)
    guardar_histograma(hist_B,  "Histograma B",    out_B)
    guardar_histograma(hist_GR, "Histograma Gris", out_GR)

    print("Histogramas guardados:")
    print(f"  R:    {out_R}")
    print(f"  G:    {out_G}")
    print(f"  B:    {out_B}")
    print(f"  Gris: {out_GR}")
    print("Conclusión: el histograma en gris condensa la distribución global; "
          "picos estrechos → baja variabilidad; distribución amplia → mayor contraste.")

if __name__ == "__main__":
    main()
