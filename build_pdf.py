#!/usr/bin/env python3
"""Phantastes Part 2 — o'zbekcha tarjimani kitob PDF holatiga yig'uvchi skript.

translation/ch*.md fayllaridan o'qiydi va styled PDF yaratadi.
Markdown formati:
  # 71-bob: Sarlavha      -> bob sarlavhasi (yangi sahifa)
  oddiy matn              -> paragraf
  *kursiv*                -> ichki monolog (kursiv)
  bo'sh qator             -> paragraf ajratuvchi
"""
import os, re, glob
from fpdf import FPDF

FONT_DIR = os.path.join(os.path.dirname(__file__), '_fonts')
TR_DIR = os.path.join(os.path.dirname(__file__), 'translation')
OUT = os.path.join(os.path.dirname(__file__), 'Phantastes_part2_uzbek.pdf')

class Book(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font('Serif', 'I', 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 6, 'Phantastes — 2-qism', align='C')
        self.set_text_color(0, 0, 0)
        self.ln(8)

    def footer(self):
        if self.page_no() == 1:
            return
        self.set_y(-15)
        self.set_font('Serif', '', 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, str(self.page_no() - 1), align='C')
        self.set_text_color(0, 0, 0)


def render_inline(pdf, text, h, size):
    """Kursiv (*...*) bo'laklarni hisobga olib matnni chiqaradi."""
    parts = re.split(r'(\*[^*]+\*)', text)
    for p in parts:
        if not p:
            continue
        if p.startswith('*') and p.endswith('*') and len(p) > 1:
            pdf.set_font('Serif', 'I', size)
            pdf.write(h, p[1:-1])
        else:
            pdf.set_font('Serif', '', size)
            pdf.write(h, p)
    pdf.ln(h)


def build():
    pdf = Book(format='A5')
    pdf.set_margins(16, 16, 16)
    pdf.set_auto_page_break(True, margin=18)
    pdf.add_font('Serif', '', os.path.join(FONT_DIR, 'DejaVuSerif.ttf'))
    pdf.add_font('Serif', 'B', os.path.join(FONT_DIR, 'DejaVuSerif-Bold.ttf'))
    pdf.add_font('Serif', 'I', os.path.join(FONT_DIR, 'DejaVuSerif-Italic.ttf'))

    # --- Title page ---
    pdf.add_page()
    pdf.ln(40)
    pdf.set_font('Serif', 'B', 26)
    pdf.multi_cell(0, 14, 'PHANTASTES', align='C')
    pdf.ln(2)
    pdf.set_font('Serif', '', 14)
    pdf.multi_cell(0, 9, 'Ikkinchi qism', align='C')
    pdf.ln(20)
    pdf.set_font('Serif', 'I', 12)
    pdf.multi_cell(0, 8, '71–140-boblar', align='C')
    pdf.ln(30)
    pdf.set_font('Serif', '', 11)
    pdf.multi_cell(0, 7, "Ingliz tilidan o'zbek tiliga badiiy tarjima", align='C')

    files = sorted(glob.glob(os.path.join(TR_DIR, 'ch*.md')))
    body_size = 11.5
    line_h = 6.4
    for fn in files:
        with open(fn, encoding='utf-8') as f:
            lines = f.read().split('\n')
        i = 0
        # first non-empty line is the chapter heading
        pdf.add_page()
        first = True
        para_buf = []

        def flush():
            nonlocal para_buf
            if para_buf:
                text = ' '.join(para_buf).strip()
                if text:
                    render_inline(pdf, text, line_h, body_size)
                    pdf.ln(2)
                para_buf = []

        for ln in lines:
            s = ln.rstrip()
            if s.startswith('# '):
                flush()
                pdf.set_font('Serif', 'B', 15)
                pdf.set_text_color(80, 30, 30)
                pdf.multi_cell(0, 9, s[2:].strip())
                pdf.set_text_color(0, 0, 0)
                pdf.ln(4)
                first = False
            elif s.startswith('> '):
                # verse line: italic, indented, no joining
                flush()
                pdf.set_font('Serif', 'I', body_size)
                pdf.set_x(pdf.l_margin + 6)
                pdf.multi_cell(0, line_h, s[2:].strip())
            elif not s:
                flush()
            else:
                para_buf.append(s)
        flush()

    pdf.output(OUT)
    print('PDF yaratildi:', OUT)
    print('Sahifalar:', pdf.page_no())


if __name__ == '__main__':
    build()
