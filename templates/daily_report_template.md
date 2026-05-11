---
template: true
for: MODE B (Daily Sync)
date: [YYYY-MM-DD]
---

# Daily Sync: [DAY_OF_WEEK], [MONTH_DATE, YEAR]

---

## § Changes Made

**Summary:** [N] changes · [N] conflicts resolved · pace on track

### Calendar Actions

- **Created:** [Activity] [Time] ([Duration], reason if catch-up)
- **Moved:** [Activity] [Old Time] → [New Time] (reason: [conflict with X, buffer violation, etc.])
- **Deleted:** [Activity] [Time] (reason: met weekly goal early, conflicts)
- **Merged:** [Activity 1] + [Activity 2] → single [Duration] block (efficiency)

**Example:**
```
- Created: 💼 Job Search Mon 11:15–13:15 (2h catch-up: +1.5h this week)
- Moved: 🎓 EDHEC Wed 17:00–19:00 → 15:00–17:00 (conflict with Runna post-buffer 17:00–17:45)
- Deleted: 🌐 PROJ2-Bancos Thu (weekly goal already met Wed)
- Merged: Two 1h CFA blocks → single 2h block Sat morning (flow efficiency)
```

---

## § Actual Progress (Today So Far)

| Activity | Actual | Goal | % | Status |
|----------|--------|------|-------|--------|
| 💼 Job Search | [Xh] | [Today goal] | [Z%] | [✅/🟡/🔴] |
| 🎓 EDHEC | [Xh] | [Today goal] | [Z%] | [✅/🟡/🔴] |
| 📊 CFA | [Xh] | [Today goal] | [Z%] | [✅/🟡/🔴] |
| Other | [cumulative] | — | — | — |

---

## § Weekly Horizon (Current Status)

**Progress toward weekly goals (today's run)**

| Activity | This Week Actual | Weekly Goal | % | Days Left | Daily Pace Needed |
|----------|---------|---------|-------|-----------|-------------------|
| 💼 Job Search | [Xh] | [Yh] | [Z%] | [N] | [Z h/day] |
| 🎓 EDHEC | [Xh] | [Yh] | [Z%] | [N] | [Z h/day] |
| 📊 CFA | [Xh] | [Yh] | [Z%] | [N] | [Z h/day] |

**Pace assessment:** On track · 🟢 (or needs acceleration · 🟡)

---

## § At-Risk Activities

**Any activities projected to miss weekly goal by end of week?**

- [ ] None detected
- [ ] [Activity name] — [Xh] actual vs. [Yh] goal · [Zd] days left · needs [Z h/day]

**Recommendation:** If at-risk, add recovery block [date/time] to catch up.

---

## § Conflicts Detected & Resolved

**Summary:** [N] conflicts found and resolved

### Immovable Conflict Check
- **P0 ↔ Personal:** [None | flagged for review]
- **Runna buffer violations:** [None | resolved]

### Regular Conflicts
- **Before:** [Conflict 1] ([Time overlap])
- **Action:** [MOVE/TRIM description]
- **After:** [No conflict; blocks non-overlapping]

**Example:**
```
- Conflict: 💼 Job Search 12:00–13:00 ↔ 🏃 Runna 12:30–13:15 (buffer violation)
- Action: Moved JS to 11:15–13:15 (non-overlapping, pre-Runna only)
- Result: Runna session 12:30–13:15 + 45-min post-buffer = free after 14:00
```

---

## § Optimization Notes

**Any observations for next MODE A run?**

- Low-utilization windows: [Time ranges underutilized]
- High-utilization windows: [Time ranges squeezed]
- Buffer efficiency: [Any buffers that could be tightened/expanded?]
- Activity clustering: [Opportunities to batch similar work?]

---

## § Outlook

**Pace check:** [1–2 sentences on today's projected contribution to weekly goals]

**Example:**  
"Strong start — Job Search block scheduled catch-up (+1.5h), EDHEC on track, Meditation confirmed. Runna session tomorrow; accounting 45-min recovery buffer. Weekly pace: JS 3/6h (50%), EDH 3/8h (38%) — both green, CFA 1/6h (17%) — catch-up block needed Wed or Thu."

---

**Generated:** [TIME by time-coach agent]  
**Mode:** MODE B (Daily Sync)  
**Log entry:** Update `/log.md` with one-line summary after report
