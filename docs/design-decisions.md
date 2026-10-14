# Design decisions (initial draft)

- Tickets are stored in a list of dictionaries; functions accept the collection as an explicit parameter.
- Each ticket has id, title, category, urgency, affected_users, priority, status, assigned_to.
- Business functions raise ValueError on invalid requests; CLI catches and explains errors.
- Validation happens before mutation.
- IDs use maximum existing numeric ID plus one, so reload does not repeat IDs.
- JSON data is a list, and storage validates every entry before accepting a load.
- Interactive input and printing belong in main.py, not the business functions.
- Engineer A owns ticket creation and priority; Engineer B owns lifecycle, queue and reports.
- Both engineers must confirm these contracts and make independently attributable changes before submission.
