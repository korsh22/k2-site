/* Скалодром К2 — корзина (все страницы).
   Хранение: localStorage, ключ «k2cart». Позиция: {id, kind, name, img, url, params[], unit, price, old, qty, max}.
     kind: training (тренировки, курсы, пробные) · event (мероприятия) · cert (сертификаты) · merch (товары).
   Кнопки «В корзину»: .js-cart-add с атрибутом data-cart='{…json позиции…}'.
   Значок в шапке: .hdr__cart .cart-n — число позиций в корзине.
   Страница корзины (korzina.html, #cart): таблица, промокод, оформление, «Оплатить» → банк → spasibo.html.
   ДЛЯ РАЗРАБОТЧИКА: цены, скидки и промокоды на сайте — только для показа. Итоговую сумму и промокод
   обязательно пересчитывает сервер при создании заказа, иначе их можно подменить в браузере. */
(function () {
  'use strict';
  var KEY = 'k2cart', ORDER_KEY = 'k2order', PROMO_KEY = 'k2promo';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var read = function (k, d) { try { var v = JSON.parse(localStorage.getItem(k)); return v == null ? d : v; } catch (e) { return d; } };
  var write = function (k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* приватный режим — корзина живёт до перезагрузки */ } };
  var mem = read(KEY, []);
  if (!Array.isArray(mem)) mem = [];
  var rub = function (n) { return Math.round(n).toLocaleString('ru-RU') + ' ₽'; };
  var esc = function (s) { var d = document.createElement('div'); d.textContent = s == null ? '' : String(s); return d.innerHTML; };
  // склонение: 1 позиция, 2 позиции, 5 позиций
  var plural = function (n, a, b, c) { var m = n % 10, h = n % 100; return m === 1 && h !== 11 ? a : m >= 2 && m <= 4 && (h < 12 || h > 14) ? b : c; };

  var Cart = {
    items: function () { return mem; },
    save: function () { write(KEY, mem); Cart.badge(); document.dispatchEvent(new CustomEvent('k2cart')); },
    key: function (it) { return it.id + '|' + (it.params || []).join('|'); },
    add: function (it, qty) {
      var k = Cart.key(it), found = mem.filter(function (x) { return Cart.key(x) === k; })[0];
      var max = it.max || 20;
      if (found) found.qty = Math.min(max, found.qty + (qty || 1));
      else mem.push({ id: it.id, kind: it.kind || 'training', name: it.name, img: it.img || '', url: it.url || '', params: it.params || [],
                      unit: it.unit || 'за штуку', price: +it.price || 0, old: +it.old || 0, qty: Math.min(max, qty || 1), max: max });
      Cart.save();
    },
    setQty: function (i, q) { if (!mem[i]) return; mem[i].qty = Math.max(1, Math.min(mem[i].max || 20, q)); Cart.save(); },
    remove: function (i) { mem.splice(i, 1); Cart.save(); },
    clear: function () { mem = []; Cart.save(); },
    count: function () { return mem.reduce(function (s, x) { return s + x.qty; }, 0); },
    badge: function () {
      var n = Cart.count();
      $$('.hdr__cart').forEach(function (a) {
        var b = $('.cart-n', a); if (b) { b.textContent = n > 99 ? '99+' : n; b.hidden = !n; }
        a.setAttribute('aria-label', n ? 'Корзина: ' + n + ' ' + plural(n, 'позиция', 'позиции', 'позиций') : 'Корзина пуста');
        a.classList.toggle('is-full', n > 0);
      });
    }
  };
  window.K2Cart = Cart;
  Cart.badge();
  window.addEventListener('storage', function (e) { if (e.key === KEY) { mem = read(KEY, []); Cart.badge(); document.dispatchEvent(new CustomEvent('k2cart')); } });

  /* ---------- Сообщение «Добавлено в корзину» ---------- */
  var toast;
  function showToast(name, base) {
    if (!toast) {
      toast = document.createElement('div'); toast.className = 'cart-toast'; toast.setAttribute('role', 'status'); toast.setAttribute('aria-live', 'polite');
      document.body.appendChild(toast);
    }
    toast.innerHTML = '<span class="cart-toast__ic" aria-hidden="true">✓</span><span><b>Добавлено в корзину</b><small>' + esc(name) + '</small></span>' +
      '<a class="btn btn--primary btn--sm" href="' + base + 'korzina.html">Перейти в корзину</a>';
    toast.classList.remove('is-on'); void toast.offsetWidth; toast.classList.add('is-on');
    clearTimeout(toast._t); toast._t = setTimeout(function () { toast.classList.remove('is-on'); }, 5000);
  }
  var base = (function () { var s = $('script[src*="js/cart.js"]'); return s ? s.getAttribute('src').replace(/js\/cart\.js.*$/, '') : ''; })();
  Cart.toast = function (name) { showToast(name, base); };

  /* ---------- Кнопки «В корзину» ---------- */
  $$('.js-cart-add').forEach(function (b) {
    b.addEventListener('click', function () {
      var it; try { it = JSON.parse(b.dataset.cart); } catch (e) { return; }
      // Варианты товара (.itp__vars): каждая группа должна быть выбрана; выбранное — в параметры позиции
      var vars = $('.itp__vars');
      if (vars) {
        var groups = $$('.itp__var', vars), miss = [], chosen = [];
        groups.forEach(function (g) {
          var c = $('input:checked', g), k = $('legend', g).textContent;
          if (c) chosen.push(k + ': ' + c.value.replace(/\u00a0/g, ' ')); else miss.push(k.toLowerCase());
        });
        var err = $('.itp__vars-err', vars);
        if (miss.length) {
          err.textContent = 'Выберите ' + miss.join(' и ') + ', чтобы добавить в корзину';
          err.hidden = false; vars.classList.add('is-bad');
          vars.scrollIntoView({ behavior: 'smooth', block: 'center' });
          var first = $('.itp__var input:not(:checked)', vars); if (first) setTimeout(function () { first.focus({ preventScroll: true }); }, 400);
          return;
        }
        err.hidden = true; vars.classList.remove('is-bad');
        it.params = (it.params || []).concat(chosen);
      }
      Cart.add(it, 1);
      showToast(it.name, base);
      if (b.dataset.cartDone) { if (!b.dataset.cartLabel) b.dataset.cartLabel = b.innerHTML; b.innerHTML = b.dataset.cartDone; }
      b.classList.add('is-added');
    });
  });

  // выбор варианта убирает подсказку «Выберите размер»
  $$('.itp__vars input').forEach(function (i) {
    i.addEventListener('change', function () {
      var v = $('.itp__vars'); if (!v || !$$('.itp__var', v).every(function (g) { return $('input:checked', g); })) return;
      v.classList.remove('is-bad'); $('.itp__vars-err', v).hidden = true;
      $$('.js-cart-add.is-added').forEach(function (b) { b.classList.remove('is-added'); if (b.dataset.cartLabel) b.innerHTML = b.dataset.cartLabel; });  // другой вариант — можно добавить снова
    });
  });

  /* ---------- Страница корзины ---------- */
  var root = $('#cart');
  if (!root) return;
  // Промокоды — ДЕМО. На сайте их проверяет сервер (адрес — атрибут data-promo-action у #cart).
  var PROMO = {
    'K2-10': { type: 'pct', v: 10, t: 'скидка 10%' },
    'START500': { type: 'sum', v: 500, t: 'скидка 500 ₽' },
    'LETO2026': { expired: true }
  };
  var promo = read(PROMO_KEY, null);
  var list = $('.cart__list', root), empty = $('.cart__empty', root), full = $('.cart__full', root);
  var pForm = $('.cart__promo', root), pIn = $('[name="promo"]', pForm), pMsg = $('.cart__promo-msg', root);

  function totals() {
    var base = 0, items = 0;
    mem.forEach(function (x) { items += x.price * x.qty; base += (x.old > x.price ? x.old : x.price) * x.qty; });
    var pd = 0;
    if (promo && PROMO[promo.code] && !PROMO[promo.code].expired) {
      var P = PROMO[promo.code]; pd = P.type === 'pct' ? Math.round(items * P.v / 100) : Math.min(items, P.v);
    }
    return { base: base, disc: base - items, items: items, promo: pd, total: Math.max(0, items - pd) };
  }
  function row(x, i) {
    var sale = x.old > x.price;
    var params = x.params && x.params.length ? '<ul class="cart__params">' + x.params.map(function (p) { return '<li>' + esc(p) + '</li>'; }).join('') + '</ul>' : '<span class="cart__none">—</span>';
    var name = x.url ? '<a class="cart__name" href="' + esc(x.url) + '">' + esc(x.name) + '</a>' : '<b class="cart__name">' + esc(x.name) + '</b>';
    return '<div class="cart__row" role="row" data-i="' + i + '">' +
      '<div class="cart__item" role="cell">' + (x.img ? '<img src="assets/img/' + esc(x.img) + '" alt="" loading="lazy">' : '<span class="cart__ph" aria-hidden="true"></span>') +
        '<span>' + name + '<span class="cart__kind">' + ({ training: 'Тренировка', event: 'Мероприятие', cert: 'Сертификат', merch: 'Товар' }[x.kind] || '') + '</span></span></div>' +
      '<div class="cart__opts" role="cell"><span class="cart__lbl">Параметры</span>' + params + '</div>' +
      '<div class="cart__unit" role="cell"><span class="cart__lbl">Цена</span>' + (sale ? '<s>' + rub(x.old) + '</s>' : '') + '<b>' + rub(x.price) + '</b><small>' + esc(x.unit) + '</small>' +
        (sale ? '<span class="cart__sale">−' + Math.round(100 - x.price * 100 / x.old) + '%</span>' : '') + '</div>' +
      '<div class="cart__qty" role="cell"><span class="cart__lbl">Количество</span><div class="step"><button type="button" class="step__b" data-d="-1" aria-label="Уменьшить количество: ' + esc(x.name) + '"' + (x.qty <= 1 ? ' disabled' : '') + '>−</button>' +
        '<output class="step__v" aria-live="polite">' + x.qty + '</output><button type="button" class="step__b" data-d="1" aria-label="Увеличить количество: ' + esc(x.name) + '"' + (x.qty >= (x.max || 20) ? ' disabled' : '') + '>+</button></div></div>' +
      '<div class="cart__sum" role="cell"><span class="cart__lbl">Сумма</span>' + (sale ? '<s>' + rub(x.old * x.qty) + '</s>' : '') + '<b>' + rub(x.price * x.qty) + '</b>' +
        (sale ? '<small class="cart__save">Скидка ' + rub((x.old - x.price) * x.qty) + '</small>' : '') + '</div>' +
      '<div class="cart__del" role="cell"><button type="button" class="cart__x" aria-label="Удалить из корзины: ' + esc(x.name) + '"><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M10 11v6M14 11v6M6 7l1 13h10l1-13M9 7V4h6v3"/></svg><span>Удалить</span></button></div>' +
      '</div>';
  }
  function render() {
    var n = mem.length;
    empty.hidden = !!n; full.hidden = !n;
    ($('.cart__count') || {}).textContent = n ? Cart.count() + ' ' + plural(Cart.count(), 'позиция', 'позиции', 'позиций') : '';
    list.innerHTML = mem.map(row).join('');
    var T = totals();
    $$('.js-t-base', root).forEach(function (e) { e.textContent = rub(T.base); });
    $$('.js-t-disc', root).forEach(function (e) { e.textContent = '−' + rub(T.disc); e.closest('.cart__line').hidden = !T.disc; });
    $$('.js-t-promo', root).forEach(function (e) { e.textContent = '−' + rub(T.promo); e.closest('.cart__line').hidden = !T.promo; });
    $$('.js-t-total', root).forEach(function (e) { e.textContent = rub(T.total); });
    var saved = T.disc + T.promo;
    $$('.js-t-saved', root).forEach(function (e) { e.hidden = !saved; e.textContent = 'Ваша выгода: ' + rub(saved) + (T.promo ? ' (в том числе по промокоду ' + promo.code + ' — ' + rub(T.promo) + ')' : ''); });
    // телефон обязателен для тренировок и мероприятий
    var needPhone = mem.some(function (x) { return x.kind === 'training' || x.kind === 'event'; });
    var ph = $('[name="phone"]', root); ph.required = needPhone;
    $('.cart__ph-opt', root).hidden = needPhone;
  }
  list.addEventListener('click', function (e) {
    var r = e.target.closest('.cart__row'); if (!r) return; var i = +r.dataset.i;
    var st = e.target.closest('.step__b'); if (st) { Cart.setQty(i, mem[i].qty + +st.dataset.d); return; }
    if (e.target.closest('.cart__x')) Cart.remove(i);
  });
  document.addEventListener('k2cart', render);

  // Промокод
  function promoMsg(t, ok) { pMsg.textContent = t; pMsg.className = 'cart__promo-msg ' + (ok ? 'is-ok' : 'is-bad'); pMsg.hidden = false; }
  pForm.addEventListener('submit', function (e) {
    e.preventDefault();
    var code = pIn.value.trim().toUpperCase();
    if (!code) { promoMsg('Введите промокод', false); pIn.focus(); return; }
    var P = PROMO[code];
    if (!P) { promoMsg('Промокод не найден. Проверьте, нет ли ошибки', false); return; }
    if (P.expired) { promoMsg('Срок действия промокода истёк', false); return; }
    promo = { code: code }; write(PROMO_KEY, promo);
    promoMsg('Промокод применён: ' + P.t, true); render();
  });
  var pDel = $('.cart__promo-del', root);
  if (pDel) pDel.addEventListener('click', function () { promo = null; write(PROMO_KEY, null); pIn.value = ''; pMsg.hidden = true; render(); });
  if (promo) { pIn.value = promo.code; promoMsg('Промокод применён: ' + (PROMO[promo.code] ? PROMO[promo.code].t : ''), true); }

  // «Добавить комментарий»
  var cBtn = $('.js-cart-comment', root), cBox = $('.cart__comment', root);
  if (cBtn) cBtn.addEventListener('click', function () { cBox.hidden = false; cBtn.hidden = true; $('textarea', cBox).focus(); });

  // Оформление: проверка полей → (разработчик: создать заказ на сервере и перейти на страницу банка) → spasibo.html
  var form = $('.cart__form', root);
  var phone = $('[name="phone"]', form);
  if (phone) {
    phone.addEventListener('focus', function () { if (!phone.value) phone.value = '+7 '; });
    phone.addEventListener('blur', function () { if (phone.value.replace(/\D/g, '').length <= 1) phone.value = ''; });
    phone.addEventListener('input', function () {
      var d = phone.value.replace(/\D/g, ''); if (d[0] === '8') d = '7' + d.slice(1); if (d[0] !== '7') d = '7' + d; d = d.slice(0, 11);
      var o = '+7'; if (d.length > 1) o += ' ' + d.slice(1, 4); if (d.length > 4) o += ' ' + d.slice(4, 7); if (d.length > 7) o += '-' + d.slice(7, 9); if (d.length > 9) o += '-' + d.slice(9, 11);
      phone.value = o;
    });
  }
  $$('input', form).forEach(function (inp) { inp.addEventListener('input', function () { inp.closest('.field') && inp.closest('.field').classList.remove('is-bad'); }); });
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!mem.length) return;
    var name = $('[name="name"]', form), mail = $('[name="email"]', form), agree = $('[name="agree"]', form);
    var ok = { name: !!name.value.trim(), phone: !phone.required ? !phone.value || phone.value.replace(/\D/g, '').length === 11 : phone.value.replace(/\D/g, '').length === 11,
               mail: /^\S+@\S+\.\S+$/.test(mail.value.trim()), agree: agree.checked };
    name.closest('.field').classList.toggle('is-bad', !ok.name);
    phone.closest('.field').classList.toggle('is-bad', !ok.phone);
    mail.closest('.field').classList.toggle('is-bad', !ok.mail);
    $('.field__err--agree', form).classList.toggle('is-on', !ok.agree);
    var first = !ok.name ? name : !ok.phone ? phone : !ok.mail ? mail : !ok.agree ? agree : null;
    if (first) { form.classList.remove('is-shake'); void form.offsetWidth; form.classList.add('is-shake'); first.focus(); return; }
    var T = totals();
    var order = { n: 'K2-' + String(Date.now()).slice(-6), date: new Date().toISOString(), items: mem, promo: promo && promo.code, totals: T,
                  buyer: { name: name.value.trim(), phone: phone.value, email: mail.value.trim(), comment: ($('[name="comment"]', form) || {}).value || '' } };
    var go = $('.cart__pay', form); go.disabled = true;
    // ЗДЕСЬ РАЗРАБОТЧИК: отправить order на сервер (data-action у формы), сервер пересчитывает суммы, создаёт заказ
    // и возвращает ссылку на оплату банка → window.location = paymentUrl. Банк после оплаты возвращает на spasibo.html?order=…
    var action = form.dataset.action;
    var finish = function () { write(ORDER_KEY, order); Cart.clear(); write(PROMO_KEY, null); window.location.href = 'spasibo.html?order=' + encodeURIComponent(order.n); };
    if (!action) { finish(); return; }
    fetch(action, { method: 'POST', headers: { 'Content-Type': 'application/json', 'X-Requested-With': 'XMLHttpRequest' }, body: JSON.stringify(order) })
      .then(function (r) { if (!r.ok) throw r; return r.json(); })
      .then(function (res) { write(ORDER_KEY, order); if (res && res.paymentUrl) window.location.href = res.paymentUrl; else finish(); })
      .catch(function () { go.disabled = false; var p = $('.cart__fail', form); if (p) p.hidden = false; });
  });
  render();
})();

/* ---------- Страница «Спасибо» (spasibo.html): номер и состав последнего заказа ---------- */
(function () {
  var box = document.getElementById('thanks'); if (!box) return;
  var o; try { o = JSON.parse(localStorage.getItem('k2order')); } catch (e) { o = null; }
  if (!o) return;
  var rub = function (n) { return Math.round(n).toLocaleString('ru-RU') + ' ₽'; };
  var esc = function (s) { var d = document.createElement('div'); d.textContent = s == null ? '' : String(s); return d.innerHTML; };
  box.querySelector('.thanks__n').textContent = o.n;
  box.querySelector('.thanks__mail').textContent = o.buyer && o.buyer.email || '';
  box.querySelector('.thanks__list').innerHTML = o.items.map(function (x) {
    return '<li><span><b>' + esc(x.name) + '</b>' + (x.params && x.params.length ? '<small>' + esc(x.params.join(' · ')) + '</small>' : '') + '</span><span>' + x.qty + ' × ' + rub(x.price) + '</span></li>';
  }).join('');
  box.querySelector('.thanks__total').textContent = rub(o.totals.total);
  box.querySelector('.thanks__order').hidden = false;
})();
