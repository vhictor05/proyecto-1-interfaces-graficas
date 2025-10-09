# ej2_histograma_pil.py
# Uso: python ej2_histograma_pil.py ruta/imagen_a.png
from PIL import Image
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
            title="Selecciona la imagen (para histograma en gris)",
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
            print("Uso: python ej2_histograma_pil.py <ruta_de_imagen>")
            sys.exit(1)

    p = Path(in_path)
    if not p.exists():
        print(f"Archivo no encontrado: {p}")
        sys.exit(1)

    # Cargar en gris y obtener histograma (PIL)
    img = Image.open(p).convert("L")
    hist = img.histogram()  # 256 bins

    # Graficar y guardar
    plt.figure()
    plt.title("Histograma (escala de grises)")
    plt.xlabel("Intensidad")
    plt.ylabel("Frecuencia")
    plt.plot(hist)
    plt.xlim(0, 255)
    plt.tight_layout()

    out = p.with_name(p.stem + "_hist_gris.png")
    plt.savefig(out, dpi=150)
    plt.close()
    print(f"Histograma guardado en {out}")

if __name__ == "__main__":
    main()
