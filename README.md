# time-coach

A Claude Code skill for time management, priority tracking, and goal calibration.

**time-coach** helps you review your weekly actuals vs. targets, approve calibration changes, and stay on track with your projects and learning goals.

## Features

- 📊 **Weekly Review**: Compare actuals to goals with visual progress bars, sorted by priority
- 📈 **Monthly Pacing**: Track trends across weeks and identify at-risk milestones
- ⚙️ **Proposal Review**: Approve or reject calibration proposals detected by streak analysis
- 🎯 **Goal Adjustment**: Change a weekly target and see all affected files (objectives, runbook, CLAUDE.md)
- 🚀 **Onboarding**: Set up vault structure with templates (objectives.md, log.md, trends.md, runbook.md)

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
- Bar chart of actuals vs. goals
- Priority-sorted table (P1 → P2, then by completion %)
- Flags: ✅ (met), 🟢 (on track), 🟡 (warning), 🔴 (missed)
- Catch-up recommendations
- Offer to log and update trends

### Monthly Pacing

```
Show me the monthly pacing for April. Vault: /Users/you/Documents/Claude/vault_personal.
```

Output:
- Weekly actuals vs. monthly targets
- At-risk milestones and recovery paths

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
I want to lower my EDHEC goal from 7h to 5h. Vault: /Users/you/Documents/Claude/vault_personal.
```

Output:
- Verifies current goal
- Shows full diff across all files (objectives.md §1+§2, runbook.md, CLAUDE.md)
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
├── log.md                      ← Append-only operational log (Karpathy format)
└── CLAUDE.md                   ← Project metadata (calendars, people, milestones)
```

### objectives.md

§1 Weekly Targets, §2 Monthly Targets, §3 Quarterly Goals, §4 Project Milestones, §5 Calibration Notes.

### log.md

Dictionary format (key: value) for LLM parsing. Weekly entries:

```
## 2026-04-20 · weekly

mode: weekly
job_search_h: 10.5
job_search_pct: 105
edhec_h: 4.8
edhec_pct: 69
running_ses: 3
running_pct: 100
note: On track this week.
```

Daily entries (optional, from agenda-manager):

```
## 2026-04-17 · daily

mode: daily
changes: 1
conflicts: 1
at_risk: 0
note: Deleted duplicate Coursera block.
```

### trends.md

§ Streak Counts, § Weekly Actuals History, § Key Patterns, § Calibration History, § ⚠️ Pending Calibration Proposals.

Calibration proposals are auto-generated when a 2+ week streak is missed. You approve/reject them; time-coach applies changes if approved.

## Design Philosophy

- **Ask before writing**: time-coach never modifies files without your explicit approval
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
