# ej7_aplicar_color.py
# Uso: python ej7_aplicar_color.py ruta/figura.png
# Genera versiones de la imagen con distintos tintes de color.

from PIL import Image, ImageOps
import sys
from pathlib import Path

def pedir_archivo_si_falta():
    """Abre un diálogo si no se pasa la ruta por argumento."""
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk(); root.withdraw()
        path = filedialog.askopenfilename(
            title="Selecciona la figura (para aplicar tintes)",
            filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg;*.bmp;*.tif;*.tiff"), ("Todos", "*.*")]
        )
        return path or None
    except Exception:
        return None

def aplicar_tinte(img, color):
    """
    color = (R,G,B) 0–255.
    Aplica un tinte multiplicativo sobre la versión en gris usando tablas LUT.
    """
    g = ImageOps.grayscale(img).convert("RGB")
    r, gc, b = g.split()
    lutR = [int(v * color[0] / 255) for v in range(256)]
    lutG = [int(v * color[1] / 255) for v in range(256)]
    lutB = [int(v * color[2] / 255) for v in range(256)]
    R = r.point(lutR); G = gc.point(lutG); B = b.point(lutB)
    return Image.merge("RGB", (R, G, B))

def main():
    # Obtener ruta
    if len(sys.argv) >= 2:
        in_path = sys.argv[1]
    else:
        in_path = pedir_archivo_si_falta()
        if not in_path:
            print("Uso: python ej7_aplicar_color.py <ruta_de_imagen>")
            sys.exit(1)

    p = Path(in_path)
    if not p.exists():
        print(f"Archivo no encontrado: {p}")
        sys.exit(1)

    img = Image.open(p)
    base = img.convert("RGB")
    alpha = img.getchannel("A") if img.mode == "RGBA" else None

    colores = {
        "rojo":     (255, 80,  80),
        "verde":    ( 80,255,  80),
        "azul":     ( 80, 80, 255),
        "magenta":  (255, 80, 255),
        "cian":     ( 80,255, 255),
        "amarillo": (255,255,  80),
    }

    generados = []
    for nombre, c in colores.items():
        out_img = aplicar_tinte(base, c)
        if alpha is not None:
            out_img = out_img.convert("RGBA")
            out_img.putalpha(alpha)
        out_path = p.with_name(p.stem + f"_tinte_{nombre}.png")
        out_img.save(out_path)
        generados.append(out_path)

    print("Tintes aplicados y guardados:")
    for g in generados:
        print(f"  {g}")
    print("Todo OK ✔️")

if __name__ == "__main__":
    main()
