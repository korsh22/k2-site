# -*- coding: utf-8 -*-
"""28.10.2026: фото по ориентации рамок — вертикальные только в вертикальных рамках, горизонтальные — в горизонтальных.
Правит главную (site/index.html) и генераторы. Запускался один раз; оставлен для истории."""
import io, os, re
T = os.path.dirname(__file__)
ROOT = os.path.join(T, '..', 'site')

def patch(path, pairs, regex=()):
    s = io.open(path, encoding='utf-8').read()
    for a, b in pairs:
        assert s.count(a) == 1, (path, a[:70]); s = s.replace(a, b)
    for a, b in regex:
        s, n = re.subn(a, b, s, count=1); assert n == 1, (path, a[:70])
    io.open(path, 'w', encoding='utf-8').write(s)

# --- Главная ---
PACK = {'start': 'k2-first-1.jpg', 'baza': 'p-mat.jpg', 'rasshirennyj': 'k2-hall.jpg', 'nizhnyaya-strahovka': 'k2-first-2.jpg',
        'uroven': 'k2-first-3.jpg', 'sila': 'p-chalk.jpg', 'vynoslivost': 'k2-hall.jpg', 'skaly': 'k2-rock.jpg', 'tehnika': 'p-cave.jpg'}
patch(os.path.join(ROOT, 'index.html'), [
    # фон первого экрана (под видео) — широкий кадр зала
    ('<img src="assets/img/k2-01.jpg" alt="Скалолаз на стене скалодрома" fetchpriority="high">', '<img src="assets/img/k2-hall.jpg" alt="Зал скалодрома К2" fetchpriority="high">'),
    # «Для детей» — широкая карточка
    ('<div class="card g6 reveal" id="kids">\n        <img src="assets/img/k2-02.jpg"', '<div class="card g6 reveal" id="kids">\n        <img src="assets/img/k2-first-2.jpg"'),
    # «Взрослый + ребёнок»: на телефоне рамка вертикальная — своё вертикальное фото
    ('<img class="choice__img" src="assets/img/k2-first-3.jpg" style="object-position:66% 55%" alt="" loading="lazy">',
     '<picture><source media="(max-width: 767px)" srcset="assets/img/p-fun.jpg"><img class="choice__img" src="assets/img/k2-first-3.jpg" style="object-position:66% 55%" alt="" loading="lazy"></picture>'),
], [(r'(<a class="pack" href="pakety\.html#%s"><span class="pack__img"><img src="assets/img/)[^"]+' % k, r'\g<1>' + v) for k, v in PACK.items()])

# --- Внутренние страницы ---
GAL_NEW = """GAL_HALL = [('p-blue.jpg', 'Синяя стена с нависанием'), ('p-mat.jpg', 'Отдых на матах'), ('p-cave.jpg', 'Под нависанием'),
            ('k2-first-1.jpg', 'Боулдеринг в зале'), ('p-roof.jpg', 'Лазание по потолку'), ('k2-first-2.jpg', 'Трасса на нависании'),
            ('k2-hall.jpg', 'Зал скалодрома К2'), ('p-dyno.jpg', 'Прыжок к зацепу'), ('k2-first-3.jpg', 'Вместе на скалодроме')]"""
p = os.path.join(T, 'build_site.py'); s = io.open(p, encoding='utf-8').read()
a = s.index('GAL_HALL = ['); b = s.index(")]", a) + 2
s = s[:a] + GAL_NEW + s[b:]
io.open(p, 'w', encoding='utf-8').write(s)
patch(p, [
    # плитки «Для детей» (4:3)
    ("('Пробная тренировка', 'Попробовать и понять, нравится ли', 'deti-pervyj-raz.html', 'k2-10.jpg', True)", "('Пробная тренировка', 'Попробовать и понять, нравится ли', 'deti-pervyj-raz.html', 'p-mat.jpg', True)"),
    ("'meropriyatiya.html#kids', 'k2-12.jpg', False)", "'meropriyatiya.html#kids', 'p-cave.jpg', False)"),
    # мероприятия (16:10)
    ("EVENTS = [('adults', 'Для взрослых', 'Соревнования по боулдерингу', 'k2-10.jpg'), ('adults', 'Для взрослых', 'Выезд на скалы', 'k2-07.jpg'),\n          ('kids', 'Для детей', 'Детские соревнования', 'k2-02.jpg'), ('kids', 'Для детей', '[Мероприятие для детей]', 'k2-first-2.jpg'),\n          ('adults', 'Для взрослых', '[Мероприятие]', 'k2-12.jpg')]",
     "EVENTS = [('adults', 'Для взрослых', 'Соревнования по боулдерингу', 'k2-first-1.jpg'), ('adults', 'Для взрослых', 'Выезд на скалы', 'k2-rock.jpg'),\n          ('kids', 'Для детей', 'Детские соревнования', 'k2-first-2.jpg'), ('kids', 'Для детей', '[Мероприятие для детей]', 'p-mat.jpg'),\n          ('adults', 'Для взрослых', '[Мероприятие]', 'k2-hall.jpg')]"),
    # «О скалодроме»: зоны (16:9) и широкое фото «Почему лазать в К2»
    ("'Зона боулдеринга', id='bouldering', img='k2-10.jpg')", "'Зона боулдеринга', id='bouldering', img='k2-first-1.jpg')"),
    ("'Зона трудности', dark=True, id='trudnost', img='k2-11.jpg')", "'Зона трудности', dark=True, id='trudnost', img='k2-hall.jpg')"),
    ('<div class="lp-why__photo"><img src="assets/img/k2-01.jpg" alt="Скалолаз под нависанием" loading="lazy"></div>', '<div class="lp-why__photo"><img src="assets/img/k2-first-2.jpg" alt="Скалолаз на нависании" loading="lazy"></div>'),
    # видео: на компьютере рамка 16:9 — горизонтальные обложки, на телефоне 4:5 — вертикальные
    ("VIDEOS = [('obzor', 'Обзор скалодрома', 'k2-01.jpg'), ('sovety', 'Советы новичку', 'k2-13.jpg'), ('deti', 'Детская секция', 'k2-10.jpg'),\n          ('razminka', 'Разминка и заминка', 'k2-07.jpg'), ('fan', '[Фан со скалодрома]', 'k2-06.jpg'), ('more', '[Видео]', 'k2-12.jpg')]",
     "VIDEOS = [('obzor', 'Обзор скалодрома', 'k2-hall.jpg', 'p-blue.jpg'), ('sovety', 'Советы новичку', 'p-chalk.jpg', 'p-focus.jpg'), ('deti', 'Детская секция', 'k2-first-2.jpg', 'k2-10.jpg'),\n          ('razminka', 'Разминка и заминка', 'p-mat.jpg', 'p-fun.jpg'), ('fan', '[Фан со скалодрома]', 'p-cave.jpg', 'p-heart.jpg'), ('more', '[Видео]', 'k2-first-1.jpg', 'p-roof.jpg')]"),
    ("""'<div class="lp-video reveal" id="%s" data-video=""><img src="assets/img/%s" alt="" loading="lazy"><span class="lp-video__shade"></span>'""",
     """'<div class="lp-video reveal" id="%s" data-video=""><picture><source media="(max-width: 767px)" srcset="assets/img/%s"><img src="assets/img/%s" alt="" loading="lazy"></picture><span class="lp-video__shade"></span>'"""),
    ("""'<span class="lp-video__soon">Видео скоро</span><span class="lp-video__meta"><b>%s</b><small>[0:45]</small></span></div>' % (s, img, t, t) for s, t, img in VIDEOS)""",
     """'<span class="lp-video__soon">Видео скоро</span><span class="lp-video__meta"><b>%s</b><small>[0:45]</small></span></div>' % (s, vimg, img, t, t) for s, t, img, vimg in VIDEOS)"""),
])
# --- «Первый раз»: на телефоне фон «Почему К2» вертикальный — своё вертикальное фото ---
patch(os.path.join(T, 'build_pages.py'), [
    ('<div class="lp-why2__bg" aria-hidden="true"><img src="assets/img/k2-rock.jpg" alt="" loading="lazy"></div>',
     '<div class="lp-why2__bg" aria-hidden="true"><picture><source media="(max-width: 767px)" srcset="assets/img/p-dyno.jpg"><img src="assets/img/k2-rock.jpg" alt="" loading="lazy"></picture></div>'),
])
print('готово')
