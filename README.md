# Скалодром К2 — сайт (превью)

- `site/` — готовый статичный сайт; публикуется на GitHub Pages автоматически при пуше в `main`.
- `tools/` — генераторы страниц: `build_pages.py` («Первый раз»), `build_blog.py` (блог), `build_site.py` (внутренние страницы и PDF прайса), `build_modx.py` (пакет для MODX).

Порядок сборки: `build_pages.py` → `build_blog.py` → `build_site.py`.
