# ej5_area_planes_rgb.py
# Uso: python ej5_area_planes_rgb.py ruta/imagen.png [umbral]
from PIL import Image
import numpy as np
import sys
from pathlib import Path

def pedir_archivo_si_falta():
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk(); root.withdraw()
        path = filedialog.askopenfilename(
            title="Selecciona la imagen (para áreas por canal RGB)",
            filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg;*.bmp;*.tif;*.tiff"), ("Todos", "*.*")]
        )
        return path or None
    except Exception:
        return None

def main():
    # Obtener ruta y umbral
    if len(sys.argv) >= 2:
        in_path = sys.argv[1]
        if len(sys.argv) >= 3:
            try:
                thresh = int(sys.argv[2])
            except ValueError:
                print(f"Advertencia: umbral inválido '{sys.argv[2]}', usando 128.")
                thresh = 128
        else:
            thresh = 128
    else:
        in_path = pedir_archivo_si_falta()
        if not in_path:
            print("Uso: python ej5_area_planes_rgb.py <ruta_de_imagen> [umbral]")
            sys.exit(1)
        thresh = 128

    p = Path(in_path)
    if not p.exists():
        print(f"Archivo no encontrado: {p}")
        sys.exit(1)

    img = Image.open(p).convert("RGB")
    r, g, b = img.split()
    R = np.array(r); G = np.array(g); B = np.array(b)

    # Áreas por canal (>= umbral)
    area_R = int((R >= thresh).sum())
    area_G = int((G >= thresh).sum())
    area_B = int((B >= thresh).sum())
    total  = R.size

    print(f"Imagen: {p.name}  |  Dimensión: {img.width}x{img.height}  |  Umbral: {thresh}")
    print(f"Área R (px): {area_R}  ({area_R/total:.2%})")
    print(f"Área G (px): {area_G}  ({area_G/total:.2%})")
    print(f"Área B (px): {area_B}  ({area_B/total:.2%})")
    print("Todo OK ✔️")

if __name__ == "__main__":
    main()
