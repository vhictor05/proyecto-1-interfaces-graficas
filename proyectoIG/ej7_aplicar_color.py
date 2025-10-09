# ej7_aplicar_color.py
# Uso: python ej7_aplicar_color.py ruta/figura.png  (genera versiones con tintes)
from PIL import Image, ImageOps
import sys
from pathlib import Path

def pedir_archivo_si_falta():
    # Intenta abrir un diálogo si no hay argumento
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
    color en (R,G,B) 0..255; aplica tinte multiplicativo sobre la versión en gris.
    """
    g = ImageOps.grayscale(img).convert("RGB")
    r, gc, b = g.split()
    R = r.point(lambda v: int(v * color[0] / 255.0))
    G = gc.point(lambda v: int(v * color[1] / 255.0))
    B = b.point(lambda v: int(v * color[2] / 255.0))
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

    img = Image.open(p).convert("RGB")

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
        out_img = aplicar_tinte(img, c)
        out_path = p.with_name(p.stem + f"_tinte_{nombre}.png")
        out_img.save(out_path)
        generados.append(out_path)

    print("Tintes aplicados y guardados:")
    for g in generados:
        print(f"  {g}")

if __name__ == "__main__":
    main()
