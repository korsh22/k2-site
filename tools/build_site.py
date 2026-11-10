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

PRICE = '<span class="price"><b class="price__new"><span class="sr">Цена: </span>от [___] ₽</b></span>'
DOC_STUB = '[Текст документа предоставит скалодром. В MODX — отдельный ресурс или поле страницы.]'


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

def cards(items, n=4):
    return '<div class="lp-cards4%s">%s</div>' % (' lp-cards4--3' if n == 3 else '', ''.join(
        '<div class="lp-c reveal"><span class="lp-c__n">%02d</span><b>%s</b><p>%s</p></div>' % (i + 1, t, d) for i, (t, d) in enumerate(items)))

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
    return '<ol class="lp-steps">%s</ol>' % ''.join('<li class="reveal"><span class="lp-steps__n">%02d</span><b>%s</b><p>%s</p></li>' % (i + 1, t, d) for i, (t, d) in enumerate(items))

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

def coaches(items):
    return '<div class="lp-coaches">%s</div>' % ''.join(
        '<article class="lp-coach reveal"><div class="lp-coach__img"><img src="assets/img/coach-%d.jpg" alt="Фото-заглушка" loading="lazy"></div>'
        '<b class="lp-coach__n">%s</b><span class="lp-coach__r">%s</span><span class="lp-coach__q">%s</span></article>' % ((i % 4 + 1,) + tuple(c)) for i, c in enumerate(items))  # фото — временные заглушки

def nextcta(h2, text, btn):
    return sec('<div class="lp-next reveal"><div><h2 class="d h2">%s</h2><p class="lead">%s</p></div>%s</div>' % (h2, text, btn), tone='neutral', cls='sec--flush')

def helpbox(b, text, btn):
    return '<div class="lp-help reveal"><p><b>%s</b> %s</p>%s</div>' % (b, text, btn)

def tiles(items):
    """Карточки-ссылки на разделы: [(заголовок, подпись, ссылка, картинка)]"""
    return '<div class="ptiles">%s</div>' % ''.join(
        '<a class="ptile reveal" href="%s"><span class="ptile__img"><img src="assets/img/%s" alt="" loading="lazy"></span><span class="ptile__b"><b class="ptile__t">%s</b><span class="ptile__d">%s</span>'
        '<span class="ptile__f">%s<span class="go go--s">%s</span></span></span></a>' % (h, img, t, d, PRICE if pr else '<span></span>', ARROW) for t, d, h, img, pr in items)

CONTACT = sec(P['CONTACT'], 'contacts', cls='sec--flush')
REVIEWS = lambda t='Отзывы': sec(sechead(t) + '\n<div class="widget reveal"><b>[Виджет отзывов]</b><span>Подтягивается с внешнего сервиса — [Яндекс Карты / 2ГИС]</span></div>', 'reviews', cls='lp-alt')
COACH_STUB = [('[Имя Фамилия]', 'Старший тренер', '[Квалификация · стаж]'), ('[Имя Фамилия]', 'Тренер по боулдерингу', '[Квалификация · стаж]'),
              ('[Имя Фамилия]', 'Тренер по трудности', '[Квалификация · стаж]'), ('[Имя Фамилия]', 'Детский тренер', '[Квалификация · стаж]')]
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
             ('Можно ли лазать самостоятельно?', 'Да, если вы уже умеете лазать и знаете правила безопасности. Есть разовые посещения и абонементы. [Условия допуска уточняются.]'),
             ('Нужно ли своё снаряжение?', 'Нет. Скальные туфли, страховочную систему и магнезию выдадим на месте. [Условия проката уточняются.]'),
             ('Есть ли ограничения по возрасту?', 'Взрослые программы — с 16 лет. Для детей от 5 лет есть детская секция и пробные тренировки.'),
             ('Как записаться?', 'Оставьте заявку или позвоните — администратор подберёт удобное время и формат.')]
body = hero([('Для взрослых', '')], 'Скалолазание для взрослых на скалодроме К2',
            'Впервые? Начните с пробной тренировки или базового курса. Уже лазаете — выбирайте школу, персональные тренировки с тренером или приходите сами.',
            'k2-05.jpg', [(I_SPARK, 'Любой уровень'), (I_GEAR, 'Снаряжение выдаём'), (I_PEOPLE, 'В группе или персонально'), (I_TIME, '7 дней в неделю')],
            join_btn('Подобрать тренировку', 'Подберём тренировку', 'trial') + link_btn('Цены', 'ceny.html', 'btn btn--sec'), 'Скалолаз на стене К2')
# Кнопка видео на фото «Первого раза» — ведёт к ролику на странице пробной тренировки
PLAY_FIRST = '<a class="lp-f__play" href="pervyj-raz.html#video"><i>' + ico('<path d="M8 5v14l11-7z"/>') + '</i><span class="lp-f__pl">Видео: как проходит первая тренировка</span><span class="lp-f__ps">Смотреть видео</span></a>'
body += sec('<p class="lp-k reveal">Новичкам</p>\n' + offers([
    offer('Первый раз', ['для любого возраста от 16 лет', 'для любого уровня подготовки', 'всё снаряжение выдаём', '60 минут', 'персонально или в группе'],
          'Час с тренером: разберём основы и пройдём первые трассы.', PRICE + link_btn('Подробнее', 'pervyj-raz.html', 'btn btn--primary'), 'Пробная тренировка', img='k2-first-3.jpg', play=PLAY_FIRST),
    offer('Базовые курсы', ['программа из 3–5 тренировок', 'всё снаряжение выдаём', 'персонально или в группе'],
          'Освоите боулдеринг, трудность и страховку — и сможете лазать без тренера.', PRICE + link_btn('Подробнее', 'bazovye-kursy.html', 'btn btn--primary'), 'Курс', img='p-chalk.jpg')]) +
    '\n<p class="lp-k lp-k--gap reveal">Уже занимаюсь</p>\n' + offers([
    offer('Тренировки в группе', ['регулярно, по расписанию', 'с тренером', 'техника, сила, прогресс'], 'Школа скалолазания: программа, группа своего уровня и заметный прогресс.',
          PRICE + link_btn('Подробнее', 'shkola.html', 'btn btn--primary'), img='k2-first-1.jpg'),
    offer('Индивидуальные тренировки', ['персонально с тренером', 'под вашу задачу', 'удобное время'], 'Самый быстрый путь к цели — один на один с тренером.',
          PRICE + link_btn('Подробнее', 'individualnye.html', 'btn btn--primary'), dark=True, img='p-cave.jpg'),
    offer('Самостоятельные посещения', ['разовые и абонементы', 'боулдеринг и трудность', 'прокат снаряжения'], 'Приходите, когда удобно, и лазайте в своём ритме.',
          PRICE + link_btn('Подробнее', 'samostoyatelno.html', 'btn btn--primary'), img='k2-hall.jpg')], 3), 'formats')
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
def pack_offer(s, dark=False, btn=None):
    p = PK[s]
    return offer(p['t'], p['b'], p['d'], PRICE + (btn or join_btn('Записаться', 'Пакет «%s»' % re.sub('<[^>]+>', '', p['t']), 'trial')), dark=dark, id=s, img=p['img'])
body += sec(sechead('Программы курса', 'Выберите, с чего начать. Сомневаетесь — тренер подскажет на пробной тренировке.') + '\n' +
            offers([pack_offer('start'), pack_offer('baza'), pack_offer('rasshirennyj')], 3) + '\n' +
            helpbox('Уже умеете лазать с верхней страховкой?', 'Следующий шаг — курс «Нижняя страховка».', link_btn('Подробнее', 'pakety.html#nizhnyaya-strahovka')), 'programs')
body += sec(sechead('Как проходит курс') + '\n' + steps([('Знакомство', 'Тренер узнаёт ваш опыт и цели, подбирает снаряжение.'), ('Основы', 'Правила безопасности, разминка и первые трассы на боулдеринге.'),
                                                         ('Страховка', 'Выходим на высокую стену и учимся страховать друг друга.'), ('Итог', 'Финальная проверка: вы лазаете и страхуете самостоятельно.')]) +
            '\n<div class="lp-after reveal"><p class="lp-after__t d">После курса вы:</p>' + li(['знаете правила безопасности на скалодроме', 'умеете страховать напарника', 'уверенно лазаете на боулдеринге и трудности', 'можете ходить в зал самостоятельно', 'знаете, как тренироваться дальше']) + '</div>', 'how', 'dark', 'stack')
body += sec(sechead('Для кого подходит') + '\n' + cards([('После пробной тренировки', 'Понравилось — и хочется научиться лазать по-настоящему.'), ('Без опыта', '«Старт» рассчитан на тех, кто ни разу не лазал.'),
                                                          ('Для пары и друзей', 'Пройдите курс вместе — и дальше страхуйте друг друга.'), ('Лазали когда-то давно', 'Вспомните технику и страховку за пару занятий.')]), 'who')
body += REVIEWS('Отзывы после курса') + faq_sec([('Сколько длится курс?', 'От 3 до 5 тренировок в зависимости от программы. [Срок и расписание уточняются.]'),
                                                  ('Можно ли пройти курс персонально?', 'Да, в группе или индивидуально с тренером.'),
                                                  ('Что будет, если пропущу занятие?', '[Условия переноса уточняются.]'), ('Нужна ли подготовка?', 'Нет. Достаточно удобной спортивной формы.')])
body += nextcta('Не знаете, какую программу выбрать?', 'Оставьте заявку — администратор подберёт курс под ваш опыт и цели.', join_btn('Оставить заявку', 'Поможем выбрать курс', 'trial', 'btn btn--light'))
page('bazovye-kursy.html', 'Базовые курсы скалолазания для взрослых — скалодром К2', 'Курс из 3–5 тренировок: освоите боулдеринг, трудность и страховку. В группе или персонально, снаряжение выдаём.', body)


# ======================= ШКОЛА СКАЛОЛАЗАНИЯ =======================
body = hero([('Для взрослых', 'dlya-vzroslyh.html'), ('Школа скалолазания', '')], 'Школа скалолазания для взрослых',
            'Регулярные тренировки с тренером: техника, сила и новые уровни сложности — по программе, а не наугад.',
            'k2-04.jpg', [(I_CAL, 'По расписанию'), (I_UP, 'Рост по уровням'), (I_PEOPLE, 'Группы и персонально'), (I_SHIELD, 'Опытные тренеры')],
            join_btn('Записаться в школу', 'Запись в школу скалолазания', 'sub') + link_btn('Расписание', '#schedule', 'btn btn--sec'), 'Тренировка скалолаза')
body += sec('<div class="lp-intro"><h2 class="d h2 reveal">Чем школа отличается от пробной тренировки</h2><p class="lead muted reveal">Пробная тренировка — знакомство. В школе вы занимаетесь регулярно по программе: тренер видит ваш прогресс и ставит следующую цель.</p></div>\n' +
            cards([('Техника', 'Работа ног, баланс, умение «читать» трассу.'), ('Сила', 'ОФП и специальные упражнения для скалолазов.'), ('Прогресс', 'Каждый месяц — трассы сложнее.'), ('Цели', 'Подготовка к выездам на скалы и соревнованиям.')]), 'who')
body += sec(sechead('Форматы') + '\n' + offers([
    offer('Групповые тренировки', ['по расписанию', 'группа [до __ человек]', 'с тренером', 'абонемент на [__] занятий'], 'Тренируйтесь в группе своего уровня — так прогресс идёт быстрее и веселее.', PRICE + join_btn('Записаться', 'Групповые тренировки в школе', 'sub'), 'Регулярно'),
    offer('Индивидуальные тренировки', ['персонально с тренером', 'под вашу цель', 'удобное время'], 'Один на один с тренером — самый быстрый прогресс.', PRICE + link_btn('Подробнее', 'individualnye.html', 'btn btn--primary'), 'Персонально', dark=True)]), 'formats', cls='stack')
body += sec(sechead('Уровни подготовки', 'Тренер определит уровень на первом занятии') + '\n' + cards([('Начальный', 'После пробной тренировки или базового курса. [Описание уточняется.]'),
                                                                                                     ('Средний', 'Уверенно лазаете и страхуете, хотите сложнее. [Описание уточняется.]'),
                                                                                                     ('Продвинутый', 'Подготовка к соревнованиям и скалам. [Описание уточняется.]')], 3), 'levels', 'dark', 'stack')
body += sec(sechead('Расписание') + '\n<div class="widget reveal"><b>[Расписание групп]</b><span>Дни и время занятий — из CRM или таблицы в админке</span></div>', 'schedule')
body += sec(sechead('Тренеры школы', '', link_btn('Все тренеры', 'trenery.html', 'btn btn--sec reveal')) + '\n' + coaches(COACH_STUB), 'coaches', cls='lp-alt')
body += REVIEWS('Отзывы и результаты') + faq_sec([('Можно ли прийти в школу без опыта?', 'Лучше начать с пробной тренировки или базового курса — тогда в школе вы сразу начнёте прогрессировать.'),
                                                   ('Как оплачивать занятия?', 'Абонементом на несколько занятий. [Условия уточняются.]'),
                                                   ('Что, если пропущу тренировку?', '[Условия переноса уточняются.]'), ('Можно ли заниматься в любой день?', 'Группы занимаются по расписанию. Если неудобно — подойдут индивидуальные тренировки.')])
body += nextcta('Хотите тренироваться регулярно?', 'Оставьте заявку — подберём группу под ваш уровень и расписание.', join_btn('Оставить заявку', 'Запись в школу скалолазания', 'sub', 'btn btn--light'))
page('shkola.html', 'Школа скалолазания для взрослых — скалодром К2', 'Регулярные тренировки с тренером: техника, сила, подготовка к выездам и соревнованиям. Группы по уровням и индивидуальные занятия.', body)


# ======================= ИНДИВИДУАЛЬНЫЕ =======================
body = hero([('Для взрослых', 'dlya-vzroslyh.html'), ('Индивидуальные тренировки', '')], 'Индивидуальные тренировки с тренером',
            'Тренер работает только с вами: от первых шагов до подготовки к скалам и соревнованиям.',
            'k2-00.jpg', [(I_PEOPLE, 'Один на один'), (I_CAL, 'Удобное время'), (I_UP, 'Под вашу цель'), (I_SPARK, 'Любой уровень')],
            join_btn('Записаться', 'Индивидуальная тренировка'), 'Лазание на «клине»')
body += sec(sechead('Когда это лучший выбор') + '\n' + cards([('Хочется быстрее', 'Всё внимание тренера — только вам.'), ('Есть конкретная задача', 'Пройти трассу, освоить нижнюю страховку, подготовиться к выезду.'),
                                                             ('Неудобно расписание групп', 'Время подбираем под вас.'), ('Нужен свой темп', 'Нагрузка и программа — под ваш уровень.')]), 'who')
body += sec(sechead('Форматы и цены') + '\n' + offers([
    offer('Разовая тренировка', ['персонально с тренером', '[60] минут', 'снаряжение — [условия уточняются]'], 'Чтобы попробовать формат или решить одну конкретную задачу.', PRICE + join_btn('Записаться', 'Индивидуальная тренировка')),
    offer('Пакет тренировок', ['[__] тренировок', 'программа под вашу цель', 'выгоднее разовых'], 'Для системного прогресса по плану.', PRICE + link_btn('Пакеты', 'pakety.html', 'btn btn--primary'), dark=True)]) + '\n' +
    helpbox('Вы новичок?', 'Персональная пробная тренировка для 1–3 участников — на странице «Первый раз».', link_btn('Первый раз', 'pervyj-raz.html')), 'formats', cls='stack')
body += sec(sechead('Тренеры', '', link_btn('Все тренеры', 'trenery.html', 'btn btn--sec reveal')) + '\n' + coaches(COACH_STUB), 'coaches', cls='lp-alt')
body += CONTACT + faq_sec([('Можно ли прийти вдвоём?', '[Условия для 2–3 участников уточняются.] Для новичков есть персональная пробная тренировка для 1–3 человек.'),
                           ('Можно ли выбрать тренера?', 'Да, укажите это в заявке.'), ('Как перенести тренировку?', '[Условия переноса уточняются.]'), ('Нужно ли своё снаряжение?', 'Нет, выдадим на месте.')])
page('individualnye.html', 'Индивидуальные тренировки по скалолазанию — скалодром К2', 'Персональные тренировки с тренером под вашу цель и в удобное время. Скалодром К2, м. Площадь Ленина.', body)


# ======================= САМОСТОЯТЕЛЬНЫЕ =======================
body = hero([('Для взрослых', 'dlya-vzroslyh.html'), ('Самостоятельные посещения', '')], 'Самостоятельные посещения',
            'Уже умеете лазать? Приходите, когда удобно: боулдеринг и трудность — разово или по абонементу.',
            'k2-01.jpg', [(I_TIME, '[Часы посещения]'), (I_CAL, 'Разово или абонемент'), (I_GEAR, 'Прокат снаряжения'), (I_SHIELD, 'Нужен допуск')],
            link_btn('Цены', '#prices', 'btn btn--primary') + link_btn('Правила посещения', 'dokumenty.html#pravila', 'btn btn--sec'), 'Скалолаз под нависанием')
# «Кто может лазать сам»: пропуск-чеклист + красная карточка «Не уверены?»
I_ROPE = ico('<path d="M9 3h6l-1 5a2 2 0 0 1-4 0z"/><path d="M12 10v3"/><circle cx="12" cy="17" r="4"/>')
WHO = [(I_UP, 'Умеете лазать', 'Прошли пробную тренировку, базовый курс или&nbsp;лазали где-то ещё.', 'Боулдеринг и&nbsp;трудность'),
       (I_SHIELD, 'Знаете технику безопасности', 'Перед первым посещением&nbsp;— инструктаж. [Порядок уточняется.]', 'Боулдеринг и&nbsp;трудность'),
       (I_ROPE, 'Умеете страховать', 'Нужен допуск к&nbsp;страховке и&nbsp;напарник. [Условия допуска уточняются.]', 'Только трудность')]
body += sec(sechead('Кто может лазать самостоятельно') + '<div class="who">'
    '<div class="who__pass reveal"><div class="who__head"><span class="who__k">Допуск</span><b class="d">Самостоятельное лазание</b><span class="who__hint">Нужно всё по&nbsp;списку</span></div><ul class="who__list">' + ''.join(
        '<li><span class="who__ic">%s</span><div><b>%s</b><p>%s</p></div><span class="who__z">%s</span><span class="who__ok" aria-hidden="true">%s</span></li>' % (ic, t, d, z, CHECK) for ic, t, d, z in WHO) + '</ul></div>'
    '<div class="who__help reveal"><span class="who__q d">?</span><b class="d">Не&nbsp;уверены?</b><p>Начните с&nbsp;базового курса: за&nbsp;3–5 тренировок научим лазать, страховать и&nbsp;всему необходимому.</p>'
    + link_btn('Базовые курсы', 'bazovye-kursy.html', 'btn btn--light') + '</div></div>', 'who')
body += sec(sechead('Какие зоны доступны') + '\n' + offers([
    offer('Боулдеринг', ['невысокие трассы', 'без верёвки, над матами', 'можно одному'], 'Короткие невысокие трассы без верёвки — можно прийти одному.', link_btn('О зоне', 'o-skalodrome.html#bouldering', 'btn btn--primary'), 'Без страховки'),
    offer('Трудность', ['стены 13 метров', 'со страховкой', 'нужен напарник и допуск'], 'Длинные трассы на высокой стене со страховкой — нужен напарник.', link_btn('О зоне', 'o-skalodrome.html#trudnost', 'btn btn--primary'), 'Со страховкой', dark=True)]), 'zones', 'dark', 'stack')
body += sec('<div class="prices__grid"><div class="prices__main">' + sechead('Разовое посещение и абонементы') + plist([
    ('Разовое посещение', 'Самостоятельно, боулдеринг и трудность', '[___] ₽'), ('Абонемент [на месяц]', 'Самостоятельные посещения', '[___] ₽'),
    ('Абонемент [на __ посещений]', 'Самостоятельные посещения', '[___] ₽'), ('Прокат снаряжения', 'Скальники, страховочная система', '[___] ₽')]) +
    '<div class="prices__all reveal">' + link_btn('Все цены', 'ceny.html') + '</div></div><aside class="prices__aside"><div class="note reveal"><b>Часы посещения</b><p>[Ежедневно, __:__–__:__]</p>' +
    link_btn('Правила посещения', 'dokumenty.html#pravila', 'btn btn--light') + '</div></aside></div>', 'prices')
body += CONTACT + faq_sec([('Нужно ли записываться заранее?', '[Порядок записи уточняется.]'), ('Можно ли прийти без напарника?', 'На боулдеринг — да. Для трудности нужен напарник со страховкой.'),
                           ('Что входит в прокат?', 'Скальные туфли, страховочная система. [Список уточняется.]'), ('Есть ли раздевалка и душ?', 'Да: раздевалки, душевые, шкафчики, аренда полотенец.')])
page('samostoyatelno.html', 'Самостоятельные посещения скалодрома — К2', 'Разовые посещения и абонементы для тех, кто умеет лазать: боулдеринг и трудность, прокат снаряжения. Скалодром К2.', body)


# ======================= ДЛЯ ДЕТЕЙ (хаб) =======================
FAQ_KIDS = [('С какого возраста можно?', 'С 5 лет: есть детские пробные тренировки и регулярная секция.'),
            ('Это безопасно?', 'Да. Дети лазают под присмотром тренера: на боулдеринге — над мягкими матами, на высокой стене — только со страховкой.'),
            ('Что взять ребёнку?', 'Только удобную спортивную форму. Снаряжение выдадим на месте.'),
            ('Можно ли родителям остаться?', '[Условия уточняются.]'),
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
# 4. Расписание (вид пока не определён: виджет или своё)
body += sec('<p class="lp-k reveal">Расписание</p>' + sechead('Выберите группу и удобное время', 'Регулярные занятия проходят по абонементам. Посмотрите расписание своей возрастной группы и доступное количество тренировок в месяц.') +
            tabs('schedule', [(k, t) for k, t, _, _, _ in KGROUPS]) +
            ''.join('<div class="widget reveal in" data-tab-of="schedule" data-t="%s"%s><b>[Расписание: группа %s]</b><span>Вид расписания определяется: виджет или таблица на сайте</span></div>' % (k, '' if i == 0 else ' hidden', t) for i, (k, t, _, _, _) in enumerate(KGROUPS)), 'schedule', cls='lp-alt')
# 5. Абонементы: карточка переворачивается по клику (список абонементов уточняется)
ABO_BACK = [('Срок действия', '[точные условия]'), ('Порядок записи', '[условия]'), ('Пропуски и переносы', '[правила]'), ('Снаряжение', '[включено или нет]'), ('Дополнительные платежи', '[если есть]')]
TURN = ico('<path d="M4 12a8 8 0 0 1 14-5.3L20 9"/><path d="M20 4v5h-5"/><path d="M20 12a8 8 0 0 1-14 5.3L4 15"/><path d="M4 20v-5h5"/>')
ABO_PH = {'5': 'p-fun.jpg', '8': 'k2-09.jpg', '11': 'k2-11.jpg'}
def abo(k, t, m):
    """Карточка абонемента: метка, фото группы, крупный возраст, условия с иконками, цена; по клику переворачивается на условия"""
    age = t.replace(' лет', '')
    return ('<button class="abo reveal" type="button" aria-pressed="false" aria-label="Абонемент для группы %s: подробнее об условиях"><span class="abo__in">'
            '<span class="abo__s abo__f"><span class="abo__top"><span class="abo__tag"><i></i>Абонемент</span><img class="abo__ph" src="assets/img/%s" alt="" loading="lazy"></span>'
            '<span class="abo__age d">%s<small>лет</small></span>'
            '<span class="abo__fs"><span class="abo__fi">%s<span>[Количество] тренировок в&nbsp;месяц</span></span><span class="abo__fi">%s<span>Занятие %s</span></span></span>'
            '<span class="abo__pr"><span class="abo__p d">[Стоимость] ₽</span><span class="abo__n">В стоимость входит: [утверждённый состав услуги]. Срок действия: [точные условия].</span></span>'
            '<span class="abo__turn">Условия абонемента%s</span></span>'
            '<span class="abo__s abo__r"><span class="abo__g">Для группы %s</span>%s<span class="abo__turn">Назад%s</span></span></span></button>') % (
        t, ABO_PH[k], age, I_CAL, I_TIME, m, TURN, t, ''.join('<span class="abo__row"><b>%s</b><span>%s</span></span>' % x for x in ABO_BACK), TURN)
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
            '<dl class="ktrial__list reveal"><div><dt>Стоимость</dt><dd><span class="price"><s class="price__old"><span class="sr">Старая цена: </span>[____] ₽</s><b class="price__new"><span class="sr">Цена: </span>[____] ₽</b></span></dd></div>'
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
body += sec(sechead('Документы и материалы для родителей', 'Всё, что понадобится до&nbsp;первого занятия: документы можно открыть и&nbsp;распечатать заранее.') + '<div class="kdoc">'
    '<div class="kdoc__list">' + ''.join(
        '<article class="kdoc__c reveal"><span class="kdoc__ic">%s</span><div class="kdoc__b"><b class="kdoc__t d">%s</b><p>%s</p>'
        '<p class="kdoc__meta"><span>%s</span><span>Редакция от&nbsp;[дата]</span></p></div>'
        '<a class="btn btn--sec kdoc__go" href="dokumenty.html#%s">Открыть%s</a></article>' % (ic, t, d, who, k, ARROW) for k, ic, t, d, who in KDOCS) + '</div>'
    '<aside class="kdoc__side reveal"><p class="kdoc__st d">Перед первым занятием</p><ol class="kdoc__steps">' + ''.join(
        '<li><b>%s</b><span>%s</span></li>' % x for x in KSTEPS) + '</ol>'
    '<p class="kdoc__more">Другие документы: <a href="dokumenty.html#pravila">Правила посещения</a>, <a href="dokumenty.html#oferta">Договор оферты</a></p>'
    + join_btn('Задать вопрос по&nbsp;документам', 'Вопрос по документам', 'kids', 'btn btn--light') + '</aside></div>', 'docs')
# 9. Тренеры
body += sec(sechead('Тренеры детской секции', '', link_btn('Все тренеры', 'trenery.html', 'btn btn--sec reveal')) + '\n' + coaches([('[Имя Фамилия]', 'Детский тренер', '[Квалификация · стаж]')] * 4), 'coaches', cls='lp-alt')
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
    '<a class="short" href="video.html"><img src="assets/img/%s" alt="" loading="lazy"><span class="scrim"></span>%s<span class="short__c"><b>[Видеоотзыв]</b><small>[0:45]</small></span></a>' % (f, PLAY)
    for f in ['k2-10.jpg', 'k2-02.jpg', 'p-fun.jpg', 'p-smile.jpg', 'k2-13.jpg', 'k2-12.jpg']) + '</div><div class="wrap"><div class="widget reveal kreviews"><b>[Виджет отзывов]</b><span>Подтягивается с внешнего сервиса — [Яндекс Карты / 2ГИС]</span></div></div></section>'
# 13. Форма связи
body += CONTACT
# 14. Вопросы (ответы — из ТЗ; чего нет в ТЗ — в скобках)
body += faq_sec([('С какого возраста можно?', 'С 5 лет. В секции три группы: 5–7, 8–10 и 11–16 лет.'),
                 ('Сколько длится занятие?', 'Для детей 5–7 лет — 60 минут, для школьников и подростков — 90 минут.'),
                 ('Можно ли сначала попробовать?', 'Да. Пробная тренировка проходит в общей группе соответствующего возраста: ребёнок знакомится с тренером и форматом занятий.'),
                 ('Что входит в пробную тренировку?', 'Всё снаряжение и работа тренера.'),
                 ('Как оплачиваются занятия?', 'Регулярные занятия проходят по абонементам на месяц. [Условия уточняются.]'),
                 ('Что, если ребёнок пропустит занятие?', '[Правила пропусков и переносов уточняются.]'),
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
body += sec(sechead('Как проходит') + '\n' + steps([('Знакомство', 'Тренер знакомится с ребёнком и подбирает ему снаряжение.'), ('Инструктаж и разминка', 'Простые правила безопасности и разминка в игровой форме.'),
                                                   ('Первые трассы', 'Сначала боулдеринг над матами, потом — высокая стена со страховкой.'), ('Итог', 'Тренер расскажет родителям, как ребёнку заниматься дальше.')]), 'how', 'dark', 'stack')
body += sec(sechead('Выберите формат') + '\n' + offers([
    offer('Детская пробная в группе', ['для детей от 5 лет', 'группа до 8 человек', 'работа тренера', 'необходимое снаряжение'], 'Весело, в компании ровесников.', PRICE + book_btn('Записаться', 'group', 0, 1), 'Группа до 8 человек'),
    offer('Персональная детская пробная', ['для 1–3 детей', 'индивидуальный темп', 'работа тренера', 'необходимое снаряжение'], 'Больше внимания тренера — удобно для братьев и сестёр.', PRICE + book_btn('Записаться', 'personal', 0, 1), '1–3 участника', dark=True)]), 'formats', cls='stack')
body += sec('<div class="lp-next lp-next--red reveal" id="family"><div><span class="mark">Для всей семьи</span><h2 class="d h2">Взрослый + ребёнок</h2><p class="lead">Полазайте вместе: тренер покажет основы обоим, а вы будете поддерживать друг друга на стене. В форме записи отметьте, сколько придёт взрослых и детей.</p></div>' +
            book_btn('Записаться вместе', 'group', 1, 1, 'btn btn--light') + '</div>', tone='neutral', cls='sec--flush')
body += sec('<div class="lp-bring"><div class="lp-bring__main reveal"><h2 class="d h2">С собой — только удобная спортивная форма</h2><p class="lead muted">Скальные туфли, страховочную систему и магнезию выдадим на месте.</p>'
            '<p class="lp-bring__note">%s<span>Приходите за 10–15 минут до начала</span></p></div><div class="lp-bring__side reveal"><p class="lp-k">Для родителей</p>' % I_TIME +
            li(['раздевалка и шкафчики', 'душевые', 'аренда полотенец', 'можно посмотреть, как ребёнок лазает']) + '</div></div>', 'bring')
body += faq_sec(FAQ_KIDS)
body += nextcta('Понравилось?', 'Продолжайте в детской секции — регулярно и с детскими тренерами.', link_btn('Детская секция', 'detskaya-sekciya.html', 'btn btn--light'))
fab = book_btn('Записаться на тренировку', 'group', 0, 1)
page('deti-pervyj-raz.html', 'Детская пробная тренировка по скалолазанию — скалодром К2', 'Пробная тренировка для детей от 5 лет и формат «взрослый + ребёнок»: с тренером, снаряжение включено. Скалодром К2.', body, book=True, fab=fab)


# ======================= ЦЕНЫ =======================
GROUPS = [('probnye', 'Пробные тренировки', [('Пробная тренировка в группе', '60 минут, группа до 8 человек, снаряжение включено', '[___] ₽', 'pervyj-raz.html#formats'),
                                             ('Персональная пробная тренировка', '60 минут, для 1–3 участников', '[___] ₽', 'pervyj-raz.html#formats'),
                                             ('Детская пробная тренировка', 'Для детей от 5 лет', '[___] ₽', 'deti-pervyj-raz.html')]),
          ('razovye', 'Разовые посещения', [('Разовое посещение', 'Самостоятельно, боулдеринг и трудность', '[___] ₽', 'samostoyatelno.html'), ('Разовое посещение [выходные]', '[Условия уточняются]', '[___] ₽')]),
          ('abonementy', 'Абонементы', [('Абонемент [на месяц]', 'Самостоятельные посещения', '[___] ₽', 'samostoyatelno.html#prices'), ('Абонемент [на __ посещений]', 'Самостоятельные посещения', '[___] ₽', 'samostoyatelno.html#prices'),
                                         ('Абонемент в школу', '[__] групповых тренировок', '[___] ₽', 'shkola.html')]),
          ('trener', 'Тренировки с тренером', [('Индивидуальная тренировка', 'С тренером', '[___] ₽', 'individualnye.html'), ('Базовый курс', '3–5 тренировок', 'от [___] ₽', 'bazovye-kursy.html')]),
          ('deti', 'Для детей', [('Детская секция', 'Абонемент на [__] занятий', '[___] ₽', 'detskaya-sekciya.html'), ('Взрослый + ребёнок', 'Пробная тренировка', '[___] ₽', 'deti-pervyj-raz.html#family')]),
          ('prokat', 'Прокат и услуги', [('Прокат снаряжения', 'Скальники, страховочная система', '[___] ₽'), ('Аренда полотенца', '', '[___] ₽'),
                                         ('Подарочный сертификат', 'На пробную тренировку', '[___] ₽', 'sertifikaty.html')])]
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
body += nextcta('Не знаете, какой пакет выбрать?', 'Оставьте заявку — поможем выбрать пакет под ваш уровень.', join_btn('Оставить заявку', 'Поможем выбрать пакет', 'trial', 'btn btn--light'))
page('pakety.html', 'Пакеты тренировок по скалолазанию — скалодром К2', 'Пакеты для новичков и продолжающих: Старт, База, Расширенный, Нижняя страховка, Уровень, Сила, Выносливость, Скалы, Техника.', body)


# ======================= СЕРТИФИКАТЫ =======================
body = hero([('Сертификаты', '')], 'Подарочные сертификаты на скалодром',
            'Подарите впечатление, а не вещь: пробная тренировка с инструктором. Опыт не нужен, снаряжение выдадим.',
            'k2-12.jpg', [(I_GIFT, 'Красивый подарок'), (I_SPARK, 'Опыт не нужен'), (I_GEAR, 'Снаряжение включено'), (I_CAL, 'Срок действия [__]')],
            join_btn('Заказать сертификат', 'Подарочный сертификат'), 'Вместе на скалодроме')
body += sec(sechead('Выберите сертификат') + '\n' + offers([
    offer('Пробная тренировка в группе', ['60 минут', 'группа до 8 человек', 'с инструктором', 'снаряжение включено'], 'Для того, кто хочет попробовать в компании таких же новичков.', PRICE + join_btn('Заказать', 'Сертификат: пробная в группе')),
    offer('Персональная пробная тренировка', ['60 минут', 'для 1–3 участников', 'индивидуальный темп', 'снаряжение включено'], 'Подарок на двоих или на троих — для пары или друзей.', PRICE + join_btn('Заказать', 'Сертификат: персональная пробная'), dark=True)]), 'formats')
body += sec(sechead('Как подарить') + '\n' + cards([('Оставьте заявку', 'Выберите сертификат — администратор свяжется и всё оформит.'), ('Оплатите', '[Способы оплаты и получения сертификата уточняются.]'),
                                                  ('Получатель записывается', 'В удобный ему день — по телефону или на сайте.')], 3), 'how', 'dark', 'stack')
body += faq_sec([('Сколько действует сертификат?', '[Срок действия уточняется.]'), ('Можно ли подарить ребёнку?', 'Да, есть детские пробные тренировки — для детей от 5 лет.'),
                 ('Нужен ли опыт?', 'Нет. Пробная тренировка рассчитана на любой уровень.'), ('Можно ли поменять дату?', '[Условия переноса уточняются.]')])
page('sertifikaty.html', 'Подарочные сертификаты на скалодром — К2', 'Подарочный сертификат на пробную тренировку по скалолазанию с инструктором: в группе или персонально. Скалодром К2.', body)


# ======================= МЕРОПРИЯТИЯ =======================
EVENTS = [('adults', 'Для взрослых', 'Соревнования по боулдерингу', 'k2-first-1.jpg'), ('adults', 'Для взрослых', 'Выезд на скалы', 'k2-rock.jpg'),
          ('kids', 'Для детей', 'Детские соревнования', 'k2-first-2.jpg'), ('kids', 'Для детей', '[Мероприятие для детей]', 'p-mat.jpg'),
          ('adults', 'Для взрослых', '[Мероприятие]', 'k2-hall.jpg')]
body = head([('О нас', 'o-skalodrome.html'), ('Мероприятия', '')], 'Мероприятия скалодрома', 'Соревнования, выезды на скалы и события для детей и взрослых — следите за расписанием.',
            '<div class="chips chips--dark" role="group" aria-label="Для кого"><button type="button" class="chip" aria-pressed="true" data-f="all">Все</button>'
            '<button type="button" class="chip" aria-pressed="false" data-f="adults">Для взрослых</button><button type="button" class="chip" aria-pressed="false" data-f="kids">Для детей</button></div>')
body += sec('<div class="bgrid">%s</div><p class="bempty" hidden>Скоро здесь появятся мероприятия</p>' % ''.join(
    '<article class="bcard ev reveal" data-cat="%s"><span class="bcard__img"><img src="assets/img/%s" alt="" loading="lazy"></span><span class="bcard__b"><span class="badge">%s</span>'
    '<span class="bcard__t">%s</span><span class="bcard__m">[дата] · [время]</span>%s</span></article>' % (c, img, cn, t, join_btn('Записаться', t, 'kids' if c == 'kids' else '', 'btn btn--sec btn--sm'))
    for c, cn, t, img in EVENTS) + '\n<!-- В MODX: мероприятия — ресурсы (дата, для кого, обложка, описание), список — pdoResources -->', 'list', cls='blog-list')
body += nextcta('Хотите первыми узнавать о мероприятиях?', 'Оставьте телефон — сообщим о ближайших соревнованиях и выездах.', join_btn('Оставить заявку', 'Мероприятия скалодрома', '', 'btn btn--light'))
page('meropriyatiya.html', 'Мероприятия — скалодром К2', 'Соревнования, выезды на скалы и мероприятия для детей и взрослых на скалодроме К2.', body)


# ======================= О СКАЛОДРОМЕ =======================
body = hero([('О скалодроме', '')], 'Новый скалодром в центре Петербурга',
            'Боулдеринг и трудность под одной крышей: 1300 м², стены 13 метров, 7 минут пешком от м. Площадь Ленина.',
            'p-blue.jpg', [(I_UP, '13 метров высоты'), (I_SPARK, '1300 м²'), (I_CAL, '7 дней в неделю'), (I_PIN, '7 минут от метро')],
            link_btn('Первый раз', 'pervyj-raz.html', 'btn btn--primary') + link_btn('Как добраться', 'kontakty.html#route', 'btn btn--sec'), 'Зал скалодрома К2')
body += sec(sechead('Две зоны для лазания') + '\n' + offers([
    offer('Боулдеринг', ['невысокие трассы', 'без верёвки, над мягкими матами', '[__] трасс', 'подходит новичкам'], 'Короткие трассы без верёвки над мягкими матами. Идеально для первого знакомства и отработки техники.', link_btn('Первый раз', 'pervyj-raz.html', 'btn btn--primary'), 'Зона боулдеринга', id='bouldering', img='k2-first-1.jpg'),
    offer('Трудность', ['стены 13 метров', 'со страховкой верёвкой', '[__] трасс', 'есть автостраховка'], 'Длинные трассы на стенах до 13 метров со страховкой. Здесь занимаются с тренером и самостоятельно.', link_btn('Базовые курсы', 'bazovye-kursy.html', 'btn btn--primary'), 'Зона трудности', dark=True, id='trudnost', img='k2-hall.jpg')]), 'zones')
body += '''<section class="lp-why dark" id="why">
  <div class="lp-why__photo"><img src="assets/img/k2-first-2.jpg" alt="Скалолаз на нависании" loading="lazy"></div>
  <div class="wrap lp-why__in">
    <h2 class="d h2 lp-why__t reveal">Почему лазать в К2</h2>
    <div class="lp-why__cards">
      <div class="lp-w reveal"><b class="d">13 метров высоты</b><p>Просторная зона трудности для занятий со страховкой.</p></div>
      <div class="lp-w reveal"><b class="d">1300 м²</b><p>Боулдеринг и трудность под одной крышей.</p></div>
      <div class="lp-w lp-w--accent reveal"><b class="d">Новый скалодром</b><p>Новые стены, зацепы и снаряжение.</p></div>
      <div class="lp-w reveal"><b class="d">PRO команда</b><p>Тренеры для взрослых и детей.</p></div>
      <div class="lp-w reveal"><b class="d">Прокат снаряжения</b><p>Всё необходимое — на месте.</p></div>
    </div>
  </div>
</section>'''
# Удобства: «маршрут вечера» шагами + плитки с иконками
I_HANGER = ico('<path d="M10 6a2 2 0 1 1 2 2v2"/><path d="M12 10l-8.5 6.5a1 1 0 0 0 .6 1.5h15.8a1 1 0 0 0 .6-1.5z"/>')
I_SHOWER = ico('<path d="M5 21V9a5 5 0 0 1 9-3"/><path d="M11 9h7l-1.5 2.5h-4z"/><path d="M12.5 14.5l-.6 1.6M15 14.5v1.7M17.5 14.5l.6 1.6M13 19l-.4 1.2M16.6 19l.4 1.2"/>')
I_LOCK = ico('<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M12 3v18M9.5 10v3M14.5 10v3"/>')
I_TOWEL = ico('<path d="M3 5h18"/><path d="M7 5v13a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V5"/><path d="M7 14h10M7 16.5h10"/>')
I_SHOE = ico('<path d="M3 17v-4.5c2-.5 3.5-2 4.5-4l1-2 3 2.5c1.5 1.3 3 2 5 2.3 2.4.4 4.5 1.4 4.5 3.7v2z"/><path d="M3 20h18M9.5 9.5l1.5 1.2M11.5 8l1.5 1.2"/>')
I_PARK = ico('<rect x="4" y="4" width="16" height="16" rx="4"/><path d="M10 17V7h3a3 3 0 0 1 0 6h-3"/>')
AM_FLOW = [(I_PIN, 'После работы'), (I_HANGER, 'Переоделись'), (I_UP, 'Тренировка'), (I_SHOWER, 'Душ')]
AM_TILES = [(I_HANGER, 'Раздевалки', ''), (I_SHOWER, 'Душевые', ''), (I_LOCK, 'Шкафчики', ''),
            (I_TOWEL, 'Аренда полотенец', ''), (I_SHOE, 'Прокат снаряжения', ''), (I_PARK, 'Парковка', '[уточнить]')]
body += sec('<div class="am"><div class="am__main reveal"><h2 class="d h2">Всё для&nbsp;комфортных тренировок</h2>'
            '<p class="lead muted">Можно прийти сразу после работы: переодеться, потренироваться и&nbsp;принять душ.</p>'
            '<ol class="am__flow" aria-label="Как проходит визит">' + ''.join('<li><span class="am__fi">%s</span><span>%s</span></li>' % x for x in AM_FLOW) + '</ol>'
            '<p class="lp-bring__note">%s<span>[Ежедневно, __:__–__:__]</span></p></div>' % I_TIME +
            '<div class="am__side"><p class="lp-k reveal">В&nbsp;К2 есть</p><ul class="am__tiles">' + ''.join(
                '<li class="reveal"><span class="am__ti">%s</span><b>%s</b>%s</li>' % (ic, t, '<small>%s</small>' % n if n else '') for ic, t, n in AM_TILES) + '</ul></div></div>', 'amenities')
body += sec(sechead('Атмосфера К2', 'Нажмите на фото — откроется галерея') + '\n' + gal(GAL_HALL), 'photos', cls='lp-alt')
body += sec(sechead('Команда', '', link_btn('Все тренеры', 'trenery.html', 'btn btn--sec reveal')) + '\n' + coaches(COACH_STUB), 'coaches')
body += REVIEWS('Отзывы о К2') + CONTACT
page('o-skalodrome.html', 'О скалодроме К2 — боулдеринг и трудность в центре Петербурга', 'Новый скалодром: 1300 м², стены 13 метров, зоны боулдеринга и трудности, раздевалки и душевые. 7 минут от м. Площадь Ленина.', body, gallery=True)


# ======================= ТРЕНЕРЫ =======================
body = head([('О нас', 'o-skalodrome.html'), ('Тренеры', '')], 'Тренеры скалодрома К2', 'Хороший тренер не только сильно лазает, но и спокойно, понятно объясняет. Наши работают и со взрослыми, и с детьми.')
body += sec(sechead('Тренеры для взрослых') + '\n' + coaches(COACH_STUB[:3] + [('[Имя Фамилия]', 'Тренер', '[Квалификация · стаж]')]) + '\n<!-- В MODX: тренеры — ресурсы или MIGX (фото, имя, должность, квалификация) -->', 'adults')
body += sec(sechead('Детские тренеры') + '\n' + coaches([('[Имя Фамилия]', 'Детский тренер', '[Квалификация · стаж]')] * 4), 'kids', cls='lp-alt')
body += nextcta('Хотите заниматься с тренером?', 'Оставьте заявку — подберём тренера под ваш уровень и цель.', join_btn('Оставить заявку', 'Занятия с тренером', 'trial', 'btn btn--light'))
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
body = head([('О нас', 'o-skalodrome.html'), ('Вакансии', '')], 'Вакансии', 'Ищем людей, которые любят скалолазание и умеют работать с людьми.')
body += sec(offers([offer('[Вакансия]', ['[Условия]', '[График]', '[Требования]'], '[Описание вакансии.]', join_btn('Откликнуться', 'Отклик на вакансию', '', 'btn btn--primary')) for _ in range(3)], 3) +
            '\n' + helpbox('Не нашли подходящую вакансию?', 'Напишите нам — расскажите о себе и опыте.', '<a class="btn btn--sec" href="mailto:[почта]">Написать на почту</a>') +
            '\n<!-- В MODX: вакансии — ресурсы или MIGX -->', 'list')
page('vakansii.html', 'Вакансии — скалодром К2', 'Работа на скалодроме К2: тренеры, администраторы и другие вакансии.', body)


# ======================= ДОКУМЕНТЫ =======================
DOCS = [('pravila', 'Правила посещения'), ('tb', 'Техника безопасности'), ('zayavlenie', 'Заявление от родителей'), ('oferta', 'Договор оферты'), ('privacy', 'Политика обработки персональных данных')]
body = head([('О нас', 'o-skalodrome.html'), ('Документы', '')], 'Документы', 'Правила посещения, техника безопасности, оферта и политика обработки персональных данных.')
body += '''<section class="neutral docs-sec"><div class="art__wrap wrap docs">
  <aside class="art__side"><p class="art__side-t">Документы</p><ol class="toc">%s</ol></aside>
  <div class="art__body">%s</div>
</div></section>''' % (''.join('<li><a href="#%s">%s</a></li>' % d for d in DOCS), ''.join(
    '<section class="doc" id="%s"><h2>%s</h2><p>%s</p><p class="doc__meta">Редакция от [дата]</p></section>' % (i, t, DOC_STUB) for i, t in DOCS))
page('dokumenty.html', 'Документы — скалодром К2', 'Правила посещения, техника безопасности, договор оферты и политика обработки персональных данных скалодрома К2.', body)


# ======================= КОНТАКТЫ =======================
body = head([('Контакты', '')], 'Контакты и как добраться', 'Скалодром К2 — 7 минут пешком от м. Площадь Ленина.')
body += CONTACT.replace('sec--flush', '')
body += sec(sechead('Как добраться') + '''
<div class="lp-bring">
  <div class="lp-bring__main reveal">
    <p class="lead">[Адрес], 7 минут пешком от м. Площадь Ленина.</p>
    <ol class="route-steps"><li>[Выход из метро — уточняется]</li><li>[Путь до скалодрома — уточняется]</li><li>[Вход в здание — уточняется]</li></ol>
    <p class="lp-bring__note">%s<span>[Ежедневно, __:__–__:__]</span></p>
  </div>
  <div class="lp-bring__side lp-map reveal"><b>[Яндекс Карта]</b><span>Карта со скалодромом — встраивается кодом конструктора карт</span></div>
</div>''' % I_TIME, 'route')
body += sec(sechead('Реквизиты') + '\n<p class="lead muted reveal">[Реквизиты]</p>', 'requisites', cls='lp-alt')
page('kontakty.html', 'Контакты и как добраться — скалодром К2', 'Телефон, мессенджеры, адрес и схема проезда: скалодром К2 в 7 минутах от м. Площадь Ленина.', body)


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
<footer>Цены действительны с [дата]. Актуальные цены — на сайте и у администратора.</footer></body></html>''' % {'F': fonts, 'LOGO': LOGO, 'ROWS': rows}
out = os.path.join(ROOT, 'assets', 'docs'); os.makedirs(out, exist_ok=True)
if os.path.exists(CHROME):
    with tempfile.TemporaryDirectory() as tmp:
        src = os.path.join(tmp, 'price.html'); io.open(src, 'w', encoding='utf-8').write(typograph(sheet))
        subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--no-pdf-header-footer', '--user-data-dir=' + os.path.join(tmp, 'p'),
                        '--print-to-pdf=' + os.path.join(out, 'k2-ceny.pdf'), pathlib.Path(src).as_uri()], check=True, capture_output=True, timeout=60)
    print('прайс: assets/docs/k2-ceny.pdf')
else:
    print('Chrome не найден — PDF прайса не пересобран')
