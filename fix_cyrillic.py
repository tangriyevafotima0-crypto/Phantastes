#!/usr/bin/env python3
"""Tarjima fayllariga tasodifan kirib qolgan kirill harflarini
o'zbek lotin ekvivalentiga almashtiradi. Har bob yozilgandan keyin ishlatiladi."""
import glob, sys

M = {
'а':'a','б':'b','в':'v','г':'g','д':'d','е':'e','ё':'yo','ж':'j','з':'z',
'и':'i','й':'y','к':'k','л':'l','м':'m','н':'n','о':'o','п':'p','р':'r',
'с':'s','т':'t','у':'u','ф':'f','х':'x','ц':'s','ч':'ch','ш':'sh','щ':'sh',
'ъ':"'",'ы':'i','ь':'','э':'e','ю':'yu','я':'ya',
'қ':'q','ғ':"g'",'ҳ':'h','ў':"o'",'Ў':"O'",'Қ':'Q','Ғ':"G'",'Ҳ':'H',
'А':'A','Б':'B','В':'V','Г':'G','Д':'D','Е':'E','Ж':'J','З':'Z','И':'I',
'К':'K','Л':'L','М':'M','Н':'N','О':'O','П':'P','Р':'R','С':'S','Т':'T',
'У':'U','Ф':'F','Х':'X','Ч':'Ch','Ш':'Sh','Э':'E','Ю':'Yu','Я':'Ya',
'Й':'Y','Ц':'S',
}

files = sys.argv[1:] or sorted(glob.glob('Phantastes/translation/ch*.md'))
total = 0
for fn in files:
    txt = open(fn, encoding='utf-8').read()
    n = sum(1 for c in txt if '\u0400' <= c <= '\u04FF')
    if n:
        fixed = ''.join(M.get(c, c) for c in txt)
        open(fn, 'w', encoding='utf-8').write(fixed)
        rem = sum(1 for c in fixed if '\u0400' <= c <= '\u04FF')
        print(f'{fn}: fixed {n} cyrillic chars, remaining {rem}')
        total += n
    # Arabic / other non-Latin detection (no auto-fix, just warn)
    txt2 = open(fn, encoding='utf-8').read()
    for i, c in enumerate(txt2):
        if '\u0600' <= c <= '\u06FF' or '\u0590' <= c <= '\u05FF':
            ctx = txt2[max(0, i-15):i+10]
            print(f'  !! {fn}: non-latin char {c!r} (U+{ord(c):04X}) near: {ctx!r}')
if total == 0:
    print('Toza: kirill harflari topilmadi.')
