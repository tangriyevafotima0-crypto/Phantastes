#!/usr/bin/env python3
"""Remove duplicated chapter sections, keeping the FIRST occurrence of each
'# BOB N:' heading. Any later section whose chapter number was already seen
is dropped (until the next new heading). Front-matter before the first
heading is preserved.
"""
import re
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "Phantastes_uzbek.md"
with open(path, encoding="utf-8") as f:
    lines = f.read().split("\n")

head_re = re.compile(r"^# BOB (\d+):")
out = []
seen = set()
skipping = False
removed = 0
for ln in lines:
    m = head_re.match(ln)
    if m:
        num = int(m.group(1))
        if num in seen:
            skipping = True
            removed += 1
            continue
        else:
            seen.add(num)
            skipping = False
            out.append(ln)
            continue
    if not skipping:
        out.append(ln)

# collapse 3+ blank lines to exactly 2
text = "\n".join(out)
text = re.sub(r"\n{4,}", "\n\n\n", text)
with open(path, "w", encoding="utf-8") as f:
    f.write(text)

print(f"Removed {removed} duplicate chapter section(s).")
print("Chapters now:", len(seen))
