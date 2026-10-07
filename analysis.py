# -*- coding: utf-8 -*-
"""Fleet Prompt Polisher review content: per-bot parts + fleet-level conflicts and the ranked top 10.
Nothing here is applied anywhere. Boyd decides."""
from analysis_part1 import ORDER, BOTS
import analysis_part2, analysis_part3, analysis_part4, analysis_part5, analysis_part6  # noqa: F401 (register bots)

FLEET_CONFLICTS = [
  dict(bots=["Jim", "Pods"], title="Two owners for the daily podcast brief", detail="Jim's “Daily podcast listen brief” (cron 0 7 * * *, enabled) and Pods' persona (“Your ONLY job…”, daily ~7:00) cover the same four channels. If both are live, Boyd gets two podcast briefs every morning."),
  dict(bots=["Kelly", "Ryan"], title="Kelly pitches product ideas; Ryan's persona says Kelly shouldn't", detail="Kelly: “3 high-probability product ideas Boyd could build”. Ryan: never be a “real-time trend dump without a business angle (Kelly)”. Kelly also has no non-compete line."),
  dict(bots=["Vic Tutor", "Char Tutor"], title="PowerSchool ownership: persona vs routine", detail="Vic Tutor's persona says “always follow” the own-browser PowerSchool pull, but its routine, Char Tutor's routine and the PowerSchool skill all say Char owns the single session and Vic stays out by default."),
  dict(bots=["Jim", "Michael"], title="Where Jim's nightly note goes", detail="Jim's persona says to send the daily picture through Michael, but Jim's routine says to tell Boyd in this chat."),
  dict(bots=["Oscar", "Michael"], title="Every money ping is delivered twice", detail="All three Oscar routines tell Boyd and then “send the same through Michael”."),
  dict(bots=["Michael", "Brief", "Jim"], title="Paused duplicate routines on Michael", detail="Michael still holds paused copies of Brief's morning brief and Jim's interest note. Michael's persona says not to recreate them."),
  dict(bots=["Brief", "Pam", "Oscar"], title="Morning inbox and calendar read three times", detail="Pam reads the calendar at 7:30, Brief reads Gmail and Calendar at 8:00, and Oscar reads Gmail at 8:45. Nothing tells Brief to skip what Pam or Oscar own."),
  dict(bots=["TokenMax", "Dwight"], title="Same Cursor pool, no coordination", detail="Both launch Cursor Cloud Agents on the monthly pool, and TokenMax's persona also permits new repos without asking."),
]

# Ranked by impact. Savings are computed in build.py from Fleet Doctor's measured agent-minutes and tool calls,
# and from prompt length (characters ÷ 4 ≈ tokens).
TOP10 = [
  dict(id="podcast-owner", title="Make Pods the single owner of the podcast brief; retire Jim's copy", bots=["Jim", "Pods"], why="Removes a duplicate daily message and Jim's second-heaviest routine.", saving=dict(kind="routine", bot="Jim", routine="Daily podcast listen brief"), extra="Up to 7 duplicate briefs a week avoided if both are live."),
  dict(id="pam-stale", title="Strip Pam's stale “Known open items” (all dated Sep 12–21) and the repeated household block", bots=["Pam"], why="Stops past conflicts being re-raised and shortens every weekday run.", saving=dict(kind="prompt_trim", bot="Pam", routine="Weekday family calendar scan")),
  dict(id="noncompete", title="Put the non-compete in every bot that pitches ideas (Ryan's persona, Kelly) and leave idea-pitching to Ryan alone", bots=["Ryan", "Kelly"], why="Today the guard lives only in Ryan's Monday routine. On-demand pitches and Kelly's “3 product ideas” have no guard.", saving=None, extra="Risk fix. Also removes duplicate idea lists."),
  dict(id="oscar-merge", title="Fold Oscar's Kia watch into the 8:45 bills run, add a stop rule, and stop double-sending through Michael", bots=["Oscar", "Michael"], why="Three back-to-back money runs re-gather the same Gmail and Drive data, and every ping arrives twice.", saving=dict(kind="oscar"), extra="Halves Oscar→Michael relays."),
  dict(id="tutor-powerschool", title="Fix Vic Tutor's PowerSchool persona-vs-routine contradiction and the literal “\\n” in its prompt", bots=["Vic Tutor", "Char Tutor"], why="An on-demand Vic pull can kick Char's session and stack password prompts for Boyd, which is exactly what the routine was written to stop.", saving=None, extra="Fewer credential prompts for Boyd."),
  dict(id="brief-dedupe", title="Tell Brief to skip what Pam (family calendar) and Oscar (bills) own, and pin “next few days” to 2 business days", bots=["Brief", "Pam", "Oscar"], why="Three bots read overlapping sources every morning. De-duping cuts repeat notices.", saving=None, extra="Fewer repeat morning items (can't be measured from disk)."),
  dict(id="jim-workpc", title="Limit Jim's nightly Chrome pull to the home PC (work PC only with Boyd's OK) and settle where the note goes", bots=["Jim", "Michael"], why="Keeps law-firm and client browsing out of a personal journal, and resolves the Boyd-vs-Michael delivery conflict.", saving=None, extra="Privacy and risk fix."),
  dict(id="tutor-weekends", title="The “weeknight” tutor check-ins fire 7 days a week; Boyd and Miranda decide whether to go Sun–Thu", bots=["Vic Tutor", "Char Tutor"], why="The routine names and schedules disagree. Suggestion only: kids' schedules are Boyd and Miranda's call.", saving=dict(kind="weekend")),
  dict(id="bft-manifest", title="Pin Boyd Family Times' remote production instructions and add a “printer offline” notice", bots=["Boyd Family Times"], why="A remote file on a public bucket can currently override the paper's behaviour, and 4 of the last 7 editions fell back to PDF without telling Boyd.", saving=None, extra="Risk fix."),
  dict(id="michael-cleanup", title="Delete Michael's two paused duplicate routines, add a roster, and move the Jim-specific Chrome rule out of Michael's persona", bots=["Michael"], why="Prevents an accidental re-enable of duplicate briefs, and trims the front-door persona Michael re-reads on every turn (its chat has 664 entries).", saving=dict(kind="persona_trim", bot="Michael")),
]
