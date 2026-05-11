#!/usr/bin/env python3
"""
filter_gcal.py — Compact a raw list_events JSON response to the 5 fields time-coach needs.

Usage:
    echo '<raw_json>' | python3 filter_gcal.py
    python3 filter_gcal.py < raw_response.json

Why: a raw list_events response for 45 events keeps ~15 fields per event in context
(htmlLink, organizer, creator, eventType, transparency, updated, created, status, etc.)
None of those are needed for scheduling. This filter cuts token cost ~3x per fetch.

Output fields: id, summary, start, end, color
"""
import json
import sys


def compact_events(raw: dict) -> list[dict]:
    events = raw.get("events", [])
    out = []
    for e in events:
        start = e.get("start", {})
        end   = e.get("end",   {})
        out.append({
            "id":      e.get("id"),
            "summary": e.get("summary", ""),
            "start":   start.get("dateTime") or start.get("date"),
            "end":     end.get("dateTime")   or end.get("date"),
            "color":   e.get("colorId"),
        })
    # Sort by start time
    out.sort(key=lambda x: x["start"] or "")
    return out


def main():
    raw = json.load(sys.stdin)
    compact = compact_events(raw)
    print(json.dumps(compact, indent=2, ensure_ascii=False))
    # Summary to stderr (doesn't pollute piped output)
    print(f"\n✓ {len(compact)} events · fields kept: id, summary, start, end, color", file=sys.stderr)


if __name__ == "__main__":
    main()
