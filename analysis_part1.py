# -*- coding: utf-8 -*-
"""Hand-written review content (part 1). Every `quote` must be an exact substring of the bot's real (redacted) text."""
ORDER = ["Michael", "Brief", "Pam", "Oscar", "Jim", "Kelly", "Ryan", "Dwight", "Pods", "Path",
         "Vic Tutor", "Char Tutor", "Boyd Family Times", "Dr. EggBot", "TokenMax"]
BOTS = {}

BOTS["Michael"] = dict(
  summary="Chief of Staff and front door. Reads Gmail, Slack and Calendar, routes specialised work to the other bots, and asks Boyd before anything external. Its two routines are paused copies of jobs that moved to Brief and Jim.",
  overlaps=[
    dict(with_=["Brief"], kind="duplicate", text="Paused copy of “Morning attention brief” (same name, nearly the same prompt) still sits on Michael. Its own persona says the brief “now lives on Brief”.", quote="The weekday morning attention brief now lives on Brief — do not recreate that standing routine on yourself."),
    dict(with_=["Jim"], kind="duplicate", text="Paused copy of “Jim daily interest note” that tells Michael to SendToAgent Jim. Jim already runs his own copy at the same 8 PM slot.", quote="Jim owns his own daily interest note cron."),
    dict(with_=["Jim"], kind="scope creep", text="Michael's persona carries Jim-specific Chrome sign-in mechanics. That's an operational rule for Jim's sources, not a Chief of Staff rule, and it costs tokens on every Michael turn.", quote="When Chrome/History (or Jim's sources) are dark and you offer box Chrome sign-in"),
  ],
  risks=[
    dict(quote="Delegate specialized tasks to the right specialist bot.", issue="No roster. Michael has to rediscover who owns what each time, and that's how duplicates like the paused brief appeared."),
    dict(quote="Ask me a clarifying question before starting any task worth more than 30 minutes.", issue="“Worth 30 minutes” is unmeasurable for a bot. Swap it for a concrete trigger (multi-step, spends money, touches someone else, or more than one specialist)."),
  ],
  schedule=[
    dict(routine="Morning attention brief", issue="Paused, and the prompt addresses “CAB” while the persona says Boyd. It duplicates Brief's live routine. Fleet Doctor flagged it as clutter that could be re-enabled by mistake."),
    dict(routine="Jim daily interest note", issue="Paused, and it duplicates Jim's live 8 PM routine. If re-enabled, Jim would be woken twice a night (≈48 agent-min/week on Jim's own copy)."),
  ],
  persona_after="""You are Boyd's Chief of Staff and the single front door. Read Gmail, Slack and Calendar; route specialised work to the owner and relay their answers.

ROSTER (route, don't redo): Brief = weekday 8:00 attention brief · Pam = family calendar, kids' sports, school, medical, travel · Oscar = money · Jim = interest journal / reading trail · Pods = podcast & YouTube briefs · Kelly = live web/X scans · Ryan = business ideas · Dwight = code via Cursor Cloud Agents · Vic Tutor / Char Tutor / Path = kids' schoolwork & HS placement (parent-mediated) · Boyd Family Times = daily paper · Dr. EggBot = new bots & fleet healthchecks · TokenMax = leftover-usage builds.

SUCCESS: every request lands with exactly one owner; Boyd gets one consolidated answer, not the same news from two bots.

ASK FIRST when a task is multi-step, involves more than one specialist, spends money, or touches anyone outside the household.

NEVER: send external messages or make purchases without Boyd's approval; recreate routines that other bots own (the morning brief is Brief's, the interest note is Jim's).

STAY QUIET when there's nothing to report or a specialist already told Boyd the same thing.""",
  routines={
    "Morning attention brief": dict(after="(Delete this paused copy. Brief owns the live routine. Nothing to rewrite.)", note="Recommendation only. Boyd deletes it if he agrees."),
    "Jim daily interest note": dict(after="(Delete this paused copy. Jim owns the live routine. Nothing to rewrite.)", note="Recommendation only."),
  },
)

BOTS["Brief"] = dict(
  summary="Writes Boyd's weekday 8:00 AM attention brief from Gmail, Slack and Calendar: decisions, deadlines, meetings and people waiting. Stays quiet when nothing is urgent.",
  overlaps=[
    dict(with_=["Pam"], kind="overlap", text="Brief reads Google Calendar “today plus the next few days” at 8:00. Pam's weekday scan reads the family calendars 30 minutes earlier. Family conflicts can surface twice.", quote="Google Calendar (today plus the next few days)"),
    dict(with_=["Oscar"], kind="overlap", text="Brief reads Gmail for mail “that needs a reply or decision”. Oscar's due-soon bills run reads the same Gmail 45 minutes later. A past-due notice can appear in both.", quote="Read Gmail (mail that needs a reply or decision)"),
    dict(with_=["Michael"], kind="duplicate", text="Michael still holds a paused copy of this routine (see Michael)."),
  ],
  risks=[
    dict(quote="Prepare CAB's weekday morning attention brief.", issue="The routine calls him “CAB” while the persona says “Boyd”. It's harmless, but it's a sign the prompt was copied from Michael's old routine, and the two copies will drift."),
    dict(quote="today plus the next few days", issue="“A few days” is vague. Pin it (today plus the next 2 business days) so briefs are comparable day to day."),
  ],
  schedule=[
    dict(routine="Morning attention brief", issue="Fleet Doctor: missed 2 of 4 scheduled runs in the logged window (to Sep 15). The prompt has no “say once if a connector is down” line in the persona, only in the routine."),
  ],
  persona_after="""You write Boyd's weekday morning attention brief. Nothing else.

SOURCES: Gmail (needs a reply or decision), Slack (mentions/threads waiting on Boyd), Google Calendar (today + next 2 business days).

SUCCESS: at most 7 bullets, each = what, who's waiting, by when, one suggested next step. Readable in under 60 seconds.

DE-DUPE: skip bills, payments and money notices (Oscar's), and kids' sports/school/family-calendar conflicts (Pam's), unless they need a decision from Boyd today and the owner hasn't flagged them.

STAY QUIET if nothing is new or urgent since yesterday's brief. No “all clear” messages.

NEVER: send external messages, buy anything, take on other work (Michael is the front door), or expand into Chief of Staff duties.

VOICE: crisp memo, no fluff. Wake: weekdays 8:00 America/New_York + on demand.""",
  routines={
    "Morning attention brief": dict(after="""Prepare Boyd's weekday morning attention brief.

1. Gmail: threads from the last 24 h (72 h on Monday) that need a reply or decision from Boyd.
2. Slack: mentions and threads waiting on Boyd.
3. Calendar: today + next 2 business days. Flag prep needed, conflicts, and meetings with no agenda.
4. Drop anything Oscar (bills/money) or Pam (family calendar) owns unless it needs Boyd's decision today.

SUCCESS: ≤ 7 bullets: item · who's waiting · deadline · suggested next step.
STAY QUIET if nothing new or urgent since the last brief. No filler.
If a connector fails, say once which one to reconnect; after two failed runs in a row, pause this routine and tell Boyd.
Never send external messages or make purchases."""),
  },
)
