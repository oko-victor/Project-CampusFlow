"""Assignment and lifecycle rules (Engineer B work area)."""
from .tickets import find_ticket
def assign_ticket(tickets,ticket_id,staff):
    ticket=find_ticket(tickets,ticket_id)
    if ticket["status"]=="resolved": raise ValueError("Reopen resolved ticket first")
    if not isinstance(staff,str) or not staff.strip(): raise ValueError("Staff name required")
    ticket["assigned_to"]=staff.strip()
    return ticket
def change_status(tickets,ticket_id,status):
    ticket=find_ticket(tickets,ticket_id)
    if not isinstance(status,str): raise ValueError("Invalid status")
    status=status.strip().lower()
    allowed={"open":{"in_progress"},"in_progress":{"resolved"},"resolved":{"open"}}
    if status not in allowed[ticket["status"]]: raise ValueError("Illegal status transition")
    if status=="in_progress" and not ticket["assigned_to"]: raise ValueError("Assign the ticket first")
    ticket["status"]=status
    return ticket
