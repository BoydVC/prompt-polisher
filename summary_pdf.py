# -*- coding: utf-8 -*-
"""Printable summary (HTML → PDF via headless Chrome in make_outputs.sh)."""
import html
E = html.escape

def write(data, path):
    h = ["""<!doctype html><html><head><meta charset="utf-8"><title>Fleet Prompt Polisher — summary</title><style>
@page{size:Letter;margin:14mm}body{font:10.5pt/1.45 -apple-system,Segoe UI,Roboto,sans-serif;color:#1b1d2a}
h1{font-size:22pt;margin:0 0 2pt}h2{font-size:14pt;margin:16pt 0 6pt;border-bottom:2px solid #ff4fb8;padding-bottom:2pt}
h3{font-size:11.5pt;margin:10pt 0 3pt}.sub{color:#666}.est{color:#0a7a3c;font-weight:600}.meth{color:#666;font-size:8.5pt}
table{border-collapse:collapse;width:100%}td,th{border-bottom:1px solid #ddd;padding:4pt;vertical-align:top;text-align:left}
.rank{font-size:15pt;font-weight:800;color:#c2187a;width:22pt}.q{font-style:italic;color:#5a2b6e;border-left:2px solid #ff4fb8;padding-left:6pt;margin:2pt 0}
.bot{break-inside:avoid;border:1px solid #e3e3ee;border-radius:6pt;padding:6pt 9pt;margin:6pt 0}.k{font-size:8pt;text-transform:uppercase;color:#b06a00}
.box{background:#f6f3ff;border-radius:6pt;padding:6pt 9pt}
</style></head><body>"""]
    h.append(f"<h1>✨ Fleet Prompt Polisher</h1><div class='sub'>Read-only review of Boyd's {data['botCount']} Grok Bots and {data['routineCount']} routine prompts on disk · built {E(data['generatedAt'])} · nothing applied, Boyd decides</div>")
    t = data["totals"]
    h.append(f"<p class='box'>The top 10 fixes would save an <b>estimated ≈{t['agentMinPerWeekSaved']} agent-min a week</b>, against ≈{t['fleetAgentMinPerWeek']} a week of enabled routines, and remove {len(data['conflicts'])} cross-bot conflicts.<br><span class='meth'>Method: {E(t['method'])}</span></p>")
    h.append("<h2>Top 10 fixes, ranked by impact</h2><table>")
    for x in data["top10"]:
        est = f"<div class='est'>Estimate: {E(x['estimate'])}</div><div class='meth'>{E(x['method'])}</div>" if x["estimate"] else ""
        ex = f"<div class='meth'>{E(x['extra'])}</div>" if x["extra"] else ""
        h.append(f"<tr><td class='rank'>{x['rank']}</td><td><b>{E(x['title'])}</b><div class='meth'>{E(' · '.join(x['bots']))}</div>{E(x['why'])}{est}{ex}</td></tr>")
    h.append("</table><h2>Conflicts between bots</h2>")
    for c in data["conflicts"]:
        h.append(f"<div class='bot'><div class='k'>{E(' ↔ '.join(c['bots']))}</div><b>{E(c['title'])}</b><br>{E(c['detail'])}</div>")
    h.append("<h2>Bot by bot</h2>")
    for b in data["bots"]:
        h.append(f"<div class='bot'><h3>{E(b['name'])} <span class='sub'>{E(b['title'])}</span></h3><div>{E(b['summary'])}</div>")
        for r in b["risks"][:2]:
            h.append(f"<div class='q'>“{E(r['quote'])}”</div><div>{E(r['issue'])}</div>")
        for s in b["schedule"][:2]:
            h.append(f"<div><b>{E(s['routine'])}</b>: {E(s['issue'])}</div>")
        pr = b["persona"]
        h.append(f"<div class='meth'>Persona rewrite ≈{pr['tokensBefore']} → {pr['tokensAfter']} tokens · {len(b['routines'])} routine rewrite(s). Full before/after diffs are in prompt-polisher.html.</div></div>")
    h.append("<h2>Honesty notes</h2><ul>" + "".join(f"<li>{E(n)}</li>" for n in data["notes"]) + "</ul></body></html>")
    open(path, "w", encoding="utf-8").write("".join(h))
