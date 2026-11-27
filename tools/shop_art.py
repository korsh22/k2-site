# -*- coding: utf-8 -*-
"""Картинки-заглушки для магазина (пока нет фото товаров): плоские иллюстрации в цветах сайта.
Для каждого товара три файла в site/assets/img/shop/: <id>.svg (карточка 4:5), <id>-a4.svg (обложка А4), <id>-h.svg (шапка 4:3).
Запуск: python tools/shop_art.py. Перед запуском магазина заменить фотографиями товаров."""
import io, os

OUT = os.path.join(os.path.dirname(__file__), '..', 'site', 'assets', 'img', 'shop')
G, RED, STONE, STONE2, W = '#2D2D2D', '#D9493E', '#F1EFEC', '#E4E0DB', '#FFFFFF'
LOGO = '<text x="0" y="0" text-anchor="middle" font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="%d" fill="%s">К2</text>'

def logo(x, y, size, color):
    return '<g transform="translate(%s %s)">%s</g>' % (x, y, LOGO % (size, color))

# Рисунок товара в поле 200×200 (центр 100,100)
ART = {
    'futbolka-k2': lambda: (
        '<path d="M62 42 L86 30 Q100 44 114 30 L138 42 L166 68 L148 88 L136 78 L136 172 L64 172 L64 78 L52 88 L34 68 Z" fill="%s"/>'
        '<path d="M86 30 Q100 44 114 30" fill="none" stroke="#000" stroke-opacity=".25" stroke-width="3"/>' % G + logo(100, 118, 30, W)),
    'hudi-k2': lambda: (
        '<path d="M58 52 L80 38 Q100 20 120 38 L142 52 L170 120 L150 128 L138 96 L138 176 L62 176 L62 96 L50 128 L30 120 Z" fill="%s"/>'
        '<path d="M80 38 Q100 66 120 38" fill="%s"/><rect x="76" y="140" width="48" height="22" rx="6" fill="#000" fill-opacity=".18"/>'
        '<path d="M94 58 v22 M106 58 v22" stroke="%s" stroke-width="2.5"/>' % (G, '#1f1f1f', W) + logo(100, 124, 24, W)),
    'meshochek-dlya-magnezii': lambda: (
        '<rect x="62" y="58" width="76" height="110" rx="16" fill="%s"/><rect x="56" y="50" width="88" height="22" rx="8" fill="%s"/>'
        '<path d="M100 50 C92 34 112 30 108 44" fill="none" stroke="%s" stroke-width="3"/><circle cx="112" cy="42" r="5" fill="%s"/>'
        '<rect x="132" y="96" width="18" height="30" rx="5" fill="none" stroke="%s" stroke-width="4"/>' % (RED, G, G, G, G) + logo(100, 126, 28, W)),
    'butylka-k2': lambda: (
        '<rect x="80" y="22" width="40" height="22" rx="6" fill="%s"/><path d="M76 50 Q76 44 84 44 L116 44 Q124 44 124 50 L128 66 L128 170 Q128 180 118 180 L82 180 Q72 180 72 170 L72 66 Z" fill="%s"/>'
        '<rect x="72" y="92" width="56" height="46" fill="%s"/>' % (G, W, RED) + logo(100, 126, 24, W) +
        '<path d="M76 50 Q76 44 84 44 L116 44 Q124 44 124 50 L128 66 L128 170 Q128 180 118 180 L82 180 Q72 180 72 170 L72 66 Z" fill="none" stroke="%s" stroke-width="3"/>' % G),
    'magneziya': lambda: (
        '<path d="M58 60 L142 60 L150 170 Q150 178 142 178 L58 178 Q50 178 50 170 Z" fill="%s"/><rect x="58" y="46" width="84" height="18" rx="4" fill="%s"/>'
        '<rect x="66" y="96" width="68" height="44" rx="6" fill="%s"/>' % (W, G, STONE2) + logo(100, 126, 22, G) +
        '<path d="M58 60 L142 60 L150 170 Q150 178 142 178 L58 178 Q50 178 50 170 Z" fill="none" stroke="%s" stroke-width="3"/>'
        '<text x="100" y="160" text-anchor="middle" font-family="Arial, sans-serif" font-weight="700" font-size="12" fill="%s">CHALK 200 g</text>' % (G, G)),
    'shoper-k2': lambda: (
        '<path d="M80 64 Q80 28 100 28 Q120 28 120 64" fill="none" stroke="%s" stroke-width="7"/>'
        '<rect x="52" y="62" width="96" height="118" rx="6" fill="%s" stroke="%s" stroke-width="3"/>' % (G, W, G) + logo(100, 132, 36, RED)),
}

def svg(pid, w, h, scale):
    s = scale; x = (w - 200 * s) / 2; y = (h - 200 * s) / 2
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d">'
            '<rect width="%d" height="%d" fill="%s"/><circle cx="%d" cy="%d" r="%d" fill="%s"/>'
            '<g transform="translate(%.1f %.1f) scale(%.2f)">%s</g></svg>') % (
        w, h, w, h, w, h, STONE, w / 2, h / 2, min(w, h) * .36, STONE2, x, y, s, ART[pid]())

os.makedirs(OUT, exist_ok=True)
for pid in ART:
    for suf, (w, h, s) in {'': (400, 500, 1.85), '-a4': (420, 594, 1.95), '-h': (800, 600, 2.6)}.items():
        io.open(os.path.join(OUT, pid + suf + '.svg'), 'w', encoding='utf-8').write(svg(pid, w, h, s))
print('ok', len(ART) * 3)
