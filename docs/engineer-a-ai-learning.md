# Engineer A — AI learning evidence and verification checklist

This document records **AI-assisted work performed in this conversation** and links to actual GitHub changes. It is **not** a claim that Engineer A personally performed experiments, independently authored the AI-generated code, or demonstrated understanding. Engineer A must add personal reflections and verification results in their own words before submission. The shared `docs/ai-learning-log.md` is being edited in Engineer B's separate PR #6; integrate both sets of entries after review rather than overwriting the partner's work.

## Interaction 1 — Positive integer validation and Python booleans

- **Engineering need:** Reject zero, negative values, decimal values, and booleans in `affected_users`.
- **Actual AI-assisted request/context:** The CampusFlow assessment explicitly required strict integer validation; the user instructed the assistant to rebuild CampusFlow using the assessment and work directly in GitHub. No separate focused conceptual question from Engineer A is recorded.
- **AI explanation/design:** `isinstance(True, int)` evaluates to `True` in Python, so `type(users) is int` is appropriate here when a boolean must be rejected.
- **Small unrelated experiment executed by AI in the development environment:**
  - Expression: `isinstance(True, int), type(True) is int`
  - Observed result: `(True, False)`.
  - This was **AI-executed**, not independently run by Engineer A.
- **Applied change/evidence:** `campusflow/tickets.py` checks `type(users) is not int or users <= 0`; `tests/test_tickets.py` includes `test_bool_users` and a full-state invalid-create test. See commit [42a4e8d](https://github.com/oko-victor/Project-CampusFlow/commit/42a4e8d00beb192eea7d07c4790f3b930eaff857).
- **Independent verification available:** [GitHub Actions passing run](https://github.com/oko-victor/Project-CampusFlow/actions/runs/38648882484). CI is not a personal experiment.
- **Decision:** Preserve strict type checking rather than accepting booleans as user counts.
- **Engineer A personal experiment and observation:** **TO COMPLETE personally** (record actual command/code, prediction, output and what it taught you).

## Interaction 2 — Ordered priority rules and boundary testing

- **Engineering need:** Priority depends on the **first matching** rule; high urgency plus at least 10 users must be critical before the broader high-priority condition is considered.
- **Actual AI-assisted request/context:** The user requested the original assessment implemented; no separate focused conceptual learning question from Engineer A was recorded.
- **AI explanation/design:** Ordered `if` statements with early returns encode precedence unambiguously.
- **Project checks:** `test_priority_precedence_at_ten_users` asserts: `priority("low", 10) == "high"`, `priority("medium", 10) == "high"`, and `priority("high", 10) == "critical"`.
- **Small unrelated experiment:** **NOT YET RUN by Engineer A.** Suggested exercise: classify book requests by two ordered rules (e.g., urgent + many readers before urgent OR many readers), predict boundary results, run and record actual results.
- **Applied change/evidence:** `campusflow/tickets.py`, `tests/test_tickets.py`, [commit 42a4e8d](https://github.com/oko-victor/Project-CampusFlow/commit/42a4e8d00beb192eea7d07c4790f3b930eaff857); [passing CI run](https://github.com/oko-victor/Project-CampusFlow/actions/runs/38648882484).
- **Decision:** Keep the critical condition first and test the 10-user boundary rather than only ordinary examples.
- **Engineer A personal question, experiment and observation:** **TO COMPLETE personally**.

## Interaction 3 — Verify no mutation after rejected input

- **Engineering need:** Rejecting an invalid ticket creation must leave the entire ticket collection unchanged.
- **Actual AI-assisted request/context:** A previous AI review discussed full-state checks; Engineer A's feature tests were subsequently strengthened. The user did not independently pose a focused concept question in this conversation.
- **AI explanation/design:** Capture a deep copy of the original list, expect `ValueError`, and compare the entire structure after rejection. This detects more unintended changes than checking just one field.
- **Small unrelated experiment executed by AI:** AI created a sample library list, made a `deepcopy`, rejected a hypothetical change with `ValueError` before mutation, and observed `items == snapshot` as `True`. This confirms only the *example's* behavior; it does not prove all invalid CampusFlow cases.
- **Applied change/evidence:** `test_invalid_creation_never_mutates_existing_tickets` covers blank titles, invalid category/urgency, negative users, floats, and bools while checking full-list equality. [Commit 42a4e8d](https://github.com/oko-victor/Project-CampusFlow/commit/42a4e8d00beb192eea7d07c4790f3b930eaff857), [passing CI](https://github.com/oko-victor/Project-CampusFlow/actions/runs/38648882484).
- **Critical evaluation:** A status-only or assignee-only assertion is weaker than a complete snapshot comparison. The same principle was reviewed in Engineer B's PR #6.
- **Decision:** Strengthen Engineer A's invalid-input regression tests to compare all ticket data.
- **Engineer A personal experiment and observation:** **TO COMPLETE personally** (preferably try an unrelated library-book example, predict the result, record actual output).

## Audit completion checklist

- [ ] Engineer A confirms these discussions reflect what they actually learned.
- [ ] Engineer A adds the *exact* learning questions actually asked (if none were asked, conduct three real focused learning questions now and record them rather than inventing past prompts).
- [ ] Engineer A runs/inspects a small unrelated experiment for each topic and records predictions/results.
- [ ] Engineer A explains one recommendation independently improved or rejected and why.
- [ ] Engineer B completes personal verification in their PR #6 learning entries.
- [ ] The final integrated `docs/ai-learning-log.md` includes both engineers' authentic records before merge into `main`.


## Additional AI-executed demonstration results (2026-10-14)

These three demonstrations were **actually executed by the ChatGPT assistant** using Python. They are reproducible evidence of the examples, **not personal verification by Engineer A**, and should not be described as such during the audit.

1. **Boolean type check (unrelated Python experiment):** Evaluated `isinstance(True, int), type(True) is int`. Actual output: `True False`. This shows why plain `isinstance(x, int)` includes booleans, while exact-type checks do not.
2. **Ordered classification (unrelated book-request example):** Used a separate `label(level, people)` function with a first rule `urgent AND people >= 10 → critical`, followed by `urgent OR people >= 10 → high`. Actual output: `('urgent', 10) → critical; ('urgent', 2) → high; ('normal', 10) → high`. This demonstrates priority-rule precedence.
3. **No-mutation rejection (unrelated book-library example):** A sample `books=[{'title':'Math','copies':2}]` was deep-copied. A request for zero copies raised `ValueError('positive copies required')` before the assignment. Actual output: `positive copies required unchanged: True`.

**Engineer A still needs to:** personally inspect or rerun these examples, predict the results, explain the code, record their own observations and exact learning questions, and confirm the log before it is treated as individual learning evidence.
