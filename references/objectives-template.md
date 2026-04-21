---
updated: YYYY-MM-DD
---

> **Purpose:** Human-set weekly/monthly/quarterly targets — ground truth for time-coach
> **Edited by:** human or via time-coach skill (natural language)

# [Your Name] · Objectives & Targets

---

## § Config

```
review_cadence: 7         ← days between reviews (default 7; set to 3, 5, 14, etc.)
sync_cadence: 1           ← days between calendar syncs (default 1 = daily; requires GCal MCP)
write_cadence: 7          ← days between full calendar writes (default 7 = weekly; requires GCal MCP)
write_horizon: 7          ← how many days ahead Calendar Write fills blocks (default 7; set to 3, 14, etc.)
timezone: Region/City     ← e.g. America/Mexico_City · used for all calendar operations
```

> `sync_cadence`, `write_cadence`, and `write_horizon` are only used when Google Calendar is connected.
> `review_cadence` controls the stale-log check — if your last review was more than this many days ago,
> the skill will prompt you to do a review before anything else.

---

## §1 · Weekly Targets

| Activity | Type | Weekly Goal | Tracking | Notes |
|---|---|---|---|---|
| [Activity 1] | must-do | ≥Xh | hours | |
| [Activity 2] | habit | ≥X sessions | sessions | |
| [Activity 3] | habit | ≥Xh | hours | |
| [Activity 4] | project | ≥Xh | completion:200pages | e.g. book — tracks to a finish line |

> **Type column values:** `must-do` · `habit` · `project`
>
> **Tracking column values:**
> - `hours` (default) — standard recurring-hours goal
> - `sessions` — session-count goal (gym, runs, etc.)
> - `completion:Xunits` — project with a finish line: `completion:200pages`, `completion:12modules`
>
> Projects must also have a target date in §3 Quarterly Goals or §4 Project Milestones.

---

## §2 · Monthly Targets

| Activity | Monthly Goal | Rationale |
|---|---|---|
| [Activity 1] | ≥Xh | Xh/week × 4 |
| [Activity 2] | ≥Xh | Xh/week × 4 |
| [Activity 3] | ≥X sessions | X/week × 4 |

> Update monthly targets at the start of each month.

---

## §3 · Quarterly Goals

| Goal | Target Date | Key Result | Status |
|---|---|---|---|
| [Goal 1] | YYYY-MM-DD | [What done looks like] | 🔴 Not started |

> Review and update quarterly goals at the start of each month.

---

## §4 · Project Milestones

| Project | Milestone | Target Date | Key Result | Status |
|---|---|---|---|---|
| [Project] | [Milestone] | YYYY-MM-DD | [What done looks like] | 🔴 Not started |

---

## §5 · Calibration Notes

- Add notes here when you adjust a goal: what changed, why, and what you observed.
