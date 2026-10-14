"""Ticket validation, creation and priority calculation."""
CATEGORIES={"network":"Network","hardware":"Hardware","software":"Software","other":"Other"}
URGENCIES={"low","medium","high"}
def category(value):
    if not isinstance(value,str) or value.strip().lower() not in CATEGORIES: raise ValueError("Invalid category")
    return CATEGORIES[value.strip().lower()]
def urgency(value):
    if not isinstance(value,str) or value.strip().lower() not in URGENCIES: raise ValueError("Invalid urgency")
    return value.strip().lower()
def priority(level,users):
    level=urgency(level)
    if type(users) is not int or users<=0: raise ValueError("Affected users must be a positive integer")
    if level=="high" and users>=10: return "critical"
    if level=="high" or users>=10: return "high"
    if level=="medium" or users>=3: return "medium"
    return "low"
def find_ticket(tickets,ticket_id):
    for ticket in tickets:
        if ticket["id"]==ticket_id: return ticket
    raise ValueError("Unknown ticket ID")
def create_ticket(tickets,title,kind,level,users):
    if not isinstance(title,str) or not title.strip(): raise ValueError("Title must not be empty")
    kind=category(kind); level=urgency(level); rank=priority(level,users)
    number=max((int(t["id"][1:]) for t in tickets),default=0)+1
    ticket={"id":f"T{number:03d}","title":title.strip(),"category":kind,"urgency":level,
            "affected_users":users,"priority":rank,"status":"open","assigned_to":None}
    tickets.append(ticket)
    return ticket
