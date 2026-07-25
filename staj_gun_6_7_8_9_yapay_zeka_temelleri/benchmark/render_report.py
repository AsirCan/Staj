"""benchmark_raporu.txt'yi terminal görünümlü bir PNG'ye dönüştürür
(staj defterine yapıştırmak için 'ekran görüntüsü' gibi bir görsel)."""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
txt = open(os.path.join(HERE, "benchmark_raporu.txt"), encoding="utf-8").read()
lines = txt.rstrip("\n").split("\n")

font = None
for p in [r"C:\Windows\Fonts\consola.ttf", r"C:\Windows\Fonts\cour.ttf"]:
    if os.path.exists(p):
        font = ImageFont.truetype(p, 19)
        break
if font is None:
    font = ImageFont.load_default()

pad = 28
tmp = ImageDraw.Draw(Image.new("RGB", (10, 10)))
ascent, descent = font.getmetrics()
lh = ascent + descent + 5
maxw = max((tmp.textlength(l, font=font) for l in lines), default=100)
W, H = int(maxw) + pad * 2, lh * len(lines) + pad * 2

img = Image.new("RGB", (W, H), (13, 17, 23))
draw = ImageDraw.Draw(img)
y = pad
for l in lines:
    color = (220, 223, 228)
    if set(l.strip()) == {"="}:
        color = (88, 166, 255)
    elif "PyTorch — GPU" in l or "En hızlı" in l:
        color = (63, 185, 80)
    elif l.strip().startswith("Not:") or "CPU — Windows" in l:
        color = (139, 148, 158)
    draw.text((pad, y), l, font=font, fill=color)
    y += lh

out = os.path.join(HERE, "benchmark_raporu.png")
img.save(out)
print("kaydedildi:", out, img.size)
