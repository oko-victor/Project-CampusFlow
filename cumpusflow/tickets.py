"""Ticket fields, validation, priority rules, and creating/finding tickets."""

CATEGORIES = ["Network", "Hardware", "Software", "Other"]
URGENCIES = ["low", "medium", "high"]
PRIORITIES = ["critical", "high", "medium", "low"]   # queue order
STATUSES = ["open", "in_progress", "resolved"]
FIELDS = ["id", "title", "category", "urgency", "affected_users",
          "priority", "status", "assigned_to"]


# ---------- Validation ----------

def clean_choice(value, options, label):
    """Match input to one of the options, ignoring case and extra spaces."""
    for option in options:
        if str(value).strip().lower() == option.lower():
            return option
    raise ValueError(f"Invalid {label} '{value}'. Choose from: {', '.join(options)}.")


def clean_title(value):
    if not str(value).strip():
        raise ValueError("Title must not be blank.")
    return str(value).strip()


def clean_users(value):
    text = str(value).strip()
    if not (text.isascii() and text.isdigit()) or int(text) < 1:
        raise ValueError(f"Affected users must be a positive whole number (got '{value}').")
    return int(text)


# ---------- Priority (checked in order, first match wins) ----------

def calculate_priority(urgency, affected_users):
    if urgency == "high" and affected_users >= 10:
        return "critical"
    if urgency == "high" or affected_users >= 10:
        return "high"
    if urgency == "medium" or affected_users >= 3:
        return "medium"
    return "low"


# ---------- Ticket operations ----------

def create_ticket(tickets, title, category, urgency, users):
    title = clean_title(title)
    category = clean_choice(category, CATEGORIES, "category")
    urgency = clean_choice(urgency, URGENCIES, "urgency")
    users = clean_users(users)

    last_number = max((int(t["id"][1:]) for t in tickets), default=0)
    ticket = {
        "id": f"T{last_number + 1:03d}",
        "title": title,
        "category": category,
        "urgency": urgency,
        "affected_users": users,
        "priority": calculate_priority(urgency, users),
        "status": "open",
        "assigned_to": None,
    }
    tickets.append(ticket)
    return ticket


def find_ticket(tickets, ticket_id):
    for ticket in tickets:
        if ticket["id"] == str(ticket_id).strip().upper():
            return ticket
    raise ValueError(f"Unknown ticket ID '{ticket_id}'.")
