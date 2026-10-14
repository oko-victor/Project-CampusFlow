"""Open work queue and status/priority reporting (Engineer B work area)."""
from collections import Counter
PRIORITIES=("critical","high","medium","low")
STATUSES=("open","in_progress","resolved")
def work_queue(tickets):
    return sorted((t for t in tickets if t["status"]=="open"),
                  key=lambda t:(PRIORITIES.index(t["priority"]),int(t["id"][1:])))
def report(tickets):
    statuses=Counter(t["status"] for t in tickets)
    priorities=Counter(t["priority"] for t in tickets)
    return {"total":len(tickets),"by_status":{s:statuses[s] for s in STATUSES},
            "by_priority":{p:priorities[p] for p in PRIORITIES}}
