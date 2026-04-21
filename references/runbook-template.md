---
updated: [YYYY-MM-DD]
---

> **Purpose:** Google Calendar schedule rules for time-coach
> **Read by:** time-coach skill during Review (reads actuals), Next Week Planning (suggests + creates blocks), Calendar Sync (daily sync), and Calendar Write (block skeleton)
> **Edited by:** human (rules, windows, calendars); time-coach proposes changes via agenda-companion flows, never applies without confirmation
>
> **To use:** Replace every `[PLACEHOLDER]` with your own values. Sections §3 and §4 have working defaults you can keep as-is. This file lives in your vault at `agents/time-coach/runbook.md`.

---

## §1 · Calendars

<!--
  Find your Calendar IDs in Google Calendar → Settings (gear icon) → click a calendar name → scroll to
  "Calendar ID". It looks like: yourname@gmail.com or a long hash@group.calendar.google.com

  You need at minimum one Read+Write calendar for time-coach to create scheduling blocks.
  Recommended: create a dedicated calendar (e.g. "Time Blocks") so skill-created events don't
  mix with personal appointments. In Google Calendar: + Other calendars → Create new calendar.

  Add additional Read-only calendars if you want the skill to read events from them
  (e.g. a fitness app calendar like Runna, a shared work calendar).
-->

User: [Your Name] · [your.email@gmail.com] · Timezone: [Region/City]

| Role         | Calendar ID                                      | Access     |
|--------------|--------------------------------------------------|------------|
| Personal     | [your.email@gmail.com]                           | Read-only  |
| [App/Team]   | [hash@group.calendar.google.com]                 | Read-only  |
| [Time Blocks]| [hash@group.calendar.google.com]                 | Read+Write |

<!--
  The Read+Write calendar is the only one time-coach writes to.
  Personal and Read-only calendars are read when checking for conflicts (§2 conflict rules)
  and when reading session-based activity actuals (e.g. fitness app blocks).
-->

---

## §2 · Schedule Rules

<!--
  One row per activity you track in objectives.md §1.

  Prio column:
    P0 = daily non-negotiables (meals, routines) — never scheduled by the skill, never moved
    P1 = highest-priority tracked activities — recovered first when behind
    P2 = secondary tracked activities — recovered after P1s are covered

  Window column: preferred time range for blocks, e.g. "10:00–13:00" or "flex/weekend" or "honor system"
    - "flex/weekend": no fixed slot; schedule on Sat/Sun if missed during the week
    - "honor system": tracked but NO calendar blocks ever created (user self-reports)
    - "Runna-owned" or "[App]-owned": the app manages these blocks; DO NOT create blocks

  Duration column: typical single-block length, e.g. "2h", "1–1.5h", "30 min"
    - Used when distributing hours evenly across available days

  Notes column:
    - colorId N (1–11 for Google Calendar event colors): 1=Lavender 2=Sage 3=Grape 4=Flamingo
      5=Banana 6=Tangerine 7=Peacock 8=Blueberry 9=Basil 10=Tomato 11=Graphite
    - "DO NOT create blocks" — read-only activity; blocks are managed by another app
    - Any special rule for this activity

  P0 activities are completely skipped during block creation — they're assumed always present.
  Activities marked "honor system" are scored in reviews but never get calendar blocks.
-->

```
Prio | Activity                     | WeekGoal    | Window           | Duration | Notes
-----|------------------------------|-------------|------------------|----------|---------------------------
P0   | [🌞 Morning Routine]         | —           | [HH:MM–HH:MM]    | [X min]  | colorId [N]
P0   | [🍳 Breakfast]               | —           | [HH:MM–HH:MM]    | [X min]  | colorId [N] · after routine
P0   | [🏠 Home Tasks]              | —           | [HH:MM–HH:MM]    | [X min]  | colorId [N] · after breakfast
P0   | [🍽️ Lunch]                   | —           | [HH:MM–HH:MM]    | [X min]  | colorId [N]
P0   | [🌙 Dinner]                  | —           | [HH:MM–HH:MM]    | [X min]  | colorId [N]
P1   | [💼 Main Work Activity]      | ≥[X]h       | [HH:MM–HH:MM]    | [Xh]     | min [X]h continuous
P1   | [🎓 Learning Activity]       | ≥[X]h       | [HH:MM–HH:MM]    | [1.5–2h] | target completion [date]
P2   | [🤖 Secondary Learning]      | ≥[X]h       | flex/weekend     | [1h]     | no fixed slot
P2   | [🌐 Side Project A]          | ≥[X]h       | [HH:MM–HH:MM]    | [1–1.5h] | colorId [N]
P2   | [🏦 Side Project B]          | ≥[X]h solo  | [HH:MM–HH:MM]    | [1–1.5h] | alt days with [Project A]
P2   | [🏃 Session Activity]        | ≥[N] ses    | [App]-owned      | —        | DO NOT create blocks
P2   | [🏋️ Self-Tracked Activity]   | ≥[N] ses    | honor system     | —        | NOT in calendar
P2   | [📚 Evening Activity]        | ≥[X]h       | [HH:MM–HH:MM]    | [30 min] | colorId [N]
```

<!--
  Window sharing: if two P2 activities compete for the same time window, add a note like:
  "[Project A] / [Project B] window sharing: [Project A] gets Mon/Wed/Fri · [Project B] gets Tue/Thu"
  (reflects relative goal weight — higher-goal project gets more slots)

  Sleeping projects: add a note "💤 [Project] — SLEEPING. Do not create blocks, track hours,
  or include in reports until reactivated." to exclude without deleting the row.
-->

---

## §3 · Buffer Rules

<!--
  Buffer rules prevent back-to-back scheduling that would be unrealistic.
  The defaults below work for most schedules. Adjust to match your routines.
  "Hard window" is the earliest and latest time any block can be placed.
-->

```
Rule                                           | Value
-----------------------------------------------|------------------
Before any fitness/session activity            | ≥15 min
After any fitness/session activity             | ≥45 min
Post-meal before any work block                | ≥15 min
Post-[gym/high-intensity] recovery             | ≥30–45 min · account in afternoon scheduling
Any activity ↔ any meal block                  | ≥15 min
Hard window (no blocks outside this range)     | [08:00–22:30]
P0 meal blocks                                 | never move / shrink / delete
```

---

## §4 · Execution

<!--
  This section configures the autonomous Calendar Sync and Calendar Write modes.
  time-coach reads §1–§3 when running interactively.

  If you use time-coach with Coworks scheduled triggers:
    - Daily trigger: point at time-coach with context "run calendar sync"
    - Weekly trigger (Sunday): point at time-coach with context "run calendar write"
    - Leave Coworks frequency unchanged; time-coach's sync_cadence / write_cadence in
      objectives.md § Config control whether each run actually executes.

  Replace [VAULT] with the absolute path to your vault root.
  Example: /Users/yourname/Documents/my-vault
-->

Mode: `Sunday → Calendar Write` | `Mon–Sat → Calendar Sync`

`[VAULT]` = `[/absolute/path/to/your/vault]`
