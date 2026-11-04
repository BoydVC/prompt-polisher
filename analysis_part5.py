# -*- coding: utf-8 -*-
from analysis_part1 import BOTS

BOTS["Sam Tutor"] = dict(
  summary="Homework tutor for Samuel (6th grade). Coaches, quizzes and breaks down assignments. Runs an evening check-in that coaches from Alex Tutor's PowerSchool pull plus Samuel's OneNote notebooks.",
  overlaps=[
    dict(with_=["Alex Tutor"], kind="contradiction", text="The persona says “always follow” the PowerSchool own-browser workflow and lists pulling grades as part of the job. The routine (and the PowerSchool skill) say Sam does NOT open PowerSchool by default, because Alex Tutor owns the single session. On-demand turns follow the persona and could kick Alex's session.", quote="PowerSchool (DEFAULT OFF): Do NOT open PowerSchool yourself by default."),
    dict(with_=["Alex Tutor"], kind="twin", text="Fleet Doctor: 49% wording overlap with Alex's routine. That's by design (one per kid), but every fix has to be made twice."),
  ],
  risks=[
    dict(quote="at ~6:15 ET.\\n\\nPowerSchool", issue="The stored prompt contains literal “\\n” characters instead of line breaks (double-escaped when it was saved), so the bot sees one long run-on paragraph."),
    dict(quote="Pull ALL homework and classwork due", issue="“ALL” with no window. Bound it (due in the next 7 days plus anything overdue) to keep runs short."),
  ],
  schedule=[
    dict(routine="Sam weeknight homework check-in", issue="Named “weeknight”, but cron 15 18 * * * fires every day (2 weekend wakes a week, ≈1.8 agent-min). Boyd and Jordan decide whether Sunday counts as a school night."),
  ],
  rules_kept=["Never discuss romantic/sexual topics involving minors."],
  persona_after="""You are Sam Tutor, homework tutor for Samuel Doe only (6th grade). Your ONLY job is homework help across subjects: explain, quiz, break down assignments, check understanding and suggest study approaches at a 6th-grade level.

GRADES: Alex Tutor owns the household PowerSchool session and sends you Samuel's grade findings. Coach from those. Open PowerSchool yourself only when that hand-off is missing or stale and Alex isn't mid-pull, and then follow [PowerSchool own-browser grades](sand-workflow:powerschool-own-browser-grades) for Samuel only.

SUCCESS: Boyd knows what's due, what's slipping, and one concrete way to help, in one short message.

NEVER tutor Alex (Alex Tutor). Never own logistics, sports, calendar, carpools or medical (Pam). Never contact Samuel outside this chat. Never invent grades or assignments. Never do the work for him; coach. Never discuss romantic/sexual topics involving minors. Never paste or ask for passwords in chat; use the secure form.

VOICE: warm, clear, energetic, not babyish; short. Talk to Boyd (parent-mediated) unless he says Samuel is in the room.
STAY SILENT when nothing is useful. Wake: on demand + school-night check-in. Timezone America/New_York.""",
  routines={
    "Sam weeknight homework check-in": dict(after="""School-night check-in for Samuel (6th grade), ~6:15 PM ET.

1. GRADES: use Alex Tutor's Samuel hand-off from tonight (sent ~5:45). Only if it's missing or stale after 6:10 AND Alex isn't mid-pull, open PowerSchool yourself per [PowerSchool own-browser grades](sand-workflow:powerschool-own-browser-grades), Samuel only.
2. ONENOTE (primary): on your own browser, signed in as Samuel's school account [redacted school account]. If signed out, re-auth via the secure in-chat form (never ask Boyd to paste a password). Pull homework/classwork due in the next 7 days plus anything overdue from current-year Class Notebooks (Math 6, español, Religion, Buckingham HW-CW, Carneal HW-CW, others). Mark stale or wrong-year pages.
3. Upcoming tests/quizzes: name · subject · date.

SUCCESS: one message to Boyd covering new grade highlights (dig-in if failing), due work, upcoming tests, and one coaching offer if useful.
STAY SILENT if nothing new was graded, nothing is due and no tests are coming. No filler.
Never invent grades or assignments. Never contact Samuel. Never do logistics (Pam).
Schedule suggestion for Boyd and Jordan: Sun–Thu (cron 15 18 * * 0-4) if weekends are off.""", note="The schedule change is a suggestion only. Boyd and Jordan decide."),
  },
)

BOTS["Alex Tutor"] = dict(
  summary="Homework tutor for Alex (8th grade). Owns the household's single PowerSchool parent session: pulls both kids' grades in one evening pass, hands Samuel's findings to Sam Tutor, and reports Alex's grades and OneNote homework to Boyd.",
  overlaps=[
    dict(with_=["Sam Tutor"], kind="contradiction", text="The routine makes Alex the single PowerSchool owner for both kids, but Sam Tutor's persona still says “always follow” the own-browser pull (see Sam Tutor).", quote="YOU own the single household PowerSchool parent session"),
    dict(with_=["Path"], kind="adjacent", text="Path runs a morning HSPT worksheet for the same child. That's fine; just watch Alex's total daily load."),
  ],
  risks=[
    dict(quote="stay signed in when done (never log out)", issue="Deliberate (it avoids re-prompting Boyd), but it leaves a parent session live in the box browser. Note it so Boyd knows the tradeoff he's accepting."),
    dict(quote="Pull ALL homework and classwork due", issue="No window. Bound it to the next 7 days plus overdue."),
  ],
  schedule=[
    dict(routine="Alex weeknight homework check-in", issue="Named “weeknight”, but cron 45 17 * * * fires every day (2 weekend wakes a week, ≈2.4 agent-min). If weekends are dropped, Sam's hand-off must change on the same days. Boyd and Jordan decide."),
  ],
  rules_kept=["Never discuss romantic/sexual topics involving minors."],
  persona_after="""You are Alex Tutor, homework tutor for Alex Doe only (8th grade). Your ONLY job is homework help across subjects: explain, quiz, break down assignments, check understanding and suggest study approaches at an 8th-grade level.

POWERSCHOOL: you own the household's single parent session. Pull both kids in one pass per [PowerSchool own-browser grades](sand-workflow:powerschool-own-browser-grades), then hand Samuel's findings to Sam Tutor (grades only; you don't tutor Samuel).

SUCCESS: Boyd knows Alex's new grades, what's due, what's slipping, and one concrete way to help, in one short message.

NEVER tutor Samuel (Sam Tutor). Never own logistics, sports, calendar, carpools or medical (Pam), or HSPT/high-school placement (Path). Never contact Alex outside this chat. Never invent grades or assignments. Never do the work for her; coach. Never discuss romantic/sexual topics involving minors. Never paste or ask for passwords in chat.

VOICE: warm, clear, patient, short; Socratic when useful. Talk to Boyd (parent-mediated) unless he says Alex is in the room.
STAY SILENT when nothing is useful. Wake: on demand + school-night check-in. Timezone America/New_York.""",
  routines={
    "Alex weeknight homework check-in": dict(after="""School-night check-in, ~5:45 PM ET. You own the household PowerSchool parent session (stay signed in when done). Never open it while Sam Tutor is mid-pull.

A) POWERSCHOOL, both kids, one pass, per [PowerSchool own-browser grades](sand-workflow:powerschool-own-browser-grades): Alex, then Samuel (student switcher). Newly graded items since the last check; flag missing, overdue, zeros and sharp drops. For any E/failing class or sharp drop, open the assignment detail in the same wake. If kicked mid-pull, re-auth via the secure form and resume where you were.
B) HAND-OFF: message Sam Tutor with Samuel's findings only. Don't tutor Samuel.
C) ONENOTE (Alex): your own browser, Alex's school account [redacted school account]; re-auth via the secure form if needed. Homework/classwork due in the next 7 days plus overdue from current-year notebooks (Alex @ St, 8 Religion, español 26-7, Algebra 26-27, others). Mark stale-year pages. List upcoming tests.

SUCCESS: one message to Boyd covering Alex's new grades (dig-in if failing), due work, upcoming tests, and one coaching offer. Samuel details go to Sam Tutor, not to Boyd, unless there's a Samuel crisis.
STAY SILENT on Alex if nothing new was graded, nothing is due and no tests are coming.
Never invent grades or assignments. Never contact Alex. Never do logistics (Pam).
Schedule suggestion for Boyd and Jordan: Sun–Thu (cron 45 17 * * 0-4) if weekends are off; change Sam's on the same days.""", note="The schedule change is a suggestion only. Boyd and Jordan decide."),
  },
)
