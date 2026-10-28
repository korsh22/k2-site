# -*- coding: utf-8 -*-
"""Разовая правка: все ссылки главной ведут на настоящие страницы (запускался один раз; оставлен для истории)."""
import io, re, os

p = os.path.join(os.path.dirname(__file__), '..', 'site', 'index.html')
s = io.open(p, encoding='utf-8').read()
n0 = s.count('href="#"')

def R(a, b, cnt=1):
    global s
    c = s.count(a)
    assert c == cnt, (c, a[:90])
    s = s.replace(a, b)

JOIN = 'type="button" aria-haspopup="dialog" aria-controls="join"'
# промобар
R('<a class="promo__in" href="#kids">', '<a class="promo__in" href="detskaya-sekciya.html">')
# меню
R('<div class="dd__menu"><a href="#goals">Начинающим</a><a href="#goals">Базовые курсы</a><a href="#goals">Школа скалолазания</a><a href="#goals">Индивидуальные тренировки</a><a href="#goals">Самостоятельные посещения</a></div>',
  '<div class="dd__menu"><a href="dlya-vzroslyh.html">Все направления</a><a href="pervyj-raz.html">Начинающим</a><a href="bazovye-kursy.html">Базовые курсы</a><a href="shkola.html">Школа скалолазания</a><a href="individualnye.html">Индивидуальные тренировки</a><a href="samostoyatelno.html">Самостоятельные посещения</a></div>')
R('<div class="dd__menu"><a href="#kids">Детская секция</a><a href="#kids">Пробная тренировка</a><a href="#kids">Мероприятия для&nbsp;детей</a></div>',
  '<div class="dd__menu"><a href="dlya-detej.html">Все направления</a><a href="detskaya-sekciya.html">Детская секция</a><a href="deti-pervyj-raz.html">Пробная тренировка</a><a href="meropriyatiya.html#kids">Мероприятия для&nbsp;детей</a></div>')
R('<div class="dd__menu"><a href="#about">О&nbsp;скалодроме</a><a href="#reviews">Отзывы</a><a href="#">Тренеры</a><a href="#">Документы</a><a href="#">Вакансии</a></div>',
  '<div class="dd__menu"><a href="o-skalodrome.html">О&nbsp;скалодроме</a><a href="trenery.html">Тренеры</a><a href="meropriyatiya.html">Мероприятия</a><a href="blog/index.html">Блог</a><a href="o-skalodrome.html#reviews">Отзывы</a><a href="dokumenty.html">Документы</a><a href="vakansii.html">Вакансии</a></div>')
R('      <a href="#prices">цены</a>\n', '      <a href="ceny.html">цены</a>\n')
R('      <a href="#contacts">контакты</a>\n', '      <a href="kontakty.html">контакты</a>\n')
R('<a class="meta loc" href="#contacts">', '<a class="meta loc" href="kontakty.html#route">')
R('<a class="btn btn--sec btn--sm hdr__cta" href="#signup">Записаться на&nbsp;тренировку</a>',
  '<button class="btn btn--sec btn--sm hdr__cta js-join" %s data-join-title="Запись на&nbsp;тренировку">Записаться на&nbsp;тренировку</button>' % JOIN)
# мобильное меню
R('''    <a href="#goals">Для&nbsp;взрослых</a>
    <a href="#kids">Для&nbsp;детей</a>
    <a href="#prices">Цены</a>
    <a href="#about">О&nbsp;нас</a>
    <a href="#contacts">Контакты</a>''', '''    <a href="dlya-vzroslyh.html">Для&nbsp;взрослых</a>
    <a href="dlya-detej.html">Для&nbsp;детей</a>
    <a href="ceny.html">Цены</a>
    <a href="o-skalodrome.html">О&nbsp;нас</a>
    <a href="blog/index.html">Блог</a>
    <a href="kontakty.html">Контакты</a>''')
R('<a class="btn btn--light" href="#contacts">Заказать обратный звонок</a>',
  '<button class="btn btn--light js-join" %s data-join-title="Обратный звонок">Заказать обратный звонок</button>' % JOIN)
R('· <a href="#contacts">Как добраться</a></small>', '· <a href="kontakty.html#route">Как добраться</a></small>')
# мессенджеры и почта — адреса аккаунтов заменить на настоящие
s = re.sub(r'(<a class="hold-btn hold-btn--\d hold-btn--tg") href="#"', r'\1 href="https://t.me/" target="_blank" rel="noopener"', s)
s = re.sub(r'(<a class="hold-btn hold-btn--\d hold-btn--max") href="#"', r'\1 href="https://max.ru/" target="_blank" rel="noopener"', s)
s = re.sub(r'(<a class="hold-btn hold-btn--\d hold-btn--wa") href="#"', r'\1 href="https://wa.me/78120000000" target="_blank" rel="noopener"', s)
s = re.sub(r'(<a class="hold-btn hold-btn--\d hold-btn--mail") href="#"', r'\1 href="mailto:[почта]"', s)
R('<a class="ccard__mid" href="#">[почта]</a>', '<a class="ccard__mid" href="mailto:[почта]">[почта]</a>')
R('<li><a href="#">[почта]</a></li>', '<li><a href="mailto:[почта]">[почта]</a></li>')
# первый раз
R('<a class="choice tilt reveal" href="#kids">', '<a class="choice tilt reveal" href="deti-pervyj-raz.html">')
R('<a class="choice tilt reveal" href="#signup">', '<a class="choice tilt reveal" href="deti-pervyj-raz.html#family">')
# цели
R('<a class="lnk" href="#goals"><span><b>В&nbsp;группах', '<a class="lnk" href="shkola.html"><span><b>В&nbsp;группах')
R('<a class="lnk" href="#goals"><span><b>Самостоятельно', '<a class="lnk" href="samostoyatelno.html"><span><b>Самостоятельно')
R('<a class="lnk" href="#kids"><span><b>Спортивная секция', '<a class="lnk" href="detskaya-sekciya.html"><span><b>Спортивная секция')
R('<a class="lnk" href="#kids"><span><b>Просто полазать', '<a class="lnk" href="deti-pervyj-raz.html"><span><b>Просто полазать')
R('<a class="card g3 reveal" href="#goals">', '<a class="card g3 reveal" href="individualnye.html">')
R('<a class="card card--raised g3 reveal" href="#prices">', '<a class="card card--raised g3 reveal" href="ceny.html#abonementy">')
R('<a class="btn btn--light" href="#prices">Выбрать сертификат</a>', '<a class="btn btn--light" href="sertifikaty.html">Выбрать сертификат</a>')
# цены и пакеты
R('<a class="btn btn--sec" href="#prices">Все цены</a>', '<a class="btn btn--sec" href="ceny.html">Все цены</a>')
R('<a class="btn btn--sec" href="#prices"><svg class="ico" viewBox="0 0 24 24"><path d="M12 4v11',
  '<a class="btn btn--sec" href="assets/docs/k2-ceny.pdf" download><svg class="ico" viewBox="0 0 24 24"><path d="M12 4v11')
PACKS = [('start', 'Старт'), ('baza', 'База'), ('rasshirennyj', 'Расширенный'), ('nizhnyaya-strahovka', '<span class="term" data-term="belay">Нижняя страховка</span>'),
         ('uroven', 'Уровень'), ('sila', 'Сила'), ('vynoslivost', 'Выносливость'), ('skaly', 'Скалы'), ('tehnika', 'Техника')]
for slug, t in PACKS:
    s, k = re.subn(r'<a class="pack" href="#prices">((?:(?!</a>).)*?<span class="pack__t">%s</span>)' % re.escape(t), r'<a class="pack" href="pakety.html#%s">\1' % slug, s, count=1)
    assert k == 1, t
R('<a class="btn btn--sec" href="#prices">Все пакеты и&nbsp;цены</a>', '<a class="btn btn--sec" href="pakety.html">Все пакеты и&nbsp;цены</a>')
# видео
R('<a class="btn btn--sec" href="#">Все видео</a>', '<a class="btn btn--sec" href="video.html">Все видео</a>')
for slug, t in [('obzor', 'Обзор скалодрома'), ('sovety', 'Советы новичку'), ('deti', 'Детская секция'), ('razminka', 'Разминка и&nbsp;заминка'),
                ('fan', '[Фан со&nbsp;скалодрома]'), ('more', '[Видео]')]:
    s, k = re.subn(r'<a class="short" href="#">((?:(?!</a>).)*?<b>%s</b>)' % re.escape(t), r'<a class="short" href="video.html#%s">\1' % slug, s, count=1)
    assert k == 1, t
# связь
R('<a class="btn btn--sec btn--sm" href="#"><svg class="ico" viewBox="0 0 24 24"><path d="M12 21s', '<a class="btn btn--sec btn--sm" href="kontakty.html#route"><svg class="ico" viewBox="0 0 24 24"><path d="M12 21s')
s = s.replace('<a href="#">обработку персональных данных</a>', '<a href="dokumenty.html#privacy">обработку персональных данных</a>')
# первый экран и подвал
R('<a class="btn btn--primary js-chalk" href="#signup">Записаться на&nbsp;тренировку</a>',
  '<button class="btn btn--primary js-chalk js-join" %s data-join-title="Запись на&nbsp;тренировку">Записаться на&nbsp;тренировку</button>' % JOIN, 2)
R('<li><a href="#goals">Для&nbsp;взрослых</a></li><li><a href="#kids">Для&nbsp;детей</a></li><li><a href="#prices">Цены</a></li><li><a href="#about">О&nbsp;скалодроме</a></li>',
  '<li><a href="dlya-vzroslyh.html">Для&nbsp;взрослых</a></li><li><a href="dlya-detej.html">Для&nbsp;детей</a></li><li><a href="ceny.html">Цены</a></li><li><a href="sertifikaty.html">Сертификаты</a></li><li><a href="o-skalodrome.html">О&nbsp;скалодроме</a></li>')
R('<li><a href="#">Тренеры</a></li><li><a href="#">Мероприятия</a></li><li><a href="#">Блог</a></li><li><a href="#reviews">Отзывы</a></li><li><a href="#">Вакансии</a></li>',
  '<li><a href="trenery.html">Тренеры</a></li><li><a href="meropriyatiya.html">Мероприятия</a></li><li><a href="blog/index.html">Блог</a></li><li><a href="video.html">Видео</a></li><li><a href="o-skalodrome.html#reviews">Отзывы</a></li><li><a href="vakansii.html">Вакансии</a></li>')
R('<li><a href="#">Правила посещения</a></li><li><a href="#">Техника безопасности</a></li><li><a href="#">Договор оферты</a></li><li><a href="#">Политика обработки персональных данных</a></li>',
  '<li><a href="dokumenty.html#pravila">Правила посещения</a></li><li><a href="dokumenty.html#tb">Техника безопасности</a></li><li><a href="dokumenty.html#oferta">Договор оферты</a></li><li><a href="dokumenty.html#privacy">Политика обработки персональных данных</a></li>')
R('<li>[Адрес], м. Площадь Ленина</li>', '<li><a href="kontakty.html#route">[Адрес], м. Площадь Ленина</a></li>')
# окно заявки: скрытое поле «что именно» — заполняется заголовком кнопки, которая открыла окно
R('<form class="cform cform--modal" novalidate>\n      <button class="modal__x js-join-close"',
  '<form class="cform cform--modal" novalidate>\n      <input type="hidden" name="what" value="">\n      <button class="modal__x js-join-close"')
io.open(p, 'w', encoding='utf-8').write(s)
print('было пустых ссылок:', n0, '· осталось:', s.count('href="#"'))
