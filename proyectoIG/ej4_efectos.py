# ej4_efectos.py
# ---------------------------------------------------------------------
# Qué hace:
#   Compone una "cara" (Lena) dentro de una imagen base usando una
#   PLANTILLA (máscara blanco/negro: blanco=visible, negro=transparente).
#   Suaviza bordes (blur), permite posición, tamaño, rotación y opacidad.
#
# Usos:
#   1) Modo simple (un resultado):
#      python ej4_efectos.py --base base.jpg --face lena.png --mask mask_circulo.png \
#            --pos 240 260 --size 360 360 --blur 2 --rotate 0 --opacity 1.0 --out base_proc.png
#
#   2) Modo asistente (produce los 4 como en la lámina):
#      python ej4_efectos.py --wizard
#      (elige: 4 bases, 1 cara, y las 4 plantillas: círculo, rect, pentágono, corazón)
#
# Tips:
#   - Si tu plantilla está invertida (negro=figura), usa --invert-mask
#   - Ajusta --pos/--size/--blur para matchear mejor la figura
# ---------------------------------------------------------------------

from PIL import Image, ImageOps, ImageFilter
from pathlib import Path
import argparse, sys, math

# ---------- utilidades de diálogo ----------
def pick_file(title, patterns="*.png;*.jpg;*.jpeg;*.bmp;*.tif;*.tiff"):
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk(); root.withdraw()
        return filedialog.askopenfilename(
            title=title,
            filetypes=[("Imágenes", patterns), ("Todos", "*.*")]
        ) or None
    except Exception:
        return None

# ---------- núcleo de composición ----------
def prepare_alpha_from_mask(mask_img: Image.Image, blur_px=2, invert=False, rotate_deg=0):
    a = ImageOps.grayscale(mask_img)
    if invert:
        a = ImageOps.invert(a)
    if rotate_deg:
        a = a.rotate(rotate_deg, resample=Image.BICUBIC, expand=True)
    if blur_px and blur_px > 0:
        a = a.filter(ImageFilter.GaussianBlur(radius=blur_px))
    return a

def resize_to(img: Image.Image, size_wh: tuple[int,int], rotate_deg=0):
    out = img.resize(size_wh, resample=Image.BICUBIC)
    if rotate_deg:
        out = out.rotate(rotate_deg, resample=Image.BICUBIC, expand=True)
    return out

def compose(base: Image.Image, face: Image.Image, alpha: Image.Image,
            pos_xy: tuple[int,int], opacity: float=1.0) -> Image.Image:
    # normaliza opacidad multiplicando alfa
    if opacity < 1.0:
        alpha = alpha.point(lambda v: int(v * max(0.0, min(1.0, opacity))))
    face_rgba = face.convert("RGBA")
    face_rgba.putalpha(alpha)
    out = base.convert("RGBA").copy()
    out.paste(face_rgba, pos_xy, face_rgba)
    return out.convert("RGB")

# ---------- modo simple ----------
def run_single(args):
    base_path = args.base or pick_file("Selecciona la IMAGEN BASE")
    face_path = args.face or pick_file("Selecciona la IMAGEN de la CARA (Lena)")
    mask_path = args.mask or pick_file("Selecciona la PLANTILLA (blanco=figura, negro=fondo)")
    if not (base_path and face_path and mask_path):
        print("Faltan archivos. Vuelve a ejecutar y selecciona base, cara y plantilla.")
        sys.exit(1)

    base_path, face_path, mask_path = Path(base_path), Path(face_path), Path(mask_path)
    base = Image.open(base_path).convert("RGB")
    face = Image.open(face_path).convert("RGB")
    mask = Image.open(mask_path)

    # tamaño: si no se pasa, usamos tamaño de la plantilla
    if args.size:
        W, H = map(int, args.size)
    else:
        W, H = mask.size

    # redimensionar y rotar
    face_r = resize_to(face, (W, H), rotate_deg=args.rotate)
    mask_r = resize_to(mask, (W, H), rotate_deg=args.rotate)

    # alfa desde plantilla
    alpha = prepare_alpha_from_mask(mask_r, blur_px=args.blur, invert=args.invert_mask)

    # posición: por defecto centrado
    if args.pos:
        x, y = map(int, args.pos)
    else:
        x = (base.width  - face_r.width ) // 2
        y = (base.height - face_r.height) // 2

    out_img = compose(base, face_r, alpha, (x, y), opacity=args.opacity)

    out_path = Path(args.out) if args.out else base_path.with_name(base_path.stem + "_comp.png")
    out_img.save(out_path)
    print("OK ->", out_path)

# ---------- modo asistente (produce los 4 de la lámina) ----------
def run_wizard(args):
    print("Asistente: generará 4 composiciones (círculo, rect, pentágono, corazón).")

    # Seleccionar la cara una vez
    face_path = args.face or pick_file("Selecciona la IMAGEN de la CARA (Lena)")
    if not face_path: print("Sin cara."); sys.exit(1)
    face = Image.open(face_path).convert("RGB")

    # Seleccionar las 4 bases
    bases = []
    labels = ["BASE 1 (círculo)", "BASE 2 (rectángulo)", "BASE 3 (pentágono)", "BASE 4 (corazón)"]
    for lab in labels:
        p = pick_file(f"Selecciona {lab}")
        if not p: print("Faltó una base."); sys.exit(1)
        bases.append(Path(p))

    # Seleccionar las 4 plantillas
    masks = []
    mlabels = ["PLANTILLA círculo", "PLANTILLA rectángulo", "PLANTILLA pentágono", "PLANTILLA corazón"]
    for ml in mlabels:
        pm = pick_file(f"Selecciona {ml}")
        if not pm: print("Faltó una plantilla."); sys.exit(1)
        masks.append(Path(pm))

    # Parámetros por defecto (ajusta si quieres)
    # tamaño relativo a la base (ancho_face = k * ancho_base)
    k_rel = [0.33, 0.38, 0.36, 0.38]  # puedes afinar estos 4 coeficientes
    blur   = [2, 2, 2, 2]
    rotate = [0, 0, 0, 0]
    opacity= [1.0, 1.0, 1.0, 1.0]

    for i, (base_path, mask_path) in enumerate(zip(bases, masks), start=1):
        base = Image.open(base_path).convert("RGB")
        mask = Image.open(mask_path)

        # tamaño desde proporción del ancho de la base manteniendo relación del mask
        target_W = int(base.width * k_rel[i-1])
        ratio = target_W / mask.width
        target_H = max(1, int(mask.height * ratio))

        # redimensionar cara y máscara, aplicar rotación y blur
        face_r = resize_to(face, (target_W, target_H), rotate_deg=rotate[i-1])
        mask_r = resize_to(mask, (target_W, target_H), rotate_deg=rotate[i-1])
        alpha  = prepare_alpha_from_mask(mask_r, blur_px=blur[i-1], invert=args.invert_mask)

        # posición centrada (puedes desplazar un poco para cuadrar mejor)
        x = (base.width  - face_r.width ) // 2
        y = (base.height - face_r.height) // 2

        out_img = compose(base, face_r, alpha, (x, y), opacity=opacity[i-1])
        out_path = base_path.with_name(base_path.stem + f"_proc_{i}.png")
        out_img.save(out_path)
        print(f"OK {i} ->", out_path)

# ---------- main ----------
def main():
    ap = argparse.ArgumentParser(description="Ej4: Composición con plantillas (círculo/rect/pentágono/corazón).")
    ap.add_argument("--base", help="Imagen base (modo simple).")
    ap.add_argument("--face", help="Imagen de la cara (Lena).")
    ap.add_argument("--mask", help="Plantilla (blanco=figura; negro=fondo).")
    ap.add_argument("--pos",  nargs=2, metavar=("X","Y"), help="Posición (x,y) donde pegar (modo simple).")
    ap.add_argument("--size", nargs=2, metavar=("W","H"), help="Tamaño (w,h) de cara/máscara (modo simple).")
    ap.add_argument("--blur", type=int, default=2, help="Feather (px) del borde.")
    ap.add_argument("--rotate", type=float, default=0.0, help="Rotación (grados).")
    ap.add_argument("--opacity", type=float, default=1.0, help="Opacidad 0..1 de la cara.")
    ap.add_argument("--invert-mask", action="store_true", help="Invierte la plantilla.")
    ap.add_argument("--out", help="Archivo de salida (modo simple).")
    ap.add_argument("--wizard", action="store_true", help="Asistente para generar las 4 composiciones.")
    args = ap.parse_args()

    if args.wizard:
        run_wizard(args)
    else:
        run_single(args)

if __name__ == "__main__":
    main()
