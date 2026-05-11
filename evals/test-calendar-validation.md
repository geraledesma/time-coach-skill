# Eval: Calendar Assignment & Week Boundary Validation

## Scenario 1: Wrong calendar in runbook
**Setup:** Create a runbook.md with write calendar ID pointing to a read-only calendar.
**Action:** Run "calendar write" for next week.
**Expected:** Error message, no events created, clear instructions to fix the calendar.
**Pass if:** User gets actionable error, not a cryptic MCP error.

## Scenario 2: Week boundary on Tuesday
**Setup:** User requests "May 12 week" (May 12 is Tuesday).
**Action:** Skill detects start date from request.
**Expected:** Clarification prompt: "Did you mean May 11–17?"
**Pass if:** Blocks are NOT created until user confirms Monday start.

## Scenario 3: Happy path with all guards
**Setup:** Correct write calendar + Monday start date.
**Action:** Run "calendar write" for May 11.
**Expected:** Blocks created for May 11–17 (Mon–Sun) on the write calendar.
**Pass if:** Exactly 7 days of blocks created, all on write calendar, no personal calendar touched.

## Scenario 4: Auto-detect next week
**Setup:** Run "calendar write" without specifying a week.
**Action:** Today is Wed, May 8. Skill should pick May 11–17.
**Expected:** Confirmation: "Planning for week of May 11 (Monday) through May 17 (Sunday)?"
**Pass if:** Correct week auto-detected, user confirms.
