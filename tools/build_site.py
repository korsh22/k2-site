# -*- coding: utf-8 -*-
"""Внутренние страницы К2 (всё, куда ведут меню, подвал и кнопки главной).
Шапка, меню, поиск, подвал, блок связи, окна — из site/index.html (через chrome.py).
Тексты — по ТЗ; всё, что должен дать скалодром (цены, имена, даты, тексты документов), — в [квадратных скобках].
Запуск после build_pages.py:  python tools/build_site.py
"""
import io, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from typograph import process as typograph
from chrome import ROOT, VER, MAIN, parts

P = parts(0)
BOOK = re.search(r'<!-- ЕДИНАЯ форма бронирования.*?</dialog>', io.open(os.path.join(ROOT, 'pervyj-raz.html'), encoding='utf-8').read(), re.S).group(0)
TIP = '<div class="tip" id="tip" role="tooltip" aria-hidden="true"><b class="tip__t"></b><span class="tip__d"></span></div>'

def ico(path): return '<svg class="ico" viewBox="0 0 24 24">%s</svg>' % path
ARROW = ico('<path d="M5 12h14M13 6l6 6-6 6"/>')
CHECK = ico('<path d="M5 12.5l4.5 4.5L19 7.5"/>')
I_TIME = ico('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>')
I_SPARK = ico('<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5L18 18M6 18l2.5-2.5M15.5 8.5L18 6"/>')
I_GEAR = ico('<path d="M7 4h10l2 6H5z"/><path d="M5 10v8a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-8"/><path d="M10 14h4"/>')
I_PEOPLE = ico('<circle cx="9" cy="8" r="3"/><path d="M3 20a6 6 0 0 1 12 0"/><circle cx="17" cy="9" r="2.5"/><path d="M15.5 14.2A5 5 0 0 1 21 19"/>')
I_CHILD = ico('<circle cx="12" cy="6" r="3"/><path d="M12 9v7M8 12h8M9 21l3-5 3 5"/>')
I_CAL = ico('<rect x="4" y="5" width="16" height="15" rx="2"/><path d="M4 10h16M9 3v4M15 3v4"/>')
I_PIN = ico('<path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>')
I_GIFT = ico('<rect x="4" y="10" width="16" height="10" rx="1"/><path d="M3 7h18v3H3zM12 7v13M12 7c-2-4-6-3-5 0M12 7c2-4 6-3 5 0"/>')
I_SHIELD = ico('<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/>')
I_UP = ico('<path d="M4 20l6-8 4 4 6-9"/><path d="M15 7h5v5"/>')

# Цены — ПРИМЕРНЫЕ (рыба для вида), реальные даст скалодром. rub(1500) → «1 500 ₽»; price(новая, старая) — блок цены карточки
def rub(v): return '{:,}'.format(v).replace(',', '&nbsp;') + '&nbsp;₽'
def price(v, old=None, frm=True):
    o = '<s class="price__old"><span class="sr">Старая цена: </span>%s%s</s>' % ('от&nbsp;' if frm else '', rub(old)) if old else ''
    return '<span class="price" data-price="%d" data-price-old="%s">%s<b class="price__new"><span class="sr">Цена: </span>%s%s</b></span>' % (v, old or '', o, 'от&nbsp;' if frm else '', rub(v))
PRICE = price(1500)
DOC_STUB = '[Текст документа предоставит скалодром. В MODX — отдельный ресурс или поле страницы.]'
# Документы — отдельные текстовые страницы (шаблон textpage); старые ссылки dokumenty.html#… перебрасывают на них (js/landing.js)
DOC_URL = {'pravila': 'pravila-poseshcheniya.html', 'tb': 'tehnika-bezopasnosti.html', 'zayavlenie': 'zayavlenie-roditelej.html', 'oferta': 'dogovor-oferty.html', 'privacy': 'politika-personalnyh-dannyh.html'}


# ---------- Кирпичики ----------
def join_btn(text, title, topic='', cls='btn btn--primary'):
    t = ' data-join-topic="%s"' % topic if topic else ''
    return '<button class="%s js-join" type="button" aria-haspopup="dialog" aria-controls="join" data-join-title="%s"%s>%s</button>' % (cls, title, t, text)

def book_btn(text, typ='', adults=None, kids=None, cls='btn btn--primary'):
    a = (' data-book-type="%s"' % typ if typ else '') + (' data-book-adults="%d"' % adults if adults is not None else '') + (' data-book-kids="%d"' % kids if kids is not None else '')
    return '<button class="%s js-book" type="button"%s>%s</button>' % (cls, a, text)

def link_btn(text, href, cls='btn btn--sec'):
    return '<a class="%s" href="%s">%s</a>' % (cls, href, text)

def crumbs(items):
    out = ['<a href="index.html">Главная</a>']
    for i, (t, h) in enumerate(items):
        out.append('<span>/</span>' + ('<a href="%s">%s</a>' % (h, t) if h and i < len(items) - 1 else '<span>%s</span>' % t))
    return '<nav class="crumbs" aria-label="Хлебные крошки">%s</nav>' % ''.join(out)

def hero(cr, h1, lead, img, marks=(), btns='', alt=''):
    m = '<ul class="lp-marks reveal">%s</ul>' % ''.join('<li>%s<span>%s</span></li>' % x for x in marks) if marks else ''
    return '''<section class="lp-hero dark" id="top">
  <div class="wrap lp-hero__g">
    <div class="lp-hero__text">
      %s
      <h1 class="d lp-hero__t lp-hero__t--fit reveal">%s</h1>
      <p class="lead lp-hero__l reveal">%s</p>
      %s
      <div class="btns reveal">%s</div>
    </div>
    <figure class="lp-hero__img reveal"><img src="assets/img/%s" alt="%s" fetchpriority="high"></figure>
  </div>
</section>''' % (crumbs(cr), h1, lead, m, btns, img, alt)

def head(cr, h1, lead='', extra=''):
    return '''<section class="blog-head dark" id="top">
  <div class="wrap">
    %s
    <h1 class="d h1 blog-head__t">%s</h1>
    %s%s
  </div>
</section>''' % (crumbs(cr), h1, '<p class="lead blog-head__l">%s</p>' % lead if lead else '', extra)

def sec(inner, id='', tone='neutral', cls=''):
    return '<section class="sec %s%s"%s>\n  <div class="wrap">\n%s\n  </div>\n</section>' % (tone, ' ' + cls if cls else '', ' id="%s"' % id if id else '', inner)

def sechead(h2, lead='', right=''):
    l = '<p class="lead muted reveal">%s</p>' % lead if lead else ''
    return '<div class="sechead"><div><h2 class="d h2 reveal">%s</h2>%s</div>%s</div>' % (h2, l, right)

# Иконки карточек и шагов по заголовку (cards() и steps() подставляют сами)
_I = {
    'shield': '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
    'shoe': '<path d="M3 17v-4.5c2-.5 3.5-2 4.5-4l1-2 3 2.5c1.5 1.3 3 2 5 2.3 2.4.4 4.5 1.4 4.5 3.7v2z"/><path d="M3 20h18"/>',
    'key': '<circle cx="8" cy="15" r="4"/><path d="M11 12l8-8M16 7l2 2M14 9l2 2"/>',
    'smile': '<circle cx="12" cy="12" r="9"/><path d="M8.5 14a4 4 0 0 0 7 0M9 9.5h.01M15 9.5h.01"/>',
    'people': '<circle cx="9" cy="8" r="3"/><path d="M3 20a6 6 0 0 1 12 0"/><circle cx="17" cy="9" r="2.5"/><path d="M16 14.2A5 5 0 0 1 21 19"/>',
    'book': '<path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2z"/><path d="M4 19V5M9 7h6"/>',
    'rope': '<path d="M9 3h6l-1 5a2 2 0 0 1-4 0z"/><path d="M12 10v3"/><circle cx="12" cy="17" r="4"/>',
    'flag': '<path d="M5 21V4M5 4h11l-2 4 2 4H5"/>',
    'route': '<circle cx="6" cy="18" r="2"/><circle cx="12" cy="11" r="2"/><circle cx="18" cy="5" r="2"/><path d="M7.2 16.3l3.6-3.6M13.3 9.5l3.4-3"/>',
    'star': '<path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z"/>',
    'seed': '<path d="M12 21v-8"/><path d="M12 13c0-4 3-7 8-7 0 5-3 7-8 7zM12 15c0-3-2.5-5-7-5 0 4 2.5 5 7 5z"/>',
    'repeat': '<path d="M4 12a8 8 0 0 1 14-5.3L20 9"/><path d="M20 4v5h-5"/><path d="M20 12a8 8 0 0 1-14 5.3L4 15"/><path d="M4 20v-5h5"/>',
    'dumbbell': '<path d="M6 7v10M18 7v10M3 10v4M21 10v4M6 12h12"/>',
    'up': '<path d="M4 20l6-8 4 4 6-9"/><path d="M15 7h5v5"/>',
    'target': '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="4"/><path d="M12 12l7-7M16 5h3v3"/>',
    'bar1': '<path d="M6 20v-5"/><path d="M12 20V10M18 20V4" opacity=".25"/>',
    'bar2': '<path d="M6 20v-5M12 20V10"/><path d="M18 20V4" opacity=".25"/>',
    'bar3': '<path d="M6 20v-5M12 20V10M18 20V4"/>',
    'bolt': '<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
    'cal': '<rect x="4" y="5" width="16" height="15" rx="2"/><path d="M4 10h16M9 3v4M15 3v4"/>',
    'clock': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    'spark': '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5L18 18M6 18l2.5-2.5M15.5 8.5L18 6"/>',
    'child': '<circle cx="12" cy="6" r="3"/><path d="M12 9v7M8 12h8M9 21l3-5 3 5"/>',
    'wall': '<path d="M4 21V5l8-2 8 2v16"/><circle cx="9" cy="9" r="1.2"/><circle cx="15" cy="12" r="1.2"/><circle cx="10" cy="16" r="1.2"/>',
    'pin': '<path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
    'pen': '<path d="M4 20h4L19 9l-4-4L4 16z"/><path d="M13 7l4 4"/>',
    'card': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 10h18M7 15h4"/>',
    'hand': '<path d="M7 11V6a1.5 1.5 0 0 1 3 0v4M10 10V4.5a1.5 1.5 0 0 1 3 0V10M13 10V5.5a1.5 1.5 0 0 1 3 0V12M16 9.5a1.5 1.5 0 0 1 3 0V14a7 7 0 0 1-7 7h-1a6 6 0 0 1-5-3l-2.5-4.5a1.5 1.5 0 0 1 2.5-1.6L7 13"/>',
}
CARD_ICO = {k: ico(_I[v]) for k, v in {
    'Безопасность': 'shield', 'Техника': 'shoe', 'Свобода': 'key', 'Уверенность': 'smile',
    'Знакомство': 'hand', 'Основы': 'book', 'Страховка': 'rope', 'Итог': 'flag', 'Инструктаж и разминка': 'shield', 'Первые трассы': 'route',
    'После пробной тренировки': 'star', 'Без опыта': 'seed', 'Для пары и друзей': 'people', 'Лазали когда-то давно': 'repeat',
    'Сила': 'dumbbell', 'Прогресс': 'up', 'Цели': 'target', 'Начальный': 'bar1', 'Средний': 'bar2', 'Продвинутый': 'bar3',
    'Хочется быстрее': 'bolt', 'Есть конкретная задача': 'target', 'Неудобно расписание групп': 'cal', 'Нужен свой темп': 'clock',
    'Новый скалодром': 'spark', 'Детские тренеры': 'child', 'Боулдеринг и трудность': 'wall', '7 минут от метро': 'pin',
    'Оставьте заявку': 'pen', 'Оплатите': 'card', 'Получатель записывается': 'cal'}.items()}

def cards(items, n=4, imgs=None):
    # imgs — фото сверху каждой карточки (горизонтальные кадры)
    return '<div class="lp-cards4%s">%s</div>' % (' lp-cards4--3' if n == 3 else '', ''.join(
        '<div class="lp-c%s reveal">%s<span class="lp-c__top">%s<span class="lp-c__n" aria-hidden="true">%02d</span></span><b>%s</b><p>%s</p></div>' % (
            ' lp-c--ph' if imgs else '', '<span class="lp-c__ph"><img src="assets/img/%s" alt="" loading="lazy"></span>' % imgs[i] if imgs else '',
            '<span class="lp-c__ic">%s</span>' % CARD_ICO[t] if t in CARD_ICO else '', i + 1, t, d) for i, (t, d) in enumerate(items)))

def li(items, cls='lp-list'):
    return '<ul class="%s">%s</ul>' % (cls, ''.join('<li>%s%s</li>' % (CHECK, x) for x in items))

def offer(title, items, desc, foot, badge='', dark=False, id='', img='', play=''):
    return '''<article class="lp-f%s reveal"%s>%s%s
  <h3 class="d lp-f__t">%s</h3>
  %s
  %s
  <div class="lp-f__foot">%s</div>
</article>''' % ((' lp-f--dark' if dark else '') + (' lp-f--img' if img else ''),' id="%s"' % id if id else '',
                 '<div class="lp-f__img"><img src="assets/img/%s" alt="" loading="lazy">%s</div>' % (img, play) if img else '',
                 '<span class="badge%s">%s</span>' % (' badge--dark' if dark else '', badge) if badge else '', title,
                 li(items, 'lp-list' + ('' if dark else ' lp-list--dark')) if items else '', '<p class="lp-f__d">%s</p>' % desc if desc else '', foot)

def offers(items, n=2):
    return '<div class="lp-formats%s">%s</div>' % (' lp-formats--3' if n == 3 else '', '\n'.join(items))

def steps(items):
    return '<ol class="lp-steps">%s</ol>' % ''.join('<li class="reveal"><span class="lp-steps__top"><span class="lp-steps__n">%02d</span>%s</span><b>%s</b><p>%s</p></li>' % (
        i + 1, '<span class="lp-steps__ic">%s</span>' % CARD_ICO[t] if t in CARD_ICO else '', t, d) for i, (t, d) in enumerate(items))

def plist(rows):
    # строка: (название, пояснение, цена[, ссылка на услугу]); нет ссылки — нет и «Подробнее»
    def row(r):
        go = '<a class="prow__go" href="%s">Подробнее%s</a>' % (r[3], ARROW) if len(r) > 3 and r[3] else ''
        return '<div class="prow%s"><p class="prow__n">%s</p><p class="prow__d">%s</p>%s<p class="prow__v">%s</p></div>' % (' prow--link' if go else '', r[0], r[1], go, r[2])
    return '<div class="plist reveal">%s</div>' % ''.join(row(r) for r in rows)

def faq(items):
    h = (len(items) + 1) // 2
    d = lambda its, first: ''.join('<details class="reveal"%s><summary>%s<i></i></summary><div class="faq__a"><p>%s</p></div></details>' % (' open' if first and i == 0 else '', q, a) for i, (q, a) in enumerate(its))
    return '<div class="faq"><div class="faq__col">%s</div><div class="faq__col">%s</div></div>' % (d(items[:h], True), d(items[h:], False))

def faq_sec(items, title='Частые вопросы'):
    return sec(sechead(title) + '\n' + faq(items), 'faq')

def gal(items, more_from=7):
    return '<div class="lp-gal">%s</div>%s' % (''.join(
        '<button class="lp-gal__i%s" type="button" data-i="%d" aria-label="Открыть фото: %s"><img src="assets/img/%s" alt="%s" loading="lazy"></button>' % (' is-more' if i >= more_from else '', i, a, f, a)
        for i, (f, a) in enumerate(items)), '<div class="lp-center"><button class="btn btn--sec js-gal-more" type="button" aria-expanded="false">Показать ещё</button></div>' if len(items) > more_from else '')

# ---------- Карточка тренера: по клику (Enter/пробел) открывается окно с описанием (js/landing.js, .js-coach) ----------
# Описание лежит в карточке скрытым блоком .lp-coach__bio — в MODX это поля тренера (о себе, специализация, с кем работает, достижения).
COACH_PLUS = '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>'
COACH_BIO_STUB = ('[Пара абзацев о&nbsp;тренере: как пришёл в&nbsp;скалолазание, какой опыт, как строит тренировки и&nbsp;что важно в&nbsp;работе с&nbsp;учениками.]',
                  '[Боулдеринг, трудность, страховка]', '[Новички, взрослые, дети, подготовка к&nbsp;соревнованиям]', '[Разряды, соревнования, выезды на&nbsp;скалы]')
def coach_card(n, r, q, img, bio=None):
    about, spec, who, ach = bio or COACH_BIO_STUB
    bio = ('<div class="lp-coach__bio" hidden><p class="cm__about">%s</p>'
           '<dl class="cm__facts"><div><dt>Специализация</dt><dd>%s</dd></div>'
           '<div><dt>С&nbsp;кем работает</dt><dd>%s</dd></div>'
           '<div><dt>Достижения</dt><dd>%s</dd></div></dl>' % (about, spec, who, ach) +
           '<button class="btn btn--primary js-join cm__go" type="button" aria-haspopup="dialog" aria-controls="join" data-join-title="Запись к&nbsp;тренеру">Записаться к&nbsp;тренеру</button></div>')
    return ('<article class="lp-coach reveal js-coach" tabindex="0" role="button" aria-haspopup="dialog" aria-label="Подробнее о тренере: %s">'
            '<div class="lp-coach__img"><img src="assets/img/%s" alt="Фото-заглушка" loading="lazy"><span class="lp-coach__plus">%s</span></div>'
            '<b class="lp-coach__n">%s</b><span class="lp-coach__r">%s</span><span class="lp-coach__q">%s</span>'
            '<span class="lp-coach__go">Подробнее о&nbsp;тренере</span>%s</article>') % (n.replace('&nbsp;', ' '), img, COACH_PLUS, n, r, q, bio)

def coaches(items):
    # фото — временные заглушки (не наши тренеры), заменить снимками тренеров К2
    return '<div class="lp-coaches">%s</div>' % ''.join(coach_card(c[0], c[1], c[2], 'coach-%d.jpg' % (i % 4 + 1), c[3] if len(c) > 3 else None) for i, c in enumerate(items))

NEXT_MARK = '<svg class="lp-next__mark" viewBox="19 24 698 322" aria-hidden="true"><path d="M716.4,59.9v89l-90,62.4l90-1v133.8h-347V219.8l90-35.4l-90-35.4V24.5h257L716.4,59.9z"/><path d="M167.4,167.2l23.7-143h146.3v4l-24,145h24v171H190.8l-23.3-141v141h-148v-320h148V167.2z"/></svg>'
def nextcta(h2, text, btn, orbit='оставьте заявку · перезвоним · '):
    """Блок-призыв в конце страницы — по шаблону «Уже занимались» (pervyj-raz): бледный знак К2 + надпись бежит по контуру кнопки"""
    return sec('<div class="lp-next lp-next--art reveal"><div><h2 class="d h2">%s</h2><p class="lead">%s</p></div>%s'
               '<div class="lp-orbit"><svg class="lp-orbit__ring" aria-hidden="true"><path fill="none"/><text><textPath data-t="%s"></textPath></text></svg>%s</div></div>' % (
                   h2, text, NEXT_MARK, orbit, btn), tone='neutral', cls='sec--flush')

def helpbox(b, text, btn):
    # заголовок плашки — отдельной крупной строкой, под ним мелкий текст, справа кнопка
    return '<div class="lp-help reveal"><div class="lp-help__txt"><b class="lp-help__t d">%s</b><p>%s</p></div>%s</div>' % (b, text, btn)

def tiles(items):
    """Карточки-ссылки на разделы: [(заголовок, подпись, ссылка, картинка)]"""
    return '<div class="ptiles">%s</div>' % ''.join(
        '<a class="ptile reveal" href="%s"><span class="ptile__img"><img src="assets/img/%s" alt="" loading="lazy"></span><span class="ptile__b"><b class="ptile__t">%s</b><span class="ptile__d">%s</span>'
        '<span class="ptile__f">%s<span class="go go--s">%s</span></span></span></a>' % (h, img, t, d, PRICE if pr else '<span></span>', ARROW) for t, d, h, img, pr in items)

CONTACT = sec(P['CONTACT'], 'contacts', cls='sec--flush')
REVIEWS = lambda t='Отзывы': sec(sechead(t) + '<div class="widget reveal"><b>Отзывы с&nbsp;Яндекс Карт и&nbsp;2ГИС</b><span>Здесь подключится виджет отзывов внешнего сервиса</span></div>', 'reviews', cls='lp-alt')
COACH_STUB = [('[Имя Фамилия]', 'Старший тренер', '[Квалификация · стаж]'), ('[Имя Фамилия]', 'Тренер по боулдерингу', '[Квалификация · стаж]'),
              ('[Имя Фамилия]', 'Тренер по трудности', '[Квалификация · стаж]'), ('[Имя Фамилия]', 'Детский тренер', '[Квалификация · стаж]')]
# Рыба: вымышленные тренеры (страница «Тренеры», детская секция): вымышленные тренеры и тексты-заглушки — заменить реальными данными скалодрома
COACH_FISH_ADULT = [
    ('Артём Соколов', 'Старший тренер', 'КМС по&nbsp;скалолазанию · стаж 10&nbsp;лет',
     ('Пришёл в&nbsp;скалолазание студентом и&nbsp;за&nbsp;десять лет прошёл путь от&nbsp;новичка до&nbsp;кандидата в&nbsp;мастера спорта. На&nbsp;тренировках начинает с&nbsp;техники и&nbsp;безопасности, а&nbsp;силу добавляет постепенно&nbsp;— так прогресс держится долго и&nbsp;без травм.',
      'Трудность, нижняя страховка, подготовка к&nbsp;соревнованиям', 'Взрослые новички и&nbsp;спортсмены', 'Призёр чемпионата Санкт-Петербурга, сотни трасс на&nbsp;скалах Крыма и&nbsp;Карелии')),
    ('Максим Лебедев', 'Тренер по боулдерингу', 'I&nbsp;спортивный разряд · стаж 6&nbsp;лет',
     ('Любит короткие сложные задачи и&nbsp;учит «читать» трассу до&nbsp;первого движения. Объясняет просто и&nbsp;с&nbsp;юмором, поэтому на&nbsp;его тренировках не&nbsp;страшно пробовать новое и&nbsp;ошибаться.',
      'Боулдеринг, техника движения, работа ног', 'Новички и&nbsp;те, кто лазает от&nbsp;года', 'Финалист городских фестивалей боулдеринга, постановщик трасс')),
    ('Илья Морозов', 'Тренер по трудности', 'Инструктор-методист · стаж 8&nbsp;лет',
     ('Отвечает за&nbsp;высокую стену: учит страховать, работать с&nbsp;верёвкой и&nbsp;не&nbsp;бояться высоты. Каждого ученика доводит до&nbsp;уверенного самостоятельного лазания на&nbsp;13&nbsp;метрах.',
      'Трудность, верхняя и&nbsp;нижняя страховка, выносливость', 'Взрослые, пары и&nbsp;группы', 'Инструктор по&nbsp;спортивному туризму, руководитель выездов на&nbsp;скалы')),
    ('Ольга Кузнецова', 'Тренер', 'Мастер спорта по&nbsp;скалолазанию · стаж 5&nbsp;лет',
     ('Сочетает лазание с&nbsp;ОФП и&nbsp;растяжкой: помогает стать сильнее и&nbsp;гибче без&nbsp;перегрузок. Строит тренировки под&nbsp;цель ученика&nbsp;— от&nbsp;первой трассы до&nbsp;подготовки к&nbsp;старту.',
      'ОФП, растяжка, персональные тренировки', 'Взрослые любого уровня', 'Чемпионка Северо-Западного округа, участница всероссийских соревнований')),
]
COACH_FISH_KIDS = [
    ('Дмитрий Орлов', 'Детский тренер', 'Педагог по&nbsp;физкультуре · стаж 7&nbsp;лет',
     ('Работает с&nbsp;младшей группой и&nbsp;превращает тренировку в&nbsp;игру: задания, эстафеты, маленькие победы на&nbsp;каждом занятии. Родители отмечают, что дети идут к&nbsp;нему с&nbsp;радостью.',
      'Игровые тренировки, координация, первые трассы', 'Дети 5–7 лет', 'Автор программы детских тренировок К2')),
    ('Никита Павлов', 'Детский тренер', 'I&nbsp;спортивный разряд · стаж 4&nbsp;года',
     ('Ведёт группу школьников: учит технике, страховке и&nbsp;командной работе. Следит, чтобы нагрузка была по&nbsp;возрасту, а&nbsp;каждый ребёнок видел свой прогресс.',
      'Техника, боулдеринг, основы страховки', 'Дети 8–10 лет', 'Подготовил воспитанников к&nbsp;первым городским стартам')),
    ('Сергей Волков', 'Детский тренер', 'КМС по&nbsp;скалолазанию · стаж 9&nbsp;лет',
     ('Тренирует подростков, которые хотят большего: соревнования, выезды на&nbsp;скалы, сложные трассы. Требовательный, но&nbsp;всегда на&nbsp;стороне ученика.',
      'Трудность, соревновательная подготовка, скалы', 'Подростки 11–16 лет', 'Ученики&nbsp;— призёры первенства города, ежегодные выезды в&nbsp;Карелию')),
    ('Анна Смирнова', 'Детский тренер', 'Тренер-преподаватель · стаж 5&nbsp;лет',
     ('Помогает детям, которые только пришли в&nbsp;секцию: спокойно знакомит с&nbsp;залом, правилами и&nbsp;первыми трассами. Особенно хорошо находит подход к&nbsp;стеснительным ребятам.',
      'Пробные тренировки, адаптация новичков, растяжка', 'Дети 5–10 лет', 'Провела больше 300&nbsp;пробных занятий для детей')),
]
GAL_HALL = [('p-blue.jpg', 'Синяя стена с нависанием'), ('p-mat.jpg', 'Отдых на матах'), ('p-cave.jpg', 'Под нависанием'),
            ('k2-first-1.jpg', 'Боулдеринг в зале'), ('p-roof.jpg', 'Лазание по потолку'), ('k2-first-2.jpg', 'Трасса на нависании'),
            ('k2-hall.jpg', 'Зал скалодрома К2'), ('p-dyno.jpg', 'Прыжок к зацепу'), ('k2-first-3.jpg', 'Вместе на скалодроме')]


# ---------- Страница целиком ----------
PAGES = []
def page(slug, title, desc, body, book=False, fab='', gallery=False):
    PAGES.append(slug)
    html = '''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(T)s</title>
<meta name="description" content="%(D)s">
<link rel="stylesheet" href="css/style.css?v=%(V)s">
<link rel="stylesheet" href="css/blog.css?v=%(V)s">
<link rel="stylesheet" href="css/landing.css?v=%(V)s">
</head>
<body class="page page--lp page--%(S)s">
%(HEADER)s

%(MMENU)s
%(SEARCH)s
<main class="lp">
%(BODY)s
</main>
%(FAB)s
%(FOOTER)s

%(OCC)s
%(JOIN)s
%(BOOK)s
%(LB)s
%(TIP)s

<script src="js/search.js?v=%(V)s"></script>
<script src="js/blog.js?v=%(V)s"></script>
<script src="js/landing.js?v=%(V)s"></script>
</body>
</html>
''' % dict(P, T=title, D=desc, V=VER, S=slug.replace('.html', ''), BODY=body, BOOK=BOOK if book else '', LB=P['LB'] if gallery else '', TIP=TIP,
           FAB='<!-- Всегда доступная кнопка записи -->\n' + fab.replace('class="btn btn--primary js-book"', 'class="lp-fab btn btn--primary js-book" aria-hidden="true" tabindex="-1"') if fab else '')
    io.open(os.path.join(ROOT, slug), 'w', encoding='utf-8').write(typograph(html))


# ======================= ДЛЯ ВЗРОСЛЫХ (хаб) =======================
FAQ_ADULT = [('С чего начать, если я никогда не лазал?', 'С пробной тренировки. Это час с тренером: опыт и своё снаряжение не нужны, а в конце вы поймёте, куда двигаться дальше.'),
             ('Чем базовый курс отличается от школы?', 'Курс — это 3–5 тренировок, чтобы освоить основы и научиться страховать. Школа — регулярные занятия для тех, кто хочет расти в технике и силе.'),
             ('Можно ли лазать самостоятельно?', 'Да, если вы уже умеете лазать и знаете правила безопасности. Есть разовые посещения и абонементы. Допуск&nbsp;— после базового курса или короткой проверки у&nbsp;тренера.'),
             ('Нужно ли своё снаряжение?', 'Нет. Скальные туфли, страховочную систему и магнезию выдадим на месте. Прокат&nbsp;— 400&nbsp;₽ за&nbsp;посещение, на&nbsp;пробной тренировке бесплатно.'),
             ('Есть ли ограничения по возрасту?', 'Взрослые программы — с 16 лет. Для детей от 5 лет есть детская секция и пробные тренировки.'),
             ('Как записаться?', 'Оставьте заявку или позвоните — администратор подберёт удобное время и формат.')]
body = hero([('Для взрослых', '')], 'Скалолазание для взрослых на скалодроме К2',
            'Впервые? Начните с пробной тренировки или базового курса. Уже лазаете — выбирайте школу, персональные тренировки с тренером или приходите сами.',
            'k2-05.jpg', [(I_SPARK, 'Любой уровень'), (I_GEAR, 'Снаряжение выдаём'), (I_PEOPLE, 'В группе или персонально'), (I_TIME, '7 дней в неделю')],
            join_btn('Подобрать тренировку', 'Подберём тренировку', 'trial') + link_btn('Цены', 'ceny.html', 'btn btn--sec'), 'Скалолаз на стене К2')
# Кнопка видео на фото «Первого раза» — ведёт к ролику на странице пробной тренировки
PLAY_FIRST = '<a class="lp-f__play" href="pervyj-raz.html#video"><i>' + ico('<path d="M8 5v14l11-7z"/>') + '</i><span class="lp-f__pl">Видео: как проходит первая тренировка</span><span class="lp-f__ps">Смотреть видео</span></a>'
body += sec('<h2 class="lp-k reveal">Новичкам</h2>\n' + offers([
    offer('Первый раз', ['для любого возраста от 16 лет', 'для любого уровня подготовки', 'всё снаряжение выдаём', '60 минут', 'персонально или в группе'],
          'Час с тренером: разберём основы и пройдём первые трассы.', price(1500, 1900) + link_btn('Подробнее', 'pervyj-raz.html', 'btn btn--primary'), 'Пробная тренировка', img='k2-first-3.jpg', play=PLAY_FIRST),
    offer('Базовые курсы', ['программа из 3–5 тренировок', 'всё снаряжение выдаём', 'персонально или в группе'],
          'Освоите боулдеринг, трудность и страховку — и сможете лазать без тренера.', price(6900) + link_btn('Подробнее', 'bazovye-kursy.html', 'btn btn--primary'), 'Курс', img='p-chalk.jpg')]) +
    '\n<h2 class="lp-k lp-k--gap reveal">Уже занимаюсь</h2>\n' + offers([
    offer('Тренировки в группе', ['регулярно, по расписанию', 'с тренером', 'техника, сила, прогресс'], 'Школа скалолазания: программа, группа своего уровня и заметный прогресс.',
          price(1200) + link_btn('Подробнее', 'shkola.html', 'btn btn--primary'), img='k2-first-1.jpg'),
    offer('Индивидуальные тренировки', ['персонально с тренером', 'под вашу задачу', 'удобное время'], 'Самый быстрый путь к цели — один на один с тренером.',
          price(3500) + link_btn('Подробнее', 'individualnye.html', 'btn btn--primary'), dark=True, img='p-cave.jpg'),
    offer('Самостоятельные посещения', ['разовые и абонементы', 'боулдеринг и трудность', 'прокат снаряжения'], 'Приходите, когда удобно, и лазайте в своём ритме.',
          price(900) + link_btn('Подробнее', 'samostoyatelno.html', 'btn btn--primary'), img='k2-hall.jpg')], 3), 'formats')
body += sec(sechead('Наш скалодром: боулдеринг и трудность', 'Нажмите на фото — откроется галерея', link_btn('О скалодроме', 'o-skalodrome.html', 'btn btn--sec reveal')) + '\n' + gal(GAL_HALL), 'photos', cls='lp-alt')
body += CONTACT + faq_sec(FAQ_ADULT)
page('dlya-vzroslyh.html', 'Скалолазание для взрослых — скалодром К2', 'Пробные тренировки, базовые курсы, школа скалолазания, индивидуальные тренировки и самостоятельные посещения для взрослых. Скалодром К2, м. Площадь Ленина.', body, gallery=True)


# ======================= БАЗОВЫЕ КУРСЫ =======================
body = hero([('Для взрослых', 'dlya-vzroslyh.html'), ('Базовые курсы', '')], 'Базовые курсы скалолазания',
            '3–5 тренировок с тренером — и вы лазаете и страхуете сами. От первых движений до высокой стены.',
            'k2-11.jpg', [(I_CAL, '3–5 тренировок'), (I_TIME, '[60] минут каждая'), (I_PEOPLE, 'В группе или персонально'), (I_GEAR, 'Снаряжение выдаём')],
            join_btn('Записаться на курс', 'Запись на базовый курс', 'trial') + link_btn('Программы', '#programs', 'btn btn--sec'), 'Трассы на высокой стене')
body += sec('<div class="lp-intro"><h2 class="d h2 reveal">Зачем курс, если есть разовые занятия</h2><p class="lead muted reveal">Пробная тренировка — знакомство. Курс — система: каждое занятие опирается на прошлое, и в конце вы выходите на стену без тренера.</p></div>\n' +
            cards([('Безопасность', 'Правила зала, страховка, работа с верёвкой — с первого занятия.'), ('Техника', 'Работа ног, положение тела, базовые движения на боулдеринге и трудности.'),
                   ('Свобода', 'После курса можно ходить в зал без тренера и лазать в паре.'), ('Уверенность', 'Тренер рядом, нагрузка растёт постепенно — без рывков и страха.')]), 'why')
packs = re.findall(r'<a class="pack" href="pakety\.html#([\w-]+)"><span class="pack__img"><img src="assets/img/([^"]+)".*?<span class="pack__t">(.*?)</span><span class="pack__d">(.*?)</span><span class="badges">(.*?)</span>', MAIN)
PK = {s: dict(img=i, t=t, d=d, b=re.findall(r'<span class="badge">(.*?)</span>', b)) for s, i, t, d, b in packs}
PACK_PRICE = {'start': (6900, 7500), 'baza': (8900, 9900), 'rasshirennyj': (11900, 12900), 'nizhnyaya-strahovka': (7900, 8900),
              'uroven': (9900, 10900), 'sila': (8900, 9900), 'vynoslivost': (8900, 9900), 'skaly': (9900, 10900), 'tehnika': (5900, 6500)}
def pack_offer(s, dark=False, btn=None):
    p = PK[s]
    if not btn and s in ('start', 'baza', 'rasshirennyj', 'nizhnyaya-strahovka'):  # у базовых курсов — своя страница (шаблон «Товар»)
        btn = link_btn('Подробнее', 'kurs-%s.html' % s, 'btn btn--primary')
    return offer(p['t'], p['b'], p['d'], price(*PACK_PRICE[s]) + (btn or join_btn('Записаться', 'Пакет «%s»' % re.sub('<[^>]+>', '', p['t']), 'trial')), dark=dark, id=s, img=p['img'])
body += sec(sechead('Программы курса', 'Выберите, с чего начать. Сомневаетесь — тренер подскажет на пробной тренировке.') + '\n' +
            offers([pack_offer('start'), pack_offer('baza'), pack_offer('rasshirennyj')], 3) + '\n' +
            helpbox('Уже умеете лазать с верхней страховкой?', 'Следующий шаг — курс «Нижняя страховка».', link_btn('Подробнее', 'kurs-nizhnyaya-strahovka.html')), 'programs')
# «Итог курса»: текст на тёмной панели (не поверх фото) + вертикальное фото высокой стены со шкалой 0→13 м; тексты — из hero, «Зачем курс» и «Как проходит»
KBAN_RES = [(I_CAL, '3–5 тренировок', 'С&nbsp;тренером, в&nbsp;группе или персонально'),
            (CARD_ICO['Страховка'], 'Страхуете напарника', 'Учимся на&nbsp;высокой стене'),
            (CARD_ICO['Свобода'], 'Лазаете самостоятельно', 'Можно ходить в&nbsp;зал без&nbsp;тренера')]
body += sec('<div class="kban reveal"><div class="kban__in"><span class="mark">Итог курса</span>'
            '<p class="kban__t d">От&nbsp;первых движений&nbsp;— до&nbsp;стены <b>13<small>м</small></b></p>'
            '<ul class="kban__res">' + ''.join('<li><span class="kban__ic">%s</span><span><b>%s</b><small>%s</small></span></li>' % x for x in KBAN_RES) + '</ul>'
            + join_btn('Записаться на курс', 'Запись на базовый курс', 'trial') + '</div>'
            '<div class="kban__ph"><img src="assets/img/p-wall.jpg" alt="Скалолазка на высокой стене скалодрома" loading="lazy">'
            '<div class="kban__scale" aria-hidden="true"><span style="--h:100%">13&nbsp;м</span><span style="--h:66%">10</span><span style="--h:33%">5</span><span style="--h:0%">0</span></div></div></div>', cls='sec--flush')
body += sec(sechead('Как проходит курс') + '\n' + steps([('Знакомство', 'Тренер узнаёт ваш опыт и цели, подбирает снаряжение.'), ('Основы', 'Правила безопасности, разминка и первые трассы на боулдеринге.'),
                                                         ('Страховка', 'Выходим на высокую стену и учимся страховать друг друга.'), ('Итог', 'Финальная проверка: вы лазаете и страхуете самостоятельно.')]) +
            '\n<div class="lp-after reveal"><p class="lp-after__t d">После курса вы:</p>' + li(['знаете правила безопасности на скалодроме', 'умеете страховать напарника', 'уверенно лазаете на боулдеринге и трудности', 'можете ходить в зал самостоятельно', 'знаете, как тренироваться дальше']) + '</div>', 'how', 'dark', 'stack')
body += sec(sechead('Для кого подходит') + '\n' + cards([('После пробной тренировки', 'Понравилось — и хочется научиться лазать по-настоящему.'), ('Без опыта', '«Старт» рассчитан на тех, кто ни разу не лазал.'),
                                                          ('Для пары и друзей', 'Пройдите курс вместе — и дальше страхуйте друг друга.'), ('Лазали когда-то давно', 'Вспомните технику и страховку за пару занятий.')], imgs=['k2-first-3.jpg', 'p-chalk.jpg', 'k2-first-2.jpg', 'p-cave.jpg']), 'who')
body += REVIEWS('Отзывы после курса') + faq_sec([('Сколько длится курс?', 'От 3 до 5 тренировок в зависимости от программы. [Срок и расписание уточняются.]'),
                                                  ('Можно ли пройти курс персонально?', 'Да, в группе или индивидуально с тренером.'),
                                                  ('Что будет, если пропущу занятие?', 'Предупредите администратора не&nbsp;позже чем за&nbsp;12 часов&nbsp;— перенесём на&nbsp;удобное время без доплаты.'), ('Нужна ли подготовка?', 'Нет. Достаточно удобной спортивной формы.')])
body += nextcta('Не знаете, какую программу выбрать?', 'Оставьте заявку — администратор подберёт курс под ваш опыт и цели.', join_btn('Оставить заявку', 'Поможем выбрать курс', 'trial', 'btn btn--light'), 'подберём курс · ответим на вопросы · ')
page('bazovye-kursy.html', 'Базовые курсы скалолазания для взрослых — скалодром К2', 'Курс из 3–5 тренировок: освоите боулдеринг, трудность и страховку. В группе или персонально, снаряжение выдаём.', body)


# ======================= ШКОЛА СКАЛОЛАЗАНИЯ =======================
body = hero([('Для взрослых', 'dlya-vzroslyh.html'), ('Школа скалолазания', '')], 'Школа скалолазания для взрослых',
            'Регулярные тренировки с тренером: техника, сила и новые уровни сложности — по программе, а не наугад.',
            'k2-04.jpg', [(I_CAL, 'По расписанию'), (I_UP, 'Рост по уровням'), (I_PEOPLE, 'Группы и персонально'), (I_SHIELD, 'Опытные тренеры')],
            join_btn('Записаться в школу', 'Запись в школу скалолазания', 'sub') + link_btn('Расписание', '#schedule', 'btn btn--sec'), 'Тренировка скалолаза')
body += sec('<div class="lp-intro"><h2 class="d h2 reveal">Чем школа отличается от пробной тренировки</h2><p class="lead muted reveal">Пробная тренировка — знакомство. В школе вы занимаетесь регулярно по программе: тренер видит ваш прогресс и ставит следующую цель.</p></div>\n' +
            cards([('Техника', 'Работа ног, баланс, умение «читать» трассу.'), ('Сила', 'ОФП и специальные упражнения для скалолазов.'), ('Прогресс', 'Каждый месяц — трассы сложнее.'), ('Цели', 'Подготовка к выездам на скалы и соревнованиям.')], imgs=['k2-first-1.jpg', 'p-chalk.jpg', 'k2-hall.jpg', 'k2-rock.jpg']), 'who')
# «Почему К2» — блок с «Первого раза» (фото на весь экран, цифры, шкала 0 → 13 м; логика — js/landing.js, setupWhy); кнопка — запись в школу
_pr = io.open(os.path.join(ROOT, 'pervyj-raz.html'), encoding='utf-8').read()
_a = _pr.index('<section class="lp-why2 dark" id="why">'); _b = _pr.index('</section>', _a) + len('</section>')
body += (_pr[_a:_b].replace('Почему первое занятие стоит провести в&nbsp;К2', 'Почему постоянные тренировки в&nbsp;К2&nbsp;— это ТОП!')
         .replace('<section class="lp-why2 dark" id="why">', '<section class="lp-why2 lp-why2--compact dark" id="why">', 1)
         .replace('<img src="assets/img/k2-rock.jpg"', '<img src="assets/img/p-boulder.jpg"', 1)
         .replace('<button class="btn btn--light js-book" type="button">Выбрать формат и&nbsp;записаться</button>',
                  join_btn('Записаться в&nbsp;школу', 'Запись в школу скалолазания', 'sub', 'btn btn--light')) + '\n')
body += sec(sechead('Форматы') + '\n' + offers([
    offer('Групповые тренировки', ['по расписанию', 'группа до 8 человек', 'с тренером', 'абонемент на 8 занятий'], 'Тренируйтесь в группе своего уровня — так прогресс идёт быстрее и веселее.', price(9600) + join_btn('Записаться', 'Групповые тренировки в школе', 'sub'), 'Регулярно', img='k2-first-3.jpg'),
    offer('Индивидуальные тренировки', ['персонально с тренером', 'под вашу цель', 'удобное время'], 'Один на один с тренером — самый быстрый прогресс.', price(3500) + link_btn('Подробнее', 'individualnye.html', 'btn btn--primary'), 'Персонально', dark=True, img='p-cave.jpg')]), 'formats', cls='stack')
body += sec(sechead('Уровни подготовки', 'Тренер определит уровень на первом занятии') + '\n' + cards([('Начальный', 'После пробной тренировки или базового курса: техника, страховка, первые трассы посложнее.'),
                                                                                                     ('Средний', 'Уверенно лазаете и страхуете, хотите сложнее: нижняя страховка, сила, новые категории.'),
                                                                                                     ('Продвинутый', 'Подготовка к соревнованиям и скалам: тренировки по плану, ОФП и разбор сложных трасс.')], 3), 'levels', 'dark', 'stack')
# Расписание групп школы — ПРИМЕРНОЕ (рыба); в MODX — таблица или виджет CRM
SCHOOL_SCHED = ('<div class="ksch reveal">' + ''.join('<div class="ksch__row"><b>%s</b><span class="d">%s</span><small>%s</small></div>' % r for r in [
    ('Начальный уровень', 'Пн, Ср · 19:00–20:30', 'Боулдеринг и&nbsp;трудность · тренер Максим Лебедев'),
    ('Средний уровень', 'Вт, Чт · 19:30–21:00', 'Трудность и&nbsp;нижняя страховка · тренер Илья Морозов'),
    ('Продвинутый уровень', 'Пн, Ср, Пт · 20:30–22:00', 'Подготовка к&nbsp;соревнованиям · тренер Артём Соколов'),
    ('Выходного дня', 'Сб · 12:00–13:30', 'Смешанная группа · тренер Ольга Кузнецова')]) +
    '<p class="ksch__note">Расписание примерное. Точное время и&nbsp;свободные места подскажет администратор.</p></div>')
body += sec(sechead('Расписание') + SCHOOL_SCHED, 'schedule')
# Видео: лента вертикальных роликов со стрелками, как на главной (листание — js/landing.js)
SH_DUR = ['0:52', '1:15', '2:10', '1:05', '1:40', '0:58']  # длительность роликов — рыба
SH_VIDEO = [('razminka', 'k2-07.jpg', 'Разминка и&nbsp;заминка'), ('sovety', 'k2-13.jpg', 'Советы новичку'), ('more', 'p-rope.jpg', 'Тренировка в&nbsp;школе'),
            ('more', 'p-dyno.jpg', 'Техника: работа ног'), ('more', 'k2-12.jpg', 'Сила и&nbsp;ОФП'), ('obzor', 'k2-01.jpg', 'Обзор скалодрома')]
SH_CTL = ('<div class="sechead__ctl reveal"><button class="ibtn ibtn--line js-prev" type="button" aria-label="Назад">' + ico('<path d="M19 12H5M11 6l-6 6 6 6"/>') + '</button>'
          '<button class="ibtn ibtn--line js-next" type="button" aria-label="Вперёд">' + ARROW + '</button>' + link_btn('Все видео', 'video.html') + '</div>')
body += ('<section class="sec dark videos stack" id="video"><div class="wrap">' + sechead('Видео с&nbsp;тренировок', '', SH_CTL) + '</div>'
         '<div class="shorts" tabindex="0" aria-label="Видео школы, листается">' + ''.join(
             '<a class="short" href="video.html#%s"><img src="assets/img/%s" alt="" loading="lazy"><span class="scrim"></span>'
             '<span class="play"><svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg></span><span class="short__c"><b>%s</b><small>%s</small></span></a>' % (x + (SH_DUR[i],)) for i, x in enumerate(SH_VIDEO)) + '</div></section>')
body += sec(sechead('Тренеры школы', '', link_btn('Все тренеры', 'trenery.html', 'btn btn--sec reveal')) + '\n' + coaches(COACH_FISH_ADULT), 'coaches', cls='lp-alt')
# Фотогалерея: высокие ячейки сетки (1, 5, 8) — вертикальные фото, остальные — горизонтальные
GAL_SCHOOL = [('p-wall.jpg', 'Скалолазка на высокой стене'), ('k2-first-1.jpg', 'Боулдеринг в зале'), ('p-chalk.jpg', 'Руки в магнезии'),
              ('k2-first-2.jpg', 'Трасса на нависании'), ('p-blue.jpg', 'Синяя стена с нависанием'), ('p-cave.jpg', 'Под нависанием'),
              ('k2-first-3.jpg', 'Вместе на скалодроме'), ('p-roof.jpg', 'Лазание по потолку'), ('k2-hall.jpg', 'Зал скалодрома К2')]
body += sec(sechead('Фотогалерея', 'Нажмите на фото — откроется галерея') + '\n' + gal(GAL_SCHOOL), 'photos')
body += REVIEWS('Отзывы и результаты') + faq_sec([('Можно ли прийти в школу без опыта?', 'Лучше начать с пробной тренировки или базового курса — тогда в школе вы сразу начнёте прогрессировать.'),
                                                   ('Как оплачивать занятия?', 'Абонементом на&nbsp;8 занятий: оплата на&nbsp;ресепшене или онлайн, срок действия&nbsp;— 30 дней.'),
                                                   ('Что, если пропущу тренировку?', 'Предупредите администратора не&nbsp;позже чем за&nbsp;12 часов&nbsp;— перенесём на&nbsp;удобное время без доплаты.'), ('Можно ли заниматься в любой день?', 'Группы занимаются по расписанию. Если неудобно — подойдут индивидуальные тренировки.')])
body += nextcta('Хотите тренироваться регулярно?', 'Оставьте заявку — подберём группу под ваш уровень и расписание.', join_btn('Оставить заявку', 'Запись в школу скалолазания', 'sub', 'btn btn--light'), 'группа под ваш уровень · ')
page('shkola.html', 'Школа скалолазания для взрослых — скалодром К2', 'Регулярные тренировки с тренером: техника, сила, подготовка к выездам и соревнованиям. Группы по уровням и индивидуальные занятия.', body, gallery=True)


# ======================= ИНДИВИДУАЛЬНЫЕ =======================
body = hero([('Для взрослых', 'dlya-vzroslyh.html'), ('Индивидуальные тренировки', '')], 'Индивидуальные тренировки с тренером',
            'Тренер работает только с вами: от первых шагов до подготовки к скалам и соревнованиям.',
            'k2-00.jpg', [(I_PEOPLE, 'Один на один'), (I_CAL, 'Удобное время'), (I_UP, 'Под вашу цель'), (I_SPARK, 'Любой уровень')],
            join_btn('Записаться', 'Индивидуальная тренировка'), 'Лазание на «клине»')
body += sec(sechead('Когда это лучший выбор') + '\n' + cards([('Хочется быстрее', 'Всё внимание тренера — только вам.'), ('Есть конкретная задача', 'Пройти трассу, освоить нижнюю страховку, подготовиться к выезду.'),
                                                             ('Неудобно расписание групп', 'Время подбираем под вас.'), ('Нужен свой темп', 'Нагрузка и программа — под ваш уровень.')]), 'who')
body += sec(sechead('Форматы и цены') + '\n' + offers([
    offer('Разовая тренировка', ['персонально с тренером', '60 минут', 'снаряжение включено'], 'Чтобы попробовать формат или решить одну конкретную задачу.', price(3500, frm=False) + join_btn('Записаться', 'Индивидуальная тренировка')),
    offer('Пакет тренировок', ['5 тренировок', 'программа под вашу цель', 'выгоднее разовых'], 'Для системного прогресса по плану.', price(15000, 17500, frm=False) + link_btn('Пакеты', 'pakety.html', 'btn btn--primary'), dark=True)]) + '\n' +
    helpbox('Вы новичок?', 'Персональная пробная тренировка для 1–3 участников — на странице «Первый раз».', link_btn('Первый раз', 'pervyj-raz.html')), 'formats', cls='stack')
body += sec(sechead('Тренеры', '', link_btn('Все тренеры', 'trenery.html', 'btn btn--sec reveal')) + '\n' + coaches(COACH_FISH_ADULT[:3] + COACH_FISH_KIDS[:1]), 'coaches', cls='lp-alt')
# Фотогалерея — стандартный блок после тренеров
body += sec(sechead('Фотогалерея', 'Нажмите на фото — откроется галерея', link_btn('О скалодроме', 'o-skalodrome.html', 'btn btn--sec reveal')) + gal(GAL_HALL), 'photos')
# Ответы — рыба (примерные условия), реальные даст скалодром
body += CONTACT + faq_sec([('Можно ли прийти вдвоём?', 'Да, можно заниматься вдвоём или втроём с одним тренером&nbsp;— цена за человека ниже, чем на персональной тренировке. Для новичков есть персональная пробная тренировка для 1–3 человек.'),
                           ('Можно ли выбрать тренера?', 'Да, укажите это в заявке.'), ('Как перенести тренировку?', 'Предупредите администратора не позже чем за 12 часов&nbsp;— перенесём на удобное время без доплаты.'), ('Нужно ли своё снаряжение?', 'Нет, выдадим на месте.')])
page('individualnye.html', 'Индивидуальные тренировки по скалолазанию — скалодром К2', 'Персональные тренировки с тренером под вашу цель и в удобное время. Скалодром К2, м. Площадь Ленина.', body, gallery=True)


# ======================= САМОСТОЯТЕЛЬНЫЕ =======================
body = hero([('Для взрослых', 'dlya-vzroslyh.html'), ('Самостоятельные посещения', '')], 'Самостоятельные посещения',
            'Уже умеете лазать? Приходите, когда удобно: боулдеринг и трудность — разово или по абонементу.',
            'k2-01.jpg', [(I_TIME, 'Ежедневно 7:00–23:00'), (I_CAL, 'Разово или абонемент'), (I_GEAR, 'Прокат снаряжения'), (I_SHIELD, 'Нужен допуск')],
            link_btn('Цены', '#prices', 'btn btn--primary') + link_btn('Правила посещения', DOC_URL['pravila'], 'btn btn--sec'), 'Скалолаз под нависанием')
# «Кто может лазать сам»: пропуск-чеклист + красная карточка «Не уверены?»
I_ROPE = ico('<path d="M9 3h6l-1 5a2 2 0 0 1-4 0z"/><path d="M12 10v3"/><circle cx="12" cy="17" r="4"/>')
WHO = [(I_UP, 'Умеете лазать', 'Прошли пробную тренировку, базовый курс или&nbsp;лазали где-то ещё.', 'Боулдеринг и&nbsp;трудность'),
       (I_SHIELD, 'Знаете технику безопасности', 'Перед первым посещением&nbsp;— короткий инструктаж у&nbsp;администратора, 10&nbsp;минут.', 'Боулдеринг и&nbsp;трудность'),
       (I_ROPE, 'Умеете страховать', 'Нужен допуск к&nbsp;страховке и&nbsp;напарник. На&nbsp;трассах с&nbsp;автостраховкой&nbsp;— не&nbsp;нужен. Допуск&nbsp;— после базового курса или короткой проверки у&nbsp;тренера.', 'Трудность с&nbsp;верёвкой')]
body += sec(sechead('Кто может лазать самостоятельно') + '<div class="who">'
    '<div class="who__pass reveal"><div class="who__head"><span class="who__k">Допуск</span><b class="d">Самостоятельное лазание</b><span class="who__hint">Нужно всё по&nbsp;списку</span></div><ul class="who__list">' + ''.join(
        '<li><span class="who__ic">%s</span><div><b>%s</b><p>%s</p></div><span class="who__z">%s</span><span class="who__ok" aria-hidden="true">%s</span></li>' % (ic, t, d, z, CHECK) for ic, t, d, z in WHO) + '</ul></div>'
    '<div class="who__help reveal"><span class="who__q d">?</span><b class="d">Не&nbsp;уверены?</b><p>Начните с&nbsp;базового курса: за&nbsp;3–5 тренировок научим лазать, страховать и&nbsp;всему необходимому.</p>'
    + link_btn('Базовые курсы', 'bazovye-kursy.html', 'btn btn--light') + '</div></div>', 'who')
# Зоны: две карточки с фото, факты с иконками и главное условие
I_MAT = ico('<rect x="3" y="14" width="18" height="6" rx="2"/><path d="M7 14V9l3-4 3 3 4-2"/>')
I_HEIGHT = ico('<path d="M12 3v18M8 7l4-4 4 4M8 17l4 4 4-4"/>')
I_SOLO = ico('<circle cx="12" cy="7" r="3"/><path d="M6 20a6 6 0 0 1 12 0"/>')
ZONES = [('Боулдеринг', 'Без страховки', 'k2-first-1.jpg', 'o-skalodrome.html#bouldering',
          [(I_MAT, 'Невысокие трассы над&nbsp;матами'), (I_SPARK, 'Без верёвки и&nbsp;снаряжения для страховки'), (I_SOLO, 'Можно прийти одному')],
          'Короткие задачи: лазаете, спрыгиваете на&nbsp;мат, пробуете снова.', 'Подойдёт, если вы&nbsp;пришли без&nbsp;напарника'),
         ('Трудность', 'Со страховкой', 'k2-hall.jpg', 'o-skalodrome.html#trudnost',
          [(I_HEIGHT, 'Стены 13&nbsp;метров'), (I_ROPE, 'Лазание со&nbsp;страховкой верёвкой'), (I_PEOPLE, 'Вдвоём: один лезет, второй страхует')],
          'Длинные трассы на&nbsp;высокой стене.', 'Для трасс с&nbsp;верёвкой нужен напарник и&nbsp;допуск к&nbsp;страховке')]
# Трудность в одиночку: зона с автостраховками — акцентная плашка в карточке «Трудность»
I_AUTO = ico('<circle cx="12" cy="8" r="5"/><path d="M12 5v3l2 1.5"/><path d="M12 13v8"/><path d="M9.5 18.5L12 21l2.5-2.5"/>')
ZN_AUTO = ('<div class="zn__auto"><span class="zn__auto-ic">%s</span><div><b class="d">Пришли один? Есть автостраховки</b>'
           '<p>В&nbsp;зоне трудности есть трассы с&nbsp;автостраховкой: устройство само выбирает верёвку и&nbsp;плавно опускает вас вниз. Напарник не&nbsp;нужен&nbsp;— можно лазать на&nbsp;высоту в&nbsp;одиночку. Таких трасс&nbsp;— 8, перед первым использованием&nbsp;— короткий инструктаж.</p></div></div>') % I_AUTO
body += sec(sechead('Какие зоны доступны', 'Для самостоятельных посещений открыты обе зоны&nbsp;— условия у&nbsp;них разные.') + '<div class="zn">' + ''.join(
    '<article class="zn__c reveal"><a class="zn__ph" href="%s"><img src="assets/img/%s" alt="" loading="lazy"><span class="zn__tag">%s</span><b class="zn__t d">%s</b></a>'
    '<div class="zn__b"><ul class="zn__f">%s</ul>%s<p class="zn__d">%s</p><p class="zn__must">%s<span>%s</span></p>%s</div></article>' % (
        h, img, tag, t, ''.join('<li><span class="zn__ic">%s</span>%s</li>' % f for f in facts), ZN_AUTO if k == 1 else '', d, I_SHIELD if k == 1 else CHECK, must, link_btn('О зоне', h, 'btn btn--sec'))
    for k, (t, tag, img, h, facts, d, must) in enumerate(ZONES)) + '</div>'
    # после карточек зон — ссылка на страницу «О скалодроме»
    '<div class="lp-center zn__more reveal">' + link_btn('Больше информации о&nbsp;скалодроме', 'o-skalodrome.html', 'btn btn--light') + '</div>', 'zones', 'dark', 'stack')
body += sec('<div class="prices__grid"><div class="prices__main">' + sechead('Разовое посещение и абонементы') + plist([
    ('Разовое посещение', 'Самостоятельно, боулдеринг и трудность', '900 ₽'), ('Абонемент на месяц', 'Безлимит самостоятельных посещений', '6 500 ₽'),
    ('Абонемент на 8 посещений', 'Самостоятельные посещения, 2 месяца', '5 600 ₽'), ('Прокат снаряжения', 'Скальники, страховочная система', '400 ₽')]) +
    '<div class="prices__all reveal">' + link_btn('Все цены', 'ceny.html') + '</div></div><aside class="prices__aside"><div class="note reveal"><b>Часы посещения</b><p>Ежедневно, 7:00–23:00</p>' +
    link_btn('Правила посещения', DOC_URL['pravila'], 'btn btn--light') + '</div></aside></div>', 'prices')
# Фотогалерея — стандартный блок (как на «Для взрослых»): клик по фото — во весь экран
body += sec(sechead('Фотогалерея', 'Нажмите на фото — откроется галерея', link_btn('О скалодроме', 'o-skalodrome.html', 'btn btn--sec reveal')) + gal(GAL_HALL), 'photos', cls='lp-alt')
body += CONTACT + faq_sec([('Нужно ли записываться заранее?', 'Не&nbsp;обязательно&nbsp;— приходите в&nbsp;часы работы. В&nbsp;вечерний пик лучше позвонить и&nbsp;уточнить загрузку зала.'), ('Можно ли прийти без напарника?', 'Да. Без напарника можно лазать на боулдеринге и на трассах с автостраховкой в зоне трудности. Для остальных трасс трудности нужен напарник с допуском к страховке.'),
                           ('Что входит в прокат?', 'Скальные туфли, страховочная система, мешочек для&nbsp;магнезии.'), ('Есть ли раздевалка и душ?', 'Да: раздевалки, душевые, шкафчики, аренда полотенец.')])
page('samostoyatelno.html', 'Самостоятельные посещения скалодрома — К2', 'Разовые посещения и абонементы для тех, кто умеет лазать: боулдеринг и трудность, прокат снаряжения. Скалодром К2.', body, gallery=True)


# ======================= ДЛЯ ДЕТЕЙ (хаб) =======================
FAQ_KIDS = [('С какого возраста можно?', 'С 5 лет: есть детские пробные тренировки и регулярная секция.'),
            ('Это безопасно?', 'Да. Дети лазают под присмотром тренера: на боулдеринге — над мягкими матами, на высокой стене — только со страховкой.'),
            ('Что взять ребёнку?', 'Только удобную спортивную форму. Снаряжение выдадим на месте.'),
            ('Можно ли родителям остаться?', 'Да, родители могут посмотреть занятие из&nbsp;зоны для&nbsp;зрителей или подождать в&nbsp;зоне отдыха.'),
            ('Можно ли полазать вместе с ребёнком?', 'Да, есть формат «Взрослый + ребёнок».'),
            ('Как записаться?', 'Оставьте заявку или позвоните — подберём удобное время.')]
body = hero([('Для детей', '')], 'Скалолазание для детей на скалодроме К2',
            'Можно просто попробовать на пробной тренировке или заниматься регулярно в детской секции. С 5 лет, с детскими тренерами.',
            'k2-02.jpg', [(I_CHILD, 'От 5 лет'), (I_SHIELD, 'Детские тренеры'), (I_GEAR, 'Снаряжение выдаём'), (I_PEOPLE, 'Можно с родителями')],
            join_btn('Подобрать занятие', 'Занятие для ребёнка', 'kids'), 'Скалолазка на стене')
KA = '<svg class="ico" viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
klnk = lambda h, t, d: '<a class="lnk" href="%s"><span><b>%s</b><small>%s</small></span><i>%s</i></a>' % (h, t, d, KA)
# Карточки форматов как блок «Скалодром для любых целей» на главной
KGOALS = ('<div class="goals">'
    '<div class="card g6 r2 reveal"><picture><source media="(max-width: 767px)" srcset="assets/img/k2-10.jpg"><img src="assets/img/k2-first-2.jpg" alt="" loading="lazy"></picture><div class="scrim"></div>'
    '<div><p class="card__t">Детская секция</p><p class="card__s">Регулярные тренировки с&nbsp;тренером, 5–16&nbsp;лет</p></div><div class="links">'
    + klnk('detskaya-sekciya.html#groups', 'Группы по&nbsp;возрасту', '5–7, 8–10 и&nbsp;11–16&nbsp;лет')
    + klnk('detskaya-sekciya.html#schedule', 'Расписание и&nbsp;цены', 'Выберите группу и&nbsp;удобные дни')
    + klnk('detskaya-sekciya.html#abonementy', 'Абонементы', 'Для каждой возрастной группы')
    + '</div></div>'
    '<div class="card g6 reveal"><img src="assets/img/p-mat.jpg" alt="" loading="lazy"><div class="scrim"></div>'
    '<div><p class="card__t">Первый раз</p><p class="card__s">Попробовать и&nbsp;понять, нравится&nbsp;ли</p></div><div class="links links--row">'
    + klnk('deti-pervyj-raz.html', 'Пробная тренировка', 'Ребёнок с&nbsp;тренером')
    + klnk('deti-pervyj-raz.html#family', 'Взрослый + ребёнок', 'Тренировка для всей семьи')
    + '</div></div>'
    '<a class="card g3 reveal" href="meropriyatiya.html#kids"><img src="assets/img/p-cave.jpg" alt="" loading="lazy"><div class="scrim"></div>'
    '<div><p class="card__t card__t--s">Мероприятия для&nbsp;детей</p><p class="card__s">Соревнования и&nbsp;события на&nbsp;скалодроме</p></div><span class="arr">' + KA + '</span></a>'
    '<a class="card card--raised g3 reveal" href="ceny.html#deti"><svg class="card__deco" viewBox="0 0 16 26" aria-hidden="true"><path d="M0 0l16 13L0 26V17l5-4-5-4z"/></svg>'
    '<div><p class="card__t card__t--s">Цены для&nbsp;детей</p><p class="card__s">Секция, пробные и&nbsp;абонементы</p></div><span class="arr">' + KA + '</span></a>'
    '</div>')
body += sec(sechead('Выберите формат') + '\n' + KGOALS, 'formats')
body += sec(sechead('Почему детям нравится в К2') + '\n' + cards([('Новый скалодром', 'Новые стены, зацепы и снаряжение.'), ('Детские тренеры', 'Объясняют просто, следят за безопасностью и не дают заскучать.'),
                                                                 ('Боулдеринг и трудность', 'Невысокие трассы над матами и высокие стены со страховкой.'), ('7 минут от метро', 'Удобно привозить ребёнка после школы.')]), 'why', 'dark', 'stack')
body += CONTACT + faq_sec(FAQ_KIDS)
page('dlya-detej.html', 'Скалолазание для детей — скалодром К2', 'Детская секция и пробные тренировки для детей от 5 лет, тренировки «взрослый + ребёнок». Скалодром К2, м. Площадь Ленина.', body)


# ======================= ДЕТСКАЯ СЕКЦИЯ =======================
# Тексты и порядок блоков — по ТЗ «ДЕТСКАЯ СЕКЦИЯ.docx»
TRIAL_TITLE = 'Пробное занятие в детской секции'
def trial_btn(text='Записать ребёнка на пробное', title=TRIAL_TITLE, cls='btn btn--primary'):
    return join_btn(text, title, 'kids', cls)
KGROUPS = [('5', '5–7 лет', 'дошкольники', '60 минут', 'Знакомство со скалолазанием через понятные задания и игровые упражнения. Учимся двигаться на стене, слушать тренера и соблюдать правила занятия.'),
           ('8', '8–10 лет', 'школьники', '90 минут', 'Осваиваем основные движения, пробуем разные трассы и учимся находить свои решения. Постепенно переходим от первых попыток к более сложным задачам.'),
           ('11', '11–16 лет', 'подростки', '90 минут', 'Работаем над техникой и прохождением трасс. Учимся разбирать свои попытки, выбирать следующий шаг и ставить тренировочные цели.')]
# Фото над карточками групп (временные; финальные — дети этого возраста на тренировке)
KPH = {'5': ('k2-first-3.jpg', 'Дошкольники 5–7 лет на тренировке: игровое задание с тренером'),
       '8': ('k2-first-2.jpg', 'Школьники 8–10 лет: тренер разбирает трассу с группой'),
       '11': ('k2-first-1.jpg', 'Подросток 11–16 лет проходит трассу на скалодроме')}
def tabs(name, items):
    return '<div class="ktabs reveal" data-tabs="%s">%s</div>' % (name, ''.join('<button class="chip" type="button" data-t="%s" aria-pressed="%s">%s</button>' % (k, 'true' if i == 0 else 'false', t) for i, (k, t) in enumerate(items)))

# 1. Первый экран
body = hero([('Для детей', 'dlya-detej.html'), ('Детская секция', '')], 'Детская секция скалолазания в К2 — от 5 до 16 лет',
            'Регулярные тренировки в трёх возрастных группах. Начните с пробного занятия в секции, познакомьтесь с форматом и выберите абонемент для дальнейших тренировок.',
            'k2-10.jpg', [(I_CHILD, 'Группы 5–7, 8–10 и 11–16 лет'), (I_TIME, 'Занятия 60 или 90 минут'), (I_CAL, 'Абонементы на месяц')],
            trial_btn() + link_btn('Посмотреть группы и расписание', '#groups', 'btn btn--sec'), 'Ребёнок на скалодроме')
# 2. Промо
body += sec('<div class="kpromo reveal"><figure class="kpromo__img"><img src="assets/img/k2-first-2.jpg" alt="Занятие на скалодроме" loading="lazy"><span class="kpromo__tag">Сезон 2027</span></figure>'
            '<div class="kpromo__b"><h2 class="d h2">Идёт набор детей на сезон 2027</h2>' + li(['От 5 до 16 лет', 'Разделение по группам', 'Удобный гибкий график', 'Большой выбор абонементов']) +
            '<p class="kpromo__k">Записаться на пробную тренировку:</p>' + trial_btn('Оставить заявку', 'Набор на сезон 2027', 'btn btn--primary') + '</div></div>', 'promo-season')
# 3. Группы
body += sec(sechead('Своя группа для каждого возраста', 'В секции три возрастные группы. Для детей 5–7 лет занятие длится 60 минут, для школьников и подростков — 90 минут.') +
            '<div class="kgrp">' + ''.join(
                '<article class="kgrp__c reveal"><span class="kgrp__ph"><img src="assets/img/%s" alt="%s" loading="lazy"></span><div class="kgrp__top"><b class="d kgrp__age">%s</b><span class="badge">%s</span></div><p class="kgrp__who">%s</p><p class="kgrp__d">%s</p>'
                '<a class="kgrp__go" href="#schedule" data-tab-go="schedule:%s">Группа %s: расписание и цена%s</a></article>' % (KPH[k][0], KPH[k][1], t, m, w, d, k, t, ARROW) for k, t, w, m, d in KGROUPS) + '</div>', 'groups')
# 4. Расписание — ПРИМЕРНОЕ (рыба): дни, время, зал и тренер. В MODX — таблица или виджет CRM
KSCHED = {'5': [('Вторник, четверг', '17:00–18:00', 'Зал боулдеринга · тренер Дмитрий Орлов'), ('Суббота', '11:00–12:00', 'Зал боулдеринга · тренер Анна Смирнова')],
          '8': [('Понедельник, среда', '17:30–19:00', 'Боулдеринг и&nbsp;трудность · тренер Никита Павлов'), ('Суббота', '12:30–14:00', 'Боулдеринг и&nbsp;трудность · тренер Никита Павлов')],
          '11': [('Вторник, четверг', '18:30–20:00', 'Трудность, 13&nbsp;м · тренер Сергей Волков'), ('Воскресенье', '12:00–13:30', 'Трудность и&nbsp;ОФП · тренер Сергей Волков')]}
body += sec('<p class="lp-k reveal">Расписание</p>' + sechead('Выберите группу и удобное время', 'Регулярные занятия проходят по абонементам. Посмотрите расписание своей возрастной группы и доступное количество тренировок в месяц.') +
            tabs('schedule', [(k, t) for k, t, _, _, _ in KGROUPS]) +
            ''.join('<div class="ksch reveal in" data-tab-of="schedule" data-t="%s"%s>%s<p class="ksch__note">Расписание примерное. Точное время и&nbsp;свободные места подскажет администратор.</p></div>' % (
                k, '' if i == 0 else ' hidden', ''.join('<div class="ksch__row"><b>%s</b><span class="d">%s</span><small>%s</small></div>' % r for r in KSCHED[k]))
                for i, (k, t, _, _, _) in enumerate(KGROUPS)), 'schedule', cls='lp-alt')
# 5. Абонементы: карточка переворачивается по клику (список абонементов уточняется)
# Условия абонемента — ПРИМЕРНЫЕ (рыба)
ABO_BACK = [('Срок действия', '30 дней с&nbsp;первого занятия'), ('Порядок записи', 'Заявка на&nbsp;сайте или по&nbsp;телефону, место в&nbsp;группе закрепляется после оплаты'),
            ('Пропуски и переносы', 'По&nbsp;болезни&nbsp;— перенос в&nbsp;пределах срока абонемента, если предупредить до&nbsp;начала занятия'),
            ('Снаряжение', 'Включено: скальные туфли, система, каска'), ('Дополнительные платежи', 'Нет')]
ABO_PRICE = {'5': (8, 7200), '8': (8, 8400), '11': (8, 8800)}  # (тренировок в месяц, цена) — ПРИМЕРНЫЕ
TURN = ico('<path d="M4 12a8 8 0 0 1 14-5.3L20 9"/><path d="M20 4v5h-5"/><path d="M20 12a8 8 0 0 1-14 5.3L4 15"/><path d="M4 20v-5h5"/>')
ABO_PH = {'5': 'p-fun.jpg', '8': 'k2-09.jpg', '11': 'k2-11.jpg'}
def abo(k, t, m):
    """Карточка абонемента: метка, фото группы, крупный возраст, условия с иконками, цена; по клику переворачивается на условия"""
    age = t.replace(' лет', '')
    return ('<button class="abo reveal" type="button" aria-pressed="false" aria-label="Абонемент для группы %s: подробнее об условиях"><span class="abo__in">'
            '<span class="abo__s abo__f"><span class="abo__top"><span class="abo__tag"><i></i>Абонемент</span><img class="abo__ph" src="assets/img/%s" alt="" loading="lazy"></span>'
            '<span class="abo__age d">%s<small>лет</small></span>'
            '<span class="abo__fs"><span class="abo__fi">%s<span>%d тренировок в&nbsp;месяц</span></span><span class="abo__fi">%s<span>Занятие %s</span></span></span>'
            '<span class="abo__pr"><span class="abo__p d">%s</span><span class="abo__n">В стоимость входит: тренировки с&nbsp;тренером, снаряжение и&nbsp;страховка. Срок действия: 30 дней.</span></span>'
            '<span class="abo__turn">Условия абонемента%s</span></span>'
            '<span class="abo__s abo__r"><span class="abo__g">Для группы %s</span>%s<span class="abo__turn">Назад%s</span></span></span></button>') % (
        t, ABO_PH[k], age, I_CAL, ABO_PRICE[k][0], I_TIME, m, rub(ABO_PRICE[k][1]), TURN, t, ''.join('<span class="abo__row"><b>%s</b><span>%s</span></span>' % x for x in ABO_BACK), TURN)
body += sec(sechead('Абонементы') + '<div class="abos">' + ''.join(abo(k, t, m) for k, t, _, m, _ in KGROUPS) + '</div>', 'abonementy', 'dark', 'stack')
# 6. Навыки
# Иконки навыков: фигура на стене, маршрут по точкам, мишень
KSK_ICO = [I_CHILD, ico('<circle cx="6" cy="18" r="2"/><circle cx="12" cy="11" r="2"/><circle cx="18" cy="5" r="2"/><path d="M7.2 16.3l3.6-3.6M13.3 9.5l3.4-3"/>'),
           ico('<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="4"/><path d="M12 12l7-7M16 5h3v3"/>')]
KSKILLS = [('Управлять движением', 'Находить опору, переносить вес и выбирать положение тела на стене.', 'Координация, выносливость, сила!'),
           ('Разбираться в задаче', 'Смотреть на трассу, пробовать разные движения и искать подходящий способ прохождения.', 'Логическое мышление, внимательность, пытливость!'),
           ('Работать над своей попыткой', 'Замечать, что получилось, разбирать сложности и пробовать снова с учётом подсказок тренера.', 'Дисциплина, усидчивость, целеустремлённость!')]
body += sec(sechead('Ключевые навыки, которые развиваем у детей', 'В секции занятия продолжают друг друга: дети знакомятся с движениями, пробуют разные способы прохождения трасс и возвращаются к задачам, которые пока не получились.') +
            '<div class="ksk">' + ''.join('<article class="ksk__c reveal"><span class="ksk__n d" aria-hidden="true">%02d</span><span class="ksk__ic">%s</span><b class="ksk__t d">%s</b><p class="ksk__d">%s</p><ul class="ksk__q">%s</ul></article>' % (
                i + 1, KSK_ICO[i], t, d, ''.join('<li>%s</li>' % w.strip(' !').capitalize() for w in q.split(','))) for i, (t, d, q) in enumerate(KSKILLS)) + '</div>', 'skills', cls='stack')
# 7. Пробная
body += sec('<div class="ktrial"><figure class="ktrial__img reveal"><img src="assets/img/k2-02.jpg" alt="Занятие в детской секции" loading="lazy"></figure><div class="ktrial__b">'
            '<p class="lp-k reveal">Пробная тренировка в секции</p><h2 class="d h2 reveal">Сначала попробуйте занятие в секции</h2>'
            '<p class="lead muted reveal">Пробная тренировка проходит в общей группе соответствующего возраста. Ребёнок знакомится с тренером и форматом занятий, а вы можете решить, подходит ли ему секция.</p>'
            '<p class="ktrial__mark reveal">Это занятие в группе секции, а не индивидуальная тренировка.</p>'
            '<dl class="ktrial__list reveal"><div><dt>Стоимость</dt><dd>' + price(1200, 1500, frm=False) + '</dd></div>'
            '<div><dt>Продолжительность</dt><dd>60–90 минут, зависит от возраста</dd></div><div><dt>В стоимость входит</dt><dd>Всё снаряжение, работа тренера</dd></div></dl>'
            '<div class="reveal">' + trial_btn() + '</div></div></div>' +
            helpbox('Остались вопросы?', 'Свяжитесь с нами — ответим и поможем определиться.', link_btn('Связаться с нами', '#contacts')), 'trial', cls='lp-alt')
# 8. Документы
I_DOC = ico('<path d="M7 3h7l5 5v13H7z"/><path d="M14 3v5h5M10 13h6M10 17h6"/>')
KDOCS = [('zayavlenie', I_DOC, 'Заявление от&nbsp;родителей', 'Согласие родителя или законного представителя на&nbsp;занятия ребёнка в&nbsp;секции.', 'Заполняет родитель'),
         ('tb', I_SHIELD, 'Техника безопасности', 'Как вести себя на&nbsp;скалодроме: страховка, маты, зоны лазания. Лучше прочитать вместе с&nbsp;ребёнком.', 'Читаем вместе с&nbsp;ребёнком')]
KSTEPS = [('Прочитайте документы', 'Заявление и&nbsp;технику безопасности&nbsp;— кнопкой «Открыть» у&nbsp;каждого документа.'),
          ('Подпишите заявление', 'Его заполняет родитель или законный представитель ребёнка.'),
          ('Возьмите спортивную форму', 'Удобную одежду для движения. Снаряжение выдадим на&nbsp;месте.')]
# Блок «Документы и материалы для родителей» — общий: стоит в детской секции и на детской пробной
KDOC_SEC = sec(sechead('Документы и материалы для родителей', 'Всё, что понадобится до&nbsp;первого занятия: документы можно открыть и&nbsp;распечатать заранее.') + '<div class="kdoc">'
    '<div class="kdoc__list">' + ''.join(
        '<article class="kdoc__c reveal"><span class="kdoc__ic">%s</span><div class="kdoc__b"><b class="kdoc__t d">%s</b><p>%s</p>'
        '<p class="kdoc__meta"><span>%s</span><span>Редакция от&nbsp;1&nbsp;сентября 2026</span></p></div>'
        '<a class="btn btn--sec kdoc__go" href="%s">Открыть%s</a></article>' % (ic, t, d, who, DOC_URL[k], ARROW) for k, ic, t, d, who in KDOCS) + '</div>'
    '<aside class="kdoc__side reveal"><p class="kdoc__st d">Перед первым занятием</p><ol class="kdoc__steps">' + ''.join(
        '<li><b>%s</b><span>%s</span></li>' % x for x in KSTEPS) + '</ol>'
    '<p class="kdoc__more">Другие документы: <a href="%s">Правила посещения</a>' % DOC_URL['pravila'] + ', <a href="%s">Договор оферты</a>' % DOC_URL['oferta'] + '</p>'
    + join_btn('Задать вопрос по&nbsp;документам', 'Вопрос по документам', 'kids', 'btn btn--light') + '</aside></div>', 'docs')
body += KDOC_SEC
# 9. Тренеры
body += sec(sechead('Тренеры детской секции', '', link_btn('Все тренеры', 'trenery.html', 'btn btn--sec reveal')) + '\n' + coaches(COACH_FISH_KIDS), 'coaches', cls='lp-alt')
# 10. Выезды и соревнования
body += sec(sechead('Выезды на скалы и соревнования') + offers([
    offer('На настоящие скалы — в школьные каникулы', [], 'Секция проводит детские выезды на скалы в Ленинградскую область и Карелию. Это возможность познакомиться с лазанием на естественном рельефе вместе с секцией.',
          link_btn('Ближайшие выезды', 'meropriyatiya.html#kids', 'btn btn--primary'), 'Выезды', img='k2-rock.jpg'),
    offer('Городские соревнования — в команде К2', [], 'Дети секции выступают на городских соревнованиях в составе команды скалодрома. На странице расскажем о подготовке, участии и выступлениях наших ребят.',
          link_btn('Ближайшие соревнования', 'meropriyatiya.html#kids', 'btn btn--primary'), 'Соревнования', dark=True, img='k2-first-1.jpg')]), 'events')
# 11. Фотогалерея с переключателями (вертикальные фото — в высоких ячейках)
KGAL = [('train', 'k2-10.jpg', 'Стена для боулдеринга', 1), ('train', 'k2-first-2.jpg', 'Трасса на нависании', 0), ('train', 'p-mat.jpg', 'Отдых на матах', 0), ('train', 'k2-first-3.jpg', 'Вместе на скалодроме', 0), ('train', 'k2-first-1.jpg', 'Боулдеринг в зале', 0),
        ('rocks', 'p-forest.jpg', 'Валун в лесу', 1), ('rocks', 'k2-rock.jpg', 'На скале', 0), ('rocks', 'p-cave.jpg', 'Под нависанием', 0), ('rocks', 'p-heart.jpg', 'На вершине скалы', 1),
        ('comp', 'p-dyno.jpg', 'Прыжок к зацепу', 1), ('comp', 'k2-hall.jpg', 'Зал скалодрома К2', 0), ('comp', 'p-blue.jpg', 'Синяя стена с нависанием', 1), ('comp', 'p-focus.jpg', 'На трассе', 1)]
body += sec(sechead('Фотогалерея') + tabs('kgal', [('train', 'Тренировки'), ('rocks', 'Выезды на скалы'), ('comp', 'Соревнования')]) +
            '<div class="lp-gal lp-gal--tabs">' + ''.join('<button class="lp-gal__i%s" type="button" data-tab-of="kgal" data-t="%s"%s aria-label="Открыть фото: %s"><img src="assets/img/%s" alt="%s" loading="lazy"></button>' % (' lp-gal__i--v' if v else '', g, '' if g == 'train' else ' hidden', al, f, al) for g, f, al, v in KGAL) + '</div>', 'photos', cls='lp-alt')
# 12. Отзывы: видеолента, как на главной, и виджет
PLAY = '<span class="play"><svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg></span>'
body += '<section class="sec dark videos stack" id="reviews"><div class="wrap">' + sechead('Отзывы') + '</div><div class="shorts" tabindex="0" aria-label="Видеоотзывы, листается">' + ''.join(
    '<a class="short" href="video.html"><img src="assets/img/%s" alt="" loading="lazy"><span class="scrim"></span>%s<span class="short__c"><b>%s</b><small>%s</small></span></a>' % (f, PLAY, t, d)
    for f, t, d in [('k2-10.jpg', 'Родители группы 5–7 лет', '0:45'), ('k2-02.jpg', 'Первая тренировка в&nbsp;секции', '1:10'), ('p-fun.jpg', 'Родители группы 8–10 лет', '0:58'),
                    ('p-smile.jpg', 'Как прошёл выезд на&nbsp;скалы', '1:24'), ('k2-13.jpg', 'Родители группы 11–16 лет', '0:52'), ('k2-12.jpg', 'Наши первые соревнования', '1:05')]) + '</div><div class="wrap"><div class="widget reveal kreviews"><b>Отзывы с&nbsp;Яндекс Карт и&nbsp;2ГИС</b><span>Здесь подключится виджет отзывов внешнего сервиса</span></div></div></section>'
# 13. Форма связи
body += CONTACT
# 14. Вопросы (ответы — из ТЗ; чего нет в ТЗ — в скобках)
body += faq_sec([('С какого возраста можно?', 'С 5 лет. В секции три группы: 5–7, 8–10 и 11–16 лет.'),
                 ('Сколько длится занятие?', 'Для детей 5–7 лет — 60 минут, для школьников и подростков — 90 минут.'),
                 ('Можно ли сначала попробовать?', 'Да. Пробная тренировка проходит в общей группе соответствующего возраста: ребёнок знакомится с тренером и форматом занятий.'),
                 ('Что входит в пробную тренировку?', 'Всё снаряжение и работа тренера.'),
                 ('Как оплачиваются занятия?', 'Регулярные занятия проходят по абонементам на месяц: 8 тренировок. Оплатить можно на ресепшене картой или наличными, а также онлайн по ссылке от администратора.'),
                 ('Что, если ребёнок пропустит занятие?', 'Предупредите администратора до начала тренировки: пропуски по болезни переносятся в пределах срока абонемента.'),
                 ('Есть ли выезды на скалы?', 'Да, в школьные каникулы: в Ленинградскую область и Карелию.'),
                 ('Участвуют ли дети в соревнованиях?', 'Да, дети секции выступают на городских соревнованиях в составе команды скалодрома.')])
# Липкое меню по разделам — как на «Первом разе»
KSUB = [('groups', 'Группы'), ('schedule', 'Расписание'), ('abonementy', 'Абонементы'), ('trial', 'Пробное'),
        ('docs', 'Документы'), ('coaches', 'Тренеры'), ('reviews', 'Отзывы'), ('faq', 'Вопросы')]
_sub = ('<nav class="lp-sub" aria-label="Разделы страницы"><button class="lp-sub__toggle" type="button" aria-expanded="false"><span class="lp-sub__cur">Разделы страницы</span>'
        '<span class="lp-sub__more">Разделы<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg></span></button><div class="wrap lp-sub__in">'
        + ''.join('<a href="#%s" style="--i:%d">%s<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5v14M6 13l6 6 6-6"/></svg></a>' % (h, i, t) for i, (h, t) in enumerate(KSUB))
        + '</div></nav>\n')
# «Почему К2» — как на «Первом разе»: фото на весь экран, цифры (без шкалы высоты; логика — js/landing.js)
KWHY = ('<section class="sec neutral sec--flush" id="why"><div class="wrap"><div class="lp-why2 lp-why2--inset dark">'
    '<div class="lp-why2__bg" aria-hidden="true"><picture><source media="(max-width: 767px)" srcset="assets/img/k2-09.jpg"><img src="assets/img/k2-first-2.jpg" alt="" loading="lazy"></picture></div>'
    '<div class="wrap lp-why2__in"><div class="lp-why2__head"><span class="mark reveal">Почему К2</span>'
    '<h2 class="d lp-why2__t reveal">Почему ребёнку стоит заниматься в&nbsp;К2</h2></div><ul class="lp-why2__stats">'
    '<li class="reveal"><b class="d"><span data-count="13">13</span><small>м</small></b><span><em>высоты</em> Высокие стены&nbsp;— лазаем только со&nbsp;страховкой.</span></li>'
    '<li class="reveal"><b class="d"><span data-count="1300">1300</span><small>м²</small></b><span>Боулдеринг и&nbsp;трудность под одной крышей.</span></li>'
    '<li class="reveal"><b class="d"><span data-count="7">7</span><small>мин</small></b><span><em>от метро</em> Удобно привозить ребёнка после школы.</span></li></ul>'
    '<div class="lp-why2__cards"><div class="lp-why2__c lp-why2__c--red reveal"><b class="d">Детские тренеры</b><p>Объясняют просто, следят за&nbsp;безопасностью и&nbsp;не&nbsp;дают заскучать.</p></div>'
    '<div class="lp-why2__c reveal"><b class="d">Новый скалодром</b><p>Новые стены, зацепы и&nbsp;снаряжение.</p></div>'
    '<div class="lp-why2__go reveal">' + trial_btn(cls='btn btn--light') + '</div></div></div></div></div></section>\n')
body = body.replace('<section class="sec neutral lp-alt" id="trial">', KWHY + '<section class="sec neutral lp-alt" id="trial">', 1)
_i = body.index('</section>') + len('</section>')
body = body[:_i] + '\n' + _sub + body[_i:]
page('detskaya-sekciya.html', 'Детская секция скалолазания от 5 до 16 лет — скалодром К2', 'Регулярные тренировки в трёх возрастных группах: 5–7, 8–10 и 11–16 лет. Занятия 60 или 90 минут, абонементы на месяц. Начните с пробного занятия в секции.', body, gallery=True)


# ======================= ДЕТСКАЯ ПРОБНАЯ + СЕМЬЯ =======================
body = hero([('Для детей', 'dlya-detej.html'), ('Пробная тренировка', '')], 'Пробная тренировка для ребёнка',
            'Час на скалодроме с тренером: покажет, подберёт трассы по силам и проследит за безопасностью. Для детей от 5 лет.',
            'k2-02.jpg', [(I_CHILD, 'От 5 лет'), (I_SPARK, 'Опыт не нужен'), (I_GEAR, 'Снаряжение включено'), (I_PEOPLE, 'В группе или персонально')],
            book_btn('Записать ребёнка', 'group', 0, 1) + link_btn('Вместе с ребёнком', '#family', 'btn btn--sec'), 'Взрослый и ребёнок на скалодроме')
# «Как проходит» — сцена «60 минут», как на «Первом разе» (таймер 0→60, шаги и фото переключаются при прокрутке; логика — js/landing.js, setupHour)
KID_HOUR = [(0, 5, 'p-gear.jpg', 'Знакомство и&nbsp;экипировка', '~5 мин', 'Тренер знакомится с&nbsp;ребёнком и&nbsp;подбирает ему снаряжение.'),
            (5, 15, 'p-fun.jpg', 'Инструктаж и&nbsp;разминка', '~10 мин', 'Простые правила безопасности и&nbsp;разминка в&nbsp;игровой форме.'),
            (15, 55, 'k2-10.jpg', 'Первые трассы', '~40 мин', 'Сначала боулдеринг над матами, потом&nbsp;— высокая стена со&nbsp;страховкой.'),
            (55, 60, 'p-smile.jpg', 'Итог', '~5 мин', 'Тренер расскажет родителям, как ребёнку заниматься дальше.')]
body += ('<section class="sec dark stack lp-hour" id="how"><div class="lp-hour__track"><div class="lp-hour__stage wrap">'
         '<div class="lp-hour__head"><h2 class="d h2 reveal">Что будет происходить 60&nbsp;минут?<sup class="lp-hour__star">*</sup></h2>'
         '<p class="lp-hour__clock reveal" aria-hidden="true"><b class="d">00</b><span>мин<br>из&nbsp;60</span></p></div>'
         '<div class="lp-hour__g"><div class="lp-hour__pics reveal" aria-hidden="true">' +
         ''.join('<img%s src="assets/img/%s" alt="" loading="lazy">' % (' class="is-on"' if i == 0 else '', x[2]) for i, x in enumerate(KID_HOUR)) +
         '<span class="lp-hour__badge"><i></i><span>Шаг 01 · ~5 мин</span></span></div><ol class="lp-hour__steps">' +
         ''.join('<li%s data-from="%d" data-to="%d"><img class="lp-hour__ph" src="assets/img/%s" alt="" loading="lazy"><button type="button"><span class="lp-hour__n d">%02d</span>'
                 '<span><b>%s</b><small>%s</small></span></button><p>%s</p></li>' % (' class="is-on"' if i == 0 else '', f, t, img, i + 1, h, d, txt)
                 for i, (f, t, img, h, d, txt) in enumerate(KID_HOUR)) + '</ol></div>'
         '<div class="lp-hour__bar reveal" aria-hidden="true">' + ''.join('<span style="--w:%d"></span>' % (t - f) for f, t, *_ in KID_HOUR) +
         ''.join('<small style="--x:%d">%d</small>' % (f, f) for f, *_ in KID_HOUR) + '<small style="--x:60">60 мин</small></div>'
         '<p class="lp-hour__note reveal">* Распределение времени может отличаться на&nbsp;усмотрение тренера.</p></div></div></section>\n')
# Видео о детской пробной — как на «Первом разе»: пока ролика нет, по кнопке — пометка «Видео скоро»; ссылку на ролик — в data-video
# В MODX: ссылка на ролик (TV). Пока ссылки нет — показывается пометка «Видео скоро»
body += ('<section class="sec dark lp-video-sec" id="video"><div class="wrap">'
         '<div class="sechead"><div><h2 class="d h2 reveal">Как проходит детская пробная тренировка</h2>'
         '<p class="lead muted reveal">Короткий видеообзор: от&nbsp;знакомства с&nbsp;тренером до&nbsp;первых трасс</p></div></div>'
         '<div class="lp-video reveal" data-video=""><picture><source media="(max-width: 767px)" srcset="assets/img/k2-12.jpg"><img src="assets/img/k2-first-3.jpg" alt="" loading="lazy"></picture>'
         '<span class="lp-video__shade"></span><button class="lp-video__play" type="button" aria-label="Смотреть видеообзор детской пробной тренировки"><svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg></button>'
         '<span class="lp-video__soon">Видео скоро</span><span class="lp-video__meta"><b>Детская пробная тренировка</b><small>1:20</small></span></div></div></section>\n')
# «Выберите удобный формат» — как на «Первом разе» (две большие карточки + плашка «Не знаете, какой выбрать?»)
KPRICE = {'group': price(1200, 1500), 'personal': price(2000, 2500)}  # за ребёнка
def kfmt(top, badge, title, sub, items, text, typ, dark=False):
    return ('<article class="lp-f%s reveal"><div class="lp-f__top"><span class="lp-f__k">%s</span><span class="badge%s">%s</span></div>'
            '<h3 class="d lp-f__t lp-f__t--big">%s</h3>%s<ul class="lp-list%s">%s</ul><p class="lp-f__d">%s</p>'
            '<div class="lp-f__foot">%s%s</div></article>') % (
        ' lp-f--dark' if dark else '', top, ' badge--dark' if dark else '', badge, title, '<p class="lp-f__sub">%s</p>' % sub if sub else '',
        '' if dark else ' lp-list--dark', ''.join('<li>%s%s</li>' % (CHECK, x) for x in items), text, KPRICE[typ], book_btn('Записаться', typ, 0, 1))
body += sec(sechead('Выберите удобный формат', 'Оба варианта подходят для первого знакомства ребёнка со&nbsp;скалолазанием. Отличаются размер группы, количество внимания тренера и&nbsp;стоимость.') +
            '<div class="lp-formats">' +
            kfmt('Пробная тренировка', 'Группа до 8 человек', 'Групповая', 'в&nbsp;спортивном клубе', ['60 минут', 'для детей от&nbsp;5&nbsp;лет', 'группа до&nbsp;8&nbsp;человек', 'работа тренера', 'необходимое снаряжение'],
                 'Ребёнок занимается вместе с&nbsp;группой секции своего возраста: знакомится с&nbsp;тренером, ровесниками и&nbsp;форматом занятий. Весело, в&nbsp;компании ровесников.', 'group') +
            kfmt('Пробная тренировка', '1–3 участника', 'Персональная', '', ['60 минут', 'для 1–3 детей', 'индивидуальный темп', 'работа тренера', 'необходимое снаряжение'],
                 'Больше внимания тренера&nbsp;— удобно для братьев и&nbsp;сестёр.', 'personal', dark=True) + '</div>' +
            helpbox('Не знаете, какой формат выбрать?', 'Оставьте заявку&nbsp;— администратор поможет подобрать подходящий вариант для ребёнка.', join_btn('Оставить заявку', 'Поможем выбрать формат', 'kids', 'btn btn--sec')),
            'formats', cls='stack lp-fmt')
body += sec('<div class="lp-next lp-next--red reveal" id="family"><div><span class="mark">Для всей семьи</span><h2 class="d h2">Взрослый + ребёнок</h2><p class="lead">Полазайте вместе: тренер покажет основы обоим, а вы будете поддерживать друг друга на стене. В форме записи отметьте, сколько придёт взрослых и детей.</p></div>' +
            book_btn('Записаться вместе', 'group', 1, 1, 'btn btn--light') + '</div>', tone='neutral', cls='sec--flush')
# «Почему ребёнку стоит заниматься в К2» — копия блока из детской секции; кнопка здесь открывает запись на пробную (окно бронирования)
body += KWHY.replace(trial_btn(cls='btn btn--light'), book_btn('Записать ребёнка на&nbsp;пробное', 'group', 0, 1, 'btn btn--light'))
body += sec('<div class="lp-bring"><div class="lp-bring__main reveal"><h2 class="d h2">С собой — только удобная спортивная форма</h2><p class="lead muted">Скальные туфли, страховочную систему и магнезию выдадим на месте.</p>'
            '<p class="lp-bring__note">%s<span>Приходите за 10–15 минут до начала</span></p></div><div class="lp-bring__side reveal"><p class="lp-k">Для родителей</p>' % I_TIME +
            li(['раздевалка и шкафчики', 'душевые', 'аренда полотенец', 'можно посмотреть, как ребёнок лазает']) + '</div></div>', 'bring')
# Фотогалерея — стандартный блок, детские кадры (высокие ячейки 1, 5, 8 — вертикальные фото)
GAL_KIDS = [('k2-10.jpg', 'Ребёнок на стене'), ('k2-first-2.jpg', 'Трасса на нависании'), ('p-mat.jpg', 'Отдых на матах'),
            ('k2-first-3.jpg', 'Вместе на скалодроме'), ('p-focus.jpg', 'На трассе'), ('k2-first-1.jpg', 'Боулдеринг в зале'),
            ('k2-rock.jpg', 'На скале'), ('p-heart.jpg', 'На вершине скалы'), ('p-cave.jpg', 'Под нависанием')]
body += sec(sechead('Фотогалерея', 'Нажмите на фото — откроется галерея', link_btn('Детская секция', 'detskaya-sekciya.html', 'btn btn--sec reveal')) + gal(GAL_KIDS), 'photos', cls='lp-alt')
# Документы для родителей — тот же блок, что в детской секции
body += KDOC_SEC
body += faq_sec(FAQ_KIDS)
body += nextcta('Понравилось?', 'Продолжайте в детской секции — регулярно и с детскими тренерами.', link_btn('Детская секция', 'detskaya-sekciya.html', 'btn btn--light'), 'детская секция · следующий шаг · ')
# Липкое меню по разделам — как в детской секции и на «Первом разе» (логика — js/landing.js)
TSUB = [('how', 'Как проходит'), ('video', 'Видео'), ('formats', 'Форматы'), ('family', 'Вместе с ребёнком'),
        ('why', 'Почему К2'), ('bring', 'Что взять'), ('photos', 'Фото'), ('docs', 'Документы'), ('faq', 'Вопросы')]
_tsub = _sub.replace(_sub[_sub.index('<div class="wrap lp-sub__in">'):], '<div class="wrap lp-sub__in">' + ''.join(
    '<a href="#%s" style="--i:%d">%s<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5v14M6 13l6 6 6-6"/></svg></a>' % (h, i, t) for i, (h, t) in enumerate(TSUB)) + '</div></nav>\n')
_i = body.index('</section>') + len('</section>')
body = body[:_i] + '\n' + _tsub + body[_i:]
fab = book_btn('Записаться на тренировку', 'group', 0, 1)
page('deti-pervyj-raz.html', 'Детская пробная тренировка по скалолазанию — скалодром К2', 'Пробная тренировка для детей от 5 лет и формат «взрослый + ребёнок»: с тренером, снаряжение включено. Скалодром К2.', body, book=True, fab=fab, gallery=True)


# ======================= ЦЕНЫ =======================
GROUPS = [('probnye', 'Пробные тренировки', [('Пробная тренировка в группе', '60 минут, группа до 8 человек, снаряжение включено', '1 500 ₽', 'pervyj-raz.html#formats'),
                                             ('Персональная пробная тренировка', '60 минут, для 1–3 участников, цена за человека', '2 500 ₽', 'pervyj-raz.html#formats'),
                                             ('Детская пробная тренировка', 'Для детей от 5 лет', '1 200 ₽', 'deti-pervyj-raz.html')]),
          ('razovye', 'Разовые посещения', [('Разовое посещение', 'Самостоятельно, боулдеринг и трудность', '900 ₽', 'samostoyatelno.html'), ('Разовое посещение в выходные', 'Суббота, воскресенье и праздники', '1 100 ₽')]),
          ('abonementy', 'Абонементы', [('Абонемент на месяц', 'Безлимит самостоятельных посещений', '6 500 ₽', 'samostoyatelno.html#prices'), ('Абонемент на 8 посещений', 'Самостоятельные посещения, 2 месяца', '5 600 ₽', 'samostoyatelno.html#prices'),
                                         ('Абонемент в школу', '8 групповых тренировок', '9 600 ₽', 'shkola.html')]),
          ('trener', 'Тренировки с тренером', [('Индивидуальная тренировка', 'С тренером, 60 минут', '3 500 ₽', 'individualnye.html'), ('Базовый курс', '3–5 тренировок', 'от 6 900 ₽', 'bazovye-kursy.html')]),
          ('deti', 'Для детей', [('Детская секция', 'Абонемент на 8 занятий в месяц', 'от 7 200 ₽', 'detskaya-sekciya.html'), ('Взрослый + ребёнок', 'Пробная тренировка', '2 700 ₽', 'deti-pervyj-raz.html#family')]),
          ('prokat', 'Прокат и услуги', [('Прокат снаряжения', 'Скальники, страховочная система', '400 ₽'), ('Аренда полотенца', '', '200 ₽'),
                                         ('Подарочный сертификат', 'На пробную тренировку', 'от 1 500 ₽', 'sertifikaty.html')])]
SHORT = {'probnye': 'Пробные', 'razovye': 'Разовые', 'abonementy': 'Абонементы', 'trener': 'С тренером', 'deti': 'Детям', 'prokat': 'Прокат'}
chips = ''.join('<a class="chip" href="#%s"><span class="pnav__l">%s</span><span class="pnav__s">%s</span></a>' % (g, t, SHORT[g]) for g, t, _ in GROUPS) + '<a class="chip" href="pakety.html">Пакеты</a>'
body = head([('Цены', '')], 'Цены скалодрома К2', 'Все тренировки, абонементы и прокат на одной странице. Пакеты — отдельно, там выгоднее.')
body += '<div class="pnav-wrap"><nav class="pnav" aria-label="Разделы цен"><div class="wrap chips chips--dark pnav__in">%s</div></nav>' % chips
body += sec('<div class="prices__grid"><div class="prices__main">' + ''.join(
    '<div class="pgroup" id="%s"><h2 class="d h3 pgroup__t reveal">%s</h2>%s</div>' % (g, t, plist(rows)) for g, t, rows in GROUPS) +
    '</div><aside class="prices__aside"><div class="pdf reveal"><span class="pdf__ic" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5"/></svg><i>PDF</i></span>'
    '<b>Полный прайс</b><p>Все тренировки, абонементы, пакеты и прокат — одним файлом</p><a class="btn btn--sec" href="assets/docs/k2-ceny.pdf" download>' + ico('<path d="M12 4v11M7 10l5 5 5-5M5 20h14"/>') + 'Скачать PDF</a></div>'
    '<div class="note reveal"><b>Пакеты тренировок</b><p>Готовые программы под задачу — выгоднее разовых занятий.</p>' + link_btn('Смотреть пакеты', 'pakety.html', 'btn btn--light') + '</div>'
    '<div class="note note--light reveal"><b>Первый раз?</b><p>Начните с пробной тренировки: инструктор всё покажет, снаряжение выдаём.</p>' + link_btn('Пробная тренировка', 'pervyj-raz.html', 'btn btn--primary') + '</div></aside></div>', 'prices') + '</div>'
body += CONTACT
page('ceny.html', 'Цены — скалодром К2', 'Цены на пробные тренировки, разовые посещения, абонементы, тренировки с тренером, детскую секцию и прокат снаряжения. Скалодром К2.', body)


# ======================= ПАКЕТЫ =======================
start, more = ['start', 'baza', 'rasshirennyj'], ['nizhnyaya-strahovka', 'uroven', 'sila', 'vynoslivost', 'skaly', 'tehnika']
body = head([('Цены', 'ceny.html'), ('Пакеты', '')], 'Пакеты тренировок', 'Готовые пакеты тренировок под любые задачи! Выберите свой — администратор свяжется и подберёт расписание.',
            '<div class="chips chips--dark"><a class="chip" href="#novichkam">Новичкам</a><a class="chip" href="#prodolzhayushchim">Продолжающим</a></div>')
body += sec(sechead('Новичкам', 'От первой тренировки до самостоятельного лазания') + '\n' + offers([pack_offer(s, i == 1) for i, s in enumerate(start)], 3), 'novichkam')
body += sec(sechead('Продолжающим', 'Страховка, сила, выносливость и техника') + '\n' + offers([pack_offer(s) for s in more], 3), 'prodolzhayushchim', cls='lp-alt')
body += nextcta('Не знаете, какой пакет выбрать?', 'Оставьте заявку — поможем выбрать пакет под ваш уровень.', join_btn('Оставить заявку', 'Поможем выбрать пакет', 'trial', 'btn btn--light'), 'подберём пакет · под ваш уровень · ')
page('pakety.html', 'Пакеты тренировок по скалолазанию — скалодром К2', 'Пакеты для новичков и продолжающих: Старт, База, Расширенный, Нижняя страховка, Уровень, Сила, Выносливость, Скалы, Техника.', body)


# ======================= СЕРТИФИКАТЫ =======================
body = hero([('Сертификаты', '')], 'Подарочные сертификаты на скалодром',
            'Подарите впечатление, а не вещь: пробная тренировка с инструктором. Опыт не нужен, снаряжение выдадим.',
            'k2-12.jpg', [(I_GIFT, 'Красивый подарок'), (I_SPARK, 'Опыт не нужен'), (I_GEAR, 'Снаряжение включено'), (I_CAL, 'Срок действия [__]')],
            join_btn('Заказать сертификат', 'Подарочный сертификат'), 'Вместе на скалодроме')
body += sec(sechead('Выберите сертификат') + '\n' + offers([
    offer('Пробная тренировка в группе', ['60 минут', 'группа до 8 человек', 'с инструктором', 'снаряжение включено'], 'Для того, кто хочет попробовать в компании таких же новичков.', price(1500, frm=False) + join_btn('Заказать', 'Сертификат: пробная в группе')),
    offer('Персональная пробная тренировка', ['60 минут', 'для 1–3 участников', 'индивидуальный темп', 'снаряжение включено'], 'Подарок на двоих или на троих — для пары или друзей.', price(2500) + join_btn('Заказать', 'Сертификат: персональная пробная'), dark=True)]), 'formats')
body += sec(sechead('Как подарить') + '\n' + cards([('Оставьте заявку', 'Выберите сертификат — администратор свяжется и всё оформит.'), ('Оплатите', '[Способы оплаты и получения сертификата уточняются.]'),
                                                  ('Получатель записывается', 'В удобный ему день — по телефону или на сайте.')], 3), 'how', 'dark', 'stack')
body += faq_sec([('Сколько действует сертификат?', '[Срок действия уточняется.]'), ('Можно ли подарить ребёнку?', 'Да, есть детские пробные тренировки — для детей от 5 лет.'),
                 ('Нужен ли опыт?', 'Нет. Пробная тренировка рассчитана на любой уровень.'), ('Можно ли поменять дату?', 'Предупредите администратора не&nbsp;позже чем за&nbsp;12 часов&nbsp;— перенесём на&nbsp;удобное время без доплаты.')])
page('sertifikaty.html', 'Подарочные сертификаты на скалодром — К2', 'Подарочный сертификат на пробную тренировку по скалолазанию с инструктором: в группе или персонально. Скалодром К2.', body)


# ======================= МЕРОПРИЯТИЯ =======================
# Даты — примерные, для вида (крупное число + месяц, день недели и время); реальные даст скалодром
# Дата: (число, месяц, день недели · время). Многодневное — диапазоном через «–»: ('24–26', 'ноября', 'пт–вс · …'),
# через месяц: ('30–2', 'ноября – декабря', …). Диапазон автоматически получает класс ev__date--range (цифры мельче, месяц — строкой ниже)
# Обложки — вертикальные, пропорции А4 (на обложку грузят афишу); пока — вертикальные фото зала
EVENTS = [('adults', 'Для взрослых', 'Соревнования по боулдерингу', 'k2-01.jpg', ('5', 'декабря', 'сб · 12:00')),
          ('adults', 'Для взрослых', 'Выезд на скалы', 'p-heart.jpg', ('12–13', 'декабря', 'сб–вс · старт в 09:00')),
          ('kids', 'Для детей', 'Детские соревнования', 'k2-10.jpg', ('19', 'декабря', 'сб · 11:00')),
          ('kids', 'Для детей', 'Новогодний детский фестиваль', 'k2-02.jpg', ('27', 'декабря', 'вс · 15:00')),
          ('adults', 'Для взрослых', 'Ночное лазание', 'p-blue.jpg', ('16', 'января', 'сб · 19:00'))]
# Страница каждого мероприятия (шаблон event_page ниже); адрес — по названию
EV_SLUG = {'Соревнования по боулдерингу': 'sorevnovaniya-po-boulderingu.html', 'Выезд на скалы': 'vyezd-na-skaly.html',
           'Детские соревнования': 'detskie-sorevnovaniya.html', 'Новогодний детский фестиваль': 'novogodnij-detskij-festival.html',
           'Ночное лазание': 'nochnoe-lazanie.html'}
# Архив: прошедшие мероприятия (примерные, для вида) — ч/б обложки А4, по одному ряду на страницу, переключатели страниц (js/landing.js)
ARCHIVE = [('8 ноября 2026', 'Соревнования по боулдерингу', 'Для взрослых', 'k2-05.jpg'), ('25 октября 2026', 'Детские соревнования', 'Для детей', 'p-fun.jpg'),
           ('10–11 октября 2026', 'Выезд на скалы', 'Для взрослых', 'p-forest.jpg'), ('27 сентября 2026', 'Вечер скалолазания', 'Для взрослых', 'k2-03.jpg'),
           ('13 сентября 2026', 'Открытая тренировка для детей', 'Для детей', 'p-smile.jpg'), ('30 августа 2026', 'Выезд на скалы', 'Для взрослых', 'p-rope.jpg'),
           ('16 августа 2026', 'Соревнования по боулдерингу', 'Для взрослых', 'k2-09.jpg'), ('26 июля 2026', 'Детские соревнования', 'Для детей', 'k2-12.jpg'),
           ('12 июля 2026', 'Вечер скалолазания', 'Для взрослых', 'p-roof.jpg'), ('21 июня 2026', 'Открытая тренировка для детей', 'Для детей', 'k2-13.jpg'),
           ('7 июня 2026', 'Выезд на скалы', 'Для взрослых', 'p-wall.jpg'), ('24 мая 2026', 'Вечер скалолазания', 'Для взрослых', 'k2-07.jpg')]
# Каждое прошедшее мероприятие открывается своей страницей (шаблон «Мероприятие», состояние «Уже прошло»)
ARC_MONTH = {'января': 'yanvarya', 'февраля': 'fevralya', 'марта': 'marta', 'апреля': 'aprelya', 'мая': 'maya', 'июня': 'iyunya', 'июля': 'iyulya',
             'августа': 'avgusta', 'сентября': 'sentyabrya', 'октября': 'oktyabrya', 'ноября': 'noyabrya', 'декабря': 'dekabrya'}
ARC_TYPE = {'Соревнования по боулдерингу': 'sorevnovaniya-po-boulderingu', 'Детские соревнования': 'detskie-sorevnovaniya', 'Выезд на скалы': 'vyezd-na-skaly',
            'Вечер скалолазания': 'vecher-skalolazaniya', 'Открытая тренировка для детей': 'otkrytaya-trenirovka-dlya-detej'}
def arc_slug(d, t):
    day, mon, year = d.split()
    return 'arhiv-%s-%s-%s-%s.html' % (ARC_TYPE[t], day.replace('–', '-'), ARC_MONTH[mon], year)
ARC_PAGER = ('<nav class="arc-pager" aria-label="Страницы архива"><button class="ibtn ibtn--line arc-pager__prev" type="button" aria-label="Предыдущая страница">' + ico('<path d="M19 12H5M11 6l-6 6 6 6"/>') + '</button>'
             '<span class="arc-pager__pages"></span><button class="ibtn ibtn--line arc-pager__next" type="button" aria-label="Следующая страница">' + ARROW + '</button></nav>')
body = head([('О нас', 'o-skalodrome.html'), ('Мероприятия', '')], 'Мероприятия скалодрома', 'Соревнования, выезды на скалы и события для детей и взрослых — следите за расписанием.')
# Фильтр «для кого» — над карточками, на светлом фоне, вместе со списком одним блоком
EV_CHIPS = ('<div class="chips" role="group" aria-label="Для кого"><button type="button" class="chip" aria-pressed="true" data-f="all">Все</button>'
            '<button type="button" class="chip" aria-pressed="false" data-f="adults">Для взрослых</button><button type="button" class="chip" aria-pressed="false" data-f="kids">Для детей</button></div>')
body += sec(EV_CHIPS + '<div class="bgrid bgrid--ev">%s</div><p class="bempty" hidden>Скоро здесь появятся мероприятия</p>' % ''.join(
    '<article class="bcard ev reveal" data-cat="%s"><span class="bcard__img"><img src="assets/img/%s" alt="" loading="lazy"></span><span class="bcard__b"><span class="badge">%s</span>'
    '<a class="bcard__t ev__link" href="%s">%s</a><span class="ev__date%s"><b class="d">%s</b><span><b>%s</b><small>%s</small></span></span>%s</span></article>' % ((c, img, cn, EV_SLUG[t], t, ' ev__date--range' if '–' in dt[0] else '') + dt + (join_btn('Записаться', t, 'kids' if c == 'kids' else '', 'btn btn--sec btn--sm') if t != 'Новогодний детский фестиваль' else '<span class="btn btn--sec btn--sm itp__off" aria-disabled="true">Мест нет</span>',))
    for c, cn, t, img, dt in EVENTS) + '\n<!-- В MODX: мероприятия — ресурсы (дата, для кого, обложка, описание), список — pdoResources -->', 'list', cls='blog-list')
body += nextcta('Хотите первыми узнавать о мероприятиях?', 'Оставьте телефон — сообщим о ближайших соревнованиях и выездах.', join_btn('Оставить заявку', 'Мероприятия скалодрома', '', 'btn btn--light'), 'соревнования · выезды · события · ')
# Архив прошедших мероприятий — под плашкой «Хотите первыми узнавать…»
body += sec(sechead('Прошедшие мероприятия', 'Архив соревнований, выездов и событий скалодрома') + '<div class="arc-grid">' + ''.join(
    '<article class="arc"><span class="arc__img"><img src="assets/img/%s" alt="" loading="lazy"></span><span class="arc__b"><span class="arc__date">%s</span>'
    '<a class="arc__t" href="%s">%s</a><span class="arc__tags"><span class="badge">%s</span><span class="badge badge--past">Прошло</span></span>'
    '<span class="arc__go">Как это было%s</span></span></article>' % (img, d, arc_slug(d, t), t, who, ARROW) for d, t, who, img in ARCHIVE) + '</div>' + ARC_PAGER +
    '\n<!-- В MODX: прошедшие мероприятия — те же ресурсы с датой в прошлом, от новых к старым -->', 'archive')
# Вопросы и ответы — внизу страницы (факты — из других страниц сайта; чего нет — в скобках)
body += faq_sec([('Как записаться на мероприятие?', 'Нажмите «Записаться» в карточке мероприятия и оставьте телефон — администратор перезвонит и всё подтвердит. Или позвоните нам.'),
                 ('Нужен ли опыт, чтобы участвовать?', 'Зависит от&nbsp;мероприятия: условия участия указаны на&nbsp;странице каждого события.'),
                 ('Сколько стоит участие?', 'Стоимость указана на&nbsp;странице каждого мероприятия&nbsp;— обычно от&nbsp;1&nbsp;000 до&nbsp;4&nbsp;500&nbsp;₽.'),
                 ('Нужно ли своё снаряжение?', 'Нет. Скальные туфли, страховочную систему и магнезию выдадим на месте. На&nbsp;выездах страховочное снаряжение входит в&nbsp;стоимость.'),
                 ('Можно ли прийти просто поболеть?', 'Да, вход для&nbsp;зрителей свободный.'),
                 ('Куда ездят на выезды?', 'Детские выезды на скалы проходят в школьные каникулы — в Ленинградскую область и Карелию. Для взрослых&nbsp;— выезды на&nbsp;выходные в&nbsp;Ленинградскую область, расписание&nbsp;— на&nbsp;этой странице.'),
                 ('Участвуют ли дети в соревнованиях?', 'Да, дети секции выступают на городских соревнованиях в составе команды скалодрома.'),
                 ('Как узнавать о новых мероприятиях?', 'Оставьте заявку в блоке выше — сообщим о ближайших соревнованиях и выездах.')], 'Вопросы и ответы')
page('meropriyatiya.html', 'Мероприятия — скалодром К2', 'Соревнования, выезды на скалы и мероприятия для детей и взрослых на скалодроме К2.', body)


# ======================= СТРАНИЦА МЕРОПРИЯТИЯ (шаблон) =======================
# Сверху: афиша А4 и ключевые данные (дата, время, место, для кого, цена, запись). Ниже: о мероприятии, программа, кто участвует,
# что взять, вопросы, другие мероприятия. Тексты — рыба (примерные), реальные даст скалодром. В MODX — ресурс мероприятия с полями.
EV_PLACE = 'Скалодром К2, ул.&nbsp;Скалистая, д.&nbsp;13'
EV_INFO = {
    'Соревнования по боулдерингу': dict(price=1500, place=EV_PLACE,
        about=['Открытые соревнования для всех, кто лазает от&nbsp;полугода. Двадцать новых трасс, три группы по&nbsp;уровню и&nbsp;финал для лучших в&nbsp;каждой.',
               'Приходите участвовать или поболеть: будет музыка, кофе и&nbsp;призы от&nbsp;партнёров.'],
        program=[('11:00', 'Регистрация и&nbsp;разминка'), ('12:00', 'Квалификация: 20 трасс, 3 часа'), ('15:30', 'Финал'), ('17:00', 'Награждение и&nbsp;общее фото')],
        who=['Лазаете от&nbsp;полугода', 'Возраст от&nbsp;16 лет', 'Три группы: новички, любители, опытные'],
        bring=['Скальные туфли и&nbsp;магнезию (можно взять в&nbsp;прокат)', 'Удобную одежду', 'Воду и&nbsp;перекус']),
    'Выезд на скалы': dict(price=4500, place='Ленинградская область, сбор у&nbsp;скалодрома К2',
        about=['Два дня на&nbsp;настоящих скалах с&nbsp;тренерами К2: лазание с&nbsp;верхней страховкой, техника на&nbsp;естественном рельефе и&nbsp;вечер у&nbsp;костра.',
               'Транспорт, страховочное снаряжение и&nbsp;работа тренеров входят в&nbsp;стоимость.'],
        program=[('09:00', 'Сбор у&nbsp;скалодрома и&nbsp;выезд'), ('12:00', 'Инструктаж и&nbsp;первые трассы'), ('19:00', 'Ужин и&nbsp;костёр'), ('Вс 17:00', 'Возвращение в&nbsp;Петербург')],
        who=['Прошли базовый курс или умеете страховать', 'Возраст от&nbsp;16 лет', 'Группа до&nbsp;12 человек'],
        bring=['Тёплую одежду и&nbsp;непромокаемую куртку', 'Спальник и&nbsp;коврик', 'Личную аптечку']),
    'Детские соревнования': dict(price=1200, place=EV_PLACE,
        about=['Соревнования для детей секции и&nbsp;гостей. Трассы по&nbsp;возрасту, судьи и&nbsp;медали для всех участников.',
               'Родители могут поболеть из&nbsp;зоны для зрителей.'],
        program=[('10:30', 'Регистрация'), ('11:00', 'Группа 5–7 лет'), ('12:30', 'Группа 8–10 лет'), ('14:00', 'Группа 11–16 лет и&nbsp;награждение')],
        who=['Дети от&nbsp;5 до&nbsp;16 лет', 'Не&nbsp;обязательно заниматься в&nbsp;секции', 'Нужно заявление от&nbsp;родителей'],
        bring=['Спортивную форму', 'Воду', 'Хорошее настроение']),
    'Новогодний детский фестиваль': dict(price=1000, place=EV_PLACE,
        about=['Праздник для детей: игровые трассы, эстафеты, мастер-класс от&nbsp;тренеров и&nbsp;подарки.',
               'Подойдёт и&nbsp;тем, кто ни&nbsp;разу не&nbsp;лазал: снаряжение выдадим, тренеры всё покажут.'],
        program=[('15:00', 'Встреча и&nbsp;разминка'), ('15:30', 'Игровые трассы и&nbsp;эстафеты'), ('16:30', 'Мастер-класс от&nbsp;тренеров'), ('17:15', 'Подарки и&nbsp;фото')],
        who=['Дети от&nbsp;5 до&nbsp;12 лет', 'Опыт не&nbsp;нужен', 'Родители — рядом'],
        bring=['Удобную одежду', 'Сменную обувь', 'Воду']),
    'Ночное лазание': dict(price=1200, place=EV_PLACE,
        about=['Вечер, когда зал открыт только для участников: приглушённый свет, музыка, новые трассы и&nbsp;компания.',
               'Можно прийти одному или с&nbsp;друзьями. Тренеры подскажут трассы под ваш уровень.'],
        program=[('19:00', 'Сбор и&nbsp;разминка'), ('19:30', 'Лазание под музыку'), ('21:30', 'Конкурс на&nbsp;лучший пролаз'), ('22:30', 'Чай и&nbsp;общение')],
        who=['Лазаете хотя бы немного', 'Возраст от&nbsp;16 лет', 'До&nbsp;40 участников'],
        bring=['Скальные туфли (или возьмите в&nbsp;прокат)', 'Удобную одежду', 'Друзей']),
}
I_EVT = {'cal': I_CAL, 'pin': I_PIN, 'who': I_PEOPLE, 'rub': ico('<circle cx="12" cy="12" r="9"/><path d="M10 17V7h3a3 3 0 0 1 0 6h-4M9 15h5"/>')}
# ======================= ШАБЛОНЫ «ТОВАР» и «МЕРОПРИЯТИЕ» (по ТЗ «Страница описания услуги или товара») =======================
# Основа — статья блога: шапка (название, краткое содержание, цена/дата, кнопка, «Задать вопрос»), широкая картинка,
# слева текст, справа липкая карточка (афиша А4, данные, кнопка, «Возникли вопросы?»). Ниже — галерея, вопросы, «Другие …».
# Товар (базовый курс, сертификат, пакет): цена старая/новая, кнопка «Купить» → форма «Покупка услуги» (взрослые, ФИО, телефон, почта, «Оплатить»).
# Мероприятие: дата, «Для детей», время начала, место сбора; кнопка «Записаться» → форма «Запись на мероприятие».
#   Состояние кнопки: state='open' — «Записаться», 'full' — «Мест нет», 'past' — «Уже прошло» (в MODX: дата ухода в архив).
I_TIME_S = ico('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>')
I_TG = ico('<path d="M21 4L3 11l6 2 2 6 3-4 5 4z"/><path d="M9 13l12-9"/>')
I_CHAT = ico('<path d="M4 5h16v11H9l-5 4z"/>')
I_PHONE = ico('<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/>')
ASK_BOX = ('<div class="itp__ask"><b class="itp__ask-t d">Возникли вопросы?</b>'
           '<a class="itp__tel" href="tel:+78120000000">%s+7 (812) 000-00-00</a>'
           '<div class="itp__msg"><a href="https://t.me/" target="_blank" rel="noopener">%sTelegram</a><a href="https://max.ru/" target="_blank" rel="noopener">%sMax</a>'
           '<a href="https://wa.me/78120000000" target="_blank" rel="noopener">%sWhatsApp</a></div>%%s</div>') % (I_PHONE, I_TG, I_CHAT, I_CHAT)
STATE_TXT = {'full': 'Мест нет', 'past': 'Уже прошло'}

def ask_link(name, cls='itp__q'):
    return '<button class="%s js-join" type="button" aria-haspopup="dialog" aria-controls="join" data-join-title="Вопрос: %s">Задать вопрос</button>' % (cls, name)

def order_btn(d, cls='btn btn--primary'):
    st = d.get('state', 'open')
    if st != 'open':
        return '<span class="%s itp__off" aria-disabled="true">%s</span>' % (cls.replace('btn--primary', 'btn--sec'), STATE_TXT[st])
    return '<button class="%s js-order" type="button" aria-haspopup="dialog" aria-controls="order">%s</button>' % (cls, 'Купить' if d['kind'] == 'product' else 'Записаться')

def item_page(slug, title, desc, d):
    """d: kind ('product'|'event'), crumbs, name, lead, cover (горизонтальное), poster (вертикальное А4), text (html), gallery, faq, more_title, more (html карточек)
    product: price, old, facts [(иконка, подпись, значение)]; event: day, month, when (время/день), kids (bool), start, meet, price, state"""
    ev = d['kind'] == 'event'
    nm = d['name'].replace('&nbsp;', ' ')
    if ev:
        rng = ' ev__date--range' if '–' in d['day'] else ''
        top = '<div class="ev__date itp__date%s"><b class="d">%s</b><span><b>%s</b><small>%s</small></span></div>' % (rng, d['day'], d['month'], d['when'])
        facts = [(I_EVT['cal'], 'Дата', '%s %s' % (d['day'], d['month'])), (I_TIME_S, 'Время начала', d['start']), (I_EVT['pin'], 'Место сбора', d['meet']),
                 (I_EVT['who'], 'Для кого', 'Для детей' if d.get('kids') else 'Для взрослых'), (I_EVT['rub'], 'Участие', rub(d['price']))]
        meta = '%s %s · %s' % (d['day'], d['month'], d['start'])
    else:
        top = '<div class="itp__price">%s<b class="d">%s</b></div>' % ('<span class="itp__old"><s>%s</s><i>−%d%%</i></span>' % (rub(d['old']), round(100 - d['price'] * 100 / d['old'])) if d.get('old') else '', rub(d['price']))
        facts = d['facts']
        meta = rub(d['price'])
    st = d.get('state', 'open'); past = st == 'past'
    badge = '<span class="badge itp__kids">Для детей</span>' if d.get('kids') else ''
    kb = badge  # на афише — только «Для детей»; что событие прошло, видно по плашке «Уже прошло»
    if past:
        badge += '<span class="badge itp__pastb">Мероприятие прошло</span>'
        d['text'] = ('<div class="itp__past"><b class="d">Это мероприятие уже прошло</b><p>%s %s — здесь рассказываем, как это было. '
                     'Записаться можно на&nbsp;ближайшие события.</p>%s</div>' % (d['day'], d['month'], link_btn('Ближайшие мероприятия', 'meropriyatiya.html#list', 'btn btn--primary btn--sm'))) + d['text']
    data = ' data-kind="%s" data-name="%s" data-img="%s" data-meta="%s" data-price="%d" data-who="%s" data-max="%d"' % (
        d['kind'], nm, d['poster'], re.sub('<[^>]+>|&nbsp;', ' ', meta), d['price'], 'kids' if d.get('kids') else 'adults', d.get('max', 6))
    b = ('<article class="art itp itp--%s%s"%s>\n<header class="art__head dark itp__head"><div class="wrap itp__hg"><div class="itp__ht">%s%s'
         '<h1 class="d art__t">%s</h1><p class="art__lead">%s</p>'
         '<div class="itp__buy">%s<div class="itp__act">%s%s</div></div></div>'
         '<figure class="itp__hero"><img src="assets/img/%s" alt="" fetchpriority="high"></figure></div></header>\n'
         '<div class="art__wrap wrap itp__wrap"><div class="art__body itp__body">%s</div>\n'
         '<aside class="itp__side"><div class="itp__card"><figure class="itp__poster"><img src="assets/img/%s" alt="Афиша: %s" loading="lazy">%s%s</figure>'
         '<b class="itp__name d">%s</b>%s<ul class="itp__facts">%s</ul>%s</div>%s</aside></div></article>\n') % (
        d['kind'], ' itp--past' if past else '', data, crumbs(d['crumbs']), badge, d['name'], d['lead'], top, order_btn(d),
        link_btn('Ближайшие мероприятия', 'meropriyatiya.html#list', 'itp__q') if past else ask_link(nm), d['cover'], d['text'],
        d['poster'], nm, kb, '<span class="itp__state">%s</span>' % STATE_TXT[st] if st != 'open' else '',
        d['name'], top.replace('itp__date', 'itp__date itp__date--s').replace('class="itp__price"', 'class="itp__price itp__price--s"'),
        ''.join('<li><span class="evp__ic">%s</span><span><small>%s</small><b>%s</b></span></li>' % f for f in facts), order_btn(d, 'btn btn--primary itp__go'),
        ASK_BOX % ask_link(nm, 'btn btn--sec btn--sm itp__ask-go'))
    if d.get('gallery'):  # следующий блок после текста: правая карточка прилипает только до него
        b += sec(sechead('Фотогалерея', 'Нажмите на фото — откроется галерея') + '\n' + gal(d['gallery']), 'photos')
    if d.get('faq'):
        b += faq_sec(d['faq'])
    if d.get('more'):
        b += sec(sechead(d['more_title'], '', d.get('more_btn', '')) + d['more'], 'more', cls='blog-list lp-alt')
    if not past:
        b += ORDER
    page(slug, title, desc, b, gallery=bool(d.get('gallery')))

# Форма «Покупка услуги» / «Запись на мероприятие» — одна на обе страницы; данные подставляет js/landing.js из data-атрибутов .itp
ORDER = '''<!-- Форма покупки / записи (шаблоны «Товар» и «Мероприятие»): заголовок, название, количество, ФИО, телефон, почта -->
<dialog class="modal book order" id="order" aria-labelledby="order-t">
  <div class="modal__card book__card">
    <form class="cform cform--modal book__form" novalidate>
      <input type="hidden" name="item" value=""><input type="hidden" name="when" value="">
      <button class="modal__x js-order-close" type="button" aria-label="Закрыть"><svg class="ico" viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18"/></svg></button>
      <div class="cform__body">
        <div class="cform__top"><h3 class="cform__t" id="order-t">Запись на&nbsp;мероприятие</h3></div>
        <div class="order__item"><img class="order__img" src="" alt=""><span><b class="order__name"></b><small class="order__meta"></small></span></div>
        <fieldset class="cform__set">
          <legend class="order__leg">Количество участников</legend>
          <div class="book__counts"><div class="book__count" data-k="n"><span><b class="order__who">Взрослые</b><small class="order__age">от&nbsp;16&nbsp;лет</small></span><div class="step"><button type="button" class="step__b" data-d="-1" aria-label="Меньше">−</button><output class="step__v">1</output><button type="button" class="step__b" data-d="1" aria-label="Больше">+</button></div></div></div>
          <input type="hidden" name="count" value="1">
        </fieldset>
        <div class="field"><input id="o-name" name="name" type="text" autocomplete="name" placeholder=" " required><label for="o-name" class="order__nl">Имя</label><span class="field__err">Как к&nbsp;вам обращаться?</span></div>
        <div class="cform__row">
          <div class="field"><input id="o-phone" name="phone" type="tel" inputmode="tel" autocomplete="tel" placeholder=" " required><label for="o-phone">Телефон</label><span class="field__err">Проверьте номер&nbsp;— нужно 10&nbsp;цифр после +7</span></div>
          <div class="field"><input id="o-mail" name="email" type="email" autocomplete="email" placeholder=" " required><label for="o-mail">Почта</label><span class="field__err">Проверьте адрес почты</span></div>
        </div>
        <div class="book__sum order__sum" aria-live="polite"><div class="book__total"><span>Итого</span><b class="book__total-v"></b></div></div>
        <div class="cform__agree">
          <label class="agree"><input type="checkbox" name="agree" required><span class="agree__box"></span><span>Согласен на&nbsp;<a href="politika-personalnyh-dannyh.html">обработку персональных данных</a></span></label>
          <span class="field__err field__err--agree">Нужно согласие, чтобы оформить заявку</span>
        </div>
        <button class="btn btn--primary cform__go" type="submit">Записаться</button>
        <p class="book__note order__note"></p>
      </div>
      <div class="cform__done" aria-live="polite" hidden>
        <svg class="done__ic" viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="32" r="29"/><path d="M19 33l9 9 17-19"/></svg>
        <h3 class="cform__t order__done-t">Готово</h3>
        <p class="cform__s done__msg"></p>
        <button class="btn btn--sec js-order-close" type="button">Закрыть</button>
      </div>
    </form>
  </div>
</dialog>'''

def body_list(items, ol=False):
    return '<%s>%s</%s>' % ('ol class="itp__prog"' if ol else 'ul', ''.join('<li>%s</li>' % x for x in items), 'ol' if ol else 'ul')

# ---------- Мероприятия на шаблоне ----------
EV_MORE = {  # широкая картинка (горизонтальная), время начала, место сбора, лимит участников в одной заявке
    'Соревнования по боулдерингу': ('k2-first-1.jpg', 'Регистрация с&nbsp;11:00', 'Ресепшен скалодрома К2', 4),
    'Выезд на скалы': ('k2-rock.jpg', '09:00, суббота', 'У&nbsp;входа в&nbsp;скалодром К2, ул.&nbsp;Скалистая, д.&nbsp;13', 4),
    'Детские соревнования': ('k2-first-2.jpg', '10:30 — регистрация', 'Ресепшен скалодрома К2', 3),
    'Новогодний детский фестиваль': ('p-mat.jpg', '15:00', 'Детская зона скалодрома К2', 3),
    'Ночное лазание': ('k2-hall.jpg', '19:00', 'Ресепшен скалодрома К2', 4),
    'Вечер скалолазания': ('k2-first-3.jpg', '19:00', 'Ресепшен скалодрома К2', 4),
}
EV_STATE = {'Новогодний детский фестиваль': 'full'}  # пример «Мест нет»; «Уже прошло» — страница из архива ниже
EV_INFO['Вечер скалолазания'] = dict(price=900, place=EV_PLACE,
    about=['Вечер для тех, кто лазает и&nbsp;хочет познакомиться с&nbsp;другими скалолазами: новые трассы, музыка и&nbsp;чай после тренировки.',
           'Тренеры показывали упражнения на&nbsp;технику, а&nbsp;в&nbsp;конце устроили небольшой конкурс.'],
    program=[('19:00', 'Сбор и&nbsp;разминка'), ('19:30', 'Новые трассы'), ('21:00', 'Конкурс'), ('22:00', 'Чай и&nbsp;общение')],
    who=['Лазаете хотя бы немного', 'Возраст от&nbsp;16 лет'], bring=['Удобную одежду', 'Скальные туфли или прокат'])
EV_FAQ = [('Как записаться?', 'Нажмите «Записаться», укажите количество участников и&nbsp;контакты&nbsp;— администратор подтвердит запись.'),
          ('Можно ли прийти зрителем?', 'Да, вход для зрителей свободный.'),
          ('Нужно ли своё снаряжение?', 'Нет, скальные туфли и&nbsp;систему можно взять в&nbsp;прокат на&nbsp;месте.'),
          ('Что, если не&nbsp;смогу прийти?', 'Предупредите администратора за&nbsp;сутки&nbsp;— вернём деньги или перенесём участие.')]

def ev_card(o):
    return ('<article class="bcard ev reveal"><span class="bcard__img"><img src="assets/img/%s" alt="" loading="lazy"></span><span class="bcard__b"><span class="badge">%s</span>'
            '<a class="bcard__t ev__link" href="%s">%s</a><span class="ev__date%s"><b class="d">%s</b><span><b>%s</b><small>%s</small></span></span></span></article>') % (
        o[3], o[1], EV_SLUG[o[2]], o[2], ' ev__date--range' if '–' in o[4][0] else '', o[4][0], o[4][1], o[4][2])

def event_page(c, cn, t, img, dt, state=None):
    inf = EV_INFO[t]; cover, start, meet, mx = EV_MORE[t]
    text = (''.join('<p>%s</p>' % x for x in inf['about'][1:]) +  # первый абзац — уже в шапке
            '<h2 id="prog">Программа</h2>' + body_list(['<b>%s</b> %s' % x for x in inf['program']], True) +
            '<h2 id="who">Кто может участвовать</h2>' + body_list(inf['who']) +
            '<h2 id="bring">Что взять с&nbsp;собой</h2>' + body_list(inf['bring']) +
            '<h2 id="route">Как добраться</h2><p>Место сбора&nbsp;— %s. От&nbsp;метро «Площадь Ленина» 7&nbsp;минут пешком, рядом есть парковка. '
            'Приходите за&nbsp;15&nbsp;минут до&nbsp;начала, чтобы спокойно переодеться и&nbsp;пройти регистрацию.</p>' % meet +
            '<h2 id="note">Важно знать</h2>' + body_list(['Запись закрывается, когда заканчиваются места', 'Фото и&nbsp;видео с&nbsp;мероприятия опубликуем в&nbsp;соцсетях скалодрома', 'Если не&nbsp;сможете прийти, предупредите администратора за&nbsp;сутки']))
    others = [e for e in EVENTS if e[2] != t][:3]
    item_page(EV_SLUG[t], t + ' — мероприятия скалодрома К2', re.sub('<[^>]+>|&nbsp;', ' ', inf['about'][0]), dict(
        kind='event', crumbs=[('О нас', 'o-skalodrome.html'), ('Мероприятия', 'meropriyatiya.html'), (t, '')], name=t, lead=inf['about'][0],
        cover=cover, poster=img, day=dt[0], month=dt[1], when=dt[2], kids=c == 'kids', start=start, meet=meet, price=inf['price'], max=mx,
        state=state or EV_STATE.get(t, 'open'), text=text, gallery=(GAL_KIDS if c == 'kids' else GAL_SCHOOL)[:7], faq=EV_FAQ,
        more_title='Другие мероприятия', more_btn=link_btn('Все мероприятия', 'meropriyatiya.html', 'btn btn--sec reveal'),
        more='<div class="bgrid bgrid--ev bgrid--ev3">' + ''.join(ev_card(o) for o in others) + '</div>'))
for e in EVENTS:
    event_page(*e)
# ---------- Прошедшие мероприятия (архив): та же страница, состояние «Уже прошло»; текст — в прошедшем времени (рыба) ----------
ARC_STORY = {  # широкая картинка, время, место, цена, краткое содержание, как это было, как прошёл день, итоги
    'Соревнования по боулдерингу': dict(cover='k2-first-1.jpg', start='12:00', meet='Скалодром К2', price=1500,
        lead='Открытые соревнования по&nbsp;боулдерингу: двадцать новых трасс, три группы по&nbsp;уровню и&nbsp;финал для лучших.',
        story=['Собрали больше шестидесяти участников&nbsp;— от&nbsp;тех, кто лазает полгода, до&nbsp;опытных спортсменов. Зрители болели с&nbsp;балкона, играла музыка.',
               'Постановщики подготовили двадцать новых трасс, а&nbsp;финал получился напряжённым до&nbsp;последней попытки.'],
        day=[('11:00', 'Регистрация и&nbsp;разминка'), ('12:00', 'Квалификация'), ('15:30', 'Финал'), ('17:00', 'Награждение')],
        res=['64 участника в&nbsp;трёх группах', '20 новых трасс', 'Призы от&nbsp;партнёров для победителей']),
    'Детские соревнования': dict(cover='k2-first-2.jpg', start='11:00', meet='Скалодром К2', price=1200,
        lead='Соревнования для детей секции и&nbsp;гостей: трассы по&nbsp;возрасту, судьи и&nbsp;медали для всех.',
        story=['На&nbsp;старт вышли дети от&nbsp;5 до&nbsp;16 лет&nbsp;— многие впервые выступали на&nbsp;соревнованиях. Родители поддерживали из&nbsp;зоны для&nbsp;зрителей.',
               'Каждый участник получил медаль, а&nbsp;лучшие в&nbsp;своих группах&nbsp;— кубки и&nbsp;подарки.'],
        day=[('10:30', 'Регистрация'), ('11:00', 'Группа 5–7 лет'), ('12:30', 'Группа 8–10 лет'), ('14:00', 'Группа 11–16 лет и&nbsp;награждение')],
        res=['48 юных участников', 'Медали для всех', 'Кубки победителям в&nbsp;каждой группе']),
    'Выезд на скалы': dict(cover='k2-rock.jpg', start='09:00, суббота', meet='У&nbsp;входа в&nbsp;скалодром К2', price=4500,
        lead='Два дня на&nbsp;настоящих скалах с&nbsp;тренерами К2: лазание с&nbsp;верхней страховкой и&nbsp;вечер у&nbsp;костра.',
        story=['Группа из&nbsp;двенадцати человек провела выходные в&nbsp;Ленинградской области. Для многих это был первый выход на&nbsp;естественный рельеф.',
               'Тренеры поставили маршруты разной сложности, а&nbsp;вечером все собрались у&nbsp;костра.'],
        day=[('09:00', 'Сбор и&nbsp;выезд'), ('12:00', 'Инструктаж и&nbsp;первые маршруты'), ('19:00', 'Ужин у&nbsp;костра'), ('Вс 17:00', 'Возвращение в&nbsp;Петербург')],
        res=['12 участников', '15 пройденных маршрутов', 'Первый скальный опыт для половины группы']),
    'Вечер скалолазания': dict(cover='k2-first-3.jpg', start='19:00', meet='Ресепшен скалодрома К2', price=900,
        lead='Вечер для тех, кто лазает и&nbsp;хочет познакомиться с&nbsp;другими скалолазами: новые трассы, музыка и&nbsp;чай.',
        story=['Пришли и&nbsp;постоянные гости, и&nbsp;те, кто лазает недавно. Тренеры показывали упражнения на&nbsp;технику и&nbsp;подсказывали трассы.',
               'В&nbsp;конце устроили небольшой конкурс, а&nbsp;потом пили чай и&nbsp;договаривались лазать вместе.'],
        day=[('19:00', 'Сбор и&nbsp;разминка'), ('19:30', 'Новые трассы'), ('21:00', 'Конкурс'), ('22:00', 'Чай и&nbsp;общение')],
        res=['35 участников', '10 новых трасс', 'Призы за&nbsp;конкурс']),
    'Открытая тренировка для детей': dict(cover='p-mat.jpg', start='12:00', meet='Детская зона скалодрома К2', price=0,
        lead='Бесплатная тренировка для детей, которые хотели попробовать скалолазание и&nbsp;познакомиться с&nbsp;тренерами секции.',
        story=['Дети прошли игровую разминку, полазали на&nbsp;боулдеринге и&nbsp;попробовали высокую стену со&nbsp;страховкой.',
               'Родители задали тренерам вопросы о&nbsp;секции, а&nbsp;многие дети после тренировки записались в&nbsp;группы.'],
        day=[('12:00', 'Знакомство и&nbsp;разминка'), ('12:20', 'Игровые трассы'), ('12:50', 'Высокая стена'), ('13:20', 'Вопросы родителей')],
        res=['25 детей', 'Знакомство с&nbsp;тренерами секции', 'Запись в&nbsp;группы со&nbsp;скидкой']),
}
for d0, t, who, img in ARCHIVE:
    A = ARC_STORY[t]; day, mon, year = d0.split(); kids = who == 'Для детей'
    text = (''.join('<p>%s</p>' % x for x in A['story']) +
            '<h2 id="prog">Как прошёл день</h2>' + body_list(['<b>%s</b> %s' % x for x in A['day']], True) +
            '<h2 id="res">Итоги</h2>' + body_list(A['res']))
    item_page(arc_slug(d0, t), '%s, %s — архив мероприятий К2' % (t, d0), re.sub('<[^>]+>|&nbsp;', ' ', A['lead']), dict(
        kind='event', crumbs=[('О нас', 'o-skalodrome.html'), ('Мероприятия', 'meropriyatiya.html'), ('Архив', 'meropriyatiya.html#archive'), (t, '')],
        name=t, lead=A['lead'], cover=A['cover'], poster=img, day=day, month='%s %s' % (mon, year), when='прошло', kids=kids, start=A['start'], meet=A['meet'],
        price=A['price'], state='past', text=text, gallery=(GAL_KIDS if kids else GAL_SCHOOL)[:7],
        more_title='Ближайшие мероприятия', more_btn=link_btn('Все мероприятия', 'meropriyatiya.html', 'btn btn--sec reveal'),
        more='<div class="bgrid bgrid--ev bgrid--ev3">' + ''.join(ev_card(o) for o in EVENTS[:3]) + '</div>'))

# ---------- Базовые курсы на шаблоне «Товар» ----------
COURSE = {  # тексты — рыба (примерные)
    'start': dict(cover='k2-first-1.jpg', poster='k2-11.jpg', n='3 тренировки', dur='90 минут', lead='Курс для тех, кто ни&nbsp;разу не&nbsp;лазал: за&nbsp;три тренировки освоите основы боулдеринга и&nbsp;трудности и&nbsp;научитесь страховать.',
                  prog=['Знакомство, правила зала и&nbsp;первые трассы на&nbsp;боулдеринге', 'Высокая стена: верхняя страховка и&nbsp;работа с&nbsp;верёвкой', 'Самостоятельное лазание в&nbsp;паре и&nbsp;итоговая проверка']),
    'baza': dict(cover='p-chalk.jpg', poster='k2-04.jpg', n='4 тренировки', dur='90 минут', lead='Основной курс: техника, страховка и&nbsp;уверенное лазание на&nbsp;трассах средней сложности.',
                 prog=['Техника ног и&nbsp;положение тела', 'Страховка и&nbsp;узлы', 'Трассы на&nbsp;высокой стене', 'Итоговая проверка и&nbsp;допуск к&nbsp;самостоятельным посещениям']),
    'rasshirennyj': dict(cover='k2-hall.jpg', poster='k2-12.jpg', n='5 тренировок', dur='90 минут', lead='Курс с&nbsp;запасом: больше практики на&nbsp;высокой стене, разбор техники и&nbsp;первые сложные трассы.',
                         prog=['Основы и&nbsp;правила зала', 'Страховка и&nbsp;узлы', 'Техника на&nbsp;боулдеринге', 'Трассы на&nbsp;высокой стене', 'Итоговая проверка и&nbsp;план тренировок']),
    'nizhnyaya-strahovka': dict(cover='p-boulder.jpg', poster='p-rope.jpg', n='3 тренировки', dur='120 минут', lead='Следующий шаг после базового курса: лазание с&nbsp;нижней страховкой, как на&nbsp;скалах и&nbsp;соревнованиях.',
                                prog=['Как устроена нижняя страховка, правила безопасности', 'Вщёлкивание и&nbsp;срывы под контролем тренера', 'Самостоятельное лазание с&nbsp;нижней страховкой и&nbsp;проверка']),
}
COURSE_SLUG = {s: 'kurs-%s.html' % s for s in COURSE}
COURSE_FAQ = [('Нужен ли опыт?', 'Для «Старта», «Базы» и&nbsp;«Расширенного» — нет. Для «Нижней страховки» нужен пройденный базовый курс.'),
              ('Как проходит оплата?', 'Нажмите «Купить», укажите количество участников и&nbsp;контакты&nbsp;— после проверки откроется оплата картой.'),
              ('Можно ли пройти курс вдвоём?', 'Да, укажите в&nbsp;форме количество взрослых&nbsp;— запишем вас в&nbsp;одну группу.'),
              ('Что, если пропущу занятие?', 'Предупредите администратора за&nbsp;12 часов&nbsp;— перенесём занятие без доплаты.')]

def course_card(s):  # карточка как на главной (блок пакетов)
    p = PK[s]
    return ('<a class="pack reveal" href="%s"><span class="pack__img"><img src="assets/img/%s" alt="" loading="lazy"></span><span class="pack__b"><span class="pack__t">%s</span>'
            '<span class="pack__d">%s</span><span class="badges">%s</span><span class="pack__f">%s<span class="go go--s">%s</span></span></span></a>') % (
        COURSE_SLUG[s], p['img'], p['t'], p['d'], ''.join('<span class="badge">%s</span>' % x for x in p['b']), price(*PACK_PRICE[s]), ARROW)

for s, c in COURSE.items():
    p = PK[s]; t = re.sub('<[^>]+>', '', p['t']); pr, old = PACK_PRICE[s]
    text = (
            '<h2 id="prog">Программа курса</h2>' + body_list(c['prog'], True) +
            '<h2 id="inc">Что входит</h2>' + body_list(['%s по&nbsp;%s с&nbsp;тренером' % (c['n'], c['dur']), 'Всё снаряжение: туфли, система, магнезия', 'Группа до&nbsp;6 человек или персонально', 'Допуск к&nbsp;самостоятельным посещениям после курса' if s != 'nizhnyaya-strahovka' else 'Допуск к&nbsp;лазанию с&nbsp;нижней страховкой']) +
            '<h2 id="how">Как проходят занятия</h2><p>Каждая тренировка начинается с&nbsp;разминки и&nbsp;короткого разбора: тренер объясняет, что сегодня отрабатываем и&nbsp;зачем. '
            'Дальше&nbsp;— практика на&nbsp;трассах под ваш уровень, а&nbsp;в&nbsp;конце&nbsp;— заминка и&nbsp;советы, что повторить к&nbsp;следующему занятию.</p>'
            '<p>Нагрузка растёт постепенно: никто не&nbsp;заставит лезть выше, чем комфортно. Если что-то не&nbsp;получается, тренер подберёт упражнение попроще и&nbsp;вернётся к&nbsp;трассе позже.</p>'
            '<h2 id="bring">Что взять с&nbsp;собой</h2>' + body_list(['Удобную спортивную одежду, которая не&nbsp;сковывает движения', 'Воду', 'Сменную обувь для зала (скальные туфли выдадим)']) +
            '<h2 id="sched">Расписание групп</h2><p>Группы стартуют каждую неделю: будни&nbsp;— вечером, выходные&nbsp;— днём. Удобное время подберёт администратор после покупки курса. '
            'Если ни&nbsp;одна группа не&nbsp;подходит, курс можно пройти персонально.</p>'
            '<h2 id="after">После курса</h2><p>Вы&nbsp;сможете приходить в&nbsp;зал без&nbsp;тренера, лазать в&nbsp;паре и&nbsp;продолжить в&nbsp;школе скалолазания&nbsp;— в&nbsp;группе своего уровня.</p>')
    item_page(COURSE_SLUG[s], 'Курс «%s» — скалодром К2' % t, re.sub('<[^>]+>|&nbsp;', ' ', c['lead']), dict(
        kind='product', crumbs=[('Для взрослых', 'dlya-vzroslyh.html'), ('Базовые курсы', 'bazovye-kursy.html'), (t, '')], name='Курс «%s»' % t, lead=c['lead'],
        cover=c['cover'], poster=c['poster'], price=pr, old=old, max=6,
        facts=[(I_CAL, 'Тренировок', c['n']), (I_TIME_S, 'Длительность', c['dur']), (I_PEOPLE, 'Формат', 'В&nbsp;группе или персонально'), (I_GEAR, 'Снаряжение', 'Выдаём')],
        text=text, gallery=GAL_SCHOOL[:7], faq=COURSE_FAQ, more_title='Другие базовые курсы',
        more_btn=link_btn('Все курсы', 'bazovye-kursy.html#programs', 'btn btn--sec reveal'),
        more='<div class="packs itp__more">' + ''.join(course_card(x) for x in COURSE if x != s) + '</div>'))


# ======================= О СКАЛОДРОМЕ =======================
body = hero([('О скалодроме', '')], 'Новый скалодром в центре Петербурга',
            'Боулдеринг и трудность под одной крышей: 1300 м², стены 13 метров, 7 минут пешком от м. Площадь Ленина.',
            'p-blue.jpg', [(I_UP, '13 метров высоты'), (I_SPARK, '1300 м²'), (I_CAL, '7 дней в неделю'), (I_PIN, '7 минут от метро')],
            link_btn('Первый раз', 'pervyj-raz.html', 'btn btn--primary') + link_btn('Как добраться', 'kontakty.html#route', 'btn btn--sec'), 'Зал скалодрома К2')
# Обращение команды — сразу после первого экрана, как цитата. Текст — пример (написан для вида); потом его заменят куском SEO-текста. Фото — временное: нужно общее фото команды
body += sec('<figure class="hello reveal"><div class="hello__ph"><img src="assets/img/k2-first-3.jpg" alt="Команда скалодрома К2" loading="lazy"><span class="hello__tag">Команда К2</span></div>'
            '<blockquote class="hello__q"><span class="hello__mark d" aria-hidden="true">“</span>'
            '<p class="hello__t d">Привет! Добро пожаловать на&nbsp;скалодром К2</p>'
            '<p class="lead">Мы ещё молодые, но&nbsp;нам есть чем вас порадовать.</p>'
            '<p class="muted">Мы открыли К2, чтобы в&nbsp;центре Петербурга появилось место, куда хочется возвращаться: после работы, всей семьёй или с&nbsp;друзьями на&nbsp;выходных. '
            'Здесь 1300&nbsp;м² боулдеринга и&nbsp;трудности, стены высотой 13&nbsp;метров и&nbsp;тренеры, которые одинаково внимательны к&nbsp;новичку и&nbsp;к&nbsp;тому, кто готовится к&nbsp;соревнованиям.</p>'
            '<p class="muted">Не&nbsp;умеете лазать&nbsp;— научим с&nbsp;первой тренировки, снаряжение выдадим на&nbsp;месте. Уже лазаете&nbsp;— приходите за&nbsp;новыми трассами, компанией и&nbsp;атмосферой. Мы только начинаем, и&nbsp;нам важно, чтобы вам у&nbsp;нас понравилось.</p></blockquote>'
            '<figcaption class="hello__sign"><b>Команда К2</b><span>Артём Соколов, старший тренер</span></figcaption></figure>', 'hello')
body += sec(sechead('Две зоны для лазания') + '\n' + offers([
    offer('Боулдеринг', ['невысокие трассы', 'без верёвки, над мягкими матами', '120 трасс', 'подходит новичкам'], 'Короткие трассы без верёвки над мягкими матами. Идеально для первого знакомства и отработки техники.', link_btn('Первый раз', 'pervyj-raz.html', 'btn btn--primary'), 'Зона боулдеринга', id='bouldering', img='k2-first-1.jpg'),
    offer('Трудность', ['стены 13 метров', 'со страховкой верёвкой', '40 трасс', 'есть автостраховка'], 'Длинные трассы на стенах до 13 метров со страховкой. Здесь занимаются с тренером и самостоятельно.', link_btn('Базовые курсы', 'bazovye-kursy.html', 'btn btn--primary'), 'Зона трудности', dark=True, id='trudnost', img='k2-hall.jpg')]), 'zones')
# «Почему лазать в К2»: слева фото (горизонтальное), справа — заголовок, крупные цифры и три преимущества с иконками.
# Фото ВРЕМЕННОЕ (чужой зал, на кадре метки и водяной знак другого скалодрома) — заменить снимком К2
body += ('<section class="sec dark lp-why3" id="why"><div class="wrap lp-why3__g">'
         '<figure class="lp-why3__ph reveal"><img src="assets/img/p-overhang.jpg" alt="Скалолаз на нависании в зоне боулдеринга" loading="lazy">'
         '<figcaption class="lp-why3__tag"><b class="d">Новый скалодром</b><span>Новые стены, зацепы и&nbsp;снаряжение</span></figcaption></figure>'
         '<div class="lp-why3__b"><span class="mark reveal">Почему К2</span><h2 class="d h2 reveal">Почему лазать в&nbsp;К2</h2>'
         '<div class="lp-why3__stats reveal"><div><b class="d">13<small>м</small></b><span>высоты&nbsp;— просторная зона трудности для&nbsp;занятий со&nbsp;страховкой</span></div>'
         '<div><b class="d">1300<small>м²</small></b><span>боулдеринг и&nbsp;трудность под&nbsp;одной крышей</span></div></div>'
         '<ul class="lp-why3__list">' + ''.join('<li class="reveal"><span class="lp-why3__ic">%s</span><div><b>%s</b><p>%s</p></div></li>' % x for x in [
             (I_SPARK, 'Новый скалодром', 'Новые стены, зацепы и&nbsp;снаряжение.'), (I_PEOPLE, 'PRO команда', 'Тренеры для&nbsp;взрослых и&nbsp;детей.'),
             (I_GEAR, 'Прокат снаряжения', 'Всё необходимое&nbsp;— на&nbsp;месте.')]) + '</ul>'
         '<div class="lp-why3__go reveal">' + link_btn('Первый раз', 'pervyj-raz.html', 'btn btn--primary') + link_btn('Как добраться', 'kontakty.html#route', 'btn btn--sec') + '</div>'
         '</div></div></section>')
# Удобства: «маршрут вечера» шагами + плитки с иконками
I_HANGER = ico('<path d="M10 6a2 2 0 1 1 2 2v2"/><path d="M12 10l-8.5 6.5a1 1 0 0 0 .6 1.5h15.8a1 1 0 0 0 .6-1.5z"/>')
I_SHOWER = ico('<path d="M5 21V9a5 5 0 0 1 9-3"/><path d="M11 9h7l-1.5 2.5h-4z"/><path d="M12.5 14.5l-.6 1.6M15 14.5v1.7M17.5 14.5l.6 1.6M13 19l-.4 1.2M16.6 19l.4 1.2"/>')
I_LOCK = ico('<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M12 3v18M9.5 10v3M14.5 10v3"/>')
I_TOWEL = ico('<path d="M3 5h18"/><path d="M7 5v13a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V5"/><path d="M7 14h10M7 16.5h10"/>')
I_SHOE = ico('<path d="M3 17v-4.5c2-.5 3.5-2 4.5-4l1-2 3 2.5c1.5 1.3 3 2 5 2.3 2.4.4 4.5 1.4 4.5 3.7v2z"/><path d="M3 20h18M9.5 9.5l1.5 1.2M11.5 8l1.5 1.2"/>')
I_PARK = ico('<rect x="4" y="4" width="16" height="16" rx="4"/><path d="M10 17V7h3a3 3 0 0 1 0 6h-3"/>')
AM_FLOW = [(I_PIN, 'После работы'), (I_HANGER, 'Переоделись'), (I_UP, 'Тренировка'), (I_SHOWER, 'Душ')]
I_SAUNA = ico('<path d="M4 20h16"/><path d="M6 20v-6h12v6"/><path d="M9 10c-1-1.5 1-2.5 0-4M12 10c-1-1.5 1-2.5 0-4M15 10c-1-1.5 1-2.5 0-4"/>')
I_STRETCH = ico('<circle cx="12" cy="5" r="2"/><path d="M4 10l8 1 8-1"/><path d="M12 11v4l-4 6M12 15l4 6"/>')
I_BAR = ico('<path d="M3 5h18"/><path d="M6 5v3M18 5v3"/><circle cx="12" cy="11" r="2"/><path d="M9 5l2 4.5M15 5l-2 4.5M12 13v4l-2 4M12 17l2 4"/>')
# Плитки «В К2 есть»: (иконка, название, пометка, превью). Фото — ВРЕМЕННЫЕ (кадры зала): заменить реальными фото зон.
# В MODX: каждая зона — строка MIGX (иконка, название, фото); по клику фото открывается во весь экран и листается по всем зонам.
AM_TILES = [(I_HANGER, 'Раздевалки', '', 'p-mat.jpg'), (I_SHOWER, 'Душевые', '', 'k2-first-2.jpg'), (I_SAUNA, 'Сауна', '', 'p-cave.jpg'),
            (I_LOCK, 'Шкафчики', '', 'k2-first-3.jpg'), (I_STRETCH, 'Зал для&nbsp;стретчинга', '', 'k2-hall.jpg'), (I_BAR, 'Турники', '', 'k2-first-1.jpg'),
            (I_CHILD, 'Детская зона', '', 'k2-rock.jpg'), (I_TOWEL, 'Аренда полотенец', '', 'p-chalk.jpg'), (I_SHOE, 'Прокат снаряжения', '', 'p-mat.jpg'),
            (I_PARK, 'Парковка', 'бесплатно', 'k2-hall.jpg')]
body += sec('<div class="am am--wide"><div class="am__main reveal"><h2 class="d h2">Всё для&nbsp;комфортных тренировок</h2>'
            '<p class="lead muted">Можно прийти сразу после работы: переодеться, потренироваться и&nbsp;принять душ.</p></div>'
            '<div class="am__route reveal"><ol class="am__flow" aria-label="Как проходит визит">' + ''.join('<li><span class="am__fi">%s</span><span>%s</span></li>' % x for x in AM_FLOW) + '</ol>'
            '<p class="lp-bring__note">%s<span>Ежедневно, 7:00–23:00</span></p></div></div>' % I_TIME +
            '<div class="am__side"><p class="lp-k reveal">В&nbsp;К2 есть <span class="am__hint">— нажмите, чтобы посмотреть фото</span></p><ul class="am__tiles am__tiles--ph" data-lb>' + ''.join(
                '<li class="reveal"><button class="am__t" type="button" data-lb-i data-cap="%s" aria-label="Фото: %s"><span class="am__ph"><img src="assets/img/%s" alt="%s" loading="lazy">'
                '<span class="am__zoom" aria-hidden="true">%s</span></span><span class="am__ti">%s</span><b>%s</b>%s</button></li>' % (
                    t.replace('&nbsp;', ' '), t.replace('&nbsp;', ' '), img, t.replace('&nbsp;', ' '), ico('<circle cx="11" cy="11" r="6"/><path d="M20 20l-4.5-4.5M11 8v6M8 11h6"/>'), ic, t,
                    '<small>%s</small>' % n if n else '') for ic, t, n, img in AM_TILES) + '</ul></div>', 'amenities')
body += sec(sechead('Атмосфера К2', 'Нажмите на фото — откроется галерея') + '\n' + gal(GAL_HALL), 'photos', cls='lp-alt')
body += sec(sechead('Команда', '', link_btn('Все тренеры', 'trenery.html', 'btn btn--sec reveal')) + '\n' + coaches(COACH_FISH_ADULT[:3] + COACH_FISH_KIDS[:1]), 'coaches')
body += REVIEWS('Отзывы о К2') + CONTACT
page('o-skalodrome.html', 'О скалодроме К2 — боулдеринг и трудность в центре Петербурга', 'Новый скалодром: 1300 м², стены 13 метров, зоны боулдеринга и трудности, раздевалки и душевые. 7 минут от м. Площадь Ленина.', body, gallery=True)


# ======================= ТРЕНЕРЫ =======================
body = head([('О нас', 'o-skalodrome.html'), ('Тренеры', '')], 'Тренеры скалодрома К2', 'Хороший тренер не только сильно лазает, но и спокойно, понятно объясняет. Наши работают и со взрослыми, и с детьми.')
body += sec(sechead('Тренеры для взрослых') + '\n' + coaches(COACH_FISH_ADULT) + '\n<!-- В MODX: тренеры — ресурсы или MIGX (фото, имя, должность, квалификация) -->', 'adults')
body += sec(sechead('Детские тренеры') + '\n' + coaches(COACH_FISH_KIDS), 'kids', cls='lp-alt')
body += nextcta('Хотите заниматься с тренером?', 'Оставьте заявку — подберём тренера под ваш уровень и цель.', join_btn('Оставить заявку', 'Занятия с тренером', 'trial', 'btn btn--light'), 'персонально · с тренером · ')
page('trenery.html', 'Тренеры — скалодром К2', 'Тренеры скалодрома К2: тренировки для взрослых и детей, пробные занятия, школа скалолазания.', body)


# ======================= ВИДЕО =======================
VIDEOS = [('obzor', 'Обзор скалодрома', 'k2-hall.jpg', 'p-blue.jpg'), ('sovety', 'Советы новичку', 'p-chalk.jpg', 'p-focus.jpg'), ('deti', 'Детская секция', 'k2-first-2.jpg', 'k2-10.jpg'),
          ('razminka', 'Разминка и заминка', 'p-mat.jpg', 'p-fun.jpg'), ('fan', '[Фан со скалодрома]', 'p-cave.jpg', 'p-heart.jpg'), ('more', '[Видео]', 'k2-first-1.jpg', 'p-roof.jpg')]
body = head([('О нас', 'o-skalodrome.html'), ('Видео', '')], 'Видео со скалодрома', 'Обзоры, советы новичкам, разминка и жизнь К2.')
body += sec('<div class="vgrid">%s</div>\n<!-- В MODX: ссылка на ролик (TV) в data-video. Пока ролика нет — обложка с пометкой «Видео скоро» -->' % ''.join(
    '<div class="lp-video reveal" id="%s" data-video=""><picture><source media="(max-width: 767px)" srcset="assets/img/%s"><img src="assets/img/%s" alt="" loading="lazy"></picture><span class="lp-video__shade"></span>'
    '<button class="lp-video__play" type="button" aria-label="Смотреть: %s"><svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg></button>'
    '<span class="lp-video__soon">Видео скоро</span><span class="lp-video__meta"><b>%s</b><small>[0:45]</small></span></div>' % (s, vimg, img, t, t) for s, t, img, vimg in VIDEOS), 'list', 'dark')
page('video.html', 'Видео — скалодром К2', 'Видео со скалодрома К2: обзор зала, советы новичкам, детская секция, разминка и заминка.', body)


# ======================= ВАКАНСИИ =======================
# Каждая вакансия: шапка (название, условия коротко, пара строк) + «Подробнее» — полное описание разделами (большой текст помещается).
# «Откликнуться» открывает окно заявки в режиме вакансии: data-join-job — название уходит в заявку, выбор тренировки скрыт (js/landing.js).
# В MODX: вакансия — ресурс (название, короткие условия, анонс, разделы описания — в контенте); список — pdoResources.
JOB_SECTIONS = [('Чем предстоит заниматься', ['[Обязанность — например, проводить групповые и персональные тренировки]', '[Обязанность]', '[Обязанность]', '[Обязанность]']),
                ('Кого мы ищем', ['[Требование — опыт, квалификация, навыки]', '[Требование]', '[Требование]', '[Будет плюсом]']),
                ('Что мы предлагаем', ['[Условие — оформление, оплата, бонусы]', '[Условие]', '[Условие]', '[Условие]']),
                ('График и оплата', ['[График — например, 2/2 или по сменам]', '[Оплата — оклад, процент, от __ ₽]', '[Испытательный срок]'])]
JOBS = [('trener', '[Тренер по скалолазанию]', ['[Полная занятость]', '[от ___ ₽]', '[Опыт от 1 года]']),
        ('administrator', '[Администратор скалодрома]', ['[Сменный график]', '[от ___ ₽]', '[Без опыта]']),
        ('detskij-trener', '[Детский тренер]', ['[Частичная занятость]', '[от ___ ₽]', '[Опыт работы с детьми]'])]
def job_btn(t, cls='btn btn--primary'):
    tt = re.sub(r'[\[\]]', '', t)
    return '<button class="%s js-join" type="button" aria-haspopup="dialog" aria-controls="join" data-join-title="Отклик на&nbsp;вакансию" data-join-job="%s">Откликнуться</button>' % (cls, tt)
def job(slug, t, tags):
    secs = ''.join('<div class="job__sec"><h3 class="job__h">%s</h3><ul class="job__ul">%s</ul></div>' % (h, ''.join('<li>%s</li>' % x for x in items)) for h, items in JOB_SECTIONS)
    return ('<article class="job reveal" id="%s"><div class="job__head"><div class="job__info"><h2 class="d job__t">%s</h2>'
            '<ul class="job__tags">%s</ul><p class="job__lead">[Пара предложений о&nbsp;вакансии: кого ищем и&nbsp;чем интересна работа.]</p></div>'
            '<div class="job__btns">%s</div></div>'
            '<details class="job__more"><summary><span class="job__open">Подробнее о&nbsp;вакансии</span><span class="job__close">Свернуть описание</span><i aria-hidden="true"></i></summary>'
            '<div class="job__body"><p class="job__about">[Вводный абзац: о&nbsp;скалодроме, команде и&nbsp;о&nbsp;том, почему эта роль важна. Здесь может быть большой текст со&nbsp;всеми нюансами&nbsp;— он разворачивается по&nbsp;кнопке «Подробнее».]</p>'
            '<div class="job__secs">%s</div><div class="job__foot"><p>Подходит? Оставьте телефон&nbsp;— перезвоним и&nbsp;расскажем подробнее.</p>%s</div></div></details></article>') % (
        slug, t, ''.join('<li>%s</li>' % x for x in tags), job_btn(t), secs, job_btn(t))
body = head([('О нас', 'o-skalodrome.html'), ('Вакансии', '')], 'Вакансии', 'Ищем людей, которые любят скалолазание и умеют работать с людьми.')
body += sec('<h2 class="sr">Открытые вакансии</h2><div class="jobs">' + ''.join(job(*j) for j in JOBS) + '</div>' +
            '\n' + helpbox('Не нашли подходящую вакансию?', 'Напишите нам — расскажите о себе и опыте.', '<a class="btn btn--sec" href="mailto:[почта]">Написать на почту</a>'), 'list')
page('vakansii.html', 'Вакансии — скалодром К2', 'Работа на скалодроме К2: тренеры, администраторы и другие вакансии.', body)


# ======================= ОТЗЫВЫ =======================
# Шапка, виджет отзывов с внешнего сервиса и лента видеоотзывов со стрелками (листание — js/landing.js).
# В MODX: виджет — код Яндекс Карт / 2ГИС; видеоотзывы — ссылки на ролики (обложка, подпись, длительность)
REV_VIDEO = [('k2-02.jpg', 'После пробной тренировки', '0:45'), ('k2-10.jpg', 'Родители детской секции', '1:10'), ('p-smile.jpg', 'Ученики школы скалолазания', '0:58'),
             ('k2-13.jpg', 'Базовый курс за&nbsp;месяц', '1:24'), ('p-fun.jpg', 'Как прошёл выезд на&nbsp;скалы', '0:52'), ('k2-12.jpg', 'Индивидуальные тренировки', '1:05'),
             ('k2-07.jpg', 'Лазаем всей семьёй', '0:49')]
REV_CTL = ('<div class="sechead__ctl reveal"><button class="ibtn ibtn--line js-prev" type="button" aria-label="Назад">' + ico('<path d="M19 12H5M11 6l-6 6 6 6"/>') + '</button>'
           '<button class="ibtn ibtn--line js-next" type="button" aria-label="Вперёд">' + ARROW + '</button></div>')
body = head([('О нас', 'o-skalodrome.html'), ('Отзывы', '')], 'Отзывы о скалодроме К2', 'Что говорят гости, ученики и&nbsp;родители наших спортсменов.',
            '<div class="blog-head__go"><button class="btn btn--primary js-rv" type="button" aria-haspopup="dialog" aria-controls="rv">Оставить отзыв</button></div>')
body += sec(sechead('Отзывы на картах', 'Честные оценки гостей с&nbsp;Яндекс Карт и&nbsp;2ГИС') +
            '<div class="widget widget--rev reveal"><b>Отзывы с&nbsp;Яндекс Карт и&nbsp;2ГИС</b><span>Здесь подключится виджет отзывов внешнего сервиса</span></div>', 'widget')
body += ('<section class="sec dark videos stack" id="video"><div class="wrap">' + sechead('Видеоотзывы', '', REV_CTL) + '</div>'
         '<div class="shorts" tabindex="0" aria-label="Видеоотзывы, листается">' + ''.join(
             '<a class="short" href="video.html"><img src="assets/img/%s" alt="" loading="lazy"><span class="scrim"></span>%s<span class="short__c"><b>%s</b><small>%s</small></span></a>' % (f, PLAY, t, d)
             for f, t, d in REV_VIDEO) + '</div></section>')
# Популярные вопросы (ответы — из фактов, которые уже есть на сайте)
body += faq_sec([('Где оставить отзыв о К2?', 'На Яндекс Картах или в 2ГИС&nbsp;— найдите «Скалодром К2». Или расскажите администратору на ресепшене: мы читаем каждый отзыв.'),
                 ('С чего начать, если я никогда не лазал?', 'С пробной тренировки. Это час с тренером: опыт и своё снаряжение не нужны.'),
                 ('Нужно ли своё снаряжение?', 'Нет. Скальные туфли, страховочную систему и магнезию выдадим на месте.'),
                 ('С какого возраста можно заниматься?', 'Детей берём с 5 лет&nbsp;— в детскую секцию. Взрослые программы&nbsp;— с 16 лет.'),
                 ('Можно ли записать видеоотзыв?', 'Да. Скажите администратору или тренеру&nbsp;— снимем короткий ролик после тренировки.'),
                 ('Где находится скалодром?', 'В центре Петербурга, в 7 минутах пешком от метро «Площадь Ленина».')], 'Популярные вопросы')
# Окно «Где оставить отзыв»: три сервиса. В href — ссылки на карточку К2 в сервисе (страница отзывов), пока «#» — подставит разработчик
RV_PIN = '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg>'
RV = [('yandex', 'Яндекс Карты', '#'), ('dgis', '2ГИС', '#'), ('google', 'Google Карты', '#')]
body += ('<dialog class="modal rv" id="rv" aria-labelledby="rv-t"><div class="rv__card">'
         '<button class="modal__x rv__x" type="button" aria-label="Закрыть">' + ico('<path d="M6 6l12 12M18 6L6 18"/>') + '</button>'
         '<h3 class="d rv__t" id="rv-t">Где оставить отзыв?</h3>'
         '<p class="rv__s">Выберите сервис&nbsp;— откроется страница К2, где можно поставить оценку и&nbsp;написать пару слов. Спасибо!</p>'
         '<ul class="rv__list">' + ''.join(
             '<li><a class="rv__i rv__i--%s" href="%s" target="_blank" rel="noopener"><span class="rv__ic">%s</span><b>%s</b><span class="rv__go">' % (k, h, RV_PIN, n) + ARROW + '</span></a></li>'
             for k, n, h in RV) + '</ul></div></dialog>')
page('otzyvy.html', 'Отзывы о скалодроме К2', 'Отзывы гостей, учеников и родителей о скалодроме К2: оценки на Яндекс Картах и 2ГИС и видеоотзывы.', body)


# ======================= ДОКУМЕНТЫ =======================
# Список документов: карточка (название, о чём документ, редакция) — ссылка на отдельную страницу документа.
DOC_ICON = ico('<path d="M7 3h7l5 5v13H7z"/><path d="M14 3v5h5M10 13h6M10 17h6"/>')
DOCS = [('pravila', 'Правила посещения', 'Как посещать скалодром: допуск к&nbsp;лазанию, поведение в&nbsp;зале, детям и&nbsp;гостям.'),
        ('tb', 'Техника безопасности', 'Страховка, маты, зоны лазания&nbsp;— что важно знать до&nbsp;первой тренировки.'),
        ('zayavlenie', 'Заявление от родителей', 'Согласие родителя или законного представителя на&nbsp;занятия ребёнка.'),
        ('oferta', 'Договор оферты', 'Условия оказания услуг, оплаты, переноса и&nbsp;возврата.'),
        ('privacy', 'Политика обработки персональных данных', 'Как мы собираем, используем и&nbsp;защищаем ваши данные.')]
DOC_PAGE = DOC_URL  # каждый документ — отдельная текстовая страница
def doc_head(i, t, d, go):
    return ('<span class="dcx__ic">%s</span><span class="dcx__b"><b class="dcx__t d">%s</b><span class="dcx__d">%s</span>'
            '<span class="dcx__meta">Редакция от&nbsp;1&nbsp;сентября 2026</span></span>%s') % (DOC_ICON, t, d, go)
DOC_GO = '<span class="dcx__go"><span class="dcx__open">Открыть</span><span class="dcx__close">Свернуть</span><i aria-hidden="true"></i></span>'
body = head([('О нас', 'o-skalodrome.html'), ('Документы', '')], 'Документы', 'Правила посещения, техника безопасности, оферта и политика обработки персональных данных.')
body += sec('<div class="dcx-list">' + ''.join(
    ('<a class="dcx dcx--link reveal" id="%s" href="%s">%s</a>' % (i, DOC_PAGE[i], doc_head(i, t, d, '<span class="dcx__go">Открыть' + ARROW + '</span>'))) if i in DOC_PAGE else
    ('<details class="dcx reveal" id="%s"><summary>%s</summary><div class="dcx__body"><p>%s</p></div></details>' % (i, doc_head(i, t, d, DOC_GO), DOC_STUB))
    for i, t, d in DOCS) + '</div>', 'list')
page('dokumenty.html', 'Документы — скалодром К2', 'Правила посещения, техника безопасности, договор оферты и политика обработки персональных данных скалодрома К2.', body)


# ======================= ТЕКСТОВАЯ СТРАНИЦА (шаблон) =======================
# Информационная страница на шаблоне «Документов»: слева — название, редакция и оглавление (липкое), справа — текст.
# sections: [(id, заголовок, html-текст раздела)]. В MODX: обычный ресурс — заголовок + контент (h2 разделов собираются в оглавление).
def textpage(slug, crumb, title, desc, lead, sections, side='Документ', meta='Редакция от&nbsp;1&nbsp;сентября 2026', back=('Все документы', 'dokumenty.html')):
    b = head([('О нас', 'o-skalodrome.html'), ('Документы', 'dokumenty.html'), (crumb, '')], title, lead)
    b += ('<section class="neutral docs-sec"><div class="art__wrap wrap docs tpage">'
          '<aside class="art__side"><p class="art__side-t">%s</p><p class="tpage__t d">%s</p>%s'
          '<ol class="toc">%s</ol>%s</aside><div class="art__body">%s</div></div></section>') % (
        side, title, '<p class="tpage__meta">%s</p>' % meta if meta else '',
        ''.join('<li><a href="#%s">%s</a></li>' % (i, re.sub(r'^\d+\.\s*', '', h)) for i, h, _ in sections),  # номер в оглавлении ставит сам .toc
        '<a class="tpage__back" href="%s">%s</a>' % (back[1], back[0]) if back else '',
        ''.join('<section class="doc" id="%s"><h2>%s</h2>%s</section>' % (i, h, t) for i, h, t in sections))
    page(slug, title + ' — скалодром К2', desc, b)

def _ul(*items): return '<ul>%s</ul>' % ''.join('<li>%s</li>' % x for x in items)
OPER = '[ООО «Название»] (ИНН [__________], ОГРН [_____________], адрес: [г.&nbsp;Санкт-Петербург, ул.&nbsp;____, д.&nbsp;__])'
# Текст политики — ПРИМЕР по 152-ФЗ «О персональных данных»; реквизиты в [скобках]. Перед публикацией — проверить юристу.
PRIVACY = [
    ('obshchie', '1. Общие положения',
     '<p>Настоящая политика определяет, как %s (далее&nbsp;— «Оператор», «скалодром К2») обрабатывает и&nbsp;защищает персональные данные посетителей сайта [адрес сайта] и&nbsp;клиентов скалодрома.</p>'
     '<p>Политика составлена в&nbsp;соответствии с&nbsp;Федеральным законом от&nbsp;27.07.2006 №&nbsp;152-ФЗ «О&nbsp;персональных данных». Оставляя данные на&nbsp;сайте, вы&nbsp;подтверждаете, что ознакомились с&nbsp;политикой и&nbsp;согласны с&nbsp;ней.</p>' % OPER),
    ('ponyatiya', '2. Основные понятия',
     _ul('<b>Персональные данные</b>&nbsp;— любая информация, относящаяся к&nbsp;прямо или косвенно определённому физическому лицу.',
         '<b>Обработка</b>&nbsp;— любое действие с&nbsp;персональными данными: сбор, запись, хранение, уточнение, использование, передача, удаление.',
         '<b>Субъект персональных данных</b>&nbsp;— человек, чьи данные обрабатываются: посетитель сайта, клиент скалодрома, родитель или законный представитель ребёнка.')),
    ('dannye', '3. Какие данные мы обрабатываем',
     '<p>Мы просим только то, что нужно для записи и&nbsp;связи с&nbsp;вами:</p>' +
     _ul('имя;', 'номер телефона;', '[адрес электронной почты&nbsp;— если вы оставляете его в&nbsp;форме];',
         'данные ребёнка (имя, возраст)&nbsp;— только со&nbsp;слов и&nbsp;с&nbsp;согласия родителя или законного представителя;',
         'технические данные: cookie-файлы, IP-адрес, сведения о&nbsp;браузере и&nbsp;действиях на&nbsp;сайте&nbsp;— [если подключена Яндекс&nbsp;Метрика].')),
    ('celi', '4. Цели обработки',
     _ul('запись на&nbsp;тренировки, курсы, мероприятия и&nbsp;в&nbsp;детскую секцию;', 'обратная связь: ответ на&nbsp;заявку, звонок или сообщение;',
         'заключение и&nbsp;исполнение договора (оферты), продажа абонементов и&nbsp;сертификатов;', 'рассмотрение откликов на&nbsp;вакансии;',
         'улучшение работы сайта и&nbsp;анализ посещаемости [при использовании Яндекс&nbsp;Метрики].')),
    ('osnovaniya', '5. Правовые основания',
     '<p>Мы обрабатываем данные на&nbsp;основании вашего согласия, которое вы даёте, отмечая галочку в&nbsp;форме на&nbsp;сайте, а&nbsp;также для&nbsp;заключения и&nbsp;исполнения договора, стороной которого вы являетесь.</p>'),
    ('poryadok', '6. Как мы обрабатываем и храним данные',
     _ul('Данные обрабатываются с&nbsp;использованием средств автоматизации и&nbsp;без них.',
         'Данные хранятся на&nbsp;серверах, расположенных на&nbsp;территории Российской Федерации.',
         'Мы храним данные не&nbsp;дольше, чем этого требуют цели обработки, или до&nbsp;отзыва согласия. [Срок хранения&nbsp;— уточнить.]',
         'Мы не&nbsp;передаём данные третьим лицам, кроме случаев, предусмотренных законом, и&nbsp;подрядчиков, которые помогают нам работать (например, [CRM-система, сервис рассылок]),&nbsp;— на&nbsp;условиях конфиденциальности.')),
    ('prava', '7. Ваши права',
     '<p>Вы можете в&nbsp;любой момент:</p>' +
     _ul('узнать, какие ваши данные мы обрабатываем;', 'попросить уточнить, исправить или удалить данные;', 'отозвать согласие на&nbsp;обработку;',
         'обжаловать действия Оператора в&nbsp;Роскомнадзоре или в&nbsp;суде.') +
     '<p>Для этого напишите нам на&nbsp;[почта] или отправьте письмо по&nbsp;адресу Оператора. Мы ответим в&nbsp;течение 10&nbsp;рабочих дней.</p>'),
    ('cookie', '8. Cookie-файлы',
     '<p>Сайт использует cookie, чтобы корректно работать и&nbsp;понимать, какие страницы полезны посетителям. Вы можете отключить cookie в&nbsp;настройках браузера&nbsp;— при этом часть функций сайта может работать хуже.</p>'),
    ('zashchita', '9. Защита данных',
     '<p>Мы принимаем правовые, организационные и&nbsp;технические меры, чтобы защитить данные от&nbsp;неправомерного доступа, изменения, распространения и&nbsp;уничтожения. Доступ к&nbsp;данным есть только у&nbsp;сотрудников, которым он нужен для работы.</p>'),
    ('kontakty', '10. Контакты и изменения политики',
     '<p>Оператор: %s.<br>Электронная почта: [почта]. Телефон: +7&nbsp;(812)&nbsp;000-00-00.</p>'
     '<p>Мы можем обновлять политику. Новая редакция действует с&nbsp;момента публикации на&nbsp;этой странице, если в&nbsp;ней не&nbsp;указано иное.</p>' % OPER),
]
textpage('politika-personalnyh-dannyh.html', 'Политика обработки персональных данных', 'Политика обработки персональных данных',
         'Как скалодром К2 собирает, использует и защищает персональные данные посетителей сайта и клиентов.',
         'Как мы собираем, используем и&nbsp;защищаем ваши данные.', PRIVACY)

# Остальные документы — те же текстовые страницы; разделы — каркас, текст даст скалодром (юридические тексты — от заказчика)
def doc_sections(heads): return [('r%d' % (n + 1), '%d. %s' % (n + 1, h), STUB_P) for n, h in enumerate(heads)]
STUB_P = '<p>[Текст раздела предоставит скалодром.]</p>'
textpage(DOC_URL['pravila'], 'Правила посещения', 'Правила посещения',
         'Правила посещения скалодрома К2: допуск к лазанию, поведение в зале, правила для детей и гостей.',
         'Как посещать скалодром: допуск к&nbsp;лазанию, поведение в&nbsp;зале, детям и&nbsp;гостям.',
         doc_sections(['Общие положения', 'Время работы и вход в зал', 'Допуск к самостоятельному лазанию', 'Правила поведения в зале', 'Дети на скалодроме', 'Ответственность посетителей']))
textpage(DOC_URL['tb'], 'Техника безопасности', 'Техника безопасности',
         'Техника безопасности на скалодроме К2: боулдеринг, страховка, автостраховки, снаряжение.',
         'Страховка, маты, зоны лазания&nbsp;— что важно знать до&nbsp;первой тренировки.',
         doc_sections(['Общие правила', 'Боулдеринг', 'Трудность и страховка', 'Автостраховки', 'Снаряжение', 'Если что-то случилось']))
textpage(DOC_URL['zayavlenie'], 'Заявление от родителей', 'Заявление от родителей',
         'Заявление родителя или законного представителя на занятия ребёнка на скалодроме К2.',
         'Согласие родителя или законного представителя на&nbsp;занятия ребёнка.',
         doc_sections(['Кто заполняет заявление', 'Текст заявления', 'Согласие на обработку персональных данных', 'Как передать заявление']))
textpage(DOC_URL['oferta'], 'Договор оферты', 'Договор оферты',
         'Договор публичной оферты скалодрома К2: услуги, цены, оплата, перенос и возврат.',
         'Условия оказания услуг, оплаты, переноса и&nbsp;возврата.',
         doc_sections(['Предмет договора', 'Услуги и цены', 'Порядок оплаты', 'Перенос и возврат', 'Права и обязанности сторон', 'Реквизиты']))


# ======================= КОНТАКТЫ =======================
body = head([('Контакты', '')], 'Контакты и как добраться', 'Скалодром К2 — 7 минут пешком от м. Площадь Ленина.')
body += CONTACT.replace('sec--flush', '')
body += sec(sechead('Как добраться') + '''
<div class="lp-bring">
  <div class="lp-bring__main reveal">
    <p class="lead">[Адрес], 7 минут пешком от м. Площадь Ленина.</p>
    <ol class="route-steps"><li>[Выход из метро — уточняется]</li><li>[Путь до скалодрома — уточняется]</li><li>[Вход в здание — уточняется]</li></ol>
    <p class="lp-bring__note">%s<span>Ежедневно, 7:00–23:00</span></p>
  </div>
  <div class="lp-bring__side lp-map reveal"><b>[Яндекс Карта]</b><span>Карта со скалодромом — встраивается кодом конструктора карт</span></div>
</div>''' % I_TIME, 'route')
body += sec(sechead('Реквизиты') + '\n<p class="lead muted reveal">[Реквизиты]</p>', 'requisites', cls='lp-alt')
page('kontakty.html', 'Контакты и как добраться — скалодром К2', 'Телефон, мессенджеры, адрес и схема проезда: скалодром К2 в 7 минутах от м. Площадь Ленина.', body)



# ======================= УНИВЕРСАЛЬНЫЙ ШАБЛОН УСЛУГИ =======================
# service_page(slug, title, desc, d) собирает страницу любой новой услуги из данных d.
# Порядок блоков фиксированный (01–14). Блок, для которого в d нет данных, на странице не выводится.
# Обязательные: 01 первый экран, 05 форматы и цены, 13 вопросы, 14 финальный призыв. Остальные — по ситуации.
# notes=True — жёлтые подписи блоков (только для страницы-образца shablon-uslugi.html).
TPL_BLOCKS = [  # (номер, ключ в d, название, обязательный, id раздела, пункт подменю)
    (1, 'hero', 'Первый экран', True, 'top', ''),
    (2, 'subnav', 'Подменю разделов', False, '', ''),
    (3, 'who', 'Кому подойдёт / чем отличается', False, 'who', 'Кому подойдёт'),
    (4, 'why', 'Почему К2', False, 'why', 'Почему К2'),
    (5, 'formats', 'Форматы и цены', True, 'formats', 'Форматы и цены'),
    (6, 'how', 'Как проходит', False, 'how', 'Как проходит'),
    (7, 'video', 'Видео', False, 'video', 'Видео'),
    (8, 'schedule', 'Расписание', False, 'schedule', 'Расписание'),
    (9, 'coaches', 'Тренеры', False, 'coaches', 'Тренеры'),
    (10, 'gallery', 'Фотогалерея', False, 'photos', 'Фото'),
    (11, 'reviews', 'Отзывы', False, 'reviews', 'Отзывы'),
    (12, 'contact', '«Нужно связаться»', False, 'contacts', ''),
    (13, 'faq', 'Частые вопросы', True, 'faq', 'Вопросы'),
    (14, 'cta', 'Финальный призыв', True, '', ''),
]

def why_block(h2, img, img_m, stats, cards2, btn, mark='Почему К2'):
    """04. Фото на весь блок, 3 цифры, 2 карточки и кнопка (цифры считаются — js/landing.js).
    stats: [(число, единица, выделенное слово или '', текст)]; cards2: [(заголовок, текст)], первая — красная"""
    return ('<section class="sec neutral sec--flush" id="why"><div class="wrap"><div class="lp-why2 lp-why2--inset dark">'
            '<div class="lp-why2__bg" aria-hidden="true"><picture><source media="(max-width: 767px)" srcset="assets/img/%s"><img src="assets/img/%s" alt="" loading="lazy"></picture></div>'
            '<div class="wrap lp-why2__in"><div class="lp-why2__head"><span class="mark reveal">%s</span><h2 class="d lp-why2__t reveal">%s</h2></div><ul class="lp-why2__stats">%s</ul>'
            '<div class="lp-why2__cards">%s<div class="lp-why2__go reveal">%s</div></div></div></div></div></section>') % (
        img_m, img, mark, h2,
        ''.join('<li class="reveal"><b class="d"><span data-count="%s">%s</span><small>%s</small></b><span>%s%s</span></li>' % (n, n, u, '<em>%s</em> ' % em if em else '', t) for n, u, em, t in stats),
        ''.join('<div class="lp-why2__c%s reveal"><b class="d">%s</b><p>%s</p></div>' % (' lp-why2__c--red' if i == 0 else '', t, p) for i, (t, p) in enumerate(cards2)), btn)

def hour_block(h2, total, items, note='* Распределение времени может отличаться на&nbsp;усмотрение тренера.'):
    """06а. «Что будет происходить N минут» — шкала времени, фото меняются по шагам (js/landing.js).
    items: [(с минуты, до минуты, фото, заголовок, длительность, текст)]"""
    return ('<section class="sec dark stack lp-hour" id="how" data-total="%d"><div class="lp-hour__track"><div class="lp-hour__stage wrap">'
            '<div class="lp-hour__head"><h2 class="d h2 reveal">%s<sup class="lp-hour__star">*</sup></h2>'
            '<p class="lp-hour__clock reveal" aria-hidden="true"><b class="d">00</b><span>мин<br>из&nbsp;%d</span></p></div>'
            '<div class="lp-hour__g"><div class="lp-hour__pics reveal" aria-hidden="true">' % (total, h2, total) +
            ''.join('<img%s src="assets/img/%s" alt="" loading="lazy">' % (' class="is-on"' if i == 0 else '', x[2]) for i, x in enumerate(items)) +
            '<span class="lp-hour__badge"><i></i><span>Шаг 01 · %s</span></span></div><ol class="lp-hour__steps">' % items[0][4] +
            ''.join('<li%s data-from="%d" data-to="%d"><img class="lp-hour__ph" src="assets/img/%s" alt="" loading="lazy"><button type="button"><span class="lp-hour__n d">%02d</span>'
                    '<span><b>%s</b><small>%s</small></span></button><p>%s</p></li>' % (' class="is-on"' if i == 0 else '', f, t, img, i + 1, h, dd, txt)
                    for i, (f, t, img, h, dd, txt) in enumerate(items)) + '</ol></div>'
            '<div class="lp-hour__bar reveal" style="--total:%d" aria-hidden="true">' % total + ''.join('<span style="--w:%d"></span>' % (t - f) for f, t, *_ in items) +
            ''.join('<small style="--x:%d">%d</small>' % (f, f) for f, *_ in items) + '<small style="--x:%d">%d мин</small></div>' % (total, total) +
            '<p class="lp-hour__note reveal">%s</p></div></div></section>' % note)

def video_block(h2, lead, img, img_m, cap, dur, url=''):
    """07а. Один ролик. Пока ссылки нет (data-video пустой) — по кнопке пометка «Видео скоро»"""
    return ('<section class="sec dark lp-video-sec" id="video"><div class="wrap">' + sechead(h2, lead) +
            '<div class="lp-video reveal" data-video="%s"><picture><source media="(max-width: 767px)" srcset="assets/img/%s"><img src="assets/img/%s" alt="" loading="lazy"></picture>'
            '<span class="lp-video__shade"></span><button class="lp-video__play" type="button" aria-label="Смотреть: %s"><svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg></button>'
            '<span class="lp-video__soon">Видео скоро</span><span class="lp-video__meta"><b>%s</b><small>%s</small></span></div></div></section>') % (url, img_m, img, cap, cap, dur)

def shorts_block(h2, items, all_href='video.html'):
    """07б. Лента вертикальных роликов со стрелками. items: [(ссылка, обложка, подпись, длительность)]"""
    return ('<section class="sec dark videos stack" id="video"><div class="wrap">' + sechead(h2, '', SH_CTL.replace('video.html', all_href)) + '</div>'
            '<div class="shorts" tabindex="0" aria-label="Видео, листается">' + ''.join(
                '<a class="short" href="%s"><img src="assets/img/%s" alt="" loading="lazy"><span class="scrim"></span>'
                '<span class="play"><svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg></span><span class="short__c"><b>%s</b><small>%s</small></span></a>' % x for x in items) + '</div></section>')

def sched_block(rows, note='Расписание примерное. Точное время и&nbsp;свободные места подскажет администратор.'):
    """08. Таблица расписания. rows: [(группа, дни и время, подпись)]"""
    return ('<div class="ksch reveal">' + ''.join('<div class="ksch__row"><b>%s</b><span class="d">%s</span><small>%s</small></div>' % r for r in rows) +
            '<p class="ksch__note">%s</p></div>' % note)

def service_page(slug, title, desc, d, notes=False):
    alt = [False]
    def light(inner, id, cls=''):  # светлые блоки чередуют фон, чтобы соседние не сливались
        alt[0] = not alt[0]
        return sec(inner, id, cls=(cls + ' lp-alt' if alt[0] else cls).strip())
    out = {}
    if d.get('hero'):
        h = d['hero']
        out['hero'] = hero(h['crumbs'], h['h1'], h['lead'], h['img'], h.get('marks', ()), h['btns'], h.get('alt', ''))
    if d.get('who'):
        w = d['who']
        out['who'] = light('<div class="lp-intro"><h2 class="d h2 reveal">%s</h2><p class="lead muted reveal">%s</p></div>\n' % (w['h2'], w['lead']) +
                           cards(w['cards'], len(w['cards']) if len(w['cards']) == 3 else 4, w.get('imgs')), 'who')
    if d.get('why'):
        out['why'] = why_block(**d['why'])
    if d.get('formats'):
        f = d['formats']
        out['formats'] = light(sechead(f.get('h2', 'Форматы и&nbsp;цены'), f.get('lead', '')) + '\n' + offers([offer(**o) for o in f['items']], 3 if len(f['items']) == 3 else 2) +
                               (helpbox(*f['help']) if f.get('help') else ''), 'formats', 'stack')
    if d.get('how'):
        hw = d['how']
        out['how'] = hour_block(hw['h2'], hw['total'], hw['items']) if hw.get('total') else sec(sechead(hw['h2'], hw.get('lead', '')) + steps(hw['items']), 'how', 'dark', 'stack')
    if d.get('video'):
        v = d['video']
        out['video'] = shorts_block(v['h2'], v['items']) if v.get('items') else video_block(v['h2'], v.get('lead', ''), v['img'], v.get('img_m', v['img']), v['cap'], v['dur'], v.get('url', ''))
    if d.get('schedule'):
        s = d['schedule']
        out['schedule'] = light(sechead(s.get('h2', 'Расписание'), s.get('lead', '')) + sched_block(s['rows']), 'schedule')
    if d.get('coaches'):
        c = d['coaches']
        out['coaches'] = light(sechead(c.get('h2', 'Тренеры'), '', link_btn('Все тренеры', 'trenery.html', 'btn btn--sec reveal')) + '\n' + coaches(c['items']), 'coaches')
    if d.get('gallery'):
        g = d['gallery']
        out['gallery'] = light(sechead(g.get('h2', 'Фотогалерея'), 'Нажмите на фото — откроется галерея') + '\n' + gal(g['items']), 'photos')
    if d.get('reviews'):
        out['reviews'] = REVIEWS(d['reviews'] if isinstance(d['reviews'], str) else 'Отзывы')
    if d.get('contact'):
        out['contact'] = CONTACT
    if d.get('faq'):
        out['faq'] = faq_sec(d['faq'])
    if d.get('cta'):
        out['cta'] = nextcta(*d['cta'])
    if d.get('subnav'):  # подменю собирается само — из тех блоков, что есть на странице
        items = [(sid, lbl) for _, k, _, _, sid, lbl in TPL_BLOCKS if lbl and k in out]
        out['subnav'] = ('<nav class="lp-sub" aria-label="Разделы страницы"><button class="lp-sub__toggle" type="button" aria-expanded="false"><span class="lp-sub__cur">Разделы страницы</span>'
                         '<span class="lp-sub__more">Разделы<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg></span></button><div class="wrap lp-sub__in">'
                         + ''.join('<a href="#%s" style="--i:%d">%s<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5v14M6 13l6 6 6-6"/></svg></a>' % (h, i, t) for i, (h, t) in enumerate(items))
                         + '</div></nav>')
    body = ''
    for n, k, name, req, _, _ in TPL_BLOCKS:
        if k not in out:
            continue
        html = out[k]
        tag = '%02d · %s · %s' % (n, name, 'обязательный' if req else 'можно выключить')
        if notes and k != 'subnav':  # жёлтая подпись — первым элементом секции
            if k == 'hero' and 'subnav' in out:
                tag += ' &nbsp;|&nbsp; ниже — 02 · Подменю разделов · можно выключить (пункты собираются сами)'
            html = re.sub(r'(<section\b[^>]*?)>', r'\1 data-tpl><span class="tpl-note">%s</span>' % tag.replace('\\', r'\\'), html, count=1)
        body += '<!-- ===== БЛОК %s ===== -->\n%s\n' % (tag.replace('&nbsp;', ' '), html)
    page(slug, title, desc, body, gallery='gallery' in out)
    if notes:  # образец не должен попадать в поиск
        p = os.path.join(ROOT, slug); t = io.open(p, encoding='utf-8').read()
        io.open(p, 'w', encoding='utf-8').write(t.replace('<meta name="description"', '<meta name="robots" content="noindex">\n<meta name="description"', 1))

# ---------- Страница-образец: все 14 блоков, текст и цены — рыба ----------
service_page('shablon-uslugi.html', 'Шаблон услуги — скалодром К2', 'Образец страницы услуги: все блоки шаблона.', dict(
    hero=dict(crumbs=[('Для взрослых', 'dlya-vzroslyh.html'), ('Название услуги', '')], h1='Название услуги на&nbsp;скалодроме К2',
              lead='Одно-два предложения: что это за&nbsp;услуга, для кого она и&nbsp;какой результат получит человек после занятий.',
              img='k2-05.jpg', alt='Скалолаз на стене К2',
              marks=[(I_SPARK, 'Любой уровень'), (I_GEAR, 'Снаряжение выдаём'), (I_PEOPLE, 'В группе или персонально'), (I_TIME, '60 минут')],
              btns=join_btn('Записаться', 'Запись на&nbsp;услугу', 'trial') + link_btn('Цены', '#formats', 'btn btn--sec')),
    subnav=True,
    who=dict(h2='Кому подойдёт', lead='Коротко: чем эта услуга отличается от&nbsp;других форматов и&nbsp;кому она нужна больше всего.',
             cards=[('Без опыта', 'Никогда не&nbsp;лазали&nbsp;— тренер покажет всё с&nbsp;нуля.'), ('Лазали когда-то давно', 'Вспомните технику и&nbsp;правила страховки.'),
                    ('Для пары и друзей', 'Можно прийти вместе и&nbsp;заниматься в&nbsp;одной группе.'), ('Хочется быстрее', 'Программа построена так, чтобы прогресс был заметен сразу.')],
             imgs=['k2-first-1.jpg', 'p-chalk.jpg', 'k2-first-3.jpg', 'k2-hall.jpg']),
    why=dict(h2='Почему заниматься в&nbsp;К2', img='k2-first-2.jpg', img_m='k2-09.jpg',
             stats=[('13', 'м', 'высоты', 'Высокие стены&nbsp;— лазаем только со&nbsp;страховкой.'), ('1300', 'м²', '', 'Боулдеринг и&nbsp;трудность под одной крышей.'),
                    ('7', 'мин', 'от метро', 'Площадь Ленина&nbsp;— удобно приехать после работы.')],
             cards2=[('Опытные тренеры', 'Объясняют понятно и&nbsp;следят за&nbsp;безопасностью.'), ('Новый скалодром', 'Новые стены, зацепы и&nbsp;снаряжение.')],
             btn=join_btn('Записаться', 'Запись на&nbsp;услугу', 'trial', 'btn btn--light')),
    formats=dict(h2='Форматы и&nbsp;цены', lead='Два или три варианта. Цены и&nbsp;состав&nbsp;— примерные.', items=[
        dict(title='В группе', items=['группа до 8 человек', 'с тренером', '60 минут', 'снаряжение выдаём'], desc='Короткое описание формата: чем он хорош.',
             foot=price(1500, 1900) + join_btn('Записаться', 'Запись: в&nbsp;группе', 'trial'), badge='Популярный', img='k2-first-1.jpg'),
        dict(title='Персонально', items=['один на один с тренером', 'удобное время', '60 минут'], desc='Короткое описание формата: чем он хорош.',
             foot=price(3500) + join_btn('Записаться', 'Запись: персонально', 'trial'), badge='Быстрее всего', dark=True, img='p-cave.jpg'),
        dict(title='Абонемент', items=['8 занятий', 'срок 30 дней', 'выгоднее разовых'], desc='Короткое описание формата: чем он хорош.',
             foot=price(9600) + join_btn('Записаться', 'Запись: абонемент', 'sub'), img='k2-hall.jpg')],
        help=('Не&nbsp;знаете, что выбрать?', 'Оставьте заявку&nbsp;— администратор подберёт формат под ваш уровень.', join_btn('Подобрать формат', 'Подберём формат', 'trial', 'btn btn--sec'))),
    how=dict(h2='Что будет происходить 60&nbsp;минут?', total=60, items=[
        (0, 10, 'p-gear.jpg', 'Знакомство и&nbsp;экипировка', '~10 мин', 'Тренер знакомится с&nbsp;вами и&nbsp;подбирает снаряжение.'),
        (10, 20, 'p-chalk.jpg', 'Инструктаж и&nbsp;разминка', '~10 мин', 'Правила безопасности и&nbsp;разминка всего тела.'),
        (20, 55, 'k2-first-2.jpg', 'Основная часть', '~35 мин', 'Трассы, техника и&nbsp;упражнения&nbsp;— под ваш уровень.'),
        (55, 60, 'k2-first-3.jpg', 'Итог', '~5 мин', 'Тренер подскажет, как двигаться дальше.')]),
    video=dict(h2='Как это проходит', lead='Короткий видеообзор услуги', img='k2-first-3.jpg', img_m='k2-12.jpg', cap='Видеообзор услуги', dur='1:20'),
    schedule=dict(h2='Расписание', rows=[('Утренняя группа', 'Пн, Ср · 9:00–10:00', 'Тренер Максим Лебедев'), ('Вечерняя группа', 'Вт, Чт · 19:30–20:30', 'Тренер Илья Морозов'),
                                         ('Выходного дня', 'Сб · 12:00–13:00', 'Тренер Ольга Кузнецова')]),
    coaches=dict(h2='Тренеры', items=COACH_FISH_ADULT),
    gallery=dict(items=GAL_SCHOOL),
    reviews='Отзывы',
    contact=True,
    faq=[('Нужен ли опыт?', 'Нет, тренер начнёт с&nbsp;основ и&nbsp;подстроится под ваш уровень.'), ('Что взять с&nbsp;собой?', 'Удобную спортивную одежду. Снаряжение выдадим на&nbsp;месте.'),
         ('Как оплатить?', 'На&nbsp;ресепшене или онлайн после заявки.'), ('Можно ли перенести занятие?', 'Да, предупредите администратора не&nbsp;позже чем за&nbsp;12 часов.'),
         ('С&nbsp;какого возраста?', 'Взрослые программы&nbsp;— с&nbsp;16 лет, для детей есть отдельные услуги.'), ('Как записаться?', 'Оставьте заявку или позвоните&nbsp;— подберём время.')],
    cta=('Готовы попробовать?', 'Оставьте заявку&nbsp;— перезвоним и&nbsp;подберём удобное время.', join_btn('Оставить заявку', 'Запись на&nbsp;услугу', 'trial', 'btn btn--light'), 'оставьте заявку · перезвоним · '),
), notes=True)

# ======================= 404 =======================
body = head([('Страница не найдена', '')], 'Такой страницы нет', 'Возможно, её перенесли. Начните с главной или найдите нужное через поиск.',
            '<div class="btns" style="margin-top:32px">' + link_btn('На главную', 'index.html', 'btn btn--primary') + link_btn('Цены', 'ceny.html', 'btn btn--sec') + '</div>')
page('404.html', 'Страница не найдена — скалодром К2', 'Такой страницы нет на сайте скалодрома К2.', body)

print('страниц:', len(PAGES), '·', ', '.join(PAGES))


# ======================= PDF с прайсом (кнопка «Скачать PDF») =======================
# Собирается из тех же GROUPS, что и страница цен. В MODX: файл загружают в админке (настройка k2_price_pdf).
import subprocess, tempfile, pathlib
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
LOGO = re.search(r'<svg viewBox="19 24 698 322" aria-hidden="true">.*?</svg>', MAIN, re.S).group(0)
fonts = pathlib.Path(ROOT, 'assets', 'fonts').as_uri()
rows = ''.join('<h2>%s</h2><table>%s</table>' % (t, ''.join('<tr><td><b>%s</b><small>%s</small></td><td class="v">%s</td></tr>' % r[:3] for r in rs)) for _, t, rs in GROUPS)
sheet = '''<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>
@font-face{font-family:U;src:url("%(F)s/Unbounded.woff2")}@font-face{font-family:O;src:url("%(F)s/Onest.woff2")}
@page{size:A4;margin:16mm 16mm 18mm}
body{font:11pt/1.45 O,sans-serif;color:#2D2D2D;margin:0}
header{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:3px solid #D9493E;padding-bottom:10px;margin-bottom:8px}
header svg{width:70px;fill:#2D2D2D}header p{margin:0;text-align:right;font-size:9pt;color:#6b6b6b}
h1{font:700 20pt/1.2 U,sans-serif;margin:18px 0 4px}h2{font:700 12pt/1.3 U,sans-serif;margin:20px 0 6px;color:#D9493E;break-after:avoid}
table{width:100%%;border-collapse:collapse;break-inside:avoid}td{padding:7px 0;border-bottom:1px solid #e4e1dc;vertical-align:top}
td small{display:block;color:#6b6b6b;font-size:9pt}td.v{text-align:right;white-space:nowrap;font-weight:600;padding-left:16px}
footer{margin-top:24px;font-size:9pt;color:#6b6b6b}
</style></head><body><header>%(LOGO)s<p>Скалодром К2 · [Адрес], м. Площадь Ленина<br>+7 (812) 000-00-00 · [почта]</p></header>
<h1>Цены скалодрома К2</h1><p>Пакеты тренировок — на сайте в разделе «Пакеты».</p>%(ROWS)s
<footer>Цены действительны с&nbsp;1&nbsp;декабря 2026. Актуальные цены — на сайте и у администратора.</footer></body></html>''' % {'F': fonts, 'LOGO': LOGO, 'ROWS': rows}
out = os.path.join(ROOT, 'assets', 'docs'); os.makedirs(out, exist_ok=True)
if os.path.exists(CHROME):
    with tempfile.TemporaryDirectory() as tmp:
        src = os.path.join(tmp, 'price.html'); io.open(src, 'w', encoding='utf-8').write(typograph(sheet))
        subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--no-pdf-header-footer', '--user-data-dir=' + os.path.join(tmp, 'p'),
                        '--print-to-pdf=' + os.path.join(out, 'k2-ceny.pdf'), pathlib.Path(src).as_uri()], check=True, capture_output=True, timeout=60)
    print('прайс: assets/docs/k2-ceny.pdf')
else:
    print('Chrome не найден — PDF прайса не пересобран')
