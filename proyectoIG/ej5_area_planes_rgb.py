# ej5_area_planes_rgb.py
# Uso:
#   python ej5_area_planes_rgb.py ruta/imagen.png [umbral] [--show]
#
# Hace:
#   - Separa los planos R, G y B (en color sobre fondo negro) y los guarda.
#   - Calcula el área ocupada (px >= umbral) en cada plano.
#   - Genera una figura comparativa: [Imagen original] [Plano Red] [Plano Green] [Plano Blue].

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
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
    # === Obtener ruta y umbral ===
    show = False
    if len(sys.argv) >= 2 and sys.argv[1] not in ("-h", "--help"):
        in_path = sys.argv[1]
        # umbral opcional
        if len(sys.argv) >= 3 and sys.argv[2] not in ("--show",):
            try:
                thresh = int(sys.argv[2])
            except ValueError:
                print(f"Advertencia: umbral inválido '{sys.argv[2]}', usando 128.")
                thresh = 128
        else:
            thresh = 128
        # bandera --show en cualquier posición
        show = ("--show" in sys.argv[2:]) or ("--show" in sys.argv[1:2])
    else:
        in_path = pedir_archivo_si_falta()
        if not in_path:
            print("Uso: python ej5_area_planes_rgb.py <ruta_de_imagen> [umbral] [--show]")
            sys.exit(1)
        thresh = 128

    p = Path(in_path)
    if not p.exists():
        print(f"Archivo no encontrado: {p}")
        sys.exit(1)

    # === Cargar y separar ===
    img = Image.open(p).convert("RGB")
    r, g, b = img.split()
    R = np.array(r); G = np.array(g); B = np.array(b)
    h, w = R.shape
    total = R.size

    # === Áreas por canal (>= umbral) ===
    area_R = int((R >= thresh).sum())
    area_G = int((G >= thresh).sum())
    area_B = int((B >= thresh).sum())

    # === Planos coloreados sobre negro ===
    zero = Image.new("L", (w, h), 0)
    plane_R = Image.merge("RGB", (r, zero, zero))
    plane_G = Image.merge("RGB", (zero, g, zero))
    plane_B = Image.merge("RGB", (zero, zero, b))

    # Guardar planos
    out_R  = p.with_name(p.stem + "_plane_R.png")
    out_G  = p.with_name(p.stem + "_plane_G.png")
    out_B  = p.with_name(p.stem + "_plane_B.png")
    plane_R.save(out_R); plane_G.save(out_G); plane_B.save(out_B)

    # === Figura comparativa al estilo de la guía ===
    fig, axs = plt.subplots(1, 4, figsize=(12, 3.2))
    axs[0].imshow(np.array(img));     axs[0].set_title("[ Imagen original ]")
    axs[1].imshow(np.array(plane_R)); axs[1].set_title("[ Plano Red ]")
    axs[2].imshow(np.array(plane_G)); axs[2].set_title("[ Plano Green ]")
    axs[3].imshow(np.array(plane_B)); axs[3].set_title("[ Plano Blue ]")
    for ax in axs: ax.axis("off")

    # Subtítulo con áreas
    fig.suptitle(
        f"Umbral={thresh} | Áreas (px y %): "
        f"R={area_R} ({area_R/total:.2%}), "
        f"G={area_G} ({area_G/total:.2%}), "
        f"B={area_B} ({area_B/total:.2%})",
        y=0.02, fontsize=9
    )
    plt.tight_layout(rect=[0, 0.06, 1, 1])

    out_fig = p.with_name(p.stem + "_fig_planes.png")
    fig.savefig(out_fig, dpi=150)
    if show:
        plt.show()
    plt.close(fig)

    # === Consola ===
    print(f"Imagen: {p.name}  |  Dimensión: {w}x{h}  |  Umbral: {thresh}")
    print(f"Área R (px): {area_R}  ({area_R/total:.2%})")
    print(f"Área G (px): {area_G}  ({area_G/total:.2%})")
    print(f"Área B (px): {area_B}  ({area_B/total:.2%})")
    print("Guardados:")
    print(f"  Plano R:  {out_R}")
    print(f"  Plano G:  {out_G}")
    print(f"  Plano B:  {out_B}")
    print(f"  Figura:   {out_fig}")
    print("Todo OK ✔️")

if __name__ == "__main__":
    main()
