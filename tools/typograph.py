"""Типограф для index.html.
- неразрывный пробел после служебных слов (предлоги, союзы, частицы): «в К2», «и тренеры»;
- неразрывный пробел между числом и единицей: «13 метров», «7 минут»;
- неразрывный пробел перед тире;
- «1–3», «6–9» не разрываются на тире;
- слова через дефис («Санкт-Петербурга», «PRO-команда») не разрываются на дефисе.
Обрабатывается только текст между тегами; <script>, <style>, атрибуты и комментарии не трогаются."""
import io, re, sys

NB = ' '
WJ = '⁠'  # word joiner — запрет переноса без видимого символа
SHORT = 'в во на с со к ко у о об обо и а но да по за из от до не ни для без при под над про или же ли бы'.split()
LET = 'A-Za-zА-Яа-яЁё'
SHORT_RE = re.compile(r'(?<![' + LET + r'\-])(' + '|'.join(sorted(SHORT, key=len, reverse=True)) + r') (?=\S)', re.I)
UNITS = r'(м²|м|мин|минут|минуты|метров|метра|человек|лет|года|год|участников|тренировок|тренировки|тренировка|занятий|месяца|месяцев|₽|руб)'
NUM_UNIT = re.compile(r'(\d) (?=' + UNITS + r'(?![' + LET + r']))')
DASH = re.compile(r' (—)')
NUM_DASH_NUM = re.compile(r'(\d)–(\d)')
HYPH = re.compile(r'[' + LET + r']+(?:-[' + LET + r']+)+')

def fix_text(t):
    if not t.strip():
        return t
    t = t.replace('&nbsp;', NB)
    prev = None
    while prev != t:
        prev = t
        t = SHORT_RE.sub(lambda m: m.group(1) + NB, t)
    t = NUM_UNIT.sub(lambda m: m.group(1) + NB, t)
    t = DASH.sub(lambda m: NB + m.group(1), t)
    t = NUM_DASH_NUM.sub(lambda m: m.group(1) + WJ + '–' + WJ + m.group(2), t)
    t = HYPH.sub(lambda m: m.group(0).replace('-', '-' + WJ), t)
    return t

def process(html):
    out, i = [], 0
    token = re.compile(r'(<script\b.*?</script>|<style\b.*?</style>|<!--.*?-->|<title>.*?</title>|<[^>]+>)', re.S | re.I)
    for m in token.finditer(html):
        out.append(fix_text(html[i:m.start()]))
        out.append(m.group(0))
        i = m.end()
    out.append(fix_text(html[i:]))
    return ''.join(out).replace(NB, '&nbsp;')

if __name__ == '__main__':
    src_path, dst_path = sys.argv[1], sys.argv[2]
    src = io.open(src_path, encoding='utf-8').read()
    res = process(src)
    io.open(dst_path, 'w', encoding='utf-8').write(res)
    print('nbsp:', res.count('&nbsp;'), '| слов через дефис:', res.count('-' + WJ), '| диапазонов:', res.count(WJ + '–'))
