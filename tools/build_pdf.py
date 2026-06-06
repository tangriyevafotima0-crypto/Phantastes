#!/usr/bin/env python3
"""Build a book-quality PDF from the translated Uzbek markdown.

Input  : Phantastes_uzbek.md  (or a path passed as argv[1])
Output : Phantastes_uzbek.pdf (or argv[2])

Markdown conventions expected in the input:
  #BOOKTITLE: <title>          (once, optional)
  #BOOKSUBTITLE: <subtitle>    (once, optional)
  #BOOKAUTHOR: <author>        (once, optional)
  # BOB N: Title               -> chapter heading (starts new page)
  blank line                   -> paragraph separator
  everything else              -> body paragraph (justified)

Uses Noto Serif (downloaded into tools/fonts) for full Uzbek glyph coverage.
"""
import os
import sys
from fpdf import FPDF

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")


class Book(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A5")
        self.set_margins(left=18, top=20, right=18)
        self.set_auto_page_break(auto=True, margin=20)
        self.add_font("NotoSerif", "", os.path.join(FONTS, "NotoSerif-Regular.ttf"))
        self.add_font("NotoSerif", "B", os.path.join(FONTS, "NotoSerif-Bold.ttf"))
        self.add_font("NotoSerif", "I", os.path.join(FONTS, "NotoSerif-Italic.ttf"))
        self.add_font("NotoSerif", "BI", os.path.join(FONTS, "NotoSerif-BoldItalic.ttf"))
        self.running_title = ""
        self.in_frontmatter = True

    def header(self):
        if self.in_frontmatter:
            return
        self.set_font("NotoSerif", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, self.running_title, align="C")
        self.set_text_color(0, 0, 0)
        self.ln(10)

    def footer(self):
        if self.in_frontmatter:
            return
        self.set_y(-15)
        self.set_font("NotoSerif", "", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, str(self.page_no()), align="C")
        self.set_text_color(0, 0, 0)


def render(md_path, pdf_path):
    with open(md_path, encoding="utf-8") as f:
        lines = f.read().split("\n")

    title = "PHANTASTES"
    subtitle = ""
    author = ""
    content = []
    for ln in lines:
        if ln.startswith("#BOOKTITLE:"):
            title = ln.split(":", 1)[1].strip()
        elif ln.startswith("#BOOKSUBTITLE:"):
            subtitle = ln.split(":", 1)[1].strip()
        elif ln.startswith("#BOOKAUTHOR:"):
            author = ln.split(":", 1)[1].strip()
        else:
            content.append(ln)

    pdf = Book()

    # ---- Title page ----
    pdf.in_frontmatter = True
    pdf.add_page()
    pdf.ln(45)
    pdf.set_font("NotoSerif", "B", 30)
    pdf.multi_cell(0, 14, title, align="C")
    pdf.ln(4)
    if subtitle:
        pdf.set_font("NotoSerif", "I", 14)
        pdf.multi_cell(0, 9, subtitle, align="C")
    pdf.ln(60)
    if author:
        pdf.set_font("NotoSerif", "", 12)
        pdf.multi_cell(0, 8, author, align="C")

    # ---- Body ----
    pdf.in_frontmatter = False
    para_buf = []

    def flush_para():
        if not para_buf:
            return
        text = " ".join(s.strip() for s in para_buf).strip()
        para_buf.clear()
        if not text:
            return
        pdf.set_font("NotoSerif", "", 11)
        # first-line indent via leading spaces is unreliable; use a small indent cell row
        pdf.multi_cell(0, 6.4, text, align="J")
        pdf.ln(1.6)

    for ln in content:
        s = ln.rstrip()
        if s.startswith("# BOB") or s.startswith("# "):
            flush_para()
            heading = s.lstrip("#").strip()
            pdf.add_page()
            pdf.running_title = heading
            pdf.ln(6)
            pdf.set_font("NotoSerif", "B", 16)
            pdf.multi_cell(0, 9, heading, align="C")
            pdf.ln(6)
            continue
        if s.strip() == "":
            flush_para()
        else:
            para_buf.append(s)
    flush_para()

    pdf.output(pdf_path)
    print("Wrote", pdf_path, "pages:", pdf.page_no())


if __name__ == "__main__":
    md = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "Phantastes_uzbek.md")
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "Phantastes_uzbek.pdf")
    render(md, out)
