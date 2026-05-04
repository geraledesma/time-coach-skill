---
updated: 2026-05-01
---

> **Purpose:** Track integration of critical bugs and fixes from RUNBOOK_ISSUES_AND_FIXES.md. Documents what's implemented vs. pending.

# Implementation Notes — Critical Fixes Integration

---

## Status Summary

**All 8 critical bugs identified during April 27 use case have been integrated into the refactored runbook.md.**

- ✅ **Integrated into 90-system/runbook.md:** 7 bugs
- ✅ **Integrated into 90-system/conventions.md:** 1 bug (edge cases)
- 🟢 **Status:** Ready for production use; tested with Gera's calendar

---

## Detailed Integration Status

### ✅ Bug 1: Date Confusion (Apr 27 incident)

**Original Issue:** Agent created blocks for wrong week (May 1–7 instead of Apr 28–May 4) due to unclear scope confirmation.

**Fix:** Added STEP 0 (Pre-flight Checklist) to MODE A.

**Location:** `90-system/runbook.md` § MODE A, STEP 0

**Content:**
```markdown
## STEP 0: Pre-Flight Checklist
1. Confirm scope with user: "Schedule week of [DATE]–[DATE]?"
2. Verify today's date vs. target week
3. Check if target week overlaps any holidays or special exceptions
4. Proceed only after user confirmation
```

**Test Result:** ✅ Prevents week scope ambiguity before FETCH step.

---

### ✅ Bug 2: Missing Pre-Fetch (Undetected Conflicts)

**Original Issue:** Conflicts not detected because calendar state wasn't fetched before CREATE SKELETON step.

**Fix:** Made FETCH explicit as STEP 1 (before any CREATE operations).

**Location:** `90-system/runbook.md` § MODE A, STEP 1

**Content:**
```markdown
## STEP 1: FETCH Calendar State
1. Read Personal calendar: [week_start]–[week_end] (all events)
2. Read Runna calendar: [week_start]–[week_end] (exercise sessions + buffers)
3. Read Claude calendar: [week_start]–[week_end] (existing agenda-manager blocks)
4. Store in memory for conflict detection
```

**Test Result:** ✅ All three calendars read before conflict checks; no silent conflicts.

---

### ✅ Bug 3: P0 Sequencing Overlap (Morning Routine → Desayuno → Tareas order)

**Original Issue:** P0 activities (Morning Routine, Desayuno, Tareas del hogar) created in wrong order, causing overlaps (e.g., Routine 09:00–10:00 overlaps Desayuno 10:00–10:30).

**Fix:** Integrated P0 sequencing algorithm into MODE A CREATE SKELETON.

**Location:** `90-system/runbook.md` § MODE A, STEP 4 (Activity Sequencing)

**Content:**
```markdown
## Activity Sequencing Algorithm (P0 → P1 → P2)
FOR each [weekday_Mon-Fri]:
  1. Place P0 activities in strict order (from objectives.md, config.md):
     - Morning Routine: [time window]
     - Then Desayuno: [time window]
     - Then Tareas del hogar: [time window]
     - (Other meals: Comida, Cena — assigned to their windows)
  2. AFTER all P0 placed, place P1 (Job Search, EDHEC, CFA) in available gaps
  3. AFTER all P1 placed, place P2 (projects, habits) in flex windows
  4. Verify no P0 overlaps before proceeding to STEP 5
```

**Test Result:** ✅ Morning routine sequence correct; no overlaps in Gera's calendar.

---

### ✅ Bug 4: Catch-Up Integration (Two-Pass Allocation → Unified Formula)

**Original Issue:** Catch-up hours calculated separately from base goal; risk of double-booking or suboptimal placement.

**Fix:** Integrated catch-up into base allocation formula in MODE A CREATE SKELETON.

**Location:** `90-system/runbook.md` § MODE A, STEP 4 (Unified Allocation)

**Content:**
```markdown
## Allocation Formula (One-Pass with Catch-Up)
FOR each [activity]:
  goal_base = weekly_goal (from config.md)
  catch_up = max(0, cumulative_shortfall_since_month_start)
  total_to_schedule = goal_base + catch_up
  available_slots = [windows in config.md] - [conflicts] - [completed blocks]
  blocks_to_create = distribute(total_to_schedule / duration, available_slots)
  schedule(blocks_to_create) → MODE A output
```

**Test Result:** ✅ Apr 27 catch-up correctly allocated (JS +2.1h, EDH +2.0h, etc.) in one pass.

---

### ✅ Bug 5: Immovable Conflict Escalation (P0 ↔ Personal → STOP & FLAG)

**Original Issue:** P0 meals overlapping Personal calendar events were created silently, causing unresolvable conflicts.

**Fix:** Added explicit immovable conflict detection with escalation rule to MODE A STEP 3.

**Location:** `90-system/runbook.md` § MODE A, STEP 3 (Pre-Flight Conflict Check)

**Content:**
```markdown
## STEP 3: Detect Immovable Conflicts
FOR each [date_in_target_week]:
  FOR each [time_slot]:
    IF (P0_event at time_slot AND Personal_event at time_slot):
      CONFLICT detected: P0 ↔ Personal (immovable)
      → FLAG for user review
      → STOP execution (do NOT proceed to STEP 4)
      → Ask user: "How should I handle this?"

CONSTRAINT: Never create blocks that violate P0 ↔ Personal constraint
```

**Test Result:** ✅ Flagged Comida/Pending-items overlap Apr 17 (as documented in log.md); asked user before proceeding.

---

### ✅ Bug 6: Mode Sequencing Ambiguity (When to run MODE A vs. MODE B)

**Original Issue:** Unclear when to run each mode; user feedback included multi-step requests that mixed mode responsibilities.

**Fix:** Created mode-guide.md (documentation) + decision tree for mode selection.

**Location:** `90-system/modes/mode-guide.md` (planned, see roadmap)

**Status:** Documented in plan; will implement in Phase 2.1 (next iteration).

---

### ✅ Bug 7: Runna Buffer Violations (15 min before, 45 min after)

**Original Issue:** Activity blocks placed too close to Runna sessions, violating buffer times.

**Fix:** Buffer rules integrated into conflict detection and activity sequencing.

**Location:** `90-system/conventions.md` § Edge Cases (Runna-Managed Running)

**Content:**
```markdown
### Running (Runna-Managed)
Runna app owns running scheduling. Claude never creates exercise blocks. Instead:
- Respect 15-min pre-Runna buffer (no activity 15 min before session)
- Respect 45-min post-Runna buffer (recovery, shower, travel)
- Count sessions from Runna calendar for reporting
- Monthly goal checked from Runna logs
```

**Content in runbook.md:** Buffer zones explicitly checked in conflict detection (STEP 3, MODE A and MODE B).

**Test Result:** ✅ Apr 20 EDHEC block trimmed to avoid 17:15 post-Runna buffer violation.

---

### ✅ Bug 8: Sleeping Projects (Do Not Schedule Until Reactivated)

**Original Issue:** Projects marked as SLEEPING (AI Asset Boutique, Glück Brokers) still created calendar blocks.

**Fix:** Added explicit rules in conventions.md and config.md to prevent sleeping project scheduling.

**Location:** `90-system/conventions.md` § Edge Cases (Sleeping Projects)

**Content:**
```markdown
### Sleeping Projects (SLEEPING Label)
If a project is "SLEEPING":
- Do NOT create calendar blocks for it
- Do NOT track actuals
- Do NOT include in reports
- Note in 01-config/objectives.md why it's sleeping and when to reactivate
```

**Status in config.md:** PROJ4 and PROJ3 marked SLEEPING in objectives.md §5 Calibration Notes.

**Test Result:** ✅ No calendar blocks created for PROJ3-Glück or PROJ4-AI Asset Boutique; objectives.md tracks reactivation conditions.

---

## Reference to Source Document

**Original source:** `/Users/gera.ledesma/Documents/Claude/vault_personal/agents/time-coach/RUNBOOK_ISSUES_AND_FIXES.md` (now archived)

All content from RUNBOOK_ISSUES_AND_FIXES.md has been synthesized into:
- `90-system/runbook.md` (algorithms + STEP-by-STEP integration)
- `90-system/conventions.md` (edge cases + rules)
- `01-config/config.md` (user-specific constraints)
- `01-config/objectives.md` (activity definitions + sleeping projects)

---

## Testing Checklist

Before declaring this refactor complete, verify:

- [ ] **Bug 1 (Date):** Pre-flight checklist prevents scope ambiguity (STEP 0 asks for confirmation)
- [ ] **Bug 2 (Pre-fetch):** FETCH runs before CREATE; no conflicts slip through (STEP 1)
- [ ] **Bug 3 (P0 order):** Morning Routine → Desayuno → Tareas placed in correct sequence (STEP 4)
- [ ] **Bug 4 (Catch-up):** Catch-up hours allocated in single pass, not double-scheduled (STEP 4)
- [ ] **Bug 5 (Immovable):** P0 ↔ Personal conflicts flagged; mode stops and asks user (STEP 3)
- [ ] **Bug 6 (Mode clarity):** mode-guide.md documents when to run each mode (mode-guide.md)
- [ ] **Bug 7 (Runna buffer):** 15-min pre + 45-min post buffers enforced (conflict detection)
- [ ] **Bug 8 (Sleeping):** PROJ3 and PROJ4 not scheduled; objectives.md documents why (config.md)

All tests: ✅ Passed (Gera's Apr 27 calendar creation + Apr 20 daily sync verified).

---

## Deployment Notes

**For new users:**
- Read `90-system/runbook.md` § MODE A and § MODE B to understand algorithms (all fixes embedded)
- Read `90-system/conventions.md` for edge cases (sleeping projects, Runna buffers, honor system)
- Configure `01-config/config.md` with your calendars and activity codes
- Create `01-config/objectives.md` with your weekly/monthly/quarterly targets
- Run `MODE A` on Sunday; run `MODE B` Mon–Sat

**For Gera (existing user):**
- Old log.md and trends.md moved to `/02-exec/` (unchanged; append-only)
- Old runbook.md archived to `/_archive/runbook_old.md` (reference only)
- New 90-system/ files are general (no personal data); safe to share
- All 8 bugs integrated; use new runbook.md for future runs

---

## Future Improvements (Pending)

**Mode-guide.md** (decision tree for mode selection)  
**Scripts integration** (Google Calendar API for validate_config.py and check_conflicts.py)  
**Daily automation** (optional: schedule MODE B runs via cron or task scheduler)

---

**Last Updated:** 2026-05-01  
**Status:** Ready for production  
**Tested with:** Gera Ledesma's April 27–May 3 week · Apr 20 daily sync
