---
updated: 2026-05-01
---

# Time-Coach System Documentation

> **Purpose:** Complete skill documentation for calendar scheduling and weekly planning. Everything in this directory is generic and shareable — no personal data or user-specific configuration.

---

## Quick Navigation

| File | Purpose | Read When |
|------|---------|-----------|
| **[index.md](index.md)** | Entry point & file guide | First time using time-coach |
| **[runbook.md](runbook.md)** | Detailed algorithms for MODE A (weekly) & MODE B (daily) | Ready to schedule your first week or day |
| **[conventions.md](conventions.md)** | Format rules, naming conventions, edge cases | Setting up your config or writing reports |
| **[config.template.md](config.template.md)** | Blank template to customize for your calendars/activities | Before your first run; copy to `01-config/config.md` |
| **[IMPLEMENTATION_NOTES.md](IMPLEMENTATION_NOTES.md)** | Tracks critical bugs fixed and their integration | Interested in robustness/testing |

---

## Getting Started (15 Minutes)

### Step 1: Copy Core Files
You already have 90-system/ on disk. No action needed — these files are generic for all users.

### Step 2: Create Your Config (5 minutes)
```bash
cp 90-system/config.template.md 01-config/config.md
# Edit 01-config/config.md with YOUR values:
# - Name, Email, Timezone
# - Calendar IDs (Personal, Exercise, Claude)
# - Activity codes (Job Search, Education, Projects, etc.)
# - Meal schedule and daily routines
```

### Step 3: Create Your Objectives (5 minutes)
Create `01-config/objectives.md` with your weekly, monthly, and quarterly targets. Use Gera's as a template if helpful.

### Step 4: Validate & Run
```bash
python3 scripts/validate_config.py 01-config/config.md
# → ✅ Ready for MODE A execution

# Follow runbook.md § MODE A to schedule your first week (Sunday)
```

---

## Understanding the Skill

### Two Modes of Operation

**MODE A: Weekly Planning (Sundays)**
- Input: Your config + this week's Personal/Exercise calendars
- Output: A skeleton week of scheduled blocks (Job Search, Education, Projects, Habits)
- Time: ~30 minutes
- Read: `runbook.md` § MODE A

**MODE B: Daily Sync (Mon–Sat)**
- Input: Yesterday's + today's calendar
- Output: Resolve conflicts, flag at-risk activities, update weekly progress
- Time: ~5 minutes
- Read: `runbook.md` § MODE B

### Key Concepts

**Priority Levels:**
- **P0 (Immovable):** Meals, morning routines, sleep. Never move unless unavoidable.
- **P1 (Must-Do):** Job search, education, major projects. Scheduled every weekday.
- **P2 (Flexible):** Hobbies, side projects, habits. Fit around P0 + P1.

**Buffer Rules:**
- **Before exercise:** 15 min warmup
- **After exercise:** 45 min recovery (shower, travel)
- **Between activity & meal:** 15 min digestive transition
- **Hard window:** 08:00–22:30 (no blocks outside this range)

**Conflict Resolution:**
- P0 ↔ Personal event → ESCALATE (ask user; don't override)
- P1 ↔ Personal event → MOVE P1 to different time
- P2 ↔ anything → DELETE or MOVE P2

---

## File Descriptions

### runbook.md
The heart of the skill. Contains:
- **MODE A (Weekly Planning):** Step-by-step algorithm for creating a week of calendar blocks
  - STEP 0: Pre-flight checklist (prevents date confusion)
  - STEP 1: FETCH all calendars (prevents missing conflicts)
  - STEP 2: Check for sleep/meal gaps
  - STEP 3: Detect immovable conflicts (P0 ↔ Personal)
  - STEP 4: CREATE SKELETON (activity sequencing, catch-up allocation, P0→P1→P2 order)
  - STEP 5: UPDATE CALENDAR (write blocks to Claude calendar)
  - STEP 6: WRITE REPORT (weekly report in 03-reports/)
  - STEP 7: UPDATE LOG & TRENDS (append to 02-exec/log.md and trends.md)
- **MODE B (Daily Sync):** Step-by-step algorithm for resolving daily conflicts
  - STEP 1: FETCH today's + tomorrow's calendars
  - STEP 2: Detect DUPLICATE blocks
  - STEP 3: Detect CONFLICTS (overlap with Personal, buffer violations, etc.)
  - STEP 4: Detect MET_PRUNE (remove completed blocks to avoid duplication)
  - STEP 5: Detect AT_RISK (activities projected to miss weekly goal)
  - STEP 6: HORIZON CHECK (monthly pacing check)
  - STEP 7: WRITE changes (execute calendar updates in parallel)
  - STEP 8: UPDATE LOG (one-line entry to 02-exec/log.md)
  - STEP 9: WRITE DAILY REPORT (in 03-reports/)

### conventions.md
Rules for consistency:
- Activity code format (JOB_SEARCH, PROJ1-Bitcoin, etc.)
- Log entry format (weekly vs. daily)
- Report sections and structure
- Trend tracking (streak counts, historical analysis)
- Edge cases (weekends vs. weekdays, honor system for gym, Runna-managed exercise, sleeping projects)

### config.template.md
Blank template for new users. Copy to `01-config/config.md` and fill in your values.

### IMPLEMENTATION_NOTES.md
Tracks 8 critical bugs discovered during the April 27 use case and how each is integrated into the new runbook:
1. Date confusion (STEP 0 pre-flight checklist)
2. Missing pre-fetch (STEP 1 explicit FETCH)
3. P0 sequencing overlaps (STEP 4 activity sequencing algorithm)
4. Catch-up integration (STEP 4 unified allocation formula)
5. Immovable conflict escalation (STEP 3 P0 ↔ Personal detection)
6. Mode sequencing ambiguity (mode-guide.md, planned)
7. Runna buffer violations (conflict detection with buffer zones)
8. Sleeping projects (conventions.md + config.md rules)

### index.md
Navigation guide with file map, getting started (5 steps, 15 minutes), and key concepts overview.

---

## Bundled Scripts

Both scripts are templates; full Google Calendar API integration requires OAuth setup (not included).

### validate_config.py
Checks that your `01-config/config.md` has all required fields before MODE A runs.

```bash
python3 scripts/validate_config.py 01-config/config.md
# → ✅ Config validation passed (or lists missing fields)
```

### check_conflicts.py
Pre-flight conflict detection before calendar writes. Prevents immovable conflicts (P0 ↔ Personal) from being created silently.

```bash
# Currently: template/documentation (requires Google Calendar API)
# Usage: Called internally by MODE A STEP 3
```

---

## References (Templates & Guides)

### references/weekly_report_template.md
Structure for MODE A output. Shows:
- Activity progress (actual vs. goal, % completion)
- Monthly horizon (pace check for month-to-date)
- Trend alerts (activities in danger of missing goals)
- Gym & running notes
- Calendar health (blocks created, conflicts resolved, at-risk blocks)
- Outlook & next week recommendations

### references/daily_report_template.md
Structure for MODE B output. Shows:
- Changes made (created/moved/deleted/merged blocks)
- Actual progress today
- Weekly horizon (current pace vs. weekly goal)
- At-risk activities
- Conflicts detected & resolved
- Optimization notes
- Outlook & pace check

---

## User-Specific Configuration

**NOT in 90-system/**; lives in `01-config/`:
- `config.md`: Your calendars, activity codes, buffers, meal schedule, timezone
- `objectives.md`: Your weekly/monthly/quarterly targets and calibration notes

**Execution logs and reports (NOT versioned):**
- `02-exec/log.md`: Append-only daily/weekly run log
- `02-exec/trends.md`: Historical patterns and calibration history
- `03-reports/`: Generated weekly and daily reports

---

## Customization for Your Life

The skill is designed to adapt to any schedule. When customizing:

1. **Activity codes:** Rename or add activities that match your goals (education, side projects, health habits)
2. **Meal schedule:** Adjust times if your mealtimes differ from Gera's (10:00 Breakfast → whatever works for you)
3. **Buffer rules:** If your post-exercise recovery is 30 min (not 45), adjust in `01-config/config.md`
4. **Windows:** Move activity windows (Job Search 10:00–13:00 → 14:00–17:00) to fit your schedule
5. **Hard window:** If you work later (08:00–23:30 instead of 08:00–22:30), update the hard scheduling window
6. **P0 order:** If you shower before breakfast, adjust the Morning Routine → Desayuno sequence

All customization stays in `01-config/`; 90-system/ remains unchanged and shareable.

---

## Testing & Validation

Before using in production:

1. **Config validation:** Run `validate_config.py` on your config.md (should pass ✅)
2. **One-week test:** Follow `runbook.md` § MODE A for your first week (Sunday)
3. **One-day sync:** Follow `runbook.md` § MODE B for one day (check report matches your calendar)
4. **Review:** Check the generated reports for accuracy and adjust config if needed

All three tests pass? You're ready to use time-coach daily. ✅

---

## Contributing & Feedback

This skill is designed to be shareable and improvable. If you find bugs or edge cases:
1. Note them in `02-exec/trends.md` § Pending Calibration Proposals
2. If critical: flag in `IMPLEMENTATION_NOTES.md` § Future Improvements
3. When ready, update runbook.md, conventions.md, or config.template.md

---

**Version:** 2026-05-01  
**Status:** Ready for production  
**Tested with:** Gera Ledesma's calendar (Apr 27–May 3 week)  
**Last Updated:** May 1, 2026  
**For:** Any user managing multiple concurrent projects, education, and health habits
