"""
turns any photo into something e-paper can show

the display only has 6 colors at 600x400,
so we crop the photo to fit, then use floyd-steinberg dithering to fake the
in between colors

preview on pc: python dither.py photo.jpg preview.png
"""
import sys
from PIL import Image, ImageOps

WIDTH, HEIGHT = 600, 400

PALETTE = [
    (0, 0, 0),        # black
    (255, 255, 255),  # white
    (0, 255, 0),      # green
    (0, 0, 255),      # blue
    (255, 0, 0),      # red
    (255, 255, 0),    # yellow
]


def _palette_image():
    pal = Image.new("P", (1, 1))
    flat = [c for rgb in PALETTE for c in rgb]
    flat += [0] * (768 - len(flat))
    pal.putpalette(flat)
    return pal


def prepare(img):
    img = ImageOps.exif_transpose(img).convert("RGB")
    img = ImageOps.fit(img, (WIDTH, HEIGHT), Image.LANCZOS)
    img = img.quantize(palette=_palette_image(), dither=Image.FLOYDSTEINBERG)
    return img.convert("RGB")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: python dither.py input.jpg output.png")
    prepare(Image.open(sys.argv[1])).save(sys.argv[2])
    print("saved", sys.argv[2])