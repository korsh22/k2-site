/* Скалодром К2 — страницы блога: шапка, меню, поиск, прогресс чтения, оглавление, фильтр рубрик. */
(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var store = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  };

  /* Кнопки: стрелка в красной кнопке и заливка от курсора — как на главной */
  var ARROW = '<svg class="ico" viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></svg>';
  $$('.btn').forEach(function (btn) {
    if (btn.classList.contains('btn--primary') && !$('.btn__arr', btn)) {
      var a = document.createElement('span');
      a.className = 'btn__arr'; a.setAttribute('aria-hidden', 'true'); a.innerHTML = ARROW + ARROW;
      btn.appendChild(a);
    }
    btn.addEventListener('mouseenter', function (e) {
      var r = btn.getBoundingClientRect();
      btn.style.setProperty('--x', (e.clientX - r.left) + 'px');
      btn.style.setProperty('--y', (e.clientY - r.top) + 'px');
      btn.style.setProperty('--s', (r.width * 2.4) + 'px');
    });
  });

  /* Промобар */
  var promo = $('#promo');
  if (promo) {
    if (store.get('k2-promo-closed') === '1') promo.classList.add('is-hidden');
    var px = $('.promo__x', promo);
    if (px) px.addEventListener('click', function () { promo.classList.add('is-hidden'); store.set('k2-promo-closed', '1'); });
  }

  /* Выпадающие меню */
  var dds = $$('.dd');
  function closeDd(except) { dds.forEach(function (d) { if (d !== except) { d.classList.remove('is-open'); $('.dd__btn', d).setAttribute('aria-expanded', 'false'); } }); }
  dds.forEach(function (d) {
    var b = $('.dd__btn', d);
    b.addEventListener('click', function (e) { e.stopPropagation(); var o = !d.classList.contains('is-open'); closeDd(d); d.classList.toggle('is-open', o); b.setAttribute('aria-expanded', String(o)); });
  });
  document.addEventListener('click', function () { closeDd(); });

  /* Мобильное меню */
  var hdr = $('#hdr'), burger = $('.burger'), mmenu = $('#mmenu');
  function setMenu(open) {
    if (!mmenu) return;
    mmenu.classList.toggle('is-open', open);
    mmenu.setAttribute('aria-hidden', String(!open));
    burger.setAttribute('aria-expanded', String(open));
    document.body.style.overflow = open ? 'hidden' : '';
    if (open) { hdr.classList.remove('is-hidden'); mmenu.style.paddingTop = (hdr.offsetHeight + 16) + 'px'; }
  }
  if (burger) burger.addEventListener('click', function () { setMenu(!mmenu.classList.contains('is-open')); });
  $$('a', mmenu || document.createElement('div')).forEach(function (a) { a.addEventListener('click', function () { setMenu(false); }); });

  /* Поиск */
  var search = $('#search'), q = $('#q');
  function setSearch(open) { if (!search) return; search.classList.toggle('is-open', open); search.setAttribute('aria-hidden', String(!open)); if (open) setTimeout(function () { q.focus(); }, 50); }
  var sOpen = $('.js-search'), sClose = $('.js-search-close');
  if (sOpen) sOpen.addEventListener('click', function () { setSearch(true); });
  if (sClose) sClose.addEventListener('click', function () { setSearch(false); });
  if (search) search.addEventListener('click', function (e) { if (e.target === search) setSearch(false); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') { setSearch(false); setMenu(false); closeDd(); } });

  /* Появление */
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -8% 0px' });
  $$('.reveal').forEach(function (el) { reduce ? el.classList.add('in') : io.observe(el); });

  /* Прокрутка: шапка, прогресс чтения, активный пункт оглавления */
  var bar = $('.readbar span'), body = $('.art__body');
  var tocLinks = $$('.toc a'), heads = tocLinks.map(function (a) { return document.getElementById(a.getAttribute('href').slice(1)); });
  var lastY = scrollY, ticking = false;
  function frame() {
    var y = scrollY, dy = y - lastY; lastY = y;
    hdr.classList.toggle('is-solid', y > 40);
    if (!mmenu || !mmenu.classList.contains('is-open')) {
      if (dy > 4 && y > 400) hdr.classList.add('is-hidden');
      else if (dy < -4 || y < 160) hdr.classList.remove('is-hidden');
    }
    if (bar && body) {
      var r = body.getBoundingClientRect();
      var k = Math.min(1, Math.max(0, (innerHeight * 0.4 - r.top) / Math.max(1, r.height - innerHeight * 0.4)));
      bar.style.setProperty('--read', k.toFixed(4));
    }
    if (heads.length) {
      var cur = 0;
      heads.forEach(function (h, i) { if (h && h.getBoundingClientRect().top < innerHeight * 0.35) cur = i; });
      tocLinks.forEach(function (a, i) { a.classList.toggle('is-on', i === cur); });
    }
    ticking = false;
  }
  window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(frame); } }, { passive: true });
  frame();

  /* Скопировать ссылку на статью */
  var cl = $('.copy-link');
  if (cl) cl.addEventListener('click', function () {
    var label = $('span', cl), base = label.textContent;
    var done = function () { cl.classList.add('is-done'); label.textContent = 'Ссылка скопирована'; setTimeout(function () { cl.classList.remove('is-done'); label.textContent = base; }, 1800); };
    if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(location.href).then(done, done);
    else { var t = document.createElement('textarea'); t.value = location.href; document.body.appendChild(t); t.select(); try { document.execCommand('copy'); } catch (e) {} t.remove(); done(); }
  });

  /* Фильтр рубрик на странице списка (рубрику можно открыть ссылкой: blog/index.html#train) */
  var chips = $$('.chip'), cards = $$('.bcard'), empty = $('.bempty');
  function filter(f) {
    chips.forEach(function (c) { c.setAttribute('aria-pressed', String(c.dataset.f === f)); });
    var shown = 0;
    cards.forEach(function (c) { var on = f === 'all' || c.dataset.cat === f; c.hidden = !on; if (on) { shown++; c.classList.add('in'); } });
    if (empty) empty.hidden = shown > 0;
  }
  if (chips.length && cards.length) {
    chips.forEach(function (c) { c.addEventListener('click', function () { filter(c.dataset.f); history.replaceState(null, '', c.dataset.f === 'all' ? location.pathname : '#' + c.dataset.f); }); });
    var h = location.hash.slice(1);
    if (h && chips.some(function (c) { return c.dataset.f === h; })) filter(h);
  }
})();

/* Загруженность зала — как на главной */
(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  /* ---------- Загруженность зала (онлайн из CRM) ----------
     Настройки — data-атрибуты у #occ:
       data-endpoint  адрес, который отдаёт JSON (через свой сервер / сниппет MODX — ключ CRM НЕ хранить на странице):
                      { "count": 23, "capacity": 120, "updated": "2026-10-14T15:20:00+03:00", "hourly": [..по часам 0–23, ожидаемое число людей..] }
       data-capacity  вместимость зала, если CRM её не отдаёт
       data-refresh   период обновления, секунд
     Пока data-endpoint пустой, показываются демо-данные с пометкой «Демо». */
  var occ = $('#occ');
  if (occ) {
    var OCC = { endpoint: occ.dataset.endpoint || '', capacity: +occ.dataset.capacity || 120, refresh: (+occ.dataset.refresh || 60) * 1000 };
    var hoursEl = $('.status'), openH = 8, closeH = 23;
    if (hoursEl) { openH = +hoursEl.dataset.open.split(':')[0]; closeH = +hoursEl.dataset.close.split(':')[0]; }
    // Типичная посещаемость по часам (демо): утро свободно, пик вечером
    var DEMO_HOURLY = [0,0,0,0,0,0,0,0,10,14,16,18,22,24,22,24,32,52,78,92,88,66,40,18];
    var spbHour = function () { return +new Date().toLocaleString('ru-RU', { timeZone: 'Europe/Moscow', hour: '2-digit', hour12: false }); };
    var chips = $$('.js-occ'), lines = $$('.js-occ-line');
    var panel = $('.occ__panel', occ);
    var level = function (k) { return k < 0.35 ? { id: 'low', t: 'Свободно', d: 'Можно спокойно выбирать трассы' } : k < 0.7 ? { id: 'mid', t: 'Средняя загрузка', d: 'Людей немного, но очереди на популярные трассы бывают' } : { id: 'high', t: 'Много людей', d: 'Сейчас пик — если хотите свободнее, загляните позже' }; };
    var plural = function (n) { var a = n % 10, b = n % 100; return a === 1 && b !== 11 ? 'человек' : a >= 2 && a <= 4 && (b < 12 || b > 14) ? 'человека' : 'человек'; };
    var render = function (d) {
      var h = spbHour(), open = h >= openH && h < closeH;
      var cap = d.capacity || OCC.capacity, n = open ? Math.max(0, Math.round(d.count)) : 0, k = Math.min(1, n / cap);
      var L = level(k);
      chips.forEach(function (c) {
        c.dataset.level = open ? L.id : 'closed';
        $('.occ-chip__n', c).textContent = open ? n : '—';
        c.setAttribute('aria-label', open ? 'Сейчас в зале ' + n + ' ' + plural(n) + ', ' + L.t.toLowerCase() + '. Подробнее о загруженности' : 'Зал закрыт. Загруженность по часам');
      });
      lines.forEach(function (l) { l.dataset.level = open ? L.id : 'closed'; $('span', l).textContent = open ? 'Сейчас в зале ' + n + ' ' + plural(n) + ' · ' + L.t.toLowerCase() : 'Сейчас закрыто · загруженность по часам'; });
      $('.occ__n', occ).textContent = open ? n : '—';
      $('.occ__unit', occ).textContent = open ? plural(n) + ' в зале' : 'зал закрыт';
      $('.occ__lvl', occ).textContent = open ? L.t : 'Сейчас закрыто';
      $('.occ__desc', occ).textContent = open ? L.d : 'Откроемся в ' + openH + ':00';
      occ.dataset.level = open ? L.id : 'closed';
      $('.occ__bar i', occ).style.width = (k * 100).toFixed(1) + '%';
      $('.occ__cap', occ).textContent = 'из ' + cap + ' мест';
      // График по часам работы
      var hourly = d.hourly || DEMO_HOURLY, max = Math.max.apply(null, hourly.slice(openH, closeH)) || 1, html = '';
      var best = null;
      for (var i = openH; i < closeH; i++) {
        var v = hourly[i] || 0, cls = i === h ? ' is-now' : i < h ? ' is-past' : '';
        html += '<li class="occ__col' + cls + '" style="--v:' + (v / max).toFixed(3) + '"><i></i><span>' + (i % 3 === 0 || i === h ? i : '') + '</span></li>';
        if (i > h && (best === null || v < hourly[best])) best = i;
      }
      $('.occ__chart', occ).innerHTML = html;
      $('.occ__tip', occ).textContent = best !== null && open ? 'Свободнее всего сегодня — около ' + best + ':00' : 'Утром обычно свободнее всего';
      var upd = d.updated ? new Date(d.updated) : new Date();
      $('.occ__upd span:last-child', occ).textContent = (d.demo ? 'Демо-данные · ' : 'Обновлено ') + upd.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit', timeZone: 'Europe/Moscow' });
      occ.classList.toggle('is-demo', !!d.demo);
    };
    var demo = function () {
      var h = spbHour(), m = new Date().getMinutes() / 60;
      var a = DEMO_HOURLY[h] || 0, b = DEMO_HOURLY[(h + 1) % 24] || 0;
      return { count: a + (b - a) * m + (Math.sin(Date.now() / 6e5) * 3), capacity: OCC.capacity, hourly: DEMO_HOURLY, demo: true };
    };
    var load = function () {
      if (!OCC.endpoint) { render(demo()); return; }
      fetch(OCC.endpoint, { cache: 'no-store' }).then(function (r) { if (!r.ok) throw r; return r.json(); })
        .then(function (d) { render(d); })
        .catch(function () { render(demo()); });   // CRM недоступна — показываем демо, а не пустоту
    };
    load();
    setInterval(load, OCC.refresh);

    // Панель: открыть по плашке, закрыть по клику мимо / Esc
    var setPanel = function (open, from) {
      occ.hidden = !open;
      chips.concat(lines).forEach(function (c) { c.setAttribute('aria-expanded', String(open)); });
      if (open) {
        if (from && window.innerWidth > 767) {
          var r = from.getBoundingClientRect();
          occ.style.top = Math.round(r.bottom + 12) + 'px';
          occ.style.left = Math.round(Math.min(Math.max(16, r.left + r.width / 2 - 190), innerWidth - 396)) + 'px';
        } else { occ.style.top = ''; occ.style.left = ''; }
        $('.occ__x', occ).focus({ preventScroll: true });
      }
    };
    chips.concat(lines).forEach(function (c) {
      c.addEventListener('click', function (e) { e.stopPropagation(); setPanel(occ.hidden, c); });
    });
    $('.occ__x', occ).addEventListener('click', function () { setPanel(false); });
    occ.addEventListener('click', function (e) { e.stopPropagation(); });
    document.addEventListener('click', function () { if (!occ.hidden) setPanel(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !occ.hidden) setPanel(false); });
    window.addEventListener('scroll', function () { if (!occ.hidden && window.innerWidth > 767) setPanel(false); }, { passive: true });
  }

})();

/* Подвал — как на главной: «камни» К и 2 встают на место при прокрутке, в букве К под «фонариком» проступает фото */
(function () {
  'use strict';
  var giant = document.querySelector('.foot__giant');
  if (!giant) return;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce) { giant.style.setProperty('--f', 1); }
  else {
    var tick = false;
    var frame = function () {
      var r = giant.getBoundingClientRect();
      giant.style.setProperty('--f', Math.min(1, Math.max(0, (innerHeight - r.top) / (r.height * 0.9))).toFixed(3));
      tick = false;
    };
    window.addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(frame); } }, { passive: true });
    window.addEventListener('resize', frame);
    frame();
  }
  var torch = giant.querySelector('.torch__c'), svg = giant.querySelector('svg'), k = giant.querySelector('.gk > path');
  if (!torch || !svg || !k) return;
  var move = function (x, y) {
    var pt = svg.createSVGPoint(); pt.x = x; pt.y = y;
    var m = svg.getScreenCTM(); if (!m) return;
    var s = pt.matrixTransform(m.inverse()), b = k.getBBox();
    torch.setAttribute('cx', s.x.toFixed(1)); torch.setAttribute('cy', s.y.toFixed(1));
    var near = s.x > b.x - 20 && s.x < b.x + b.width + 20 && s.y > b.y - 20 && s.y < b.y + b.height + 20;
    torch.setAttribute('r', near ? 130 : 0);
    giant.classList.toggle('is-torch', near);
  };
  var off = function () { torch.setAttribute('r', 0); giant.classList.remove('is-torch'); };
  giant.addEventListener('mousemove', function (e) { move(e.clientX, e.clientY); });
  giant.addEventListener('mouseleave', off);
  giant.addEventListener('touchmove', function (e) { var t = e.touches[0]; move(t.clientX, t.clientY); }, { passive: true });
  giant.addEventListener('touchend', off);
})();
