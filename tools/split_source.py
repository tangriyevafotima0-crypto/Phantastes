#!/usr/bin/env python3
"""Clean the noisy extracted source and split it into per-chapter files.

Removes:
  - "## Sahifa N" page markers
  - "---" horizontal rules
  - standalone "Phantastes" footer lines
Then splits on "Chapter N: Title" headings into chapters/ch_XXX.txt
Also reflows paragraphs: the source hard-wraps lines mid-sentence, so we
join lines into paragraphs (blank line = paragraph break).
"""
import os
import re

SRC = os.path.join(os.path.dirname(__file__), "..", "Phantastes_tahrirlangan.md")
OUT = os.path.join(os.path.dirname(__file__), "..", "chapters_src")
os.makedirs(OUT, exist_ok=True)

with open(SRC, encoding="utf-8") as f:
    raw_lines = f.readlines()

clean = []
for ln in raw_lines:
    s = ln.rstrip("\n")
    st = s.strip()
    if st.startswith("## Sahifa"):
        clean.append("")  # treat page break as a soft separator
        continue
    if st == "---":
        continue
    if st == "Phantastes":
        continue
    # Strip dash-form chapter lines: "Chapter N - Title" (TOC entries / page-header repeats).
    # Keep colon-form "Chapter N: Title" which marks the real chapter starts.
    if re.match(r"^Chapter \d+ - ", st):
        continue
    clean.append(s)

text = "\n".join(clean)

# Find chapter headings of form "Chapter N: Title"
heading_re = re.compile(r"^Chapter (\d+):\s*(.*)$", re.MULTILINE)
matches = list(heading_re.finditer(text))
print(f"Found {len(matches)} chapter headings")

index_lines = []
for i, m in enumerate(matches):
    num = int(m.group(1))
    title = m.group(2).strip()
    start = m.end()
    end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
    body = text[start:end]

    # Reflow: collapse single newlines into spaces, keep blank-line paragraph breaks
    paras = re.split(r"\n\s*\n", body)
    reflowed = []
    for p in paras:
        joined = " ".join(seg.strip() for seg in p.split("\n") if seg.strip())
        joined = re.sub(r"\s+", " ", joined).strip()
        if joined:
            reflowed.append(joined)
    body_clean = "\n\n".join(reflowed)

    fn = os.path.join(OUT, f"ch_{num:03d}.txt")
    with open(fn, "w", encoding="utf-8") as fo:
        fo.write(f"Chapter {num}: {title}\n\n")
        fo.write(body_clean + "\n")

    wc = len(body_clean.split())
    index_lines.append((num, title, wc))

with open(os.path.join(OUT, "_index.tsv"), "w", encoding="utf-8") as fo:
    total = 0
    for num, title, wc in index_lines:
        fo.write(f"{num}\t{title}\t{wc}\n")
        total += wc
    fo.write(f"#TOTAL\t-\t{total}\n")

print("Wrote", len(index_lines), "chapters")
print("Total words:", sum(wc for _, _, wc in index_lines))
