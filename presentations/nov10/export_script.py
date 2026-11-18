"""Writes SCRIPT.md from the speaker notes of the Nov 10 slides.
Usage: export_script.py <deck root> (the folder holding project/deck.json)."""
import html, json, os, re, sys

ROOT = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
deck = json.load(open(os.path.join(ROOT, "project/deck.json")))
order = deck["order"][deck["order"].index("nov10-cover"):]
text = lambda s: re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s.replace("<br>", " ")))).strip()

who = {}
for sid in order:
    t = open(os.path.join(ROOT, "project/slides", sid + ".html"), encoding="utf-8").read()
    who.setdefault(re.search(r"Presenter: ([^<]+)<", t).group(1), []).append(order.index(sid) + 39)
def span(v):
    runs = []
    for x in v:
        if runs and x == runs[-1][-1] + 1:
            runs[-1].append(x)
        else:
            runs.append([x])
    return " and ".join(f"{r[0]}–{r[-1]}" if len(r) > 1 else f"{r[0]}" for r in runs)
out = ["# Nov 17 script (the Nov 10 slides, presented Nov 17)", "",
       "Generated from the deck's speaker notes. These are talking points: learn each point and say it in your own words. \"If asked\" entries are backup answers, used only "
       "if the topic comes up. Presenters: " + ", ".join(f"{n} {span(v)}" for n, v in who.items()) + ".", ""]
for i, sid in enumerate(order):
    t = open(os.path.join(ROOT, "project/slides", sid + ".html"), encoding="utf-8").read()
    title = text(re.search(r"<h[12][^>]*>(.*?)</h[12]>", t, re.S).group(1).replace("<br>", " "))
    out += [f"### Slide {i + 39}: {title}", "", "Presenter: " + re.search(r"Presenter: ([^<]+)<", t).group(1), ""]
    for block in re.search(r"<aside>(.*?)</aside>", t, re.S).group(1).split("<br><br>"):
        label, body = block.split("<br>", 1)
        out += [f"**{html.unescape(label)}**", "", text(body), ""]
open(os.path.join(HERE, "SCRIPT.md"), "w", encoding="utf-8").write("\n".join(out))
print("wrote SCRIPT.md,", len(order), "slides")
