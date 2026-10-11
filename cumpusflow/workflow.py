"""Assigning tickets, moving them through the workflow, and the work queue."""

from campusflow.tickets import PRIORITIES, find_ticket

# Allowed workflow moves: current status -> the one status it may move to.
NEXT_STATUS = {"open": "in_progress", "in_progress": "resolved", "resolved": "open"}


def assign_ticket(tickets, ticket_id, name):
    ticket = find_ticket(tickets, ticket_id)
    if not str(name).strip():
        raise ValueError("Staff member name must not be blank.")
    if ticket["status"] == "resolved":
        raise ValueError(f"{ticket['id']} is resolved. Reopen it before changing it.")
    ticket["assigned_to"] = str(name).strip()
    return ticket


def change_status(tickets, ticket_id, new_status):
    ticket = find_ticket(tickets, ticket_id)
    current = ticket["status"]
    if NEXT_STATUS[current] != new_status:
        raise ValueError(f"{ticket['id']} is '{current}'; it can only move to "
                         f"'{NEXT_STATUS[current]}'.")
    if new_status == "in_progress" and not ticket["assigned_to"]:
        raise ValueError(f"{ticket['id']} is unassigned. Assign it before starting work.")
    ticket["status"] = new_status
    return ticket


def work_queue(tickets):
    """Unresolved tickets, critical first; ties go to the lower ticket number."""
    pending = [t for t in tickets if t["status"] != "resolved"]
    return sorted(pending, key=lambda t: (PRIORITIES.index(t["priority"]),
                                          int(t["id"][1:])))
