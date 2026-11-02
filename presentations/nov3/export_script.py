"""Writes the Nov 3 speaker notes from the deck folder to SCRIPT.md, so the script can be read
without opening the deck. Usage: export_script.py <deck root>."""
import json, os, re, sys

P = os.path.join(sys.argv[1], "project")
order = json.load(open(os.path.join(P, "deck.json")))["order"]
out, who = ["# Nov 3 script", "",
            "Generated from the deck's speaker notes. Read the quoted lines aloud. \"If asked\" entries are backup answers, read only if the topic comes up."], None
for i, sid in enumerate(order, 1):
    if not sid.startswith("nov3"):
        continue
    html = open(os.path.join(P, "slides", sid + ".html")).read()
    name = re.search(r"Presenter: (\w+)", html).group(1)
    if name != who:
        who = name
        out += ["", f"## {name}"]
    title = re.sub(r"<br>", " ", re.search(r"<h[12][^>]*>(.*?)</h[12]>", html, re.S).group(1))
    out += ["", f"### Slide {i}: {re.sub(r'<[^>]+>', '', title)}"]
    for block in re.search(r"<aside>(.*?)</aside>", html, re.S).group(1).split("<br><br>"):
        if block.startswith("["):
            where, line = block.split("<br>", 1)
            out += ["", f"**{where}**", "", line]
        else:                                                    # a note added by hand on the deck page
            out += ["", block.replace("<br>", "\n\n")]
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "SCRIPT.md"), "w").write("\n".join(out) + "\n")
