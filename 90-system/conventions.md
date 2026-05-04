---
updated: 2026-05-01
---

> **Purpose:** Format and naming conventions for consistency. Describes how reports are written, how log entries are formatted, how activity codes are defined.

# Time-Coach Conventions

---

## Activity Code Format

**Pattern:** `ACTIVITY_SLUG` or `PROJ#-Name`

**Examples:**
```
JOB_SEARCH       (work-related, generic)
EDHEC            (education, short label)
CFA              (certification program, short label)
MEDITATION       (habit, generic)
PROJ1-Bitcoin    (project, numbered with name)
PROJ2-Bancos     (project, numbered with name)
RUN              (exercise via Runna app)
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

## Log Entry Format

**Location:** `02-exec/log.md` (append-only)

**Weekly Entry (MODE A):**
```
## [YYYY-MM-DD] weekly | JS: XX% · EDH: XX% · CFA: XX% · MED: X ses · PROJ1: XX% · PROJ2: XX% · RUN: X ses · blocks: N created · conflicts: N escalated
```

**Daily Entry (MODE B):**
```
## [YYYY-MM-DD] daily | Changes: N · Conflicts: N · AT_RISK: M · [optional brief note if unusual]
```

**Activity Abbreviations (in log):**
- JS = Job Search
- EDH = EDHEC
- CFA = CFA Level II
- MED = Meditation
- PROJ1 = PROJ1-Bitcoin Insurance
- PROJ2 = PROJ2-Bancos y Sofipos
- RUN = Running

**Example Entry (full):**
```
## [2026-05-05] weekly | JS: 121% · EDH: 94% · CFA: 100% · MED: 4 ses · PROJ1: 100% · PROJ2: 75% · RUN: 3 ses · blocks: 18 created · conflicts: 1 escalated
```

**Note:** Log entries are immutable once written. Do not edit or delete old entries.

---

## Weekly Report Format

**Location:** `03-reports/weekly/YYYY-MM-DD_weekly.md` (example: `2026-05-05_weekly.md`)

**Required Sections:**
1. **Title:** `# Weekly Report: May 5–11, 2026`
2. **Bar Chart:** Planned vs. Goal for each tracked activity (20-char visualization)
3. **Monthly Horizon:** Cumulative actuals vs. monthly targets + remaining pace
4. **Trend Proposals:** Any activities with ≥2-week streak of missing goal (optional section if no proposals)
5. **Gym Note:** Honor-system confirmation (yes/no + session count)
6. **Outlook:** 2–3 sentences on what's on track, what needs attention, one concrete suggestion

**Bar Chart Style:**
```
💼 Job Search        [████████████░░] 12.1h / 10h (121%) ✅
🎓 EDHEC Coursera    [██████░░░░░░░░] 7.5h / 8h (94%) 🟡
📊 CFA Level II      [████████░░░░░░] 6h / 6h (100%) ✅
🧘 Meditation        [██████░░░░░░░░] 4 sessions / 4 (100%) ✅
```

**Flags:**
- ✅ = ≥100% of goal
- 🟢 = 80–99% on track
- 🟡 = 60–79% at risk
- 🔴 = <60% critical

**Trend Proposal Format (if needed):**
```
### 📚 Lectura — TARGET_HIGH (streak: 3 weeks)
- Weeks: Apr 21–27 (67%), Apr 28–May 4 (58%), May 5–11 (projected 70%)
- Pattern: Evening slot (21:15–22:15) consistently displaced by late dinners
- Proposed change to 01-config/config.md:
  Field: Lectura window
  From: 21:15–22:15
  To: 20:45–21:45
  Rationale: Earlier slot absorbs social dinners without sacrificing reading habit
```

---

## Daily Report Format

**Location:** `03-reports/daily/YYYY-MM-DD_daily.md` (example: `2026-05-06_daily.md`)

**Required Sections:**
1. **Title:** `# Daily Sync: Tuesday, May 6, 2026`
2. **Changes Made:** Bullet list of moves, creates, deletes with brief reasoning
3. **Bar Chart:** Actual (so far) vs. Goal for today + remaining
4. **Monthly Horizon:** Current pace check (same as weekly but daily snapshot)
5. **Outlook:** 1–2 sentences on pace and next actions

**Changes Format:**
```
## ✏️ Calendar Changes
- Moved: Job Search Wed 10:00–13:00 → 14:00–17:00 (conflict with Workshop 10:00–11:30)
- Created: Lectura recovery 21:15–21:45 (30 min, fell short this week)
- Deleted: EDHEC Thu afternoon (met weekly goal early)
- Merged: Two 1h CFA blocks → single 2h block
- Conflicts resolved: 2
- At-risk blocks created: 1
- Total changes: 5
```

---

## Trend Tracking (in `02-exec/trends.md`)

**Streak Count Table:**
```
| Activity | Consecutive weeks met | Consecutive weeks missed | Last updated |
|---|---|---|---|
| 💼 Job Search | 2 | 0 | 2026-05-01 |
| 🎓 EDHEC Coursera | 1 | 0 | 2026-05-01 |
| 📊 CFA Level II | 1 | 0 | 2026-05-01 |
```

**Historical Analysis Section:**
```
### Weekly Actuals (Claude Calendar)

| Activity | W1 Apr 23–29 | W2 Apr 30–May 6 | W3 May 7–13 | Monthly Goal |
|---|---|---|---|---|
| 💼 Job Search | 9.5h | 10.5h | 12.1h | ≥24h |
| 🎓 EDHEC | 8.8h | 6.2h | 7.5h | ≥32h |
```

---

## Naming: Files vs. Calendar Events

### Calendar Event Names (In Google Calendar)

Use emoji prefix + activity code for clarity in calendar view:

```
💼 Job Search (30 min on Mon)
🎓 EDHEC Coursera (1.5h on Wed)
📊 CFA Level II (2h on Sat)
🧘 Meditation (10 min on Tue)
🌐 PROJ2-Bancos y Sofipos (1h on Fri)
₿ PROJ1-Bitcoin Insurance (1h on Sun)
📚 Lectura (30 min on Wed)
🏃 Running (Runna-managed, not created by Claude)
🏋️ Gym (Honor system, not in calendar)
```

### File Names

**Weekly Reports:** `YYYY-MM-DD_weekly.md` (start date of week, e.g., `2026-05-05_weekly.md` for May 5–11)

**Daily Reports:** `YYYY-MM-DD_daily.md` (calendar date, e.g., `2026-05-06_daily.md` for Tuesday May 6)

**Log:** Single file `02-exec/log.md` (append-only, never overwrite)

---

## Edge Cases & Clarifications

### Weekends vs. Weekdays

**Weekday (Mon–Fri):**
- P0 and P1 activities required (meals, routine, job search)
- P2 activities flexible (projects, habits)

**Weekend (Sat–Sun):**
- P0 meals still required (humans eat weekends too)
- P1 work activities optional (no job search blocks on Sat/Sun unless special case)
- P2 activities encouraged (projects, learning, habits)

### Honor System (Gym)

Gym sessions are NOT in calendar (Runna deletes them). Instead:
- Track sessions manually or via Runna app
- Confirm sessions in weekly report: "Gym this week: 2 sessions ✅"
- Account for post-gym recovery (30–45 min) in afternoon scheduling on gym days
- Monthly goal checked via weekly honor-system confirmation, not calendar

### Running (Runna-Managed)

Runna app owns running scheduling. Claude never creates exercise blocks. Instead:
- Respect 15-min pre-Runna buffer (no activity 15 min before session)
- Respect 45-min post-Runna buffer (recovery, shower, travel)
- Count sessions from Runna calendar for reporting
- Monthly goal checked from Runna logs

### Sleeping Projects (SLEEPING Label)

If a project is "SLEEPING":
- Do NOT create calendar blocks for it
- Do NOT track actuals
- Do NOT include in reports
- Note in 01-config/objectives.md why it's sleeping and when to reactivate

### Immovable Conflict Escalation

If P0 meal overlaps a Personal event (both immovable):
- Do NOT create blocks that cause this
- FLAG for user review
- Ask: "How should I handle this conflict?"
- Do NOT proceed until user clarifies

---

## Configuration Maintenance

**When to Update `01-config/config.md`:**
- New activity created or named
- Activity windows change (e.g., job search moves from 10:00-13:00 to 14:00-17:00)
- Buffer rules customized
- New calendar added

**When to Update `01-config/objectives.md`:**
- Weekly goals adjusted
- Monthly targets changed
- Quarterly goals updated
- Calibration notes added

**When to Update `02-exec/log.md`:**
- After every MODE A run (weekly entry)
- After every MODE B run (daily entry)
- Never edit or delete old entries

**When to Update `02-exec/trends.md`:**
- After every MODE A run (update streak counts + historical table)
- Add analysis when patterns emerge
- Add calibration notes when goals change

---

## Cross-References & Paths

**Always use relative paths for portability:**
```
Good: ../01-config/config.md
Good: ../../02-exec/log.md
Bad: /Users/gera.ledesma/Documents/Claude/vault_personal/agents/time-coach/01-config/config.md
```

**File references in reports:**
- "See `01-config/config.md` for activity codes"
- "Refer to `02-exec/trends.md` for historical patterns"
- "Update `01-config/objectives.md` if targets change"

---

**Last Updated:** 2026-05-01  
**For:** All users of time-coach skill

