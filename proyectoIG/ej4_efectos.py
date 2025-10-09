# ej4_efectos.py
# Uso: python ej4_efectos.py ruta/imagen.png
from PIL import Image, ImageOps, ImageEnhance
import sys
from pathlib import Path

def pedir_archivo_si_falta():
    # Intenta abrir un diálogo si no hay argumento
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk(); root.withdraw()
        path = filedialog.askopenfilename(
            title="Selecciona la imagen (para aplicar efectos)",
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
            print("Uso: python ej4_efectos.py <ruta_de_imagen>")
            sys.exit(1)

    p = Path(in_path)
    if not p.exists():
        print(f"Archivo no encontrado: {p}")
        sys.exit(1)

    # Cargar imagen
    img = Image.open(p).convert("RGB")

    # Salidas deterministas
    out_neg   = p.with_name(p.stem + "_negativo.png")
    out_fliph = p.with_name(p.stem + "_flipH.png")
    out_flipv = p.with_name(p.stem + "_flipV.png")
    out_contr = p.with_name(p.stem + "_contraste+.png")

    # Aplicar efectos
    ImageOps.invert(img).save(out_neg)
    ImageOps.mirror(img).save(out_fliph)
    ImageOps.flip(img).save(out_flipv)
    ImageEnhance.Contrast(img).enhance(1.5).save(out_contr)

    print("Efectos generados y guardados:")
    print(f"  Negativo:   {out_neg}")
    print(f"  Espejo H:   {out_fliph}")
    print(f"  Espejo V:   {out_flipv}")
    print(f"  Contraste+: {out_contr}")

if __name__ == "__main__":
    main()
