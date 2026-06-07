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
'і':'i','ї':'i','є':'e','ґ':"g'",'ѕ':'s','џ':'j','ј':'y','њ':'n','љ':'l',
'І':'I','Ї':'I','Є':'E','Ґ':"G'",
# Arabcha gliflar (vizual almashinish natijasida kirib qoladi)
'ا':'a','ب':'b','ت':'t','ث':'s','ج':'j','ح':'h','خ':'x','د':'d','ذ':'z',
'ر':'r','ز':'z','س':'s','ش':'sh','ص':'s','ض':'z','ط':'t','ظ':'z','ع':"'",
'غ':"g'",'ف':'f','ق':'q','ك':'k','ل':'l','م':'m','ن':'n','ه':'h','و':'o',
'ي':'i','ى':'i','ة':'a','ء':"'",'پ':'p','چ':'ch','ژ':'j','گ':'g','ک':'k','ی':'i','ۄ':'i','ۀ':'h','ے':'e',
}

files = sys.argv[1:] or sorted(glob.glob('Phantastes/translation/ch*.md'))
total = 0
def is_nonlatin(c):
    return ('\u0400' <= c <= '\u04FF') or ('\u0600' <= c <= '\u06FF') or ('\u0590' <= c <= '\u05FF')
for fn in files:
    txt = open(fn, encoding='utf-8').read()
    n = sum(1 for c in txt if is_nonlatin(c))
    if n:
        fixed = ''.join(M.get(c, c) for c in txt)
        open(fn, 'w', encoding='utf-8').write(fixed)
        rem = sum(1 for c in fixed if is_nonlatin(c))
        print(f'{fn}: fixed {n} non-latin chars, remaining {rem}')
        total += n
        if rem:
            t2 = open(fn, encoding='utf-8').read()
            for i, c in enumerate(t2):
                if is_nonlatin(c):
                    print(f'  !! leftover {c!r} (U+{ord(c):04X}) near: {t2[max(0,i-15):i+10]!r}')
if total == 0:
    print('Toza: begona harflar topilmadi.')
