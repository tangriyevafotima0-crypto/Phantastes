#!/usr/bin/env python3
"""Transliterate any stray Cyrillic characters to Uzbek Latin.
The translation must be 100% Latin; any Cyrillic that slips in is an artifact.
Usage: python3 fix_cyrillic.py <file>
"""
import sys

M = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "yo",
    "ж": "j", "з": "z", "и": "i", "й": "y", "к": "k", "л": "l", "м": "m",
    "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t", "у": "u",
    "ф": "f", "х": "x", "ц": "ts", "ч": "ch", "ш": "sh", "щ": "shch",
    "ъ": "'", "ы": "i", "ь": "", "э": "e", "ю": "yu", "я": "ya",
    "ғ": "g'", "қ": "q", "ҳ": "h", "ў": "o'", "ѓ": "g'",
}
# uppercase
for k in list(M):
    M[k.upper()] = M[k].upper() if len(M[k]) == 1 else M[k].capitalize()

path = sys.argv[1]
with open(path, encoding="utf-8") as f:
    text = f.read()

out = []
changed = 0
for ch in text:
    if ch in M:
        out.append(M[ch])
        changed += 1
    elif 0x0400 <= ord(ch) <= 0x04FF:
        # any other Cyrillic char not in map -> report
        out.append("?")
        changed += 1
        print("UNMAPPED Cyrillic:", repr(ch), hex(ord(ch)))
    else:
        out.append(ch)

with open(path, "w", encoding="utf-8") as f:
    f.write("".join(out))
print(f"Replaced {changed} Cyrillic characters in {path}")
