# -*- coding: utf-8 -*-
"""Собирает посадочные страницы К2 (пока «Первый раз»): site/pervyj-raz.html
Шапка, меню, поиск, подвал, загруженность и окно заявки берутся из site/index.html.
Запуск:  python tools/build_pages.py
"""
import io, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from typograph import process as typograph

from chrome import ROOT, VER, parts
P = parts(0)
HEADER, MMENU, SEARCH, FOOTER, OCC, JOIN, LB = P['HEADER'], P['MMENU'], P['SEARCH'], P['FOOTER'], P['OCC'], P['JOIN'], P['LB']

CHEV = '<svg class="chev" viewBox="0 0 16 26"><path d="M0 0l16 13L0 26V17l5-4-5-4z"/></svg>'
CHECK = '<svg class="ico" viewBox="0 0 24 24"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>'
def ico(path): return '<svg class="ico" viewBox="0 0 24 24">%s</svg>' % path
I_TIME = ico('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>')
I_SPARK = ico('<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5L18 18M6 18l2.5-2.5M15.5 8.5L18 6"/>')
I_GEAR = ico('<path d="M7 4h10l2 6H5z"/><path d="M5 10v8a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-8"/><path d="M10 14h4"/>')
I_PEOPLE = ico('<circle cx="9" cy="8" r="3"/><path d="M3 20a6 6 0 0 1 12 0"/><circle cx="17" cy="9" r="2.5"/><path d="M15.5 14.2A5 5 0 0 1 21 19"/>')
I_LOCKER = ico('<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M12 3v18M9 11v2M15 11v2"/>')
I_SHOWER = ico('<path d="M4 20V8a4 4 0 0 1 8 0"/><path d="M8 8h8"/><path d="M14 12v1M17 12v1M20 12v1M14 16v1M17 16v1M20 16v1"/>')
I_HANGER = ico('<path d="M12 7a2 2 0 1 1 2-2"/><path d="M12 7v2L3 15a1 1 0 0 0 .6 1.8h16.8a1 1 0 0 0 .6-1.8L12 9"/>')
I_TOWEL = ico('<path d="M6 3h12v14a3 3 0 0 1-3 3H9a3 3 0 0 1-3-3z"/><path d="M6 8h12"/>')
ARROW = '<svg class="ico" viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
PRICE = ('<span class="price" data-price="" data-price-old=""><s class="price__old"><span class="sr">Старая цена: </span>от [____]&nbsp;₽</s>'
         '<b class="price__new"><span class="sr">Цена: </span>от [____]&nbsp;₽</b></span>')

def li(items): return ''.join('<li>%s%s</li>' % (CHECK, x) for x in items)

COACHES = [('[Имя Фамилия]', 'Старший тренер', '[КМС по скалолазанию · стаж 10 лет]'),
           ('[Имя Фамилия]', 'Тренер по боулдерингу', '[Инструктор-методист · стаж 6 лет]'),
           ('[Имя Фамилия]', 'Тренер по трудности', '[Инструктор по страховке · стаж 5 лет]'),
           ('[Имя Фамилия]', 'Детский тренер', '[Педагог доп. образования · стаж 4 года]')]
FAQ = [('Нужна ли физическая подготовка?', 'Нет. Пробная тренировка рассчитана на любой уровень: тренер подберёт трассы и нагрузку под вас.'),
       ('Что, если мне станет страшно на высоте?', 'Это нормально. Начинаем с боулдеринга — невысоких трасс над матами, а на высокие стены идём только когда вы готовы и со страховкой.'),
       ('Можно ли прийти одному?', 'Да. В групповой тренировке вы познакомитесь с другими новичками, а персонально можно прийти одному, вдвоём или втроём.'),
       ('Что взять с собой?', 'Только удобную спортивную форму. Скальные туфли, страховочную систему и магнезию выдадим на месте.'),
       ('Когда приходить?', 'Лучше за 10–15 минут до начала тренировки, чтобы спокойно переодеться и подобрать снаряжение.'),
       ('С какого возраста можно?', 'Взрослая пробная тренировка — с 16 лет. Для детей от 6 лет есть детские пробные тренировки и секция.'),
       ('Можно ли перенести или отменить запись?', '[Условия переноса и отмены уточняются.]'),
       ('Что делать после пробной тренировки?', 'Тренер подскажет следующий формат: базовые курсы, групповые тренировки или самостоятельные посещения.')]
GAL = [('p-blue.jpg', 'Синяя стена с нависанием'), ('p-mat.jpg', 'Отдых на матах'), ('p-cave.jpg', 'Под нависанием'),
       ('k2-first-1.jpg', 'Боулдеринг в зале'), ('p-roof.jpg', 'Лазание по потолку'), ('k2-first-2.jpg', 'Трасса на нависании'),
       ('k2-hall.jpg', 'Зал скалодрома К2'), ('p-dyno.jpg', 'Прыжок к зацепу'), ('k2-first-3.jpg', 'Вместе на скалодроме')]
SUBNAV = [('who', 'Кому подойдёт'), ('how', 'Как проходит'), ('video', 'Видео'), ('formats', 'Форматы и цены'),
          ('bring', 'Что взять'), ('coaches', 'Тренеры'), ('reviews', 'Отзывы'), ('faq', 'Вопросы')]

body = '''<main class="lp">
<!-- 1. Первый экран -->
<section class="lp-hero dark" id="top">
  <div class="wrap lp-hero__g">
    <div class="lp-hero__text">
      <nav class="crumbs" aria-label="Хлебные крошки"><a href="index.html">Главная</a><span>/</span><span>Первый раз</span></nav>
      <h1 class="d lp-hero__t reveal">Скалолазание для взрослых новичков&nbsp;— пробная тренировка</h1>
      <p class="lead lp-hero__l reveal">Первое знакомство со скалолазанием без опыта и собственного снаряжения. За 60 мин. с тренером разберём основы и полазаем!</p>
      <ul class="lp-marks reveal">
        <li>%(I_TIME)s<span>60 минут</span></li>
        <li>%(I_SPARK)s<span>Опыт не нужен</span></li>
        <li>%(I_GEAR)s<span>Снаряжение включено</span></li>
        <li>%(I_PEOPLE)s<span>В группе или персонально</span></li>
      </ul>
      <div class="btns reveal"><button class="btn btn--primary js-book" type="button">Выбрать формат и записаться</button></div>
    </div>
    <figure class="lp-hero__img reveal">
      <img src="assets/img/p-focus.jpg" alt="Скалолазка на стене" fetchpriority="high">
      <!-- Нужно фото: взрослый новичок на доступной трассе, рядом тренер объясняет, лицо видно, чувствуется масштаб зала -->
      <figcaption class="lp-hero__cap"><span class="occ-line js-occ-line" role="button" tabindex="0" aria-controls="occ"><i aria-hidden="true"></i><span>Загруженность зала</span></span></figcaption>
    </figure>
  </div>
</section>

<!-- Липкое меню по разделам -->
<nav class="lp-sub" aria-label="Разделы страницы">
  <button class="lp-sub__toggle" type="button" aria-expanded="false"><span class="lp-sub__cur">Разделы страницы</span><span class="lp-sub__more">Разделы<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg></span></button>
  <div class="wrap lp-sub__in">%(SUBNAV)s</div>
</nav>

<!-- 2. Кому подойдёт -->
<section class="sec neutral" id="who">
  <div class="wrap">
    <div class="lp-intro">
      <h2 class="d h2 reveal">Можно прийти, даже если вы никогда не&nbsp;лазали</h2>
      <p class="lead muted reveal">Пробная тренировка создана именно для первого знакомства со скалолазанием. Не нужно заранее изучать технику или покупать экипировку&nbsp;— тренер всё объяснит на месте и подберёт задания под ваш стартовый уровень.</p>
    </div>
    <p class="lp-k reveal">Приходите в К2, даже если вы:</p>
    <div class="lp-cards4">
      <div class="lp-c reveal"><span class="lp-c__n">01</span><b>Никогда не пробовали</b><p>Начнём с базовых правил и простых движений.</p></div>
      <div class="lp-c reveal"><span class="lp-c__n">02</span><b>Хотите понять, ваш ли это спорт</b><p>За одно занятие вы познакомитесь с форматом и попробуете первые трассы.</p></div>
      <div class="lp-c reveal"><span class="lp-c__n">03</span><b>Хотите прийти один или с друзьями</b><p>Можно выбрать групповую или персональную тренировку для 1–3 участников.</p></div>
      <div class="lp-c reveal"><span class="lp-c__n">04</span><b>Не уверены в своей подготовке</b><p>Тренер поможет выбрать подходящую нагрузку и темп.</p></div>
    </div>
  </div>
</section>

<!-- 3. Как проходит -->
<section class="sec dark stack lp-hour" id="how">
  <!-- Сцена «60 минут»: на компьютере блок закреплён, прокрутка ведёт таймер 0→60 и переключает шаги и фото;
       на телефоне шаги листаются сами (пока блок на экране) и по нажатию. Логика — js/landing.js (setupHour) -->
  <div class="lp-hour__track">
    <div class="lp-hour__stage wrap">
      <div class="lp-hour__head">
        <h2 class="d h2 reveal">Что будет происходить 60&nbsp;минут?</h2>
        <p class="lp-hour__clock reveal" aria-hidden="true"><b class="d">00</b><span>мин<br>из&nbsp;60</span></p>
      </div>
      <div class="lp-hour__g">
        <div class="lp-hour__pics reveal" aria-hidden="true">
          <img class="is-on" src="assets/img/p-gear.jpg" alt="" loading="lazy">
          <img src="assets/img/p-fun.jpg" alt="" loading="lazy">
          <img src="assets/img/p-wall.jpg" alt="" loading="lazy">
          <img src="assets/img/p-smile.jpg" alt="" loading="lazy">
          <span class="lp-hour__badge"><i></i><span>Шаг 01 · ~10 мин</span></span>
        </div>
        <ol class="lp-hour__steps">
          <li class="is-on" data-from="0" data-to="10"><img class="lp-hour__ph" src="assets/img/p-gear.jpg" alt="" loading="lazy"><button type="button"><span class="lp-hour__n d">01</span><span><b>Знакомство и&nbsp;экипировка</b><small>~10 мин</small></span></button><p>Тренер уточнит ваш опыт, расскажет о&nbsp;занятии и&nbsp;поможет подобрать необходимое снаряжение.</p></li>
          <li data-from="10" data-to="20"><img class="lp-hour__ph" src="assets/img/p-fun.jpg" alt="" loading="lazy"><button type="button"><span class="lp-hour__n d">02</span><span><b>Инструктаж и&nbsp;разминка</b><small>~10 мин</small></span></button><p>Вы познакомитесь с&nbsp;основными правилами безопасности и&nbsp;подготовитесь к&nbsp;лазанию.</p></li>
          <li data-from="20" data-to="55"><img class="lp-hour__ph" src="assets/img/p-wall.jpg" alt="" loading="lazy"><button type="button"><span class="lp-hour__n d">03</span><span><b>Первые трассы</b><small>~35 мин</small></span></button><p>Тренер покажет базовые движения, поможет работать ногами и&nbsp;подберёт трассы подходящего уровня. Сначала полазаем на&nbsp;<span class="term" data-term="bould">боулдеринге</span> (низкий скалодром), а&nbsp;потом перейдём на&nbsp;<span class="term" data-term="lead">трудность</span> (высокий скалодром).</p></li>
          <li data-from="55" data-to="60"><img class="lp-hour__ph" src="assets/img/p-smile.jpg" alt="" loading="lazy"><button type="button"><span class="lp-hour__n d">04</span><span><b>Обратная связь</b><small>~5 мин</small></span></button><p>В&nbsp;конце занятия тренер ответит на&nbsp;вопросы и&nbsp;подскажет, какой формат выбрать дальше.</p></li>
        </ol>
      </div>
      <div class="lp-hour__bar reveal" aria-hidden="true">
        <span style="--w:10"></span><span style="--w:10"></span><span style="--w:35"></span><span style="--w:5"></span>
        <small style="--x:0">0</small><small style="--x:10">10</small><small style="--x:20">20</small><small style="--x:55">55</small><small style="--x:60">60 мин</small>
      </div>
    </div>
  </div>
  <div class="wrap">
    <!-- Финиш: пункты по очереди «отмечаются», когда блок появляется на экране -->
    <div class="lp-fin reveal">
      <span class="lp-fin__big d" aria-hidden="true">60:00</span>
      <div class="lp-fin__l">
        <span class="lp-fin__k"><i></i>Финиш · 60&nbsp;минут</span>
        <p class="lp-fin__t d">После тренировки вы:</p>
        <button class="btn btn--light js-book" type="button">Записаться на&nbsp;пробную</button>
      </div>
      <ol class="lp-fin__list">%(AFTER)s</ol>
    </div>
  </div>
</section>

<!-- 3б. Видеообзор пробной тренировки (видео добавим позже) -->
<section class="sec dark lp-video-sec" id="video">
  <div class="wrap">
    <div class="sechead"><div><h2 class="d h2 reveal">Как проходит пробная тренировка</h2><p class="lead muted reveal">Короткий видеообзор: от&nbsp;знакомства с&nbsp;тренером до&nbsp;первых трасс</p></div></div>
    <!-- В MODX: ссылка на ролик (TV). Пока роликa нет — показывается обложка с пометкой «Видео скоро» -->
    <div class="lp-video reveal" data-video="">
      <picture><source media="(max-width: 767px)" srcset="assets/img/p-forest.jpg"><img src="assets/img/p-chalk.jpg" alt="" loading="lazy"></picture>
      <span class="lp-video__shade"></span>
      <button class="lp-video__play" type="button" aria-label="Смотреть видеообзор пробной тренировки"><svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg></button>
      <span class="lp-video__soon">Видео скоро</span>
      <span class="lp-video__meta"><b>Видеообзор пробной тренировки</b><small>[0:00]</small></span>
    </div>
  </div>
</section>

<!-- 4. Форматы и цены -->
<section class="sec neutral stack lp-fmt" id="formats">
  <div class="wrap">
    <div class="sechead"><div><h2 class="d h2 reveal">Выберите удобный формат</h2><p class="lead muted reveal">Оба варианта подходят для первого знакомства со скалолазанием. Отличаются размер группы, количество внимания тренера и стоимость.</p></div></div>
    <div class="lp-formats">
      <article class="lp-f reveal">
        <span class="badge">Группа до 8 человек</span>
        <h3 class="d lp-f__t">Пробная тренировка в&nbsp;группе</h3>
        <ul class="lp-list lp-list--dark">%(F1)s</ul>
        <p class="lp-f__d">Подойдёт, если хочется попробовать скалолазание в&nbsp;живой атмосфере и&nbsp;познакомиться с&nbsp;другими новичками. Тренер объясняет общую базу и&nbsp;помогает каждому участнику.</p>
        <div class="lp-f__foot">%(PRICE)s<button class="btn btn--primary js-book" type="button" data-book-type="group">Записаться</button></div>
      </article>
      <article class="lp-f lp-f--dark reveal">
        <span class="badge badge--dark">1–3 участника</span>
        <h3 class="d lp-f__t">Персональная пробная тренировка</h3>
        <ul class="lp-list">%(F2)s</ul>
        <p class="lp-f__d">Больше внимания тренера и&nbsp;возможность двигаться в&nbsp;своём темпе. Можно прийти одному, вдвоём или втроём.</p>
        <div class="lp-f__foot">%(PRICE)s<button class="btn btn--primary js-book" type="button" data-book-type="personal">Записаться</button></div>
      </article>
    </div>
    <div class="lp-help reveal">
      <p><b>Не знаете, какой формат выбрать?</b> Оставьте заявку&nbsp;— администратор поможет подобрать подходящий вариант.</p>
      <button class="btn btn--sec js-join" type="button" aria-haspopup="dialog" aria-controls="join" data-join-title="Поможем выбрать формат" data-join-topic="trial">Оставить заявку</button>
    </div>
  </div>
</section>

<!-- 5. Что взять с собой -->
<section class="sec neutral" id="bring">
  <div class="wrap lp-bring">
    <div class="lp-bring__main reveal">
      <h2 class="d h2">С&nbsp;собой&nbsp;— только удобная спортивная форма</h2>
      <p class="lead muted">Выберите одежду, которая не ограничивает движения. Специальное снаряжение покупать не нужно: <span class="term" data-term="shoes">скальные туфли</span>, страховочную систему и&nbsp;<span class="term" data-term="chalk">магнезию</span> выдадим на&nbsp;месте.</p>
      <p class="lp-bring__note">%(I_TIME)s<span>Прийти лучше за&nbsp;10–15 минут до&nbsp;начала тренировки</span></p>
    </div>
    <div class="lp-bring__side reveal">
      <p class="lp-k">В К2 есть всё для комфортного посещения и&nbsp;тренировок:</p>
      <ul class="lp-amen">
        <li>%(I_HANGER)s<span>Раздевалка</span></li>
        <li>%(I_SHOWER)s<span>Душевая</span></li>
        <li>%(I_LOCKER)s<span>Шкафчики</span></li>
        <li>%(I_TOWEL)s<span>Аренда полотенец</span></li>
      </ul>
    </div>
  </div>
</section>

<!-- 6. Почему К2: фото на весь экран с параллаксом, крупные цифры (набегают от нуля), шкала 0 → 13 м справа. Логика — js/landing.js (setupWhy) -->
<section class="lp-why2 dark" id="why">
  <div class="lp-why2__bg" aria-hidden="true"><picture><source media="(max-width: 767px)" srcset="assets/img/p-dyno.jpg"><img src="assets/img/k2-rock.jpg" alt="" loading="lazy"></picture></div>
  <div class="lp-why2__meter" aria-hidden="true">
    <span class="lp-why2__tick" style="--h:0">0</span><span class="lp-why2__tick" style="--h:5">5</span><span class="lp-why2__tick" style="--h:10">10</span><span class="lp-why2__tick" style="--h:13">13 м</span>
    <i class="lp-why2__fill"></i><span class="lp-why2__dot"><b>0.0</b> м</span>
  </div>
  <div class="wrap lp-why2__in">
    <div class="lp-why2__head">
      <span class="mark reveal">Почему К2</span>
      <h2 class="d lp-why2__t reveal">Почему первое занятие стоит провести в&nbsp;К2</h2>
    </div>
    <ul class="lp-why2__stats">
      <li class="reveal"><b class="d"><span data-count="13">13</span><small>м</small></b><span><em>высоты</em> Просторная зона трудности для занятий со&nbsp;страховкой.</span></li>
      <li class="reveal"><b class="d"><span data-count="1300">1300</span><small>м²</small></b><span>Боулдеринг и&nbsp;трудность под одной крышей.</span></li>
      <li class="reveal"><b class="d"><span data-count="7">7</span><small>мин</small></b><span><em>от метро</em> Удобно добираться от&nbsp;станции «Площадь Ленина».</span></li>
    </ul>
    <div class="lp-why2__cards">
      <div class="lp-why2__c lp-why2__c--red reveal"><b class="d">Новый скалодром</b><p>Новые стены, зацепы и&nbsp;снаряжение.</p></div>
      <div class="lp-why2__c reveal"><b class="d">Всё необходимое на&nbsp;месте</b><p>Не нужно покупать снаряжение перед первым занятием.</p></div>
      <div class="lp-why2__go reveal"><button class="btn btn--light js-book" type="button">Выбрать формат и&nbsp;записаться</button></div>
    </div>
  </div>
</section>

<!-- 7. Тренеры -->
<section class="sec neutral" id="coaches">
  <div class="wrap">
    <div class="sechead"><div><h2 class="d h2 reveal">Кто проводит первые тренировки</h2><p class="lead muted reveal">Важно не только хорошо лазать, но и&nbsp;уметь спокойно и&nbsp;понятно объяснять новичкам</p></div></div>
    <!-- В MODX: тренеры — ресурсы/MIGX (фото, имя, должность, квалификация) -->
    <div class="lp-coaches">%(COACHES)s</div>
    <div class="lp-center reveal"><a class="btn btn--sec" href="trenery.html">Познакомиться со всеми тренерами</a></div>
  </div>
</section>

<!-- 8. Отзывы -->
<section class="sec neutral stack lp-alt" id="reviews">
  <div class="wrap">
    <div class="sechead"><h2 class="d h2 reveal">Отзывы новичков</h2></div>
    <div class="widget reveal"><b>[Виджет отзывов]</b><span>Подтягивается с&nbsp;внешнего сервиса&nbsp;— [Яндекс Карты / 2ГИС]</span></div>
  </div>
</section>

<!-- 9. Фото -->
<section class="sec neutral lp-alt" id="photos">
  <div class="wrap">
    <div class="sechead"><h2 class="d h2 reveal">Атмосфера К2</h2><p class="muted hint reveal">Нажмите на&nbsp;фото&nbsp;— откроется галерея</p></div>
    <div class="lp-gal">%(GAL)s</div>
    <div class="lp-center"><button class="btn btn--sec js-gal-more" type="button" aria-expanded="false">Показать ещё</button></div>
  </div>
</section>

<!-- 10. FAQ -->
<section class="sec neutral" id="faq">
  <div class="wrap">
    <div class="sechead"><h2 class="d h2 reveal">Частые вопросы новичков</h2></div>
    <div class="faq"><div class="faq__col">%(FAQ1)s</div><div class="faq__col">%(FAQ2)s</div></div>
  </div>
</section>

<!-- 11. Блог -->
<section class="sec neutral lp-alt" id="blog">
  <div class="wrap">
    <div class="sechead"><h2 class="d h2 reveal">Полезно перед первым занятием</h2><a class="btn btn--sec reveal" href="blog/index.html">Все статьи</a></div>
    <div class="posts lp-posts">
      <a class="post reveal" href="blog/kak-ustroen-skalodrom-k2.html"><span class="post__img"><img src="assets/img/k2-hall.jpg" alt="" loading="lazy"></span><span class="post__b"><span class="badges"><span class="badge">Наш клуб</span></span><span class="post__t">Как устроен скалодром К2</span><span class="post__m">[дата] · 2 мин чтения</span></span></a>
      <a class="post reveal" href="blog/snaryazhenie-vybor-i-uhod.html"><span class="post__img"><img src="assets/img/p-mat.jpg" alt="" loading="lazy"></span><span class="post__b"><span class="badges"><span class="badge">Снаряжение</span></span><span class="post__t">Скальники, система, магнезия: как выбрать и хранить снаряжение</span><span class="post__m">[дата] · 2 мин чтения</span></span></a>
      <a class="post reveal" href="blog/kak-ustroena-trenirovka.html"><span class="post__img"><img src="assets/img/p-chalk.jpg" alt="" loading="lazy"></span><span class="post__b"><span class="badges"><span class="badge">Тренировки</span></span><span class="post__t">Сила, выносливость, техника: как устроена тренировка скалолаза</span><span class="post__m">[дата] · 2 мин чтения</span></span></a>
    </div>
  </div>
</section>

<!-- 12. Уже занимались -->
<section class="sec neutral sec--flush">
  <div class="wrap">
    <div class="lp-next lp-next--art reveal">
      <div><h2 class="d h2">Уже занимались скалолазанием?</h2><p class="lead">Если вы знакомы с&nbsp;базовой техникой и&nbsp;хотите тренироваться регулярно, посмотрите пакетные предложения К2&nbsp;— от&nbsp;системного освоения базы до&nbsp;работы над техникой, силой и&nbsp;выносливостью.</p></div>
            <!-- фон: бледный знак К2 за краем блока + круглая «печать» с текстом по кругу (приём из референсов) -->
      <svg class="lp-next__mark" viewBox="19 24 698 322" aria-hidden="true"><path d="M716.4,59.9v89l-90,62.4l90-1v133.8h-347V219.8l90-35.4l-90-35.4V24.5h257L716.4,59.9z"/><path d="M167.4,167.2l23.7-143h146.3v4l-24,145h24v171H190.8l-23.3-141v141h-148v-320h148V167.2z"/></svg>
      <a class="lp-stamp" href="pakety.html" aria-label="Смотреть пакеты тренировок"><svg viewBox="0 0 120 120" aria-hidden="true"><defs><path id="stampC" d="M60 60m-46 0a46 46 0 1 1 92 0a46 46 0 1 1-92 0"/></defs><text textLength="286" lengthAdjust="spacingAndGlyphs"><textPath href="#stampC" textLength="286" lengthAdjust="spacingAndGlyphs">следующий уровень · пакеты · </textPath></text></svg><i><svg class="ico" viewBox="0 0 24 24"><path d="M7 17L17 7M9 7h8v8"/></svg></i></a>
      <a class="btn btn--light" href="pakety.html">Смотреть пакетные предложения</a>
    </div>
  </div>
</section>
</main>

<!-- Всегда доступная кнопка записи -->
<button class="lp-fab btn btn--primary js-book" type="button" aria-hidden="true" tabindex="-1">Записаться на&nbsp;тренировку</button>
'''

OK_TICK = '<svg class="lp-fin__ok" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="11"/><path d="M7 12.5l3.2 3.2L17 9" pathLength="1"/></svg>'
FIN = ''.join('<li><span class="lp-fin__ic">%s</span><span class="lp-fin__tx">%s</span>%s</li>' % (ic, t, OK_TICK) for ic, t in [
    (ico('<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/>'), 'поймёте основные правила поведения на скалодроме'),
    (ico('<path d="M6 20c1-4 3-6 6-7M12 13c3-1 5-4 5-8"/><circle cx="17" cy="5" r="2"/><circle cx="7" cy="14" r="2"/><circle cx="13" cy="9" r="1.6"/>'), 'попробуете первые трассы'),
    (ico('<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5L18 18M6 18l2.5-2.5M15.5 8.5L18 6"/>'), 'познакомитесь с базовыми движениями'),
    (ico('<path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/>'), 'поймёте, хотите ли заниматься дальше'),
    (ico('<path d="M4 20l6-8 4 4 6-9"/><path d="M15 7h5v5"/>'), 'получите рекомендацию по следующему формату')])

def coach(c, i=0):
    # фото — временные заглушки (не наши тренеры), заменить снимками тренеров К2
    return ('<article class="lp-coach reveal"><div class="lp-coach__img"><img src="assets/img/coach-%d.jpg" alt="Фото-заглушка" loading="lazy"></div>'
            '<b class="lp-coach__n">%s</b><span class="lp-coach__r">%s</span><span class="lp-coach__q">%s</span></article>') % (i % 4 + 1, c[0], c[1], c[2])
def faq(items, first=False):
    return ''.join('<details class="reveal"%s><summary>%s<i></i></summary><div class="faq__a"><p>%s</p></div></details>' % (' open' if (first and i == 0) else '', q, a) for i, (q, a) in enumerate(items))
def gal(items):
    return ''.join('<button class="lp-gal__i%s" type="button" data-i="%d" aria-label="Открыть фото: %s"><img src="assets/img/%s" alt="%s" loading="lazy"></button>' % (' is-more' if i >= 7 else '', i, a, f, a) for i, (f, a) in enumerate(items))

body = body % {
    'I_TIME': I_TIME, 'I_SPARK': I_SPARK, 'I_GEAR': I_GEAR, 'I_PEOPLE': I_PEOPLE, 'I_HANGER': I_HANGER, 'I_SHOWER': I_SHOWER, 'I_LOCKER': I_LOCKER, 'I_TOWEL': I_TOWEL,
    'SUBNAV': ''.join('<a href="#%s" style="--i:%d">%s<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5v14M6 13l6 6 6-6"/></svg></a>' % (h, i, t) for i, (h, t) in enumerate(SUBNAV)),
    'AFTER': FIN,
    'F1': li(['60 минут', 'группа до 8 человек', 'для взрослых новичков', 'работа тренера', 'необходимое снаряжение', 'вход на скалодром']),
    'F2': li(['60 минут', 'для 1–3 участников', 'индивидуальный темп', 'работа тренера', 'необходимое снаряжение', 'вход на скалодром [подтвердить включение]']),
    'PRICE': PRICE,
    'COACHES': ''.join(coach(c, i) for i, c in enumerate(COACHES)),
    'FAQ1': faq(FAQ[:4], True), 'FAQ2': faq(FAQ[4:]),
    'GAL': gal(GAL),
}

BOOK = '''<!-- ЕДИНАЯ форма бронирования с калькулятором. Цены — data-атрибуты (в MODX из прайса), оплата — переход в банк (подключит разработчик) -->
<dialog class="modal book" id="book" aria-labelledby="book-t" data-price-group="" data-price-group-kid="" data-price-personal="" data-price-personal-kid="">
  <div class="modal__card book__card">
    <form class="cform cform--modal book__form" novalidate>
      <button class="modal__x js-book-close" type="button" aria-label="Закрыть"><svg class="ico" viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18"/></svg></button>
      <div class="cform__body">
        <div class="cform__top"><h3 class="cform__t" id="book-t">Запись на&nbsp;пробную тренировку</h3><p class="cform__s">Выберите формат и&nbsp;участников&nbsp;— стоимость посчитается сразу</p></div>
        <fieldset class="cform__set">
          <legend>Формат</legend>
          <div class="book__types">
            <label class="book__type"><input type="radio" name="type" value="group" checked><span><b>В группе</b><small>до 8 человек</small></span></label>
            <label class="book__type"><input type="radio" name="type" value="personal"><span><b>Персонально</b><small>1–3 участника</small></span></label>
          </div>
        </fieldset>
        <fieldset class="cform__set">
          <legend>Кто придёт</legend>
          <div class="book__counts">
            <div class="book__count" data-k="adults"><span><b>Взрослые</b><small>от 16 лет</small></span><div class="step"><button type="button" class="step__b" data-d="-1" aria-label="Меньше взрослых">−</button><output class="step__v">1</output><button type="button" class="step__b" data-d="1" aria-label="Больше взрослых">+</button></div></div>
            <div class="book__count" data-k="kids"><span><b>Дети</b><small>6–15 лет</small></span><div class="step"><button type="button" class="step__b" data-d="-1" aria-label="Меньше детей">−</button><output class="step__v">0</output><button type="button" class="step__b" data-d="1" aria-label="Больше детей">+</button></div></div>
          </div>
          <p class="book__limit" aria-live="polite"></p>
        </fieldset>
        <div class="cform__row">
          <div class="field"><input id="b-date" name="date" type="date" placeholder=" "><label for="b-date">Желаемая дата</label></div>
          <div class="field field--select"><select id="b-time" name="time"><option value="">Любое время</option><option>Утро (8–12)</option><option>День (12–17)</option><option>Вечер (17–23)</option></select><label for="b-time" class="is-up">Удобное время</label></div>
        </div>
        <div class="cform__row">
          <div class="field"><input id="b-name" name="name" type="text" autocomplete="given-name" placeholder=" " required><label for="b-name">Ваше имя</label><span class="field__err">Как к&nbsp;вам обращаться?</span></div>
          <div class="field"><input id="b-phone" name="phone" type="tel" inputmode="tel" autocomplete="tel" placeholder=" " required><label for="b-phone">Телефон</label><span class="field__err">Проверьте номер&nbsp;— нужно 10&nbsp;цифр после +7</span></div>
        </div>
        <div class="book__sum" aria-live="polite">
          <div class="book__rows"></div>
          <div class="book__total"><span>Итого</span><b class="book__total-v">[____]&nbsp;₽</b></div>
        </div>
        <div class="cform__agree">
          <label class="agree"><input type="checkbox" name="agree" required><span class="agree__box"></span><span>Согласен на&nbsp;<a href="dokumenty.html#privacy">обработку персональных данных</a> и&nbsp;<a href="dokumenty.html#oferta">условия оферты</a></span></label>
          <span class="field__err field__err--agree">Нужно согласие, чтобы оформить запись</span>
        </div>
        <button class="btn btn--primary cform__go" type="submit">Перейти к&nbsp;оплате</button>
        <p class="book__note">Оплата картой через банк. Запись подтвердим звонком или сообщением.</p>
      </div>
      <div class="cform__done" aria-live="polite" hidden>
        <svg class="done__ic" viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="32" r="29"/><path d="M19 33l9 9 17-19"/></svg>
        <h3 class="cform__t">Почти готово</h3>
        <p class="cform__s done__msg"></p>
        <p class="book__demo">Демо-версия: переход в&nbsp;банк подключит разработчик.</p>
        <button class="btn btn--sec js-book-close" type="button">Закрыть</button>
      </div>
    </form>
  </div>
</dialog>
'''

GLOSS_TIP = '<div class="tip" id="tip" role="tooltip" aria-hidden="true"><b class="tip__t"></b><span class="tip__d"></span></div>'

html = '''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Пробная тренировка по скалолазанию для взрослых новичков — скалодром К2</title>
<meta name="description" content="Пробная тренировка для взрослых без опыта: 60 минут с тренером, всё снаряжение выдаём, в группе или персонально. Скалодром К2, 7 минут от м. Площадь Ленина.">
<link rel="stylesheet" href="css/style.css?v=%(V)s">
<link rel="stylesheet" href="css/blog.css?v=%(V)s">
<link rel="stylesheet" href="css/landing.css?v=%(V)s">
</head>
<body class="page page--lp">
%(HEADER)s

%(MMENU)s
%(SEARCH)s
%(BODY)s

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
''' % {'V': VER, 'HEADER': HEADER, 'MMENU': MMENU, 'SEARCH': SEARCH, 'BODY': body, 'FOOTER': FOOTER, 'OCC': OCC, 'JOIN': JOIN, 'BOOK': BOOK, 'LB': LB, 'TIP': GLOSS_TIP}

io.open(os.path.join(ROOT, 'pervyj-raz.html'), 'w', encoding='utf-8').write(typograph(html))
print('страница: pervyj-raz.html, версия', VER)
