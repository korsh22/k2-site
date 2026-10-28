/* Скалодром К2 — поиск по сайту: подсказки прямо под строкой поиска.
   Список страниц ниже — статичный. В MODX его заменит SimpleSearch / mSearch2 (или JSON из pdoResources). */
(function () {
  'use strict';
  var box = document.querySelector('#search .search__box'), q = document.getElementById('q');
  if (!box || !q) return;
  var me = document.currentScript && document.currentScript.src;
  var root = me ? me.replace(/js\/search\.js.*$/, '') : '';

  // [адрес от корня сайта, заголовок, раздел, слова для поиска]
  var PAGES = [
    ['index.html', 'Главная', 'Скалодром К2', 'скалодром к2 главная боулдеринг трудность 13 метров 1300'],
    ['pervyj-raz.html', 'Первый раз: пробная тренировка для взрослых', 'Новичкам', 'первый раз пробная тренировка новичок начинающим инструктор 60 минут взрослые'],
    ['dlya-vzroslyh.html', 'Скалолазание для взрослых', 'Для взрослых', 'взрослые направления тренировки'],
    ['bazovye-kursy.html', 'Базовые курсы', 'Для взрослых', 'базовый курс обучение страховка боулдеринг трудность программа 3-5 тренировок'],
    ['shkola.html', 'Школа скалолазания', 'Для взрослых', 'школа регулярные тренировки группа тренер прогресс соревнования'],
    ['individualnye.html', 'Индивидуальные тренировки', 'Для взрослых', 'индивидуальные персональные тренер'],
    ['samostoyatelno.html', 'Самостоятельные посещения', 'Для взрослых', 'самостоятельно разовое посещение абонемент допуск'],
    ['dlya-detej.html', 'Скалолазание для детей', 'Для детей', 'дети ребёнок ребенок детям'],
    ['detskaya-sekciya.html', 'Детская секция', 'Для детей', 'детская секция дети ребёнок ребенок группа 6 лет тренер'],
    ['deti-pervyj-raz.html', 'Пробная тренировка для ребёнка и семьи', 'Для детей', 'пробная детская ребёнок ребенок семья семейная взрослый ребёнок'],
    ['ceny.html', 'Цены', 'Цены', 'цены прайс стоимость абонемент разовое прокат pdf'],
    ['pakety.html', 'Пакеты тренировок', 'Цены', 'пакеты старт база расширенный нижняя страховка уровень сила выносливость скалы техника'],
    ['sertifikaty.html', 'Подарочные сертификаты', 'Цены', 'сертификат подарок подарочный'],
    ['meropriyatiya.html', 'Мероприятия', 'О нас', 'мероприятия соревнования выезд скалы события'],
    ['o-skalodrome.html', 'О скалодроме', 'О нас', 'о скалодроме зал боулдеринг трудность раздевалка душ отзывы'],
    ['trenery.html', 'Тренеры', 'О нас', 'тренеры инструкторы команда'],
    ['video.html', 'Видео', 'О нас', 'видео ролики обзор советы разминка'],
    ['vakansii.html', 'Вакансии', 'О нас', 'вакансии работа резюме'],
    ['dokumenty.html', 'Документы', 'О нас', 'документы правила техника безопасности оферта политика персональные данные'],
    ['kontakty.html', 'Контакты и как добраться', 'Контакты', 'контакты адрес телефон как добраться метро площадь ленина почта telegram max whatsapp'],
    ['blog/index.html', 'Блог о скалолазании', 'Блог', 'блог статьи'],
    ['blog/pervyj-vyezd-na-skaly.html', 'Первый выезд на скалы', 'Блог · Путешествия', 'скалы выезд путешествия'],
    ['blog/kak-ustroena-trenirovka.html', 'Сила, выносливость, техника: как устроена тренировка', 'Блог · Тренировки', 'тренировка сила выносливость техника разминка'],
    ['blog/snaryazhenie-vybor-i-uhod.html', 'Скальники, система, магнезия: снаряжение', 'Блог · Снаряжение', 'снаряжение скальники система магнезия'],
    ['blog/kak-ustroen-skalodrom-k2.html', 'Как устроен скалодром К2', 'Блог · Наш клуб', 'скалодром устроен зоны клуб']
  ];

  var norm = function (t) { return t.toLowerCase().replace(/ё/g, 'е').replace(/[^a-zа-я0-9 ]+/g, ' '); };
  var res = document.createElement('div');
  res.className = 'search__res'; res.id = 'search-res'; res.setAttribute('role', 'listbox'); res.hidden = true;
  box.insertAdjacentElement('afterend', res);
  q.setAttribute('aria-controls', 'search-res');

  function render() {
    var words = norm(q.value).split(' ').filter(function (w) { return w.length > 1; });
    if (!words.length) { res.hidden = true; res.innerHTML = ''; return; }
    var found = PAGES.map(function (p) {
      var hay = norm(p[1] + ' ' + p[3]), title = norm(p[1]), score = 0;
      words.forEach(function (w) {
        var stem = w.length > 4 ? w.slice(0, w.length - 2) : w; // «тренировки» находит «тренировка»
        if (hay.indexOf(stem) >= 0) score += title.indexOf(stem) >= 0 ? 3 : 1; else score -= 10;
      });
      return [score, p];
    }).filter(function (x) { return x[0] > 0; }).sort(function (a, b) { return b[0] - a[0]; }).slice(0, 6);
    res.hidden = false;
    res.innerHTML = found.length
      ? found.map(function (x) { return '<a class="search__i" role="option" href="' + root + x[1][0] + '"><b>' + x[1][1] + '</b><small>' + x[1][2] + '</small></a>'; }).join('')
      : '<p class="search__none">Ничего не нашли. Попробуйте «цены», «дети» или «пробная тренировка» — или позвоните нам.</p>';
  }
  q.addEventListener('input', render);
  box.addEventListener('submit', function (e) { e.preventDefault(); var first = res.querySelector('.search__i'); if (first) location.href = first.href; });
  box.removeAttribute('onsubmit');
})();
