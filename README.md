# ✨ Fleet Prompt Polisher

TokenMax build night, Oct 7 2026. This is a **read-only** review of all 15 Grok Bots in Boyd's fleet: Michael, Pam, Oscar, Jim, Kelly, Ryan, Dwight, Brief, Pods, Path, Vic Tutor, Char Tutor, Boyd Family Times, Dr. EggBot and TokenMax.

For each bot it shows:
- a plain-English summary of the bot's job
- overlaps and conflicts with other bots, quoting the real text
- vague or risky instructions
- routines whose prompt doesn't match their schedule or purpose
- a suggested rewrite of the persona and every routine prompt on disk, shown as a before/after diff (side by side or inline), with explicit success criteria and stay-quiet rules

At fleet level there's a ranked top 10, and each fix carries an **estimated** saving with its method shown.

**Nothing is applied.** No bot, routine or file outside this folder was touched. Boyd decides what to apply, and Boyd and Miranda decide anything about the kids' schedules.

## Run
```bash
./run.sh                    # rebuild from the bots' current prompts + start http://127.0.0.1:4270 (nohup, pid in data/server.pid)
./make_outputs.sh           # PDF + screenshots (needs the server up)
python3 tests/smoke_test.py # all bots covered, quotes real, diffs render, rules kept, no secrets, no JS errors
```
Viewer routes: `#fleet`, `#bot=Jim`, `#bot=Oscar&focus=routine-0&mode=inline`. Endpoints: `/api/data`, `/health`, `/summary.pdf`.

## Outputs
- `dist/prompt-polisher.html`: offline single file with every bot and every diff. It works without internet.
- `dist/prompt-polisher-summary.pdf`: a 9-page summary with the top 10, the conflicts, and each bot's summary and top issues.
- `screenshots/00-best-jim-podcast-duplicate-diff.png`, `01-fleet-top10.png`, `02-pam-stale-items-diff.png`, `03-vic-tutor-conflict.png`, `04-oscar-inline-diff.png`, `05-phone-fleet.png`
- `data/polish.json`: the machine-readable review (redacted).

## Sources (read-only)
- `/home/box/agent-data/agents/*/profile.json` (persona) and `automations/*/automation.json` (routine prompt, cron, enabled)
- `/workspace/tokenmax/fleet-doctor/data/report.json` (measured agent-minutes, tool calls, findings)
- `/home/box/agent-data/workflows/powerschool-own-browser-grades/SKILL.md`, read to confirm the PowerSchool ownership conflict

## Privacy
"Before" text is quoted verbatim except that emails and school accounts, calendar ids, the Drive folder id, the newspaper's manifest URL, dollar amounts, birthdates and raw agent ids are replaced with `[redacted …]`. The smoke test scans every shipped file and the PDF for those patterns. No grades, balances or credentials appear in any prompt.

## Standing rules
The rewrites keep, word for word or stronger:
- Pam's "NEVER auto-assign … coverage" rule (it now also covers grandparents)
- the collections non-compete, which is kept in Ryan, Pods and TokenMax and added to Ryan's persona and Kelly
- never invent, never send, never buy
- the kids-safety lines in the tutor and Path rewrites

The smoke test fails if a rewrite drops any of these.

## Honesty notes
- Pods, Path, Boyd Family Times and TokenMax describe daily routines that aren't on disk (newer bots; their routines live server-side). Only their wake lines were reviewed.
- Savings are estimates. Agent-minutes come from Fleet Doctor's logs, which end Sep 15. Prompt-token savings are characters ÷ 4. The Oscar 25% stop-rule trim is labelled as an assumption.
- Fleet Doctor flagged Jim's Bill Simmons watch as "finished". Its prompt is weekly by design, so that flag is likely a false positive; this review flags ownership and the missing season end date instead.


---
## Repo notes
- **Built:** Oct 7 2026, by TokenMax (Boyd's Grok Bot) on the Grok Bot box.
- **Run:** `./run.sh` (then open the localhost URL it prints).
- Imported from `/workspace/tokenmax/prompt-polisher` on Oct 23, 2026. node_modules, virtualenvs, logs and files over 20 MB were left out.
