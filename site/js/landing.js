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
        p.textContent = 'Не получилось отправить заявку. Позвоните нам или попробуйте ещё раз.';
        go.insertAdjacentElement('afterend', p);
      })
      .then(function () { go.disabled = false; });
  }
  $$('form.cform').forEach(function (form) {
    var phone = $('[name="phone"]', form), name = $('[name="name"]', form), agree = $('[name="agree"]', form);
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
    var J = setupDialog(join, function () { if (jForm.classList.contains('is-sent')) resetForm(jForm); });
    $$('.js-join').forEach(function (b) {
      b.addEventListener('click', function () {
        jT.innerHTML = b.dataset.joinTitle || jTitle;
        var what = $('[name="what"]', join); if (what) what.value = jT.textContent; // в заявке видно, откуда её отправили
        var t = b.dataset.joinTopic && $('[name="topic"][value="' + b.dataset.joinTopic + '"]', join);
        if (t) t.checked = true;
        J.open();
      });
    });
    $$('.js-join-close', join).forEach(function (b) { b.addEventListener('click', J.close); });
    jForm.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!validate(jForm)) return;
      send(jForm, function () { showDone(jForm, $('[name="name"]', jForm).value.trim() + ', спасибо! Перезвоним в рабочее время и поможем выбрать формат.'); });
    });
  }

  /* ---------- Форма заявки в блоке «Нужно связаться с нами?» ---------- */
  $$('form.cform').forEach(function (form) {
    if (form.closest('dialog')) return;
    var seg = $('.seg', form);
    if (seg) $$('input', seg).forEach(function (inp, i) { inp.addEventListener('change', function () { seg.style.setProperty('--i', i); }); });
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!validate(form)) return;
      var via = $('[name="via"]:checked', form);
      var how = { call: 'Перезвоним', tg: 'Напишем в Telegram', max: 'Напишем в Max', wa: 'Напишем в WhatsApp' }[via ? via.value : 'call'];
      send(form, function () { showDone(form, $('[name="name"]', form).value.trim() + ', спасибо! ' + how + ' в рабочее время — подберём тренировку.'); });
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
    var LIMIT = { group: { min: 1, max: 8, t: 'В группе — до 8 человек' }, personal: { min: 1, max: 3, t: 'Персонально — от 1 до 3 участников' } };
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
      $('.book__limit', bForm).textContent = L.t + (cnt.kids ? ' · для детей — детская пробная тренировка с тренером' : '');
      var pA = price(t === 'group' ? 'priceGroup' : 'pricePersonal'), pK = price(t === 'group' ? 'priceGroupKid' : 'pricePersonalKid');
      var rows = '', sum = 0, known = true;
      var label = t === 'group' ? 'Пробная в группе' : 'Персональная пробная';
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
      if (!validate(bForm)) return;
      // Здесь разработчик: отправить заявку в CRM и перейти на страницу оплаты банка (new FormData(bForm) + сумма)
      var who = cnt.adults + cnt.kids;
      showDone(bForm, $('[name="name"]', bForm).value.trim() + ', записываем вас: ' + (type() === 'group' ? 'пробная в группе' : 'персональная пробная') + ', участников — ' + who + '. Сейчас откроется оплата.');
    });
    recalc();
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

  /* ---------- Сцена «60 минут»: таймер, полоса времени, фото и шаги ----------
     Компьютер: блок закреплён, прокрутка ведёт минуты 0 → 60. Телефон и «уменьшить движение»: шаги листаются сами, пока блок на экране, и по нажатию */
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
      hSet(clamp((scrollY - M.top) / M.len, 0, 1) * 60);
    };
    var hList = $('.lp-hour__steps', hour), hSwipe = false;
    var hMode = function () {
      hScroll = !reduce && matchMedia('(min-width: 1041px) and (min-height: 640px)').matches;
      // телефон: шаги — карточки, которые листаются пальцем; таймер и полоса показывают текущую
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
      wVal.textContent = m.toFixed(1);
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
    bould: ['Боулдеринг', 'Лазание по невысоким трассам без верёвки — над мягкими матами.'],
    lead: ['Трудность', 'Лазание по высоким трассам со страховкой верёвкой. У нас стены 13 метров.'],
    shoes: ['Скальники', 'Специальная обувь для лазания с цепкой резиновой подошвой. Выдаём на месте.'],
    chalk: ['Магнезия', 'Порошок для рук: сушит ладони, чтобы они не скользили по зацепам.']
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

  /* ---------- Галерея ---------- */
  var lb = $('#lb'), gal = $('.lp-gal');
  if (lb && lb.showModal && gal) {
    var gItems = $$('.lp-gal__i', gal).map(function (b) { var im = $('img', b); return { src: im.getAttribute('src'), alt: im.getAttribute('alt') || '' }; });
    var gImg = $('.lb__img', lb), gCap = $('.lb__cap', lb), gCount = $('.lb__count', lb), gThumbs = $('.lb__thumbs', lb), gCur = 0;
    gItems.forEach(function (it, i) {
      var t = document.createElement('button'); t.type = 'button'; t.className = 'lb__th'; t.setAttribute('aria-label', 'Фото ' + (i + 1));
      t.innerHTML = '<img src="' + it.src + '" alt="" loading="lazy">'; t.addEventListener('click', function () { gShow(i); }); gThumbs.appendChild(t);
    });
    var gTh = $$('.lb__th', gThumbs);
    var gShow = function (i) {
      gCur = (i + gItems.length) % gItems.length;
      gImg.classList.remove('is-in'); void gImg.offsetWidth; gImg.src = gItems[gCur].src; gImg.alt = gItems[gCur].alt; gImg.classList.add('is-in');
      gCap.textContent = gItems[gCur].alt; gCount.textContent = (gCur + 1) + ' / ' + gItems.length;
      gTh.forEach(function (t, n) { t.setAttribute('aria-current', String(n === gCur)); });
    };
    var gClose = function () { if (lb.open) lb.close(); document.documentElement.classList.remove('lb-open'); };
    $$('.lp-gal__i', gal).forEach(function (b, i) { b.addEventListener('click', function () { document.documentElement.classList.add('lb-open'); lb.showModal(); gShow(i); }); });
    $('.lb__x', lb).addEventListener('click', gClose);
    $('.lb__nav--prev', lb).addEventListener('click', function () { gShow(gCur - 1); });
    $('.lb__nav--next', lb).addEventListener('click', function () { gShow(gCur + 1); });
    lb.addEventListener('keydown', function (e) { if (e.key === 'ArrowRight') gShow(gCur + 1); if (e.key === 'ArrowLeft') gShow(gCur - 1); });
    lb.addEventListener('close', function () { document.documentElement.classList.remove('lb-open'); });
    lb.addEventListener('click', function (e) { if (e.target === lb || e.target.classList.contains('lb__stage') || e.target.classList.contains('lb__fig')) gClose(); });
    var sx = null;
    lb.addEventListener('touchstart', function (e) { sx = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener('touchend', function (e) { if (sx === null) return; var dx = e.changedTouches[0].clientX - sx; sx = null; if (Math.abs(dx) > 50) gShow(gCur + (dx < 0 ? 1 : -1)); });
    var more = $('.js-gal-more');
    if (more) more.addEventListener('click', function () {
      var all = gal.classList.toggle('is-all');
      more.textContent = all ? 'Свернуть' : 'Показать ещё';
      more.setAttribute('aria-expanded', String(all));
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

  /* ---------- Липкое меню разделов и плавающая кнопка ---------- */
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
