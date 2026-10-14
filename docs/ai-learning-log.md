# AI learning log

This log records actual AI-assisted engineering discussions and traceable code/review evidence. **Human learning and personally run experiments must be confirmed by the respective engineer; automated checks are identified as CI rather than personal experiments.** Do not treat this document alone as proof of individual understanding.

## Engineer A — entries to be completed by Engineer A

Engineer A will add three genuine interactions, actual questions, personal verification, outputs, and decisions. Engineer B has intentionally not invented Engineer A's learning evidence.

## Engineer B — Interaction 1: testing numeric ticket IDs

- What I needed to understand: Why sorting ticket IDs as text can appear correct for T001–T005 but fail for T010.
- Actual AI-assisted task/discussion: Create regression tests for queue priority ordering and numeric ticket ID tie-breaking; subsequent GitHub review asked for T002 and T010 with equal priorities.
- AI explanation / reasoning used: Lexicographic comparison compares characters; a numeric tie-break extracts the integer suffix so ticket 2 sorts before ticket 10.
- Verification performed in the project: Revised the test to create T001–T010 at equal priority, reverse the input, assert numeric order, and explicitly assert T002 precedes T010.
- Actual output / reference: `tests/test_engineer_b.py::test_queue_priority_and_numeric_id_tie_break`; commit `a6867e4`; PR #6 follow-up review confirms the corrected test and passing GitHub Actions run https://github.com/oko-victor/Project-CampusFlow/actions/runs/38649092190.
- Decision: Improved the original AI-assisted test because T001–T005 alone would not detect a lexical-sort bug.
- What this demonstrates: A regression test must include a case that fails for the plausible incorrect implementation.
- Personal experiment: **Not recorded as run locally by Engineer B**. Engineer B must personally run or inspect the test and record what happened before claiming personal verification.

## Engineer B — Interaction 2: rejected operations and atomic state

- What I needed to understand: Why checking only a ticket's status or assignee is insufficient to prove a failed operation has no side effects.
- Actual AI-assisted task/discussion: Add tests for invalid assignment, illegal status changes, and lifecycle restrictions; Engineer A's review requested whole-collection checks with `copy.deepcopy()`.
- AI explanation / reasoning used: A deep copy captures nested ticket dictionaries before an operation; comparing the entire list after an expected `ValueError` detects unintended changes to other fields or tickets.
- Verification performed in the project: Updated invalid-assignee, illegal-transition, unassigned-progress, and resolved-reassignment tests to compare `self.tickets` with a deep-copy snapshot.
- Actual output / reference: `tests/test_engineer_b.py`, commit `a6867e4`; PR #6 follow-up review confirms full-collection assertions; CI run linked above passed.
- Decision: Improved the earlier narrower assertions after review feedback.
- What this demonstrates: Tests for rejected operations should verify both the exception and unchanged complete state.
- Personal experiment: **Not recorded as run locally by Engineer B**. Engineer B must personally execute/review the test and add their own observed result.

## Engineer B — Interaction 3: test coverage and independent review

- What I needed to understand: How to build meaningful workflow, queue, and reporting regression coverage without changing implementation behavior or mutating queue inputs.
- Actual AI-assisted task/discussion: Review PR #5's `workflow.py` and `reports.py`, add separate Engineer B tests, and submit focused GitHub review feedback.
- AI explanation / reasoning used: Cover valid and invalid state transitions, trimmed/reassigned staff, open-only queue filtering, stable numeric priority ties, non-mutating queue operations, and complete report buckets including zero counts.
- Verification performed in the project: Added ten `unittest` cases in `tests/test_engineer_b.py`; PR #5 contains Engineer B's review comment; PR #6 records corrections and a passing GitHub Actions run.
- Actual output / reference: commit `efd8f187` (initial tests), commit `a6867e4` (improvements), PR #5 https://github.com/oko-victor/Project-CampusFlow/pull/5 and PR #6 https://github.com/oko-victor/Project-CampusFlow/pull/6.
- Decision: Kept Engineer B regression tests in a separate branch/PR for reciprocal review and corrected weak assertions when review found gaps.
- What this demonstrates: Peer review and CI provide useful evidence, but do not replace personally understanding and checking the tests.
- Personal experiment: **Not recorded as run locally by Engineer B**. Engineer B must personally run the suite, record its output, and confirm their own understanding.

## Final evidence still required

Each engineer should personally confirm that these are genuine learning experiences, record three personally verified experiments and their actual outputs, and approve the other's final changes. Do not invent terminal results, personal actions, or approvals. Neither PR is authorized to merge by this log.
