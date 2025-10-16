# ej3_planos_y_gris.py
# Uso: python ej3_planos_y_gris.py ruta/imagen_b.png
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import sys
from pathlib import Path

def pedir_archivo_si_falta():
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk(); root.withdraw()
        path = filedialog.askopenfilename(
            title="Selecciona la imagen (para separar R, G, B y Gris)",
            filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg;*.bmp;*.tif;*.tiff"), ("Todos", "*.*")]
        )
        return path or None
    except Exception:
        return None

def main():
    if len(sys.argv) >= 2:
        in_path = sys.argv[1]
    else:
        in_path = pedir_archivo_si_falta()
        if not in_path:
            print("Uso: python ej3_planos_y_gris.py <ruta_de_imagen>")
            sys.exit(1)

    p = Path(in_path)
    if not p.exists():
        print(f"Archivo no encontrado: {p}")
        sys.exit(1)

    img = Image.open(p).convert("RGB")
    r, g, b = img.split()
    gray = img.convert("L")

    out_r = p.with_name(p.stem + "_R.png")
    out_g = p.with_name(p.stem + "_G.png")
    out_b = p.with_name(p.stem + "_B.png")
    out_gray = p.with_name(p.stem + "_GRAY.png")
    r.save(out_r); g.save(out_g); b.save(out_b); gray.save(out_gray)

    # Graficar planos
    fig, axs = plt.subplots(1, 4, figsize=(10, 3))
    axs[0].imshow(np.array(r), cmap="Reds");   axs[0].set_title("R")
    axs[1].imshow(np.array(g), cmap="Greens"); axs[1].set_title("G")
    axs[2].imshow(np.array(b), cmap="Blues");  axs[2].set_title("B")
    axs[3].imshow(np.array(gray), cmap="gray");axs[3].set_title("Gris")
    for ax in axs: ax.axis("off")
    plt.tight_layout()

    out_fig = p.with_name(p.stem + "_planos.png")
    plt.savefig(out_fig, dpi=150)
    plt.close(fig)

    print("Planos y gris guardados:")
    print(f"  R:    {out_r}")
    print(f"  G:    {out_g}")
    print(f"  B:    {out_b}")
    print(f"  GRAY: {out_gray}")
    print(f"Figura comparativa: {out_fig}")
    print("Todo OK ✔️")

if __name__ == "__main__":
    main()
