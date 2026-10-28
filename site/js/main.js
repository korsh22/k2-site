/* Скалодром К2 — эффекты главной. Без зависимостей. */
(function () {
  'use strict';

  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var clamp = function (v, a, b) { return Math.min(b, Math.max(a, v)); };
  var store = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  };

  /* ---------- Разбивка заголовков на слова ---------- */
  $$('.js-split').forEach(function (el) {
    var i = 0;
    var nodes = Array.prototype.slice.call(el.childNodes);
    el.textContent = '';
    nodes.forEach(function (n) {
      if (n.nodeType === 3) {
        n.textContent.split(' ').forEach(function (word, idx, arr) {
          if (word) el.appendChild(wrap(document.createTextNode(word), i++));
          if (idx < arr.length - 1) el.appendChild(document.createTextNode(' '));
        });
      } else {
        el.appendChild(wrap(n, i++));
      }
    });
    function wrap(node, index) {
      var w = document.createElement('span');
      var s = document.createElement('span');
      w.className = 'w';
      s.style.setProperty('--i', index);
      s.appendChild(node);
      w.appendChild(s);
      return w;
    }
  });

  /* ---------- Кнопки: стрелка и заливка от курсора ---------- */
  var ARROW = '<svg class="ico" viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></svg>';
  $$('.btn').forEach(function (btn) {
    if (btn.classList.contains('btn--primary')) {
      var a = document.createElement('span');
      a.className = 'btn__arr';
      a.setAttribute('aria-hidden', 'true');
      a.innerHTML = ARROW + ARROW;
      btn.appendChild(a);
    }
    btn.addEventListener('mouseenter', function (e) {
      var r = btn.getBoundingClientRect();
      btn.style.setProperty('--x', (e.clientX - r.left) + 'px');
      btn.style.setProperty('--y', (e.clientY - r.top) + 'px');
      btn.style.setProperty('--s', (r.width * 2.4) + 'px');
    });
    btn.addEventListener('mouseleave', function (e) {
      var r = btn.getBoundingClientRect();
      btn.style.setProperty('--x', (e.clientX - r.left) + 'px');
      btn.style.setProperty('--y', (e.clientY - r.top) + 'px');
    });
  });

  /* ---------- Прелоадер ---------- */
  var loader = $('.loader');
  var started = Date.now();
  function ready() {
    var wait = reduce ? 0 : Math.max(0, 1500 - (Date.now() - started));
    setTimeout(function () {
      loader.classList.add('is-done');
      document.body.classList.remove('is-loading');
      document.body.classList.add('is-ready');
      $$('.hero .js-split, .hero .reveal').forEach(function (el) { el.classList.add('in'); });
      setTimeout(function () { loader.remove(); }, 1100);
    }, wait);
  }
  if (document.readyState === 'complete') ready();
  else window.addEventListener('load', ready);
  setTimeout(function () { if (document.body.classList.contains('is-loading')) ready(); }, 4000);

  /* ---------- Фоновое видео в hero ---------- */
  // Грузим после страницы. При «меньше анимации» и экономии трафика остаётся фото.
  var heroVideo = $('.hero__video');
  var saveData = navigator.connection && navigator.connection.saveData;
  function loadHeroVideo() {
    if (!heroVideo || reduce || saveData) return;
    heroVideo.addEventListener('playing', function () { heroVideo.classList.add('is-on'); }, { once: true });
    heroVideo.muted = true;
    heroVideo.autoplay = true;
    heroVideo.src = heroVideo.dataset.src;
    function tryPlay() {
      if (!heroVideo.paused) return;
      var p = heroVideo.play();
      if (p && p.catch) p.catch(function () {}); // автозапуск запрещён — просто остаётся фото
    }
    heroVideo.addEventListener('canplay', tryPlay);
    document.addEventListener('visibilitychange', function () { if (!document.hidden) tryPlay(); });
    tryPlay();
  }
  if (document.readyState === 'complete') setTimeout(loadHeroVideo, 200);
  else window.addEventListener('load', function () { setTimeout(loadHeroVideo, 200); });

  /* ---------- Появление при прокрутке ---------- */
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      e.target.classList.add('in');
      if (e.target.classList.contains('count')) countUp(e.target);
      io.unobserve(e.target);
    });
  }, { rootMargin: '0px 0px -10% 0px', threshold: 0.12 });
  $$('.reveal, .js-split, .wall, .stair, .biglogo, .count').forEach(function (el) {
    if (el.closest('.hero') && !el.classList.contains('count') && !el.classList.contains('stat')) return;
    io.observe(el);
  });

  /* ---------- Счётчики 13 · 1300 · 7 ---------- */
  function countUp(el) {
    var to = +el.dataset.to;
    if (reduce) { el.textContent = to; return; }
    var t0 = null, dur = 1600;
    function step(t) {
      if (!t0) t0 = t;
      var k = clamp((t - t0) / dur, 0, 1);
      var e = k === 1 ? 1 : 1 - Math.pow(2, -10 * k);
      el.textContent = Math.round(to * e);
      if (k < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  /* ---------- Промобар: закрытие запоминается ---------- */
  var promo = $('#promo');
  if (store.get('k2-promo-closed') === '1') promo.classList.add('is-hidden');
  $('.promo__x').addEventListener('click', function () {
    promo.classList.add('is-hidden');
    store.set('k2-promo-closed', '1');
  });

  /* ---------- Выпадающие меню ---------- */
  var dds = $$('.dd');
  function closeDd(except) { dds.forEach(function (d) { if (d !== except) { d.classList.remove('is-open'); $('.dd__btn', d).setAttribute('aria-expanded', 'false'); } }); }
  dds.forEach(function (d) {
    var btn = $('.dd__btn', d);
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = !d.classList.contains('is-open');
      closeDd(d);
      d.classList.toggle('is-open', open);
      btn.setAttribute('aria-expanded', String(open));
    });
    if (finePointer) {
      var t;
      d.addEventListener('mouseenter', function () { clearTimeout(t); closeDd(d); d.classList.add('is-open'); btn.setAttribute('aria-expanded', 'true'); });
      d.addEventListener('mouseleave', function () { t = setTimeout(function () { d.classList.remove('is-open'); btn.setAttribute('aria-expanded', 'false'); }, 180); });
    }
  });
  document.addEventListener('click', function () { closeDd(); });

  /* ---------- Мобильное меню ---------- */
  var burger = $('.burger'), mmenu = $('#mmenu');
  function setMenu(open) {
    mmenu.classList.toggle('is-open', open);
    mmenu.setAttribute('aria-hidden', String(!open));
    burger.setAttribute('aria-expanded', String(open));
    burger.setAttribute('aria-label', open ? 'Закрыть меню' : 'Открыть меню');
    document.body.style.overflow = open ? 'hidden' : '';
    if (open) { hdr.classList.remove('is-hidden'); mmenu.style.paddingTop = (hdr.offsetHeight + 16) + 'px'; }
  }
  burger.addEventListener('click', function () { setMenu(!mmenu.classList.contains('is-open')); });
  $$('a', mmenu).forEach(function (a) { a.addEventListener('click', function () { setMenu(false); }); });

  /* ---------- Поиск ---------- */
  var search = $('#search'), q = $('#q');
  function setSearch(open) {
    search.classList.toggle('is-open', open);
    search.setAttribute('aria-hidden', String(!open));
    if (open) setTimeout(function () { q.focus(); }, 50);
  }
  $('.js-search').addEventListener('click', function () { setSearch(true); });
  $('.js-search-close').addEventListener('click', function () { setSearch(false); });
  search.addEventListener('click', function (e) { if (e.target === search) setSearch(false); });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    setSearch(false); setMenu(false); closeDd(); hideTip();
  });

  /* ---------- Словарик ---------- */
  var GLOSSARY = {
    bould: ['Боулдеринг', 'Лазание по невысоким трассам без верёвки — над мягкими матами.'],
    lead: ['Трудность', 'Лазание по высоким трассам со страховкой верёвкой. У нас стены 13 метров.'],
    shoes: ['Скальники', 'Специальная обувь для лазания с цепкой резиновой подошвой. Выдаём на месте.'],
    chalk: ['Магнезия', 'Порошок для рук: сушит ладони, чтобы они не скользили по зацепам.'],
    belay: ['Нижняя страховка', 'Способ страховки, при котором верёвку по ходу подъёма прощёлкивают в точки на стене.']
  };
  var tip = $('#tip'), tipT = $('.tip__t', tip), tipD = $('.tip__d', tip), tipFor = null;
  function showTip(el) {
    var g = GLOSSARY[el.dataset.term];
    if (!g) return;
    tipFor = el;
    tipT.textContent = g[0]; tipD.textContent = g[1];
    var r = el.getBoundingClientRect();
    tip.style.visibility = 'hidden'; tip.classList.add('is-on');
    var tw = tip.offsetWidth, th = tip.offsetHeight;
    var x = clamp(r.left + r.width / 2 - tw / 2, 12, window.innerWidth - tw - 12);
    var y = r.top - th - 10;
    if (y < 12) y = r.bottom + 10;
    tip.style.left = x + 'px'; tip.style.top = y + 'px';
    tip.style.visibility = '';
    tip.setAttribute('aria-hidden', 'false');
  }
  function hideTip() { tipFor = null; tip.classList.remove('is-on'); tip.setAttribute('aria-hidden', 'true'); }
  $$('.term').forEach(function (el) {
    el.setAttribute('tabindex', '0');
    el.setAttribute('aria-describedby', 'tip');
    el.addEventListener('mouseenter', function () { showTip(el); });
    el.addEventListener('mouseleave', hideTip);
    el.addEventListener('focus', function () { showTip(el); });
    el.addEventListener('blur', hideTip);
    el.addEventListener('click', function (e) { e.preventDefault(); e.stopPropagation(); tipFor === el ? hideTip() : showTip(el); });
  });
  window.addEventListener('scroll', function () { if (tipFor) hideTip(); }, { passive: true });

  /* ---------- Наклон карточек за курсором ---------- */
  if (finePointer && !reduce) {
    $$('.tilt').forEach(function (el) {
      el.addEventListener('mousemove', function (e) {
        var r = el.getBoundingClientRect();
        var x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
        el.classList.add('is-tilting');
        el.style.setProperty('--ry', (x * 10).toFixed(2) + 'deg');
        el.style.setProperty('--rx', (-y * 8).toFixed(2) + 'deg');
      });
      el.addEventListener('mouseleave', function () {
        el.classList.remove('is-tilting');
        el.style.setProperty('--ry', '0deg'); el.style.setProperty('--rx', '0deg');
      });
    });

  }

  /* ---------- Магнезия: облачко частиц при клике ---------- */
  var cv = $('.chalk'), ctx = cv.getContext('2d'), parts = [], dpr = Math.min(2, window.devicePixelRatio || 1), chalkRaf = 0;
  function sizeCanvas() { cv.width = innerWidth * dpr; cv.height = innerHeight * dpr; }
  sizeCanvas();
  window.addEventListener('resize', sizeCanvas);
  function burst(x, y, n) {
    if (reduce) return;
    for (var i = 0; i < (n || 46); i++) {
      var a = Math.random() * Math.PI * 2, s = 1.5 + Math.random() * 5.5;
      parts.push({ x: x, y: y, vx: Math.cos(a) * s, vy: Math.sin(a) * s - 2, r: 1.5 + Math.random() * 4.5, life: 1, decay: 0.012 + Math.random() * 0.02 });
    }
    if (!chalkRaf) chalkRaf = requestAnimationFrame(drawChalk);
  }
  function drawChalk() {
    ctx.clearRect(0, 0, cv.width, cv.height);
    parts = parts.filter(function (p) { return p.life > 0; });
    parts.forEach(function (p) {
      p.x += p.vx; p.y += p.vy; p.vx *= 0.95; p.vy = p.vy * 0.95 + 0.06; p.life -= p.decay;
      ctx.beginPath();
      ctx.fillStyle = 'rgba(255,255,255,' + Math.max(0, p.life * 0.85) + ')';
      ctx.arc(p.x * dpr, p.y * dpr, p.r * dpr * (1.4 - p.life * 0.4), 0, Math.PI * 2);
      ctx.fill();
    });
    chalkRaf = parts.length ? requestAnimationFrame(drawChalk) : 0;
    if (!parts.length) ctx.clearRect(0, 0, cv.width, cv.height);
  }
  $$('.js-chalk').forEach(function (el) {
    el.addEventListener('click', function (e) {
      var r = el.getBoundingClientRect();
      burst(e.clientX || r.left + r.width / 2, e.clientY || r.top + r.height / 2);
    });
  });

  /* ---------- Hero: буквы заголовка реагируют на курсор ---------- */
  var heroSec = $('.hero'), heroH1 = $('.hero .h1');
  if (heroSec && heroH1 && finePointer && !reduce) {
    // Каждую букву — в свой span (внутри слов, которые уже разбиты для появления)
    (function wrapChars(node) {
      Array.prototype.slice.call(node.childNodes).forEach(function (n) {
        if (n.nodeType === 3) {
          // Буквы одного слова (и слов, склеенных неразрывным пробелом) — в неразрывную группу,
          // иначе браузер может перенести строку между буквами
          var frag = document.createDocumentFragment();
          n.textContent.split(' ').forEach(function (word, wi, arr) {
            if (word) {
              var wd = document.createElement('span');
              wd.className = 'wd';
              Array.prototype.forEach.call(word, function (ch) {
                var s = document.createElement('span');
                s.className = 'ch';
                s.textContent = ch;
                wd.appendChild(s);
              });
              frag.appendChild(wd);
            }
            if (wi < arr.length - 1) frag.appendChild(document.createTextNode(' '));
          });
          node.replaceChild(frag, n);
        } else if (n.nodeType === 1) wrapChars(n);
      });
    })(heroH1);
    var chars = $$('.ch', heroH1), centers = [], hx = -9999, hy = -9999, heroRaf = 0, heroIn = false;
    var measureChars = function () {
      centers = chars.map(function (c) {
        var r = c.getBoundingClientRect();
        return { x: r.left + r.width / 2, y: r.top + r.height / 2 + scrollY };
      });
    };
    var R = 180;
    var renderChars = function () {
      heroRaf = 0;
      for (var i = 0; i < chars.length; i++) {
        var dx = hx - centers[i].x, dy = (hy + scrollY) - centers[i].y;
        var d = Math.sqrt(dx * dx + dy * dy);
        var k = d < R ? Math.pow(1 - d / R, 2) : 0;
        chars[i].style.transform = k ? 'translate3d(' + (-dx / d * k * 6).toFixed(1) + 'px,' + (-k * 16).toFixed(1) + 'px,0) rotate(' + (dx / d * k * -8).toFixed(1) + 'deg)' : '';
      }
    };
    // Первый экран заезжает под прозрачную шапку — свет и буквы реагируют и когда курсор над шапкой
    var lit = false, firstSec = $('#first');
    window.addEventListener('mousemove', function (e) {
      var r = heroSec.getBoundingClientRect(), fr = firstSec ? firstSec.getBoundingClientRect() : r;
      // свет живёт в первом экране и блоке «Первый раз» (общий графитовый фон)
      var inside = e.clientY >= r.top && e.clientY <= fr.bottom && e.clientX >= r.left && e.clientX <= r.right;
      if (inside) {
        if (!heroIn) { measureChars(); heroIn = true; }
        hx = e.clientX; hy = e.clientY; lit = true;
        heroSec.style.setProperty('--mx', (e.clientX - r.left) + 'px');
        heroSec.style.setProperty('--my', (e.clientY - r.top) + 'px');
        heroSec.classList.add('is-lit');
      } else if (lit) {
        hx = hy = -9999; heroIn = false; lit = false;
        heroSec.classList.remove('is-lit');
      } else return;
      if (!heroRaf) heroRaf = requestAnimationFrame(renderChars);
    }, { passive: true });
    window.addEventListener('resize', function () { heroIn = false; });
    // Заголовок «выезжает» после загрузки — пересчитываем позиции букв, когда он встал на место
    window.addEventListener('load', function () { setTimeout(function () { heroIn = false; }, 2800); });
  }

  /* ---------- Курсор «магнезия»: меловая точка + кольцо-хват ---------- */
  if (finePointer && !reduce) {
    var cur = document.createElement('div');
    cur.className = 'cur';
    cur.setAttribute('aria-hidden', 'true');
    cur.innerHTML = '<span class="cur__ring"><span class="cur__label"></span></span><span class="cur__dot"></span>';
    document.body.appendChild(cur);
    document.documentElement.classList.add('has-cur');
    var ring = $('.cur__ring', cur), dot = $('.cur__dot', cur), curLabel = $('.cur__label', cur);
    var mx = innerWidth / 2, my = innerHeight / 2, rx = mx, ry = my, seen = false;
    window.addEventListener('mousemove', function (e) {
      mx = e.clientX; my = e.clientY;
      if (!seen) { seen = true; rx = mx; ry = my; cur.classList.add('is-on'); }
      dot.style.transform = 'translate3d(' + mx + 'px,' + my + 'px,0)';
    }, { passive: true });
    document.addEventListener('mouseleave', function () { cur.classList.remove('is-on'); seen = false; });
    (function follow() {
      rx += (mx - rx) * 0.18; ry += (my - ry) * 0.18;
      ring.style.transform = 'translate3d(' + rx.toFixed(1) + 'px,' + ry.toFixed(1) + 'px,0)';
      requestAnimationFrame(follow);
    })();
    // Состояния над разными элементами
    var LABELS = [['.short', 'смотреть'], ['.cell', 'открыть'], ['.route', 'идём'], ['.shorts', 'тяни']];
    var forced = '';
    window.K2cursor = function (text) {
      forced = text;
      curLabel.textContent = text;
      cur.classList.toggle('is-label', !!text);
      if (text) cur.classList.remove('is-link');
    };
    document.addEventListener('mouseover', function (e) {
      var t = e.target;
      var text = t.closest('input, textarea, select');
      cur.classList.toggle('is-text', !!text);
      var label = '';
      for (var i = 0; i < LABELS.length; i++) { if (t.closest(LABELS[i][0])) { label = LABELS[i][1]; break; } }
      if (forced && t.closest('.foot__giant')) return;
      curLabel.textContent = label;
      cur.classList.toggle('is-label', !!label && !text);
      cur.classList.toggle('is-link', !label && !text && !!t.closest('a, button, label, summary, .term, [role="button"], [role="slider"]'));
    });
    window.addEventListener('mousedown', function () {
      cur.classList.add('is-down');
      burst(mx, my, 10);
    });
    window.addEventListener('mouseup', function () { cur.classList.remove('is-down'); });
  }

  /* ---------- Подвал: фонарик внутри «К» ---------- */
  var giantEl = $('.foot__giant'), torch = $('.torch__c');
  if (giantEl && torch) {
    var torchSvg = $('svg', giantEl), torchK = $('.gk > path', giantEl);
    var torchMove = function (x, y) {
      var pt = torchSvg.createSVGPoint(); pt.x = x; pt.y = y;
      var m = torchSvg.getScreenCTM();
      if (!m) return;
      var s = pt.matrixTransform(m.inverse());
      torch.setAttribute('cx', s.x.toFixed(1));
      torch.setAttribute('cy', s.y.toFixed(1));
      // Свет включается, только когда курсор над буквой К (с небольшим запасом)
      var b = torchK.getBBox();
      var near = s.x > b.x - 20 && s.x < b.x + b.width + 20 && s.y > b.y - 20 && s.y < b.y + b.height + 20;
      torch.setAttribute('r', near ? 130 : 0);
      giantEl.classList.toggle('is-torch', near);
      if (window.K2cursor) window.K2cursor(near ? 'свети' : '');
    };
    giantEl.addEventListener('mousemove', function (e) { torchMove(e.clientX, e.clientY); });
    giantEl.addEventListener('mouseleave', function () {
      torch.setAttribute('r', 0); giantEl.classList.remove('is-torch');
      if (window.K2cursor) window.K2cursor('');
    });
    giantEl.addEventListener('touchmove', function (e) { var t = e.touches[0]; torchMove(t.clientX, t.clientY); }, { passive: true });
    giantEl.addEventListener('touchend', function () { torch.setAttribute('r', 0); giantEl.classList.remove('is-torch'); });
  }

  /* ---------- FAQ: плавное раскрытие ---------- */
  $$('.faq details').forEach(function (d) {
    var sum = $('summary', d), body = $('.faq__a', d);
    sum.addEventListener('click', function (e) {
      if (reduce) return;
      e.preventDefault();
      if (d.open) {
        var h = body.offsetHeight;
        body.animate([{ height: h + 'px', opacity: 1 }, { height: '0px', opacity: 0 }], { duration: 320, easing: 'cubic-bezier(.22,1,.36,1)' }).onfinish = function () { d.open = false; };
      } else {
        d.open = true;
        var h2 = body.offsetHeight;
        body.animate([{ height: '0px', opacity: 0 }, { height: h2 + 'px', opacity: 1 }], { duration: 420, easing: 'cubic-bezier(.22,1,.36,1)' });
      }
    });
  });

  /* ---------- Связь: статус «открыто/закрыто» по времени Петербурга ---------- */
  var status = $('.status');
  if (status) {
    var toMin = function (s) { var p = s.split(':'); return +p[0] * 60 + +p[1]; };
    var open = status.dataset.open, close = status.dataset.close;
    var updateStatus = function () {
      var now = new Date().toLocaleTimeString('ru-RU', { timeZone: 'Europe/Moscow', hour: '2-digit', minute: '2-digit', hour12: false });
      var m = toMin(now), o = toMin(open), c = toMin(close);
      var isOpen = m >= o && m < c;
      status.classList.toggle('is-open', isOpen);
      $('.status__t', status).innerHTML = isOpen
        ? 'Сейчас открыто · до <b>' + close + '</b>'
        : 'Сейчас закрыто · откроемся в <b>' + open.replace(/^0/, '') + '</b>';
    };
    updateStatus();
    setInterval(updateStatus, 60000);
  }

  /* ---------- Формы заявки (блок связи и всплывающее окно): маска телефона, проверка, экран «Спасибо» ---------- */
  // В MODX: отправку подключает разработчик (FormIt / AjaxForm) — место отмечено ниже
  function initForm(form) {
    var phone = $('[name="phone"]', form), name = $('[name="name"]', form), agree = $('[name="agree"]', form);
    var errAgree = $('.field__err--agree', form), seg = $('.seg', form), done = $('.cform__done', form);

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
    name.addEventListener('input', function () { if (name.value.trim()) name.parentNode.classList.remove('is-bad'); });
    agree.addEventListener('change', function () { if (agree.checked) errAgree.classList.remove('is-on'); });

    if (seg) $$('input', seg).forEach(function (inp, i) {
      inp.addEventListener('change', function () { seg.style.setProperty('--i', i); });
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var okName = !!name.value.trim();
      var okPhone = phone.value.replace(/\D/g, '').length === 11;
      name.parentNode.classList.toggle('is-bad', !okName);
      phone.parentNode.classList.toggle('is-bad', !okPhone);
      errAgree.classList.toggle('is-on', !agree.checked);
      if (!okName || !okPhone || !agree.checked) {
        form.classList.remove('is-shake'); void form.offsetWidth; form.classList.add('is-shake');
        (!okName ? name : !okPhone ? phone : agree).focus();
        return;
      }
      var viaEl = $('[name="via"]:checked', form), via = viaEl ? viaEl.value : 'call';
      var how = { call: 'Перезвоним', tg: 'Напишем в Telegram', max: 'Напишем в Max', wa: 'Напишем в WhatsApp' }[via];
      var showDone = function () {
        $('.done__msg', form).textContent = name.value.trim() + ', спасибо! ' + how + ' в рабочее время — подберём тренировку.';
        form.classList.add('is-sent');
        done.hidden = false;
        var ic = $('.done__ic', done); ic.replaceWith(ic.cloneNode(true)); // перезапуск анимации галочки
      };
      // Отправка: если у формы есть data-action (обработчик FormIt / AjaxForm в MODX) — шлём туда; иначе демо
      var action = form.dataset.action;
      if (!action) { showDone(); return; }
      var go = $('.cform__go', form); go.disabled = true;
      fetch(action, { method: 'POST', body: new FormData(form), headers: { 'X-Requested-With': 'XMLHttpRequest' } })
        .then(function (r) { if (!r.ok) throw r; showDone(); })
        .catch(function () {
          var err = $('.cform__fail', form);
          if (!err) { err = document.createElement('p'); err.className = 'cform__fail'; err.setAttribute('role', 'alert'); go.parentNode.insertBefore(err, go.nextSibling); }
          err.textContent = 'Не получилось отправить заявку. Попробуйте ещё раз или позвоните нам.';
        })
        .then(function () { go.disabled = false; });
    });
    var again = $('.js-again', form);
    if (again) again.addEventListener('click', function () {
      form.reset(); if (seg) seg.style.setProperty('--i', 0);
      form.classList.remove('is-sent'); done.hidden = true;
      name.focus();
    });
  }
  $$('form.cform').forEach(initForm);

  /* ---------- Всплывающее окно «Присоединяйтесь» ---------- */
  var modal = $('#join');
  if (modal && modal.showModal) {
    var mForm = $('form', modal);
    var joinT = $('#join-t'), joinTitle = joinT.innerHTML;
    var openModal = function (e) {
      // Заголовок и тема — от кнопки, которая открыла окно (data-join-title, data-join-topic)
      var t = e && e.currentTarget;
      joinT.innerHTML = (t && t.dataset.joinTitle) || joinTitle;
      var what = $('[name="what"]', modal); if (what) what.value = joinT.textContent; // в заявке видно, откуда её отправили
      var topic = t && t.dataset.joinTopic && $('[name="topic"][value="' + t.dataset.joinTopic + '"]', modal);
      if (topic) topic.checked = true;
      document.documentElement.classList.add('modal-open');
      modal.showModal();
      setTimeout(function () { var f = $('[name="name"]', modal); if (f && finePointer) f.focus(); }, 60);
    };
    var cleanup = function () {
      document.documentElement.classList.remove('modal-open');
      if (mForm.classList.contains('is-sent')) { mForm.reset(); mForm.classList.remove('is-sent'); $('.cform__done', mForm).hidden = true; }
    };
    var closeModal = function () {
      modal.classList.add('is-closing');
      setTimeout(function () { modal.classList.remove('is-closing'); if (modal.open) modal.close(); cleanup(); }, reduce ? 0 : 220);
    };
    modal.addEventListener('close', cleanup);
    $$('.js-join').forEach(function (b) { b.addEventListener('click', openModal); });
    $$('.js-join-close', modal).forEach(function (b) { b.addEventListener('click', closeModal); });
    // клик по затемнению вокруг карточки
    modal.addEventListener('click', function (e) { if (e.target === modal) closeModal(); });
    modal.addEventListener('cancel', function (e) { e.preventDefault(); closeModal(); });
  }

  /* ---------- Связь: копирование номера и почты ---------- */
  $$('.copy').forEach(function (btn) {
    var label = $('span', btn), base = label.textContent;
    btn.addEventListener('click', function () {
      var text = btn.dataset.copy;
      var done = function () {
        btn.classList.add('is-done'); label.textContent = 'Скопировано';
        setTimeout(function () { btn.classList.remove('is-done'); label.textContent = base; }, 1600);
      };
      if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(text).then(done, done);
      else {
        var t = document.createElement('textarea'); t.value = text; t.style.position = 'fixed'; t.style.opacity = '0';
        document.body.appendChild(t); t.select();
        try { document.execCommand('copy'); } catch (err) {}
        t.remove(); done();
      }
    });
  });

  /* ---------- Связь: «прогулка» от метро до К2 ---------- */
  var route = $('.route');
  if (route) {
    var walk = $('#walk', route), minEl = $('.route__min', route), walking = false;
    var startWalk = function () {
      if (walking || reduce || !walk || !walk.beginElement) return;
      walking = true;
      route.classList.add('is-walking');
      walk.beginElement();
      var t0 = performance.now(), dur = 5000;
      (function tick(t) {
        var k = Math.min(1, (t - t0) / dur);
        minEl.textContent = Math.max(0, Math.ceil(7 * (1 - k)));
        if (k < 1) requestAnimationFrame(tick);
        else {
          minEl.textContent = '7';
          setTimeout(function () { route.classList.remove('is-walking'); walking = false; }, 900);
        }
      })(t0);
    };
    new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) startWalk(); }); }, { threshold: 0.6 }).observe(route);
    route.addEventListener('mouseenter', startWalk);
    route.addEventListener('click', startWalk);
  }

  /* ---------- Пакеты: «Новичкам / Продолжающим» ---------- */
  var tabs = $('.tabs');
  if (tabs) {
    var tabBtns = $$('.tabs__b', tabs);
    tabBtns.forEach(function (b, i) {
      b.addEventListener('click', function () {
        tabs.style.setProperty('--i', i);
        tabBtns.forEach(function (x) {
          var on = x === b;
          x.setAttribute('aria-selected', String(on));
          var panel = document.getElementById(x.getAttribute('aria-controls'));
          panel.hidden = !on;
          if (on) { panel.classList.add('in'); panel.classList.remove('is-enter'); void panel.offsetWidth; panel.classList.add('is-enter'); }
        });
      });
    });
  }

  /* ---------- «Ещё атмосферы»: раскрыть / свернуть дополнительные фото ---------- */
  var moreBtn = $('.js-more'), more = $('#more-photos');
  if (moreBtn && more) {
    moreBtn.addEventListener('click', function () {
      var open = more.hidden;
      more.hidden = !open;
      moreBtn.setAttribute('aria-expanded', String(open));
      $('.js-more-t', moreBtn).textContent = open ? 'Свернуть' : 'Ещё атмосферы';
      if (!open) {
        var top = more.previousElementSibling.getBoundingClientRect().bottom;
        if (top < 0) scrollBy({ top: top - innerHeight / 2, behavior: reduce ? 'auto' : 'smooth' });
      }
    });
  }

  /* ---------- Галерея: клик по фото в «Почему К2» ---------- */
  var lb = $('#lb');
  if (lb && lb.showModal) {
    var cells = $$('.why .cell'), items = cells.map(function (c) { var im = $('img', c); return { src: im.getAttribute('src'), alt: im.getAttribute('alt') || '' }; });
    var lbImg = $('.lb__img', lb), lbCap = $('.lb__cap', lb), lbCount = $('.lb__count', lb), lbThumbs = $('.lb__thumbs', lb), lbCur = 0, opener = null;
    items.forEach(function (it, i) {
      var b = document.createElement('button');
      b.type = 'button'; b.className = 'lb__th'; b.setAttribute('role', 'listitem');
      b.setAttribute('aria-label', 'Фото ' + (i + 1) + (it.alt ? ': ' + it.alt : ''));
      b.innerHTML = '<img src="' + it.src + '" alt="" loading="lazy">';
      b.addEventListener('click', function () { show(i); });
      lbThumbs.appendChild(b);
    });
    var thumbs = $$('.lb__th', lbThumbs);
    var show = function (i) {
      lbCur = (i + items.length) % items.length;
      lbImg.classList.remove('is-in'); void lbImg.offsetWidth;
      lbImg.src = items[lbCur].src; lbImg.alt = items[lbCur].alt;
      lbImg.classList.add('is-in');
      lbCap.textContent = items[lbCur].alt;
      lbCount.textContent = (lbCur + 1) + ' / ' + items.length;
      thumbs.forEach(function (t, n) { t.setAttribute('aria-current', String(n === lbCur)); });
      thumbs[lbCur].scrollIntoView({ block: 'nearest', inline: 'center' });
      // подгружаем соседние кадры заранее
      [lbCur + 1, lbCur - 1].forEach(function (n) { var im = new Image(); im.src = items[(n + items.length) % items.length].src; });
    };
    var openLb = function (i) {
      opener = document.activeElement;
      document.documentElement.classList.add('lb-open');
      lb.showModal(); show(i);
    };
    var lbCleanup = function () {
      if (!document.documentElement.classList.contains('lb-open')) return;
      document.documentElement.classList.remove('lb-open');
      if (opener && opener.focus) opener.focus({ preventScroll: true });
    };
    var closeLb = function () { if (lb.open) lb.close(); lbCleanup(); };
    lb.addEventListener('close', lbCleanup);
    cells.forEach(function (c, i) {
      c.setAttribute('tabindex', '0'); c.setAttribute('role', 'button');
      c.setAttribute('aria-label', 'Открыть фото' + (items[i].alt ? ': ' + items[i].alt : ''));
      c.addEventListener('click', function () { openLb(i); });
      c.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openLb(i); } });
    });
    $('.lb__x', lb).addEventListener('click', closeLb);
    $('.lb__nav--prev', lb).addEventListener('click', function () { show(lbCur - 1); });
    $('.lb__nav--next', lb).addEventListener('click', function () { show(lbCur + 1); });
    lb.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') { e.preventDefault(); show(lbCur + 1); }
      if (e.key === 'ArrowLeft') { e.preventDefault(); show(lbCur - 1); }
    });
    // клик мимо фото и кнопок — закрыть
    lb.addEventListener('click', function (e) { if (e.target === lb || e.target.classList.contains('lb__stage') || e.target.classList.contains('lb__fig')) closeLb(); });
    // свайп на телефоне
    var sx = null;
    lb.addEventListener('touchstart', function (e) { sx = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener('touchend', function (e) {
      if (sx === null) return;
      var dx = e.changedTouches[0].clientX - sx; sx = null;
      if (Math.abs(dx) > 50) show(lbCur + (dx < 0 ? 1 : -1));
    });
  }

  /* ---------- Логотип К2: фото внутри букв по словам «Атмосфера / Возможности / Люди» ---------- */
  var logoLayers = $$('.biglogo__photo'), stairW = $$('.stair__w[data-i]');
  var setLogo = function (i) {
    logoLayers.forEach(function (l) { l.classList.toggle('is-on', +l.dataset.i === i); });
  };
  stairW.forEach(function (w) {
    w.addEventListener('mouseenter', function () { setLogo(+w.dataset.i); w.classList.add('is-hover'); });
    w.addEventListener('mouseleave', function () { setLogo(0); w.classList.remove('is-hover'); });
  });
  window.__k2setLogo = setLogo;

  (function () { // своя область видимости: имена переменных виджета не пересекаются с остальным кодом
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

  /* ---------- Фильтр блога ---------- */
  var chips = $$('.chip');
  chips.forEach(function (c) {
    c.addEventListener('click', function () {
      chips.forEach(function (x) { x.setAttribute('aria-pressed', String(x === c)); });
      var f = c.dataset.f;
      $$('.post').forEach(function (p) { p.classList.toggle('is-out', f !== 'all' && p.dataset.cat !== f); });
    });
  });

  /* ---------- Лента видео: тянуть мышью и стрелки ---------- */
  var shorts = $('.shorts');
  (function () {
    var down = false, sx = 0, sl = 0, moved = false;
    shorts.addEventListener('pointerdown', function (e) {
      if (e.pointerType !== 'mouse') return;
      down = true; moved = false; sx = e.clientX; sl = shorts.scrollLeft;
    });
    window.addEventListener('pointermove', function (e) {
      if (!down) return;
      var dx = e.clientX - sx;
      if (Math.abs(dx) > 5) { moved = true; shorts.classList.add('is-drag'); }
      shorts.scrollLeft = sl - dx;
    });
    window.addEventListener('pointerup', function () {
      if (!down) return;
      down = false;
      setTimeout(function () { shorts.classList.remove('is-drag'); }, 0);
    });
    shorts.addEventListener('click', function (e) { if (moved) { e.preventDefault(); moved = false; } }, true);
    var step = function () { var s = $('.short', shorts); return s ? s.offsetWidth + 16 : 300; };
    $('.js-next').addEventListener('click', function () { shorts.scrollBy({ left: step(), behavior: 'smooth' }); });
    $('.js-prev').addEventListener('click', function () { shorts.scrollBy({ left: -step(), behavior: 'smooth' }); });
  })();

  /* ---------- Шкала 0 → 13 м ---------- */
  var gauge = $('.gauge'), gVal = $('.gauge__val'), marks = $('.gauge__marks');
  for (var m = 0; m <= 13; m++) {
    var li = document.createElement('li');
    li.style.bottom = (m / 13 * 100) + '%';
    if (m % 5 === 0 || m === 13) { li.className = 'is-major'; li.innerHTML = '<span>' + m + '</span>'; }
    marks.appendChild(li);
  }

  // Навигация по шкале: клик — плавно туда, перетаскивание — страница едет следом, стрелки — на метр
  (function () {
    var tip = $('.gauge__tip', gauge), dragging = false, moved = false;
    var NAMES = [['#top', 'Главная'], ['#first', 'Первый раз'], ['#about', 'Почему К2'], ['#goals', 'Для любых целей'],
                 ['#prices', 'Цены и пакеты'], ['.videos', 'Видео'], ['#blog', 'Блог и отзывы'], ['#contacts', 'Связь и вопросы'], ['.foot', 'Контакты']];
    var maxScroll = function () { return document.documentElement.scrollHeight - innerHeight; };
    var gFromY = function (y) { var r = gauge.getBoundingClientRect(); return clamp(1 - (y - r.top) / r.height, 0, 1); };
    var sectionAt = function (g) {
      var target = g * maxScroll() + innerHeight * 0.35, name = NAMES[0][1];
      NAMES.forEach(function (n) { var el = $(n[0]); if (el && el.getBoundingClientRect().top + scrollY <= target) name = n[1]; });
      return name;
    };
    var showTip = function (g) {
      tip.textContent = sectionAt(g) + ' · ' + (g * 13).toFixed(1) + ' м';
      gauge.style.setProperty('--tip-y', (g * 100) + '%');
      gauge.classList.add('is-tip');
    };
    var go = function (g, smooth) { window.scrollTo({ top: g * maxScroll(), behavior: smooth && !reduce ? 'smooth' : 'instant' }); };
    gauge.addEventListener('pointermove', function (e) {
      var g = gFromY(e.clientY);
      showTip(g);
      if (dragging) { moved = true; go(g, false); }
    });
    gauge.addEventListener('pointerleave', function () { if (!dragging) gauge.classList.remove('is-tip'); });
    gauge.addEventListener('pointerdown', function (e) {
      dragging = true; moved = false;
      try { gauge.setPointerCapture(e.pointerId); } catch (err) {}
      gauge.classList.add('is-drag');
      e.preventDefault();
    });
    var end = function (e) {
      if (!dragging) return;
      dragging = false;
      gauge.classList.remove('is-drag');
      if (!moved) go(gFromY(e.clientY), true);   // простой клик — плавный переход
      if (e.pointerType !== 'mouse') gauge.classList.remove('is-tip');
    };
    gauge.addEventListener('pointerup', end);
    gauge.addEventListener('pointercancel', end);
    gauge.addEventListener('keydown', function (e) {
      var g = clamp(scrollY / Math.max(1, maxScroll()), 0, 1), step = 1 / 13;
      var map = { ArrowUp: g + step, ArrowRight: g + step, ArrowDown: g - step, ArrowLeft: g - step, PageUp: g + step * 3, PageDown: g - step * 3, Home: 0, End: 1 };
      if (!(e.key in map)) return;
      e.preventDefault();
      var ng = clamp(map[e.key], 0, 1);
      go(ng, true); showTip(ng);
      clearTimeout(gauge._t); gauge._t = setTimeout(function () { gauge.classList.remove('is-tip'); }, 1200);
    });
  })();

  /* ---------- Две ленты: заполняем ширину копиями ---------- */
  var bands = $$('.mq__t').map(function (t) {
    return { t: t, item: $('.mq__i', t), w: 0, x: 0, dir: +t.dataset.dir || 1, paused: false };
  });
  function fillMarquee() {
    bands.forEach(function (b) {
      $$('.mq__i', b.t).slice(1).forEach(function (n) { n.remove(); });
      b.w = b.item.offsetWidth;
      var need = Math.ceil((innerWidth * 2.2) / Math.max(1, b.w)) + 1;
      for (var i = 0; i < need; i++) {
        var c = b.item.cloneNode(true);
        c.setAttribute('aria-hidden', 'true');
        b.t.appendChild(c);
      }
      b.t.parentNode.addEventListener('mouseenter', function () { b.paused = true; });
      b.t.parentNode.addEventListener('mouseleave', function () { b.paused = false; });
    });
  }
  fillMarquee();
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(fillMarquee);

  /* ---------- Главный цикл прокрутки ---------- */
  var hdr = $('#hdr'), heroMedia = $('.hero__media'), heroStage = $('.hero__stage');
  var logoPhoto = $('.biglogo__photo'), biglogo = $('.biglogo'), giant = $('.foot__giant');
  var wallCols = $$('.wall__col');
  var stairWords = $$('.stair__w');
  var mobile = window.matchMedia('(max-width: 767px)');
  // Блоки, которые наезжают на предыдущий
  var flow = $$('main > section, main > .xband, body > footer');
  var stacks = flow.map(function (el, i) {
    if (!el.classList.contains('stack')) return null;
    var prev = flow[i - 1];
    if (prev && prev.classList.contains('xband')) prev = flow[i - 2];
    if (prev) prev.classList.add('is-covered');
    return prev ? { el: el, prev: prev } : null;
  }).filter(Boolean);
  var lastY = scrollY, vel = 0, ticking = false, wasTop = false;
  var stageTop = 0;
  function measure() { stageTop = heroStage.getBoundingClientRect().top + scrollY; }
  measure();
  window.addEventListener('resize', function () { measure(); fillMarquee(); });

  function frame() {
    var y = scrollY, vh = innerHeight;
    var dy = y - lastY;
    lastY = y;
    vel = vel * 0.85 + dy * 0.15;

    // Хедер: прячется при прокрутке вниз, возвращается при прокрутке вверх
    hdr.classList.toggle('is-solid', y > 60);
    if (!mmenu.classList.contains('is-open')) {
      if (dy > 4 && y > 500) hdr.classList.add('is-hidden');
      else if (dy < -4 || y < 200) hdr.classList.remove('is-hidden');
    }

    if (!reduce) {
      // Hero: карточка с фото раскрывается на всю ширину
      var hdrH = hdr.offsetHeight;
      var p = clamp(y / Math.max(1, stageTop - hdrH - 40), 0, 1);
      heroMedia.style.setProperty('--p', p.toFixed(4));

      // Фото внутри логотипа — параллакс
      var lr = biglogo.getBoundingClientRect();
      if (lr.bottom > 0 && lr.top < vh) {
        var c = (lr.top + lr.height / 2 - vh / 2) / vh;
        biglogo.style.setProperty('--py', (c * -120).toFixed(1) + 'px');
      }

      // Стена: колонки едут с разной скоростью
      if (!mobile.matches) {
        wallCols.forEach(function (col) {
          var r = col.parentNode.getBoundingClientRect();
          if (r.bottom < -200 || r.top > vh + 200) return;
          var k = (r.top + r.height / 2 - vh / 2);
          col.style.transform = 'translate3d(0,' + clamp(k * +col.dataset.speed, -40, 40).toFixed(1) + 'px,0)';
        });
      }

      // Наезд блоков: предыдущий уменьшается и темнеет
      stacks.forEach(function (s) {
        var t = s.el.getBoundingClientRect().top;
        var k = clamp(1 - t / vh, 0, 1);
        s.prev.style.setProperty('--sc', (1 - k * 0.06).toFixed(4));
        s.prev.style.setProperty('--dim', (k * 0.55).toFixed(3));
      });

      // Телефон: слова «Атмосфера / Возможности / Люди» зажигаются по очереди при прокрутке
      if (mobile.matches) {
        var lit = 0;
        stairWords.forEach(function (w, i) {
          var r = w.getBoundingClientRect();
          var on = r.top + r.height / 2 < vh * 0.62;
          w.classList.toggle('is-on', on);
          if (on) lit = i;
        });
        if (window.__k2setLogo) window.__k2setLogo(lit);
      }

      // Подвал: «камни» К и 2 встают на место
      var gr = giant.getBoundingClientRect();
      var f = clamp((vh - gr.top) / (gr.height * 0.9), 0, 1);
      giant.style.setProperty('--f', f.toFixed(3));
    } else {
      giant.style.setProperty('--f', 1);
    }

    // Шкала высоты
    var max = document.documentElement.scrollHeight - vh;
    var g = clamp(y / Math.max(1, max), 0, 1);
    gauge.style.setProperty('--g-p', g.toFixed(4));
    gVal.textContent = (g * 13).toFixed(1);
    gauge.setAttribute('aria-valuenow', (g * 13).toFixed(1)); gauge.setAttribute('aria-valuetext', (g * 13).toFixed(1) + ' метров');
    gauge.classList.toggle('is-on', y > 240);
    var top = g > 0.995;
    if (top !== wasTop) { gauge.classList.toggle('is-top', top); wasTop = top; }

    ticking = false;
  }
  window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(frame); } }, { passive: true });
  frame();

  // Ленты едут навстречу друг другу; скорость растёт от скорости скролла, направление меняется вместе с ним
  var scrollDir = 1;
  function marquee() {
    if (Math.abs(vel) > 0.5) scrollDir = vel > 0 ? 1 : -1;
    var speed = 0.6 + Math.min(18, Math.abs(vel) * 0.6);
    bands.forEach(function (b) {
      if (b.paused || !b.w) return;
      b.x -= speed * b.dir * scrollDir;
      if (b.x <= -b.w) b.x += b.w;
      if (b.x > 0) b.x -= b.w;
      b.t.style.transform = 'translate3d(' + b.x.toFixed(2) + 'px,0,0)';
    });
    vel *= 0.94;
    requestAnimationFrame(marquee);
  }
  if (!reduce) requestAnimationFrame(marquee);
})();

/* ---------- ВРЕМЕННО: выбор акцентного цвета для согласования (?palette в адресе) ---------- */
(function () {
  var OPTIONS = [
    { id: 'deep',   name: 'Глубокий коралл (выбран)', red: '#D9493E', press: '#C23A30', on: '#FFFFFF' },
    { id: 'now',    name: 'Был красный',       red: '#FF261C', press: '#D61A12', on: '#FFFFFF' },
    { id: 'coral',  name: 'Коралл',            red: '#F0584A', press: '#E0493B', on: '#2D2D2D' },
    { id: 'dusty',  name: 'Пыльный коралл',    red: '#DE6B5F', press: '#CF5B4F', on: '#2D2D2D' },
    { id: 'soft',   name: 'Мягкий коралл',     red: '#EC6A5C', press: '#E05A4C', on: '#2D2D2D' },
    { id: 'pastel', name: 'Пастельный коралл', red: '#F28B7D', press: '#EA7A6B', on: '#2D2D2D' }
  ];
  var root = document.documentElement;
  function apply(o) {
    root.style.setProperty('--red', o.red);
    root.style.setProperty('--red-press', o.press);
    root.style.setProperty('--on-red', o.on);
  }
  var saved = null;
  try { saved = localStorage.getItem('k2-accent-v2'); } catch (e) {}
  var param = new URLSearchParams(location.search).get('accent');
  var cur = OPTIONS.filter(function (o) { return o.id === (param || saved); })[0];
  if (cur) apply(cur);
  if (!/[?&]palette/.test(location.search)) return;
  var box = document.createElement('div');
  box.className = 'pal';
  box.innerHTML = '<b>Акцентный цвет</b><div class="pal__list"></div>';
  var list = box.querySelector('.pal__list');
  OPTIONS.forEach(function (o) {
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'pal__o';
    btn.setAttribute('aria-pressed', String((cur || OPTIONS[0]).id === o.id));
    btn.innerHTML = '<span class="pal__sw" style="background:' + o.red + ';color:' + o.on + '">Аа</span><span>' + o.name + '<small>' + o.red + ' · текст ' + (o.on === '#FFFFFF' ? 'белый' : 'графит') + '</small></span>';
    btn.addEventListener('click', function () {
      apply(o);
      try { localStorage.setItem('k2-accent-v2', o.id); } catch (e) {}
      [].forEach.call(list.children, function (b) { b.setAttribute('aria-pressed', String(b === btn)); });
    });
    list.appendChild(btn);
  });
  document.body.appendChild(box);
})();
