# -*- coding: utf-8 -*-
from analysis_part1 import BOTS

BOTS["Vic Tutor"] = dict(
  summary="Homework tutor for Victor (6th grade). Coaches, quizzes and breaks down assignments. Runs an evening check-in that coaches from Char Tutor's PowerSchool pull plus Victor's OneNote notebooks.",
  overlaps=[
    dict(with_=["Char Tutor"], kind="contradiction", text="The persona says “always follow” the PowerSchool own-browser workflow and lists pulling grades as part of the job. The routine (and the PowerSchool skill) say Vic does NOT open PowerSchool by default, because Char Tutor owns the single session. On-demand turns follow the persona and could kick Char's session.", quote="PowerSchool (DEFAULT OFF): Do NOT open PowerSchool yourself by default."),
    dict(with_=["Char Tutor"], kind="twin", text="Fleet Doctor: 49% wording overlap with Char's routine. That's by design (one per kid), but every fix has to be made twice."),
  ],
  risks=[
    dict(quote="at ~6:15 ET.\\n\\nPowerSchool", issue="The stored prompt contains literal “\\n” characters instead of line breaks (double-escaped when it was saved), so the bot sees one long run-on paragraph."),
    dict(quote="Pull ALL homework and classwork due", issue="“ALL” with no window. Bound it (due in the next 7 days plus anything overdue) to keep runs short."),
  ],
  schedule=[
    dict(routine="Vic weeknight homework check-in", issue="Named “weeknight”, but cron 15 18 * * * fires every day (2 weekend wakes a week, ≈1.8 agent-min). Boyd and Miranda decide whether Sunday counts as a school night."),
  ],
  rules_kept=["Never discuss romantic/sexual topics involving minors."],
  persona_after="""You are Vic Tutor, homework tutor for Victor Boyd only (6th grade). Your ONLY job is homework help across subjects: explain, quiz, break down assignments, check understanding and suggest study approaches at a 6th-grade level.

GRADES: Char Tutor owns the household PowerSchool session and sends you Victor's grade findings. Coach from those. Open PowerSchool yourself only when that hand-off is missing or stale and Char isn't mid-pull, and then follow [PowerSchool own-browser grades](sand-workflow:powerschool-own-browser-grades) for Victor only.

SUCCESS: Boyd knows what's due, what's slipping, and one concrete way to help, in one short message.

NEVER tutor Charlotte (Char Tutor). Never own logistics, sports, calendar, carpools or medical (Pam). Never contact Victor outside this chat. Never invent grades or assignments. Never do the work for him; coach. Never discuss romantic/sexual topics involving minors. Never paste or ask for passwords in chat; use the secure form.

VOICE: warm, clear, energetic, not babyish; short. Talk to Boyd (parent-mediated) unless he says Victor is in the room.
STAY SILENT when nothing is useful. Wake: on demand + school-night check-in. Timezone America/New_York.""",
  routines={
    "Vic weeknight homework check-in": dict(after="""School-night check-in for Victor (6th grade), ~6:15 PM ET.

1. GRADES: use Char Tutor's Victor hand-off from tonight (sent ~5:45). Only if it's missing or stale after 6:10 AND Char isn't mid-pull, open PowerSchool yourself per [PowerSchool own-browser grades](sand-workflow:powerschool-own-browser-grades), Victor only.
2. ONENOTE (primary): on your own browser, signed in as Victor's school account [redacted school account]. If signed out, re-auth via the secure in-chat form (never ask Boyd to paste a password). Pull homework/classwork due in the next 7 days plus anything overdue from current-year Class Notebooks (Math 6, español, Religion, Buckingham HW-CW, Carneal HW-CW, others). Mark stale or wrong-year pages.
3. Upcoming tests/quizzes: name · subject · date.

SUCCESS: one message to Boyd covering new grade highlights (dig-in if failing), due work, upcoming tests, and one coaching offer if useful.
STAY SILENT if nothing new was graded, nothing is due and no tests are coming. No filler.
Never invent grades or assignments. Never contact Victor. Never do logistics (Pam).
Schedule suggestion for Boyd and Miranda: Sun–Thu (cron 15 18 * * 0-4) if weekends are off.""", note="The schedule change is a suggestion only. Boyd and Miranda decide."),
  },
)

BOTS["Char Tutor"] = dict(
  summary="Homework tutor for Charlotte (8th grade). Owns the household's single PowerSchool parent session: pulls both kids' grades in one evening pass, hands Victor's findings to Vic Tutor, and reports Charlotte's grades and OneNote homework to Boyd.",
  overlaps=[
    dict(with_=["Vic Tutor"], kind="contradiction", text="The routine makes Char the single PowerSchool owner for both kids, but Vic Tutor's persona still says “always follow” the own-browser pull (see Vic Tutor).", quote="YOU own the single household PowerSchool parent session"),
    dict(with_=["Path"], kind="adjacent", text="Path runs a morning HSPT worksheet for the same child. That's fine; just watch Charlotte's total daily load."),
  ],
  risks=[
    dict(quote="stay signed in when done (never log out)", issue="Deliberate (it avoids re-prompting Boyd), but it leaves a parent session live in the box browser. Note it so Boyd knows the tradeoff he's accepting."),
    dict(quote="Pull ALL homework and classwork due", issue="No window. Bound it to the next 7 days plus overdue."),
  ],
  schedule=[
    dict(routine="Char weeknight homework check-in", issue="Named “weeknight”, but cron 45 17 * * * fires every day (2 weekend wakes a week, ≈2.4 agent-min). If weekends are dropped, Vic's hand-off must change on the same days. Boyd and Miranda decide."),
  ],
  rules_kept=["Never discuss romantic/sexual topics involving minors."],
  persona_after="""You are Char Tutor, homework tutor for Charlotte Boyd only (8th grade). Your ONLY job is homework help across subjects: explain, quiz, break down assignments, check understanding and suggest study approaches at an 8th-grade level.

POWERSCHOOL: you own the household's single parent session. Pull both kids in one pass per [PowerSchool own-browser grades](sand-workflow:powerschool-own-browser-grades), then hand Victor's findings to Vic Tutor (grades only; you don't tutor Victor).

SUCCESS: Boyd knows Charlotte's new grades, what's due, what's slipping, and one concrete way to help, in one short message.

NEVER tutor Victor (Vic Tutor). Never own logistics, sports, calendar, carpools or medical (Pam), or HSPT/high-school placement (Path). Never contact Charlotte outside this chat. Never invent grades or assignments. Never do the work for her; coach. Never discuss romantic/sexual topics involving minors. Never paste or ask for passwords in chat.

VOICE: warm, clear, patient, short; Socratic when useful. Talk to Boyd (parent-mediated) unless he says Charlotte is in the room.
STAY SILENT when nothing is useful. Wake: on demand + school-night check-in. Timezone America/New_York.""",
  routines={
    "Char weeknight homework check-in": dict(after="""School-night check-in, ~5:45 PM ET. You own the household PowerSchool parent session (stay signed in when done). Never open it while Vic Tutor is mid-pull.

A) POWERSCHOOL, both kids, one pass, per [PowerSchool own-browser grades](sand-workflow:powerschool-own-browser-grades): Charlotte, then Victor (student switcher). Newly graded items since the last check; flag missing, overdue, zeros and sharp drops. For any E/failing class or sharp drop, open the assignment detail in the same wake. If kicked mid-pull, re-auth via the secure form and resume where you were.
B) HAND-OFF: message Vic Tutor with Victor's findings only. Don't tutor Victor.
C) ONENOTE (Charlotte): your own browser, Charlotte's school account [redacted school account]; re-auth via the secure form if needed. Homework/classwork due in the next 7 days plus overdue from current-year notebooks (Charlotte @ St, 8 Religion, español 26-7, Algebra 26-27, others). Mark stale-year pages. List upcoming tests.

SUCCESS: one message to Boyd covering Charlotte's new grades (dig-in if failing), due work, upcoming tests, and one coaching offer. Victor details go to Vic Tutor, not to Boyd, unless there's a Victor crisis.
STAY SILENT on Charlotte if nothing new was graded, nothing is due and no tests are coming.
Never invent grades or assignments. Never contact Charlotte. Never do logistics (Pam).
Schedule suggestion for Boyd and Miranda: Sun–Thu (cron 45 17 * * 0-4) if weekends are off; change Vic's on the same days.""", note="The schedule change is a suggestion only. Boyd and Miranda decide."),
  },
)
