#!/usr/bin/env python3
"""Smoke test: every bot covered, quotes are real, diffs render, standing rules kept, no secret-looking strings, no JS errors."""
import json, os, re, subprocess, sys, glob, urllib.request
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
FAIL = []; N = [0]
def ok(cond, msg):
    N[0] += 1
    if not cond: FAIL.append(msg)

d = json.load(open(os.path.join(HERE, "data/polish.json")))
EXPECTED = ["Michael","Pam","Oscar","Jim","Kelly","Ryan","Dwight","Brief","Pods","Path","Vic Tutor","Char Tutor","Boyd Family Times","Dr. EggBot","TokenMax"]
names = [b["name"] for b in d["bots"]]
for e in EXPECTED: ok(e in names, f"bot missing: {e}")

# every on-disk routine of each expected bot is covered with a real rewrite
disk = {}
for f in glob.glob("/home/box/agent-data/agents/*/profile.json"):
    p = json.load(open(f)); disk[p["name"]] = [json.load(open(a))["name"] for a in glob.glob(os.path.join(os.path.dirname(f), "automations/*/automation.json"))]
for b in d["bots"]:
    ok(b["summary"].strip(), f"{b['name']}: no summary")
    ok(b["persona"]["before"].strip() and b["persona"]["after"].strip(), f"{b['name']}: persona before/after empty")
    ok(any(t != "equal" for t, _, _ in b["persona"]["ops"]), f"{b['name']}: persona diff has no changes")
    have = {r["name"] for r in b["routines"]}
    for rn in disk.get(b["name"], []): ok(rn in have, f"{b['name']}: routine not covered: {rn}")
    for r in b["routines"]:
        ok(r["after"] and r["after"] != "(no rewrite proposed)", f"{b['name']}/{r['name']}: no rewrite")
        ok(any(t != "equal" for t, _, _ in r["ops"]), f"{b['name']}/{r['name']}: empty diff")
        # diff reconstructs both sides exactly
        ok("".join(x for t, x, _ in r["ops"]) == r["before"] and "".join(y for t, _, y in r["ops"]) == r["after"], f"{b['name']}/{r['name']}: diff does not reconstruct")
    ok("".join(x for t, x, _ in b["persona"]["ops"]) == b["persona"]["before"], f"{b['name']}: persona diff does not reconstruct")
    # quotes are real text
    corpus = b["persona"]["before"] + "\n" + "\n".join(r["before"] for r in b["routines"])
    for o in b["overlaps"]:
        if o.get("quote"): ok(o["quote"] in corpus, f"{b['name']}: overlap quote not found in real text: {o['quote'][:60]}")
    for r in b["risks"]: ok(r["quote"] in corpus, f"{b['name']}: risk quote not found in real text: {r['quote'][:60]}")
    # standing rules kept word for word in the rewrite (persona or a routine)
    after_all = b["persona"]["after"] + "\n" + "\n".join(r["after"] for r in b["routines"])
    for rule in b.get("rulesKept", []):
        ok(rule in corpus, f"{b['name']}: kept rule isn't in the original: {rule[:50]}")
    low_before, low_after = corpus.lower(), after_all.lower()
    if "non-compete" in low_before: ok("non-compete" in low_after, f"{b['name']}: rewrite dropped the non-compete")
    if "auto-assign" in low_before: ok("never auto-assign" in low_after, f"{b['name']}: rewrite weakened the coverage rule")
    for kw in ["never invent", "romantic/sexual"]:
        if kw in low_before: ok(kw in low_after, f"{b['name']}: rewrite dropped '{kw}'")
    ok("stay quiet" in low_after or "stay silent" in low_after, f"{b['name']}: rewrite has no stay-quiet rule")
    ok("success" in low_after, f"{b['name']}: rewrite has no success criteria")
ok(len(d["top10"]) == 10, "top10 is not 10 items")
for t in d["top10"]:
    if t["estimate"]: ok(t["method"], f"top10 #{t['rank']}: estimate without method")
# Non-compete rule must exist in Ryan + Kelly + Pods rewrites
for n in ["Ryan", "Kelly", "Pods", "TokenMax"]:
    b = next(x for x in d["bots"] if x["name"] == n); ok("non-compete" in b["persona"]["after"].lower(), f"{n}: persona rewrite lacks non-compete")

# secret-looking strings in every shipped file
SECRET = [(r"[\w.+-]+@[\w-]+\.[\w.-]+", "email/calendar id"), (r"https?://pub-[^\s\"']*r2\.dev", "manifest URL"),
          (r"\$\s?\d", "dollar amount"), (r"\b\d{1,2}/\d{1,2}/(19|20)\d{2}\b", "date of birth"),
          (r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", "raw agent uuid"),
          (r"(?i)\b(sk|pk|ghp|xox[abp])[-_][A-Za-z0-9]{16,}", "API token"), (r"1jsaoMB", "Drive folder id"),
          (r"(?i)password\s*[:=]\s*\S", "password value")]
files = ["data/polish.json", "web/index.html", "dist/prompt-polisher.html", "dist/summary.html"]
for f in files:
    txt = open(os.path.join(HERE, f), encoding="utf-8").read()
    for pat, label in SECRET:
        m = re.search(pat, txt)
        ok(not m, f"{f}: secret-looking {label}: {m.group(0) if m else ''}")
pdf = os.path.join(HERE, "dist/prompt-polisher-summary.pdf")
if os.path.exists(pdf):
    t = subprocess.run(["pdftotext", pdf, "-"], capture_output=True, text=True).stdout
    ok("Top 10" in t, "PDF lacks top 10")
    for pat, label in SECRET: ok(not re.search(pat, t), f"PDF: secret-looking {label}")
else: ok(False, "PDF missing")

# JS render check in headless Chrome (offline file + live server), several views
def dom(url):
    r = subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--disable-gpu", "--user-data-dir=/tmp/pp-smoke-chrome",
                        "--virtual-time-budget=3000", "--dump-dom", url], capture_output=True, text=True, timeout=60)
    return r.stdout
views = ["#fleet"] + ["#bot=" + n.replace(" ", "%20") for n in EXPECTED] + ["#bot=Oscar&mode=inline"]
targets = ["file://" + os.path.join(HERE, "dist/prompt-polisher.html")]
try:
    urllib.request.urlopen("http://127.0.0.1:4270/health", timeout=3); targets.append("http://127.0.0.1:4270/")
except Exception:
    ok(False, "server on :4270 not responding")
for base in targets:
    for v in (views if base.startswith("file") else ["#fleet", "#bot=Jim"]):
        h = dom(base + v)
        ok('data-ready="1"' in h, f"not rendered: {base}{v}")
        body = re.search(r"<body[^>]*>", h); btag = body.group(0) if body else ""
        ok("data-jserr" not in btag, f"JS error at {base}{v}: {btag}")
        ok('data-ready="1"' in btag, f"body not marked ready: {base}{v}")
        if "bot=" in v:
            m = re.search(r'data-diffs="(\d+)"', h); ok(m and int(m.group(1)) >= 1, f"no diffs rendered at {v}")
            ok("<ins>" in h or "<del>" in h, f"diff highlights missing at {v}")
print(f"{N[0] - len(FAIL)}/{N[0]} checks passed")
for f in FAIL: print("FAIL:", f)
sys.exit(1 if FAIL else 0)
