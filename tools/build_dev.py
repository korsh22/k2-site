# -*- coding: utf-8 -*-
"""Папка для разработчика в репозитории: dlya-razrabotchika/verstka — чистая вёрстка ВСЕХ страниц одним набором
(css/, js/, assets/ — один раз), без номеров версий ?v= и без упоминаний CMS; плюс список страниц stranicy.md.
Запуск (после сборки сайта):  python tools/build_dev.py
Документы (README.md, tz/, backend/, cms/, dizajn/, foto/) пишутся вручную и этим скриптом не трогаются.
"""
import io, os, re, shutil
from build_clean import SITE, K2, clean_text, clean_css, clean_js, CMS

OUT = os.path.join(K2, 'dlya-razrabotchika')
V = os.path.join(OUT, 'verstka')
LIVE = 'https://korsh22.github.io/k2-site/'

# Шаблон каждой страницы — для списка (по имени файла)
def template(name):
    if name.startswith('arhiv-'): return 'Мероприятие (прошло)'
    if name.startswith('kurs-'): return 'Товар'
    if name in ('sorevnovaniya-po-boulderingu.html', 'vyezd-na-skaly.html', 'detskie-sorevnovaniya.html', 'novogodnij-detskij-festival.html', 'nochnoe-lazanie.html'): return 'Мероприятие'
    if name in ('politika-personalnyh-dannyh.html', 'pravila-poseshcheniya.html', 'tehnika-bezopasnosti.html', 'zayavlenie-roditelej.html', 'dogovor-oferty.html'): return 'Текстовая страница'
    if name.startswith('blog/'): return 'Статья блога' if name != 'blog/index.html' else 'Список статей'
    if name == 'shablon-uslugi.html': return 'Образец «Шаблон услуги» (14 блоков)'
    if name in ('korzina.html', 'spasibo.html'): return 'Корзина / оплата'
    if name == 'index.html': return 'Главная'
    return 'Посадочная услуги / раздела'

shutil.rmtree(V, ignore_errors=True)
pages = []
for root, _, files in os.walk(SITE):
    for f in files:
        if f.endswith('.html'):
            pages.append(os.path.relpath(os.path.join(root, f), SITE).replace(os.sep, '/'))
pages.sort(key=lambda p: (p.count('/'), p != 'index.html', p))
rows, left = [], []
for pg in pages:
    html = io.open(os.path.join(SITE, pg), encoding='utf-8').read()
    html = re.sub(r'((?:css|js)/[^"?]+)\?v=\d+', r'\1', html)
    html = clean_text(html)
    dst = os.path.join(V, pg); os.makedirs(os.path.dirname(dst), exist_ok=True)
    io.open(dst, 'w', encoding='utf-8').write(html)
    t = re.search(r'<title>(.*?)</title>', html, re.S)
    rows.append('| `%s` | %s | %s | [открыть](%s%s) |' % (pg, (t.group(1) if t else '').replace('|', '/'), template(pg), LIVE, pg))
for d in ('css', 'js'):
    for f in sorted(os.listdir(os.path.join(SITE, d))):
        s = io.open(os.path.join(SITE, d, f), encoding='utf-8').read()
        s = clean_text(s); s = clean_css(s) if f.endswith('.css') else clean_js(s)
        os.makedirs(os.path.join(V, d), exist_ok=True)
        io.open(os.path.join(V, d, f), 'w', encoding='utf-8').write(s)
shutil.copytree(os.path.join(SITE, 'assets'), os.path.join(V, 'assets'), ignore=shutil.ignore_patterns('p-hands.jpg'))  # p-hands.jpg — не используется
for root, _, fs in os.walk(V):
    for f in fs:
        if f.endswith(('.html', '.css', '.js')):
            left += [f + ': ' + m.group(0) for m in CMS.finditer(io.open(os.path.join(root, f), encoding='utf-8').read())]
io.open(os.path.join(OUT, 'stranicy.md'), 'w', encoding='utf-8').write(
    '# Все страницы сайта\n\nСписок собирается автоматически (`python tools/build_dev.py`). Вёрстка каждой страницы — в `verstka/`, '
    'живая версия — по ссылке.\n\n| Файл | Заголовок | Шаблон | Сайт |\n|---|---|---|---|\n' + '\n'.join(rows) + '\n')
print('страниц:', len(pages), '| осталось упоминаний CMS:', left[:5])
