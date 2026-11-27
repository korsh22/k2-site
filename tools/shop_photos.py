# -*- coding: utf-8 -*-
"""Фото товаров магазина → три кадра для сайта (site/assets/img/shop/):
<id>.jpg (карточка 4:5), <id>-a4.jpg (обложка А4), <id>-h.jpg (шапка страницы 4:5).
Предмет на однотонном фоне: обрезаем по предмету и дополняем тем же цветом фона до нужных пропорций (без обрезки предмета).
Фото с градиентным фоном (модель в футболке): кадрируем по центру. Запуск: python tools/shop_photos.py <папка с исходниками>"""
import os, sys
from PIL import Image, ImageChops

SRC = sys.argv[1] if len(sys.argv) > 1 else '.'
OUT = os.path.join(os.path.dirname(__file__), '..', 'site', 'assets', 'img', 'shop')
FRAMES = {'': (800, 1000), '-a4': (840, 1188), '-h': (1000, 1250)}
PHOTOS = {  # id товара: (файл, способ)
    'hudi-k2': ('37.webp', 'pad'),
    'futbolka-k2': ('38.webp', 'crop'),
    'meshochek-dlya-magnezii': ('39.webp', 'pad'),
    'butylka-k2': ('40.png', 'pad'),
    'magneziya': ('41.webp', 'crop'),
    'shoper-k2': ('43.webp', 'pad'),
}

def bbox(im, bg, tol=18):
    diff = ImageChops.difference(im, Image.new('RGB', im.size, bg)).convert('L').point(lambda v: 255 if v > tol else 0)
    return diff.getbbox() or (0, 0) + im.size

def pad(im, w, h, fill=0.78):
    bg = im.getpixel((3, 3))
    obj = im.crop(bbox(im, bg))
    s = min(w * fill / obj.width, h * fill / obj.height)
    obj = obj.resize((round(obj.width * s), round(obj.height * s)), Image.LANCZOS)
    out = Image.new('RGB', (w, h), bg)
    out.paste(obj, ((w - obj.width) // 2, (h - obj.height) // 2))
    return out

def crop(im, w, h):
    r = w / h
    if im.width / im.height > r:
        cw = round(im.height * r); x = (im.width - cw) // 2; im = im.crop((x, 0, x + cw, im.height))
    else:
        ch = round(im.width / r); y = (im.height - ch) // 2; im = im.crop((0, y, im.width, y + ch))
    return im.resize((w, h), Image.LANCZOS)

os.makedirs(OUT, exist_ok=True)
for pid, (f, how) in PHOTOS.items():
    im = Image.open(os.path.join(SRC, f)).convert('RGB')
    for suf, (w, h) in FRAMES.items():
        (pad(im, w, h) if how == 'pad' else crop(im, w, h)).save(os.path.join(OUT, pid + suf + '.jpg'), quality=86, optimize=True, progressive=True)
print('ok', len(PHOTOS) * len(FRAMES))
