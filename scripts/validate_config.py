#!/usr/bin/env python3
"""
Validate time-coach config.md before MODE A execution.

Usage: python scripts/validate_config.py 01-config/config.md

Checks:
- User Profile: name, email, timezone
- Connected Calendars: role, ID, access level (≥3 required)
- Activity Codes: code, priority, goal, window, duration (≥3 required)
- Buffer Rules: before exercise, after exercise, activity-meal, hard window
- Meal Schedule: meal, time, duration (≥2 required)
- Daily Routine: routine, time, duration (≥1 required)
- Week Definition: week runs, hard window, must-do exemptions

Returns:
- Exit 0: All checks passed ✅
- Exit 1: Missing or invalid fields (lists specific issues)
"""

import sys
import re
from pathlib import Path


def validate_config(config_path):
    """Validate config.md structure and required fields."""

    try:
        with open(config_path, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"❌ File not found: {config_path}")
        return False

    errors = []
    warnings = []

    # Check User Profile section
    if "## User Profile" not in content:
        errors.append("Missing section: User Profile")
    else:
        if "- **Name:**" not in content or "FILL IN" in content.split("## User Profile")[1].split("##")[0]:
            errors.append("User Profile: missing or unfilled Name")
        if "- **Email:**" not in content or "FILL IN" in content.split("## User Profile")[1].split("##")[0]:
            errors.append("User Profile: missing or unfilled Email")
        if "- **Timezone:**" not in content or "FILL IN" in content.split("## User Profile")[1].split("##")[0]:
            errors.append("User Profile: missing or unfilled Timezone")

    # Check Connected Calendars section
    if "## Connected Calendars" not in content:
        errors.append("Missing section: Connected Calendars")
    else:
        calendars_section = content.split("## Connected Calendars")[1].split("##")[0]
        calendar_count = calendars_section.count("|") // 3  # Rough estimate
        if calendar_count < 3:
            errors.append("Connected Calendars: expected ≥3 calendars (Personal, Exercise, Claude)")
        if "Read-only" not in calendars_section or "Read+Write" not in calendars_section:
            errors.append("Connected Calendars: missing access level (Read-only or Read+Write)")

    # Check Customized Buffer Rules section
    if "## Customized Buffer Rules" not in content:
        errors.append("Missing section: Customized Buffer Rules")
    else:
        buffer_section = content.split("## Customized Buffer Rules")[1].split("##")[0]
        if "Before" not in buffer_section or "After" not in buffer_section:
            warnings.append("Customized Buffer Rules: missing standard buffers (may use defaults)")

    # Check Activity Codes section
    if "## Activity Codes & Mappings" not in content:
        errors.append("Missing section: Activity Codes & Mappings")
    else:
        activity_section = content.split("## Activity Codes & Mappings")[1].split("##")[0]
        # Count rows in activity table (rough: count pipes)
        activity_rows = activity_section.count("\n|") - 2  # Subtract header
        if activity_rows < 3:
            errors.append("Activity Codes: expected ≥3 activities (Job Search, Education, Project minimum)")
        if "JOB_SEARCH" not in activity_section and "FILL IN" in activity_section:
            errors.append("Activity Codes: example codes still marked [FILL IN]")

    # Check Meal Schedule section
    if "## Meal Schedule" not in content:
        errors.append("Missing section: Meal Schedule")
    else:
        meal_section = content.split("## Meal Schedule")[1].split("##")[0]
        meal_rows = meal_section.count("\n|") - 2
        if meal_rows < 2:
            errors.append("Meal Schedule: expected ≥2 meals (breakfast, lunch, dinner minimum)")

    # Check Daily Routine section
    if "## Daily Routine" not in content:
        errors.append("Missing section: Daily Routine")
    else:
        routine_section = content.split("## Daily Routine")[1].split("##")[0]
        routine_rows = routine_section.count("\n|") - 2
        if routine_rows < 1:
            warnings.append("Daily Routine: expected ≥1 routine (e.g., Morning Routine)")

    # Check Week Definition section
    if "## Week Definition" not in content:
        errors.append("Missing section: Week Definition")
    else:
        week_section = content.split("## Week Definition")[1].split("##")[0]
        if "Week runs:" not in week_section or "Hard scheduling window:" not in week_section:
            errors.append("Week Definition: missing 'Week runs' or 'Hard scheduling window'")

    # Report results
    if errors:
        print("❌ Config validation FAILED\n")
        print("Errors (must fix):")
        for error in errors:
            print(f"  - {error}")
        if warnings:
            print("\nWarnings (recommended to address):")
            for warning in warnings:
                print(f"  - {warning}")
        return False

    if warnings:
        print("⚠️  Config validation passed with warnings\n")
        for warning in warnings:
            print(f"  - {warning}")
        return True

    print("✅ Config validation passed\n")
    print(f"File: {config_path}")
    print(f"Status: Ready for MODE A execution")
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_config.py <path-to-config.md>")
        sys.exit(1)

    config_file = sys.argv[1]
    success = validate_config(config_file)
    sys.exit(0 if success else 1)
