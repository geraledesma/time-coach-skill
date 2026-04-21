---
name: time-coach
description: >
  Personal time management coach that reviews actuals vs goals, tracks monthly pacing, proposes
  and applies calibration changes — all from plain markdown files, no calendar or external tools
  required. Use this skill whenever the user wants to: review how their week went ("how did I do
  this week?", "weekly review", "score my week"), plan the upcoming week ("how does next week
  look?", "plan next week"), check if they're on pace for the month ("am I on track?", "monthly
  pacing", "how many hours left"), surface or approve pending goal proposals ("show pending
  proposals", "approve the exercise change"), adjust a specific target ("lower my Online Course
  goal to 5h", "raise Work Project to 12h"), or set up a time-tracking vault from scratch
  ("onboard me", "set up time tracking"). Trigger even when the user just says "time-coach" or
  uses casual phrasing like "how's my week looking" or "should I adjust my hours".
---

# time-coach

A personal time management coach that works entirely from plain markdown files. It reads your
goals and activity log, computes progress, flags risks, and proposes concrete calibrations —
then applies approved changes back to your config files.

No calendar required. Google Calendar integration is optional and auto-detected.
When connected, the skill reads actuals from your calendar, suggests and creates
scheduling blocks, and runs autonomous daily/weekly sync. Without it, the skill
works entirely from plain markdown files.

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

## Activity Types

Every activity in `objectives.md` §1 has a `Type` column. The type controls how the coach
tracks, coaches, and calibrates each activity. Three types are supported:

| Type | Definition | Examples |
|---|---|---|
| `must-do` | Compulsory, non-negotiable. Skipping is a problem, not a calibration signal. | Breakfast, homework, scheduled work hours, school obligations |
| `habit` | Non-compulsory but beneficial, recurring. Includes learning activities. Consistency over time is the goal. | Exercise, reading, meditation, online course (ongoing), language practice |
| `project` | Self-imposed, has a defined finish line. Requires metrics and milestone follow-ups. | Building a product, completing a certification, writing a book, launching something |

### How type changes coach behavior

**must-do:**
- Always highest priority within its tier; missed = blocker
- Coach asks "what happened?" — not "should we lower this?"
- Never generates a calibration proposal to lower the goal
- No streak-to-proposal logic

**habit:**
- 80%+ consistency = success (habits don't need 100%)
- Streak tracking is the primary metric — celebrate streaks, gently flag breaks
- 2+ week misses trigger a calibration proposal (standard logic)
- Coach frames check-ins positively: "Did you keep the chain going for [Habit]?"

**project:**
- Must have `Tracking: completion:Xunits` and a target date in §3/§4
- Coach computes estimated finish at current pace:
  `estimated_finish = today + (remaining_units / avg_units_per_week)`
  If `estimated_finish > target_date` → flag 🔴 at-risk, show gap in days
- Rhythm-based progress check-ins (Check C, Step 1b)
- Calibration proposal may adjust pace **or** target date — present both options

---

## Step 0 — Capability Probe (silent, always runs first)

Attempt `mcp__claude_ai_Google_Calendar__list_calendars` with no arguments.
- Success → set `gcal_available = true`. Cache the returned calendar list in session memory.
- Any error (tool not found, permission denied, or any other error) → set `gcal_available = false`. Do not surface this to the user.

After Step 1 locates the vault, also check for `<vault-root>/agents/<agent-name>/runbook.md` with a `§1 · Calendars` section:
- Present with §1 → set `runbook_available = true`. Parse the Read+Write calendar ID from §1.
- Absent or §1 missing → set `runbook_available = false`.

Also read `objectives.md § Config` to get `review_cadence`, `sync_cadence`, `write_cadence`, `write_horizon`, `timezone`.
If `§ Config` is absent, use defaults: `review_cadence=7`, `sync_cadence=1`, `write_cadence=7`, `write_horizon=7`.

---

## Step 1 — Orient (always first)

Before doing anything else, figure out where the vault lives:

1. **Check context first.** Is there a CLAUDE.md, system prompt, or prior conversation that
   names a vault path? If yes, confirm it: "I'll use `<path>` — is that right?"
2. **Otherwise ask once:** "Where's your vault root? (e.g. `~/Documents/my-vault`)"
   Also ask: "What's the agent folder called? (default: `agenda-manager`)"

**Legacy vault migration:** Before checking files, detect whether a vault migration is needed:
1. Check `<vault-root>/agents/time-coach/` — if present, use it.
2. Else check `<vault-root>/agents/agenda-manager/` — if present, offer once:
   > "I found your vault at `agents/agenda-manager/`. Want me to rename it to `agents/time-coach/` to match the skill? (yes / keep as-is)"
   - If yes: rename the folder, report `✅ Vault migrated to agents/time-coach/`, continue.
   - If no: use `agents/agenda-manager/` for the session.
3. If neither exists: go to **Onboarding** mode.

Then check which files exist at `<vault-root>/agents/<agent-name>/`:
- All present → continue to Step 1b
- Some missing → offer onboarding for the missing ones, then continue
- None present → go to **Onboarding** mode

### Step 1b — Proactive check-in (before routing)

Run these two checks silently after confirming vault files exist. Only run for modes that use
log data (Weekly Review, Next Week Planning, Monthly Pacing). Skip for Proposal Review and
Goal Adjustment.

**Check A — Stale log:**
Read the date header of the most recent `## YYYY-MM-DD · review` (or legacy `## YYYY-MM-DD · weekly`) entry in `log.md`.
If that date is more than `review_cadence` days before today:
> "Last review was [YYYY-MM-DD] — [N] days ago. Want to do a quick check-in first before [requested mode]? (yes / no)"
If yes: run Review first, then return to the originally requested mode.

**Check B — Undated quarterly goals:**
Scan `raw/objectives.md` §3 Quarterly Goals for any row where Target Date is blank, `—`, `TBD`,
or `YYYY-MM-DD`.
If any are found, ask once:
> "I notice [Goal X] (and N others) in §3 have no target date — when do you want to complete them? (or 'skip')"
Collect dates if provided and offer to write them: "Want me to fill in those dates in objectives.md? (yes / no)"

**Check C — Rhythm-based progress check-ins:**

Goals have different natural check-in frequencies. After confirming the vault, scan
`objectives.md` §3 Quarterly Goals and §4 Project Milestones for activities, and §1 for
any completion-tracked goals (`Tracking: completion:Xunits`). For each, determine its
check-in cadence from its time horizon:

| Time horizon | Check-in cadence | Example |
|---|---|---|
| < 4 weeks (short-term) | Every session | Sprint tasks, weekly deliverables |
| 4–12 weeks (medium-term) | Every 2 weeks | Monthly projects, courses |
| > 12 weeks (long-term) | Every 4 weeks | Quarterly goals, multi-month work |

To know when you last asked, look for `progress_checkin_[activity]:` entries in `log.md`
(written when you log a progress update) or note the date of the last `activity_completion`
field for that activity. If no record exists, treat it as overdue.

For each goal that is **due for a check-in**, surface it proactively at session start:
> "Quick progress check — [Activity]: [last known state, e.g. 'you were on page 80 of 200 last week']. Where are you now?"

Parse the answer, render the completion bar inline, and store it in log.md:
```
progress_checkin_[activity]: YYYY-MM-DD · X/Y · NN%
```

**Limit:** surface at most 2 progress check-ins per session (the most overdue ones).
Batch them: "A couple of quick progress checks before we dive in:" then ask one at a time.

Run all three checks in sequence. If none fire, proceed to routing silently.

---

## Step 2 — Route to a mode

| User intent | Mode |
|---|---|
| "how did my week go", "weekly review", "review", "score my week", "review actuals" | Review |
| "next week", "plan next week", "how does next week look", "weekly planning", "what should I focus on next week", "prepare for next week" | Next Week Planning |
| "monthly pacing", "am I on track", "how many hours left this month" | Monthly Pacing |
| "show proposals", "pending changes", "approve…", "reject…" | Proposal Review |
| "change my X goal", "lower/raise X to Y", "adjust target" | Goal Adjustment |
| "set up", "new vault", "onboard me", "start fresh" | Onboarding |
| "sync calendar", "run daily sync", "update blocks", "daily sync" | Calendar Sync |
| "create next week blocks", "schedule next week", "write calendar", "weekly write" | Calendar Write |
| "quick status", "status", "how are things" | Quick Status |
| Present-tense + no temporal marker (e.g. "how is my week looking") | Ask: "Do you mean how this week went (review actuals), or how next week looks (planning ahead)?" |
| Unclear | Ask: "What would you like to do — review, next week planning, monthly pacing, review proposals, adjust a goal, or calendar sync?" |

---

## Mode: Review

**Goal:** Show the user exactly how the tracked period went and what needs attention.

### Read
- `raw/objectives.md` §1 — weekly targets (activities + goals)
- `log.md` — look for the most recent `## [YYYY-MM-DD] weekly` entry

### Log format
Review entries use a labeled key-value format, one field per line. Header uses `· review`; legacy `· weekly` entries are parsed identically.

```
## YYYY-MM-DD · review

mode: review
<activity-key>_h: X.X         ← hours (float)
<activity-key>_ses: N         ← sessions (integer, for exercise etc.)
<activity-key>_pct: NN        ← % of weekly goal (integer)
blocks_created: N
conflicts: N
note: optional free-text
```

Example:
```
## 2026-04-20 · review

mode: review
work_project_h: 10.5
work_project_pct: 105
online_course_h: 4.8
online_course_pct: 69
side_project_a_h: 0
side_project_a_pct: 0
side_project_b_h: 3.2
side_project_b_pct: 107
side_project_c_h: 0
side_project_c_pct: 0
exercise_ses: 3
exercise_pct: 100
reading_h: 0.9
reading_pct: 45
blocks_created: 8
conflicts: 2
```

### Get actuals

**If a review entry exists for the current period:** parse the `_h`, `_ses`, `_pct` fields directly.

**If no entry exists and `gcal_available = true`:** Read actuals from Google Calendar.

1. Compute period start/end: from the last review entry date + `review_cadence` days (or from the start of the current week if no prior entry).
2. Call `mcp__claude_ai_Google_Calendar__list_events` for each calendar in runbook §1. Use ISO 8601 `timeMin`/`timeMax` with the `timezone` from `§ Config`.
3. Map event titles to activity keys using §2 activity names and emojis (exact title → emoji prefix → fuzzy text). P0 events: skip. All-day events: skip. Events < 10 min: skip.
4. Derive hours: `sum((end - start) in hours)` per activity key. For session-tracked activities, count qualifying events as sessions (e.g. Runna calendar events → running sessions).
5. Show a pre-scorecard confirmation before computing:
   ```
   From your calendar ([start] – [end]):
     💼 Main Activity:   8.5h   (Mon 2h, Tue 2h, Wed 2h, Thu 2.5h)
     🎓 Learning:        5.0h
     🏃 Running:         3 sessions  (from [App] calendar)
     ⚠️  Unmatched (2): "Lunch with Ana" · "Call Luis"

   Does this look right? (yes / edit / skip to manual entry)
   ```
6. If "edit": allow the user to correct specific values per activity. If "skip to manual entry": fall through to manual entry below.
7. On confirmation: feed actuals into the scoring pipeline. Add `actuals_source: gcal` to the log entry.

**Edge cases:**
- Partial coverage (e.g. calendar only has 3 of 7 days): warn — "I could only find events [range]. Want me to fill in the rest manually?"
- Multi-activity event titles: treat as unmatched, surface for user decision.
- `gcal_available = true` but `runbook_available = false`: prompt once for calendar ID + timezone before fetching.

**If no entry exists and `gcal_available = false`:** Tell the user: "I don't see a log entry for this period yet. Could you walk me through your actuals?" Ask per activity (or as a list), then derive `_pct` from the goals in `objectives.md`.

**Fallback — trends.md:** If `log.md` has no relevant entries but `wiki/trends.md` has a
weekly actuals table covering the current or most recent period, use that data and note the source.

### Get priority

Read priority from `runbook.md` §2 Schedule Rules (the `Prio` column: P0, P1, P2).
If `runbook.md` is absent, infer priority from ordering in `objectives.md` §1 — activities
listed first are assumed higher priority — or ask the user once during onboarding.

P0 activities (meals, routines) are never in the scorecard. Only P1 and P2 appear.

### Completion-tracked goals

Some goals track progress toward a finish line rather than recurring hours. Detect these by
checking the `Tracking` column in `objectives.md` §1 (see references/objectives-template.md).

Tracking column values:
- `hours` (or absent) — standard recurring-hours goal; no special handling
- `sessions` — standard session-count goal; no special handling
- `completion:Xunits` — e.g. `completion:200pages`, `completion:12modules`, `completion:100%`

**During weekly review, for any completion-tracked goal**, ask before computing:
> "Where are you in [Activity]? (e.g. page X of 200, or module X of 12)"

Parse the answer:
```
completion_pct = current_position / total × 100
```

Show in the scorecard: `X/Y units` in the Actual column, completion % in the % column.
The progress bar represents completion percentage, not hours this week.

Store in the log entry as optional additional fields:
```
activity_completion: X/Y          ← e.g. reading_completion: 80/200
activity_completion_pct: NN       ← e.g. reading_completion_pct: 40
```

**When the user provides a progress update mid-session** (e.g. "I'm on page 80 of 200"):
immediately render a completion bar inline before asking any follow-up:
```
📚 Reading  ████████░░░░░░░░░░░░  80/200 pages  40% complete
```
Bar formula: `filled = round(completion_pct / 100 * 20)`, same as the weekly scorecard.

### Proactive questions during review

While gathering actuals, apply these checks per activity:

**Zero-hours check (P1 only):** If a P1 activity has 0 logged hours and the user hasn't
explicitly said "I did nothing on X":
> "You have 0 logged for [Activity] this week — did you do any, or was it truly 0?"
Ask before finalizing the scorecard, not after.

**Session-based activity prompt:** If an activity uses `_ses` tracking and the user provided
hours instead of sessions, clarify:
> "For [Activity], how many sessions did you do? (you logged X hours — want to convert, or track sessions separately?)"

**Post-scorecard coaching question:** After displaying the scorecard, for the single most-at-risk
🔴 activity (highest priority, biggest gap ≥ 30% of goal), ask one coaching question:
> "What got in the way of [Activity] this week?"
Use the answer conversationally only — do not log it unless the user asks.
**Limit: one coaching question per session.** Do not ask for every red activity.

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

### Output — Review Scorecard

```
──────────────────────────────────────────────────────────────────
Review · Mon DD – Sun DD, YYYY
──────────────────────────────────────────────────────────────────
P   Type      Activity            Progress              Actual    %      Flag
─── ──────── ─────────────────── ──────────────────── ───────── ─────  ────
P1  must-do  💼 Work Project     ████████████████░░░░  9.5/10h    95%  🟡
P1  project  🎓 Online Course    ████████░░░░░░░░░░░░  4.0/ 7h    57%  🔴  ← 3.0h short
──────────────────────────────────────────────────────────────────
P2  project  🏦 Side Project B   ████████████████████  3.2/ 3h   107%  ✅
P2  habit    🏃 Exercise         ████████████████████  3 / 3ses  100%  ✅
P2  project  📌 Side Project C   ████████████████░░░░  1.5/ 2h    75%  🟡
P2  project  🌐 Side Project A   ████████░░░░░░░░░░░░  2.0/ 4h    50%  🔴  ← 2.0h short
P2  habit    📚 Reading          ████████░░░░░░░░░░░░  1.0/ 2h    50%  🔴  ← 1.0h short
P2  habit    🤖 AI Learning      ░░░░░░░░░░░░░░░░░░░░  0 / 1h      0%  🔴  ← 1.0h short
──────────────────────────────────────────────────────────────────
```

Use a separator line (`──────`) between the P1 and P2 groups for visual clarity.

**Type-specific notes after the scorecard:**
- For each 🔴 `must-do`: "⚠️ [Activity] was missed — this is a non-negotiable. What happened?"
- For each 🔴/🟡 `habit`: note the streak status ("3-week streak broken" or "2nd miss in a row")
- For each `project`: show estimated finish at current pace vs. target date (if available)
  e.g. "🎓 Online Course: at this pace, done ~Jun 14. Target: May 29. ⚠️ 16 days behind."

Then:
- **Catch-up** (activities < 80%, excluding must-dos which are always flagged separately): recommended recovery hours
- **Outlook**: 2–3 sentences — what's strong, what's at risk, one concrete suggestion

### Log the entry

After showing the scorecard, ask:
> "Want me to log this review entry to `log.md` and update streak counts in `trends.md`? (yes / no)"

If yes, append to `log.md` using the key-value format above.

And update the streak counts table in `wiki/trends.md`:
- Increment "consecutive weeks met" for each ✅/🟢 activity
- Increment "consecutive weeks missed" for each 🟡/🔴 activity (reset the other column)
- Update "Last updated" column

### Time series trend chart (optional)

After the logging offer, also ask:
> "Want to see a trend chart for any activity? (name or 'skip')"

**Data source:** `wiki/trends.md` — `§ Weekly Actuals History` table. Read up to the last 8
weeks of data for the requested activity.

**Render format:**
```
🎓 Online Course — last 6 weeks
Mar W3  ████████████░░░░░░░░  62%
Mar W4  ████████████████░░░░  80%
Apr W1  ████░░░░░░░░░░░░░░░░  20%
Apr W2  ████████████████████ 100%
Apr W3  ────── current week ──────
```
- Row label: abbreviated month + week number (e.g. `Apr W2`)
- Bar: 20 chars, `filled = round(pct / 100 * 20)`, same formula as scorecard
- If current week has no data yet: show `────── current week ──────` as last row
- **Guard:** if fewer than 2 weeks of data, say: "Not enough trend data yet (need at least 2 weeks)."
- Maximum 8 weeks of history shown

After rendering, offer: "Want to see another activity's trend, or continue? (activity name / done)"

### Next period offer

After the trend chart (or if the user skips it), offer:
> "Want to plan next week while we're here? (yes / skip)"
If yes, proceed directly to **Next Week Planning** mode using the same vault context.

---

## Mode: Next Week Planning

**Goal:** Build a prioritized, data-driven allocation plan for the upcoming week, accounting for
monthly trajectory and any known constraints.

### Read
- `raw/objectives.md` §1 — weekly targets (activities + goals + priorities)
- `raw/objectives.md` §2 — monthly targets
- `log.md` — most recent `## YYYY-MM-DD · weekly` entry (catch-up context)
- `log.md` — all weekly entries dated within the current calendar month (monthly actuals to date)

### Compute monthly trajectory

For each activity:
```
weeks_in_month         = 4 (or derive from calendar)
weeks_elapsed          = number of weekly log entries found this month
weeks_remaining        = weeks_in_month − weeks_elapsed  (minimum 1)
monthly_actual_to_date = sum of _h / _ses across this month's entries
monthly_deficit        = monthly_target − monthly_actual_to_date
catch_up_per_week      = monthly_deficit / weeks_remaining
normal_weekly_goal     = §1 weekly target

catch_up_flag:
  catch_up_per_week > normal_weekly_goal × 1.3  → 🔴  significant catch-up needed
  catch_up_per_week > normal_weekly_goal × 1.05 → 🟡  slight catch-up needed
  catch_up_per_week ≤ normal_weekly_goal         → 🟢  on track or ahead
```

### Ask about constraints (once)

Before generating the plan, ask:
> "Any constraints for next week? (e.g. travel, reduced availability, events — or Enter to skip)"

If the user provides constraints, factor them in:
- If total available hours are reduced, scale down proportionally, prioritizing P1 activities
- Note acknowledged constraints in the output footer

### Output — Next Week Plan

```
──────────────────────────────────────────────────────
Next Week Plan · Mon DD – Sun DD, YYYY
Monthly trajectory: N weeks elapsed · N weeks remaining
──────────────────────────────────────────────────────
P   Activity            Suggested             Reason
─── ─────────────────── ──────────────────── ──────────────────────────────
P1  💼 Work Project     ██████████░░░░░░░░░░  11h   🔴 catch-up (2.5h behind)
P1  🎓 Online Course    ████████████████░░░░   7h   🟢 on track
──────────────────────────────────────────────────────
P2  🏃 Exercise         ████████████████████  3ses  🟢 on track
P2  📚 Reading          █████████████░░░░░░░   2h   🟡 slight catch-up
P2  🌐 Side Project A   ████████░░░░░░░░░░░░   4h   🔴 catch-up (3h behind)
──────────────────────────────────────────────────────
Total suggested: ~XX hours
[Constraint note if applicable: "Note: Reduced week — Friday travel assumed off."]
──────────────────────────────────────────────────────
```

Bar scale: 20 chars where a full bar = the suggested allocation for that activity.

Then:
- **Priority callout:** "Focus on [top at-risk P1 activity] first — it's the biggest gap."
- **One concrete scheduling tip** based on the highest catch-up activity.

**No file write in this mode — advisory only.** Do not offer to log this plan.

### § Schedule Windows (runs if `runbook_available = true`)

After the Next Week Plan output table, show a schedule suggestions table using §2 data:

```
──────────────────────────────────────────────────────────────────────
Schedule Suggestions · Mon DD – Sun DD, YYYY
──────────────────────────────────────────────────────────────────────
Activity           Suggested   Window             Days
─────────────────  ─────────   ────────────────── ──────────────────
💼 Main Activity   11h         10:00–13:00        Mon–Fri  (2h/day)
🎓 Learning         7h         17:00–20:00        Mon,Wed,Thu,Fri
🌐 Side Project A   4h         13:30–15:00        Mon/Wed/Fri
🏃 Session Act.     3 ses      [App]-owned        —
📚 Evening Act.     2h         21:15–22:15        Any 4 days
──────────────────────────────────────────────────────────────────────
```

- `Window` and `Duration` data from runbook.md §2.
- Activities with `flex/weekend` or `honor system`: show "flexible" for Window.
- Session-only / `DO NOT create blocks` activities: show window source (e.g. "[App]-owned") and `—` for days.
- Window-sharing rules (e.g. competing P2 projects): reproduce the note from §2 below the table.

### § Create Calendar Blocks (runs if `gcal_available = true`)

After the schedule suggestions, offer:
> "Want me to create these blocks on your Google Calendar? I'll use your write calendar and stay within your §2 windows. (yes / customize / skip)"

**"yes" flow:**
1. Call `mcp__claude_ai_Google_Calendar__list_events` on the write calendar for next week's date range.
2. For each activity in the plan, skip days that already have a block for that category (same emoji/title prefix).
3. For missing days: compute slot start from §2 window. Check §3 buffer rules against fetched events. If conflict: shift to next available 30-min slot within the window. If no slot available: flag AT_RISK, do not create.
4. Call `mcp__claude_ai_Google_Calendar__create_event` for each needed block:
   - `calendarId`: Read+Write calendar ID from runbook §1
   - `summary`: activity emoji + name (matching §2 exactly)
   - `start` / `end`: computed ISO 8601 with timezone from §1
   - `colorId`: from §2 Notes column if specified
5. Never create blocks for activities marked `DO NOT create blocks` or `honor system`.
6. Report: "Created N blocks · Skipped N (already had blocks) · Flagged N AT_RISK."

**"customize" flow:** Present each proposed block individually — "Create [Activity] [Day] [Time]? (yes / change time / skip)". Batch-create confirmed blocks.

**`gcal_available = false`:** Both sub-sections omitted entirely. Output unchanged.

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
──────────────────────────────────────────────────────────────────────────────
Monthly Pacing · May 2026 · 13 days left
──────────────────────────────────────────────────────────────────────────────
Type      Activity           Actual / Target    Pace needed    (normal)    Flag
──────── ─────────────────── ────────────────── ────────────── ──────────  ────
must-do  💼 Work Project     20.0 / 40h         1.54h/day      (1.43h/day) 🟡
project  🎓 Online Course    13.0 / 28h         0.83h/day      (1.00h/day) 🟢
project  🌐 Side Project A    6.0 / 16h         0.56h/day      (0.57h/day) 🟢
project  📌 Side Project C    2.0 /  8h         0.33h/day      (0.29h/day) 🟡
habit    🏃 Exercise           7  / 12ses        0.28ses/day    (0.43/day)  🔴
habit    📚 Reading            4.2/  8h          0.21h/day      (0.29h/day) 🟢
──────────────────────────────────────────────────────────────────────────────
```

If data for the current month is sparse, note it: "Only found N week(s) of log data for
[Month]. Actuals may be understated."

### Monthly grid (optional)

After presenting the pacing table, offer:
> "Want to see the last 4 weeks stacked by activity? (yes / skip)"

If yes, render a compact grid — last 4 weekly entries from log.md, one column per week,
one row per activity:

```
──────────────────────────────────────────────────────
4-Week Activity Grid · April 2026
──────────────────────────────────────────────────────
Activity           [Apr W1] [Apr W2] [Apr W3] [Apr W4]
─────────────────  ──────── ──────── ──────── ────────
💼 Work Project       95%      78%     102%      57%
🎓 Online Course      69%      80%      44%     100%
🏃 Exercise          100%     100%      67%      33%
📚 Reading            45%     100%       0%      90%
──────────────────────────────────────────────────────
```

Values are `_pct` from log.md entries. Use `—` if no entry exists for that week.

---

## Mode: Proposal Review

**Goal:** Surface pending calibration proposals, let the user approve or reject each one,
and apply approved changes to `objectives.md` and `trends.md`.

### Read
`wiki/trends.md` — find the `## § ⚠️ Pending Calibration Proposals` section (or any heading
containing "Pending" and "Proposals").

If the section is empty or doesn't exist: "No pending proposals found in `trends.md`."

**Type guardrail:** Before presenting any proposal, check the `Type` of the activity in
`objectives.md` §1. If `Type` is `must-do`, skip the proposal entirely and note:
> "⚠️ Skipped proposal for [Activity] — must-dos are never calibrated down. Address the miss directly instead."

### Present proposals

Show each proposal clearly:

```
⚠️ Pending Calibration Proposals (2 found)

──── Proposal 1 ────
🏃 Exercise — TARGET_HIGH (streak: 3 weeks missed)
  Current:  ≥4 sessions/week · ≥16 sessions/month
  Proposed: ≥3 sessions/week · ≥12 sessions/month
  Reason:   Schedule consistently delivers 3 sessions. The 4th is structurally unavailable.

──── Proposal 2 ────
📚 Reading — TARGET_HIGH (streak: 2 weeks missed)
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
Proposed change — Online Course weekly goal: ≥7h → ≥5h

1. raw/objectives.md §1:
   Before: | 🎓 Online Course | ≥7h  | …
   After:  | 🎓 Online Course | ≥5h  | …

2. raw/objectives.md §2 (monthly, if cascading):
   Before: | 🎓 Online Course | ≥28h | 7h/week × 4 |
   After:  | 🎓 Online Course | ≥20h | 5h/week × 4 |

3. runbook.md §2 (if present):
   Before: P1 | 🎓 Online Course | ≥7h | …
   After:  P1 | 🎓 Online Course | ≥5h | …

4. CLAUDE.md Weekly Goals (if present):
   Before: | 🎓 Online Course | ≥7h | … |
   After:  | 🎓 Online Course | ≥5h | … |

Apply all of the above? (yes / no)
```

If any of files 2–4 are not found, skip them silently — don't error.

### On confirmation

1. Apply all diffs (edit each file in turn)
2. If the change affects a completion timeline, flag the impact:
   "At ≥5h/week, estimated completion date shifts. Check §3 Quarterly Goals for the current
   target date."
   Ask: "Do you also want to update the completion date in §3 Quarterly Goals / §4 Milestones?"
3. Append to `wiki/trends.md` § Calibration History:
   ```
   | [DATE] | [Activity] [old] → [new] | User requested via time-coach |
   ```
4. Report: `✅ Updated across [N] files.`

---

## Mode: Quick Status

**Goal:** Give a 3-line orientation without running a full review.

**Read:** `log.md` (last review entry date and top actuals), latest `reports/YYYY-MM-DD_daily.md` if present.

**Output:**
```
Last review: [YYYY-MM-DD] · [N] days ago
This period's pace: [top 3 activities with %]
Next sync: [last sync date + sync_cadence, or "not configured" if gcal_available = false]
```

No file writes. Offer: "Want a full review, or run a calendar sync? (review / sync / done)"

---

## Mode: Calendar Sync

**Goal:** Run the daily calendar maintenance pass — deduplicate, resolve conflicts, prune met goals, create recovery blocks.

**Requires:** `gcal_available = true` AND `runbook_available = true`. If either is false: "Calendar sync requires Google Calendar and a configured runbook.md. See `references/runbook-template.md` to set one up."

**Cadence gate:** Read the most recent `## YYYY-MM-DD · sync` or `## YYYY-MM-DD · daily` entry in `log.md`.
If `today - last_sync_date < sync_cadence` days: "Last sync was [N] day(s) ago (cadence: [sync_cadence]). Running early — proceed anyway? (yes / no)"

**FETCH** (3 parallel calls):
- Write calendar · today through Sunday (or today + write_horizon if that's larger)
- Personal calendar · same range
- All Read-only calendars in runbook §1 · same range

**ANALYZE** (single pass, no API calls):

```
past   = blocks where end < now  →  tally actual hours/sessions per category
future = blocks where start > now

Categories: read from runbook.md §2 Prio column (P1 + P2 only). Skip P0 and sleeping projects.

STEP 1 [DUPLICATE]  ≥2 Claude blocks same category same future day
  → merge: sum durations · place in preferred window · respect §3
  → run first — merged result feeds steps 2–4

STEP 2 [CONFLICT]  Claude block overlaps any block or violates §3 buffer rules
  → P0/Personal/Read-only calendar blocks: untouchable
  → move lower-priority Claude block to next available slot in window
  → if no slot: trim to 30 min minimum or flag AT_RISK
  → single pass; re-check after each move

STEP 3 [MET_PRUNE]  actual ≥ goal
  → delete ALL future Claude blocks for that category
  → if actual + remaining future > goal × 1.10 → trim to goal × 1.0

STEP 4 [AT_RISK]  actual + future < goal  (P1 first, then P2)
  → create recovery block in preferred window · respect §3
  → if window full, use nearest available slot within hard window from §3
```

**WRITE:** Execute all flagged actions in parallel via `mcp__claude_ai_Google_Calendar__create_event`, `update_event`, `delete_event`.

**HORIZON CHECK** (compute only, no API calls):
For each P1/P2 activity with a monthly target in `objectives.md §2`:
```
remaining_needed   = monthly_target − cumulative_actual_this_month
remaining_days     = calendar days left in month (including today)
needed_daily_pace  = remaining_needed / remaining_days
normal_daily_pace  = weekly_goal / 7

flag:  ≤0 → ✅   >normal×1.2 → 🔴   >normal → 🟡   else → 🟢
```

**Log:** Append `## YYYY-MM-DD · sync | Changes: N · Conflicts: N · AT_RISK: N · [brief note if unusual]`

**Report:** Bar chart of actuals + one line per change made + 2-sentence outlook + Monthly Horizon section.
Offer to write to `reports/YYYY-MM-DD_daily.md`.

---

## Mode: Calendar Write

**Goal:** Create a block skeleton covering the next `write_horizon` days, log the weekly report, and update trends.

**Requires:** `gcal_available = true` AND `runbook_available = true`. If either is false: see Calendar Sync error message.

**Cadence gate:** Read the most recent `## YYYY-MM-DD · write` entry in `log.md`.
If `today - last_write_date < write_cadence` days: warn and ask to confirm before proceeding.

**FETCH:** Write calendar · today through today + `write_horizon` days.

**CREATE SKELETON** (gaps only, P0 → P1 → P2):
- A Claude block already exists for that category on that day → skip
- Missing → create one block in preferred §2 window, respecting §3 buffer rules
- P0 ordering: if both Breakfast and Home Tasks are being created on the same day, place Home Tasks immediately after Breakfast
- Distribute remaining hours evenly across days missing a block; round to 30 min; minimum 30 min per block
- Window-sharing rules from §2 note block (e.g. alternate days between competing P2 projects)
- `DO NOT create blocks` activities (e.g. session activities managed by a fitness app): skip
- `honor system` activities: skip

**WEEKLY REPORT:**
1. Bar chart: actual vs weekly goal per activity (20 chars · % · flag) — P1 first, P2 second. Omit P0 and sleeping projects.
2. Monthly progress: cumulative actual vs monthly target (% + days remaining).
3. Trend proposals: for each activity with a missed-goal streak ≥2 consecutive weeks, diagnose and propose a config change (same logic as the existing Proposal Review mode — do not apply; write proposal text only to the report).
4. Catch-up: activities < 80% → recommended recovery hours for the coming week.
5. Outlook: 3 sentences — what's on track, what needs attention, one concrete suggestion.

**UPDATE LOG + TRENDS:**
- Append to `log.md`: `## YYYY-MM-DD · write | Blocks created: N · Skipped: N`
- Update streak counts table in `wiki/trends.md` (same logic as Review mode log step).

Offer to write the full report to `reports/YYYY-MM-DD_weekly.md`.

---

## Mode: Onboarding

**Goal:** Scaffold the vault from scratch for a new user.

Triggered when `raw/objectives.md` doesn't exist at the expected path.

### Collect info

Ask:
1. "What's your name?" (for the objectives.md header)
2. "What activities do you want to track? Give me a list — e.g. 'Work Project, Reading, Side Project, Exercise'."
3. For each activity, ask two questions in sequence:

   a. **Type:** "What type is [Activity]?
      - **must-do** — compulsory, non-negotiable (breakfast, homework, work hours)
      - **habit** — recurring, non-compulsory but good to have; includes learning (exercise, reading, online course)
      - **project** — self-imposed, has a finish line and requires metrics (product launch, book, certification)"

   b. **Goal:** Based on type:
      - must-do / habit: "Weekly goal for [Activity]? (e.g. '8h' or '3 sessions')"
      - project: "What's the total scope? (e.g. '200 pages', '12 modules')" + "Weekly hours goal?" + "Target completion date?"

4. "Monthly targets — should I derive them as 4× the weekly goal, or do you want to set them manually?"

### Step 4b — GCal configuration (runs if `gcal_available = true`)

After collecting activities and goals, offer:
> "I can see Google Calendar is connected. Want me to set up a scheduling runbook? This lets me read your actuals from the calendar and create/sync blocks automatically. (yes / skip)"

**If yes:**
1. Show the cached `gcal_calendars` list → "Which calendar should I write scheduling blocks to? (enter number)"
2. For each activity: "What time window works best for [Activity]? (e.g. '10:00–13:00 weekdays', 'flex/weekend', 'honor system', or press Enter to skip)"
3. Ask: "What's your timezone? (e.g. America/Mexico_City)"
4. Ask: "Any buffer rules? (e.g. 'always 15 min before lunch', or Enter to use defaults)"
5. Scaffold `runbook.md` from `references/runbook-template.md`, filling in §1 (calendars + timezone), §2 (one row per activity with entered windows), §3 (buffer rules or defaults), §4 (`[VAULT]` placeholder).
6. Add `runbook.md` to the files created list in the Finish output.

**If skip:** Continue to file creation with no runbook.md. Skill operates in no-calendar mode.

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
  runbook.md         ← Google Calendar schedule rules  [only if Step 4b completed]

Run /time-coach again and say "review" to start tracking.
[If runbook.md was created: "During review, I'll read your actuals directly from Google Calendar."]
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
- **Skipped activities are OK.** If the user hasn't tracked an activity (honor system), note it
  separately — don't force it into the scorecard.
- **One coaching question per session.** Ask the single most important clarifying or coaching
  question — don't stack multiple prompts on the user.

---

## For GitHub / Cowork marketplace publishing

This skill has **no required external MCP dependencies**. Google Calendar integration is optional and auto-detected at session start. Without it, the skill reads and writes plain `.md` files only.

The vault structure is intentionally flexible:
- Activity names and emojis are read from `objectives.md` — not hardcoded
- Log format is structured key-value — LLM-parseable and human-readable
- Review cadence, sync cadence, and calendar write horizon are all user-configurable via `objectives.md § Config`

**Coworks scheduled triggers:** Point a daily trigger and a weekly trigger at this skill. The skill's internal cadence gates (`sync_cadence`, `write_cadence` in `§ Config`) control whether each run actually executes — Coworks frequency does not need to change when you adjust cadences.

**Deprecates:** `agenda-manager` and `agenda-companion` skills. If migrating, re-point existing Coworks scheduled triggers from those skills to `time-coach` with context hints "run calendar sync" (daily) and "run calendar write" (weekly/Sunday).

To publish: copy this directory to your GitHub repo. Users install via Cowork marketplace or by placing the folder in their skills directory.

Reference templates for new-user onboarding live in `references/`:
- `objectives-template.md` — goals config including the `§ Config` cadence block
- `runbook-template.md` — Google Calendar schedule rules (fill in for calendar integration)
- `log-template.md`, `trends-template.md` — activity log and streak tracking starters
