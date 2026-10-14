# AI learning log

This log records actual AI-assisted engineering discussions and traceable code/review evidence. **Human learning and personally run experiments must be confirmed by the respective engineer; automated checks are identified as CI rather than personal experiments.** Do not treat this document alone as proof of individual understanding.

## Engineer A — three documented learning interactions (source-linked)

Engineer A has recorded three detailed AI-assisted learning drafts in [`docs/engineer-a-ai-learning.md`](https://github.com/oko-victor/Project-CampusFlow/blob/feat/rebuild-campusflow/docs/engineer-a-ai-learning.md) on `feat/rebuild-campusflow`. This shared index preserves the original source and does not misattribute AI-executed experiments as personal work.

1. **Python booleans and strict integer validation.** Compared `isinstance(True, int)` (True) with `type(True) is int` (False); applied strict positive-integer validation and tests in `campusflow/tickets.py` and `tests/test_tickets.py`.
2. **Priority rule precedence.** Explored why the `high`-urgency plus ten-users `critical` rule must precede the broader `high` rule, including boundary cases and an unrelated book-request classification example.
3. **No mutation on invalid creation.** Used a deep-copy snapshot to verify rejected ticket creation leaves the full collection unchanged, with a separate sample book-library demonstration.

**Evidence distinction:** The three Python demonstration outputs in Engineer A's source document were run by an AI assistant, not independently by Engineer A. Engineer A still needs to record their own questions, experiments, observations, and reflections. See the linked source for exact examples, results, code references, and checklist.

## Engineer B — Interaction 1: testing numeric ticket IDs

- What I needed to understand: Why sorting zero-padded ticket IDs as text works through T999 but fails when IDs expand to T1000.
- Actual AI-assisted task/discussion: Create regression tests for queue priority ordering and numeric ticket ID tie-breaking; an initial review suggested T002 and T010, but Engineer A later correctly identified T999 versus T1000 as the meaningful width-change boundary.
- AI explanation / reasoning used: Lexicographic comparison of equal-width zero-padded IDs (such as T002 and T010) already agrees with numeric order. When ID width grows at T1000, lexical order incorrectly places T1000 before T999. Converting the suffix to an integer avoids that bug.
- Verification performed in the project: First tested T001–T010, which did not distinguish lexical from numeric sorting. Corrected the test to create T001–T1000 at equal priority, reverse the input, assert the complete numeric order, and explicitly assert T999 precedes T1000.
- Actual output / reference: `tests/test_engineer_b.py::test_queue_priority_and_numeric_id_tie_break`; commits `a6867e4` (earlier insufficient boundary test) and the subsequent T999/T1000 correction on PR #6. The updated correction passed GitHub Actions: https://github.com/oko-victor/Project-CampusFlow/actions/runs/38650603923 (the earlier run https://github.com/oko-victor/Project-CampusFlow/actions/runs/38649092190 applied to the prior commit).
- Decision: Rejected the earlier AI-assisted claim that T002/T010 distinguishes lexical from numeric sorting. Adopted Engineer A's correction to test the T999/T1000 boundary.
- What this demonstrates: Zero-padding preserves lexical/numeric agreement only while ID widths match; meaningful boundary tests must expose the actual failure mode.
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
