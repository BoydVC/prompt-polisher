#!/usr/bin/env python3
"""Fleet Prompt Polisher: read-only review of every bot's persona and routine prompts.
Reads /home/box/agent-data/agents/*/profile.json + automations/*/automation.json and
/workspace/tokenmax/fleet-doctor/data/report.json. Writes ONLY inside this folder."""
import json, os, re, glob, difflib, html, datetime
from analysis import ORDER, BOTS, FLEET_CONFLICTS, TOP10

HERE = os.path.dirname(os.path.abspath(__file__))
AGENTS = "/home/box/agent-data/agents"
FD = "/workspace/tokenmax/fleet-doctor/data/report.json"

def load_agents():
    out = {}
    for d in sorted(glob.glob(os.path.join(AGENTS, "*/"))):
        aid = os.path.basename(d.rstrip("/"))
        try:
            p = json.load(open(os.path.join(d, "profile.json")))
        except Exception:
            continue
        routines = []
        for f in sorted(glob.glob(os.path.join(d, "automations/*/automation.json"))):
            a = json.load(open(f))
            routines.append(dict(name=a.get("name"), prompt=a.get("prompt", ""), cron=a.get("schedule", ""),
                                 enabled=bool(a.get("enabled")), provenance=a.get("provenance"),
                                 folder=os.path.basename(os.path.dirname(f))))
        out[p.get("name")] = dict(id=aid, profile=p, routines=routines)
    return out

AGENT_DATA = load_agents()
ID2NAME = {v["id"]: k for k, v in AGENT_DATA.items()}

# ---------------------------------------------------------------- redaction
def redact(s):
    if not s:
        return s
    s = re.sub(r"https?://pub-[^\s)\]]*r2\.dev[^\s)\]]*", "[redacted manifest URL]", s)
    s = re.sub(r"[\w.+-]+@(group|import)\.calendar\.google\.com", "[redacted calendar id]", s)
    s = re.sub(r"\b\d{2}[a-z]{3,}@[\w-]+\.org\b", "[redacted school account]", s)
    s = re.sub(r"[\w.+-]+@[\w-]+(\.[\w-]+)+", "[redacted email]", s)
    s = re.sub(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b",
               lambda m: "[agent id: %s]" % ID2NAME.get(m.group(0), "bot"), s)
    s = re.sub(r"\$\s?\d[\d,]*(\.\d+)?", "[redacted amount]", s)
    s = re.sub(r"\b\d{1,2}/\d{1,2}/\d{4}\b", "[redacted DOB]", s)
    s = re.sub(r"(?=[A-Za-z0-9_-]*\d)(?=[A-Za-z0-9_-]*[A-Za-z])\b[A-Za-z0-9_-]{20,}\b", "[redacted id]", s)
    s = re.sub(r"(?i)(password|passwd|api[_ -]?key|token|secret)\s*[:=]\s*\S+", r"\1: [redacted]", s)
    return s

# ---------------------------------------------------------------- helpers
DOW = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
def human_cron(c):
    try:
        mi, hr, dom, mon, dow = c.split()
        hours = [int(h) for h in hr.split(",")]
        times = ", ".join(datetime.time(h, int(mi)).strftime("%-I:%M %p") for h in hours)
        if dow == "*": days = "every day"
        elif dow == "1-5": days = "weekdays"
        elif dow == "0-4": days = "Sun–Thu"
        elif dow.isdigit(): days = DOW[int(dow) % 7] + "s"
        else: days = "days " + dow
        return f"{days} at {times} ET"
    except Exception:
        return c

def fires_per_week(c):
    try:
        mi, hr, dom, mon, dow = c.split()
        per_day = len(hr.split(","))
        if dow == "*": d = 7
        elif "-" in dow:
            a, b = dow.split("-"); d = int(b) - int(a) + 1
        else: d = len(dow.split(","))
        return per_day * d
    except Exception:
        return None

TOK = re.compile(r"\s+|\w+|[^\w\s]", re.U)
def diff_ops(a, b):
    ta, tb = TOK.findall(a), TOK.findall(b)
    sm = difflib.SequenceMatcher(None, ta, tb, autojunk=False)
    ops = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        ops.append([tag, "".join(ta[i1:i2]), "".join(tb[j1:j2])])
    # readability: fold tiny equal runs (<= 6 chars, no newline) sitting between two changes into the change
    out = []
    for k, op in enumerate(ops):
        if (op[0] == "equal" and 0 < k < len(ops) - 1 and len(op[1]) <= 6 and "\n" not in op[1]
                and ops[k - 1][0] != "equal" and ops[k + 1][0] != "equal"):
            op = ["replace", op[1], op[2]]
        if out and op[0] != "equal" and out[-1][0] != "equal":
            out[-1] = ["replace", out[-1][1] + op[1], out[-1][2] + op[2]]
        else:
            out.append(list(op))
    return out, round(sm.ratio(), 3)

def tok_est(s):
    return round(len(s) / 4)

# ---------------------------------------------------------------- fleet doctor context
FDR = json.load(open(FD))
FD_ROUT = {(r["bot"], r["name"]): r for r in FDR["routines"]}
FD_CARDS = {c["name"]: c for c in FDR["cards"]}
FD_FIND = {}
for f in FDR["findings"]:
    for b in (f.get("bots") or ([f["bot"]] if f.get("bot") else [])):
        FD_FIND.setdefault(b, []).append(dict(severity=f["severity"], title=f["title"], fix=f.get("fix", "")))

def build():
    bots = []
    for name in ORDER:
        rec = AGENT_DATA.get(name)
        a = BOTS[name]
        before_persona = redact(rec["profile"].get("description", "")) if rec else ""
        after_persona = a["persona_after"]
        ops, ratio = diff_ops(before_persona, after_persona)
        routines = []
        for r in (rec["routines"] if rec else []):
            rb = redact(r["prompt"])
            rw = a["routines"].get(r["name"], {})
            ra = rw.get("after", "(no rewrite proposed)")
            rops, rratio = diff_ops(rb, ra)
            fd = FD_ROUT.get((name, r["name"]))
            routines.append(dict(name=r["name"], cron=r["cron"], when=human_cron(r["cron"]), enabled=r["enabled"],
                                 firesPerWeek=fires_per_week(r["cron"]), before=rb, after=ra, ops=rops, similarity=rratio,
                                 note=rw.get("note", ""), tokensBefore=tok_est(rb), tokensAfter=tok_est(ra),
                                 measured=dict(minutesPerWeek=fd["minutesPerWeek"], toolCallsPerWeek=fd["toolCallsPerWeek"],
                                               medianMinutes=fd["medianMinutes"], runs=fd["runs"]) if fd else None))
        card = FD_CARDS.get(name, {})
        bots.append(dict(name=name, title=(rec["profile"].get("title") if rec else "") or "",
                         summary=a["summary"], overlaps=[dict(with_=o["with_"], kind=o["kind"], text=o["text"], quote=o.get("quote", "")) for o in a["overlaps"]],
                         risks=a["risks"], schedule=a["schedule"], rulesKept=a.get("rules_kept", []),
                         persona=dict(before=before_persona, after=after_persona, ops=ops, similarity=ratio,
                                      tokensBefore=tok_est(before_persona), tokensAfter=tok_est(after_persona)),
                         routines=routines, fleetDoctor=dict(grade=card.get("grade"), findings=FD_FIND.get(name, [])),
                         routinesOnDisk=len(routines)))
    # ---- savings (estimates)
    byname = {b["name"]: b for b in bots}
    top = []
    for i, t in enumerate(TOP10, 1):
        s = t.get("saving"); est = None; method = None
        if s and s["kind"] == "routine":
            m = FD_ROUT[(s["bot"], s["routine"])]
            est = f"≈{m['minutesPerWeek']:.0f} agent-min and ≈{m['toolCallsPerWeek']} tool calls a week"
            method = f"Fleet Doctor measured {m['runs']} runs: median {m['medianMinutes']} min × {m['firesPerWeek']} fires a week. Assumes the routine is fully retired."
        elif s and s["kind"] == "prompt_trim":
            r = next(x for x in byname[s["bot"]]["routines"] if x["name"] == s["routine"])
            d = r["tokensBefore"] - r["tokensAfter"]
            est = f"≈{d} prompt tokens a run, ≈{d * r['firesPerWeek']:,} a week"
            method = f"Prompt length before/after ÷ 4 characters per token ({r['tokensBefore']} → {r['tokensAfter']} tokens) × {r['firesPerWeek']} fires a week. Counts only the prompt text, not tool output."
        elif s and s["kind"] == "oscar":
            k = FD_ROUT[("Oscar", "Watch for Kia Finance statement")]; d = FD_ROUT[("Oscar", "Due-soon bills and money surprises")]
            trim = round(d["minutesPerWeek"] * 0.25, 1)
            est = f"≈{k['minutesPerWeek'] + trim:.0f} agent-min and ≈{k['toolCallsPerWeek'] + round(d['toolCallsPerWeek'] * 0.25)} tool calls a week"
            method = (f"Kia watch measured at {k['minutesPerWeek']} min and {k['toolCallsPerWeek']} tool calls a week (Fleet Doctor), assumed fully absorbed. "
                      f"Plus an ASSUMED 25% trim from the stop rule on the bills run ({d['minutesPerWeek']} min and {d['toolCallsPerWeek']} calls a week measured). The 25% is a guess, not a measurement.")
        elif s and s["kind"] == "weekend":
            v = FD_ROUT[("Vic Tutor", "Vic weeknight homework check-in")]; c = FD_ROUT[("Char Tutor", "Char weeknight homework check-in")]
            mins = 2 * v["medianMinutes"] + 2 * c["medianMinutes"]; calls = 2 * v["toolCallsPerRun"] + 2 * c["toolCallsPerRun"]
            est = f"≈{mins:.1f} agent-min, ≈{calls:.0f} tool calls and 4 wakes a week"
            method = "Two weekend fires per tutor × Fleet Doctor's median run length and tool calls per run. Applies only if Boyd and Miranda choose Sun–Thu."
        elif s and s["kind"] == "persona_trim":
            p = byname[s["bot"]]["persona"]; d = p["tokensBefore"] - p["tokensAfter"]
            if d >= 0:
                est = f"≈{d} tokens per Michael turn"
            else:
                est = f"+{-d} tokens per turn for the roster (a net cost); the saving is in avoided duplicate routines"
            method = f"Persona length before/after ÷ 4 ({p['tokensBefore']} → {p['tokensAfter']} tokens). If either paused copy were re-enabled, it would cost ≈{FD_ROUT[('Michael','Morning attention brief')]['minutesPerWeek'] + FD_ROUT[('Michael','Jim daily interest note')]['minutesPerWeek']:.0f} agent-min a week (Fleet Doctor's figure from when they ran)."
        top.append(dict(rank=i, id=t["id"], title=t["title"], bots=t["bots"], why=t["why"], estimate=est, method=method, extra=t.get("extra", "")))
    total_min = 0
    for t in TOP10:
        s = t.get("saving")
        if s and s["kind"] == "routine": total_min += FD_ROUT[(s["bot"], s["routine"])]["minutesPerWeek"]
        if s and s["kind"] == "oscar":
            total_min += FD_ROUT[("Oscar", "Watch for Kia Finance statement")]["minutesPerWeek"] + 0.25 * FD_ROUT[("Oscar", "Due-soon bills and money surprises")]["minutesPerWeek"]
        if s and s["kind"] == "weekend":
            total_min += 2 * FD_ROUT[("Vic Tutor", "Vic weeknight homework check-in")]["medianMinutes"] + 2 * FD_ROUT[("Char Tutor", "Char weeknight homework check-in")]["medianMinutes"]
    fleet_min = sum(r["minutesPerWeek"] for r in FDR["routines"] if r["enabled"])
    data = dict(generatedAt=datetime.datetime.now().strftime("%a %b %-d %Y, %-I:%M %p ET"),
                botCount=len(bots), routineCount=sum(len(b["routines"]) for b in bots),
                bots=bots, conflicts=FLEET_CONFLICTS, top10=top,
                totals=dict(agentMinPerWeekSaved=round(total_min, 1), fleetAgentMinPerWeek=round(fleet_min, 1),
                            method="The sum of the measured or estimated agent-minutes in the top 10, compared with the fleet's enabled routines in Fleet Doctor (runs logged up to Sep 15). Agent-minutes stand in for tokens because per-bot token counts aren't stored on disk."),
                notes=["Read-only. Nothing was changed on any bot. Boyd decides what to apply, and Boyd and Miranda decide anything about the kids' schedules.",
                       "“Before” text is quoted from each bot's profile.json and automation.json, with emails, calendar ids, folder ids, the manifest URL, dollar amounts and birthdates replaced by [redacted].",
                       "Pods, Path, Boyd Family Times and TokenMax describe daily routines that aren't on disk (newer bots whose routines live server-side). Only their wake lines were reviewed.",
                       "Fleet Doctor's run logs end Tue Sep 15, 9:35 PM ET (box restored from an Oct 3 snapshot)."])
    return data

def main():
    data = build()
    os.makedirs(os.path.join(HERE, "data"), exist_ok=True)
    json.dump(data, open(os.path.join(HERE, "data/polish.json"), "w"), indent=1, ensure_ascii=False)
    tpl = open(os.path.join(HERE, "web/template.html"), encoding="utf-8").read()
    blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    page = tpl.replace("/*__DATA__*/null", blob)
    open(os.path.join(HERE, "web/index.html"), "w", encoding="utf-8").write(page)
    os.makedirs(os.path.join(HERE, "dist"), exist_ok=True)
    open(os.path.join(HERE, "dist/prompt-polisher.html"), "w", encoding="utf-8").write(page)
    import summary_pdf
    summary_pdf.write(data, os.path.join(HERE, "dist/summary.html"))
    print("built", data["botCount"], "bots,", data["routineCount"], "routines; est saved", data["totals"]["agentMinPerWeekSaved"], "agent-min/wk of", data["totals"]["fleetAgentMinPerWeek"])

if __name__ == "__main__":
    main()
