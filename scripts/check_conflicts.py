#!/usr/bin/env python3
"""
Detect calendar conflicts before MODE A calendar writes.

This is a pre-flight check that runs BEFORE creating any calendar blocks.
Prevents the April 27 bug where immovable conflicts were silently created.

Usage: python scripts/check_conflicts.py --personal CALENDAR_ID --claude CALENDAR_ID --runna CALENDAR_ID --start 2026-05-05 --end 2026-05-11

Note: This script is a template. Full implementation requires Google Calendar API integration
and credential setup. For now, it serves as documentation of the conflict detection algorithm.

Algorithm:
1. FETCH all three calendars for target week date range
2. Group events by date
3. For each date, sort events by priority (P0 > Personal/Runna > P1 > P2)
4. Check for overlaps between immovable blocks (P0 ↔ Personal/Runna)
5. If found: FLAG for user review (do NOT proceed)
6. If none: Continue to MODE A calendar creation

Conflict hierarchy (can override):
- P0 (meals, routines) > Personal > Runna > P1 (job search, education) > P2 (projects, habits)
"""

import sys
from datetime import datetime, timedelta
from typing import List, Dict


class Conflict:
    """Represents a calendar conflict."""

    def __init__(self, source1: str, source2: str, time_range: str, severity: str, action: str):
        self.source1 = source1
        self.source2 = source2
        self.time_range = time_range
        self.severity = severity  # "CRITICAL" | "HIGH" | "LOW"
        self.action = action  # "TRIM" | "MOVE" | "FLAG" | "ESCALATE"

    def __repr__(self):
        return (
            f"Conflict({self.source1} ↔ {self.source2} @ {self.time_range} "
            f"| severity={self.severity} | action={self.action})"
        )


def check_conflicts(personal_events: List[Dict], claude_events: List[Dict], runna_events: List[Dict],
                    week_start: str, week_end: str) -> List[Conflict]:
    """
    Detect immovable conflicts before calendar writes.

    Args:
        personal_events: Events from Personal calendar (read-only)
        claude_events: Events from Claude calendar (read+write)
        runna_events: Events from Runna calendar (read-only)
        week_start: ISO 8601 date (e.g., 2026-05-05)
        week_end: ISO 8601 date (e.g., 2026-05-11)

    Returns:
        List of Conflict objects with severity and recommended action.
    """

    conflicts = []

    # Priority hierarchy
    priority_map = {
        "P0": 4,  # Meals, Morning Routine, Tareas del hogar
        "Personal": 3,  # Personal calendar events (immovable)
        "Runna": 3,  # Running/exercise sessions (immovable)
        "P1": 2,  # Job Search, EDHEC, CFA
        "P2": 1,  # Projects, habits
    }

    # Conflict resolution rules
    # P0 ↔ Personal/Runna → ESCALATE (ask user)
    # P1 ↔ Personal/Runna → MOVE or TRIM P1
    # P2 ↔ anything → MOVE or DELETE P2

    # Step 1: Group events by date
    event_groups = {}
    for event in personal_events + claude_events + runna_events:
        date_key = event.get("date")  # ISO format YYYY-MM-DD
        if date_key not in event_groups:
            event_groups[date_key] = []
        event_groups[date_key].append(event)

    # Step 2: For each date, detect overlaps
    for date_key, events in sorted(event_groups.items()):
        if not (week_start <= date_key <= week_end):
            continue  # Outside target week

        # Sort by priority (highest first)
        sorted_events = sorted(
            events,
            key=lambda e: priority_map.get(e.get("priority", "P2"), 0),
            reverse=True
        )

        # Check pairwise for overlaps
        for i in range(len(sorted_events)):
            for j in range(i + 1, len(sorted_events)):
                e1, e2 = sorted_events[i], sorted_events[j]

                # Check if time ranges overlap
                if _time_overlap(e1.get("start_time"), e1.get("end_time"),
                                e2.get("start_time"), e2.get("end_time")):

                    source1 = e1.get("source", "Unknown")  # e.g., "P0", "Personal", "Runna"
                    source2 = e2.get("source", "Unknown")

                    # Determine severity and action
                    if source1 == "P0" and source2 in ["Personal", "Runna"]:
                        severity = "CRITICAL"
                        action = "ESCALATE"  # Ask user; don't proceed
                    elif source1 in ["Personal", "Runna"] and source2 == "P0":
                        severity = "CRITICAL"
                        action = "ESCALATE"
                    elif source1 in ["Personal", "Runna"] and source2 == "P1":
                        severity = "HIGH"
                        action = "MOVE"  # Move P1 block
                    elif source1 == "P1" and source2 in ["Personal", "Runna"]:
                        severity = "HIGH"
                        action = "MOVE"
                    else:
                        severity = "LOW"
                        action = "TRIM"  # Trim or delete lower-priority block

                    time_range = f"{e1.get('start_time')}–{e1.get('end_time')}"
                    conflicts.append(Conflict(source1, source2, time_range, severity, action))

    return conflicts


def _time_overlap(start1: str, end1: str, start2: str, end2: str) -> bool:
    """Check if two time ranges overlap (HH:MM format)."""
    try:
        t1_start = datetime.strptime(start1, "%H:%M").time()
        t1_end = datetime.strptime(end1, "%H:%M").time()
        t2_start = datetime.strptime(start2, "%H:%M").time()
        t2_end = datetime.strptime(end2, "%H:%M").time()
        return not (t1_end <= t2_start or t2_end <= t1_start)
    except (ValueError, TypeError):
        return False


def report_conflicts(conflicts: List[Conflict], action_threshold: str = "ESCALATE") -> bool:
    """
    Report conflicts and determine if MODE A should proceed.

    Args:
        conflicts: List of Conflict objects
        action_threshold: Only stop if action >= this level ("ESCALATE" > "MOVE" > "TRIM")

    Returns:
        True if safe to proceed; False if critical conflicts require user review.
    """

    if not conflicts:
        print("✅ No conflicts detected. Safe to proceed with MODE A calendar creation.")
        return True

    escalate_conflicts = [c for c in conflicts if c.action == "ESCALATE"]
    high_conflicts = [c for c in conflicts if c.action == "MOVE"]
    low_conflicts = [c for c in conflicts if c.action == "TRIM"]

    if escalate_conflicts:
        print("⚠️  CRITICAL CONFLICTS DETECTED — Immovable blocks overlap\n")
        for conflict in escalate_conflicts:
            print(f"  {conflict.source1} ↔ {conflict.source2} @ {conflict.time_range}")
        print("\n❌ Cannot proceed with MODE A. User review required.\n")
        print("Options:")
        print("  1. Adjust Personal calendar event (if flexible)")
        print("  2. Adjust P0 meal window (if possible)")
        print("  3. Skip this conflict for now (manual resolution)")
        return False

    if high_conflicts:
        print("⚠️  High-priority conflicts detected — P1 overlaps with Personal/Runna\n")
        for conflict in high_conflicts:
            print(f"  {conflict.source1} ↔ {conflict.source2} @ {conflict.time_range}")
        print("\n⏸️  MODE A can proceed, but these P1 blocks will be moved or trimmed.")

    if low_conflicts:
        print("ℹ️  Low-priority conflicts detected — P2 can be moved\n")
        for conflict in low_conflicts:
            print(f"  {conflict.source1} ↔ {conflict.source2} @ {conflict.time_range}")

    return True


if __name__ == "__main__":
    # Placeholder: Full implementation requires Google Calendar API
    print("Conflict detection script loaded.\n")
    print("Current mode: Template (documentation only)")
    print("To enable: integrate Google Calendar API and OAuth credentials\n")
    print("Algorithm summary:")
    print("  1. FETCH Personal + Claude + Runna calendars")
    print("  2. Group events by date")
    print("  3. Check for overlaps (P0 ↔ Personal/Runna = CRITICAL)")
    print("  4. Report conflicts with recommended actions")
    print("  5. Return True/False to proceed with MODE A")
