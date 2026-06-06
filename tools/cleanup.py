#!/usr/bin/env python3
"""Robust post-batch cleanup for the Uzbek translation file.
- Transliterates stray Cyrillic to Uzbek Latin.
- Fixes stray Latin-extended / Arabic / Indic characters.
- Reorders chapters by number and removes duplicate chapter numbers
  (keeps the longest version if duplicates differ).
- Reports remaining non-ASCII artifacts and chapter count.
Usage: python3 cleanup.py <file>
"""
import re
import sys

CYR = {
    "а": "a", "б": "b", "в": "v", "г": "g", "ғ": "g'", "д": "d", "е": "e", "ё": "yo",
    "ж": "j", "з": "z", "и": "i", "й": "y", "к": "k", "қ": "q", "л": "l", "м": "m",
    "н": "n", "о": "o", "ў": "o'", "п": "p", "р": "r", "с": "s", "т": "t", "у": "u",
    "ф": "f", "х": "x", "ҳ": "h", "ц": "ts", "ч": "ch", "ш": "sh", "щ": "shch",
    "ъ": "'", "ы": "i", "ь": "", "э": "e", "ю": "yu", "я": "ya", "ѓ": "g'",
}
for k in list(CYR):
    u = CYR[k]
    CYR[k.upper()] = u.upper() if len(u) == 1 else u.capitalize()

# stray latin-extended / arabic / indic -> latin
MISC = {
    "ı": "i", "İ": "I", "ş": "sh", "Ş": "Sh", "ç": "ch", "Ç": "Ch",
    "ğ": "g'", "Ğ": "G'", "ə": "a", "Ə": "A",
    "ا": "a", "ن": "n", "ي": "i", "د": "d", "ر": "r", "ل": "l", "م": "m",
    "ت": "t", "ب": "b", "ك": "k", "گ": "g", "ق": "q", "س": "s", "ه": "h",
    "و": "o", "ع": "a",
    "ా": "a", "ి": "i", "న": "n", "గ": "g", "ర": "r", "ల": "l",
    "ा": "a", "ी": "i", "न": "n", "ग": "g",
}

ALLOWED = set("’‘“”—…–'£")


def translit(s):
    out = []
    for ch in s:
        if ch in CYR:
            out.append(CYR[ch])
        elif ch in MISC:
            out.append(MISC[ch])
        else:
            out.append(ch)
    return "".join(out)


def reorder(s):
    m = re.search(r"^# BOB \d+:", s, re.MULTILINE)
    if not m:
        return s
    front = s[:m.start()].rstrip("\n")
    body = s[m.start():]
    parts = re.split(r"(?m)^(# BOB (\d+):.*)$", body)
    blocks = {}
    i = 1
    while i < len(parts):
        heading, num, text = parts[i], int(parts[i + 1]), parts[i + 2]
        full = (heading + text).rstrip("\n")
        if num in blocks and len(blocks[num]) >= len(full):
            pass  # keep longer existing
        else:
            blocks[num] = full
        i += 3
    return front + "\n\n" + "\n\n".join(blocks[n] for n in sorted(blocks)) + "\n", sorted(blocks)


def main():
    path = sys.argv[1]
    s = open(path, encoding="utf-8").read()
    s = translit(s)
    s, chapters = reorder(s)
    open(path, "w", encoding="utf-8").write(s)
    rem = {}
    for ch in s:
        if ord(ch) > 127 and ch not in ALLOWED:
            rem[ch] = rem.get(ch, 0) + 1
    print("chapters:", len(chapters), "range:", chapters[0], "-", chapters[-1])
    # check contiguous
    missing = [n for n in range(chapters[0], chapters[-1] + 1) if n not in chapters]
    print("missing:", missing if missing else "none")
    print("non-ascii artifacts:", rem if rem else "NONE")


if __name__ == "__main__":
    main()
