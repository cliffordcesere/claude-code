#!/usr/bin/env python3
"""
Compose le dossier éditorial complet en PDF lisible (A4, sommaire paginé,
tableaux, accents et guillemets français corrects).

Usage : python3 md2pdf.py sortie.pdf fichier1.md fichier2.md ...
"""
import os
import re
import sys

import matplotlib
from fpdf import FPDF
from fpdf.fonts import FontFace

FONTS = os.path.join(os.path.dirname(matplotlib.__file__), "mpl-data", "fonts", "ttf")

INK = (18, 18, 18)
GREY = (105, 105, 105)
RULE = (205, 200, 195)
ACCENT = (107, 43, 43)

BODY = "Serif"
HEAD = "Sans"


# ---------------------------------------------------------------- nettoyage
REPLACED = {
    "\u2019": "\u2019", "\u02b3": "r", "\u1d49": "e", "\u00d7": "\u00d7",
    "\u2192": "\u2192", "\u2264": "\u2264", "\u00a0": " ",
}


def clean(s):
    for k, v in REPLACED.items():
        s = s.replace(k, v)
    s = s.replace("\t", " ")
    return s.strip()


INLINE = re.compile(r"(\*\*.+?\*\*|\*[^*\n]+?\*|`[^`\n]+?`)")


def segments(text):
    """Découpe un paragraphe en (texte, gras, italique), espaces préservés."""
    out = []
    for part in INLINE.split(text):
        if not part:
            continue
        bold = italic = False
        if part.startswith("**") and part.endswith("**") and len(part) > 4:
            part, bold = part[2:-2], True
        elif part.startswith("*") and part.endswith("*") and len(part) > 2:
            part, italic = part[1:-1], True
        elif part.startswith("`") and part.endswith("`") and len(part) > 2:
            part = part[1:-1]
        part = part.replace("\u00a0", " ")
        if part:
            out.append((part, bold, italic))
    return out


def strip_md(text):
    t = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    t = re.sub(r"(?<!\*)\*([^*\n]+?)\*(?!\*)", r"\1", t)
    t = re.sub(r"`([^`\n]+?)`", r"\1", t)
    return clean(t)


# ---------------------------------------------------------------- document
class Dossier(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_margins(22, 22, 22)
        self.set_auto_page_break(True, margin=27)
        self.add_font(BODY, "", os.path.join(FONTS, "DejaVuSerif.ttf"))
        self.add_font(BODY, "B", os.path.join(FONTS, "DejaVuSerif-Bold.ttf"))
        self.add_font(BODY, "I", os.path.join(FONTS, "DejaVuSerif-Italic.ttf"))
        self.add_font(BODY, "BI", os.path.join(FONTS, "DejaVuSerif-BoldItalic.ttf"))
        self.add_font(HEAD, "", os.path.join(FONTS, "DejaVuSans.ttf"))
        self.add_font(HEAD, "B", os.path.join(FONTS, "DejaVuSans-Bold.ttf"))
        self.add_font(HEAD, "I", os.path.join(FONTS, "DejaVuSans-Oblique.ttf"))
        self.add_font(HEAD, "BI", os.path.join(FONTS, "DejaVuSans-BoldOblique.ttf"))
        self.set_font(BODY, "", 10)
        self.set_text_color(*INK)
        self._running = ""

    # -- footer
    def footer(self):
        if self.page_no() == 1:
            return
        self.set_y(-15)
        self.set_font(HEAD, "", 7.5)
        self.set_text_color(*GREY)
        left = self._running
        self.cell(0, 5, left, align="L")
        self.set_x(-40)
        self.cell(18, 5, str(self.page_no() - 1), align="R")

    # -- helpers
    def rule(self, w=None, gap=2.4, color=RULE):
        if self.get_y() > 255:
            self.add_page()
        self.set_draw_color(*color)
        self.set_line_width(0.25)
        y = self.get_y() + gap
        self.line(self.l_margin, y, self.l_margin + (w or self.epw), y)
        self.set_y(y + gap)

    def _tokens(self, text):
        toks = []
        for seg, bold, italic in segments(text):
            for ch in re.split(r"(\s+)", seg):
                if ch:
                    toks.append((ch, bold, italic))
        return toks

    def _style(self, size, bold, italic):
        st = ("B" if bold else "") + ("I" if italic else "")
        st = {"IB": "BI"}.get(st, st)
        self.set_font(BODY, st, size)

    def _lines(self, tokens, width, size):
        lines, cur, curw = [], [], 0.0
        for tok, bold, italic in tokens:
            if tok.isspace():
                if cur:
                    cur.append((tok, bold, italic, self.get_string_width(tok)))
                    curw += cur[-1][3]
                continue
            self._style(size, bold, italic)
            w = self.get_string_width(tok)
            if cur and curw + w > width:
                while cur and cur[-1][0].isspace():
                    curw -= cur[-1][3]
                    cur.pop()
                lines.append(cur)
                cur, curw = [], 0.0
            cur.append((tok, bold, italic, w))
            curw += w
        if cur:
            lines.append(cur)
        return lines

    def para(self, text, size=10, lh=5.3, style="", color=INK, indent=0.0,
             space_after=3.0, align="L"):
        if not text.strip():
            return
        width = self.epw - indent
        lines = self._lines(self._tokens(text), width, size)
        if not lines:
            return
        if self.get_y() + len(lines) * lh > self.page_break_trigger:
            self.add_page()
        self.set_text_color(*color)
        auto = self.auto_page_break
        self.set_auto_page_break(False)
        for line in lines:
            if self.get_y() + lh > self.page_break_trigger:
                self.add_page()
                self.set_text_color(*color)
            x = self.l_margin + indent
            y = self.get_y()
            total = sum(f[3] for f in line)
            if align == "C":
                x += (width - total) / 2
            for tok, bold, italic, w in line:
                self._style(size, bold, italic)
                if style:
                    self.set_font(BODY, style, size)
                self.cell(w, lh, tok, align="L",
                          new_x="RIGHT", new_y="TOP")
                self.set_xy(x + w if False else self.get_x(), y)
            self.set_xy(self.l_margin, y + lh)
        self.set_auto_page_break(auto, margin=27)
        self.ln(space_after)

    def bullets(self, items, numbered=False):
        for i, it in enumerate(items, 1):
            marker = ("%d." % i) if numbered else "\u2013"
            width = self.epw - 7
            lines = self._lines(self._tokens(it), width, 10)
            if self.get_y() + len(lines) * 5.3 > self.page_break_trigger:
                self.add_page()
            self.set_text_color(*INK)
            self.set_font(BODY, "", 10)
            auto = self.auto_page_break
            self.set_auto_page_break(False)
            self.set_xy(self.l_margin, self.get_y())
            self.cell(7, 5.3, marker, align="L", new_x="RIGHT", new_y="TOP")
            y0 = self.get_y()
            for j, line in enumerate(lines):
                self.set_xy(self.l_margin + 7, y0 + j * 5.3)
                for tok, bold, italic, w in line:
                    self._style(10, bold, italic)
                    self.cell(w, 5.3, tok, align="L", new_x="RIGHT", new_y="TOP")
                    self.set_y(y0 + j * 5.3)
            self.set_auto_page_break(auto, margin=27)
            self.set_xy(self.l_margin, y0 + len(lines) * 5.3)
            self.ln(1.6)

    def h1(self, text, toc_title=None):
        self._running = strip_md(text)
        self.add_page()
        self.start_section(toc_title or strip_md(text), level=0)
        self.set_font(HEAD, "B", 17)
        self.set_text_color(*ACCENT)
        self.multi_cell(0, 7.8, strip_md(text), align="L")
        self.rule(gap=3.0, color=ACCENT)
        self.ln(3)

    def h2(self, text):
        self.start_section(strip_md(text), level=1)
        self.need(18)
        self.ln(2)
        self.set_font(HEAD, "B", 12)
        self.set_text_color(*INK)
        self.multi_cell(0, 6, strip_md(text), align="L")
        self.ln(2)

    def h3(self, text):
        self.need(14)
        self.set_font(HEAD, "B", 10)
        self.set_text_color(*GREY)
        self.multi_cell(0, 5.2, strip_md(text), align="L")
        self.ln(1.2)

    def need(self, h):
        if self.get_y() + h > self.page_break_trigger:
            self.add_page()

    def bullets(self, items, numbered=False):
        for i, it in enumerate(items, 1):
            self.set_font(BODY, "", 10)
            nl = len(self.multi_cell(self.epw - 7, 5.3, strip_md(it),
                                     dry_run=True, output="LINES"))
            if self.get_y() + nl * 5.3 > self.page_break_trigger:
                self.add_page()
            marker = ("%d." % i) if numbered else "\u2013"
            self.set_text_color(*INK)
            self.set_font(BODY, "", 10)
            self.set_x(self.l_margin)
            self.cell(7, 5.3, marker, align="L")
            x0 = self.l_margin
            old_lm = self.l_margin
            self.set_left_margin(old_lm + 7)
            self.set_x(old_lm + 7)
            for seg, bold, italic in segments(it):
                st = ("B" if bold else "") + ("I" if italic else "")
                st = {"IB": "BI"}.get(st, st)
                self.set_font(BODY, st, 10)
                self.write(5.3, seg)
            self.ln(5.3)
            self.set_left_margin(old_lm)
            self.set_x(old_lm)
            self.ln(1.6)

    def render_table(self, rows):
        if not rows:
            return
        ncols = max(len(r) for r in rows)
        rows = [r + [""] * (ncols - len(r)) for r in rows]
        if ncols == 1:
            for r in rows:
                self.para(r[0])
            return
        widths = {
            2: (34, 66),
            3: (26, 30, 44),
            4: (16, 18, 22, 44),
        }.get(ncols)
        if widths is None:
            base = 100.0 / ncols
            widths = tuple([base] * ncols)
        total = sum(widths)
        widths = tuple(w * self.epw / total for w in widths)

        self.need(16)
        self.set_font(HEAD, "", 7.6)
        self.set_draw_color(*RULE)
        self.set_line_width(0.2)
        with self.table(
            col_widths=widths,
            text_align="LEFT",
            line_height=4.1,
            first_row_as_headings=True,
            headings_style=FontFace(family=HEAD, emphasis="BOLD", size_pt=7.6,
                                     fill_color=(238, 234, 229), color=INK),
            borders_layout="HORIZONTAL_LINES",
            padding=1.1,
        ) as t:
            for i, r in enumerate(rows):
                row = t.row()
                for c in r:
                    row.cell(strip_md(c) if i else strip_md(c).upper())
        self.ln(3.5)


# ---------------------------------------------------------------- parseur
def parse_blocks(path):
    """Transforme un fichier MD en liste de blocs typés."""
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    blocks = []
    i = 0
    buf = []
    while i < len(lines):
        s = clean(lines[i])
        if not s:
            if buf:
                blocks.append(("p", " ".join(buf)))
                buf = []
            i += 1
            continue
        if s.startswith("# "):
            if buf:
                blocks.append(("p", " ".join(buf)))
                buf = []
            blocks.append(("h1", s[2:]))
            i += 1
            continue
        if s.startswith("## "):
            if buf:
                blocks.append(("p", " ".join(buf)))
                buf = []
            blocks.append(("h2", s[3:]))
            i += 1
            continue
        if s.startswith("### "):
            if buf:
                blocks.append(("p", " ".join(buf)))
                buf = []
            blocks.append(("h3", s[4:]))
            i += 1
            continue
        if set(s) <= {"-", " "} and len(s) >= 3:
            if buf:
                blocks.append(("p", " ".join(buf)))
                buf = []
            blocks.append(("rule", ""))
            i += 1
            continue
        if s.startswith("|"):
            if buf:
                blocks.append(("p", " ".join(buf)))
                buf = []
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                r = lines[i].strip()
                if not re.match(r"^\|[\s:\-|]+\|$", r):
                    rows.append([c.strip() for c in r.strip("|").split("|")])
                i += 1
            blocks.append(("table", rows))
            continue
        if s.startswith("> "):
            if buf:
                blocks.append(("p", " ".join(buf)))
                buf = []
            blocks.append(("quote", s[2:]))
            i += 1
            continue
        m = re.match(r"^(-|\d+\.)\s+(.*)$", s)
        if m:
            if buf:
                blocks.append(("p", " ".join(buf)))
                buf = []
            items = []
            numbered = m.group(1) != "-"
            while i < len(lines):
                t = clean(lines[i])
                m2 = re.match(r"^(-|\d+\.)\s+(.*)$", t)
                if not m2:
                    break
                items.append(m2.group(2))
                i += 1
            blocks.append(("list", (items, numbered)))
            continue
        buf.append(s)
        i += 1
    if buf:
        blocks.append(("p", " ".join(buf)))
    return blocks


def render_blocks(pdf, blocks, record=None):
    for kind, payload in blocks:
        if kind == "h1":
            pdf.h1(payload)
            if record is not None:
                record.append((strip_md(payload), 0, pdf.page_no()))
        elif kind == "h2":
            pdf.h2(payload)
            if record is not None:
                record.append((strip_md(payload), 1, pdf.page_no()))
        elif kind == "h3":
            pdf.h3(payload)
        elif kind == "rule":
            pdf.rule()
        elif kind == "table":
            pdf.render_table(payload)
        elif kind == "quote":
            pdf.ln(1)
            pdf.para(payload, size=9.5, color=GREY, indent=7, style="I")
        elif kind == "list":
            items, numbered = payload
            pdf.bullets(items, numbered=numbered)
        else:
            pdf.para(payload)


def build(src_paths, out_path, title="Dossier editorial", subtitle=None):
    parsed = [parse_blocks(p) for p in src_paths]

    # --- passe 1 : pagination du corps seul
    probe = Dossier()
    probe.add_page()
    toc = []
    for blocks in parsed:
        render_blocks(probe, blocks, record=toc)
    body_pages = probe.page_no()

    toc_pages = max(1, -(-len(toc) // 28))

    # --- passe 2 : document final
    pdf = Dossier()
    pdf.add_page()  # couverture
    pdf.set_y(80)
    pdf.set_font(HEAD, "", 10)
    pdf.set_text_color(*GREY)
    pdf.multi_cell(0, 6, "CE QUE JE TE DOIS", align="C")
    pdf.ln(6)
    pdf.set_font(HEAD, "B", 27)
    pdf.set_text_color(*INK)
    pdf.multi_cell(0, 13, title, align="C")
    pdf.ln(3)
    pdf.set_font(BODY, "I", 12)
    pdf.set_text_color(*GREY)
    pdf.multi_cell(0, 7, subtitle or "Bible v6.0, charte v1.0.0, manuscrit", align="C")
    pdf.ln(10)
    pdf.set_font(BODY, "", 9.5)
    pdf.multi_cell(0, 5.6,
                   "Note de lecture \u00b7 Audit du manuscrit \u00b7 Feuille de d\u00e9cisions\n"
                   "Traduction des six sc\u00e8nes \u00b7 Continuit\u00e9 et motifs \u00b7 Grille d'audit\n"
                   "Note pour l'\u00e9diteur",
                   align="C")
    pdf.set_y(-40)
    pdf.set_font(HEAD, "", 9)
    pdf.set_text_color(*GREY)
    pdf.multi_cell(0, 5, "22 octobre 2026", align="C")

    # sommaire
    per_page = 28
    offset = toc_pages - 1  # la couverture n'est pas numerotee
    for tp in range(toc_pages):
        pdf.add_page()
        pdf.set_auto_page_break(False)
        pdf.set_x(pdf.l_margin)
        pdf.set_font(HEAD, "B", 13)
        pdf.set_text_color(*INK)
        pdf.multi_cell(pdf.epw, 8, "Sommaire" if tp == 0 else "Sommaire (suite)",
                       new_x="LMARGIN", new_y="NEXT")
        pdf.ln(4)
        for label, level, page in toc[tp * per_page:(tp + 1) * per_page]:
            indent = 0 if level == 0 else 6
            pdf.set_x(pdf.l_margin + indent)
            pdf.set_font(HEAD, "B" if level == 0 else "", 9.5 if level == 0 else 8.6)
            pdf.set_text_color(*(INK if level == 0 else GREY))
            if len(label) > 92:
                label = label[:89] + "\u2026"
            avail = pdf.epw - indent - 12
            pdf.cell(avail, 6.2, label)
            pdf.cell(12, 6.2, str(page + offset), align="R",
                     new_x="LMARGIN", new_y="NEXT")
        pdf.set_auto_page_break(True, margin=27)

    # corps
    for blocks in parsed:
        render_blocks(pdf, blocks)

    pdf.output(out_path)
    return pdf.page_no()


if __name__ == "__main__":
    out = sys.argv[1]
    srcs = sys.argv[2:]
    title = os.environ.get("PDF_TITLE", "Dossier \u00e9ditorial")
    subtitle = os.environ.get("PDF_SUBTITLE") or None
    n = build(srcs, out, title=title, subtitle=subtitle)
    print("\u00e9crit :", out, "|", n, "pages")
