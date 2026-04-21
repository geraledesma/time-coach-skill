# time-coach

A Claude Code skill for time management, priority tracking, and goal calibration.

**time-coach** helps you review your weekly actuals vs. targets, plan ahead, stay on pace for the month, approve calibration changes, and keep long-term projects on track — all from plain markdown files.

## Features

- 📊 **Weekly Review**: Compare actuals to goals with visual progress bars, sorted by priority
- 🗓️ **Next Week Planning**: Build a data-driven allocation plan from monthly trajectory — catch-up activities get more hours, overperforming ones less
- 📈 **Monthly Pacing**: Track trends across weeks and identify at-risk milestones
- ⚙️ **Proposal Review**: Approve or reject calibration proposals detected by streak analysis
- 🎯 **Goal Adjustment**: Change a weekly target and see all affected files (objectives, runbook, CLAUDE.md)
- 🚀 **Onboarding**: Set up vault structure with templates (objectives.md, log.md, trends.md, runbook.md)
- 🔔 **Proactive coaching**: Surfaces stale logs, undated quarterly goals, and zero-hour P1 gaps before you have to ask
- ⏰ **Rhythm-based check-ins**: Automatically asks for progress on completion-tracked goals at the right cadence (short-term: every session; medium-term: every 2 weeks; long-term: every 4 weeks)
- 📉 **Visual trend charts**: Time series bars for any activity over the last 8 weeks; 4-week grid in Monthly Pacing

## Installation

### Claude Code

```bash
/install-skill /path/to/time-coach.skill
```

Or clone this repo and run:

```bash
/install-skill /path/to/time-coach/
```

## Usage

### Weekly Review

```
Hey, do a weekly review for me. Vault is at /Users/you/Documents/Claude/vault_personal, agent folder is agenda-manager.
```

Output:
- Bar chart of actuals vs. goals (█/░, 20-char scale)
- Priority-sorted table (P1 → P2, then by completion %)
- Flags: ✅ (met), 🟢 (on track), 🟡 (warning), 🔴 (missed)
- Catch-up recommendations
- One coaching question for the top at-risk activity
- Offer to log and update trends
- Optional: time series trend chart for any activity

### Next Week Planning

```
How does next week look? Vault: /Users/you/Documents/Claude/vault_personal
```

Output:
- Monthly trajectory: weeks elapsed / remaining, per-activity deficit
- Prioritized allocation table with suggested hours and catch-up bars
- Constraint intake (travel, reduced availability)
- No file writes — advisory output only

### Monthly Pacing

```
Show me the monthly pacing for April. Vault: /Users/you/Documents/Claude/vault_personal.
```

Output:
- Actuals vs. monthly targets with daily pace needed vs. normal
- At-risk milestones and recovery paths
- Optional: 4-week activity grid showing weekly % per activity

### Proposal Review

```
Show me pending calibration proposals. Vault: /Users/you/Documents/Claude/vault_personal.
```

Output:
- Lists ⚠️ Pending proposals from trends.md
- Shows current vs. proposed values
- Asks approve/reject per proposal

### Goal Adjustment

```
I want to lower my Online Course goal from 7h to 5h. Vault: /Users/you/Documents/Claude/vault_personal.
```

Output:
- Verifies current goal
- Shows full diff across all files (objectives.md §1+§2, runbook.md, CLAUDE.md)
- Flags milestone date impact if completion timeline shifts
- Appends calibration history to trends.md upon approval

### Onboarding

```
Set up my vault for time tracking. Vault: /Users/you/Documents/Claude/vault_personal, agent: agenda-manager.
```

Output:
- Creates all templates if missing
- Explains the structure: raw/ (config), wiki/ (patterns), log.md (append-only data)

## Vault Structure

```
vault_personal/agents/agenda-manager/
├── raw/
│   ├── objectives.md          ← Weekly, monthly, quarterly targets
│   └── runbook.md             ← Schedule rules, priority tiers
├── wiki/
│   └── trends.md              ← Streaks, actuals history, calibration history
├── log.md                      ← Append-only operational log
└── CLAUDE.md                   ← Project metadata (calendars, people, milestones)
```

### objectives.md

§1 Weekly Targets, §2 Monthly Targets, §3 Quarterly Goals, §4 Project Milestones, §5 Calibration Notes.

#### Type column (§1)

Every activity has a type that controls how the coach tracks and coaches it:

| Type | Definition | Coach behavior |
|---|---|---|
| `must-do` | Compulsory, non-negotiable | Misses flagged as blockers, never calibrated down |
| `habit` | Recurring, non-compulsory but beneficial (includes learning) | Streak tracking, calibration proposals on 2+ week misses |
| `project` | Self-imposed, has a finish line | Completion tracking, estimated finish date vs. target, rhythm check-ins |

During onboarding the coach asks the type for each activity before setting the goal.

#### Tracking column (§1)

The `Tracking` column in §1 tells the coach how to measure progress for each activity:

| Value | Meaning |
|---|---|
| `hours` (default) | Recurring weekly hours goal |
| `sessions` | Session-count goal (gym, runs, etc.) |
| `completion:Xunits` | Goal with a finish line: `completion:200pages`, `completion:12modules` |

Completion-tracked goals get proactive progress check-ins at the right cadence and show a completion bar when you report progress:
```
📚 Reading  ████████░░░░░░░░░░░░  80/200 pages  40% complete
```

### log.md

Dictionary format (key: value) for LLM parsing. Weekly entries:

```
## 2026-04-20 · weekly

mode: weekly
work_project_h: 10.5
work_project_pct: 105
online_course_h: 4.8
online_course_pct: 69
online_course_completion: 4/12
online_course_completion_pct: 33
exercise_ses: 3
exercise_pct: 100
note: On track this week.
```

Progress check-in fields (written when coach asks a rhythm-based check-in):
```
progress_checkin_reading: 2026-04-19 · 80/200 · 40%
```

Daily entries (optional, from agenda-manager):

```
## 2026-04-17 · daily

mode: daily
changes: 1
conflicts: 1
at_risk: 0
note: Deleted duplicate block.
```

### trends.md

§ Streak Counts, § Weekly Actuals History, § Key Patterns, § Calibration History, § ⚠️ Pending Calibration Proposals.

Calibration proposals are auto-generated when a 2+ week streak is missed. You approve/reject them; time-coach applies changes if approved.

The § Weekly Actuals History table is the data source for time series trend charts.

## Design Philosophy

- **Ask before writing**: time-coach never modifies files without your explicit approval
- **Proactive, not reactive**: Surfaces stale data, missing deadlines, and completion gaps before you have to ask
- **Vault-agnostic**: Works with any vault location; you pass the path each run
- **Natural language**: Adjust goals in plain English; time-coach parses and shows diffs
- **LLM-parseable**: log.md uses dictionary format for easy parsing; trends.md is markdown for human readability
- **No external MCPs**: Plain markdown file I/O only; works offline

## Development

Evals are in `evals/evals.json`. Run them with the Claude Code Cowork skill-creator:

```bash
# In skill-creator repo
python3 -m scripts.eval_runner /path/to/time-coach/evals/evals.json
```

## License

MIT

## Author

Built for time-conscious builders. Questions? Open an issue.
