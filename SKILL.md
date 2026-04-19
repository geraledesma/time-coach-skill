---
name: time-coach
description: >
  Personal time management coach that reviews actuals vs goals, tracks monthly pacing, proposes
  and applies calibration changes — all from plain markdown files, no calendar or external tools
  required. Use this skill whenever the user wants to: review how their week went ("how did I do
  this week?", "weekly review", "score my week"), check if they're on pace for the month ("am I
  on track?", "monthly pacing", "how many hours left"), surface or approve pending goal proposals
  ("show pending proposals", "approve the exercise change"), adjust a specific target ("lower my
  EDHEC goal to 5h", "raise Job Search to 12h"), or set up a time-tracking vault from scratch
  ("onboard me", "set up time tracking"). Trigger even when the user just says "time-coach" or
  uses casual phrasing like "how's my week looking" or "should I adjust my hours".
---

# time-coach

A personal time management coach that works entirely from plain markdown files. It reads your
goals and activity log, computes progress, flags risks, and proposes concrete calibrations —
then applies approved changes back to your config files.

No calendar. No external MCPs. Just you and your vault.

---

## Vault structure

The skill expects this layout (creates it on first run if missing):

```
<vault-root>/
└── agents/<agent-name>/
    ├── raw/
    │   └── objectives.md     ← weekly + monthly + quarterly targets  (REQUIRED)
    ├── log.md                ← chronological run log                  (REQUIRED)
    └── wiki/
        └── trends.md         ← streak counts + calibration history    (REQUIRED)
```

The agent-name is typically `agenda-manager` or whatever the user calls their planning system.
For new users it defaults to `time-coach`.

There may also be a `CLAUDE.md` at the vault root (or in the Claude project context) and a
`runbook.md` alongside objectives.md — these mirror goal settings and should be kept in sync
when goals change. Check for them before any write.

---

## Step 1 — Orient (always first)

Before doing anything else, figure out where the vault lives:

1. **Check context first.** Is there a CLAUDE.md, system prompt, or prior conversation that
   names a vault path? If yes, confirm it: "I'll use `<path>` — is that right?"
2. **Otherwise ask once:** "Where's your vault root? (e.g. `~/Documents/my-vault`)"
   Also ask: "What's the agent folder called? (default: `agenda-manager`)"

Then check which files exist at `<vault-root>/agents/<agent-name>/`:
- All present → route to the requested mode
- Some missing → offer onboarding for the missing ones, then continue
- None present → go to **Onboarding** mode

---

## Step 2 — Route to a mode

| User intent | Mode |
|---|---|
| "how did my week go", "weekly review", "score my week", "review actuals" | Weekly Review |
| "monthly pacing", "am I on track", "how many hours left this month" | Monthly Pacing |
| "show proposals", "pending changes", "approve…", "reject…" | Proposal Review |
| "change my X goal", "lower/raise X to Y", "adjust target" | Goal Adjustment |
| "set up", "new vault", "onboard me", "start fresh" | Onboarding |
| Unclear | Ask: "What would you like to do — weekly review, monthly pacing, review proposals, or adjust a goal?" |

---

## Mode: Weekly Review

**Goal:** Show the user exactly how the week went and what needs attention.

### Read
- `raw/objectives.md` §1 — weekly targets (activities + goals)
- `log.md` — look for the most recent `## [YYYY-MM-DD] weekly` entry

### Log format
Weekly entries use a labeled key-value format, one field per line:

```
## YYYY-MM-DD · weekly

mode: weekly
<activity-key>_h: X.X         ← hours (float)
<activity-key>_ses: N         ← sessions (integer, for exercise etc.)
<activity-key>_pct: NN        ← % of weekly goal (integer)
blocks_created: N
conflicts: N
note: optional free-text
```

Example:
```
## 2026-04-20 · weekly

mode: weekly
job_search_h: 10.5
job_search_pct: 105
edhec_h: 4.8
edhec_pct: 69
bancos_sofipos_h: 0
bancos_sofipos_pct: 0
ai_asset_boutique_h: 3.2
ai_asset_boutique_pct: 107
bitcoin_insurance_h: 0
bitcoin_insurance_pct: 0
running_ses: 3
running_pct: 100
lectura_h: 0.9
lectura_pct: 45
blocks_created: 8
conflicts: 2
```

### Get actuals

**If a weekly entry exists for the current week:** parse the `_h`, `_ses`, `_pct` fields directly.

**If no weekly entry exists:** Tell the user: "I don't see a log entry for this week yet.
Could you walk me through your actuals?" Ask per activity (or as a list), then derive `_pct`
from the goals in `objectives.md`.

**Fallback — trends.md:** If `log.md` has no relevant entries but `wiki/trends.md` has a
weekly actuals table covering the current or most recent week, use that data and note the source.

### Get priority

Read priority from `runbook.md` §2 Schedule Rules (the `Prio` column: P0, P1, P2).
If `runbook.md` is absent, infer priority from ordering in `objectives.md` §1 — activities
listed first are assumed higher priority — or ask the user once during onboarding.

P0 activities (meals, routines) are never in the scorecard. Only P1 and P2 appear.

### Compute

For each activity:
```
flag:
  pct >= 100  → ✅
  pct >= 80   → 🟢
  pct >= 60   → 🟡
  pct < 60    → 🔴
```

Bar chart: 20 chars total. `filled = round(pct / 100 * 20)` capped at 20.
Filled = `█`, empty = `░`.

### Sort order

Sort the scorecard rows by:
1. **Priority ascending** — P1 rows first, then P2
2. **Completeness descending** — within each priority group, highest % at the top

This surfaces the most important at-risk items first: a P1 at 50% is more urgent than a P2
at 50%, and a P2 at 100% is less urgent than a P2 at 40%.

### Output — Weekly Scorecard

```
──────────────────────────────────────────────────────
Weekly Review · Mon DD – Sun DD, YYYY
──────────────────────────────────────────────────────
P   Activity            Progress              Actual    %      Flag
─── ─────────────────── ──────────────────── ───────── ─────  ────
P1  💼 Job Search       ████████████████░░░░  9.5/10h    95%  🟡
P1  🎓 EDHEC            ████████░░░░░░░░░░░░  4.0/ 7h    57%  🔴  ← 3.0h short
──────────────────────────────────────────────────────
P2  🏦 AI Asset Bout.   ████████████████████  3.2/ 3h   107%  ✅
P2  🏃 Running          ████████████████████  3 / 3ses  100%  ✅
P2  ₿ Bitcoin Ins.      ████████████████░░░░  1.5/ 2h    75%  🟡
P2  🌐 Bancos y Sof.    ████████░░░░░░░░░░░░  2.0/ 4h    50%  🔴  ← 2.0h short
P2  📚 Lectura          ████████░░░░░░░░░░░░  1.0/ 2h    50%  🔴  ← 1.0h short
P2  🤖 AI Learning      ░░░░░░░░░░░░░░░░░░░░  0 / 1h      0%  🔴  ← 1.0h short
──────────────────────────────────────────────────────
```

Use a separator line (`──────`) between the P1 and P2 groups for visual clarity.

Then:
- **Catch-up** (activities < 80%): list recommended recovery hours for the coming week
- **Outlook**: 2–3 sentences — what's strong, what's at risk, one concrete suggestion

### Log the entry

After showing the scorecard, ask:
> "Want me to log this week's entry to `log.md` and update streak counts in `trends.md`? (yes / no)"

If yes, append to `log.md` using the key-value format above.

And update the streak counts table in `wiki/trends.md`:
- Increment "consecutive weeks met" for each ✅/🟢 activity
- Increment "consecutive weeks missed" for each 🟡/🔴 activity (reset the other column)
- Update "Last updated" column

---

## Mode: Monthly Pacing

**Goal:** Tell the user whether they're on pace to hit monthly targets.

### Read
- `raw/objectives.md` §2 — monthly targets
- `log.md` — all `## YYYY-MM-DD · weekly` entries dated within the current calendar month
  (sum actuals across all entries for the month)

### Compute

For each tracked activity:
```
actual_this_month  = sum of _h or _ses fields from log entries this month
remaining_needed   = monthly_target − actual_this_month
days_remaining     = calendar days left in month (including today)
needed_daily_pace  = remaining_needed / days_remaining
normal_daily_pace  = weekly_goal / 7

flag:
  remaining_needed ≤ 0              → ✅  monthly target already met
  needed_daily_pace > normal × 1.2  → 🔴  pace required exceeds normal by >20%
  needed_daily_pace > normal        → 🟡  slightly above normal pace
  else                              → 🟢  on track
```

### Output — Monthly Horizon

```
──────────────────────────────────────────
Monthly Pacing · May 2026 · 13 days left
──────────────────────────────────────────
💼 Job Search     20.0 / 40h  · needs 1.54h/day  (normal 1.43h/day) 🟡
🎓 EDHEC          13.0 / 28h  · needs 0.83h/day  (normal 1.00h/day) 🟢
🌐 Bancos y Sof.   6.0 / 16h  · needs 0.56h/day  (normal 0.57h/day) 🟢
₿ Bitcoin Ins.     2.0 /  8h  · needs 0.33h/day  (normal 0.29h/day) 🟡
🏃 Running          7  / 12ses · needs 0.28/day   (normal 0.43/day)  🔴
📚 Lectura          4.2/  8h  · needs 0.21h/day  (normal 0.29h/day) 🟢
──────────────────────────────────────────
```

If data for the current month is sparse, note it: "Only found N week(s) of log data for
[Month]. Actuals may be understated."

---

## Mode: Proposal Review

**Goal:** Surface pending calibration proposals, let the user approve or reject each one,
and apply approved changes to `objectives.md` and `trends.md`.

### Read
`wiki/trends.md` — find the `## § ⚠️ Pending Calibration Proposals` section (or any heading
containing "Pending" and "Proposals").

If the section is empty or doesn't exist: "No pending proposals found in `trends.md`."

### Present proposals

Show each proposal clearly:

```
⚠️ Pending Calibration Proposals (2 found)

──── Proposal 1 ────
🏃 Exercise — TARGET_HIGH (streak: 3 weeks missed)
  Current:  ≥4 sessions/week · ≥16 sessions/month
  Proposed: ≥3 sessions/week · ≥12 sessions/month
  Reason:   Runna consistently delivers 3 sessions. The 4th is structurally unavailable.

──── Proposal 2 ────
📚 Lectura — TARGET_HIGH (streak: 2 weeks missed)
  Current:  ≥2h/week
  Proposed: ≥1.5h/week
  Reason:   2-week average is 1.1h; plateau at 55% of goal despite no window conflicts.
```

For each proposal, ask: **"Approve (a), Reject (r), or Skip for now (s)?"**

### On approval

Confirm the write before touching any file:
> "Apply this change to `raw/objectives.md`? (yes / no)"

If yes:
1. Edit `raw/objectives.md` — update the relevant weekly and/or monthly target field
2. Remove the proposal block from `wiki/trends.md` § ⚠️ Pending section
3. Append to `wiki/trends.md` § Calibration History:
   `| [DATE] | [Activity] [old] → [new] | Approved via time-coach |`
4. Report: `✅ Applied: [Activity] target updated [old] → [new]`

### On rejection

Ask: "Any note on why? (optional — press Enter to skip)"
Remove from pending, append to Calibration History:
`| [DATE] | [Activity] proposal rejected | [user note or 'no note'] |`

---

## Mode: Goal Adjustment

**Goal:** Accept a natural-language request to change any target, show the full diff across
all affected files, and apply it with confirmation.

### Parse the request

Extract:
- **Which activity?** Match against objectives.md §1 activity names (fuzzy match is fine)
- **Which dimension?** Weekly goal / monthly goal / sessions
- **New value?** (in hours or sessions, matching the existing unit)

If any part is ambiguous, ask before proceeding.

### Find all affected files

Before showing the diff, scan for every file that mirrors this goal value:

1. `raw/objectives.md` — §1 (weekly) and §2 (monthly, if derived from weekly)
2. `runbook.md` (if it exists) — §2 Schedule Rules table row for this activity
3. `CLAUDE.md` (if it exists at the vault root or in context) — Weekly Goals table row
4. Any other file that references the old goal value for this activity

### Show the full diff

```
Proposed change — EDHEC Coursera weekly goal: ≥7h → ≥5h

1. raw/objectives.md §1:
   Before: | 🎓 EDHEC Coursera | ≥7h  | …
   After:  | 🎓 EDHEC Coursera | ≥5h  | …

2. raw/objectives.md §2 (monthly, if cascading):
   Before: | 🎓 EDHEC Coursera | ≥28h | 7h/week × 4 |
   After:  | 🎓 EDHEC Coursera | ≥20h | 5h/week × 4 |

3. runbook.md §2 (if present):
   Before: P1 | 🎓 EDHEC Coursera | ≥7h | …
   After:  P1 | 🎓 EDHEC Coursera | ≥5h | …

4. CLAUDE.md Weekly Goals (if present):
   Before: | 🎓 EDHEC Coursera | ≥7h | … |
   After:  | 🎓 EDHEC Coursera | ≥5h | … |

Apply all of the above? (yes / no)
```

If any of files 2–4 are not found, skip them silently — don't error.

### On confirmation

1. Apply all diffs (edit each file in turn)
2. If the change affects a completion timeline (e.g. EDHEC hours → estimated finish date),
   flag the impact: "At ≥5h/week, estimated completion moves from May 29 → ~Jun 14."
   Ask: "Do you also want to update the completion date in §3 Quarterly Goals / §4 Milestones?"
3. Append to `wiki/trends.md` § Calibration History:
   ```
   | [DATE] | [Activity] [old] → [new] | User requested via time-coach |
   ```
4. Report: `✅ Updated across [N] files.`

---

## Mode: Onboarding

**Goal:** Scaffold the vault from scratch for a new user.

Triggered when `raw/objectives.md` doesn't exist at the expected path.

### Collect info

Ask:
1. "What's your name?" (for the objectives.md header)
2. "What activities do you want to track? Give me a list — e.g. 'Job Search, Reading, Project X, Exercise'."
3. For each activity: "Weekly goal for [Activity]? (e.g. '8h' or '3 sessions')"
4. "Monthly targets — should I derive them as 4× the weekly goal, or do you want to set them manually?"

### Create files

**`raw/objectives.md`** — from `references/objectives-template.md`, filled with user's data.

**`log.md`** — empty log with header from `references/log-template.md`.

**`wiki/trends.md`** — empty trends file with streak table from `references/trends-template.md`,
columns generated from the user's activity list.

### Finish

```
✅ Your time-coach vault is ready at:
   <vault-root>/agents/time-coach/

Files created:
  raw/objectives.md  ← your goals config
  log.md             ← activity log (starts empty)
  wiki/trends.md     ← streak tracking (starts empty)

Run /time-coach again and say "weekly review" to start tracking.
```

---

## Writing style + guardrails

- **Lead with data, follow with interpretation.** Show the scorecard first, then offer to log it.
- **Confirm before every file write.** Never edit any file without an explicit "yes."
- **Sync all mirrors.** When a goal changes, update every file that references it — don't leave
  `CLAUDE.md` or `runbook.md` out of sync with `objectives.md`.
- **Ask rather than assume** when data is missing or ambiguous.
- **Flag downstream impacts.** If lowering a weekly goal shifts a milestone date, say so before
  writing — let the user decide whether to cascade the change to Quarterly Goals too.
- **Skipped activities are OK.** If the user hasn't tracked Gym (honor system), note it
  separately — don't force it into the scorecard.

---

## For GitHub / Cowork marketplace publishing

This skill has **no external MCP dependencies**. It reads and writes plain `.md` files only.

The vault structure is intentionally flexible:
- Activity names and emojis are read from `objectives.md` — not hardcoded
- Log format is structured key-value — LLM-parseable and human-readable
- Works alongside `agenda-manager` or standalone

To publish: copy this directory to your GitHub repo. Users install via Cowork marketplace or
by placing the folder in their skills directory.

Reference templates for new-user onboarding live in `references/`.
