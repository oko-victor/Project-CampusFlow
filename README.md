# CampusFlow

A Python command-line helpdesk for tracking campus support tickets.

## Run
```bash
python main.py
```

## Test
```bash
python -m unittest discover -s tests -v
```

## Features
Create, list and view tickets; assign staff; enforce open → in_progress → resolved and explicit reopen; open-only priority queue; status and priority reports; JSON persistence.

## Priority
high + at least 10 users → critical; high OR at least 10 → high; medium OR at least 3 → medium; otherwise low. First matching rule wins.

## Storage
A JSON list of ticket dictionaries is stored at `data/tickets.json`. This runtime file is ignored by Git. Missing storage starts with no tickets; corrupted storage halts startup without overwriting data.

## Team workflow
Engineer A: `campusflow/tickets.py` and `tests/test_tickets.py`.
Engineer B: `campusflow/workflow.py`, `campusflow/reports.py`, `tests/test_workflow.py`.
Storage and CLI are shared integration components. Code on this branch is AI-generated scaffolding to inspect, improve, and verify; it does not substitute for independent teammate contributions.

## Limitations
Single-user CLI; no concurrent write support or authentication. No GUI or external packages.
