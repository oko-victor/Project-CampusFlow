"""JSON persistence with validation and non-destructive load errors."""
import json
from pathlib import Path
from .tickets import category,urgency,priority
REQUIRED={"id","title","category","urgency","affected_users","priority","status","assigned_to"}
def validate_tickets(data):
    if not isinstance(data,list): raise ValueError("Expected JSON list")
    seen=set()
    for t in data:
        if not isinstance(t,dict) or set(t)!=REQUIRED: raise ValueError("Invalid ticket fields")
        key=t["id"]
        if not isinstance(key,str) or not key.startswith("T") or not key[1:].isdigit() or int(key[1:])<1 or key in seen:
            raise ValueError("Invalid or duplicate ticket ID")
        seen.add(key)
        if not isinstance(t["title"],str) or not t["title"].strip(): raise ValueError("Invalid title")
        if category(t["category"])!=t["category"] or urgency(t["urgency"])!=t["urgency"]:
            raise ValueError("Invalid category or urgency format")
        if priority(t["urgency"],t["affected_users"])!=t["priority"]: raise ValueError("Invalid priority")
        if t["status"] not in ("open","in_progress","resolved"): raise ValueError("Invalid status")
        name=t["assigned_to"]
        if name is not None and (not isinstance(name,str) or not name.strip()): raise ValueError("Invalid assignee")
        if t["status"]!="open" and name is None: raise ValueError("Missing assignee")
    return data
def load_tickets(path):
    path=Path(path)
    if not path.exists(): return []
    try:
        with path.open(encoding="utf-8") as stream: value=json.load(stream)
    except (OSError,json.JSONDecodeError) as exc: raise ValueError(f"Cannot load ticket file: {exc}") from exc
    return validate_tickets(value)
def save_tickets(path,tickets):
    validate_tickets(tickets)
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    temp=path.with_suffix(path.suffix+".tmp")
    with temp.open("w",encoding="utf-8") as stream: json.dump(tickets,stream,indent=2)
    temp.replace(path)
