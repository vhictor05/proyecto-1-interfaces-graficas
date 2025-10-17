# ej7_aplicar_color.py
# Uso:
#   python ej7_aplicar_color.py ruta/figura.png [--show]
# Opcional (ajustes del azul):
#   --dark  r g b    # color para las sombras (por defecto 0 20 90)
#   --light r g b    # color para las luces  (por defecto 140 190 255)

from PIL import Image, ImageOps
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import argparse, sys

def pedir_archivo_si_falta():
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk(); root.withdraw()
        return filedialog.askopenfilename(
            title="Selecciona la figura (gris + coloreado azul)",
            filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg;*.bmp;*.tif;*.tiff"), ("Todos", "*.*")]
        ) or None
    except Exception:
        return None

def colorizar_azul(img_gray: Image.Image, dark=(0,20,90), light=(140,190,255)) -> Image.Image:
    """
    Mapea el gris a azul usando ImageOps.colorize:
    - 'dark' = color para valores oscuros (0)
    - 'light' = color para valores claros (255)
    """
    return ImageOps.colorize(img_gray, black=tuple(dark), white=tuple(light))

def main():
    ap = argparse.ArgumentParser(description="Ej7: convertir a gris y colorear en azul (como la guía).")
    ap.add_argument("imagen", nargs="?", help="Ruta de la imagen de entrada")
    ap.add_argument("--show", action="store_true", help="Mostrar figura comparativa en pantalla")
    ap.add_argument("--dark",  nargs=3, type=int, metavar=("R","G","B"), default=(0,20,90),
                    help="Color para sombras (0..255 0..255 0..255)")
    ap.add_argument("--light", nargs=3, type=int, metavar=("R","G","B"), default=(140,190,255),
                    help="Color para luces (0..255 0..255 0..255)")
    args = ap.parse_args()

    in_path = args.imagen or pedir_archivo_si_falta()
    if not in_path:
        print("Uso: python ej7_aplicar_color.py <ruta_de_imagen> [--show] [--dark r g b] [--light r g b]")
        sys.exit(1)

    p = Path(in_path)
    if not p.exists():
        print(f"Archivo no encontrado: {p}")
        sys.exit(1)

    # 1) Abrir y convertir a gris
    img = Image.open(p).convert("RGB")
    gray = img.convert("L")  # gris normal (0.299R + 0.587G + 0.114B)
    out_gray = p.with_name(p.stem + "_GRAY.png")
    gray.save(out_gray)

    # 2) Colorear en azul (como la lámina)
    colored = colorizar_azul(gray, dark=args.dark, light=args.light)
    out_col = p.with_name(p.stem + "_color_azul.png")
    colored.save(out_col)

    # 3) Figura comparativa como en el enunciado
    fig, axs = plt.subplots(1, 2, figsize=(9.5, 3.8))
    axs[0].imshow(np.array(gray), cmap="gray")
    axs[0].set_title("[ Figura original en Gris ]")
    axs[1].imshow(np.array(colored))
    axs[1].set_title("[ Figura coloreada ]")
    for ax in axs: ax.axis("off")
    plt.tight_layout()
    out_fig = p.with_name(p.stem + "_comparativa.png")
    plt.savefig(out_fig, dpi=150)
    if args.show:
        plt.show()
    plt.close(fig)

    print("Listo ✅")
    print(f"  Gris:        {out_gray}")
    print(f"  Color azul:  {out_col}")
    print(f"  Comparativa: {out_fig}")

if __name__ == "__main__":
    main()
