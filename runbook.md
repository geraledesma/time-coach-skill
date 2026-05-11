---
updated: 2026-05-01
---

> **Purpose:** Algorithms and execution rules for time-coach. Covers MODE A (weekly write) and MODE B (daily sync). · **Read first:** runbook.md · **Reference:** 01-config/config.md (your user settings)

# Time-Coach Runbook

---

## § Execution Model

**Two Modes, One Cycle:**

| Mode | When | What | Output |
|------|------|------|--------|
| **MODE A** | Sundays | Plan next week: create skeleton blocks | Calendar blocks + weekly report |
| **MODE B** | Mon–Sat | Daily sync: resolve conflicts, flag risks | Updated calendar + daily log entry |

---

## § MODE A: Weekly Write (Sundays)

**Goal:** Create a skeleton week of conflict-free calendar blocks distributed across your priorities.

**Cycle Duration:** ~30–45 minutes (fetch calendars, create blocks, write report)

---

### STEP 0: Pre-Flight (Confirm Scope)

Before creating any calendar blocks, confirm:

1. **Today's date?** (e.g., "Sunday, May 4, 2026")
2. **Week definition:** Does your week run Mon–Sun? (most users yes)
3. **Target date range:** Which week are you planning? (e.g., "May 5–11")
4. **Any known conflicts this week?** (e.g., "Workshop May 7, vacation May 9–10")

**Why:** The April 27 bug: wrong week dates caused mass creation of blocks on wrong days.

---

### STEP 1: FETCH (Read All Three Calendars)

Fetch in parallel:
- **Personal calendar** (read-only): See immovable personal events, meetings, social blocks
- **Exercise calendar** (read-only, e.g., Runna): See scheduled exercise sessions — you will NOT create exercise blocks
- **Claude calendar** (read-write): See existing Claude-scheduled blocks from previous weeks

**Range:** Target week date range (e.g., Mon May 5 00:00 → Sun May 11 23:59 in your timezone)

**Output:** 3 calendar snapshots for the target week

---

### STEP 2: Identify Gaps (Only Create Where Missing)

For each day Mon–Sun:
- Look for existing Claude blocks for each activity from `01-config/config.md`
- If a block exists for that activity on that day: **skip** (don't duplicate)
- If no block exists: **mark as a gap** and schedule for creation

---

### STEP 3: Check for Immovable Conflicts

Before proceeding to skeleton creation, scan for **immovable vs. immovable conflicts:**

```
Immovable = P0 meal blocks (breakfast, lunch, dinner) or Personal events
If P0 meal block overlaps a Personal event:
  → CONFLICT TYPE: IMMOVABLE_VS_IMMOVABLE
  → ACTION: STOP and FLAG for user
  → Ask: "Desayuno (10:00–10:30) conflicts with Workshop (10:00–11:30). Both are locked. How should I handle this?"
  → Do NOT proceed until user clarifies
```

**Why:** The Apr 28 bug: immovable conflicts were created silently and never resolved.

---

### STEP 4: CREATE SKELETON (Distribute Hours Into Gaps)

For each gap identified in STEP 2:

1. **Get goal hours from `01-config/objectives.md`** (weekly target for that activity)
2. **Calculate catch-up from last week:**
   ```
   last_week_actual = hours logged in log.md for that activity
   catch_up = max(0, weekly_goal − last_week_actual)
   allocation = weekly_goal + catch_up
   ```
3. **Distribute allocation across days with gaps:**
   - Skip days with existing blocks
   - Distribute remaining allocation evenly across gap days
   - Round to 30-min chunks (minimum)
4. **Respect windows from `01-config/config.md`:**
   - Use the preferred window for that activity
   - Respect buffer rules (15 min before/after transitions, 45 min post-exercise, etc.)
   - Hard window: no blocks before 08:00 or after 22:30

**Example:**
```
Job Search: goal 10h, last week 7.9h → catch-up 2.1h → allocation 12.1h
Gaps: Mon, Tue, Wed, Fri (Thu has existing block)
Distribute 12.1h across 4 days ≈ 3h each
Mon 10:00-13:00, Tue 10:00-13:00, Wed 10:00-13:00, Fri 10:00-13:00
→ Check buffers, move if needed
```

**Activity Sequencing (When Multiple Share a Window):**

If multiple activities share a preferred window (e.g., 09:00–13:00 for P0 + P1):
1. Schedule P0 blocks in order: Morning Routine → Breakfast → Home Tasks
2. Calculate END time of last P0 block
3. Schedule P1 blocks STARTING at P0 end time (back-to-back, no gap)
4. Schedule P2 blocks in remaining gaps

**Example:**
```
09:00-10:00: Morning Routine (P0)
10:00-10:30: Breakfast (P0)
10:30-11:15: Home Tasks (P0)
→ P0 end = 11:15
11:15-13:15: Job Search (P1) ← starts at 11:15, NOT at 10:00
```

---

### STEP 5: Resolve Remaining Conflicts

For each proposed block:

1. **Check for overlap with Personal calendar** → Personal is untouchable, move Claude block to next available slot in window
2. **Check for buffer violations:**
   - 15 min before/after exercise session (if near Runna block)
   - 15 min before/after any meal block
   - 45 min post-exercise recovery
   - Hard window 08:00–22:30
3. **If no clean slot in preferred window:** Use first available 08:00–22:30 slot and note in report

---

### STEP 6: CREATE Blocks on Claude Calendar

Write all proposed blocks to Claude calendar in parallel.

---

### STEP 7: WEEKLY REPORT (Write to `reports/weekly/YYYY-MM-DD_weekly.md`)

Create a markdown file with:

1. **Bar chart (20 chars × %): Planned vs. Goal for each activity**
   ```
   💼 Job Search        [████████████░░] 12.1h / 10h (121%) ✅
   🎓 EDHEC Coursera    [██████░░░░░░░░] 7.5h / 8h (94%) 🟡
   📊 CFA Level II      [████████░░░░░░] 6h / 6h (100%) ✅
   ```
   Include: Job Search · EDHEC · CFA · Meditation · PROJ1 · PROJ2 · Running · Reading

2. **Monthly horizon (if applicable):**
   ```
   ## 📅 Monthly Progress
   💼 Job Search:     18h / 24h goal · 10d left · needs 0.6h/day (normal: 1.5h/day) ✅
   🎓 EDHEC:         24h / 32h goal · 10d left · needs 0.8h/day (normal: 2h/day) 🟡
   ```

3. **Trend proposals (if any activity missed goal ≥2 consecutive weeks):**
   ```
   ### 📚 Lectura — TARGET_HIGH (streak: 3 weeks)
   - Weeks: Apr 21–27 (67%), Apr 28–May 4 (58%), May 5–11 (planned 70%)
   - Pattern: Evening slot (21:15–22:15) consistently displaced by late dinners
   - Proposed change: Move window from 21:15–22:15 to 20:45–21:45
     File: 01-config/config.md § Activity Codes & Mappings
     Field: Lectura window  From: 21:15–22:15  To: 20:45–21:45
   ```

4. **Gym honor-system note:**
   ```
   Gym this week: [to be confirmed at end of week]
   ```

5. **Catch-up summary:**
   ```
   ## 💪 Catch-Up Hours (Included Above)
   Activities <80% last week needing recovery:
   - 🎓 EDHEC: 2h catch-up
   - ₿ Bitcoin: 0.5h catch-up
   ```

6. **Outlook (2–3 sentences):**
   ```
   Strong start on Job Search and CFA momentum. EDHEC sprint on track but tight.
   Lectura continues to slip — consider earlier window or shorter sessions (10min minimum).
   All conflicts resolved; calendar ready for the week.
   ```

---

### STEP 8: UPDATE LOG & TRENDS

**Append to `log.md`:**
```
## [2026-05-05] weekly | JS: 121% · EDH: 94% · CFA: 100% · MED: 4 ses · PROJ1: 100% · PROJ2: 75% · RUN: 3 ses · blocks: 18 created · conflicts: 1 escalated
```

**Update `trends.md`:**
- Update streak counts for each activity (✅ or 🔴)
- Add new row to historical table if proposing a config change
- Note any patterns or observations

---

---

## § MODE B: Daily Sync (Mon–Sat)

**Goal:** Daily 5-minute sync to resolve emerging conflicts, flag at-risk activities, and catch shortfalls before they cascade.

**Frequency:** Every weekday evening or early morning (before calendar deadlines)

---

### STEP 0: FETCH (Read Calendars for Today + Tomorrow)

Fetch in parallel:
- **Personal calendar** (today + tomorrow)
- **Exercise calendar** (today + tomorrow)
- **Claude calendar** (today + tomorrow)

**Scope:** Now through 23:59 tomorrow (roughly 36–48 hour window)

---

### STEP 1: ANALYZE (Single Pass, No API Calls)

Extract two time windows:

```
past   = all blocks where end_time < now
future = all blocks where start_time > now

For each activity code from 01-config/config.md:
  tally_actuals(past) = hours or sessions from completed blocks
  list_future(future) = hours or sessions scheduled but not yet done
```

---

### STEP 2: DUPLICATE (Merge Overlapping Blocks)

If 2+ Claude blocks for the same activity on the same future day:
- Merge: sum durations, place single block in preferred window (from config)
- Respect buffers (§ MODE A STEP 5)
- Re-check for conflicts after merge

---

### STEP 3: CONFLICT (Detect & Resolve)

```
for each Claude block:
  if overlaps(claude_block, personal_block):
    if personal_block is immovable (P0 meal or marked untouchable):
      → PERSONAL IS UNTOUCHABLE
      → Try to move Claude block to next available window slot
      → If no slot exists: trim to 30-min min, flag AT_RISK
  
  if overlaps(claude_block, runna_block):
    if runna_block is close (< 45 min post or < 15 min pre):
      → RUNNA HAS BUFFERS
      → Move Claude block to respect 45-min post-Runna recovery, 15-min pre-Runna
      → If no slot exists: trim, flag AT_RISK
  
  if overlaps(claude_block, p0_meal):
    → IMPOSSIBLE CASE (P0 meals are created by user, not moved by Claude)
    → If this happens, escalate to user
```

**Conflict Resolution Hierarchy:**
1. Claude blocks are movable (find another time)
2. P0 meals are immovable (never move)
3. Personal events are untouchable (never modify)
4. Runna sessions are untouchable but have buffers (respect them)

---

### STEP 4: MET_PRUNE (If Goal Already Hit)

```
for each activity:
  if tally_actuals(past) >= goal:
    → Delete ALL future Claude blocks for that activity
    → Rationale: No need to schedule more; goal is met
```

---

### STEP 5: AT_RISK (If Goal At Risk)

```
for each activity with remaining_needed = goal - tally_actuals(past):
  if remaining_needed > 0:
    → Create recovery block in preferred window (from config)
    → Respect buffers (§ MODE A STEP 5)
    → If preferred window is full, use first available 08:00–22:30 slot
    → Duration = remaining_needed / days_left_in_month (minimum 30 min)
    → Log as "recovery block"
```

---

### STEP 6: WRITE (Execute All Changes)

Write all moves, deletions, and new blocks to Claude calendar in parallel.

---

### STEP 7: HORIZON CHECK (No API Calls — Compute Only)

For each activity with a monthly target (from `01-config/objectives.md`):

```
remaining_needed   = monthly_target − cumulative_actual_so_far
remaining_days     = calendar days left in month (including today)
needed_daily_pace  = remaining_needed / remaining_days
normal_daily_pace  = weekly_goal / 7

Flag:
  remaining_needed ≤ 0           → ✅ already met
  needed_daily_pace > normal×1.2 → 🔴 unsustainable (pace > 120% normal)
  needed_daily_pace > normal     → 🟡 elevated (pace > 100% normal)
  else                           → 🟢 on track
```

---

### STEP 8: DAILY REPORT (Write to `reports/daily/YYYY-MM-DD_daily.md`)

Create a markdown file with:

1. **Changes made:**
   ```
   ## ✏️ Calendar Changes
   - Moved: Job Search Wed 10:00→14:00 (conflict with Workshop)
   - Created: Lectura recovery 21:15 (30 min, short this week)
   - Deleted: EDHEC Thu (met weekly goal)
   - Conflicts resolved: 2
   - Changes total: 3
   ```

2. **Bar chart (emoji · actual/goal · % · flag):**
   ```
   💼 Job Search    3.5h / 10h (35%) 🔴 at-risk
   🎓 EDHEC         6h / 8h (75%) 🟡 on track
   📊 CFA           4h / 6h (67%) 🟡 on track
   ```

3. **Monthly horizon:**
   ```
   ## 📅 Monthly Horizon (as of today)
   💼 Job Search [JS]: 15.5h / 24h · 9d left · needs 0.94h/day (normal: 1.5h/day) 🟡
   🎓 EDHEC [—]: 22h / 32h · 9d left · needs 1.11h/day (normal: 2h/day) 🟡
   📊 CFA [—]: 18h / 24h · 9d left · needs 0.67h/day (normal: 1.5h/day) 🟡
   🧘 Meditation [—]: 12 ses / 16 · 9d left · needs 0.44/day (normal: 0.57/day) 🟢
   ```

4. **2-sentence outlook:**
   ```
   On pace overall but Job Search tightening. EDHEC needs catch-up by week's end.
   Calendar updated; no immovable conflicts.
   ```

---

### STEP 9: UPDATE LOG

**Append one line to `log.md`:**
```
## [2026-05-06] daily | Changes: 3 · Conflicts: 2 · AT_RISK: 1 · EDHEC +1.5h recovery scheduled
```

---

---

## § Rules & Constraints

### Buffer Rules (From `01-config/config.md` or Defaults)

| Constraint | Value | Reason |
|-----------|-------|--------|
| Before any exercise session | ≥15 min | Transition/warmup |
| After any exercise session | ≥45 min | Recovery + shower + travel |
| Any activity ↔ any meal | ≥15 min | Digestive transition |
| Hard window | 08:00–22:30 | No blocks outside range |
| P0 meal blocks | Never move | Immovable |
| Personal events | Never modify | Untouchable |
| Runna sessions | Never modify but respect buffers | Untouchable but has rules |

### Activity Codes (From `01-config/config.md`)

Each activity has:
- **Code** (e.g., `JOB_SEARCH`, `EDHEC`, `CFA`, `PROJ2-Bancos y Sofipos`)
- **Priority** (P0, P1, or P2)
- **Weekly Goal** (hours or sessions)
- **Preferred Window** (e.g., 10:00–13:00)
- **Duration** (e.g., 1.5h, 30 min)
- **Tracking Method** (hours, sessions, completion, honor system)

---

## § Key Concepts

### Priority Levels

| Level | Definition | Examples | Movability |
|-------|-----------|----------|-----------|
| **P0** | Immovable daily routine | Meals, morning routine, home tasks | Never move |
| **P1** | Must-do weekly goal | Job search, education, projects with deadlines | Movable, lower movability |
| **P2** | Flexible habit/project | Side projects, learning, fitness, reading | Movable, highest priority |

### Weekday vs. Weekend

**Must-do scheduling:** P0 + P1 apply **weekdays only (Mon–Fri)**. Weekends exempt from must-do commitment (meals optional in calendar, jobs on hold, routines flexible).

### Horizon Check

Monthly pacing metric: Are you on track to hit your monthly goal by end of month?
- ✅ = pace is sustainable
- 🟡 = pace elevated but achievable
- 🔴 = unsustainable, need catch-up or goal adjustment

### Catch-Up Integration

If you fell short last week, this week's allocation automatically includes catch-up:
```
allocation = weekly_goal + max(0, weekly_goal − last_week_actual)
```

This ensures you don't drift behind your annual targets while maintaining a steady pace.

---

## § Testing & Verification

**How to Know MODE A Worked:**
- [ ] All 7 days (Mon–Sun) have blocks for P0 activities (meals, routine)
- [ ] No overlaps between Claude blocks and Personal calendar
- [ ] No buffer violations (45 min post-Runna, etc.)
- [ ] Blocks are in preferred windows (or fallback if window full)
- [ ] Weekly report shows allocations (base + catch-up if any)
- [ ] Log entry appended to `log.md`

**How to Know MODE B Worked:**
- [ ] Conflicts detected and resolved without silent collisions
- [ ] AT_RISK blocks created for activities <80% toward goal
- [ ] MET_PRUNE deleted future blocks for completed activities
- [ ] Horizon flags reflect actual remaining pace
- [ ] Daily report shows all changes with reasons
- [ ] Log entry appended to `log.md`

---

## § Troubleshooting

| Problem | Check |
|---------|-------|
| Blocks not created for an activity | STEP 2: Did that activity already have a block that day? If yes, it was skipped (by design). |
| Conflict not resolved | STEP 3: Was it P0-vs-Personal (immovable-vs-immovable)? Check for escalation flag. |
| Same activity scheduled twice same day | STEP 2 (MODE B): DUPLICATE step should have merged them. Verify merge logic. |
| Block moved to weird time | STEP 5: Preferred window was full. Check available slots 08:00–22:30. |
| Weekly report missing | STEP 7: Check file path `reports/weekly/YYYY-MM-DD_weekly.md` exists. |

---

**Last updated:** 2026-05-01  
**Status:** Live, tested, integrated with 8 bug fixes from April–May 2026  
**For:** Any user with 2+ calendars, 3+ concurrent activities, and immovable constraints (meals, routines)

---

## § Conventions

### Activity Code Format

**Pattern:** `ACTIVITY_SLUG` or `PROJ#-Name`

**Examples:**
```
JOB_SEARCH       (work-related, generic)
EDHEC            (education, short label)
CFA              (certification program, short label)
MEDITATION       (habit, generic)
PROJ1-Bitcoin    (project, numbered with name)
PROJ2-Bancos     (project, numbered with name)
RUN              (exercise via app)
GYM              (exercise, honor system)
LECTURA          (hobby, short label)
```

**Rules:**
- Uppercase alphanumeric + underscore/hyphen
- No spaces (use hyphen or underscore)
- Projects include number prefix (PROJ1, PROJ2, etc.)
- Keep ≤20 characters total for readability
- Match codes used in `01-config/config.md` Activity Codes table

---

### Log Entry Format

**Location:** `log.md` (append-only — never edit or delete old entries)

**Weekly Entry (MODE A):**
```
## [YYYY-MM-DD] weekly | ACT1: XX% · ACT2: XX% · ... · blocks: N created · conflicts: N escalated
```

**Daily Entry (MODE B):**
```
## [YYYY-MM-DD] daily | Changes: N · Conflicts: N · AT_RISK: M · [optional brief note]
```

---

### Report Formats

**Weekly report location:** `reports/weekly/YYYY-MM-DD_weekly.md`

Required sections:
1. Title: `# Weekly Report: Mon DD–Sun DD, YYYY`
2. Bar chart (20-char scale) — Planned vs. Goal per activity
3. Monthly Horizon — cumulative actuals vs. targets + remaining pace
4. Trend Proposals — activities with ≥2-week streak of missing goal (omit if none)
5. Gym Note — honor-system session count
6. Outlook — 2–3 sentences on pace + one concrete suggestion

Bar chart style:
```
💼 Job Search     [████████████░░] 12.1h / 10h (121%) ✅
🎓 EDHEC          [██████░░░░░░░░]  7.5h /  8h  (94%) 🟡
📊 CFA Level II   [████████░░░░░░]  6.0h /  6h (100%) ✅
```
Flags: ✅ ≥100% · 🟢 80–99% · 🟡 60–79% · 🔴 <60%

**Daily report location:** `reports/daily/YYYY-MM-DD_daily.md`

Required sections:
1. Title: `# Daily Sync: Weekday, Mon DD, YYYY`
2. Changes Made — bullet list of moves/creates/deletes with reasoning
3. Bar chart — Actual so far vs. weekly goal
4. Monthly Horizon — daily pacing snapshot
5. Outlook — 1–2 sentences

---

### Calendar Event Names

```
💼 Job Search (1h on Mon)
🎓 EDHEC Coursera (1.5h on Wed)
📊 CFA Level II (3h on Thu)
📚 Lectura (30 min on Wed)
🏃 Running (Runna-managed — never create)
🏋️ Gym (honor system — never create)
```

### File Naming

- Weekly reports: `YYYY-MM-DD_weekly.md` (Monday start date)
- Daily reports: `YYYY-MM-DD_daily.md` (calendar date)
- Log: single file `log.md` (append-only)

---

### Edge Cases

**Weekends:** P0 meals still required; P1 work on hold unless catch-up needed; P2 habits encouraged.

**Honor system (gym):** Not in calendar. Track manually, confirm in weekly report. Account for 30–45 min post-gym recovery in scheduling.

**App-managed exercise (e.g., Runna):** Never create exercise blocks. Respect pre-session (15 min) and post-session (45 min) buffers only.

**Sleeping projects:** Do NOT create blocks, track actuals, or include in reports. Note in `01-config/objectives.md` why sleeping and when to reactivate.

**Immovable conflict (P0 ↔ Personal):** Flag for user — do NOT proceed until clarified.

---

### Configuration Maintenance

| When | Update |
|------|--------|
| New activity or name change | `01-config/config.md` Activity Codes table |
| Window or buffer change | `01-config/config.md` |
| Weekly goal change | `01-config/objectives.md` §1 + calibration note in §5 |
| Monthly target change | `01-config/objectives.md` §2 |
| After every MODE A run | `log.md` (weekly entry) + `trends.md` (streaks) |
| After every MODE B run | `log.md` (daily entry) |

