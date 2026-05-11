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

### § Config · Calendars

| Role | Calendar Name | Calendar ID | Access |
|---|---|---|---|
| write | [Your label, e.g. "Time Blocks"] | [User fills in] | Read+Write |
| manual | [Your label, e.g. "Personal"] | [User fills in] | Read-only |
| read-only | [Your label, e.g. "Fitness Tracker"] | [User fills in] | Read-only |

**How to find your Calendar ID:**
1. Go to Google Calendar → Settings (⚙️ gear icon)
2. In the left sidebar, click on the calendar name
3. Scroll down to "Integrate calendar"
4. Copy the Calendar ID (looks like: `yourname@gmail.com` or `abc123...@group.calendar.google.com`)
5. Paste it into the "Calendar ID" column above

**Role definitions:**
- **write**: The calendar where time-coach will create scheduling blocks (must have Read+Write access)
- **manual**: Reserved for calendars you manage manually (read-only from time-coach's perspective)
- **read-only**: Shared or external calendars that time-coach reads to check for conflicts

<!--
  The Read+Write calendar (Role="write") is the only one time-coach writes to.
  Manual and Read-only calendars are read when checking for conflicts (§2 conflict rules)
  and when reading session-based activity actuals (e.g. fitness app blocks).
-->

---

## §2 · Activities

Activity priorities, windows, and durations are configured in `raw/objectives.md §1`.
This file covers calendar credentials (§1), buffer rules (§3), and execution config (§4) only.

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
