/* Скалодром К2 — посадочные страницы: бронирование с калькулятором, окно заявки, галерея,
   словарик, липкое меню разделов, плавающая кнопка записи, видео. Общие шапка/меню/загруженность — в blog.js */
(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var clamp = function (v, a, b) { return Math.min(b, Math.max(a, v)); };

  /* ---------- Поля форм: маска телефона, проверка ---------- */
  function phoneMask(phone) {
    phone.addEventListener('focus', function () { if (!phone.value) phone.value = '+7 '; });
    phone.addEventListener('blur', function () { if (phone.value.replace(/\D/g, '').length <= 1) phone.value = ''; });
    phone.addEventListener('input', function () {
      var d = phone.value.replace(/\D/g, '');
      if (d[0] === '8' || d[0] === '7') d = d.slice(1);
      d = d.slice(0, 10);
      var out = '+7 ';
      if (d.length) out += '(' + d.slice(0, 3);
      if (d.length >= 3) out += ') ' + d.slice(3, 6);
      if (d.length >= 6) out += '-' + d.slice(6, 8);
      if (d.length >= 8) out += '-' + d.slice(8, 10);
      phone.value = out;
      if (d.length === 10) phone.parentNode.classList.remove('is-bad');
    });
  }
  function validate(form) {
    var name = $('[name="name"]', form), phone = $('[name="phone"]', form), agree = $('[name="agree"]', form);
    var okName = !!name.value.trim(), okPhone = phone.value.replace(/\D/g, '').length === 11;
    name.parentNode.classList.toggle('is-bad', !okName);
    phone.parentNode.classList.toggle('is-bad', !okPhone);
    $('.field__err--agree', form).classList.toggle('is-on', !agree.checked);
    if (okName && okPhone && agree.checked) return true;
    form.classList.remove('is-shake'); void form.offsetWidth; form.classList.add('is-shake');
    (!okName ? name : !okPhone ? phone : agree).focus();
    return false;
  }
  function showDone(form, msg) {
    $('.done__msg', form).textContent = msg;
    form.classList.add('is-sent');
    var done = $('.cform__done', form); done.hidden = false;
    var ic = $('.done__ic', done); ic.replaceWith(ic.cloneNode(true));
  }
  function resetForm(form) { form.reset(); form.classList.remove('is-sent'); $('.cform__done', form).hidden = true; var seg = $('.seg', form); if (seg) seg.style.setProperty('--i', 0); }
  // Отправка: если у формы есть data-action (обработчик FormIt / AjaxForm в MODX) — шлём туда; иначе демо
  function send(form, ok) {
    var action = form.dataset.action, fail = $('.cform__fail', form);
    if (fail) fail.remove();
    if (!action) { ok(); return; }
    var go = $('.cform__go', form); go.disabled = true;
    fetch(action, { method: 'POST', body: new FormData(form), headers: { 'X-Requested-With': 'XMLHttpRequest' } })
      .then(function (r) { if (!r.ok) throw r; ok(); })
      .catch(function () {
        var p = document.createElement('p'); p.className = 'cform__fail'; p.setAttribute('role', 'alert');
        p.textContent = 'Не\u00a0получилось отправить заявку. Позвоните нам или\u00a0попробуйте ещё раз.';
        go.insertAdjacentElement('afterend', p);
      })
      .then(function () { go.disabled = false; });
  }
  $$('form.cform').forEach(function (form) {
    var phone = $('[name="phone"]', form), name = $('[name="name"]', form), agree = $('[name="agree"]', form);
    if (form.hasAttribute('data-own') || !phone || !name || !agree) return;  // корзина и окно пробной — со своей логикой
    phoneMask(phone);
    name.addEventListener('input', function () { if (name.value.trim()) name.parentNode.classList.remove('is-bad'); });
    agree.addEventListener('change', function () { if (agree.checked) $('.field__err--agree', form).classList.remove('is-on'); });
  });

  /* ---------- Окна (dialog): открыть / закрыть ---------- */
  function setupDialog(dlg, onClose) {
    var cleanup = function () { document.documentElement.classList.remove('modal-open'); if (onClose) onClose(); };
    var close = function () {
      dlg.classList.add('is-closing');
      setTimeout(function () { dlg.classList.remove('is-closing'); if (dlg.open) dlg.close(); cleanup(); }, reduce ? 0 : 220);
    };
    dlg.addEventListener('click', function (e) { if (e.target === dlg) close(); });
    dlg.addEventListener('cancel', function (e) { e.preventDefault(); close(); });
    return { open: function () { document.documentElement.classList.add('modal-open'); dlg.showModal(); }, close: close };
  }

  /* ---------- Окно «Оставить заявку» ---------- */
  var join = $('#join');
  if (join && join.showModal) {
    var jForm = $('form', join), jT = $('#join-t'), jTitle = jT.innerHTML;
    var jS = $('.cform__s', join), jSub = jS ? jS.innerHTML : '';
    var J = setupDialog(join, function () { if (jForm.classList.contains('is-sent')) resetForm(jForm); });
    $$('.js-join').forEach(function (b) {
      b.addEventListener('click', function () {
        // Отклик на вакансию (data-join-job="Название"): без выбора тренировки, в окне и в заявке — название вакансии
        var job = b.dataset.joinJob || '';
        var review = 'joinReview' in b.dataset; // «Оставить отзыв»: поле для текста вместо выбора тренировки
        join.classList.toggle('is-job', !!job);
        join.classList.toggle('is-review', review);
        var goTxt = $('.cform__go', jForm); goTxt = goTxt && [].filter.call(goTxt.childNodes, function (n) { return n.nodeType === 3 && n.textContent.trim(); })[0];
        if (goTxt) { if (!goTxt.k2orig) goTxt.k2orig = goTxt.textContent; goTxt.textContent = review ? 'Отправить отзыв' : goTxt.k2orig; }
        jT.innerHTML = b.dataset.joinTitle || jTitle;
        if (jS) jS.innerHTML = job ? 'Вакансия: <b class="cform__job"></b><br>Оставьте телефон — перезвоним и расскажем подробнее' : review ? 'Расскажите, как вам у нас. Оставьте телефон — если нужно, администратор ответит' : jSub;
        if (job) $('.cform__job', join).textContent = job;
        var what = $('[name="what"]', join); if (what) what.value = job ? 'Отклик на вакансию: ' + job : review ? 'Отзыв' : jT.textContent; // в заявке видно, откуда её отправили
        var t = !job && !review && b.dataset.joinTopic && $('[name="topic"][value="' + b.dataset.joinTopic + '"]', join);
        if (t) t.checked = true;
        J.open();
      });
    });
    $$('.js-join-close', join).forEach(function (b) { b.addEventListener('click', J.close); });
    jForm.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!validate(jForm)) return;
      var who = $('[name="name"]', jForm).value.trim();
      send(jForm, function () { showDone(jForm, who + (join.classList.contains('is-review') ? ', спасибо за отзыв! Нам важно каждое мнение.' : join.classList.contains('is-job') ?', спасибо за отклик! Перезвоним и расскажем о вакансии.' : ', спасибо! Перезвоним в рабочее время и поможем выбрать формат.')); });
    });
  }

  /* ---------- Тренер: клик по карточке (или Enter / пробел) — окно с описанием ----------
     Описание — скрытый блок .lp-coach__bio внутри карточки; на время показа его содержимое переезжает в окно (кнопки сохраняют обработчики) */
  var coachCards = $$('.js-coach');
  if (coachCards.length && window.HTMLDialogElement) {
    var cm = document.createElement('dialog');
    cm.className = 'modal cm'; cm.id = 'coach'; cm.setAttribute('aria-labelledby', 'cm-n');
    cm.innerHTML = '<div class="modal__card"><div class="modal__img cm__img"><img alt=""></div><div class="cm__body">' +
      '<button class="modal__x cm__x" type="button" aria-label="Закрыть"><svg class="ico" viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18"/></svg></button>' +
      '<span class="cm__r"></span><h3 class="d cm__n" id="cm-n"></h3><p class="cm__q"></p><div class="cm__slot"></div></div></div>';
    document.body.appendChild(cm);
    var cmSlot = $('.cm__slot', cm), cmFrom = null;
    var cmBack = function () { if (!cmFrom) return; while (cmSlot.firstChild) cmFrom.appendChild(cmSlot.firstChild); cmFrom = null; };
    var CM = setupDialog(cm, cmBack);
    cm.addEventListener('close', cmBack);
    $('.cm__x', cm).addEventListener('click', CM.close);
    // «Записаться к тренеру»: окно тренера закрываем сразу, дальше открывается обычная заявка
    cmSlot.addEventListener('click', function (e) { if (e.target.closest('.js-join')) cm.close(); }, true);
    var cmOpen = function (card) {
      cmBack();
      var im = $('.lp-coach__img img', card), name = $('.lp-coach__n', card).textContent;
      $('.cm__img img', cm).src = im ? im.getAttribute('src') : '';
      $('.cm__n', cm).textContent = name;
      $('.cm__r', cm).textContent = $('.lp-coach__r', card).textContent;
      $('.cm__q', cm).textContent = $('.lp-coach__q', card).textContent;
      cmFrom = $('.lp-coach__bio', card);
      if (cmFrom) while (cmFrom.firstChild) cmSlot.appendChild(cmFrom.firstChild);
      var go = $('.js-join', cmSlot); if (go) go.dataset.joinTitle = 'Запись к тренеру: ' + name;
      CM.open();
      $('.cm__body', cm).scrollTop = 0;
    };
    coachCards.forEach(function (c) {
      c.addEventListener('click', function () { cmOpen(c); });
      c.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); cmOpen(c); } });
    });
  }

  /* ---------- Окно «Где оставить отзыв» (страница «Отзывы»): Яндекс Карты, 2ГИС, Google ---------- */
  var rv = $('#rv');
  if (rv && rv.showModal) {
    var RVD = setupDialog(rv);
    $$('.js-rv').forEach(function (b) { b.addEventListener('click', RVD.open); });
    $('.rv__x', rv).addEventListener('click', RVD.close);
    $$('.rv__i', rv).forEach(function (a) { a.addEventListener('click', function () { RVD.close(); }); });
  }

  /* ---------- Форма заявки в блоке «Нужно связаться с нами?» ---------- */
  $$('form.cform').forEach(function (form) {
    if (form.closest('dialog') || form.hasAttribute('data-own')) return;
    var seg = $('.seg', form);
    if (seg) $$('input', seg).forEach(function (inp, i) { inp.addEventListener('change', function () { seg.style.setProperty('--i', i); }); });
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!validate(form)) return;
      var via = $('[name="via"]:checked', form);
      var how = { call: 'Перезвоним', tg: 'Напишем в\u00a0Telegram', max: 'Напишем в\u00a0Max', wa: 'Напишем в\u00a0WhatsApp' }[via ? via.value : 'call'];
      send(form, function () { showDone(form, $('[name="name"]', form).value.trim() + ', спасибо! ' + how + ' в\u00a0рабочее время\u00a0— подберём тренировку.'); });
    });
    var again = $('.js-again', form);
    if (again) again.addEventListener('click', function () { resetForm(form); $('[name="name"]', form).focus(); });
  });

  /* ---------- ЕДИНАЯ форма бронирования с калькулятором ----------
     Цены — data-атрибуты у #book (в MODX — из прайса): data-price-group, data-price-group-kid, data-price-personal, data-price-personal-kid.
     Пусто — показываем [____] ₽. Оплата: после проверки — переход в банк (подключит разработчик). */
  var book = $('#book');
  if (book && book.showModal) {
    var bForm = $('form', book);
    var LIMIT = { group: { min: 1, max: 8, t: 'В\u00a0группе\u00a0— до\u00a08\u00a0человек' }, personal: { min: 1, max: 3, t: 'Персонально\u00a0— от\u00a01 до\u00a03\u00a0участников' } };
    var cnt = { adults: 1, kids: 0 };
    var price = function (k) { var v = book.dataset[k]; return v ? +v : null; };
    var rub = function (n) { return n === null ? '[____]&nbsp;₽' : n.toLocaleString('ru-RU') + '&nbsp;₽'; };
    var type = function () { return $('[name="type"]:checked', bForm).value; };
    var recalc = function () {
      var t = type(), L = LIMIT[t], total = cnt.adults + cnt.kids;
      // держим участников в пределах формата
      while (total > L.max) { if (cnt.kids > 0) cnt.kids--; else cnt.adults--; total = cnt.adults + cnt.kids; }
      if (total < L.min) { cnt.adults = L.min; total = cnt.adults + cnt.kids; }
      $$('.book__count', bForm).forEach(function (row) {
        var k = row.dataset.k, v = cnt[k];
        $('.step__v', row).textContent = v;
        $('[data-d="-1"]', row).disabled = k === 'adults' ? (v <= 0 || total <= L.min) : v <= 0;
        $('[data-d="1"]', row).disabled = total >= L.max;
      });
      $('.book__limit', bForm).textContent = L.t + (cnt.kids ? ' · для\u00a0детей\u00a0— детская пробная тренировка с\u00a0тренером' : '');
      var pA = price(t === 'group' ? 'priceGroup' : 'pricePersonal'), pK = price(t === 'group' ? 'priceGroupKid' : 'pricePersonalKid');
      var rows = '', sum = 0, known = true;
      var label = t === 'group' ? 'Пробная в\u00a0группе' : 'Персональная пробная';
      if (cnt.adults) { rows += '<div><span>' + label + ' · взрослые × ' + cnt.adults + '</span><span>' + (pA === null ? '[____]&nbsp;₽' : rub(pA * cnt.adults)) + '</span></div>'; if (pA === null) known = false; else sum += pA * cnt.adults; }
      if (cnt.kids) { rows += '<div><span>' + label + ' · дети × ' + cnt.kids + '</span><span>' + (pK === null ? '[____]&nbsp;₽' : rub(pK * cnt.kids)) + '</span></div>'; if (pK === null) known = false; else sum += pK * cnt.kids; }
      $('.book__rows', bForm).innerHTML = rows;
      $('.book__total-v', bForm).innerHTML = known ? rub(sum) : '[____]&nbsp;₽';
    };
    $$('.step__b', bForm).forEach(function (b) {
      b.addEventListener('click', function () { var k = b.closest('.book__count').dataset.k; cnt[k] = Math.max(0, cnt[k] + +b.dataset.d); recalc(); });
    });
    $$('[name="type"]', bForm).forEach(function (r) { r.addEventListener('change', recalc); });
    var dateIn = $('[name="date"]', bForm);
    if (dateIn) dateIn.min = new Date().toISOString().slice(0, 10);
    var B = setupDialog(book, function () { if (bForm.classList.contains('is-sent')) { resetForm(bForm); cnt = { adults: 1, kids: 0 }; recalc(); } });
    $$('.js-book').forEach(function (b) {
      b.addEventListener('click', function () {
        if (b.dataset.bookType) { var r = $('[name="type"][value="' + b.dataset.bookType + '"]', bForm); if (r) r.checked = true; }
        // сколько взрослых и детей сразу: data-book-adults / data-book-kids (детская и семейная пробная)
        if (b.dataset.bookAdults || b.dataset.bookKids) cnt = { adults: +(b.dataset.bookAdults || 0), kids: +(b.dataset.bookKids || 0) };
        recalc(); B.open();
      });
    });
    $$('.js-book-close', book).forEach(function (b) { b.addEventListener('click', B.close); });
    bForm.addEventListener('submit', function (e) {
      e.preventDefault();
      // Пробная тренировка → корзина: взрослые и дети — отдельными строками (у них разная цена); контакты и оплата — в корзине
      if (!window.K2Cart) return;
      var t = type(), fmt = t === 'group' ? 'В\u00a0группе' : 'Персонально';
      var dv = $('[name="date"]', bForm).value, tv = $('[name="time"]', bForm).value;
      var params = ['Формат: ' + fmt, 'Дата: ' + (dv ? dv.split('-').reverse().join('.') : 'подберём с\u00a0администратором'), 'Время: ' + (tv || 'любое')];
      var name = t === 'group' ? 'Пробная тренировка в\u00a0группе' : 'Персональная пробная тренировка';
      var page = location.pathname.split('/').pop() || 'pervyj-raz.html';
      var pA = price(t === 'group' ? 'priceGroup' : 'pricePersonal'), pK = price(t === 'group' ? 'priceGroupKid' : 'pricePersonalKid');
      if (cnt.adults) K2Cart.add({ id: 'trial-' + t, kind: 'training', name: name, img: 'k2-first-3.jpg', url: page, params: params.concat('Взрослые'), unit: 'за участника', price: pA || 0, max: LIMIT[t].max }, cnt.adults);
      if (cnt.kids) K2Cart.add({ id: 'trial-' + t + '-kid', kind: 'training', name: name + ' (ребёнок)', img: 'k2-10.jpg', url: page, params: params.concat('Дети 5–16 лет'), unit: 'за ребёнка', price: pK || 0, max: LIMIT[t].max }, cnt.kids);
      B.close();
      window.location.href = 'korzina.html';
    });
    recalc();
  }

  /* ---------- Шаблоны «Товар» / «Мероприятие»: правая карточка липкая и всегда видна целиком — прилипает верхним краем
     сразу под шапкой (шапка прячется при листании вниз — карточка поднимается к верху экрана).
     Не помещается на невысоком экране — компактный вид (.is-compact: афиша-миниатюра рядом с названием), затем .is-tight (без фактов), .is-min (без мессенджеров) ---------- */
  var itpSide = $('.itp__side');
  if (itpSide) {
    var itpWide = window.matchMedia('(min-width: 1041px)'), itpHd = $('#hdr');
    var hdH = function () { return itpHd && !itpHd.classList.contains('is-hidden') ? itpHd.offsetHeight : 0; };
    var itpTop = function () { if (itpWide.matches) itpSide.style.top = (hdH() + 16) + 'px'; };
    var itpFit = function () {
      itpSide.classList.remove('is-compact', 'is-tight', 'is-min');
      if (!itpWide.matches) { itpSide.style.top = ''; return; }
      var avail = window.innerHeight - (itpHd ? itpHd.offsetHeight : 64) - 32;  // с учётом показанной шапки
      ['is-compact', 'is-tight', 'is-min'].forEach(function (c) { if (itpSide.offsetHeight > avail) itpSide.classList.add(c); });
      itpTop();
    };
    itpFit(); window.addEventListener('resize', itpFit); window.addEventListener('load', itpFit);
    if (itpHd && window.MutationObserver) new MutationObserver(itpTop).observe(itpHd, { attributes: true, attributeFilter: ['class'] });
  }

  /* ---------- Форма «Покупка услуги» / «Запись на мероприятие» (шаблоны «Товар» и «Мероприятие») ----------
     Данные берутся из data-атрибутов .itp: kind (product|event), name, img, meta (дата или цена), price, who (adults|kids), max.
     Покупка: взрослые × цена, ФИО, телефон, почта → «Оплатить» (переход в банк подключит разработчик). Запись: дети или взрослые, имя, телефон, почта. */
  var order = $('#order'), itp = $('.itp');
  if (order && order.showModal && itp) {
    var oForm = $('form', order), D = itp.dataset, buy = D.kind === 'product', kids = D.who === 'kids', MAX = +D.max || 6, n = 1;
    var rubO = function (v) { return v.toLocaleString('ru-RU') + ' ₽'; };
    $('.cform__t', order).textContent = buy ? 'Покупка услуги' : 'Запись на мероприятие';
    $('.order__name', order).textContent = D.name;
    $('.order__meta', order).textContent = D.meta;
    $('.order__img', order).src = 'assets/img/' + D.img;
    $('[name="item"]', oForm).value = D.name; $('[name="when"]', oForm).value = D.meta;
    $('.order__leg', order).textContent = buy ? 'Количество' : 'Кто придёт';
    $('.order__who', order).textContent = kids ? 'Дети' : 'Взрослые';
    $('.order__age', order).textContent = kids ? '5⁠–⁠16 лет' : 'от 16 лет';
    $('.order__nl', order).textContent = buy ? 'ФИО' : (kids ? 'Имя родителя' : 'Имя');
    $('.cform__go', order).textContent = buy ? 'Оплатить' : 'Записаться';
    $('.order__note', order).textContent = buy ? 'Оплата картой через банк. Чек придёт на почту.' : 'Дату и время подставили из описания мероприятия. Запись подтвердим звонком.';
    $('.order__sum', order).hidden = !buy;
    var oRecalc = function () {
      $('.step__v', oForm).textContent = n; $('[name="count"]', oForm).value = n;
      $('[data-d="-1"]', oForm).disabled = n <= 1; $('[data-d="1"]', oForm).disabled = n >= MAX;
      if (buy) $('.book__total-v', oForm).textContent = rubO((+D.price || 0) * n);
    };
    $$('.step__b', oForm).forEach(function (b) { b.addEventListener('click', function () { n = clamp(n + +b.dataset.d, 1, MAX); oRecalc(); }); });
    var mail = $('[name="email"]', oForm), okMail = function () { return /^\S+@\S+\.\S+$/.test(mail.value.trim()); };
    mail.addEventListener('input', function () { if (okMail()) mail.parentNode.classList.remove('is-bad'); });
    var O = setupDialog(order, function () { if (oForm.classList.contains('is-sent')) { resetForm(oForm); n = 1; oRecalc(); } });
    $$('.js-order').forEach(function (b) { b.addEventListener('click', function () { oRecalc(); O.open(); }); });
    $$('.js-order-close', order).forEach(function (b) { b.addEventListener('click', O.close); });
    oForm.addEventListener('submit', function (e) {
      e.preventDefault();
      var ok = validate(oForm), m = okMail();
      mail.parentNode.classList.toggle('is-bad', !m);
      if (!ok) return;
      if (!m) { mail.focus(); return; }
      var who = $('[name="name"]', oForm).value.trim().split(' ')[0];
      // Здесь разработчик: отправить заявку в CRM; для покупки — перейти на страницу оплаты банка (сумма = цена × количество)
      send(oForm, function () {
        $('.order__done-t', order).textContent = buy ? 'Почти готово' : 'Вы записаны';
        showDone(oForm, buy ? who + ', переходим к оплате: ' + D.name + ' × ' + n + ', ' + rubO((+D.price || 0) * n) + '. Демо: переход в банк подключит разработчик.'
                            : who + ', записали: ' + D.name + ', ' + D.meta + ', участников: ' + n + '. Подтвердим звонком.');
      });
    });
    oRecalc();
  }

  /* ---------- Связь: статус «открыто/закрыто», копирование, «прогулка» от метро ---------- */
  var status = $('.status');
  if (status) {
    var toMin = function (t) { var x = t.split(':'); return +x[0] * 60 + +x[1]; };
    var updateStatus = function () {
      var o = status.dataset.open, c = status.dataset.close;
      var now = toMin(new Date().toLocaleTimeString('ru-RU', { timeZone: 'Europe/Moscow', hour: '2-digit', minute: '2-digit', hour12: false }));
      var isOpen = now >= toMin(o) && now < toMin(c);
      status.classList.toggle('is-open', isOpen);
      $('.status__t', status).innerHTML = isOpen ? 'Сейчас открыто · до <b>' + c + '</b>' : 'Сейчас закрыто · откроемся в <b>' + o.replace(/^0/, '') + '</b>';
    };
    updateStatus(); setInterval(updateStatus, 60000);
  }
  $$('.copy').forEach(function (btn) {
    var label = $('span', btn), base = label.textContent;
    btn.addEventListener('click', function () {
      var done = function () { btn.classList.add('is-done'); label.textContent = 'Скопировано'; setTimeout(function () { btn.classList.remove('is-done'); label.textContent = base; }, 1600); };
      if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(btn.dataset.copy).then(done, done);
      else { var t = document.createElement('textarea'); t.value = btn.dataset.copy; document.body.appendChild(t); t.select(); try { document.execCommand('copy'); } catch (err) {} t.remove(); done(); }
    });
  });
  var route = $('.route');
  if (route) {
    var walk = $('#walk', route), minEl = $('.route__min', route), walking = false;
    var startWalk = function () {
      if (walking || reduce || !walk || !walk.beginElement) return;
      walking = true; route.classList.add('is-walking'); walk.beginElement();
      var t0 = performance.now();
      (function tick(t) {
        var k = Math.min(1, (t - t0) / 5000);
        minEl.textContent = Math.max(0, Math.ceil(7 * (1 - k)));
        if (k < 1) requestAnimationFrame(tick);
        else { minEl.textContent = '7'; setTimeout(function () { route.classList.remove('is-walking'); walking = false; }, 900); }
      })(t0);
    };
    new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) startWalk(); }); }, { threshold: 0.6 }).observe(route);
    route.addEventListener('mouseenter', startWalk);
    route.addEventListener('click', startWalk);
  }

  /* ---------- Сцена «60\u00a0минут»: таймер, полоса времени, фото и\u00a0шаги ----------
     Компьютер: блок закреплён, прокрутка ведёт минуты 0 → 60. Телефон и\u00a0«уменьшить движение»: шаги листаются сами, пока блок на\u00a0экране, и\u00a0по\u00a0нажатию */
  var hour = $('.lp-hour');
  if (hour) {
    var hSteps = $$('.lp-hour__steps li', hour), hPics = $$('.lp-hour__pics img', hour), hSegs = $$('.lp-hour__bar > span', hour);
    var hClock = $('.lp-hour__clock b', hour), hBadge = $('.lp-hour__badge span', hour), hTrack = $('.lp-hour__track', hour), hStage = $('.lp-hour__stage', hour);
    var hR = hSteps.map(function (li) { return [+li.dataset.from, +li.dataset.to]; });
    var hCur = -1, hMin = 0, hScroll = false, hTimer = null, hTween = 0, hTouched = false;
    var hSet = function (m) {
      hMin = m;
      hClock.textContent = (m < 9.5 ? '0' : '') + Math.round(m);
      hSegs.forEach(function (s, i) { s.style.setProperty('--hf', clamp((m - hR[i][0]) / (hR[i][1] - hR[i][0]), 0, 1)); });
      var k = 0; hR.forEach(function (r, i) { if (m > r[0] || (i === 0)) k = i; });
      if (k === hCur) return;
      hCur = k;
      hSteps.forEach(function (li, i) { li.classList.toggle('is-on', i === k); $('button', li).setAttribute('aria-expanded', String(i === k)); });
      hPics.forEach(function (im, i) { im.classList.toggle('is-on', i === k); });
      hBadge.textContent = 'Шаг 0' + (k + 1) + ' · ' + $('small', hSteps[k]).textContent;
    };
    // плавно «докрутить» минуты до нужной (телефон, нажатия)
    var hGo = function (to) {
      cancelAnimationFrame(hTween);
      var from = hMin, t0 = performance.now(), dur = reduce ? 0 : 900;
      (function tick(t) { var u = dur ? Math.min(1, (t - t0) / dur) : 1; hSet(from + (to - from) * (1 - Math.pow(1 - u, 3))); if (u < 1) hTween = requestAnimationFrame(tick); })(t0);
    };
    var hMetrics = function () { var top = hTrack.getBoundingClientRect().top + scrollY, stickTop = parseFloat(getComputedStyle(hStage).top) || 0; return { top: top - stickTop, len: hTrack.offsetHeight - hStage.offsetHeight }; };
    var hOnScroll = function () {
      if (!hScroll) return;
      var M = hMetrics();
      hSet(clamp((scrollY - M.top) / M.len, 0, 1) * (+hour.dataset.total || 60));
    };
    var hList = $('.lp-hour__steps', hour), hSwipe = false;
    var hMode = function () {
      hScroll = !reduce && matchMedia('(min-width: 1041px) and (min-height: 640px)').matches;
      // телефон: шаги\u00a0— карточки, которые листаются пальцем; таймер и\u00a0полоса показывают текущую
      hSwipe = !hScroll && matchMedia('(max-width: 767px)').matches;
      hour.classList.toggle('is-scroll', hScroll);
      hour.classList.toggle('is-swipe', hSwipe);
      if (hScroll || hSwipe) { clearInterval(hTimer); hTimer = null; }
      if (hScroll) hOnScroll();
      if (hSwipe && hMin < 1) hSet(hR[0][1]); // на телефоне сразу видно первый шаг целиком: 10 минут
    };
    var hSwipeTick = false;
    hList.addEventListener('scroll', function () {
      if (!hSwipe || hSwipeTick) return; hSwipeTick = true;
      requestAnimationFrame(function () {
        var w = hSteps[0].offsetWidth + 12, k = clamp(Math.round(hList.scrollLeft / w), 0, hR.length - 1);
        if (k !== hCur) hGo(hR[k][1]);
        hSwipeTick = false;
      });
    }, { passive: true });
    // нажатие на шаг или отрезок полосы
    var hPick = function (i) {
      hTouched = true; clearInterval(hTimer); hTimer = null;
      if (hScroll) { var M = hMetrics(); scrollTo({ top: M.top + M.len * ((hR[i][0] + hR[i][1]) / 2) / 60, behavior: reduce ? 'auto' : 'smooth' }); }
      else if (hSwipe) hList.scrollTo({ left: hSteps[i].offsetLeft - hList.offsetLeft - 16, behavior: reduce ? 'auto' : 'smooth' });
      else hGo(hR[i][1]);
    };
    hSteps.forEach(function (li, i) { $('button', li).addEventListener('click', function () { hPick(i); }); });
    hSegs.forEach(function (s, i) { s.addEventListener('click', function () { hPick(i); }); });
    // телефон: пока блок на экране — шаги сами идут по кругу, после нажатия перестают
    new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (hScroll || hSwipe || hTouched || reduce) return;
        if (e.isIntersecting && !hTimer) {
          if (hMin < 1) hGo(hR[0][1]);
          hTimer = setInterval(function () { var n = (hCur + 1) % hR.length; if (n === 0) hSet(0); hGo(hR[n][1]); }, 3600);
        } else if (!e.isIntersecting) { clearInterval(hTimer); hTimer = null; }
      });
    }, { threshold: 0.4 }).observe(hour);
    var hTick = false;
    window.addEventListener('scroll', function () { if (hScroll && !hTick) { hTick = true; requestAnimationFrame(function () { hOnScroll(); hTick = false; }); } }, { passive: true });
    window.addEventListener('resize', hMode);
    hMode(); hSet(hMin);
  }

  /* ---------- «Почему К2»: параллакс фото, шкала 0 → 13 м по прокрутке, цифры набегают от нуля ---------- */
  var why = $('.lp-why2');
  if (why) {
    var wVal = $('.lp-why2__dot b', why), wTick = false;
    var wFrame = function () {
      var r = why.getBoundingClientRect(), vh = innerHeight;
      if (r.bottom < 0 || r.top > vh) { wTick = false; return; }
      var p = clamp((vh - r.top) / (vh + r.height), 0, 1);
      why.style.setProperty('--p', p.toFixed(4));
      var m = clamp((vh * 0.85 - r.top) / (r.height * 0.8), 0, 1) * 13;
      why.style.setProperty('--m', m.toFixed(2));
      if (wVal) wVal.textContent = m.toFixed(1);  // шкалы может не быть (детская секция)
      wTick = false;
    };
    if (!reduce) {
      window.addEventListener('scroll', function () { if (!wTick) { wTick = true; requestAnimationFrame(wFrame); } }, { passive: true });
      wFrame();
    }
    var counters = $$('[data-count]', why);
    if (!reduce && 'IntersectionObserver' in window) {
      counters.forEach(function (c) { c.textContent = '0'; });
      var cio = new IntersectionObserver(function (es) {
        es.forEach(function (e) {
          if (!e.isIntersecting) return;
          cio.unobserve(e.target);
          var el = e.target, to = +el.dataset.count, t0 = performance.now(), dur = to > 100 ? 1800 : 1300;
          (function tick(t) { var u = Math.min(1, (t - t0) / dur); el.textContent = Math.round(to * (1 - Math.pow(1 - u, 4))); if (u < 1) requestAnimationFrame(tick); })(t0);
        });
      }, { threshold: 0.6 });
      counters.forEach(function (c) { cio.observe(c); });
    }
  }

  /* ---------- Словарик (подсказки к терминам) ---------- */
  var GLOSSARY = {
    bould: ['Боулдеринг', 'Лазание по\u00a0невысоким трассам без\u00a0верёвки\u00a0— над\u00a0мягкими матами.'],
    lead: ['Трудность', 'Лазание по\u00a0высоким трассам со\u00a0страховкой верёвкой. У\u00a0нас стены 13\u00a0метров.'],
    shoes: ['Скальники', 'Специальная обувь для\u00a0лазания с\u00a0цепкой резиновой подошвой. Выдаём на\u00a0месте.'],
    chalk: ['Магнезия', 'Порошок для\u00a0рук: сушит ладони, чтобы они не\u00a0скользили по\u00a0зацепам.']
  };
  var tip = $('#tip');
  if (tip) {
    var tipFor = null;
    var showTip = function (el) {
      var g = GLOSSARY[el.dataset.term]; if (!g) return;
      tipFor = el; $('.tip__t', tip).textContent = g[0]; $('.tip__d', tip).textContent = g[1];
      var r = el.getBoundingClientRect(); tip.classList.add('is-on');
      var x = clamp(r.left + r.width / 2 - tip.offsetWidth / 2, 12, innerWidth - tip.offsetWidth - 12), y = r.top - tip.offsetHeight - 10;
      if (y < 12) y = r.bottom + 10;
      tip.style.left = x + 'px'; tip.style.top = y + 'px';
    };
    var hideTip = function () { tipFor = null; tip.classList.remove('is-on'); };
    $$('.term').forEach(function (el) {
      el.setAttribute('tabindex', '0');
      el.addEventListener('mouseenter', function () { showTip(el); });
      el.addEventListener('mouseleave', hideTip);
      el.addEventListener('focus', function () { showTip(el); });
      el.addEventListener('blur', hideTip);
      el.addEventListener('click', function (e) { e.preventDefault(); tipFor === el ? hideTip() : showTip(el); });
    });
    window.addEventListener('scroll', function () { if (tipFor) hideTip(); }, { passive: true });
  }

  /* ---------- Переключатели: [data-tabs="имя"] показывает [data-tab-of="имя"] с нужным data-t; ссылка [data-tab-go="имя:значение"] выбирает вкладку ---------- */
  function tabSelect(name, t) {
    $$('[data-tabs="' + name + '"] [data-t]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.t === t)); });
    $$('[data-tab-of="' + name + '"]').forEach(function (el) { el.hidden = el.dataset.t !== t; });
  }
  $$('[data-tabs]').forEach(function (box) {
    $$('[data-t]', box).forEach(function (b) { b.addEventListener('click', function () { tabSelect(box.dataset.tabs, b.dataset.t); }); });
  });
  $$('[data-tab-go]').forEach(function (a) {
    a.addEventListener('click', function () { var p = a.dataset.tabGo.split(':'); tabSelect(p[0], p[1]); });
  });

  /* ---------- Абонементы: карточка переворачивается по\u00a0клику ---------- */
  $$('.abo').forEach(function (c) {
    c.addEventListener('click', function () { c.setAttribute('aria-pressed', String(c.getAttribute('aria-pressed') !== 'true')); });
  });

  /* ---------- Лента видео (.shorts): стрелки в заголовке секции и перетаскивание мышью ---------- */
  $$('.videos').forEach(function (sec) {
    var sh = $('.shorts', sec); if (!sh) return;
    var step = function () { var s = $('.short', sh); return s ? s.offsetWidth + 16 : 300; };
    var prev = $('.js-prev', sec), next = $('.js-next', sec);
    if (prev) prev.addEventListener('click', function () { sh.scrollBy({ left: -step(), behavior: 'smooth' }); });
    if (next) next.addEventListener('click', function () { sh.scrollBy({ left: step(), behavior: 'smooth' }); });
    var down = false, moved = false, sx = 0, sl = 0;
    sh.addEventListener('pointerdown', function (e) { if (e.pointerType !== 'mouse') return; down = true; moved = false; sx = e.clientX; sl = sh.scrollLeft; });
    window.addEventListener('pointermove', function (e) {
      if (!down) return; var dx = e.clientX - sx;
      if (Math.abs(dx) > 5) { moved = true; sh.classList.add('is-drag'); }
      sh.scrollLeft = sl - dx;
    });
    window.addEventListener('pointerup', function () { if (!down) return; down = false; setTimeout(function () { sh.classList.remove('is-drag'); }, 0); });
    sh.addEventListener('click', function (e) { if (moved) { e.preventDefault(); moved = false; } }, true);
  });

  /* ---------- Вакансии: ссылка vakansii.html#slug сразу открывает подробное описание ---------- */
  var jobHash = location.hash && document.getElementById(decodeURIComponent(location.hash.slice(1)));
  if (jobHash && jobHash.classList.contains('job')) { var jm = $('.job__more', jobHash); if (jm) jm.open = true; }

  /* ---------- Документы: старая ссылка dokumenty.html#oferta открывает страницу документа ---------- */
  var dcxOpen = function () {
    var el = location.hash && document.getElementById(decodeURIComponent(location.hash.slice(1)));
    if (el && el.classList.contains('dcx') && el.tagName === 'DETAILS') { el.open = true; setTimeout(function () { el.scrollIntoView({ block: 'start' }); }, 60); }
    if (el && el.classList.contains('dcx') && el.tagName === 'A') location.replace(el.href); // документ теперь — отдельная страница
  };
  if ($('.dcx')) {
    dcxOpen(); window.addEventListener('hashchange', dcxOpen);
    // при открытии страницы сразу с #документом браузер сбивает прокрутку загрузкой — докручиваем после load
    window.addEventListener('load', function () { var el = location.hash && document.getElementById(decodeURIComponent(location.hash.slice(1))); if (el && el.classList.contains('dcx')) setTimeout(function () { el.scrollIntoView({ block: 'start', behavior: 'auto' }); }, 120); });
  }

  /* ---------- Архив мероприятий: на странице один ряд сетки, ниже — переключатели страниц ---------- */
  $$('.arc-grid').forEach(function (grid) {
    var items = $$('.arc', grid), pager = grid.nextElementSibling;
    if (!pager || !pager.classList.contains('arc-pager')) return;
    var pagesBox = $('.arc-pager__pages', pager), prev = $('.arc-pager__prev', pager), next = $('.arc-pager__next', pager);
    var per = 4, page = 0;
    var cols = function () { return getComputedStyle(grid).gridTemplateColumns.split(' ').filter(Boolean).length || 1; };
    var total = function () { return Math.max(1, Math.ceil(items.length / per)); };
    function render(anim) {
      items.forEach(function (it, i) {
        var on = i >= page * per && i < (page + 1) * per;
        it.hidden = !on;
        it.classList.toggle('is-on', on && anim);
      });
      var n = total();
      pager.hidden = n < 2;
      pagesBox.innerHTML = '';
      for (var p = 0; p < n; p++) {
        var b = document.createElement('button'); b.type = 'button'; b.textContent = p + 1;
        b.setAttribute('aria-label', 'Страница ' + (p + 1));
        if (p === page) b.setAttribute('aria-current', 'page');
        b.addEventListener('click', (function (q) { return function () { go(q); }; })(p));
        pagesBox.appendChild(b);
      }
      prev.disabled = page === 0; next.disabled = page >= n - 1;
    }
    function go(p) { page = Math.max(0, Math.min(total() - 1, p)); render(true); }
    function fit() { var first = page * per; per = cols(); page = Math.floor(first / per); render(false); }
    prev.addEventListener('click', function () { go(page - 1); });
    next.addEventListener('click', function () { go(page + 1); });
    var t; window.addEventListener('resize', function () { clearTimeout(t); t = setTimeout(function () { if (cols() !== per) fit(); }, 150); });
    fit();
  });

  /* ---------- Галерея: одно окно #lb на странице, галерей может быть несколько.
     Группа — .lp-gal (сетка фото) или любой контейнер с data-lb (например, плитки «Удобства»).
     Пункт — .lp-gal__i или [data-lb-i]; большое фото — data-full (если нет — src превью), подпись — data-cap или alt ---------- */
  var lb = $('#lb'), groups = $$('.lp-gal, [data-lb]');
  if (lb && lb.showModal && groups.length) {
    var gImg = $('.lb__img', lb), gCap = $('.lb__cap', lb), gCount = $('.lb__count', lb), gThumbs = $('.lb__thumbs', lb);
    var gBtns = [], gItems = [], gTh = [], gCur = 0;
    var itemOf = function (b) {
      var im = $('img', b);
      return { src: b.dataset.full || (im && im.getAttribute('src')) || '', alt: b.dataset.cap || (im && im.getAttribute('alt')) || '' };
    };
    // в галерее с переключателями листаем только фото выбранной вкладки
    var gVis = function () { return gItems.map(function (_, i) { return i; }).filter(function (i) { return !gBtns[i].hidden; }); };
    var gShow = function (i) {
      gCur = (i + gItems.length) % gItems.length;
      gImg.classList.remove('is-in'); void gImg.offsetWidth; gImg.src = gItems[gCur].src; gImg.alt = gItems[gCur].alt; gImg.classList.add('is-in');
      var act = gVis();
      gCap.textContent = gItems[gCur].alt; gCount.textContent = (act.indexOf(gCur) + 1) + ' / ' + act.length;
      gTh.forEach(function (t, n) { t.setAttribute('aria-current', String(n === gCur)); t.hidden = act.indexOf(n) < 0; });
    };
    var gStep = function (d) { var a = gVis(); gShow(a[(a.indexOf(gCur) + d + a.length) % a.length]); };
    var gOpen = function (btns, i) {
      gBtns = btns; gItems = btns.map(itemOf); gThumbs.innerHTML = '';
      gItems.forEach(function (it, n) {
        var t = document.createElement('button'); t.type = 'button'; t.className = 'lb__th'; t.setAttribute('aria-label', 'Фото ' + (n + 1));
        t.innerHTML = '<img src="' + it.src + '" alt="" loading="lazy">'; t.addEventListener('click', function () { gShow(n); }); gThumbs.appendChild(t);
      });
      gTh = $$('.lb__th', gThumbs);
      document.documentElement.classList.add('lb-open'); lb.showModal(); gShow(i);
    };
    groups.forEach(function (g) {
      var btns = $$('.lp-gal__i, [data-lb-i]', g);
      btns.forEach(function (b, i) { b.addEventListener('click', function () { gOpen(btns, i); }); });
    });
    var gClose = function () { if (lb.open) lb.close(); document.documentElement.classList.remove('lb-open'); };
    $('.lb__x', lb).addEventListener('click', gClose);
    $('.lb__nav--prev', lb).addEventListener('click', function () { gStep(-1); });
    $('.lb__nav--next', lb).addEventListener('click', function () { gStep(1); });
    lb.addEventListener('keydown', function (e) { if (e.key === 'ArrowRight') gStep(1); if (e.key === 'ArrowLeft') gStep(-1); });
    lb.addEventListener('close', function () { document.documentElement.classList.remove('lb-open'); });
    lb.addEventListener('click', function (e) { if (e.target === lb || e.target.classList.contains('lb__stage') || e.target.classList.contains('lb__fig')) gClose(); });
    var sx = null;
    lb.addEventListener('touchstart', function (e) { sx = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener('touchend', function (e) { if (sx === null) return; var dx = e.changedTouches[0].clientX - sx; sx = null; if (Math.abs(dx) > 50) gStep(dx < 0 ? 1 : -1); });
    $$('.js-gal-more').forEach(function (more) {
      var gal = more.closest('.lp-center') ? more.closest('.lp-center').previousElementSibling : $('.lp-gal');
      if (!gal) return;
      more.addEventListener('click', function () {
        var all = gal.classList.toggle('is-all');
        more.textContent = all ? 'Свернуть' : 'Показать ещё';
        more.setAttribute('aria-expanded', String(all));
      });
    });
  }

  /* ---------- Видео: если указан data-video — встраиваем; иначе пометка «Видео скоро» ---------- */
  $$('.lp-video').forEach(function (v) {
    var play = $('.lp-video__play', v);
    play.addEventListener('click', function () {
      var src = v.dataset.video;
      if (!src) { v.classList.remove('is-msg'); void v.offsetWidth; v.classList.add('is-msg'); return; }
      var el;
      if (/\.(mp4|webm)(\?|$)/.test(src)) { el = document.createElement('video'); el.src = src; el.controls = true; el.autoplay = true; el.playsInline = true; }
      else { el = document.createElement('iframe'); el.src = src + (src.indexOf('?') < 0 ? '?' : '&') + 'autoplay=1'; el.allow = 'autoplay; fullscreen; picture-in-picture'; el.allowFullscreen = true; el.title = 'Видеообзор пробной тренировки'; }
      v.innerHTML = ''; v.appendChild(el);
    });
  });

  /* ---------- Цены: закреплённое меню разделов прилипает под шапкой и подсвечивает текущий раздел ---------- */
  var pnav = $('.pnav');
  if (pnav) {
    var pHdr = $('#hdr'), pTick = false;
    var pLinks = $$('a[href^="#"]', pnav), pSecs = pLinks.map(function (a) { return document.getElementById(a.getAttribute('href').slice(1)); });
    var pFrame = function () {
      if (pHdr) pnav.style.setProperty('--pnav-top', (pHdr.classList.contains('is-hidden') ? 0 : pHdr.offsetHeight) + 'px');
      var line = innerHeight * 0.4, cur = -1;
      pSecs.forEach(function (sec, i) { if (sec && sec.getBoundingClientRect().top < line) cur = i; });
      pLinks.forEach(function (a, i) { if (i === cur) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current'); });
      pTick = false;
    };
    window.addEventListener('scroll', function () { if (!pTick) { pTick = true; requestAnimationFrame(pFrame); } }, { passive: true });
    window.addEventListener('resize', pFrame);
    if (pHdr) new MutationObserver(pFrame).observe(pHdr, { attributes: true, attributeFilter: ['class'] });
    pFrame();
  }

  /* ---------- Липкое меню разделов и\u00a0плавающая кнопка ---------- */
  var sub = $('.lp-sub'), hdr = $('#hdr'), fab = $('.lp-fab'), hero = $('.lp-hero');
  var links = sub ? $$('a', sub) : [];
  var subBtn = sub && $('.lp-sub__toggle', sub), subCur = sub && $('.lp-sub__cur', sub);
  if (subBtn) {
    var subSet = function (open) { sub.classList.toggle('is-open', open); subBtn.setAttribute('aria-expanded', String(open)); };
    subBtn.addEventListener('click', function () { subSet(!sub.classList.contains('is-open')); });
    links.forEach(function (a) { a.addEventListener('click', function () { subSet(false); }); });
    document.addEventListener('click', function (e) { if (!sub.contains(e.target)) subSet(false); });
  }
  var secs = links.map(function (a) { return document.getElementById(a.getAttribute('href').slice(1)); });
  var ticking = false;
  function frame() {
    // меню разделов прилипает под шапкой, когда шапка видна, и к самому верху, когда она спрятана
    if (sub && hdr) sub.style.setProperty('--lp-sub-top', (hdr.classList.contains('is-hidden') ? 0 : hdr.offsetHeight) + 'px');
    var cur = -1;
    secs.forEach(function (s, i) { if (s && s.getBoundingClientRect().top < innerHeight * 0.3) cur = i; });
    links.forEach(function (a, i) { a.classList.toggle('is-on', i === cur); });
    if (subCur) subCur.textContent = cur >= 0 ? links[cur].textContent.trim() : 'Разделы страницы';
    if (cur >= 0 && links[cur]) { var sc = links[cur].parentNode, l = links[cur]; if (l.offsetLeft < sc.scrollLeft || l.offsetLeft + l.offsetWidth > sc.scrollLeft + sc.clientWidth) sc.scrollTo({ left: l.offsetLeft - 16, behavior: reduce ? 'auto' : 'smooth' }); }
    if (fab && hero) {
      var foot = document.querySelector('.foot');
      // у подвала своя кнопка записи — плавающую прячем
      var own = ['formats', 'family', 'how'].some(function (id) { var el = document.getElementById(id); if (!el) return false; var r = el.getBoundingClientRect(); return r.top < innerHeight - 40 && r.bottom > innerHeight * 0.4; }); // там свои кнопки записи
      var on = hero.getBoundingClientRect().bottom < 0 && !own && !document.documentElement.classList.contains('modal-open') && !(foot && foot.getBoundingClientRect().top < innerHeight - 40);
      fab.classList.toggle('is-on', on); fab.setAttribute('aria-hidden', String(!on)); fab.tabIndex = on ? 0 : -1;
    }
    ticking = false;
  }
  window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(frame); } }, { passive: true });
  if (hdr) new MutationObserver(frame).observe(hdr, { attributes: true, attributeFilter: ['class'] });
  frame();
})();

/* Блоки-призывы («Уже занимались» и др.): надпись бежит по контуру кнопки (путь — скруглённый прямоугольник, пройденный дважды, чтобы текст шёл без шва) */
(function () {
  'use strict';
  var boxes = document.querySelectorAll('.lp-orbit');
  if (!boxes.length) return;
  var still = window.matchMedia('(prefers-reduced-motion: reduce)').matches, rings = [];
  Array.prototype.forEach.call(boxes, function (box, n) {
    var svg = box.querySelector('svg'), path = box.querySelector('path'), tp = box.querySelector('textPath');
    var id = 'orbitP' + n, R = { tp: tp, per: 0 };
    path.setAttribute('id', id); tp.setAttribute('href', '#' + id);
    var unit = tp.getAttribute('data-t');
    R.build = function () {
      var w = box.offsetWidth, h = box.offsetHeight, d = 9, r = (h - 2 * d) / 2, x0 = d + r, x1 = w - d - r;
      if (w < 40) return;
      svg.setAttribute('viewBox', '0 0 ' + w + ' ' + h);
      var loop = 'H' + x1 + 'A' + r + ' ' + r + ' 0 0 1 ' + x1 + ' ' + (h - d) + 'H' + x0 + 'A' + r + ' ' + r + ' 0 0 1 ' + x0 + ' ' + d;
      path.setAttribute('d', 'M' + x0 + ' ' + d + loop + loop);
      R.per = 2 * (x1 - x0) + 2 * Math.PI * r;
      tp.textContent = unit;
      var len = tp.getComputedTextLength() || 1;
      tp.textContent = new Array(Math.max(1, Math.round(R.per / len)) + 1).join(unit);
      tp.setAttribute('textLength', R.per); tp.setAttribute('lengthAdjust', 'spacing');
    };
    R.build(); rings.push(R);
  });
  var all = function () { rings.forEach(function (R) { R.build(); }); };
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(all);
  window.addEventListener('resize', all);
  if (still) return;
  var t0 = performance.now();
  (function tick(t) { rings.forEach(function (R) { if (R.per) R.tp.setAttribute('startOffset', ((t - t0) * 0.03) % R.per); }); requestAnimationFrame(tick); })(t0);
})();
