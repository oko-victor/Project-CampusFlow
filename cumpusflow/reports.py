"""Ticket counts for the reports screen."""

from campusflow.tickets import PRIORITIES, STATUSES


def report(tickets):
    return {
        "total": len(tickets),
        "status": {s: sum(t["status"] == s for t in tickets) for s in STATUSES},
        "priority": {p: sum(t["priority"] == p for t in tickets) for p in PRIORITIES},
    }
