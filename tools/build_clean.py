# -*- coding: utf-8 -*-
"""Чистая вёрстка страниц для разработчика: один HTML-файл на страницу + css/, js/, assets/ — без привязки к CMS.
Запуск:  python tools/build_clean.py index.html [pervyj-raz.html ...]  →  k2/handoff/<имя>/ и k2/handoff/<имя>.zip
Берёт файлы из site/; кладёт только то, что страница подключает; убирает временную панель цвета и номера версий.
"""
import io, os, re, shutil, sys

K2 = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
SITE = os.path.join(K2, 'site')
NAMES = {'index.html': 'K2_glavnaya'}

# Комментарии с упоминанием CMS → нейтральные
COMMENTS = [
    ('В MODX — галерея (MIGX) ', ''),
    ('Отправку в CRM подключит разработчик (обработчик submit в main.js)', 'Отправка: атрибут data-action у формы (см. main.js)'),
    ('Отправку подключит разработчик (FormIt / AjaxForm)', 'Отправка: атрибут data-action у формы (см. main.js)'),
    ('(сниппет MODX), ', ', '),
    ('// В MODX: отправку подключает разработчик (FormIt / AjaxForm) — место отмечено ниже', '// Отправка настраивается атрибутом data-action у формы — место отмечено ниже'),
    ('(обработчик FormIt / AjaxForm в MODX)', '(адрес обработчика заявок)'),
    ('(через свой сервер / сниппет MODX — ', '(через свой сервер — '),
    (' В MODX его заменит SimpleSearch / mSearch2 (или JSON из pdoResources).', ' При подключении к серверу заменить настоящим поиском.'),
    ('/* В MODX: data-price / data-price-old из MIGX; если', '/* data-price / data-price-old — цены; если'),
    ('В MODX: ссылка на ролик (TV). ', 'Ссылка на ролик — атрибут data-video. '),
    ('В MODX: тренеры — ресурсы/MIGX (фото, имя, должность, квалификация)', 'Тренеры: фото, имя, должность, квалификация'),
    ('(в MODX из прайса)', '(из прайса)'),
    ('(в MODX — из прайса)', '(из прайса)'),
]
CMS = re.compile(r'modx|formit|ajaxform|migx|pdoresources|msearch|simplesearch|сниппет', re.I)

def clean_text(s):
    for a, b in COMMENTS:
        s = s.replace(a, b)
    return s

def clean_css(s):
    s, n = re.subn(r'/\* -+ ВРЕМЕННО: панель выбора акцента.*?(?=\n/\* -)', '', s, count=1, flags=re.S)
    return s

def clean_js(s):
    i = s.find('/* ---------- ВРЕМЕННО: выбор акцентного цвета')
    return s[:i].rstrip() + '\n' if i > 0 else s

def build(page):
    name = NAMES.get(page, 'K2_' + page.replace('.html', '').replace('/', '_'))
    out = os.path.join(K2, 'handoff', name)
    shutil.rmtree(out, ignore_errors=True)
    html = io.open(os.path.join(SITE, page), encoding='utf-8').read()
    used = set(re.findall(r'(?:href|src)="((?:css|js)/[^"?]+)', html))
    html = re.sub(r'((?:css|js)/[^"?]+)\?v=\d+', r'\1', html)
    html = clean_text(html)
    os.makedirs(out, exist_ok=True)
    io.open(os.path.join(out, os.path.basename(page)), 'w', encoding='utf-8').write(html)
    assets = set(re.findall(r'(assets/[^"\')\s?,]+)', html))
    for rel in sorted(used):
        s = io.open(os.path.join(SITE, rel), encoding='utf-8').read()
        s = clean_text(s)
        if rel.endswith('.css'):
            s = clean_css(s)
            assets |= {m for m in re.findall(r'\.\./(assets/[^"\')]+)', s)}
        else:
            s = clean_js(s)
        p = os.path.join(out, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
        io.open(p, 'w', encoding='utf-8').write(s)
    for rel in sorted(assets):
        src = os.path.join(SITE, rel)
        assert os.path.exists(src), rel
        p = os.path.join(out, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
        shutil.copy(src, p)
    left = []
    for root, _, fs in os.walk(out):
        for f in fs:
            if f.endswith(('.html', '.css', '.js')):
                t = io.open(os.path.join(root, f), encoding='utf-8').read()
                left += [f + ': ' + m.group(0) for m in CMS.finditer(t)]
                if re.search(r'ВРЕМЕННО|palette|\.pal\b', t): left.append(f + ': панель цвета')
    z = os.path.join(K2, 'handoff', name)
    if os.path.exists(z + '.zip'): os.remove(z + '.zip')
    shutil.make_archive(z, 'zip', out)
    print(name, '| файлов:', sum(len(f) for _, _, f in os.walk(out)), '| архив, МБ:', round(os.path.getsize(z + '.zip') / 1e6, 1), '| осталось упоминаний:', left)

for pg in sys.argv[1:] or ['index.html']:
    build(pg)
