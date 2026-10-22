#!/usr/bin/env python3
"""
Génère une version HTML d'un seul tenant, en lecture confortable sur téléphone
(reflow, colonne étroite, mode sombre automatique).

Usage : python3 md2html.py sortie.html fichier1.md fichier2.md ...
"""
import html
import os
import re
import sys

from md2pdf import parse_blocks, segments


def inline(text):
    out = []
    for seg, bold, italic in segments(text):
        s = html.escape(seg)
        if bold:
            s = f"<strong>{s}</strong>"
        if italic:
            s = f"<em>{s}</em>"
        out.append(s)
    return "".join(out)


def conv(path):
    parts = []
    for kind, payload in parse_blocks(path):
        if kind in ("h1", "h2"):
            parts.append(f"<h2>{inline(payload)}</h2>")
        elif kind == "h3":
            parts.append(f"<h3>{inline(payload)}</h3>")
        elif kind == "rule":
            continue
        elif kind == "p":
            parts.append(f"<p>{inline(payload)}</p>")
        elif kind == "quote":
            parts.append(f"<blockquote>{inline(payload)}</blockquote>")
        elif kind == "list":
            items, numbered = payload
            tag = "ol" if numbered else "ul"
            lis = "".join(f"<li>{inline(i)}</li>" for i in items)
            parts.append(f"<{tag}>{lis}</{tag}>")
        elif kind == "table":
            rows = payload
            head = "".join(f"<th>{inline(c)}</th>" for c in rows[0])
            body = "".join(
                "<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>"
                for r in rows[1:]
            )
            parts.append(
                f"<div class='tw'><table><thead><tr>{head}</tr></thead>"
                f"<tbody>{body}</tbody></table></div>"
            )
    return "\n".join(parts)


CSS = """
:root{
  --ink:#141414; --grey:#6a6a6a; --bg:#fbfaf8; --rule:#ded8d0; --accent:#6b2b2b;
  --head:#2a2523; --tbl:#f2ede6;
}
@media (prefers-color-scheme: dark){
  :root{ --ink:#e8e4de; --grey:#9b948c; --bg:#171614; --rule:#332f2b; --accent:#c98a7d;
         --head:#f0ebe4; --tbl:#232120; }
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{
  margin:0; background:var(--bg); color:var(--ink);
  font-family:Georgia,'Iowan Old Style','Times New Roman',serif;
  font-size:18px; line-height:1.62;
  padding:28px 20px 80px;
}
main{max-width:34rem;margin:0 auto}
h1{
  font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
  font-size:1.05rem; letter-spacing:.14em; text-transform:uppercase;
  color:var(--grey); font-weight:600; margin:0 0 .2rem;
}
.subtitle{font-style:italic;color:var(--grey);margin:0 0 2.6rem;font-size:1rem}
h2{
  font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
  font-size:1.32rem; line-height:1.28; color:var(--accent);
  margin:3.2rem 0 1.1rem; padding-top:1.3rem;
  border-top:1px solid var(--rule); font-weight:700;
}
h3{
  font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
  font-size:.78rem; letter-spacing:.1em; text-transform:uppercase;
  color:var(--grey); margin:2rem 0 .6rem; font-weight:700;
}
p{margin:0 0 1.05rem; text-align:left}
strong{color:var(--head)}
ul,ol{margin:0 0 1.15rem; padding-left:1.3rem}
li{margin:0 0 .45rem}
blockquote{
  margin:1.2rem 0; padding:.1rem 0 .1rem 1rem;
  border-left:2px solid var(--rule); color:var(--grey); font-style:italic;
}
.tw{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:1.1rem 0 1.6rem}
table{border-collapse:collapse;width:100%;font-size:.86rem;line-height:1.42}
th{
  font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
  font-size:.68rem; letter-spacing:.07em; text-transform:uppercase;
  text-align:left; background:var(--tbl); color:var(--head);
  padding:.55rem .6rem; border-bottom:1px solid var(--rule);
}
td{padding:.55rem .6rem;border-bottom:1px solid var(--rule);vertical-align:top}
tr:last-child td{border-bottom:none}
code{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:.88em}
a{color:var(--accent)}
@media (max-width:420px){ body{font-size:17px;padding:20px 16px 64px} table{font-size:.8rem} }
"""


def main():
    out = sys.argv[1]
    srcs = sys.argv[2:]
    body = "\n".join(conv(p) for p in srcs)
    doc = f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light dark">
<title>CE QUE JE TE DOIS — dossier éditorial</title>
<style>{CSS}</style>
</head>
<body>
<main>
<h1>CE QUE JE TE DOIS</h1>
<p class="subtitle">Dossier éditorial — bible v6.0, charte v1.0.0, manuscrit</p>
{body}
</main>
</body>
</html>
"""
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(doc)
    print("écrit :", out, "|", len(doc) // 1024, "Ko")


if __name__ == "__main__":
    main()
