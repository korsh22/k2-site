/* Скалодром К2 — переключатель языка RU / EN (все страницы).
   Английская версия — автоперевод Google Translate: кнопка .js-lang ставит cookie «googtrans=/ru/en» и перезагружает страницу;
   скрипт переводчика загружается ТОЛЬКО у тех, кто выбрал EN (остальным сторонний код не грузится).
   Чтобы текст не переводился (логотип, телефон, цены в рублях), у элемента — класс notranslate. */
(function () {
  'use strict';
  var COOKIE = 'googtrans';
  var read = function () { var m = document.cookie.match(/(?:^|;\s*)googtrans=([^;]+)/); return m ? decodeURIComponent(m[1]) : ''; };
  var isEn = /\/en$/.test(read());
  var write = function (val) {
    var host = location.hostname, tail = val ? '' : '; expires=Thu, 01 Jan 1970 00:00:00 GMT';
    var v = COOKIE + '=' + (val || '') + '; path=/' + tail;
    document.cookie = v;
    if (host.indexOf('.') > 0) { document.cookie = v + '; domain=' + host; document.cookie = v + '; domain=.' + host; }
  };
  var buttons = Array.prototype.slice.call(document.querySelectorAll('.js-lang'));
  buttons.forEach(function (b) {
    b.classList.add('notranslate');
    b.setAttribute('translate', 'no');
    var long = b.hasAttribute('data-long'), span = b.querySelector('span');
    var txt = long ? (isEn ? 'Русская версия' : 'English version') : (isEn ? 'RU' : 'EN');
    if (span) span.textContent = txt; else b.textContent = txt;
    b.setAttribute('aria-label', isEn ? 'Русская версия сайта' : 'English version (machine translation)');
    b.setAttribute('lang', isEn ? 'ru' : 'en');
    b.addEventListener('click', function () {
      write(isEn ? '' : '/ru/en');
      location.reload();
    });
  });
  if (!isEn) return;
  document.documentElement.classList.add('is-en');
  document.documentElement.setAttribute('lang', 'en');
  var box = document.createElement('div'); box.id = 'gt'; box.hidden = true; document.body.appendChild(box);
  window.k2GoogleTranslateInit = function () {
    /* global google */
    new google.translate.TranslateElement({ pageLanguage: 'ru', includedLanguages: 'en', autoDisplay: false }, 'gt');
  };
  var s = document.createElement('script');
  s.src = 'https://translate.google.com/translate_a/element.js?cb=k2GoogleTranslateInit';
  s.async = true;
  s.onerror = function () {  // переводчик недоступен (блокировка, нет сети) — вернуть русский, чтобы кнопка не «залипла»
    buttons.forEach(function (b) { b.title = 'Автоперевод сейчас недоступен'; });
  };
  document.head.appendChild(s);
})();
