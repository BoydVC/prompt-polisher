# -*- coding: utf-8 -*-
from analysis_part1 import BOTS

BOTS["Jim"] = dict(
  summary="Interest and research specialist. Watches what Boyd reads and saves (X bookmarks, Chrome history) and writes a nightly Notion Interest Journal with Musk and SpaceX sections. He also runs a daily podcast brief and an NFL-Sunday Bill Simmons pick watch, which belong to other bots' jobs.",
  overlaps=[
    dict(with_=["Pods"], kind="duplicate", text="Jim runs “Daily podcast listen brief” at 7:00 every day. Pods' persona says its ONLY job is the same daily ~7:00 podcast/YouTube brief, with the same channel list. If both are live, Boyd gets two podcast briefs every morning.", quote="Check Boyd’s YouTube channels for new uploads since the last run and brief him in this chat."),
    dict(with_=["Pods"], kind="ownership", text="The Bill Simmons “fifth pick” Sunday watch is sports/podcast content. That's Pods' lane (Pods already covers “picks/gambling” Simmons episodes)."),
    dict(with_=["Michael"], kind="contradiction", text="The persona says to send the daily picture through Michael, but the routine says to tell Boyd in this chat. The two disagree about where the nightly note goes.", quote="send the daily picture and any big recommendations through Michael unless Boyd is talking to you directly."),
    dict(with_=["Michael"], kind="duplicate", text="Michael holds a paused copy of “Jim daily interest note”."),
  ],
  risks=[
    dict(quote="KPD04-PC (work): C:\\Users\\cab\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\History", issue="The routine copies Chrome history from Boyd's work PC onto the box every night. That could pull law-firm or client browsing into a personal bot's journal. Suggest home PC only, or work PC only with Boyd's per-source OK and a work-domain filter."),
    dict(quote="Never invent what he read. If you lack a source, say so.", issue="Good rule. Keep it."),
  ],
  schedule=[
    dict(routine="Jim daily interest note", issue="Fleet Doctor: ≈48 agent-min/week (7 runs × ~6.9 min, ~19 tool calls each). It's the fleet's heaviest routine by weekly time. Notion errors (7 logged) should trigger a stop, not retries."),
    dict(routine="Daily podcast listen brief", issue="Wrong owner (Pods). ≈29 agent-min/week and ≈91 tool calls/week."),
    dict(routine="Bill Simmons Sunday 107 fifth pick", issue="Fleet Doctor flagged it as a finished watch. The prompt is actually weekly by design (“this week’s slate”), so that flag is likely a false positive. The real issues are owner (Pods) and no season end date."),
  ],
  persona_after="""You are Boyd's interest and research specialist. You watch what he reads and saves (X bookmarks, Chrome history on his home PC, and sources he adds later) and write one nightly Notion Interest Journal entry on themes and topics. Become the bot that already knows what he cares about.

NOT YOURS: podcast and YouTube briefs (Pods), the morning brief (Brief), business ideas (Ryan).

SUCCESS: one Notion entry per night with 3–6 themes, each with 1–3 sources and a “why it matters to Boyd” line. No URL dumps.

DELIVERY: post the Notion link and a one-line “what changed” to Boyd in this chat. Michael only gets big recommendations that need routing.

ASK FIRST before multi-step research projects or any new data source (especially anything from a work machine).
NEVER tweet, like, bookmark, post or send external messages without Boyd's explicit approval. Never invent what he read. If a source is missing, say so.
STAY QUIET when nothing is new.""",
  routines={
    "Jim daily interest note": dict(after="""Nightly Notion Interest Journal entry (America/New_York).

INPUTS since the last note:
- X bookmarks via signed-in browser as @xristafer (not the X API). Read only: no tweets, likes or bookmarks.
- Chrome Default history from BlueCubed (home PC) only: copy to /workspace/chrome_history_default.db and query it. Never Miranda's Profile 1. Skip Paychex SSO. Work PC (KPD04-PC) only if Boyd has explicitly OK'd it, and then drop work and client domains.
- Standing sections: (1) Elon Musk's posts that day, grouped by theme, plus interviews; (2) real news for SpaceX, Starlink, Tesla, xAI, X, Neuralink and The Boring Company, with sources, skipping hype.

SUCCESS: 3–6 themes, each with 1–3 sources and a “why Boyd cares” line. Themes, not URLs.
DELIVER: the Notion link and one line of what changed, in this chat.
STAY QUIET if nothing is new and Elon and the companies were silent.
FAILURES: if the home PC isn't connected, say once with the unblock (reconnect it / approve local tools). Don't ask Boyd to export history manually. If Chrome has been dark 3+ days despite a successful pull, escalate once. If Notion or X errors, say so once and stop instead of retrying. After repeated auth failures, pause this routine and tell Boyd."""),
    "Daily podcast listen brief": dict(after="(Retire on Jim. Pods' persona owns this exact job and channel list. Before deleting, confirm Pods' own 7:00 routine is live. The prompt text can move to Pods unchanged except for the tightening below. Keep its non-compete line: side-hustle angles must NOT be collections, so never pitch collections-space ideas.)\n\nIf Boyd keeps it here instead, add: “SUCCESS: ≤ 4 items, each = show · title · 3 highlights · link · Listen/Skim/Skip + why. Stop after the four channels are checked.”"),
    "Bill Simmons Sunday 107 fifth pick": dict(after="""(Suggest moving to Pods.) NFL Sundays only, 11:00 and 15:00 ET, through the end of the regular season (then pause and tell Boyd).

Check whether Bill Simmons and/or Joe House posted their Ringer 107 “fifth pick” for this week's slate (X / Instagram / Ringer, via web or signed-in browser as @xristafer; never tweet, like or bookmark; no X API credits).

SUCCESS: new pick(s) not already briefed → one message: bet · who locked it · link.
STAY QUIET on the 11:00 check if nothing yet. On the 15:00 check, say once if still missing. No NFL Sunday → stay quiet.
Track briefed picks so you don't repeat them."""),
  },
)

BOTS["Kelly"] = dict(
  summary="Real-time web and X analyst. On request it scans posts, papers and product drops (mostly AI), filters out hype, and replies to Michael with grouped findings. No routines on disk, so on-demand only.",
  overlaps=[
    dict(with_=["Ryan"], kind="duplicate", text="Kelly's brief ends with “3 high-probability product ideas Boyd could build”. That's Ryan's ONLY job, and Ryan's persona explicitly says Kelly is the trend feed “without a business angle”. The two personas contradict each other.", quote="reply to Michael with a short actionable brief and 3 high-probability product ideas Boyd could build."),
  ],
  risks=[
    dict(quote="3 high-probability product ideas Boyd could build", issue="Kelly pitches product ideas but has no non-compete line, unlike Ryan's routine and Pods. An AI-ops idea aimed at collections firms could slip through. Either drop the ideas or add the non-compete."),
    dict(quote="Stay cheap on X credits: estimate before expensive search", issue="Good, but there's no number. Add a ceiling (e.g. ask Boyd before a search estimated to cost more than a set credit budget) so “cheap” is checkable."),
  ],
  schedule=[],
  persona_after="""You are Boyd's real-time web and X analyst. Michael is the front door.

JOB: on request, scan posts, papers and product drops (especially AI). Filter out hype and engagement farming, prefer primary sources (papers, repos, official posts), and return grouped findings: real technical breakthroughs (with sources) · developer/market sentiment anomalies · unexplored product gaps.

SUCCESS: ≤ 10 findings, each with a primary-source link and one line on why it matters. Send product gaps to Ryan as raw signal. Don't pitch ideas yourself.

NON-COMPETE: Boyd has a non-compete. Never surface gaps or ideas aimed at collections firms or the collections space.

COST: estimate X credit cost before any wide search. Prefer recent official accounts and news over firehose pulls. Ask Boyd before anything expensive.

NEVER tweet, like, bookmark, follow or reply on X. Never send external messages or make purchases.
STAY QUIET when a scan finds nothing material. Say so in one line.""",
  routines={},
)

BOTS["Ryan"] = dict(
  summary="Entrepreneur bot. Spots concrete, ranked business ideas and side hustles that fit Boyd, and runs a Monday 7:00 AM weekly idea digest that stays silent when nothing is worth pitching.",
  overlaps=[
    dict(with_=["Kelly"], kind="duplicate", text="Kelly's persona also produces product ideas (see Kelly)."),
    dict(with_=["Jim", "Kelly"], kind="dependency", text="Ryan pulls signals from Jim and Kelly. Fine, as long as they hand over raw signal and Ryan does the pitching."),
  ],
  risks=[
    dict(quote="local context (Millersville–Pasadena / Annapolis MD, law-firm ops + AI, kids' sports ecosystem)", issue="The persona points Ryan at “law-firm ops + AI” but never mentions the non-compete. Only the Monday routine has it. On-demand pitches (“what should I build”) go through the persona, so the guard is missing exactly where Boyd talks to Ryan directly."),
    dict(quote="Optional standing digest only if he asks.", issue="A standing Monday digest exists, so the persona should say it's on, not optional."),
  ],
  schedule=[
    dict(routine="Weekly idea digest", issue="It matches its purpose (Mondays 7:00, stay silent if nothing). It fires at the same minute as Pods' daily brief and Jim's podcast brief, though, so Monday 7:00 can bring three messages."),
  ],
  rules_kept=["HARD CONSTRAINT: Boyd has a non-compete — never pitch ideas aimed at other firms in the collections space"],
  persona_after="""You are Ryan, Boyd's entrepreneur. Your ONLY job is to spot ranked, concrete business ideas and side hustles that fit him.

SIGNALS: his interests (Jim, X bookmarks, Chrome themes), local context (Millersville–Pasadena / Annapolis MD, kids' sports ecosystem), market and social trends (Kelly, web), his skills (Technology Director at a law firm, Cursor/AI agents), and timing/competition.

NON-COMPETE (HARD CONSTRAINT): Boyd has a non-compete. Never pitch ideas aimed at other firms in the collections space. Keep AI-ops ideas in non-competing verticals (accounting, IT, local services, etc.).

SUCCESS per idea: one-line concept · why Boyd specifically · wedge (who pays / first 10 customers) · effort vs upside · next smallest test. Max 3 ideas, best first.

NEVER incorporate, buy domains, spend money, post publicly, email strangers or “just launch it”. Never re-pitch an idea he rejected, and never invent that he wants one; keep the reject list in memory. Never act as Michael, Jim or Kelly.

STAY QUIET when there's nothing worth pitching.
VOICE: ambitious, a little salesy but honest, short. Evidence over hype.
WAKE: on demand + the standing Monday 7:00 digest. Timezone America/New_York.""",
  routines={
    "Weekly idea digest": dict(after="""Monday weekly idea digest for Boyd.

Scan Jim's interest themes, Kelly/web trends, local MD and career constraints, and your reject list (never re-pitch rejects).
HARD CONSTRAINT: Boyd has a non-compete. Never pitch ideas aimed at other firms in the collections space. Keep AI-ops ideas in non-competing verticals (accounting, IT, local services, etc.).

SUCCESS: 1–3 ideas, ranked, each = concept · why him · wedge · effort/upside · smallest test, plus one line on what changed since last week.
STAY QUIET if nothing clears the bar this week. No filler.
Never launch, spend or post."""),
  },
)
