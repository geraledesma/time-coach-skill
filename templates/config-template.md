---
updated: 2026-05-01
---

> **Purpose:** Blank template for new users. Copy this file to `01-config/config.md` and fill in your own values.
> **Instructions:** Each field is marked with [FILL IN]. Replace with your actual data. Delete this note when done.

# Time-Coach User Configuration

---

## User Profile

- **Name:** [FILL IN: Your full name]
- **Email:** [FILL IN: Your primary email]
- **Timezone:** [FILL IN: e.g., America/New_York, Europe/London, Asia/Tokyo]

---

## Connected Calendars

| Role | Calendar ID | Access |
|------|---|---|
| Personal | [FILL IN: Personal calendar email or ID] | Read-only |
| Exercise | [FILL IN: Runna, Strava, or fitness app calendar ID, if applicable] | Read-only |
| Claude | [FILL IN: Claude agent calendar ID for scheduling] | Read+Write |

**Note:** Personal and Exercise calendars are read-only (Claude respects them). Claude calendar is where time-coach creates blocks.

---

## Customized Buffer Rules

If different from defaults, override here:

| Buffer | Time | Notes |
|---|---|---|
| Before exercise session | [FILL IN: e.g., 15 min] | Warmup/transition time |
| After exercise session | [FILL IN: e.g., 45 min] | Recovery + shower + travel |
| Between activity ↔ meal | [FILL IN: e.g., 15 min] | Digestive transition |
| Hard scheduling window | [FILL IN: e.g., 08:00–22:30] | No blocks outside this range |

**Defaults** (if not customized):
- Before exercise: 15 min
- After exercise: 45 min
- Activity ↔ Meal: 15 min
- Hard window: 08:00–22:30

---

## Activity Codes & Mappings

Define your activities here. Each activity has a code, priority, goal, window, and tracking method.

| Code | Priority | Activity Name | Weekly Goal | Preferred Window | Duration | Tracking | Notes |
|---|---|---|---|---|---|---|---|
| [FILL IN CODE] | P0/P1/P2 | [FILL IN: e.g., Breakfast] | [e.g., —] | [e.g., 10:00–10:30] | 30 min | — | [Daily routine/must-do] |
| [FILL IN CODE] | P1 | [FILL IN: e.g., Job Search] | [FILL IN: ≥6h] | [FILL IN: 10:00–13:00] | 1.5h | hours | [Weekdays only] |
| [FILL IN CODE] | P1 | [FILL IN: e.g., Education] | [FILL IN: ≥8h] | [FILL IN: 17:00–20:00] | 2h | hours | [Sprint to deadline] |
| [FILL IN CODE] | P2 | [FILL IN: e.g., Side Project] | [FILL IN: ≥5h] | [FILL IN: flex] | 1–2h | hours | [Flexible slot] |
| [FILL IN CODE] | P2 | [FILL IN: e.g., Gym] | [FILL IN: ≥2 sessions] | — | — | sessions | [Honor system, not in calendar] |
| [FILL IN CODE] | P2 | [FILL IN: e.g., Reading] | [FILL IN: ≥2h] | [FILL IN: 21:00–22:00] | 30 min | hours | [Wind-down habit] |

**Instructions:**
- **Code:** Unique identifier (e.g., JOB_SEARCH, EDHEC, PROJ1-MyProject). Use alphanumeric + underscore/hyphen, ≤20 chars.
- **Priority:** P0 (immovable daily routine), P1 (must-do weekly goal), P2 (flexible habit/project)
- **Weekly Goal:** Hours (e.g., ≥6h) or sessions (e.g., ≥3 sessions)
- **Preferred Window:** Time range (e.g., 10:00–13:00) or "flex" if flexible
- **Duration:** Single block duration (e.g., 1.5h, 30 min)
- **Tracking:** hours, sessions, completion, honor-system
- **Notes:** Context (weekdays only? sprint? flex? honor-system?)

---

## Week Definition

- **Week runs:** [FILL IN: Mon–Sun or other, e.g., Sun–Sat]
- **Hard scheduling window:** [FILL IN: e.g., 08:00–22:30]
- **Must-do exemptions:** [FILL IN: e.g., Weekends, or specific dates]
- **Special exceptions:** [FILL IN: e.g., Holidays, annual events]

**Example:**
```
- Week runs: Mon–Sun
- Hard window: 08:00–22:30 (no blocks outside this range)
- Must-do exemptions: Weekends (P0 meals still required, P1 work on hold)
- Exceptions: Christmas (Dec 25), Summer vacation (Jul 15–Aug 15)
```

---

## Meal Schedule (P0 - Immovable)

Define your daily meals for P0 meal block creation:

| Meal | Time | Duration |
|---|---|---|
| [FILL IN: e.g., Breakfast] | [FILL IN: e.g., 10:00–10:30] | 30 min |
| [FILL IN: e.g., Lunch] | [FILL IN: e.g., 14:30–15:15] | 45 min |
| [FILL IN: e.g., Dinner] | [FILL IN: e.g., 20:30–21:15] | 45 min |

---

## Daily Routine (P0 - Immovable)

Define your fixed daily routine blocks:

| Routine | Time | Duration | Days |
|---|---|---|---|
| [FILL IN: e.g., Morning Routine] | [FILL IN: e.g., 09:00–10:00] | 1 hour | Mon–Fri |
| [FILL IN: e.g., Home Tasks] | [FILL IN: e.g., 10:30–11:15] | 45 min | Mon–Fri |

---

## Notes for First Run

- Copy this file to `01-config/config.md` and fill in all [FILL IN] fields
- Create `01-config/objectives.md` with your weekly/monthly targets (use `templates/objectives-template.md`)
- Create `runtime/` and `reports/weekly/` and `reports/daily/` directories
- Run: `python scripts/validate_config.py 01-config/config.md`
- Follow `runbook.md` § MODE A to run your first week

---

**Template Version:** 2026-05-01  
**For:** New users getting started with time-coach
