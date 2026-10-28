# -*- coding: utf-8 -*-
"""Собирает страницы блога К2: site/blog/index.html и страницу на каждую статью.
Шапка, меню, поиск и подвал берутся из site/index.html, ссылки переписываются на ../
Запуск:  python tools/build_blog.py
"""
import io, os, re, html, sys
sys.path.insert(0, os.path.dirname(__file__))
from blog_content import ARTICLES, CATEGORIES
from typograph import process as typograph

ROOT = os.path.join(os.path.dirname(__file__), '..', 'site')
OUT = os.path.join(ROOT, 'blog')
os.makedirs(OUT, exist_ok=True)
CATNAME = dict(CATEGORIES)
esc = html.escape

from chrome import MAIN as main, VER, parts
P = parts(1)
HEADER, MMENU, SEARCH, OCC, FOOTER, JOIN = P['HEADER'], P['MMENU'], P['SEARCH'], P['OCC'], P['FOOTER'], P['JOIN']
ARROW = '<svg class="ico" viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'

def words(a):
    t = ' '.join(x[1] if isinstance(x[1], str) else ' '.join(x[1]) for x in a['body'] if x[0] != 'img')
    return len(t.split()) + len(a['lead'].split())

def minutes(a):
    return max(2, round(words(a) / 160))

def page(title, desc, body, extra_class=''):
    return '''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<link rel="stylesheet" href="../css/style.css?v=%s">
<link rel="stylesheet" href="../css/blog.css?v=%s">
</head>
<body class="page %s">
<div class="readbar" aria-hidden="true"><span></span></div>
%s

%s
%s
%s

%s

%s
%s
<script src="../js/search.js?v=%s"></script>
<script src="../js/blog.js?v=%s"></script>
<script src="../js/landing.js?v=%s"></script>
</body>
</html>
''' % (esc(title), esc(desc), VER, VER, extra_class, HEADER, MMENU, SEARCH, body, FOOTER, OCC, JOIN, VER, VER, VER)

def card(a, big=False):
    return ('<a class="bcard%s reveal" href="%s.html" data-cat="%s">'
            '<span class="bcard__img"><img src="../assets/img/%s" alt="" loading="lazy"></span>'
            '<span class="bcard__b"><span class="badge">%s</span><span class="bcard__t">%s</span>'
            '<span class="bcard__l">%s</span><span class="bcard__m">%s · %d мин чтения</span></span></a>') % (
        ' bcard--big' if big else '', a['slug'], a['cat'], a['cover'], CATNAME[a['cat']], esc(a['title']),
        esc(a['lead']) if big else '', a['date'], minutes(a))

def render_body(a):
    out, toc = [], []
    for i, b in enumerate(a['body']):
        k = b[0]
        if k == 'h2':
            hid = 's%d' % (len(toc) + 1)
            toc.append((hid, b[1]))
            out.append('<h2 id="%s">%s</h2>' % (hid, esc(b[1])))
        elif k == 'p':
            out.append('<p>%s</p>' % esc(b[1]))
        elif k == 'ul':
            out.append('<ul>' + ''.join('<li>%s</li>' % esc(x) for x in b[1]) + '</ul>')
        elif k == 'tip':
            out.append('<aside class="art__tip"><b>%s</b><p>%s</p></aside>' % (esc(b[1]), esc(b[2])))
        elif k == 'quote':
            out.append('<blockquote class="art__quote"><p>%s</p></blockquote>' % esc(b[1]))
        elif k == 'img':
            out.append('<figure class="art__fig"><img src="../assets/img/%s" alt="%s" loading="lazy"><figcaption>%s</figcaption></figure>' % (b[1], esc(b[2]), esc(b[2])))
    return '\n        '.join(out), toc

# ---------- Страницы статей ----------
for idx, a in enumerate(ARTICLES):
    content, toc = render_body(a)
    others = [x for x in ARTICLES if x['slug'] != a['slug']][:3]
    toc_html = ''.join('<li><a href="#%s">%s</a></li>' % (h, esc(t)) for h, t in toc)
    body = '''<main>
<article class="art">
  <header class="art__head dark">
    <div class="wrap">
      <nav class="crumbs" aria-label="Хлебные крошки"><a href="../index.html">Главная</a><span>/</span><a href="index.html">Блог</a><span>/</span><a href="index.html#%s">%s</a></nav>
      <span class="badge badge--dark">%s</span>
      <h1 class="d art__t">%s</h1>
      <p class="art__lead">%s</p>
      <p class="art__meta">%s · %d мин чтения</p>
    </div>
  </header>
  <div class="art__cover wrap"><img src="../assets/img/%s" alt=""></div>
  <div class="art__wrap wrap">
    <aside class="art__side">
      <p class="art__side-t">Содержание</p>
      <ol class="toc">%s</ol>
      <button class="copy-link" type="button"><svg class="ico" viewBox="0 0 24 24"><path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1"/><path d="M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/></svg><span>Скопировать ссылку</span></button>
    </aside>
    <div class="art__body">
        %s
      <div class="art__cta">
        <div><b>Попробуйте сами</b><p>Пробная тренировка с инструктором — для любого уровня подготовки, всё снаряжение выдаём.</p></div>
        <a class="btn btn--primary" href="../pervyj-raz.html">Записаться на тренировку</a>
      </div>
      <a class="art__back" href="index.html"><svg class="ico" viewBox="0 0 24 24"><path d="M19 12H5M11 6l-6 6 6 6"/></svg>Все статьи</a>
    </div>
  </div>
</article>
<section class="sec neutral related">
  <div class="wrap">
    <div class="sechead"><h2 class="d h2">Читайте также</h2><a class="btn btn--sec" href="index.html">Все статьи</a></div>
    <div class="bgrid bgrid--3">%s</div>
  </div>
</section>
</main>''' % (a['cat'], CATNAME[a['cat']], CATNAME[a['cat']], esc(a['title']), esc(a['lead']), a['date'], minutes(a),
              a['cover'], toc_html, content, ''.join(card(x) for x in others))
    doc = page(a['title'] + ' — блог скалодрома К2', a['lead'], body, 'page--art')
    io.open(os.path.join(OUT, a['slug'] + '.html'), 'w', encoding='utf-8').write(typograph(doc))
    print('статья:', a['slug'])

# ---------- Список статей ----------
chips = '<button type="button" class="chip" aria-pressed="true" data-f="all">Все статьи</button>' + ''.join(
    '<button type="button" class="chip" aria-pressed="false" data-f="%s">%s</button>' % (k, v) for k, v in CATEGORIES)
body = '''<main>
<section class="blog-head dark">
  <div class="wrap">
    <nav class="crumbs" aria-label="Хлебные крошки"><a href="../index.html">Главная</a><span>/</span><span>Блог</span></nav>
    <h1 class="d h1 blog-head__t">Блог о&nbsp;скалолазании</h1>
    <p class="lead blog-head__l">Тренировки, снаряжение, путешествия и&nbsp;жизнь клуба</p>
    <div class="chips chips--dark" role="group" aria-label="Рубрики блога">%s</div>
  </div>
</section>
<section class="sec neutral blog-list">
  <div class="wrap">
    <div class="bgrid">%s</div>
    <p class="bempty" hidden>В этой рубрике пока нет статей</p>
  </div>
</section>
</main>''' % (chips, card(ARTICLES[0], big=True) + ''.join(card(x) for x in ARTICLES[1:]))
doc = page('Блог о скалолазании — скалодром К2', 'Статьи о тренировках, снаряжении, путешествиях и жизни скалодрома К2', body, 'page--list')
io.open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(typograph(doc))
print('список статей: blog/index.html')

# ---------- Главная: карточки блога ведут на статьи ----------
CAT_BY_SLUG = {a['cat']: a for a in ARTICLES}
a0 = main.index('<div class="posts">'); a1 = main.index('</div>', main.index('</a>\n    </div>', a0)) + len('</div>')
posts = '<div class="posts">\n      ' + '\n      '.join(
    ('<a class="post reveal" href="blog/%s.html" data-cat="%s"><span class="post__img"><img src="assets/img/%s" alt="" loading="lazy"></span>'
     '<span class="post__b"><span class="badges"><span class="badge">%s</span></span><span class="post__t">%s</span>'
     '<span class="post__m">%s · %d мин чтения</span></span></a>') % (a['slug'], a['cat'], a['cover'], CATNAME[a['cat']], esc(a['title']), a['date'], minutes(a))
    for a in ARTICLES) + '\n    </div>'
new_main = main[:a0] + typograph(posts) + main[a1:]
new_main = new_main.replace('<h2 class="d h2 js-split">Блог о&nbsp;скалолазании</h2><a class="btn btn--sec reveal" href="#">Все статьи</a>',
                            '<h2 class="d h2 js-split">Блог о&nbsp;скалолазании</h2><a class="btn btn--sec reveal" href="blog/index.html">Все статьи</a>')
io.open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(new_main)
print('главная: карточки блога обновлены')
