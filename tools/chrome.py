# -*- coding: utf-8 -*-
"""Общие части всех страниц К2: шапка, мобильное меню, поиск, подвал, загруженность, окно заявки, галерея.
Берутся из site/index.html (она — источник правды), ссылки переписываются под глубину страницы.
"""
import io, os, re

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'site'))
MAIN = io.open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
VER = re.search(r'style\.css\?v=(\d+)', MAIN).group(1)


def block(start, end):
    a = MAIN.index(start); b = MAIN.index(end, a) + len(end)
    return MAIN[a:b]


def relink(s, depth=0):
    """Якоря главной ведут на главную; для страниц в подпапке (depth=1) все относительные пути получают ../"""
    s = s.replace('href="#top"', 'href="index.html"')
    s = re.sub(r'href="#([\w-]+)"', r'href="index.html#\1"', s)
    if depth:
        s = re.sub(r'(href|src)="(?!https?:|mailto:|tel:|#|/|\.\./|data:)', r'\1="' + '../' * depth, s)
    return s


def parts(depth=0):
    p = {
        'HEADER': block('<header class="hdr dark" id="hdr">', '</header>'),
        'MMENU': block('<div class="mmenu dark" id="mmenu"', '\n</div>\n'),
        'SEARCH': block('<div class="search" id="search"', '\n</div>\n'),
        'FOOTER': block('<footer class="foot dark stack">', '</footer>').replace('class="foot dark stack"', 'class="foot dark"'),
        'OCC': block('<!-- Загруженность зала:', '\n</div>\n'),
        'JOIN': block('<!-- Всплывающее окно «Присоединяйтесь»', '</dialog>'),
        'LB': block('<!-- Галерея: открывается по клику', '</dialog>'),
        'CONTACT': block('<div class="contact reveal">', '\n        </div>\n      </div>\n    </div>\n'),
    }
    return {k: relink(v, depth) for k, v in p.items()}
