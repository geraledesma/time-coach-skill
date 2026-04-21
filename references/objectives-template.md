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

<!--
  One row per activity. Priority column:
    P0 = daily non-negotiables (meals, routines) — never scored, never scheduled by the skill, never moved
    P1 = highest-priority tracked activities — recovered first when behind
    P2 = secondary tracked activities — recovered after P1s are covered

  P0 rows: set Weekly Goal = — and Tracking = —
  Window column: preferred time range, e.g. "10:00–13:00", "flex/weekend", "honor system", "[App]-owned"
  Duration column: typical single-block length, e.g. "2h", "1–1.5h", "30 min"
  Notes column: colorId N (1–11), "DO NOT create blocks", special rules

  Add window-sharing and special notes as plain text below the table.
-->

| Priority | Activity | Type | Weekly Goal | Window | Duration | Tracking | Notes |
|---|---|---|---|---|---|---|---|
| P0 | [🌞 Morning Routine] | must-do | — | [HH:MM–HH:MM] | [X min] | — | colorId [N] |
| P0 | [🍳 Breakfast] | must-do | — | [HH:MM–HH:MM] | [X min] | — | colorId [N] · after routine |
| P0 | [🏠 Home Tasks] | must-do | — | [HH:MM–HH:MM] | [X min] | — | colorId [N] · after breakfast |
| P0 | [🍽️ Lunch] | must-do | — | [HH:MM–HH:MM] | [X min] | — | colorId [N] |
| P0 | [🌙 Dinner] | must-do | — | [HH:MM–HH:MM] | [X min] | — | colorId [N] |
| P1 | [💼 Main Work Activity] | must-do | ≥[X]h | [HH:MM–HH:MM] | [Xh] | hours | min [X]h continuous |
| P1 | [🎓 Learning Activity] | project | ≥[X]h | [HH:MM–HH:MM] | [1.5–2h] | completion:[X]units | target completion [date] |
| P2 | [🤖 Secondary Learning] | habit | ≥[X]h | flex/weekend | [1h] | hours | no fixed slot |
| P2 | [🌐 Side Project A] | project | ≥[X]h | [HH:MM–HH:MM] | [1–1.5h] | hours | colorId [N] |
| P2 | [🏦 Side Project B] | project | ≥[X]h solo | [HH:MM–HH:MM] | [1–1.5h] | hours | alt days with [Project A] |
| P2 | [🏃 Session Activity] | habit | ≥[N] sessions | [App]-owned | — | sessions | DO NOT create blocks |
| P2 | [🏋️ Self-Tracked Activity] | habit | ≥[N] sessions | honor system | — | sessions | NOT in calendar |
| P2 | [📚 Evening Activity] | habit | ≥[X]h | [HH:MM–HH:MM] | [30 min] | hours | colorId [N] |

<!--
  Add window-sharing, sleeping projects, and special rules below as plain text:

  **Window sharing — [Project A] / [Project B]:** Both share [HH:MM–HH:MM].
  Default: [Project A] gets Mon/Wed/Fri · [Project B] gets Tue/Thu. Swap if one met goal.

  **[Sleeping project]:** SLEEPING. Do not schedule, track hours, or include in reports until reactivated.

  **[Self-tracked activity]:** Not in calendar ([reason]). Honor system: confirm in weekly review.
-->

> **Type values:** `must-do` · `habit` · `project`
>
> **Tracking values:** `hours` · `sessions` · `completion:Xunits` (e.g. `completion:200pages`)
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
