# -*- coding: utf-8 -*-
"""Пакет главной страницы К2 для MODX Revolution: k2/modx/ и k2/K2_main_MODX.zip
 - assets/templates/k2/   — стили, скрипты, шрифты, картинки, видео
 - elements/templates/    — шаблон главной
 - elements/chunks/       — чанки (шапка, подвал, блоки главной, строки MIGX)
 - elements/snippets/     — заготовка сниппета загруженности зала
 - data/                  — настройки MIGX и текущие тексты (цены, пакеты, вопросы) для заполнения TV
Запуск:  python tools/build_modx.py
"""
import io, os, re, json, shutil, html as H

K2 = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
SITE = os.path.join(K2, 'site')
OUT = os.path.join(K2, 'modx')
A = '[[++assets_url]]templates/k2/'
shutil.rmtree(OUT, ignore_errors=True)
for d in ('assets/templates/k2', 'elements/templates', 'elements/chunks', 'elements/snippets', 'data'):
    os.makedirs(os.path.join(OUT, d), exist_ok=True)

def w(path, text):
    p = os.path.join(OUT, path); os.makedirs(os.path.dirname(p), exist_ok=True)
    io.open(p, 'w', encoding='utf-8', newline='\n').write(text)

# ---------- Файлы ----------
AS = os.path.join(OUT, 'assets/templates/k2')
for sub in ('img', 'fonts', 'video'):
    shutil.copytree(os.path.join(SITE, 'assets', sub), os.path.join(AS, sub))
css = io.open(os.path.join(SITE, 'css/style.css'), encoding='utf-8').read()
css = css.replace('url("../assets/img/', 'url("../img/').replace('url("../assets/fonts/', 'url("../fonts/')
css = re.sub(r'\n/\* ---------- ВРЕМЕННО: панель выбора акцента.*?(?=\n/\* ---------- |\Z)', '\n', css, flags=re.S)
os.makedirs(os.path.join(AS, 'css')); io.open(os.path.join(AS, 'css/style.css'), 'w', encoding='utf-8').write(css)
js = io.open(os.path.join(SITE, 'js/main.js'), encoding='utf-8').read()
i = js.find('/* ---------- ВРЕМЕННО: выбор акцентного цвета')
if i > 0: js = js[:i].rstrip() + '\n'
os.makedirs(os.path.join(AS, 'js')); io.open(os.path.join(AS, 'js/main.js'), 'w', encoding='utf-8').write(js)
shutil.copy(os.path.join(SITE, 'js/search.js'), os.path.join(AS, 'js/search.js'))
shutil.copytree(os.path.join(SITE, 'assets', 'docs'), os.path.join(AS, 'docs'))

# ---------- Разметка главной ----------
src = io.open(os.path.join(SITE, 'index.html'), encoding='utf-8').read()
body = src[src.index('<body'):]
body = body[body.index('>') + 1: body.index('<script src="js/search.js')]

MARKS = [('<!-- Прелоадер', 'k2_preloader'), ('<!-- Шкала высоты 0', 'k2_gauge'), ('<!-- 01 Промобар', 'k2_header'),
         ('<!-- Мобильное меню', 'k2_mmenu'), ('<!-- Поиск', 'k2_search'), ('<!-- 03 Hero', 'k2_home_hero'),
         ('<!-- 04 Первый раз', 'k2_home_first'), ('<!-- 05 Промолайн', 'k2_home_band'), ('<!-- 06 К2', 'k2_home_why'),
         ('<!-- 08 Для любых целей', 'k2_home_goals'), ('<!-- 09 Цены', 'k2_home_prices'), ('<!-- 11 Видео', 'k2_home_videos'),
         ('<!-- 12 Блог', 'k2_home_blog'), ('<!-- 14 Связь', 'k2_home_contacts'), ('<!-- 16 Подвал', 'k2_footer'),
         ('<!-- Всплывающее окно', 'k2_join'), ('<!-- Галерея: открывается', 'k2_lightbox'), ('<!-- Загруженность зала:', 'k2_occ'),
         ('<!-- Словарик', 'k2_tip')]
pos = [(body.index(m), n) for m, n in MARKS]
chunks = {}
for k, (p, n) in enumerate(pos):
    end = pos[k + 1][0] if k + 1 < len(pos) else len(body)
    chunks[n] = body[p:end].replace('\n<main>\n', '\n').replace('\n</main>\n', '\n').strip() + '\n'

def common(s):
    s = s.replace('"assets/', '"' + A).replace("'assets/", "'" + A)
    s = s.replace('href="pervyj-raz.html"', 'href="[[~[[++k2_page_first]]]]"').replace('href="blog/index.html"', 'href="[[~[[++k2_page_blog]]]]"')
    s = s.replace('href="index.html"', 'href="[[~[[++site_start]]]]"')
    s = s.replace('+7 (812) 000-00-00', '[[++k2_phone]]').replace('tel:+78120000000', 'tel:[[++k2_phone_link]]')
    s = re.sub(r'\[с(?:&nbsp;| )__:__ до(?:&nbsp;| )__:__\]', '[[++k2_call_hours]]', s)
    s = s.replace('mailto:[почта]', 'mailto:[[++k2_email]]').replace('[почта]', '[[++k2_email]]')
    s = s.replace('[Адрес]', '[[++k2_address]]').replace('[Реквизиты]', '[[++k2_requisites]]')
    s = re.sub(r'\[ежедневно[^\]]*\]', '[[++k2_schedule]]', s).replace('[График работы]', '[[++k2_schedule]]').replace('[график]', '[[++k2_schedule]]')
    for cls, key in (('tg', 'k2_tg'), ('max', 'k2_max'), ('wa', 'k2_wa')):
        s = re.sub(r'(<a class="hold-btn hold-btn--\d hold-btn--%s") href="#"' % cls, r'\1 href="[[++%s]]" target="_blank" rel="noopener"' % key, s)
    s = re.sub(r'(<a class="hold-btn hold-btn--\d hold-btn--mail") href="#"', r'\1 href="mailto:[[++k2_email]]"', s)
    s = s.replace('<a href="#">[[++k2_email]]</a>', '<a href="mailto:[[++k2_email]]">[[++k2_email]]</a>').replace('<li><a href="#">Блог</a></li>', '<li><a href="[[~[[++k2_page_blog]]]]">Блог</a></li>')
    s = s.replace('<a class="btn btn--sec" href="#prices"><svg class="ico" viewBox="0 0 24 24"><path d="M12 4v11', '<a class="btn btn--sec" href="[[++k2_price_pdf:default=`#prices`]]" download><svg class="ico" viewBox="0 0 24 24"><path d="M12 4v11')
    return s
chunks = {n: common(c) for n, c in chunks.items()}

# Промобар — отдельный чанк, включается настройкой
hdr = chunks['k2_header']
m = re.search(r'<!-- Промобар:.*?\n  <div class="promo".*?\n</div>\n', hdr, re.S)
promo = m.group(0)
hdr = hdr.replace(promo, '  [[++k2_promo_on:is=`1`:then=`[[$k2_promo]]`]]\n')
promo = re.sub(r'<div class="promo" id="promo"', '<div class="promo" id="promo" style="--promo-bg:[[++k2_promo_bg:default=`var(--stone-100)`]]"', promo)
promo = re.sub(r'<a class="promo__in" href="[^"]*">', '<a class="promo__in" href="[[++k2_promo_link]]">', promo)
promo = re.sub(r'<span class="promo__tag"><i></i>.*?</span>', '<span class="promo__tag"><i></i>[[++k2_promo_tag]]</span>', promo)
promo = re.sub(r'<span class="promo__txt">.*?</span>\n', '<span class="promo__txt">[[++k2_promo_text]]</span>\n', promo, flags=re.S)
promo_text = re.search(r'<span class="promo__txt">(.*?)</span>', m.group(0), re.S).group(1)
chunks['k2_promo'] = promo.strip() + '\n'
chunks['k2_header'] = hdr

# Первый экран: видео и заставка — TV главной
hero = chunks['k2_home_hero']
hero = hero.replace('data-src="%svideo/hero.mp4"' % A, 'data-src="[[*k2_hero_video:default=`%svideo/hero.mp4`]]"' % A)
hero = hero.replace('poster="%svideo/hero-poster.jpg"' % A, 'poster="[[*k2_hero_poster:default=`%svideo/hero-poster.jpg`]]"' % A)
chunks['k2_home_hero'] = hero

# Цены (MIGX k2_prices) и пакеты (MIGX k2_packs_start / k2_packs_more)
pr = chunks['k2_home_prices']
rows = re.findall(r'<div class="prow"><p class="prow__n">(.*?)</p><p class="prow__d">(.*?)</p><p class="prow__v">(.*?)</p></div>', pr)
seed_prices = [{'MIGX_id': i + 1, 'name': a, 'note': b, 'price': c} for i, (a, b, c) in enumerate(rows)]
pr = re.sub(r'(<div class="plist reveal">)\s*(?:<div class="prow">.*?</div>\s*)+(</div>)', r'\1\n          [[getImageList? &tvname=`k2_prices` &tpl=`k2_price_row`]]\n        \2', pr, flags=re.S)
chunks['k2_price_row'] = '<div class="prow"><p class="prow__n">[[+name]]</p><p class="prow__d">[[+note]]</p><p class="prow__v">[[+price]]</p></div>\n'

def packs_of(panel_id):
    seg = re.search(r'<div class="packs[^"]*" id="%s"[^>]*>(.*?)\n    </div>' % panel_id, pr, re.S).group(1)
    out = []
    for card in re.findall(r'<a class="pack".*?</a>', seg, re.S):
        g = lambda rx: (re.search(rx, card, re.S) or [None, ''])[1]
        out.append({'title': g(r'<span class="pack__t">(.*?)</span><span class="pack__d">'), 'desc': g(r'<span class="pack__d">(.*?)</span>'),
                    'image': re.search(r'img/([^"]+)"', card).group(1), 'hit': '1' if 'pack__hit' in card else '',
                    'badges': ', '.join(re.findall(r'<span class="badge">(.*?)</span>', card)).replace('&nbsp;', ' '),
                    'price': '', 'price_old': '', 'link': re.search(r'href="([^"]*)"', card).group(1)})
    return [dict(o, MIGX_id=i + 1) for i, o in enumerate(out)]
seed_start, seed_more = packs_of('packs-start'), packs_of('packs-more')
for pid, tv in (('packs-start', 'k2_packs_start'), ('packs-more', 'k2_packs_more')):
    pr = re.sub(r'(<div class="packs[^"]*" id="%s"[^>]*>).*?(\n    </div>)' % pid, r'\1\n      [[getImageList? &tvname=`%s` &tpl=`k2_pack_card`]]\2' % tv, pr, count=1, flags=re.S)
chunks['k2_home_prices'] = pr
chunks['k2_pack_card'] = ('<a class="pack" href="[[+link:default=`#prices`]]"><span class="pack__img"><img src="[[+image]]" alt="" loading="lazy">'
    '[[+hit:is=`1`:then=`<span class="pack__hit">Чаще всего выбирают</span>`]]</span><span class="pack__b"><span class="pack__t">[[+title]]</span>'
    '<span class="pack__d">[[+desc]]</span><span class="badges">[[!k2Badges? &list=`[[+badges]]`]]</span><span class="pack__f">'
    '<span class="price" data-price="[[+price]]" data-price-old="[[+price_old]]">[[+price_old:notempty=`<s class="price__old"><span class="sr">Старая цена: </span>[[+price_old]]&nbsp;₽</s>`]]'
    '<b class="price__new"><span class="sr">Цена: </span>[[+price:default=`[____]`]]&nbsp;₽</b></span>'
    '<span class="go go--s"><svg class="ico" viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></svg></span></span></span></a>\n')

# Вопросы (MIGX k2_faq)
ct = chunks['k2_home_contacts']
faq = [{'q': q, 'a': a} for q, a in re.findall(r'<summary>(.*?)<i></i></summary><div class="faq__a"><p>(.*?)</p></div>', ct)]
seed_faq = [dict(f, MIGX_id=i + 1) for i, f in enumerate(faq)]
half = (len(faq) + 1) // 2
ct = re.sub(r'<div class="faq">.*?\n    </div>\n', ('<div class="faq">\n      <div class="faq__col">[[getImageList? &tvname=`k2_faq` &limit=`%d` &tplFirst=`k2_faq_item_open` &tpl=`k2_faq_item`]]</div>\n'
            '      <div class="faq__col">[[getImageList? &tvname=`k2_faq` &offset=`%d` &tpl=`k2_faq_item`]]</div>\n    </div>\n') % (half, half), ct, count=1, flags=re.S)
ct = ct.replace('<p class="seo">', '<div class="seo">[[*content]]</div><!-- было: <p class="seo">').replace('</p>\n  </div>\n</section>', '</p> -->\n  </div>\n</section>', 1)
# Формы: обработчик FormIt (ресурс), имя формы
ct = ct.replace('<form class="cform" id="cform" novalidate>', '<form class="cform" id="cform" novalidate data-action="[[~[[++k2_form_handler]]]]">\n          <input type="hidden" name="form" value="contacts">')
ct = ct.replace('data-open="08:00" data-close="23:00"', 'data-open="[[++k2_open:default=`08:00`]]" data-close="[[++k2_close:default=`23:00`]]"')
chunks['k2_home_contacts'] = ct
chunks['k2_faq_item'] = '<details class="reveal"><summary>[[+q]]<i></i></summary><div class="faq__a"><p>[[+a]]</p></div></details>\n'
chunks['k2_faq_item_open'] = '<details class="reveal" open><summary>[[+q]]<i></i></summary><div class="faq__a"><p>[[+a]]</p></div></details>\n'
jn = chunks['k2_join'].replace('<form class="cform cform--modal" novalidate>', '<form class="cform cform--modal" novalidate data-action="[[~[[++k2_form_handler]]]]">\n      <input type="hidden" name="form" value="join">')
chunks['k2_join'] = jn

# Загруженность зала: адрес JSON и вместимость — настройки
chunks['k2_occ'] = chunks['k2_occ'].replace('data-endpoint=""', 'data-endpoint="[[++k2_occ_endpoint]]"').replace('data-capacity="120"', 'data-capacity="[[++k2_capacity:default=`120`]]"')

# Блог: последние 4 статьи (pdoResources), рубрики — TV k2_category
bl = chunks['k2_home_blog']
bl = re.sub(r'<div class="posts">.*?\n    </div>', '<div class="posts">\n      [[pdoResources? &parents=`[[++k2_page_blog]]` &limit=`4` &sortby=`publishedon` &sortdir=`DESC` &includeTVs=`k2_cover,k2_category,k2_read_min` &processTVs=`1` &tpl=`k2_blog_card`]]\n    </div>', bl, count=1, flags=re.S)
chunks['k2_home_blog'] = bl
CAT = {'travel': 'Путешествия', 'train': 'Тренировки', 'gear': 'Снаряжение', 'club': 'Наш клуб'}
chunks['k2_blog_card'] = ('<a class="post reveal" href="[[~[[+id]]]]" data-cat="[[+tv.k2_category]]"><span class="post__img"><img src="[[+tv.k2_cover]]" alt="" loading="lazy"></span>'
    '<span class="post__b"><span class="badges"><span class="badge">[[+tv.k2_category:is=`travel`:then=`Путешествия`:else=`[[+tv.k2_category:is=`train`:then=`Тренировки`:else=`[[+tv.k2_category:is=`gear`:then=`Снаряжение`:else=`Наш клуб`]]`]]`]]</span></span>'
    '<span class="post__t">[[+pagetitle]]</span><span class="post__m">[[+publishedon:date=`%d.%m.%Y`]] · [[+tv.k2_read_min:default=`3`]] мин чтения</span></span></a>\n')

for n, c in chunks.items():
    w('elements/chunks/%s.html' % n, c)

# ---------- Шаблон главной ----------
order_top = ['k2_preloader', 'k2_gauge', 'k2_header', 'k2_mmenu', 'k2_search']
order_main = ['k2_home_hero', 'k2_home_first', 'k2_home_band', 'k2_home_why', 'k2_home_goals', 'k2_home_prices', 'k2_home_videos', 'k2_home_blog', 'k2_home_contacts']
order_end = ['k2_footer', 'k2_join', 'k2_lightbox', 'k2_occ', 'k2_tip']
tpl = '''<!doctype html>
<html lang="ru">
<head>
<meta charset="[[++modx_charset]]">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>[[*longtitle:default=`[[*pagetitle]]`]]</title>
<meta name="description" content="[[*description]]">
<link rel="stylesheet" href="%(A)scss/style.css?v=[[++k2_assets_version:default=`1`]]">
</head>
<body class="is-loading">
%(TOP)s
<main>
%(MAIN)s
</main>
%(END)s
<script src="%(A)sjs/search.js?v=[[++k2_assets_version:default=`1`]]"></script>
<script src="%(A)sjs/main.js?v=[[++k2_assets_version:default=`1`]]"></script>
</body>
</html>
''' % {'A': A, 'TOP': '\n'.join('[[$%s]]' % n for n in order_top), 'MAIN': '\n'.join('[[$%s]]' % n for n in order_main), 'END': '\n'.join('[[$%s]]' % n for n in order_end)}
w('elements/templates/k2_home.html', tpl)

# ---------- Сниппеты ----------
w('elements/snippets/k2Badges.php', '''<?php
/**
 * k2Badges — превращает список «3 тренировки, боулдеринг» в плашки.
 * Вызов: [[!k2Badges? &list=`[[+badges]]`]]
 */
$out = '';
foreach (array_filter(array_map('trim', explode(',', (string) $list))) as $b) {
    $out .= '<span class="badge">' . htmlspecialchars($b, ENT_QUOTES, 'UTF-8') . '</span>';
}
return $out;
''')
w('elements/snippets/k2Occupancy.php', '''<?php
/**
 * k2Occupancy — отдаёт загруженность зала для виджета на сайте (JSON).
 * Положить на отдельный ресурс: шаблон «пустой», тип содержимого JSON, без кеширования: [[!k2Occupancy]]
 * Адрес ресурса указать в системной настройке k2_occ_endpoint.
 *
 * ВАЖНО: ключ API CRM хранить только здесь, в системной настройке k2_crm_key (не на странице и не в JS).
 * Ниже — заготовка: запрос к CRM надо дописать под конкретную CRM (какую — уточнить у заказчика).
 */
$cacheKey = 'k2/occupancy';
$cached = $modx->cacheManager->get($cacheKey);
if ($cached) { return $cached; }

$capacity = (int) $modx->getOption('k2_capacity', null, 120);
$count = null;
$hourly = null; // необязательно: массив из 24 чисел — сколько людей обычно в зале в каждый час

/* --- Пример запроса к CRM (заменить на настоящий) ---
$key = $modx->getOption('k2_crm_key');
$ch = curl_init('https://crm.example/api/occupancy');
curl_setopt_array($ch, [CURLOPT_RETURNTRANSFER => true, CURLOPT_TIMEOUT => 5, CURLOPT_HTTPHEADER => ['Authorization: Bearer ' . $key]]);
$res = json_decode(curl_exec($ch), true);
curl_close($ch);
$count = isset($res['inside']) ? (int) $res['inside'] : null;
--- */

if ($count === null) {
    http_response_code(503); // виджет покажет демо-данные с пометкой «Демо»
    return json_encode(['error' => 'no data']);
}
$json = json_encode(['count' => $count, 'capacity' => $capacity, 'updated' => date('c'), 'hourly' => $hourly], JSON_UNESCAPED_UNICODE);
$modx->cacheManager->set($cacheKey, $json, 30); // не дёргаем CRM чаще раза в 30 секунд
return $json;
''')

# ---------- MIGX: настройки полей и текущие значения ----------
def migx(fields, cols):
    return {'formtabs': json.dumps([{'MIGX_id': 1, 'caption': 'Данные', 'fields': fields}], ensure_ascii=False),
            'columns': json.dumps(cols, ensure_ascii=False)}
F = lambda name, cap, typ='text': {'field': name, 'caption': cap, 'inputTVtype': typ}
C = lambda name, cap: {'header': cap, 'dataIndex': name}
migx_cfg = {
    'k2_prices': migx([F('name', 'Название'), F('note', 'Пояснение'), F('price', 'Цена (с «₽»)')], [C('name', 'Название'), C('price', 'Цена')]),
    'k2_packs': migx([F('title', 'Название'), F('desc', 'Описание', 'textarea'), F('image', 'Обложка', 'image'), F('badges', 'Плашки через запятую'),
                      F('price', 'Цена, ₽ (число)'), F('price_old', 'Старая цена, ₽ (если есть скидка)'), F('hit', 'Плашка «Чаще всего выбирают» (1 — да)'), F('link', 'Ссылка на страницу пакета')],
                     [C('title', 'Название'), C('price', 'Цена'), C('price_old', 'Старая')]),
    'k2_faq': migx([F('q', 'Вопрос'), F('a', 'Ответ', 'textarea')], [C('q', 'Вопрос')]),
}
w('data/migx_configs.json', json.dumps(migx_cfg, ensure_ascii=False, indent=2))
for s in (seed_start, seed_more):
    for o in s: o['image'] = '/assets/templates/k2/img/' + o['image']
seed = {'k2_prices': seed_prices, 'k2_packs_start': seed_start, 'k2_packs_more': seed_more, 'k2_faq': seed_faq}
for k, v in seed.items():
    w('data/tv_%s.json' % k, json.dumps(v, ensure_ascii=False, indent=2))

SETTINGS = [
    ('k2_phone', '+7 (812) 000-00-00', 'Телефон, как показывать'), ('k2_phone_link', '+78120000000', 'Телефон для ссылки tel:'),
    ('k2_call_hours', '[с __:__ до __:__]', 'Часы приёма звонков'), ('k2_email', '[почта]', 'Почта'),
    ('k2_address', '[Адрес]', 'Адрес'), ('k2_schedule', '[ежедневно, __:__–__:__]', 'График работы (текстом)'),
    ('k2_open', '08:00', 'Открытие, ЧЧ:ММ — для плашки «Сейчас открыто»'), ('k2_close', '23:00', 'Закрытие, ЧЧ:ММ'),
    ('k2_tg', '#', 'Ссылка на Telegram'), ('k2_max', '#', 'Ссылка на Max'), ('k2_wa', '#', 'Ссылка на WhatsApp'),
    ('k2_price_pdf', '', 'Ссылка на PDF с полным прайсом'),
    ('k2_requisites', '[Реквизиты]', 'Реквизиты в подвале'),
    ('k2_promo_on', '1', 'Промобар включён (1/0)'), ('k2_promo_tag', 'Новая группа', 'Промобар: плашка'),
    ('k2_promo_text', H.unescape(promo_text), 'Промобар: текст (можно <b>)'), ('k2_promo_link', '#kids', 'Промобар: ссылка'),
    ('k2_promo_bg', '', 'Промобар: цвет фона (пусто — светлый камень по дизайну)'),
    ('k2_page_first', '', 'ID ресурса «Первый раз»'), ('k2_page_blog', '', 'ID раздела «Блог»'),
    ('k2_form_handler', '', 'ID ресурса-обработчика заявок (FormIt)'),
    ('k2_occ_endpoint', '', 'Адрес JSON загруженности (ресурс со сниппетом k2Occupancy)'), ('k2_capacity', '120', 'Вместимость зала'),
    ('k2_crm_key', '', 'Ключ API CRM — только для сниппета, на страницу не выводится'),
    ('k2_assets_version', '1', 'Версия стилей/скриптов: увеличить после правок, чтобы сбросить кеш браузеров'),
]
w('data/system_settings.json', json.dumps([{'key': k, 'value': v, 'name': n, 'namespace': 'k2', 'area': 'k2'} for k, v, n in SETTINGS], ensure_ascii=False, indent=2))

# ---------- README ----------
chunk_list = '\n'.join('| `%s` | %s |' % (n, d) for n, d in [
    ('k2_preloader', 'заставка при загрузке'), ('k2_gauge', 'шкала 0 → 13 м справа (навигация по странице)'),
    ('k2_header', 'шапка; промобар подключается из `k2_promo`'), ('k2_promo', 'промобар (тексты из настроек)'),
    ('k2_mmenu', 'мобильное меню'), ('k2_search', 'окно поиска'),
    ('k2_home_hero', 'первый экран (видео — TV `k2_hero_video`, заставка — `k2_hero_poster`)'), ('k2_home_first', '«Первый раз? Сейчас разберёмся!»'),
    ('k2_home_band', 'красная бегущая лента'), ('k2_home_why', 'логотип К2 со сменой фото + «Почему нужно лазать в К2» + «Ещё атмосферы»'),
    ('k2_home_goals', '«Скалодром для любых целей»'), ('k2_home_prices', 'цены (MIGX `k2_prices`) и пакеты (MIGX `k2_packs_start`, `k2_packs_more`)'),
    ('k2_home_videos', 'лента видео'), ('k2_home_blog', 'блог (pdoResources) и отзывы'),
    ('k2_home_contacts', 'связь, форма заявки, вопросы (MIGX `k2_faq`), SEO-текст (`[[*content]]`)'),
    ('k2_footer', 'подвал'), ('k2_join', 'окно «Присоединяйтесь»'), ('k2_lightbox', 'галерея на весь экран'),
    ('k2_occ', 'панель загруженности зала'), ('k2_tip', 'подсказка словарика'),
    ('k2_price_row', 'строка цены (для getImageList)'), ('k2_pack_card', 'карточка пакета (для getImageList)'),
    ('k2_faq_item / k2_faq_item_open', 'вопрос FAQ (первый — раскрыт)'), ('k2_blog_card', 'карточка статьи (для pdoResources)')])
settings_list = '\n'.join('| `%s` | %s | `%s` |' % (k, n, v.replace('|', '\\|')) for k, v, n in SETTINGS)
readme = '''# Скалодром К2 — главная страница для MODX Revolution

Готовая вёрстка главной, разложенная под MODX. Дизайн, анимации и адаптив — как на превью
(`zingy-faun-2ee984.netlify.app`) — по нему можно сверять.

## Что нужно на сайте
MODX Revolution 2.8+ или 3.x и дополнения: **pdoTools**, **MIGX**, **FormIt** (по желанию **ClientConfig** —
тогда настройки ниже удобно вынести на одну страницу для заказчика).

## Как установить
1. **Файлы.** Скопировать `assets/templates/k2/` в `/assets/templates/k2/` на сервере.
2. **Чанки.** Для каждого файла из `elements/chunks/` создать чанк с таким же именем (без `.html`) и вставить содержимое.
   (Или подключить как статические элементы из файлов.)
3. **Шаблон.** Создать шаблон `K2 — главная` из `elements/templates/k2_home.html` и назначить его главной странице.
4. **Сниппеты.** Создать `k2Badges` и `k2Occupancy` из `elements/snippets/`.
5. **Настройки.** Создать системные настройки (пространство имён `k2`) из `data/system_settings.json` — список ниже.
6. **TV главной** (назначить шаблону `K2 — главная`):
   - `k2_prices`, `k2_packs_start`, `k2_packs_more`, `k2_faq` — тип **migx**; поля и колонки — в `data/migx_configs.json`
     (`k2_packs_start` и `k2_packs_more` используют конфигурацию `k2_packs`).
     Текущие тексты уже подготовлены: вставить содержимое `data/tv_*.json` в значение соответствующего TV.
   - `k2_hero_video` (файл/URL видео первого экрана), `k2_hero_poster` (картинка-заставка) — тип image/file.
   - SEO-текст внизу главной — поле «Содержимое» (`[[*content]]`) самой главной.
7. **Блог.** У статей — TV `k2_cover` (image), `k2_category` (список: `travel`, `train`, `gear`, `club`), `k2_read_min` (число).
   Главная показывает 4 последние статьи из раздела, ID которого в `k2_page_blog`.
8. **Заявки.** Создать ресурс-обработчик (шаблон «пустой», не кешировать), например:
   ```
   [[!FormIt?
     &hooks=`email`
     &validate=`name:required,phone:required,agree:required`
     &emailTo=`[[++k2_email]]`
     &emailSubject=`Заявка с сайта К2 ([[+form]])`
     &emailTpl=`k2_email_tpl`
     &successMessage=`ok`
   ]][[!+fi.successMessage]]
   ```
   Его ID — в `k2_form_handler`. Обе формы (внизу страницы и окно «Присоединяйтесь») отправляют сюда поля
   `form` (contacts / join), `topic`, `name`, `phone`, `via`, `agree`. Сайт считает заявку отправленной при ответе 200,
   при ошибке покажет «Не получилось отправить». Чанк письма `k2_email_tpl` — на ваше усмотрение.
   Отправку в CRM добавить хуком FormIt.
9. **Загруженность зала.** Ресурс с `[[!k2Occupancy]]` (шаблон «пустой», тип JSON, не кешировать), его URL — в
   `k2_occ_endpoint`. Запрос к CRM дописать в сниппете (там заготовка). **Ключ CRM — только в настройке `k2_crm_key`,
   на страницу он не попадает.** Пока данных нет, виджет показывает демо с пометкой «Демо».
10. **Ссылки.** ID страниц «Первый раз» и «Блог» — в `k2_page_first`, `k2_page_blog`. Заполнить сразу: пока ID пустые, ссылки будут пустыми. Если страниц ещё нет — указать ID главной.

## Важно
- **Ссылки на внутренние страницы** в чанках — вида `ceny.html`, `dlya-vzroslyh.html`. Они заработают, если включены
  дружественные URL с суффиксом `.html` и у ресурсов такие же псевдонимы (alias): dlya-vzroslyh, bazovye-kursy, shkola,
  individualnye, samostoyatelno, dlya-detej, detskaya-sekciya, deti-pervyj-raz, ceny, pakety, sertifikaty, meropriyatiya,
  o-skalodrome, trenery, video, vakansii, dokumenty, kontakty. Вёрстка этих страниц — в статичной версии сайта, пакеты под MODX — следующим этапом.
- **Поиск** (`js/search.js`) — статичный список страниц; в MODX заменить на SimpleSearch / mSearch2.
- **`<base href>` не добавлять.** На главной много якорей (`#prices`, `#contacts`…), с `<base>` они уведут на другой адрес.
- **Кеш браузеров.** После правки стилей или скриптов увеличить `k2_assets_version` — ссылки на файлы обновятся.
- **Неразрывные пробелы.** В вёрстке после предлогов и в числах стоят `&nbsp;`. В текстах, которые вводят в админке
  (цены, пакеты, вопросы, статьи), их нужно ставить вручную или подключить плагин-типограф.
- **Пути к картинкам** в чанках — через `[[++assets_url]]templates/k2/`.
- Тексты в [квадратных скобках] — заглушки: заполнить в настройках/TV.
- Ссылки `href="#"` (соцсети, документы, тренеры, мероприятия, видео) — заглушки: поставить, когда появятся страницы.
- Лента видео и фото в «Почему К2» сейчас в чанках вручную; при желании их тоже можно перевести на MIGX.

## Чанки
| Чанк | Что внутри |
|---|---|
%s

## Системные настройки
| Ключ | Что это | Сейчас |
|---|---|---|
%s
''' % (chunk_list, settings_list)
w('README.md', readme)

zp = os.path.join(K2, 'K2_main_MODX')
if os.path.exists(zp + '.zip'): os.remove(zp + '.zip')
shutil.make_archive(zp, 'zip', OUT)
print('готово:', OUT, '| чанков:', len(chunks), '| цены:', len(seed_prices), '| пакеты:', len(seed_start), '+', len(seed_more), '| вопросы:', len(seed_faq))
